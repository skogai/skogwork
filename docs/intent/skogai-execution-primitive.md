# SkogAI execution primitive

## Outcome

Provide the smallest useful execution primitive for SkogAI: start an agent turn,
continue its session, and return structured events through a provider-neutral
JSON-RPC interface.

## User

This is infrastructure for SkogAI. It is not intended as a general-purpose
replacement for Claude Code, Codex, Cowork, or their user interfaces.

## Why now

Claude Code and Codex already provide the same essential interaction shape:
submit a turn, continue a session, and receive structured output. SkogAI can
normalize that shape without creating another agent runtime.

The need is practical. Small tasks must not inherit large, opaque system prompts,
tool catalogs, or unsafe filesystem scope merely because those happen to be the
defaults of a larger agent environment.

## Success

- The complete base configuration is static, lean, and inspectable.
- Every tool, skill, connector, permission, and instruction added to the base is
  an active choice.
- Configuration overlays resolve predictably and the resolved configuration can
  be displayed before execution.
- Claude and Codex can be used through the same small SkogAI JSON-RPC boundary.
- A basic turn and a continued session require no SkogAI-owned agent loop.

## Constraint

Reuse each provider's agent loop, authentication, tools, and transcript or
session machinery. SkogAI owns configuration resolution, invocation, and the
normalization of structured events.

Start from nothing and add capabilities only when SkogAI has a demonstrated need
for them.

## Current prototype

`skogwork` proves the Claude path with the smallest useful consumer. Its REPL is
essentially a convenience over an initial `claude "hello"` followed by
`claude --continue "now we have a session"`. The REPL is verification plumbing,
not the product boundary.

Codex is another provider adapter. SkogAI JSON-RPC is the stable boundary above
both providers.

## Out of scope

- Replacing or recreating Claude Code, Codex, or their agent runtimes.
- Growing the REPL into a substantial standalone product.
- Inheriting capabilities merely because a provider or local installation makes
  them available.
- Moving provider-owned authentication, tools, or transcript storage into
  SkogAI.
