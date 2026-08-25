# AGENTS.md

## What this is

skogwork is a local, terminal-only reimplementation of Cowork built on the Codex Agent SDK: an
agent REPL with real file tools, skill discovery, MCP connectors, and persistent session history —
no JS, no browser, no daemon. It's a thin orchestration layer; nearly all agent behavior comes from
`claude_agent_sdk` (`ClaudeSDKClient` / `query`), not from code in this repo.

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
