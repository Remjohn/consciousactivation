# Operator Gate Sequence

## Gate 0 — Authorize evidence sweep

Required input: repository checkout and current authorities available.

Accept CA-CSR-01 only when its evidence packet is reproducible and limitations are recorded.

## Gate 1 — Accept current-state reconciliation

Required input: CA-CSR-01 evidence packet.

Accept CA-CSR-02 only when each material subsystem has an explicit status and each verified claim traces to repository evidence.

## Gate 2 — Authorize PRD synchronization

Required input: accepted CA-CSR-02 ledger/report.

Accept CA-CSR-03 only when the proposed PRD diff is supported by that ledger and preserves unresolved states/history.

## Gate 3 — Freeze the synchronized state

Required input: updated PRD plus CA-CSR-02 ledger.

Accept CA-CSR-04 only when an independent verifier confirms the PRD is an accurate representation of repository reality.

## Gate 4 — Separate authorization for runtime convergence

CA-CSR-04 does not authorize runtime work. Its output is a handoff. Any implementation program after this point requires its own approved PRD/Tech-Spec/mandate path.

## Hard stop conditions

A gate fails when:

- evidence is missing;
- a claim is based only on documentation;
- an implementation status is asserted without current executable proof;
- an authority conflict is silently resolved;
- the PRD claims more than the evidence supports;
- a mandate widens into runtime development;
- a requested operator decision is absent.
