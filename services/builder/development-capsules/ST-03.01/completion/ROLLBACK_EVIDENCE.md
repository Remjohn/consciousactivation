# ST-03.01 Rollback Evidence

Verdict: `PASS`.

- Injected commit failure leaves zero question graph, package, receipt, event,
  command record, or observation intent.
- A governed invalidation clears the active package reference without deleting or
  mutating the historical graph, recommendation, package, receipt, or canonical bytes.
- Replaying the identical invalidation returns the original result without duplicate
  state; a conflicting command payload fails closed.
- Re-entry requires a new immutable package identity when definitions, evidence,
  dependency completion, saturation, or Draft Harness Model meaning changes.
- Source Lock, saturation, frozen boundary, human ratification and Draft Harness Model
  remain untouched by rollback.
