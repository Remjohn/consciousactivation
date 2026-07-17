# ST-03.02 Rollback Evidence

Verdict: `PASS`.

Injected atomic failure leaves zero answer, decision, amendment, memory, receipt,
event, command, or outbox state. Human-only reopening creates an immutable invalidation,
clears the active memory, records affected amendments and descendant decisions, and
preserves the original canonical bytes. Replayed reopen commands return the original
invalidation; conflicting payloads fail closed.
