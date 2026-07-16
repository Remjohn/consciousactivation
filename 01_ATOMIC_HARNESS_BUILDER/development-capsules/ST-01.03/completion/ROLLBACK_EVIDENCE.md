# ST-01.03 Rollback and invalidation evidence

Verdict: `PASS`.

An injected repository failure before the atomic commit left the run at stream version
5 with zero evidence indexes, zero evidence-index receipts, no Story command record
and no observation outbox. No partial state survived.

Non-destructive rollback was demonstrated after a valid commit. The active index
`evidence-index_8313ac3271f3cca92c998d9e523d5b443dcfac95347e75b174aad87c58e5e281`
was invalidated by
`evidence-index-invalidation_b826f6c559518eb68c54675f0255ab94539b3a6fd3701365c3a05074834cdd7e`.
The run records the invalidation, `active_evidence_index` returns none, and the exact
historical canonical bytes remain byte-identical and independently queryable.

Source Locks and specimens are never mutated. Replacement requires a new immutable
Source Lock and evidence-index identity. Observation failure after commit leaves
retryable intent and returns the committed receipt rather than a false failure.
