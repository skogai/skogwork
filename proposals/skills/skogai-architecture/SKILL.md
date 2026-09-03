---
name: skogai-architecture
description: Maintain lean SkogAI architecture records from requested work or observed changes. Use when creating or updating feature definitions, recording durable architectural decisions, identifying responsible modules and expected context, or checking whether implementation and verification agree with documented intent.
---

# SkogAI Architecture

Keep architectural context small, live, and testable.

## Workflow

1. Inspect the requested action, completed action, or current diff.
2. Read `references/ownership.toml` and select only owners touched by the work.
3. Load the selected owners' `context` files. Treat them as authoritative over summaries.
4. Read `references/rules.md` and classify the record:
   - Feature: observable behavior that can be verified.
   - Decision: a durable choice with a meaningful alternative or tradeoff.
   - Neither: routine implementation detail already covered by a feature or decision.
5. Search existing records before creating one. Update the existing record when it describes the same behavior or choice.
6. Use `scripts/records.py` to create a record from the templates in `assets/`.
7. Replace every placeholder. Keep expected files narrow and verification concrete.
8. Run `scripts/records.py check <record>`.
9. Report affected owners, loaded context, record changes, and verification still required.

## Boundaries

- Treat ownership as responsibility and expected file scope, not permission to edit.
- Do not invent an owner when no mapping matches. Report the gap.
- Do not copy authoritative project context into the skill or a record. Link to the live file.
- Do not mark proposed decisions accepted or features verified without evidence.
- Do not create a decision for a reversible implementation detail.
- Do not infer that documentation proves runtime behavior.

## Commands

```sh
python .claude/skills/skogai-architecture/scripts/records.py new feature "Continue a session"
python .claude/skills/skogai-architecture/scripts/records.py new decision "Provider-owned sessions"
python .claude/skills/skogai-architecture/scripts/records.py check docs/features/continue-a-session.md
```
