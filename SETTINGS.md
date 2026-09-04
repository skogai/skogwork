## Where the real leverage is

skogwork sits directly on `ClaudeAgentOptions` (not on `settings.json`), so the SDK's own dataclass fields are the primary knob — env vars are secondary/fallback. Here's what actually controls "how much stuff loads at session start."

This file only covers what's specific to skogwork: decisions actually made in `config.py`/`config.example.toml`, and empirical results from probes run through the real `skogwork` binary that no doc can give you. For the underlying mechanics, it now cites `docs/sdk/` (Agent SDK reference) and `docs/claude-code/` (CLI/product reference, added after this file was first written) directly rather than re-explaining them — check those before trusting a claim here that looks stale.

### Field semantics (verified against the resolved config, not just the docs)

skogwork's `CLAUDE.md` says _"tool access is controlled by `[agent] tools`..."_ `config.py` keeps three distinct fields, and `tools` — the restricting one — is wired through to `ClaudeAgentOptions`:

| Field                                                                     | Effect                                                                                                                                                                                      |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_tools`                                                           | Auto-_approves_ the listed tools (skips the permission prompt). Anything not covered by `tools`/`disallowed_tools` is **still loaded into context** and still callable — it just falls through to `permission_mode`. |
| `disallowed_tools`                                                        | A bare name (`"Bash"`) removes that tool's definition from the request entirely. A scoped rule (`"Bash(rm *)"`) leaves the tool available and denies only matching calls, even under `bypassPermissions`. `"*"` removes everything.                                                                              |
| `tools` (`list[str] \| {"type":"preset","preset":"claude_code"} \| None`) | The actual tool-set selector — the SDK/CLI equivalent of `--tools "Bash,Edit,Read"`. This is what restricts what Claude _sees_, not just what it can do without asking.                     |

Source: `docs/sdk/permissions.md:65-97` (the allow/deny table). Confirmed live via `skogwork --config`: `config.py` has a `tools: list[str] | None` field (`config.py:54`), separate from `allowed_tools`/`disallowed_tools`, force-appends `"Skill"` when skills are enabled (`config.py:164-165`), and passes straight through to `ClaudeAgentOptions(tools=...)`.

### Verified in practice: `tools` restriction confirmed through the real CLI

Ran two one-shot probes through the actual `skogwork` binary (`cli.py:main` → `one_shot()`, not a script bypassing it) — a project-scoped `.skogwork.toml` per variant, same fixed prompt: _"Don't call any tools. List every tool you have access to."_

- **`tools=["Skill"]`**: model reported *"I don't have access to any built-in tools... The only tools available to me are: Skill, mcp__skogmcp__..."* — confirms `tools` actually hides `Read`/`Write`/`Bash`/etc. from the model, not just gates approval.
- **`tools=` the old 11-item list**: model reported `Agent, Bash, Edit, Glob, Grep, Read, Skill, WebFetch, WebSearch, Write` — 10 of 11 configured tools surfaced (it under-reported `TodoWrite`/`Task`; treat self-reported tool lists as approximate, not authoritative). Note: on Sonnet 5 (this repo's likely default model — see the task-tracking-tools correction below), `TodoWrite`/`Task*` wouldn't have loaded anyway without an opt-in env var, regardless of what's in `tools`.
- A separate direct-SDK probe (`tools=None` for true "unrestricted") only surfaced **11** tools, not the ~40-strong theoretical max of every built-in — several are feature-gated behind other config (plan mode, cron, tasks) and never load without their trigger, and `CLAUDE_CODE_DISABLE_ARTIFACT=1` in this repo's `env` block explicitly removes `Artifact`.
- Cache/context size (direct-SDK variant, since `skogwork`'s own CLI doesn't surface token usage): `tools=["Skill"]` → ~7.3k cache-creation tokens vs. `tools=None` → ~19.8k — roughly **2.7x** less context at session start from this one field alone.

**Known gap**: `render.py`'s `result()` method only prints `"N turns · X.Xs"` — `ResultMessage.usage` (`input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`) and `total_cost_usd` are available from the SDK but never surfaced. Confirming token cost differences currently requires a standalone script driving `query()` directly.

Acted on this: `config.example.toml` (the shipped template) defaults `tools` to `["Skill"]` only — the bare baseline this section recommends, with the old 11-item list commented out to build back up from.

### The context-cost levers, by feature

Straight from `docs/claude-code/features-overview.md:206-213` (the "Context cost by feature" table, which didn't exist in this repo's doc mirror when this section was first written — it cited a nonexistent local `features-overview.md`; that's fixed now that `docs/claude-code/` is checked in):

| Feature           | Loads                                                | Context cost                                                     | Off switch                                                                    |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **CLAUDE.md**      | Session start, full content                          | Every request                                                        | `setting_sources=[]`, or per-source omission                                  |
| **Skills**         | Descriptions at start; full content when used         | Low; **zero** for a skill with `disable-model-invocation: true` until you invoke it | `skills=[]`, or `disable-model-invocation: true` per-skill                    |
| **MCP servers**    | Tool names at start; schemas deferred                 | Low until a tool is used (tool search is on by default)              | `mcp_servers={}` + `strict_mcp_config=True`                                   |
| **Subagents**      | On demand, when spawned                               | Isolated from the main session (own fresh context, doesn't accumulate) | Don't grant the `Agent` tool                                                  |
| **Hooks**          | On trigger                                            | Zero, unless the hook returns output added to the conversation       | Don't configure hooks                                                         |

**System prompt** isn't in that table but is the other big one: unset `system_prompt` gives the SDK's minimal tool-calling-only prompt; the full `claude_code` preset (tool guidance, safety rules, env context) is opt-in only. Source: `docs/sdk/modifying-system-prompts.md:15`.

### `ClaudeAgentOptions` fields to actually build the strip-down around

| Field              | Set to (bare)                                                                     | Then build up with                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `tools`            | `[]` or a short explicit list                                                     | Add tool names back one at a time                                                                                              |
| `setting_sources`  | `[]`                                                                              | Add `"project"`, `"user"`, `"local"` individually — each pulls in CLAUDE.md, rules, skills, hooks, settings.json for that scope |
| `system_prompt`    | leave unset (`None`)                                                              | Only set `{"type":"preset","preset":"claude_code"}` (+`append`) when you want the full CLI-equivalent behavior                  |
| `mcp_servers`      | `{}`                                                                              | Add servers explicitly; use `strict_mcp_config=True` to also block `.mcp.json`/claude.ai connectors from sneaking in            |
| `skills`           | `[]`                                                                              | `"all"` or an explicit name list once you want skill descriptions back                                                          |
| `agents`           | omit                                                                              | Define your own subagents explicitly instead of inheriting built-ins                                                            |
| `disallowed_tools` | `["*"]` if using `tools` isn't granular enough, or scoped rules like `Bash(rm *)` | Loosen per-tool                                                                                                                 |

Note: `setting_sources=[]` still doesn't stop everything — `~/.claude.json`, managed/policy settings, and (unless you also set `strict_mcp_config=True` or `disableClaudeAiConnectors`) claude.ai MCP connectors load regardless. For real isolation, `docs/sdk/claude-code-features.md:98-100` explicitly recommends `setting_sources=[]` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`.

### Env vars worth wiring into skogwork's `env` map

All confirmed against `docs/claude-code/env-vars.md` (not mirrored in this repo when this section was first written — several entries below were previously unverifiable or wrong for that reason; corrections called out explicitly).

**Tools / agents**

- `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` — drops every built-in subagent type (`Explore`, `Plan`, and the `general-purpose` fallback used when an `Agent` call omits `subagent_type`, which then fails with `subagent_type is required`). **Only applies in non-interactive mode (`-p`)**, i.e. skogwork's `cli.py:one_shot()` path — it has no effect on `repl.py`'s streaming `ClaudeSDKClient` sessions. For the REPL, use `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` instead (drops just `Explore`/`Plan`, works in interactive mode too; a custom subagent literally named `Explore` or `Plan` is unaffected).
- `ENABLE_TOOL_SEARCH` — `auto`/`auto:N`/`false`/`true`; controls whether MCP tool _schemas_ (not names) load upfront. Unset (the default) already defers all MCP tools. Matters once MCP servers are added back.

**Task-tracking tools (`TodoWrite`/`Task*`) — corrected**

The original version of this section claimed `CLAUDE_CODE_ENABLE_TASKS=0`/unset "keeps `TaskCreate/Get/List/Update` off... since `TodoWrite` is already in skogwork's default list." That was backwards and named the wrong variable. Per `docs/claude-code/env-vars.md`:

- On Sonnet 5, Opus 4.8, Fable 5, Mythos 5+ (this session's own model family, and skogwork's likely default), **none** of `TodoWrite`/`TaskCreate`/`TaskGet`/`TaskUpdate`/`TaskList` load by default. Opt in with `CLAUDE_CODE_ENABLE_TODO_TOOLS=1`, or by naming one of them in `allowed_tools`/`tools`.
- `CLAUDE_CODE_ENABLE_TASKS` only picks *which* family you get once task-tracking tools are present at all: unset/default → the `Task*` tools; `CLAUDE_CODE_ENABLE_TASKS=0` → the legacy `TodoWrite` instead. It does not turn task-tracking off.
- skogwork's live default (`config.example.toml`) is `tools=["Skill"]` — neither family is in it today, so this whole knob is currently moot until `tools` is built back up.

**Memory / project context**

- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — stops the `~/.claude/projects/<project>/memory/` auto-memory read/write (the one input read even with `setting_sources=[]`). `=0` forces it *on* even when `--bare`/`CLAUDE_CODE_SIMPLE` or `autoMemoryEnabled: false` would otherwise disable it.

**Skills / commands**

- `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` — removes Claude Code's bundled skills/workflows entirely. Built-in commands like `/init` stay typable but hidden from the model; `/doctor` also stays typable (hide it separately with `DISABLE_DOCTOR_COMMAND`). Skills from plugins, `.claude/skills/`, `.claude/commands/` are unaffected.
- `DISABLE_DOCTOR_COMMAND=1` — hides `/doctor` (and its `/checkup` alias) from the model. Doesn't affect the `claude doctor` terminal diagnostics command.

**MCP**

- `ENABLE_CLAUDEAI_MCP_SERVERS=false` — blocks claude.ai connector auto-load (survives `setting_sources=[]`).

**Misc bloat/noise, not token-costly but worth knowing for a "nothing extra" baseline**

- `CLAUDE_CODE_DISABLE_ARTIFACT=1` — drops the `Artifact` tool; once set, no settings file can turn it back on (the settings-file equivalent is `enableArtifact: false`).
- `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` — turns off background agents/agent view (`claude agents`, `--bg`, `/background`, the on-demand supervisor).
- `DISABLE_AUTOUPDATER=1` — disables background auto-update; manual `claude update` still works. `DISABLE_UPDATES=1` is stricter and blocks manual updates too.
- `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING` — set to any non-empty value (including `0`/`false` — those still count as "set"). `DISABLE_TELEMETRY` also disables feature-flag fetching, which breaks Remote Control.
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` — one flag that bundles auto-updates, telemetry, error reporting, `/feedback`, release-notes checks, and a few other network calls.

**Thinking budget**

- `MAX_THINKING_TOKENS=0` disables extended thinking on the Anthropic API — **except** on adaptive-reasoning models (Sonnet 5, Fable, Opus 4.7+), where nonzero/zero values are ignored unless `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` is also set. Since skogwork likely defaults to a Sonnet 5-class model, `MAX_THINKING_TOKENS=0` alone will silently no-op — both vars are needed together.

### Reference point: what Anthropic itself calls "stripped"

Two CLI flags, now confirmed via `docs/claude-code/cli-reference.md:71,123` and `docs/claude-code/headless.md:62` (previously unverifiable — no local doc mentioned either flag):

- **`--bare`** (env equivalent: `CLAUDE_CODE_SIMPLE=1`): skips auto-discovery of hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory, and CLAUDE.md. Leaves Bash + file read + file edit tools, plus a minimal system prompt. Explicitly _"the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."_ Roughly `tools=["Bash","Read","Edit"]` + `setting_sources=[]` + `mcp_servers={}`.

  **Gotcha for skogwork specifically**: bare mode never reads OAuth credentials or the system keychain — it requires `ANTHROPIC_API_KEY` (or an `apiKeyHelper`). skogwork's own `CLAUDE.md` says _"Auth comes from the same place Claude Code gets it — an existing `claude` login."_ Those two are in direct tension: adopting `--bare`/`CLAUDE_CODE_SIMPLE` as the strip-down baseline would require adding API-key auth, not just trimming `tools`/`setting_sources` by hand as this file otherwise recommends.

- **`--safe-mode`** (env equivalent: `CLAUDE_CODE_SAFE_MODE=1`): opposite intent — keeps everything functional (auth, model selection, built-in tools, permissions all work normally) but disables all _customization_ sources (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents, output styles, workflows, themes, keybindings, status line, LSP, auto memory). Managed/policy settings still apply. Useful as an "is my config the problem" diagnostic, not as a token-savings mechanism.

**Bottom line for skogwork's `config.py`:** the `tools` (restrict) field distinct from `allowed_tools` (auto-approve) already exists, is verified (via `skogwork --config` and one-shot probes through the real CLI) to actually restrict what the model sees, and defaults to `["Skill"]` in `config.example.toml` as the bare starting point. The task-tracking env var entry above was wrong in the original version of this file and has been corrected. Remaining gap: `render.py` doesn't surface `ResultMessage.usage`/`total_cost_usd`, so quantifying the token savings of any given `tools` combination still requires a standalone script rather than the CLI itself.
