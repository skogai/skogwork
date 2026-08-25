---
title: introduction to skogwork
permalink: skogwork/skogai
type: router
---

<routes>

- @config.toml.

</routes>

<what_is_this>

skogwork is a local, terminal-only reimplementation of cowork built on the codex agent sdk: an
agent repl with real file tools, skill discovery, mcp connectors, and persistent session history —
no js, no browser, no daemon. it's a thin orchestration layer; nearly all agent behavior comes from
`claude_agent_sdk` (`claudesdkclient` / `query`), not from code in this repo.

the goal of the repo is _not_ to build a claude code harness replica! but instead creating what we need, when we need it and build by adding complexity and not fighting against claude codes 600.000 rows of javascript to do what is needed.

it will simply become a lean, personal way to run claude code — deliberately scoped to the features actually needed, not a general-purpose cowork replacement.

cowork's four moving parts, run locally from a terminal:

| cowork                  | skogwork                                                                           |
| ----------------------- | ---------------------------------------------------------------------------------- |
| agent loop + file tools | `claudesdkclient` with `read/write/edit/bash/glob/grep` against real `cwd`         |
| skills                  | filesystem discovery via `setting_sources = ["user", "project"]`, `skills = "all"` |
| connectors              | `mcp_servers` from `config.toml` `[mcp.*]` and/or project `.mcp.json`              |
| session history         | session ids indexed per project dir in `~/.local/state/skogwork/sessions.json`     |

no js, no browser, no daemon. the agent sdk bundles its own cli; you only need python.

</what_is_this>

<glossary>

## Language

**Bloat**:
Any context, token, or compute spend a task didn't need — whether that's an app-shell dependency (GUI, daemon, browser) or an oversized agent invocation for a subtask a cheaper path could handle. Example: generating a commit message by loading the full agent (~85k tokens) instead of feeding a local model just the diff (~4k tokens).
_Avoid_: overhead, cruft

**Delegation queue**:
The mechanism by which skogwork's agent hands off a subtask it judges "quick" to something outside its own main execution path. skogwork's responsibility ends at enqueueing — it does not choose or manage where the task actually runs.
_Avoid_: routing, offloading

**Gateway router** (external, referenced only):
The system, outside skogwork, responsible for deciding where a delegated task actually executes (e.g. a local model, a cheaper hosted model). skogwork enqueues to it but does not implement it.

<glossary>

<usage>

## Install

```sh
uv tool install --from /path/to/skogwork skogwork
```

Or run from the source tree without installing:

```sh
uv run --directory /path/to/skogwork skogwork
```

Auth comes from the same place Claude Code gets it — an existing `claude` login.

## Use

```sh
skogwork                       # REPL in the current directory
skogwork -C ~/git/skogai       # REPL scoped to another project
skogwork -c                    # resume the last session for this directory
skogwork -r 1f2e3d4c           # resume a specific session
skogwork "audit .zshrc for dead config"   # one-shot, prints and exits
skogwork --sessions            # list recent sessions across all directories
skogwork --config              # dump resolved options and exit
```

In the REPL: `/help`, `/model`, `/mode`, `/mcp`, `/skills`, `/tools`,
`/new`, `/sessions`, `/cwd`, `/quit`.

</usage>

<configuration>

## Config

`~/.config/skogwork/config.toml`, overridden by `<project>/.skogwork.toml`,
overridden by CLI flags. See `config.example.toml`.

</configuration>

<tools>

## Skills

Drop a directory containing `SKILL.md` into either location:

```
~/.claude/skills/<name>/SKILL.md      # available everywhere
<project>/.claude/skills/<name>/SKILL.md
```

`setting_sources` must include `"user"` and/or `"project"` or nothing is discovered —
that is the single most common reason skills go missing. `/skills` in the REPL lists
what actually loaded.

Note: `allowed-tools` in SKILL.md frontmatter is ignored by the SDK. Tool access is
controlled by `[agent] tools` only.

</tools>

<notes>

- `permission_mode = "acceptEdits"` is the default here. Use `"plan"` for read-only
  reconnaissance, `"dontAsk"` to hard-deny anything outside the tool list.
- Transcripts themselves live wherever the bundled CLI puts them; skogwork only
  indexes the ids so `-c` works.

</notes>

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

There is no build step, lint config, or test suite in this repo — verify changes by running the
CLI directly (`uv run --directory . skogwork ...`) and exercising the affected path.

## Architecture

Four files, each owning one concern, wired together in `cli.py:main`:

- **`config.py`** — resolves a `Config` dataclass by layering `~/.config/skogwork/config.toml` →
  `<project>/.skogwork.toml` → CLI-flag overrides (see `load()`). MCP servers are merged from
  project `.mcp.json` (Codex's own format) and `[mcp.*]` TOML tables, with `${VAR}` expansion
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
  transcripts — those live wherever the bundled Codex CLI puts them.
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
  called out in the README as the most common way skills silently go missing.
- `allowed-tools` in a skill's `SKILL.md` frontmatter is ignored by the SDK; tool access is
  controlled solely by `[agent] tools` in config.
- When an explicit tool list is configured, `config.load()` force-appends `"Skill"` if skills are
  enabled — don't reintroduce a path where skills are configured but the `Skill` tool is missing.
