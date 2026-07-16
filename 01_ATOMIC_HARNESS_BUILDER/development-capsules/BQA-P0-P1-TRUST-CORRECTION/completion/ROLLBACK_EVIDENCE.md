# BQA P0/P1 Trust Correction Rollback Evidence

Verdict: `PASS`

The correction is additive validation and transaction behavior inside the exact
allowlist. It does not migrate a schema, database, external contract or persisted
production artifact.

Rollback and failure evidence:

- All five lifecycle operations were injected at the `events`, `checkpoint` and
  `command_record` transaction gates. Each of 15 failures retained the exact
  pre-command stream, checkpoint set and command-record set. The same governed
  command then completed once on clean retry.
- Ten concurrent same-version transaction races each retained one complete winner
  event and its matching receipt-bearing command record; the losing command left no
  state.
- Target-validation observation delivery failure occurs after the authoritative
  commit. The original result is never rolled back or relabeled. Pending delivery
  remains immutable and retryable; acknowledged observations are not duplicated.
- Invalid semantic authority, stale compiler authority and altered lineage fail
  before report, receipt, event, outbox or command-record persistence.
- ZIP replacement after the immutable read cannot change the descriptors derived
  from the verified buffer. Existing malformed/member/resource rejection tests pass.
- Existing invalidation and historical-reproduction suites pass unchanged inside
  both `600/600` full regressions.

If these source changes are reverted, no data migration or cleanup action is needed.
The separate correction and supersession receipts must remain as historical evidence;
they must not be rewritten to imply that the earlier audit never found the defects.
