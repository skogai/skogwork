# Architecture record rules

## Features

- Describe one user-visible or caller-visible outcome.
- Express scenarios as given, when, then observations.
- Name expected owners, files, and authoritative context.
- Separate deterministic contract verification from live provider verification.
- Use `proposed`, `implemented`, or `verified` status.

## Decisions

- Record only choices that constrain later work or cross an architectural boundary.
- State the problem, real alternatives, chosen option, and material consequences.
- Use `proposed`, `accepted`, or `superseded` status.
- Link a superseding record in the body instead of maintaining a separate registry.

## Context and ownership

- Load context through the matching owner in `ownership.toml`.
- Prefer the narrowest matching owner. Include multiple owners for genuine boundary changes.
- Keep `files` in records to expected impact, not an exhaustive dependency list.
- Recheck live files and tests. Records express intent and status, not proof by themselves.
