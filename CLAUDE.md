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
  through the real CLI, see `SETTINGS.md`) that `tools` genuinely restricts what the model can see,
  not just what it's pre-approved to call — with `tools=["Skill"]` the model reports zero built-in
  tools other than `Skill`. Uncomment entries in `config.example.toml` to build back up.
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
(including scoped rules like `Bash(rm *)`). See `SETTINGS.md` for the full breakdown.

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
