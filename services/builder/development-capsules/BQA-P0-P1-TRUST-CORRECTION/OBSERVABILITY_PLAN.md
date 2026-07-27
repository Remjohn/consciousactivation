# Observability Plan

- Authority/semantic rejection records a typed finding code, command ID, run ID,
  candidate identity and authority-reference identities without secret or source payloads.
- Observation outbox exposes deterministic pending/delivered counts, command ID,
  receipt ID and retry result. It never emits `NOT_COMMITTED` after commit.
- Concurrency evidence records exactly one accepted command and one version conflict.
- Atomic run-command failure records failure before commit and proves zero event,
  checkpoint, receipt and command-record deltas.
- ZIP evidence records one candidate hash and member descriptor hashes derived from
  the same immutable buffer; archive bytes and local absolute paths are not logged.
- Supplemental receipts pin test results, original receipt hashes, changed-file hashes,
  rollback evidence and the final integration-gate verdict.

