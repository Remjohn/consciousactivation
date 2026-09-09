# CAE-M0068 — Production Readiness and Residual-Gap Certification

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0068
Mandate Title: Production Readiness and Residual-Gap Certification
Requirement / Invariant: INV-CERT-REAL-001
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: certification/evidence docs and existing verification harnesses

## 1. Decision / Objective

Certify whether CAE is genuinely operable and testable for the supported vertical slice, separating verified product capability from remaining gaps and defining the exact next implementation campaign.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0067 complete evidence pack
- current PRD
- PROMPT_REFERENCE_BLOCKS
- mandate protocol
- operator gate

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Produce a certification matrix across product operation, Program execution, asset retrieval, video runtime, operator control, QA/release, evidence, test/replay and environment fidelity. Mark each as VERIFIED, PARTIAL, BLOCKED or NOT IN SCOPE. Do not implement new features.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Certification report; readiness matrix; residual-gap ledger; proposed next campaign frontier; exact evidence/commit references.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No polishing code, no hidden fixes, no status inflation, no changing acceptance criteria after seeing results.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Certification report; readiness matrix; residual-gap ledger; proposed next campaign frontier; exact evidence/commit references.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Re-run the decisive proof commands. Confirm at least one full real campaign path and test suite. Preserve failed cases and explicitly distinguish environment failure from code failure.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: a product is declared ready because every individual component is green, while cross-service flow fails. Certification is cross-boundary and requires real vertical evidence.

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

`EVIDENCE_COMPLETE → CERTIFY → READY|CONDITIONAL|BLOCKED`.

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

No code rollback; preserve certification evidence. Any newly discovered implementation work becomes a separate next campaign.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept the M0068 certification and authorize the next campaign from the residual-gap ledger?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0068 — Production Readiness and Residual-Gap Certification.

Authority:
M0067 complete evidence pack; current PRD; PROMPT_REFERENCE_BLOCKS; mandate protocol; operator gate

Scope:
Produce a certification matrix across product operation, Program execution, asset retrieval, video runtime, operator control, QA/release, evidence, test/replay and environment fidelity. Mark each as VERIFIED, PARTIAL, BLOCKED or NOT IN SCOPE. Do not implement new features.

Objective:
Certify whether CAE is genuinely operable and testable for the supported vertical slice, separating verified product capability from remaining gaps and defining the exact next implementation campaign.

Prohibitions:
No polishing code, no hidden fixes, no status inflation, no changing acceptance criteria after seeing results.

Execution:
Re-run the decisive proof commands. Confirm at least one full real campaign path and test suite. Preserve failed cases and explicitly distinguish environment failure from code failure.

Required evidence:
False proof: a product is declared ready because every individual component is green, while cross-service flow fails. Certification is cross-boundary and requires real vertical evidence.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept the M0068 certification and authorize the next campaign from the residual-gap ledger?

Do not begin the next mandate.
