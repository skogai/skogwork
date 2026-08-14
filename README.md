# skogwork

Cowork's four moving parts, run locally from a terminal:

| Cowork | skogwork |
| --- | --- |
| agent loop + file tools | `ClaudeSDKClient` with `Read/Write/Edit/Bash/Glob/Grep` against real `cwd` |
| skills | filesystem discovery via `setting_sources = ["user", "project"]`, `skills = "all"` |
| connectors | `mcp_servers` from `config.toml` `[mcp.*]` and/or project `.mcp.json` |
| session history | session ids indexed per project dir in `~/.local/state/skogwork/sessions.json` |

No JS, no browser, no daemon. The Agent SDK bundles its own CLI; you only need Python.

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

## Config

`~/.config/skogwork/config.toml`, overridden by `<project>/.skogwork.toml`,
overridden by CLI flags. See `config.example.toml`.

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

## Notes

- `permission_mode = "acceptEdits"` is the default here. Use `"plan"` for read-only
  reconnaissance, `"dontAsk"` to hard-deny anything outside the tool list.
- Transcripts themselves live wherever the bundled CLI puts them; skogwork only
  indexes the ids so `-c` works.
