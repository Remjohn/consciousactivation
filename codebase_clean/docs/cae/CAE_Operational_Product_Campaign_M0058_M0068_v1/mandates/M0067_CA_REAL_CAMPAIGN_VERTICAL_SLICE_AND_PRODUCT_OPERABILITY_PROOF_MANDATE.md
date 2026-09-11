# CAE-M0067 — Real Campaign Vertical Slice and Product Operability Proof

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0067
Mandate Title: Real Campaign Vertical Slice and Product Operability Proof
Requirement / Invariant: INV-PRODUCT-REAL-001
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: E2E harness + all integrated product/runtime surfaces

## 1. Decision / Objective

Prove the actual product can run a representative campaign from semantic intent through asset retrieval, production Program execution, native runtime, operator intervention and release evidence.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0058–M0066 accepted artifacts
- current PRD
- E2E fixture harness
- operator gate checklist
- all runtime receipts

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Run one clean representative campaign and one adversarial campaign. Capture every required checkpoint, runtime receipt, operator intervention, artifact lineage and terminal state. Exercise retrieval, runtime, operator and QA failure paths.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Full campaign evidence pack; E2E report; artifact manifest; runtime receipts; operator decision records; residual gap ledger.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No mock substitution where native runtime proof is required; no manual backdoor steps omitted from evidence; no deletion of failures.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Full campaign evidence pack; E2E report; artifact manifest; runtime receipts; operator decision records; residual gap ledger.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Run from clean fixture state. Repeat at least once. The campaign must be operable by the intended operator flow rather than developer-only shell intervention.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: developers manually repair state between stages and the campaign is reported as automated. All intervention must be recorded and authorized.

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

`CAMPAIGN_READY → EXECUTING → OPERATOR_GATE → RELEASE_READY|BLOCKED|FAILED`.

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

Preserve the complete evidence pack. Return only the first failing layer to its responsible mandate.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0067 as the first real product operability proof and authorize M0068?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0067 — Real Campaign Vertical Slice and Product Operability Proof.

Authority:
M0058–M0066 accepted artifacts; current PRD; E2E fixture harness; operator gate checklist; all runtime receipts

Scope:
Run one clean representative campaign and one adversarial campaign. Capture every required checkpoint, runtime receipt, operator intervention, artifact lineage and terminal state. Exercise retrieval, runtime, operator and QA failure paths.

Objective:
Prove the actual product can run a representative campaign from semantic intent through asset retrieval, production Program execution, native runtime, operator intervention and release evidence.

Prohibitions:
No mock substitution where native runtime proof is required; no manual backdoor steps omitted from evidence; no deletion of failures.

Execution:
Run from clean fixture state. Repeat at least once. The campaign must be operable by the intended operator flow rather than developer-only shell intervention.

Required evidence:
False proof: developers manually repair state between stages and the campaign is reported as automated. All intervention must be recorded and authorized.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0067 as the first real product operability proof and authorize M0068?

Do not begin the next mandate.
