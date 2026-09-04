## Where the real leverage is

skogwork sits directly on `ClaudeAgentOptions` (not on `settings.json`), so the SDK's own dataclass fields are the primary knob — env vars are secondary/fallback. Here's what actually controls "how much stuff loads at session start."

### Field semantics (verified against the resolved config, not just the docs)

skogwork's `CLAUDE.md` says _"tool access is controlled solely by `[agent] tools` in config."_ That prose reads as if `[agent] tools` were the only knob, but `config.py` actually keeps three distinct fields, and `tools` — the restricting one — is already wired through to `ClaudeAgentOptions`:

| Field                                                                     | Effect                                                                                                                                                                                      |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_tools`                                                           | Auto-_approves_ the listed tools (skips the permission prompt). Anything not covered by `tools`/`disallowed_tools` is **still loaded into context** and still callable — it just falls through to `permission_mode`. |
| `disallowed_tools`                                                        | A bare name (`"Bash"`) actually **removes that tool's definition** from the request. `"*"` removes everything.                                                                              |
| `tools` (`list[str] \| {"type":"preset","preset":"claude_code"} \| None`) | The actual tool-set selector — the SDK/CLI equivalent of `--tools "Bash,Edit,Read"`. This is what restricts what Claude _sees_, not just what it can do without asking.                     |

Confirmed live via `skogwork --config`: `config.py` already has a `tools: list[str] | None` field (`config.py:54`), separate from `allowed_tools`/`disallowed_tools`, force-appends `"Skill"` when skills are enabled (`config.py:164-165`, mirroring the `allowed_tools` append CLAUDE.md already documents), and passes straight through to `ClaudeAgentOptions(tools=...)`. That surface (`Agent`, `Artifact`, `AskUserQuestion`, `CronCreate/Delete/List`, `EndConversation`, `EnterPlanMode`, `EnterWorktree`, `ExitPlanMode`, `ExitWorktree`, `ListAgents`, `ListMcpResourcesTool`, `LSP`, `Monitor`, `NotebookEdit`, `PowerShell`, `PushNotification`, `ReadMcpResourceTool`, `RemoteTrigger`, `ReportFindings`, `ScheduleWakeup`, `SendMessage`, `SendUserFile`, `ShareOnboardingGuide`, `TaskCreate/Get/List/Update`, `ToolSearch`, `WaitForMcpServers`, `Workflow`, etc. — roughly 40 built-ins) is the *theoretical* max if `tools` were left unset entirely; `allowed_tools`/`disallowed_tools` layer on top of whatever `tools` leaves in for auto-approval and hard vetoes (including scoped ones like `Bash(rm *)`, which work even under `bypassPermissions`).

`CLAUDE.md`'s wording has been updated to spell out the three-field split instead of implying `[agent] tools` alone controls access.

### Verified in practice: `tools` restriction confirmed through the real CLI

Ran two one-shot probes through the actual `skogwork` binary (`cli.py:main` → `one_shot()`, not a script bypassing it) — a project-scoped `.skogwork.toml` per variant, same fixed prompt: _"Don't call any tools. List every tool you have access to."_

- **`tools=["Skill"]`**: model reported *"I don't have access to any built-in tools... The only tools available to me are: Skill, mcp__skogmcp__..."* — confirms `tools` actually hides `Read`/`Write`/`Bash`/etc. from the model, not just gates approval.
- **`tools=` the old 11-item list**: model reported `Agent, Bash, Edit, Glob, Grep, Read, Skill, WebFetch, WebSearch, Write` — 10 of 11 configured tools surfaced (it under-reported `TodoWrite`/`Task`; treat self-reported tool lists as approximate, not authoritative).
- A separate direct-SDK probe (same `config.py`/`to_options_kwargs()`, `tools=None` for true "unrestricted") only surfaced **11** tools, not the ~40-strong theoretical max above — several of those built-ins are feature-gated behind other config (plan mode, cron, tasks) and never load without their trigger, and `CLAUDE_CODE_DISABLE_ARTIFACT=1` in this repo's `env` block explicitly removes `Artifact`. So "~40 built-ins" is the outer bound, not what a bare unrestricted session actually shows.
- Cache/context size (via a direct-SDK variant of the same probe, since `skogwork`'s own CLI doesn't surface token usage — see gap below): `tools=["Skill"]` → ~7.3k cache-creation tokens vs. `tools=None` → ~19.8k — roughly **2.7x** less context at session start from this one field alone.

**Known gap**: `render.py`'s `result()` method only prints `"N turns · X.Xs"` — `ResultMessage.usage` (`input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`) and `total_cost_usd` are available from the SDK but never surfaced. Confirming token cost differences currently requires a standalone script driving `query()` directly; behavioral differences (what the model can see/do) are confirmable through the real CLI today.

Acted on this: `config.example.toml` (the shipped template) now defaults `tools` to `["Skill"]` only — the bare baseline this section recommends, with the old 11-item list left commented out to build back up from. `~/.config/skogwork/config.toml` was already set this way independently.

### The four biggest context-cost levers (from `features-overview.md`)

| Feature           | Loads                                            | Cost                                                                                                                                                                            | Off switch                                                                    |
| ----------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **System prompt** | Always                                           | `claude_code` preset is large (tool guidance, style rules, env context); the SDK's default when `system_prompt` is unset is a **minimal prompt** with just tool-calling support | Leave `system_prompt=None` for minimal; only opt into the preset deliberately |
| **CLAUDE.md**     | Session start, full content, every request       | Can be large; no on-demand loading                                                                                                                                              | `setting_sources=[]`, or per-source omission, or `claudeMdExcludes`           |
| **Skills**        | Descriptions at start (low), full content on use | Near-zero if `disable-model-invocation: true` or `skills=[]`                                                                                                                    | `skills=[]`                                                                   |
| **MCP servers**   | Tool names at start, schemas deferred            | Low with tool search on; can spike if `ENABLE_TOOL_SEARCH=false` or many `alwaysLoad` tools                                                                                     | `mcp_servers={}` + `strict_mcp_config=True`                                   |

Subagents and hooks are effectively free at session start (isolated context / external execution).

### `ClaudeAgentOptions` fields to actually build the strip-down around

| Field              | Set to (bare)                                                                     | Then build up with                                                                                                              |
| ------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `tools`            | `[]` or a short explicit list                                                     | Add tool names back one at a time                                                                                               |
| `setting_sources`  | `[]`                                                                              | Add `"project"`, `"user"`, `"local"` individually — each pulls in CLAUDE.md, rules, skills, hooks, settings.json for that scope |
| `system_prompt`    | leave unset (`None`)                                                              | Only set `{"type":"preset","preset":"claude_code"}` (+`append`) when you want the full CLI-equivalent behavior                  |
| `mcp_servers`      | `{}`                                                                              | Add servers explicitly; use `strict_mcp_config=True` to also block `.mcp.json`/claude.ai connectors from sneaking in            |
| `skills`           | `[]`                                                                              | `"all"` or an explicit name list once you want skill descriptions back                                                          |
| `agents`           | omit                                                                              | Define your own subagents explicitly instead of inheriting built-ins                                                            |
| `disallowed_tools` | `["*"]` if using `tools` isn't granular enough, or scoped rules like `Bash(rm *)` | Loosen per-tool                                                                                                                 |

Note: `settingSources: []` still doesn't stop everything — `~/.claude.json`, managed/policy settings, and (unless you also set `strict_mcp_config: true` or `disableClaudeAiConnectors`) claude.ai MCP connectors load regardless. For real isolation the docs explicitly recommend `setting_sources=[]` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`.

### Env vars worth wiring into skogwork's `env` map

Grouped by what they strip:

**Tools / agents**

- `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` — drops built-in subagent types (Explore, Plan). Non-interactive only.
- `ENABLE_TOOL_SEARCH` — `auto`/`auto:N`/`false`/`true`; controls whether tool _schemas_ (not names) load upfront. Matters once MCP servers are added back.

**Memory / project context**

- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — stops the `~/.claude/projects/<project>/memory/` auto-memory read/write (this is the one input that's read even with `setting_sources=[]`).

**Skills / commands**

- `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` — removes bundled skills/workflows entirely (not just hides them).
- `DISABLE_DOCTOR_COMMAND=1` — hides `/doctor` from the model too.

**MCP**

- `ENABLE_CLAUDEAI_MCP_SERVERS=false` — blocks claude.ai connector auto-load (survives `setting_sources=[]`).

**Misc bloat/noise, not token-costly but worth knowing for a "nothing extra" baseline**

- `CLAUDE_CODE_DISABLE_ARTIFACT=1`, `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` (kills `Artifact`, background-agent surface)
- `DISABLE_AUTOUPDATER=1`, `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- `CLAUDE_CODE_ENABLE_TASKS=0`/unset — keeps `TaskCreate/Get/List/Update` off in favor of nothing, since `TodoWrite` is already in skogwork's default list and the two are mutually exclusive-ish

**Thinking budget**

- `thinking` / `effort` fields (or `MAX_THINKING_TOKENS=0` via env) if extended thinking tokens matter for your budget.

### Reference point: what Anthropic itself calls "stripped"

Two CLI flags are useful mental models even though skogwork uses the SDK directly, not `claude -p`:

- **`--bare`**: skips hooks, skills, plugins, MCP, auto memory, CLAUDE.md; leaves only Bash + Read + Edit; explicitly _"the recommended mode for scripted and SDK calls."_ This is roughly `tools=["Bash","Read","Edit"]` + `setting_sources=[]` + `mcp_servers={}`.
- **`--safe-mode`**: opposite intent — keeps everything functional but disables all _customization_ sources (CLAUDE.md, skills, plugins, hooks, MCP, output styles, workflows, LSP, auto memory) for debugging a broken config, while built-in tools/permissions stay normal. Useful if you ever need "is my stripped-down config the problem" diagnostics.

**Bottom line for skogwork's `config.py`:** the `tools` (restrict) field distinct from `allowed_tools` (auto-approve) already exists, is verified (via `skogwork --config` and one-shot probes through the real CLI) to actually restrict what the model sees, and now defaults to `["Skill"]` in `config.example.toml` as the bare starting point. `CLAUDE.md`'s wording has been corrected to match. Remaining gap: `render.py` doesn't surface `ResultMessage.usage`/`total_cost_usd`, so quantifying the token savings of any given `tools` combination still requires a standalone script rather than the CLI itself.
