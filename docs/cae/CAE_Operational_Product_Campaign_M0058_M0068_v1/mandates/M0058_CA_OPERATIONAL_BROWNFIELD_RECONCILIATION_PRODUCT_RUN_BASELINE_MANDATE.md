# CAE-M0058 — Operational Brownfield Reconciliation & Product Run Baseline

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0058
Mandate Title: Operational Brownfield Reconciliation & Product Run Baseline
Requirement / Invariant: FR-OPS-BASELINE
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: `programs/`, `packages/ca_runtime/`, current pipeline/runtime tests

## 1. Decision / Objective

Establish a verified post-M057 product-operability baseline and prove which existing Program, Harness, runtime, state, operator and test paths are actually reachable today.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- `docs/PRD/CURRENT.md`
- `docs/cae/PROMPT_REFERENCE_BLOCKS.md`
- `01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- current `programs/`
- current `packages/ca_runtime/`
- current Pipeline/Asset/VAE/production surfaces

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Trace one representative campaign from product entry through Program dispatch, harness execution, artifact/state persistence, operator gate, evaluation and available release path. Build an executable-state ledger identifying working, partial, mocked, unreachable and conflicting segments. Do not repair them yet.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Brownfield evidence ledger; reachable-call-path graph; product run baseline; blocker register; control-state entry.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No architecture redesign, no retrieval/index implementation, no UI rewrite, no runtime adapter work, no claim of readiness based on docs.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Brownfield evidence ledger; reachable-call-path graph; product run baseline; blocker register; control-state entry.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Execute current tests and one minimal real product run using an existing supported fixture. Trace calls and receipts. Record exact commit and environment. Identify the smallest blocking chain that prevents operating/testing the product.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: all tests green while no actual campaign reaches the intended runtime. Require at least one real state transition or runtime execution. `EXECUTABLE` evidence is required for claims of reachability.

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

`UNKNOWN → INSPECT/EXECUTE → VERIFIED|PARTIAL|BLOCKED`.

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

Revert only the evidence/baseline artifacts.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0058 and authorize M0059/M0060?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0058 — Operational Brownfield Reconciliation & Product Run Baseline.

Authority:
`docs/PRD/CURRENT.md`; `docs/cae/PROMPT_REFERENCE_BLOCKS.md`; `01_CA_MANDATE_AUTHORING_PROTOCOL.md`; `02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`; current `programs/`; current `packages/ca_runtime/`

Scope:
Trace one representative campaign from product entry through Program dispatch, harness execution, artifact/state persistence, operator gate, evaluation and available release path. Build an executable-state ledger identifying working, partial, mocked, unreachable and conflicting segments. Do not repair them yet.

Objective:
Establish a verified post-M057 product-operability baseline and prove which existing Program, Harness, runtime, state, operator and test paths are actually reachable today.

Prohibitions:
No architecture redesign, no retrieval/index implementation, no UI rewrite, no runtime adapter work, no claim of readiness based on docs.

Execution:
Execute current tests and one minimal real product run using an existing supported fixture. Trace calls and receipts. Record exact commit and environment. Identify the smallest blocking chain that prevents operating/testing the product.

Required evidence:
False proof: all tests green while no actual campaign reaches the intended runtime. Require at least one real state transition or runtime execution. `EXECUTABLE` evidence is required for claims of reachability.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0058 and authorize M0059/M0060?

Do not begin the next mandate.
