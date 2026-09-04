# CLAUDE.md

## Current objective

> we take a regular claude code cli (like the one you have) and we tweak it so it actually goes
> quicker, actually can focus, listen and reason. help me set up a testing setup where we
> essentially can test every combination of settings and make a framework for
> claude-code-settings in general.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

skogwork is a local, terminal-only reimplementation of Cowork built on the Claude Agent SDK: an
agent REPL with real file tools, skill discovery, MCP connectors, and persistent session history —
no JS, no browser, no daemon. It's a thin orchestration layer; nearly all agent behavior comes from
`claude_agent_sdk` (`ClaudeSDKClient` / `query`), not from code in this repo.

The goal of the repo is *not* to build a Claude Code harness replica. Instead it builds what's
needed, when it's needed, adding complexity deliberately rather than fighting against Claude Code's
~600,000 lines of JavaScript to do what's needed. It's meant to stay a lean, personal way to run
Claude Code — deliberately scoped to the features actually needed, not a general-purpose Cowork
replacement.

Cowork's four moving parts, run locally from a terminal:

| Cowork | skogwork |
| --- | --- |
| agent loop + file tools | `ClaudeSDKClient` with `Read/Write/Edit/Bash/Glob/Grep` against real `cwd` |
| skills | filesystem discovery via `setting_sources = ["user", "project"]`, `skills = "all"` |
| connectors | `mcp_servers` from `config.toml` `[mcp.*]` and/or project `.mcp.json` |
| session history | session ids indexed per project dir in `~/.local/state/skogwork/sessions.json` |

No JS, no browser, no daemon. The Agent SDK bundles its own CLI; you only need Python.

### Glossary

**Bloat**: Any context, token, or compute spend a task didn't need — whether that's an app-shell
dependency (GUI, daemon, browser) or an oversized agent invocation for a subtask a cheaper path
could handle. Example: generating a commit message by loading the full agent (~85k tokens) instead
of feeding a local model just the diff (~4k tokens). *Avoid*: overhead, cruft.

**Delegation queue**: The mechanism by which skogwork's agent hands off a subtask it judges "quick"
to something outside its own main execution path. skogwork's responsibility ends at enqueueing — it
does not choose or manage where the task actually runs. *Avoid*: routing, offloading.

**Gateway router** (external, referenced only): The system, outside skogwork, responsible for
deciding where a delegated task actually executes (e.g. a local model, a cheaper hosted model).
skogwork enqueues to it but does not implement it.

## Docs mirrors

Two local doc mirrors back this file. Consult them before guessing at SDK/CLI behavior or reaching
for a workaround — skogwork's `config.py`/`cli.py`/`repl.py` only expose a subset of what's
available, so the answer to "can this do X" is usually in one of these, not in this repo's code.
When the two disagree or overlap, `docs/sdk/` wins for anything going through `ClaudeAgentOptions`
(that's what this repo actually calls); `docs/claude-code/` is the only source for CLI flags and
env vars, since the SDK docs don't cover those.

### `docs/sdk/` — Agent Sdk (Python/TypeScript) reference

The library this whole repo is a thin wrapper around (see "What this is" above).

- `overview.md`, `quickstart.md`, `python.md` — SDK basics, install, first client
- `agent-loop.md`, `streaming-vs-single-mode.md`, `streaming-output.md` — how `query()` /
  `ClaudeSDKClient` drive turns; relevant to `cli.py`/`repl.py`
- `permissions.md` — `tools` / `allowed_tools` / `disallowed_tools` / permission modes; the source
  of truth behind the "Config" and "Skills" sections below
- `skills.md` — skill discovery mechanics behind `setting_sources`
- `mcp.md` — MCP server wiring, relevant to `[mcp.*]` config and `.mcp.json` merging
- `subagents.md`, `custom-tools.md`, `hooks.md` — extension points not yet used in this repo
- `session-storage.md`, `sessions.md` — how the bundled CLI persists transcripts; relevant to
  `store.py`
- `structured-outputs.md`, `todo-tracking.md`, `tool-search.md`, `file-checkpointing.md`,
  `cost-tracking.md`, `observability.md` — feature areas not yet wired into skogwork; check here
  before building a custom version of any of them
- `troubleshooting.md`, `migration-guide.md` — when an SDK call errors or behaves unexpectedly
- `claude-code-features.md` — parity notes between the SDK and the full Claude Code CLI, useful for
  understanding what skogwork intentionally doesn't reimplement
- `secure-deployment.md`, `hosting.md`, `plugins.md`, `user-input.md`,
  `modifying-system-prompts.md`, `examples.md`, `typescript.md`, `typescript-v2-preview.md` — round
  out the rest; `typescript*.md` covers the JS/TS SDK and is background only, since this repo is
  Python-only

### `docs/claude-code/` — CLI / product reference

The full Claude Code CLI docs, useful for anything that's a CLI flag or env var rather than an SDK
option — the SDK reads Claude Code's underlying behavior (env vars, bundled tool defaults, task-tool
availability) but doesn't document it itself.

- `env-vars.md` — every env var Claude Code reads, including the ones worth setting in skogwork's
  `[env]` block (see "Settings deep dive" below)
- `cli-reference.md` — every CLI flag; useful as ground truth for what `ClaudeAgentOptions` fields
  actually map to, since the SDK is a thin wrapper over the same binary
- `features-overview.md` — the canonical "what costs context, and how much" breakdown by feature
- `permission-modes.md`, `settings-reference.md` — deeper detail than `docs/sdk/permissions.md` on
  mode edge cases and `settings.json` keys
- `headless.md` — `--bare`/`-p` behavior, relevant since skogwork's one-shot mode is conceptually
  the same as headless CLI usage
- `sub-agents.md`, `hooks.md`, `hooks-guide.md`, `skills.md`, `mcp.md` — CLI-level counterparts to
  the `docs/sdk/` pages of the same topic, with more product detail (e.g. built-in `Explore`/`Plan`
  agent behavior) than the SDK pages carry

## Install

```sh
uv tool install --from /path/to/skogwork skogwork
```

Or run from the source tree without installing:

```sh
uv run --directory /path/to/skogwork skogwork
```

Auth comes from the same place Claude Code gets it — an existing `claude` login.

## Commands

```sh
uv run --directory . skogwork              # run the REPL from source, no install
uv tool install --from . skogwork          # install the `skogwork` CLI
skogwork "one-shot prompt"                 # one-shot mode, prints and exits
skogwork -C <dir>                          # scope to another project dir
skogwork -c                                # resume latest session for this dir
skogwork -r <session-id>                   # resume a specific session
skogwork --config                          # print fully-resolved config and exit
skogwork --sessions                        # list recent sessions across all dirs
```

In the REPL: `/help`, `/model`, `/mode`, `/mcp`, `/skills`, `/tools`, `/new`, `/sessions`, `/cwd`,
`/quit`.

There is no build step, lint config, or test suite in this repo — verify changes by running the
CLI directly (`uv run --directory . skogwork ...`) and exercising the affected path. For config
changes specifically, use `skogwork --config` to see the fully-resolved output — it exercises the
real `config.py:load()` path (merge order, MCP `.mcp.json` merge, `${VAR}` expansion, the
`Skill`-append rule), which a standalone `tomllib`/`json` snippet does not. Reach for the project's
own commands before ad-hoc scripting.

## Config

`~/.config/skogwork/config.toml`, overridden by `<project>/.skogwork.toml`, overridden by CLI
flags. See `config.example.toml`.

- `permission_mode = "acceptEdits"` is the default here. Use `"plan"` for read-only
  reconnaissance, `"dontAsk"` to hard-deny anything outside the tool list.
- `[agent] tools` defaults to `["Skill"]` — a deliberately bare baseline, not the full
  `Read`/`Write`/`Edit`/`Bash`/... surface. Verified (via `skogwork --config` and one-shot probes
  through the real CLI, see "Settings deep dive" below) that `tools` genuinely restricts what the
  model can see, not just what it's pre-approved to call — with `tools=["Skill"]` the model reports
  zero built-in tools other than `Skill`. Uncomment entries in `config.example.toml` to build back up.
- Transcripts themselves live wherever the bundled CLI puts them; skogwork only indexes the ids
  so `-c` works.

## Skills

Drop a directory containing `SKILL.md` into either location:

```
~/.claude/skills/<name>/SKILL.md      # available everywhere
<project>/.claude/skills/<name>/SKILL.md
```

`setting_sources` must include `"user"` and/or `"project"` or nothing is discovered — that is the
single most common reason skills go missing. `/skills` in the REPL lists what actually loaded.

Note: `allowed-tools` in SKILL.md frontmatter is ignored by the SDK. Tool access is controlled by
`[agent]` config, split across three fields: `tools` restricts which tools are even loaded,
`allowed_tools` auto-approves a subset without a restriction, and `disallowed_tools` hard-vetoes
(including scoped rules like `Bash(rm *)`). See "Settings deep dive" below for the full breakdown.

## Settings deep dive

skogwork sits directly on `ClaudeAgentOptions` (not on `settings.json`), so the SDK's own dataclass
fields are the primary knob — env vars are secondary/fallback. This section covers what's specific
to skogwork: decisions actually made in `config.py`/`config.example.toml`, and empirical results
from probes run through the real `skogwork` binary that no doc can give you. For the underlying
mechanics it cites `docs/sdk/` and `docs/claude-code/` directly rather than re-explaining them —
check those before trusting a claim here that looks stale.

### Field semantics (verified against the resolved config, not just the docs)

`config.py` keeps three distinct fields, and `tools` — the restricting one — is wired through to
`ClaudeAgentOptions`:

| Field                                                                     | Effect                                                                                                                                                                                      |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_tools`                                                           | Auto-_approves_ the listed tools (skips the permission prompt). Anything not covered by `tools`/`disallowed_tools` is **still loaded into context** and still callable — it just falls through to `permission_mode`. |
| `disallowed_tools`                                                        | A bare name (`"Bash"`) removes that tool's definition from the request entirely. A scoped rule (`"Bash(rm *)"`) leaves the tool available and denies only matching calls, even under `bypassPermissions`. `"*"` removes everything.                                                                              |
| `tools` (`list[str] \| {"type":"preset","preset":"claude_code"} \| None`) | The actual tool-set selector — the SDK/CLI equivalent of `--tools "Bash,Edit,Read"`. This is what restricts what Claude _sees_, not just what it can do without asking.                     |

Source: `docs/sdk/permissions.md:65-97` (the allow/deny table). Confirmed live via `skogwork
--config`: `config.py` has a `tools: list[str] | None` field (`config.py:54`), separate from
`allowed_tools`/`disallowed_tools`, force-appends `"Skill"` when skills are enabled
(`config.py:164-165`), and passes straight through to `ClaudeAgentOptions(tools=...)`.

### Verified in practice: `tools` restriction confirmed through the real CLI

Ran two one-shot probes through the actual `skogwork` binary (`cli.py:main` → `one_shot()`, not a
script bypassing it) — a project-scoped `.skogwork.toml` per variant, same fixed prompt: _"Don't
call any tools. List every tool you have access to."_

- **`tools=["Skill"]`**: model reported *"I don't have access to any built-in tools... The only
  tools available to me are: Skill, mcp__skogmcp__..."* — confirms `tools` actually hides
  `Read`/`Write`/`Bash`/etc. from the model, not just gates approval.
- **`tools=` the old 11-item list**: model reported `Agent, Bash, Edit, Glob, Grep, Read, Skill,
  WebFetch, WebSearch, Write` — 10 of 11 configured tools surfaced (it under-reported
  `TodoWrite`/`Task`; treat self-reported tool lists as approximate, not authoritative). Note: on
  Sonnet 5 (this repo's likely default model — see the task-tracking-tools note below),
  `TodoWrite`/`Task*` wouldn't have loaded anyway without an opt-in env var, regardless of what's
  in `tools`.
- A separate direct-SDK probe (`tools=None` for true "unrestricted") only surfaced **11** tools,
  not the ~40-strong theoretical max of every built-in — several are feature-gated behind other
  config (plan mode, cron, tasks) and never load without their trigger, and
  `CLAUDE_CODE_DISABLE_ARTIFACT=1` in this repo's `env` block explicitly removes `Artifact`.
- Cache/context size (direct-SDK variant, since `skogwork`'s own CLI doesn't surface token usage):
  `tools=["Skill"]` → ~7.3k cache-creation tokens vs. `tools=None` → ~19.8k — roughly **2.7x** less
  context at session start from this one field alone.

**Known gap**: `render.py`'s `result()` method only prints `"N turns · X.Xs"` — `ResultMessage.usage`
(`input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`) and `total_cost_usd` are
available from the SDK but never surfaced. Confirming token cost differences currently requires a
standalone script driving `query()` directly.

Acted on this: `config.example.toml` (the shipped template) defaults `tools` to `["Skill"]` only —
the bare baseline this section recommends, with the old 11-item list commented out to build back up
from.

### The context-cost levers, by feature

Straight from `docs/claude-code/features-overview.md:206-213` (the "Context cost by feature" table):

| Feature           | Loads                                                | Context cost                                                     | Off switch                                                                    |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **CLAUDE.md**      | Session start, full content                          | Every request                                                        | `setting_sources=[]`, or per-source omission                                  |
| **Skills**         | Descriptions at start; full content when used         | Low; **zero** for a skill with `disable-model-invocation: true` until you invoke it | `skills=[]`, or `disable-model-invocation: true` per-skill                    |
| **MCP servers**    | Tool names at start; schemas deferred                 | Low until a tool is used (tool search is on by default)              | `mcp_servers={}` + `strict_mcp_config=True`                                   |
| **Subagents**      | On demand, when spawned                               | Isolated from the main session (own fresh context, doesn't accumulate) | Don't grant the `Agent` tool                                                  |
| **Hooks**          | On trigger                                            | Zero, unless the hook returns output added to the conversation       | Don't configure hooks                                                         |

**System prompt** isn't in that table but is the other big one: unset `system_prompt` gives the
SDK's minimal tool-calling-only prompt; the full `claude_code` preset (tool guidance, safety rules,
env context) is opt-in only. Source: `docs/sdk/modifying-system-prompts.md:15`.

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

Note: `setting_sources=[]` still doesn't stop everything — `~/.claude.json`, managed/policy
settings, and (unless you also set `strict_mcp_config=True` or `disableClaudeAiConnectors`)
claude.ai MCP connectors load regardless. For real isolation, `docs/sdk/claude-code-features.md:98-100`
explicitly recommends `setting_sources=[]` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`.

### Env vars worth wiring into skogwork's `env` map

All confirmed against `docs/claude-code/env-vars.md`.

**Tools / agents**

- `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` — drops every built-in subagent type (`Explore`,
  `Plan`, and the `general-purpose` fallback used when an `Agent` call omits `subagent_type`, which
  then fails with `subagent_type is required`). **Only applies in non-interactive mode (`-p`)**,
  i.e. skogwork's `cli.py:one_shot()` path — it has no effect on `repl.py`'s streaming
  `ClaudeSDKClient` sessions. For the REPL, use `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` instead
  (drops just `Explore`/`Plan`, works in interactive mode too; a custom subagent literally named
  `Explore` or `Plan` is unaffected).
- `ENABLE_TOOL_SEARCH` — `auto`/`auto:N`/`false`/`true`; controls whether MCP tool _schemas_ (not
  names) load upfront. Unset (the default) already defers all MCP tools. Matters once MCP servers
  are added back.

**Task-tracking tools (`TodoWrite`/`Task*`)**

- On Sonnet 5, Opus 4.8, Fable 5, Mythos 5+ (this session's own model family, and skogwork's likely
  default), **none** of `TodoWrite`/`TaskCreate`/`TaskGet`/`TaskUpdate`/`TaskList` load by default.
  Opt in with `CLAUDE_CODE_ENABLE_TODO_TOOLS=1`, or by naming one of them in
  `allowed_tools`/`tools`.
- `CLAUDE_CODE_ENABLE_TASKS` only picks *which* family you get once task-tracking tools are present
  at all: unset/default → the `Task*` tools; `CLAUDE_CODE_ENABLE_TASKS=0` → the legacy `TodoWrite`
  instead. It does not turn task-tracking off.
- skogwork's live default (`config.example.toml`) is `tools=["Skill"]` — neither family is in it
  today, so this whole knob is currently moot until `tools` is built back up.

**Memory / project context**

- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — stops the `~/.claude/projects/<project>/memory/`
  auto-memory read/write (the one input read even with `setting_sources=[]`). `=0` forces it *on*
  even when `--bare`/`CLAUDE_CODE_SIMPLE` or `autoMemoryEnabled: false` would otherwise disable it.

**Skills / commands**

- `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` — removes Claude Code's bundled skills/workflows entirely.
  Built-in commands like `/init` stay typable but hidden from the model; `/doctor` also stays
  typable (hide it separately with `DISABLE_DOCTOR_COMMAND`). Skills from plugins,
  `.claude/skills/`, `.claude/commands/` are unaffected.
- `DISABLE_DOCTOR_COMMAND=1` — hides `/doctor` (and its `/checkup` alias) from the model. Doesn't
  affect the `claude doctor` terminal diagnostics command.

**MCP**

- `ENABLE_CLAUDEAI_MCP_SERVERS=false` — blocks claude.ai connector auto-load (survives
  `setting_sources=[]`).

**Misc bloat/noise, not token-costly but worth knowing for a "nothing extra" baseline**

- `CLAUDE_CODE_DISABLE_ARTIFACT=1` — drops the `Artifact` tool; once set, no settings file can turn
  it back on (the settings-file equivalent is `enableArtifact: false`).
- `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` — turns off background agents/agent view (`claude agents`,
  `--bg`, `/background`, the on-demand supervisor).
- `DISABLE_AUTOUPDATER=1` — disables background auto-update; manual `claude update` still works.
  `DISABLE_UPDATES=1` is stricter and blocks manual updates too.
- `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING` — set to any non-empty value (including
  `0`/`false` — those still count as "set"). `DISABLE_TELEMETRY` also disables feature-flag
  fetching, which breaks Remote Control.
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` — one flag that bundles auto-updates, telemetry, error
  reporting, `/feedback`, release-notes checks, and a few other network calls.

**Thinking budget**

- `MAX_THINKING_TOKENS=0` disables extended thinking on the Anthropic API — **except** on
  adaptive-reasoning models (Sonnet 5, Fable, Opus 4.7+), where nonzero/zero values are ignored
  unless `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` is also set. Since skogwork likely defaults to a
  Sonnet 5-class model, `MAX_THINKING_TOKENS=0` alone will silently no-op — both vars are needed
  together.

### Reference point: what Anthropic itself calls "stripped"

Two CLI flags, confirmed via `docs/claude-code/cli-reference.md:71,123` and
`docs/claude-code/headless.md:62`:

- **`--bare`** (env equivalent: `CLAUDE_CODE_SIMPLE=1`): skips auto-discovery of hooks, skills,
  custom commands, subagents, plugins, MCP servers, auto memory, and CLAUDE.md. Leaves Bash + file
  read + file edit tools, plus a minimal system prompt. Explicitly _"the recommended mode for
  scripted and SDK calls, and will become the default for `-p` in a future release."_ Roughly
  `tools=["Bash","Read","Edit"]` + `setting_sources=[]` + `mcp_servers={}`.

  **Gotcha for skogwork specifically**: bare mode never reads OAuth credentials or the system
  keychain — it requires `ANTHROPIC_API_KEY` (or an `apiKeyHelper`). skogwork's "Install" section
  above says _"Auth comes from the same place Claude Code gets it — an existing `claude` login."_
  Those two are in direct tension: adopting `--bare`/`CLAUDE_CODE_SIMPLE` as the strip-down baseline
  would require adding API-key auth, not just trimming `tools`/`setting_sources` by hand as this
  section otherwise recommends.

- **`--safe-mode`** (env equivalent: `CLAUDE_CODE_SAFE_MODE=1`): opposite intent — keeps everything
  functional (auth, model selection, built-in tools, permissions all work normally) but disables all
  _customization_ sources (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents,
  output styles, workflows, themes, keybindings, status line, LSP, auto memory). Managed/policy
  settings still apply. Useful as an "is my config the problem" diagnostic, not as a token-savings
  mechanism.

**Bottom line for skogwork's `config.py`:** the `tools` (restrict) field, distinct from
`allowed_tools` (auto-approve), already exists, is verified (via `skogwork --config` and one-shot
probes through the real CLI) to actually restrict what the model sees, and defaults to `["Skill"]`
in `config.example.toml` as the bare starting point. Remaining gap: `render.py` doesn't surface
`ResultMessage.usage`/`total_cost_usd`, so quantifying the token savings of any given `tools`
combination still requires a standalone script rather than the CLI itself.

## Architecture

Four files, each owning one concern, wired together in `cli.py:main`:

- **`config.py`** — resolves a `Config` dataclass by layering `~/.config/skogwork/config.toml` →
  `<project>/.skogwork.toml` → CLI-flag overrides (see `load()`). MCP servers are merged from
  project `.mcp.json` (Claude Code's own format) and `[mcp.*]` TOML tables, with `${VAR}` expansion
  in env/headers so secrets stay out of the file. `Config.to_options_kwargs()` is the single
  translation point into `ClaudeAgentOptions` kwargs — any new SDK option that needs surfacing goes
  through here.
- **`cli.py`** — argument parsing and the one-shot path (`one_shot()`), which drives the SDK's
  stateless `query()` and streams messages into `StreamRenderer`. Also home to `_explain()`, which
  turns common SDK exceptions (missing CLI, auth failure) into actionable terminal messages instead
  of raw tracebacks.
- **`repl.py`** — the interactive loop (`Repl` class), built on the stateful `ClaudeSDKClient`
  (connect once, `query()`/`receive_response()` per turn). Slash commands are dispatched in
  `Repl.command()`; add new ones there and to the `SLASH`/`HELP` constants at the top of the file so
  completion and `/help` stay in sync.
- **`store.py`** — a flat JSON index (`~/.local/state/skogwork/sessions.json`) mapping session id →
  project cwd, used only so `-c`/`--sessions` work without shelling out to the CLI. It does not own
  transcripts — those live wherever the bundled Claude Code CLI puts them.
- **`render.py`** — turns the SDK's streamed message types (`StreamEvent`, `AssistantMessage`,
  `ResultMessage`, etc.) into terminal output. Text deltas print raw as they stream; tool calls
  render as dim one-liners via `tool_headline()`, which picks a headline field per tool name from
  `_HEADLINE_KEY`. Both `cli.one_shot()` and `repl.Repl.turn()` funnel the same SDK message stream
  through this module, so rendering logic belongs here, not duplicated in the callers.

Both entry points (one-shot and REPL) consume the same `Config` and the same SDK message stream —
if you change how a message type is handled, check whether both `cli.py` and `repl.py` need the fix
or whether it belongs in the shared `render.py`.

## Key behaviors to preserve

- Skill discovery requires `setting_sources` to include `"user"` and/or `"project"` — this is
  called out above as the most common way skills silently go missing.
- `allowed-tools` in a skill's `SKILL.md` frontmatter is ignored by the SDK; tool access is
  controlled by `[agent] tools` (restricts), `allowed_tools` (auto-approves), and
  `disallowed_tools` (vetoes) in config — not by any single one of them.
- When an explicit tool list is configured, `config.load()` force-appends `"Skill"` if skills are
  enabled — don't reintroduce a path where skills are configured but the `Skill` tool is missing.
