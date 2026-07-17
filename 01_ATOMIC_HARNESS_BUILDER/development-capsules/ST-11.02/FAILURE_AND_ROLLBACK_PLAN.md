# Failure and rollback

All validation precedes commit. Injected or real commit failure leaves no plan,
receipt or command record. Rollback removes only the additive ST-11.02 source,
tests and stored in-memory state. Upstream invalidation makes the plan inactive but
does not mutate historical plan bytes or receipts. A changed plan requires a new
immutable identity and command.

