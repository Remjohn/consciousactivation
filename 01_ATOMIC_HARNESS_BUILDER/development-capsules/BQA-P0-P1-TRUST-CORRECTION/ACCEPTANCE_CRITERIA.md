# Acceptance Criteria

## AC-01 — Authority-bound meaning

Given an active definition and all hash-pinned governed upstream artifacts, when
the definition is validated, then every semantic field and every section identity,
applicability, source reference and basis equals the independently reconstructed value.

## AC-02 — Forged-and-rehashed rejection

Given any governed semantic or section field is changed and the attacker recomputes
definition, receipt and report hashes, when validation is attempted, then the command
fails before report, receipt, event, observation-outbox or command-record commit.

## AC-03 — Actor authority

Given a self-consistent definition names an unknown, unauthorized, stale or different
compiler actor, when target validation begins, then authority validation fails closed
before state changes.

## AC-04 — Valid identity preservation

Given the exact existing governed inputs, when the corrected validator reconstructs
the definition, then valid canonical bytes, identities and receipts remain unchanged.

## AC-05 — Unambiguous post-commit observability

Given report, receipt, event, command record and observations commit atomically, when
the observation sink fails during delivery, then the caller receives the committed
receipt, pending delivery remains queryable, and no rejected or `NOT_COMMITTED` outcome
is emitted for that command.

## AC-06 — Deterministic observation retry

Given pending observations from a committed command, when delivery is retried, then
each observation is delivered at most once, the original receipt is returned on replay,
and no report, event, command record or acceptance decision is duplicated.

## AC-07 — Atomic same-version concurrency

Given two barrier-controlled writers use the same run and expected stream version,
when both attempt a commit, then exactly one succeeds, exactly one receives
`ConcurrencyConflict`, and the retained event and command record belong to the winner.

## AC-08 — Atomic run lifecycle command

Given create, transition, waiver, checkpoint or resume storage fails at any injected
boundary, when the command returns failure, then no event, checkpoint, receipt or
command record from that command exists and a clean retry succeeds once.

## AC-09 — ZIP byte binding

Given a ZIP path is replaced after its bytes are read, when the workspace calculates
candidate identity and descriptors, then both derive from the original immutable bytes;
the replacement archive cannot influence accepted descriptors.

## AC-10 — Security and failure preservation

Given malformed, oversized, traversing, colliding or otherwise prohibited ZIP input,
when byte-bound inspection runs, then every existing archive safety rule still fails closed.

## AC-11 — Scope and history

Given the correction completes, when file scope and receipts are audited, then only
allowlisted files changed, no dependency/schema/external repository changed, original
PASS receipts are byte-identical, and supplemental correction receipts reference them.

## AC-12 — Regression and integration gate

Given all five findings are corrected, when affected suites, architecture/failure tests,
two fresh full regressions and the synthetic integration gate run, then all tests pass,
all five findings are `CLOSED`, and the gate may become `PASS` without production or
certification claims.

