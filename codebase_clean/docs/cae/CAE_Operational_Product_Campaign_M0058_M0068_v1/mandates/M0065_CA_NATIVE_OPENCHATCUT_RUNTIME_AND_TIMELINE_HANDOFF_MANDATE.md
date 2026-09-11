# CAE-M0065 — Native OpenChatCut Runtime and Timeline Handoff

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0065
Mandate Title: Native OpenChatCut Runtime and Timeline Handoff
Requirement / Invariant: INV-VIDEO-RUNTIME-001
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: Pipeline video edit path + OpenChatCut integration surface

## 1. Decision / Objective

Make the existing video Program executable against a real OpenChatCut runtime/timeline so selected CAE assets become actual native edit structures rather than JSON-only or mock representations.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0064
- existing video_edit_program
- Pipeline media/EDL/binding implementation
- actual OpenChatCut runtime contract
- current runtime receipts

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Build the narrowest CAE-side runtime adapter/import bridge. Transfer media identity, source ranges, track/role metadata, semantic obligation, provenance and version. Keep CAE as system of record.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Native runtime adapter; real fixture project/timeline; import/command mapping; media-range verification; smoke/render/export evidence.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No OpenChatCut fork without separately authorized incompatibility; no CAE authority transfer; no semantic reinterpretation in adapter; no mock-only final proof.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Native runtime adapter; real fixture project/timeline; import/command mapping; media-range verification; smoke/render/export evidence.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Use the actual OpenChatCut runtime. Verify native timeline state and exact media in/out. Capture runtime identity and receipt.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: timeline visually contains a clip but wrong media bytes or source range were imported.

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

`BOUND → ADAPT → NATIVE_TIMELINE_READY → EXECUTED|BLOCKED`.

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

Invalidate/remove only generated runtime fixture/project; preserve CAE semantic state.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0065 and authorize M0066?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0065 — Native OpenChatCut Runtime and Timeline Handoff.

Authority:
M0064; existing video_edit_program; Pipeline media/EDL/binding implementation; actual OpenChatCut runtime contract; current runtime receipts

Scope:
Build the narrowest CAE-side runtime adapter/import bridge. Transfer media identity, source ranges, track/role metadata, semantic obligation, provenance and version. Keep CAE as system of record.

Objective:
Make the existing video Program executable against a real OpenChatCut runtime/timeline so selected CAE assets become actual native edit structures rather than JSON-only or mock representations.

Prohibitions:
No OpenChatCut fork without separately authorized incompatibility; no CAE authority transfer; no semantic reinterpretation in adapter; no mock-only final proof.

Execution:
Use the actual OpenChatCut runtime. Verify native timeline state and exact media in/out. Capture runtime identity and receipt.

Required evidence:
False proof: timeline visually contains a clip but wrong media bytes or source range were imported.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0065 and authorize M0066?

Do not begin the next mandate.
