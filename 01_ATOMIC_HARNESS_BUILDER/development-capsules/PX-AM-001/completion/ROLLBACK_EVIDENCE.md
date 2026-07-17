# PX-AM-001 Rollback Evidence

Verdict: `PASS`

- SQLite injects failure after record insertion and after receipt insertion; the
  enclosing `BEGIN IMMEDIATE` transaction rolls both back with zero partial state.
- Expected-version and duplicate-command conflicts commit no new rows.
- Portable export writes deterministic bytes to a sibling temporary file and uses
  atomic replacement only after complete validation. Injected failure before
  replacement preserves the prior package and removes the temporary file.
- Manifest and compilation validation failures occur before durable commit.
- Immutable earlier Story receipts and artifacts were not rewritten.
