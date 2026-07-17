# Failure and rollback

Validate all item evidence and authority before atomic commit. Failure leaves no
proposal, receipt or command record. Upstream invalidation disables active proposal
use without mutating historical bytes. Rollback removes only additive ST-11.03 code,
tests and in-memory state; no frozen authority or predecessor receipt is rewritten.

