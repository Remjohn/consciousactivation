# CAE-M0066 — Operator Control, Native Editing and Human Resolution Persistence

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0066
Mandate Title: Operator Control, Native Editing and Human Resolution Persistence
Requirement / Invariant: INV-HUMAN-RESOLUTION-001
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: operator workspace + HumanResolutionEpisode/revision state

## 1. Decision / Objective

Make the native editing surface genuinely operator-operable and persist operator interventions as governed human-resolution lineage linked to the CAE run.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0065
- operator runtime/control path
- HumanResolutionEpisode/revision mechanisms
- current QA/release receipts
- authority lanes

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Operator must inspect timeline, change selected asset/timing within allowed boundaries, save the change, see resulting state, and produce persistent before/after lineage and receipt. Release remains separately authorized.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Operator route/launch/embedding; persisted human-resolution record; CAS/revision safety; before/after evidence; acceptance workflow.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No UI-only state, no silent overwrite, no promotion of one operator edit into doctrine, no release bypass.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Operator route/launch/embedding; persisted human-resolution record; CAS/revision safety; before/after evidence; acceptance workflow.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Test edit propagation from native runtime to authoritative CAE state. Test refresh/reopen and concurrent revision failure.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: UI shows changed clip but persisted state still points to old source.

Evidence classes:
`EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`.

The agent must state:
- what the verifier actually measures;
- what it does not measure;
- the false-proof countercase;
- environment-fidelity requirement;
- whether operator validation is required.

A score, screenshot, import statement or green unit test is not evidence beyond its declared fidelity.

## 9. State Transition

`NATIVE_READY → HUMAN_EDIT → REVISION_RECORDED → QA_REQUIRED`.

For all stateful behavior specify actor, preconditions, validators, postconditions, receipt, error route and recovery.

## 10. Completion / Stop Condition

Complete only when:
- requested artifacts exist;
- verification is run at the required fidelity;
- limitations are recorded;
- control state is updated;
- exact commit is captured;
- operator decision is requested.

STOP after the operator decision below.

## 11. Rollback / Recovery

Revert only current unpromoted revision while preserving history.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Does M0066 satisfy the operator gate and authorize M0067?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0066 — Operator Control, Native Editing and Human Resolution Persistence.

Authority:
M0065; operator runtime/control path; HumanResolutionEpisode/revision mechanisms; current QA/release receipts; authority lanes

Scope:
Operator must inspect timeline, change selected asset/timing within allowed boundaries, save the change, see resulting state, and produce persistent before/after lineage and receipt. Release remains separately authorized.

Objective:
Make the native editing surface genuinely operator-operable and persist operator interventions as governed human-resolution lineage linked to the CAE run.

Prohibitions:
No UI-only state, no silent overwrite, no promotion of one operator edit into doctrine, no release bypass.

Execution:
Test edit propagation from native runtime to authoritative CAE state. Test refresh/reopen and concurrent revision failure.

Required evidence:
False proof: UI shows changed clip but persisted state still points to old source.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Does M0066 satisfy the operator gate and authorize M0067?

Do not begin the next mandate.
