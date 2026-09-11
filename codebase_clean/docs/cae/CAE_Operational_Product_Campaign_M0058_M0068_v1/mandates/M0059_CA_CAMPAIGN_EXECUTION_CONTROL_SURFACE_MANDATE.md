# CAE-M0059 — Campaign Execution Control Surface

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0059
Mandate Title: Campaign Execution Control Surface
Requirement / Invariant: FR-OPS-CONTROL
Model Recommendation: Claude / ChatGPT
Target Subsystem / Files: `packages/ca_runtime/`, program execution/control APIs

## 1. Decision / Objective

Make the existing campaign/program runtime operable from an explicit product control surface: launch, inspect state, pause/resume where supported, surface failures and retrieve receipts without bypassing authority.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0058 accepted baseline
- current `packages/ca_runtime/`
- current Program registry/state machine
- operator gate and receipts
- current product/API/UI control path

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Implement only the missing control operations required to start and inspect a real campaign execution. Preserve existing authority lanes and state machine semantics. Use typed operations and existing receipts.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Launch/status/control operations; minimal operator endpoint/UI wiring; receipt viewer or retrieval path; integration tests.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No new scheduler, no new Program runtime, no direct DB mutation from UI, no automatic approval.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Launch/status/control operations; minimal operator endpoint/UI wiring; receipt viewer or retrieval path; integration tests.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Exercise start, status, failure, recovery and supported pause/resume behavior against a real fixture workspace. Verify server state, not just UI state.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: a button reports 'running' while no worker/Program state changes. Require authoritative persisted state and receipt evidence.

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

`READY|IDLE → START → RUNNING|BLOCKED`; supported `RUNNING → PAUSED → RESUMED`; terminal states remain terminal.

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

Revert only new control-path code and preserve prior execution state.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0059 and authorize M0061?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0059 — Campaign Execution Control Surface.

Authority:
M0058 accepted baseline; current `packages/ca_runtime/`; current Program registry/state machine; operator gate and receipts; current product/API/UI control path

Scope:
Implement only the missing control operations required to start and inspect a real campaign execution. Preserve existing authority lanes and state machine semantics. Use typed operations and existing receipts.

Objective:
Make the existing campaign/program runtime operable from an explicit product control surface: launch, inspect state, pause/resume where supported, surface failures and retrieve receipts without bypassing authority.

Prohibitions:
No new scheduler, no new Program runtime, no direct DB mutation from UI, no automatic approval.

Execution:
Exercise start, status, failure, recovery and supported pause/resume behavior against a real fixture workspace. Verify server state, not just UI state.

Required evidence:
False proof: a button reports 'running' while no worker/Program state changes. Require authoritative persisted state and receipt evidence.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0059 and authorize M0061?

Do not begin the next mandate.
