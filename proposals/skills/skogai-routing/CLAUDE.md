# skogai-routing (proposal)

## What this is

A skill for working with SkogAI "router" files — `SKOGAI.md`/`CLAUDE.md` files that use XML-ish
route tags and `@-file` links to point an agent at the right context (the pattern used in
`~/dot-skogai/knowledge/SKOGAI.md`, which has `<routes>`/`@file` tags and `<when_to_use>`
guidance). Per `SKILL.md`'s description, the intended scope is to **author, read, scaffold,
validate, list, and explain** these router files and their route tags — not just list XML tags,
which is all it currently does.

Live at `.claude/skills/skogai-routing` (a relative symlink → `../../proposals/skills/skogai-routing`,
so the real files live here). It's wired into this session already — `/reload-skills` picks it up.

## Current state (2026-09-04)

Only `list-xml-tags.sh` is actually invoked, from `SKILL.md`'s frontmatter body:

```
!`${CLAUDE_SKILL_DIR}/scripts/list-xml-tags.sh`
```

It walks `SKILL.md`, `workflows/`, `references/`, `templates/` under the skill's own root and prints
every XML tag found in each `.md` file. Two bugs fixed today, both in `scripts/list-xml-tags.sh`:

- Default search paths used to be resolved relative to the **caller's cwd**, not the skill's own
  directory — so invoking it via `${CLAUDE_SKILL_DIR}/...` from a different cwd (the real
  invocation shape) silently found nothing. Now resolved via `BASH_SOURCE`, so it works regardless
  of caller cwd and survives being reached through the `.claude/skills/` symlink.
- `find "$@"` used to error (and, under `set -euo pipefail`, kill the whole script) whenever any of
  the four default paths didn't exist — which is always, since this skill has no `workflows/`,
  `references/`, or `templates/` dirs. Now missing paths are filtered out before calling `find`.

Verified working via the real `/skogai-routing` slash command after these fixes.

Also cleaned up: `SKILL.md`'s frontmatter/body had accumulated three stacked debug attempts (bare
call, `sh ...`, a typo'd `bashsh ...`) plus a stray `Bash(...)` line that had leaked out of the
`allowed-tools` frontmatter field into the body. Reduced back to one working invocation.

Committed in `be409c8` (on top of the skill's initial commit `22f295b`).

## What's not built yet

- **`parse-frontmatter.sh`** and **`validate-schema.sh`** exist in `scripts/` but nothing in
  `SKILL.md` calls them yet — they're unwired.
- **`validate-schema.sh` needs a `schemas/` directory** (`*.schema.json` files) and a
  **`scripts/_validate_file.py`** helper. Neither exists. Running it as-is fails immediately with
  `schemas dir not found`.
- No `workflows/`, `references/`, or `templates/` directories yet (the scripts already anticipate
  them defensively).
- Scaffolding, validating, explaining, and `@`-link-following are all still just words in the
  `description` field — only "list the XML tags in this skill's own files" is real.
- `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/list-xml-tags.sh *)` in `SKILL.md` frontmatter is
  a no-op under skogwork specifically (skogwork's Agent SDK path ignores `allowed-tools` in
  frontmatter entirely — see repo-root `CLAUDE.md`). It only matters if this skill is later run
  under the full Claude Code CLI instead of skogwork.

## Tests

`scripts/list-xml-tags.bats` — a `bats` regression suite (10 tests) pinning down both fixes above
(cwd-independence, missing default dirs), symlink-indirection (mirrors the `.claude/skills` →
`proposals/skills` setup), tag-extraction correctness (dedup, attribute stripping), sorted
multi-file output, the empty-match exit-0/no-output case, and a `shellcheck` pass. All 10 currently
pass.

`bats` isn't on this machine's default `PATH` — it's installed via `mise` (see
`~/.config/mise/config.toml`), so it's a real project dependency now, not implicit. Run it with:

```sh
mise exec bats -- bats proposals/skills/skogai-routing/scripts/list-xml-tags.bats
```

(or plain `bats ...` if your shell has mise's shims activated).

## Related, not yet connected

`proposals/skills/skogai-architecture/` is a **separate** proposal (decision/feature record
authoring for `docs/adr/`, `docs/intent/`, `docs/features/`) — not symlinked into `.claude/skills/`,
not active. Don't conflate the two: `skogai-routing` is about router files (`SKOGAI.md`/`CLAUDE.md`
+ route tags), `skogai-architecture` is about ADR/feature records. They may eventually compose (a
router file could route to architecture records) but nothing ties them together today.

`~/dot-skogai/knowledge/SKOGAI.md` is the most mature real-world example of the router-file format
this skill is meant to eventually parse/scaffold/validate against — worth reading before designing
the schema(s) that `validate-schema.sh` will need.

## Suggested next step

Pick one real router file (e.g. this repo's own `CLAUDE.md`, or `~/dot-skogai/knowledge/SKOGAI.md`)
and design the first `schemas/*.schema.json` against it, then write the minimal
`scripts/_validate_file.py` to make `validate-schema.sh` actually run — that unblocks "validate"
being real instead of aspirational.
