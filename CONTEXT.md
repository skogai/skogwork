# skogwork

A lean, personal way to run claude code — deliberately scoped to the features actually needed, not a general-purpose Cowork replacement.

## Language

**Bloat**:
Any context, token, or compute spend a task didn't need — whether that's an app-shell dependency (GUI, daemon, browser) or an oversized agent invocation for a subtask a cheaper path could handle. Example: generating a commit message by loading the full agent (~85k tokens) instead of feeding a local model just the diff (~4k tokens).
_Avoid_: overhead, cruft

**Delegation queue**:
The mechanism by which skogwork's agent hands off a subtask it judges "quick" to something outside its own main execution path. skogwork's responsibility ends at enqueueing — it does not choose or manage where the task actually runs.
_Avoid_: routing, offloading

**Gateway router** (external, referenced only):
The system, outside skogwork, responsible for deciding where a delegated task actually executes (e.g. a local model, a cheaper hosted model). skogwork enqueues to it but does not implement it.
