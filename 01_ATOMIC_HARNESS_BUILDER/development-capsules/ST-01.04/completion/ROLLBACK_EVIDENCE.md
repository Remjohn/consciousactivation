# ST-01.04 Rollback and invalidation evidence

Verdict: `PASS`.

An injected repository failure before the atomic commit left the run at stream
version 6 with zero saturation evaluations, zero saturation receipts, no Story
command record and no observation outbox. No partial event or artifact survived.

Non-destructive rollback was demonstrated after a valid commit. The active evaluation
`saturation-evaluation_547928ca1fb29b930af299a5c33a86c5a69105ebc1429f0b6a7ee9293e4f5d91`
was invalidated by
`saturation-invalidation_82b9bad3b2ab121d5b505c6bb74755087ea21be7c10d902b4f897621bae7a37d`.
The run records the invalidation, `active_saturation_evaluation` returns none, and
the exact historical canonical bytes remain byte-identical and queryable.

Source Locks, Evidence Indexes and historical evaluations are never mutated.
Replacement requires a new immutable contract or evidence input and therefore a new
evaluation identity. Observation failure after commit leaves retryable intent and
returns the committed receipt rather than a false failure.
