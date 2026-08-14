# skogwork review

Review date: 2026-08-13

## Summary

skogwork is a good thin terminal wrapper around Claude Code, but it is not yet equivalent to Claude Cowork or Desktop. Its strongest quality is restraint: roughly 550 lines, clear modules, and direct use of the Claude Agent SDK instead of recreating an agent runtime.

The immediate priorities are secret redaction, project trust, safer defaults, and session-store hardening.

## Findings

### 1. Required: resolved configuration can disclose secrets

`skogwork --config` prints the entire resolved Agent SDK configuration after environment expansion. This can include MCP environment variables, authorization headers, tokens, and the general subprocess environment.

Relevant code:

- `skogwork/cli.py:114`
- `skogwork/config.py:111`
- `skogwork/config.py:153`

Recommended change: redact secrets or print only non-sensitive configuration shape.

### 2. Required: project configuration can introduce executable commands

Starting skogwork in a repository loads `.skogwork.toml` and `.mcp.json`, then passes configured local MCP commands to the SDK. A malicious cloned repository could consequently request execution of an arbitrary MCP command before ordinary agent tool permissions provide meaningful protection.

Relevant code:

- `skogwork/config.py:93`
- `skogwork/config.py:125`

Recommended change: require explicit project trust before loading executable project configuration.

### 3. Required: the default permission profile is broad

The default combines `acceptEdits` with `Write`, `Edit`, and `Bash`. This is convenient for a trusted personal workspace, but unsafe as a general desktop-style default.

Relevant code:

- `skogwork/config.py:33`
- `skogwork/config.py:53`

Recommended change: add a first-run permission explanation or choose a safer initial mode.

### 4. Required: prompt history needs an explicit privacy model

Complete prompt history is written locally, while the first 120 characters of each initial prompt are also stored in `sessions.json`. There is no documented retention control, private mode, or explicit file-permission enforcement.

Relevant code:

- `skogwork/repl.py:61`
- `skogwork/store.py:72`

Recommended change: document storage and retention, enforce private file modes, and consider a no-history mode.

### 5. Correctness: a damaged session index can be silently replaced

Malformed session JSON is treated as an empty index. The next successful write can then replace the damaged index, losing all existing entries.

Relevant code:

- `skogwork/store.py:33`

Recommended change: preserve the damaged file and report the error instead of silently returning an empty list.

### 6. Correctness: concurrent processes can lose session-index updates

Every process uses the same `sessions.json.tmp`, with no locking. Two skogwork instances can overwrite each other's updates or collide during replacement.

Relevant code:

- `skogwork/store.py:42`

Recommended change: serialize writes with a file lock and use process-specific temporary files.

### 7. Maintenance: reproducibility and automated verification are missing

There is no test suite or lockfile, and the core SDK dependency has only a lower version bound. A future SDK release can change behavior during installation. The repository also tracks compiled `__pycache__` files despite having a `.gitignore`.

Recommended changes:

- Add focused tests for configuration precedence, redaction, session corruption, concurrent writes, and CLI behavior.
- Commit a dependency lockfile for reproducible application installs.
- Stop tracking compiled Python files.

## Product assessment

### What it does well

- Clean, understandable separation between CLI, configuration, rendering, REPL, and storage.
- Reuses Claude Code sessions, skills, tools, MCP, and authentication instead of implementing incompatible equivalents.
- Covers useful one-shot and interactive terminal workflows.
- Uses simple, documented configuration precedence.
- Avoids an unnecessary daemon, browser shell, database, or custom agent protocol.

### What remains different from Cowork or Desktop

- No workspace trust or sandbox boundary.
- No visual artifact or document workflow.
- No connector authorization UI or lifecycle management.
- No permission-review interface beyond Claude Code modes.
- No searchable transcript UI, attachments, previews, or background-task management.
- Session storage is only an index over Claude Code's underlying transcripts.

## Verdict

Promising personal prototype. Changes are recommended before presenting it as a generally safe Cowork replacement.

The architecture is appropriately small and understandable. The principal risks are at trust boundaries rather than in the basic agent loop: secrets in diagnostic output, executable repository configuration, permissive defaults, and local history handling.

## Verification performed

- All Python modules compiled successfully.
- CLI help executed successfully.
- Configuration resolution completed successfully.
- A session-store smoke test passed.
- The installed virtual environment uses `claude-agent-sdk` 0.2.137.
- No automated test suite was present to run.
- No project or user skogwork configuration was present during the review.

The required global instruction file at `~/.Codex/memory/GLOBAL.md` was not present on this machine during the review.
