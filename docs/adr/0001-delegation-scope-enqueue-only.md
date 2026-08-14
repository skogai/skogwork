# Delegation scope: skogwork enqueues, it does not route

skogwork's agent can judge a subtask "quick" and hand it off the main execution path via a **delegation queue** (agent-initiated; a manual/explicit trigger is a deferred future addition, not decided now). We decided skogwork's own responsibility stops at enqueueing — it does not select or manage a **gateway router** target itself (local model, cheaper hosted model, etc.). That decision lives entirely outside skogwork.

We considered embedding target selection directly (skogwork picks and calls the cheaper model itself), but rejected it: skogwork's core purpose is to stay lean and grow only from felt need, and model-selection/routing logic is a durable commitment skogwork hasn't needed yet. Keeping the boundary at "enqueue only" preserves that minimalism and avoids skogwork accumulating routing logic that belongs to a separate system.

## Consequences

- skogwork can add delegation without taking on the maintenance burden of tracking or evaluating delegation targets.
- Any future need to *choose* a target (not just enqueue) is a new decision, not an extension of this one — don't assume skogwork will naturally grow routing logic later.
