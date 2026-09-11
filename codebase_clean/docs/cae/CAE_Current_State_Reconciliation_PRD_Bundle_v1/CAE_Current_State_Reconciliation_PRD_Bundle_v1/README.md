# CAE Current-State Reconciliation & PRD Synchronization Mandate Bundle v1

This package is the controlled bridge between the repository's already-executed CAE work and the next implementation program.

It does not add a new architecture. It does not authorize runtime convergence. It establishes one evidence-backed current state and synchronizes `docs/PRD/CURRENT.md` to that state before the next build decision.

## Execution order

`CA-CSR-01 Evidence Sweep`
→ operator gate
→ `CA-CSR-02 Authority & Status Reconciliation`
→ operator gate
→ `CA-CSR-03 PRD Synchronization`
→ operator gate
→ `CA-CSR-04 Final Verification & Handoff`
→ operator authorization for a separate runtime-convergence program.

Run one mandate per Gemini session. The repository's authoritative mandate authoring protocol and Gemini execution skill govern every session.

## Why this is a brownfield control operation

The current repository already contains a substantial control plane, PostgreSQL/state foundation, Editorial Intelligence authority artifacts, executed mandate history, and multiple proven slices. The purpose of this program is to determine exactly what those artifacts prove today, reconcile contradictory or stale claims, and make the canonical PRD tell the truth about the current repository.

## Important non-goal

Do not create a second status system. Reuse the repository's existing `governance/program-control/03_PROGRAM_STATUS/` surfaces where possible. Create the scoped reconciliation directory only if the existing status surfaces cannot carry the required evidence packet without ambiguity.

## Authoritative sources

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/skills/EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`
- `docs/PRD/CURRENT.md`
- current `governance/program-control/03_PROGRAM_STATUS/*`
- current `docs/cae/editorial_intelligence/*`
- relevant Tech Specs, constitutions, mandate records, tests, receipts, and code

## Completion meaning

Completion means:

1. current repository evidence was inspected;
2. material claims were classified with evidence;
3. authority/status conflicts were preserved and routed;
4. the canonical PRD was updated from accepted evidence;
5. an independent final pass confirmed the result;
6. the next runtime-convergence program is still a separate operator-authorized step.
