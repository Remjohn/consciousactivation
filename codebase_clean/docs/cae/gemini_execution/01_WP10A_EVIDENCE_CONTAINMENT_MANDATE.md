# Gemini Execution Mandate — Phase 01 / WP-10A

**Status:** `DRAFT FOR OPERATOR AUTHORIZATION`  
**Phase ID:** `WP-10A`  
**Title:** Vertical-Slice Evidence Containment and Acceptance  
**Execution classification:** Documentation, verification, and bounded staging reproduction only  
**Required gate on completion:** `OPERATOR_REVIEW`  
**This mandate does not authorize:** production change, authority cutover, schema design, migration, RLS change, runtime feature work, or CA-MAP-01.

## 1. Authority and purpose

This mandate applies the CAE Governance & Specification Bridge Bundle v3, especially the Implementation Gate, Reality-Contact Evaluation protocol, State and Transition Control protocol, State-Control Test and Proof protocol, and Phase 0 Object Constitution doctrine. It is governed by [the 12-phase execution program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md), [the current CAE control state](../implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md), and [the WP-00 through WP-09 evidence handoff](../implementation/CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md).

WP-10A exists to prevent a dangerous category error: interpreting a proven, bounded staging slice as a production-ready CAE architecture or as a repository-wide PostgreSQL cutover. The preceding work established brownfield findings, a Supabase/PostgreSQL staging foundation, typed first-slice transitions, inherited registry ingestion with quarantines, receipt lineage, E3 reality-contact countertests, and a read-only Interview Expression bridge. Those are valuable claims with defined evidence boundaries. They are not a license to infer that every CAE object, service, data source, user workflow, registry consumer, or semantic/taste claim is implemented.

The executing agent SHALL evaluate whether the recorded proof is reproducible at its stated fidelity and whether the records correctly distinguish proven claims, gaps, and non-claims. It SHALL not expand, repair, generalize, or replace the architecture merely because a later phase could benefit from doing so.

## 2. Mandatory reading before action

Before making a plan, changing any file, or executing a command beyond safe repository inspection, the agent SHALL read in full:

1. `docs/cae/gemini_execution/00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md`.
2. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
3. `docs/cae/implementation/CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md`.
4. `docs/cae/implementation/CAE_WP02A_FOUNDATION_PROOF.md`.
5. `docs/cae/implementation/CAE_WP03_SEMANTIC_OPERATION_PROOF.md`.
6. `docs/cae/implementation/CAE_WP04_REGISTRY_MIGRATION_PROOF.md`.
7. `docs/cae/implementation/CAE_WP07_EXECUTION_RECEIPTS_EVIDENCE_LINEAGE.md`.
8. `docs/cae/implementation/CAE_WP08_REALITY_CONTACT_AND_REWARD_HACKING.md`.
9. `docs/cae/implementation/CAE_WP09_FIRST_VERTICAL_RUNTIME_SLICE.md`.
10. `Conscious Activation Engine Brownfield/CAE_Governance_and_Specification_Bridge_Bundle_v3/CAE_Governance_and_Specification_Bridge_Bundle_v3/08_CAE_IMPLEMENTATION_GATE.md` and `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`.

The agent SHALL treat the implementation commits named in the handoff as immutable patch evidence. It SHALL inspect them with Git where required rather than relying on a prose summary alone.

## 3. Scope

The sole objective is to create an acceptance record for the following proposition:

> “WP-00 through WP-09 constitute bounded, reproducible brownfield evidence and one staging-proven vertical slice, with all limitations stated explicitly.”

The work SHALL:

- build a claim/non-claim matrix covering WP-00 through WP-09;
- identify each claim’s evidence location, exact commit, verifier, declared E0–E4 fidelity, and independent countertest where available;
- re-run static validators that do not mutate a database;
- inspect a selective sample of dynamic proof runners for their preconditions, rollback behavior, cleanup behavior, and false-proof checks;
- reproduce dynamic evidence only when the environment is explicitly confirmed as disposable staging and the runner’s guards prevent durable fixture residue;
- record any mismatch between documentation, source, migrations, checksums, or current executable reality;
- state an exact recommendation: accept, accept with recorded exceptions, or reject the WP-09 evidence boundary.

## 4. Explicitly authorized file changes

The agent MAY create or update only:

- `docs/cae/implementation/CAE_WP10A_ACCEPTANCE_REPORT.md`
- `docs/cae/implementation/CAE_WP10A_REGRESSION_LEDGER.md`
- `docs/cae/implementation/CAE_WP10A_CLAIM_BOUNDARY_MATRIX.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`
- a narrowly scoped WP-10A evaluation manifest or verification script under `docs/cae/evaluations/` or `scripts/cae/` **only when it tests a missing acceptance assertion without changing runtime behavior**.

The agent SHALL preserve all unrelated working-tree changes. It SHALL use the project’s normal patch mechanism for edits and shall commit only the files listed above.

## 5. Prohibitions and hard stops

The agent SHALL NOT:

- create or modify SQL migrations, database tables, functions, RLS policies, Storage buckets, or database contents outside disposable force-rolled-back proof fixtures;
- alter `packages/ca_runtime`, `api`, `services`, semantic operations, registry import behavior, or any production-facing route;
- change `.env`, print secrets, copy credentials into documentation, or replace configured endpoints;
- import legacy data, dual-write, reconfigure SQLite, or declare PostgreSQL authoritative for an aggregate;
- resolve ontology, scope, tenancy, source-authority, registry, or object-class collisions;
- clean up, normalize, or “fix” inherited SDA/SFL/Primitive quarantine findings;
- convert an E0/E1/E2/E3 result into E4 semantic, taste, human, or world-outcome proof.

If the agent encounters an evidence mismatch that cannot be explained without changing runtime code, a migration, a registry authority decision, or a source-of-truth decision, it SHALL classify the issue as `CONTRACT_CONFLICT` or `BLOCKED`, record it, and stop. It SHALL not repair the mismatch in this phase.

## 6. Required verification and evidence discipline

First, run the static checks already named by the evidence handoff:

```powershell
python scripts/cae/verify_wp05_specs.py
python scripts/cae/verify_wp06_runbook.py
```

Record command, exit status, repository commit, and the real proposition each result tests. A successful static result proves structural conformance only; it does not prove database application, RLS, Storage access, runtime integration, or semantic quality.

Next, inspect the source and documentation of the WP-02A, WP-03, WP-04, WP-07, WP-08, and WP-09 runners. Confirm whether each runner has precondition checks, isolation/rollback behavior, cleanup, negative cases, and actual independent evidence. The acceptance record SHALL not claim a runner was reproduced merely because its source was read.

Selective dynamic reproduction is OPTIONAL and permitted only when all of the following are true:

1. the agent identifies the target as the configured non-production CAE staging environment;
2. credentials are already safely configured and are not emitted;
3. the runner is known to force rollback and clean external Storage objects, or the agent first stops and asks for an operator decision;
4. the verification claim matches the target fidelity; and
5. no new migration or permanent data change is required.

For a reproduced runner, preserve its receipt/evidence identifiers only if the proof protocol permits them to be documented without exposing sensitive data. Record environment identity at a non-secret level, the cleanup outcome, and any reason the result is narrower than the original claim.

The acceptance matrix must expressly preserve at least these non-claims: no full legacy-data migration, no repository-wide PostgreSQL authority, no runtime registry consumer cutover, no SFL missing-family resolution, no live user API bridge, no agent orchestrator execution, no semantic/taste/E4 claim, and no production readiness claim.

## 7. Required artifacts

`CAE_WP10A_CLAIM_BOUNDARY_MATRIX.md` SHALL list, for every WP-00 through WP-09 package: implementation/control commits, asserted behavior, evidence artifact, verifier or inspection method, fidelity, adversarial or countertest coverage, result, non-claim, and current confidence. “Current confidence” is an evidence classification, never a subjective assertion of quality.

`CAE_WP10A_REGRESSION_LEDGER.md` SHALL list every command actually run, its purpose, exit status, environment class, mutation/rollback behavior, cleanup, and observed limitation. It shall also list inspections that were deliberately not run and why.

`CAE_WP10A_ACCEPTANCE_REPORT.md` SHALL contain: scope, authority sources, actual findings, reproducibility results, discrepancies, accepted claims, rejected/qualified claims, risks, exact operator inspection points, and the final decision request.

The control-state record SHALL be updated with completed checks, all blocked items, the acceptance status, exact commit, and the next proposed transition. It shall not change the active work package to CA-MAP-01 unless the operator approves the requested transition.

## 8. Completion, decision, and stop condition

WP-10A is complete only if the three artifacts exist, static evidence is actually rechecked, all documentation claims are classified against direct evidence, any dynamic reproduction is recorded honestly, and all non-claims remain explicit. The agent must report the following operator decision verbatim:

> **Accept WP-09 as bounded staging evidence, maintain all stated non-claims, and authorize CA-MAP-01 only: scope, authority, canonical/operational-plane mapping, and collision registration?**

After presenting that decision, the agent SHALL stop. It has no authority to begin CA-MAP-01, create an object constitution, draft a new schema, or implement tenancy.

## 9. Gemini activation prompt (approximately 240 words)

You are the CAE governed execution agent for `WP-10A — Vertical-Slice Evidence Containment and Acceptance`. Read `docs/cae/gemini_execution/01_WP10A_EVIDENCE_CONTAINMENT_MANDATE.md` in full, then read every mandatory reference it names before making a plan, changing files, or executing verification. This mandate authorizes only an evidence-acceptance review of WP-00 through WP-09. It does not authorize CA-MAP-01, object constitutions, PostgreSQL cutover, RLS, migrations, runtime code, registry repair, API changes, user-data migration, or any production action.

Create a concise internal plan mapped only to the allowed files, required evidence, verification commands, rollback/cleanup conditions, and stop rule in the mandate. Treat commits, scripts, migrations, and declared proof environments as evidence to inspect—not as proof merely because documentation says they exist. Distinguish direct observation, static validation, dynamic staging reproduction, and untested claims. A green check, a Storage URL, a schema row, or a receipt authored by the same operation is never sufficient independent proof without the stated countertest or readback.

You may run the two named static validators. You may reproduce a dynamic runner only after confirming it targets disposable staging, preserves secret confidentiality, force-rolls back database work, and cleans external Storage effects. If that cannot be proven before execution, record the gap and do not run it. Never modify runtime code, SQL, RLS, Storage configuration, `.env`, registry contents, or legacy state.

Produce the acceptance report, claim-boundary matrix, regression ledger, and narrowly scoped control-state update. Record actual commands/results, environment class, limitations, contradictions, and non-claims. Commit only those allowed artifacts. End by requesting exactly the operator decision in Section 8, then stop.
