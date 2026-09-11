# CAE-M0061 — Production Asset Demand / Resolution Contract

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0061
Mandate Title: Production Asset Demand / Resolution Contract
Requirement / Invariant: INV-ASSET-DEMAND-001
Model Recommendation: Claude / ChatGPT
Target Subsystem / Files: `services/asset-intelligence/`, production-program, VAE/Delegation

## 1. Decision / Objective

Establish the executable contract between existing semantic/production Programs and asset resolution so a Program can express exactly what physical media is required without teaching the runtime how to decide meaning.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0058 evidence ledger
- M10 Asset Intelligence Edroll mandate
- M11 Production Semantic Program mandate
- current AssetAnnotation/AssetCatalog
- current VAE/Delegation boundary
- current CompositionAssetPack/VideoEditProgram

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Reuse existing asset and program objects. Define or complete the derived demand/resolution boundary carrying semantic obligation, media/source requirements, time/duration constraints, rights state, workspace, provenance and resolution outcome.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Typed demand/resolution contract; adapter/translator; contract tests; sample demand emitted from an existing Program.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No universal media AST, no new canonical asset ontology, no retrieval engine yet, no runtime-specific semantics in the Program.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Typed demand/resolution contract; adapter/translator; contract tests; sample demand emitted from an existing Program.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Prove a real existing Program can emit the demand and the downstream asset layer can accept it without semantic re-selection.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: a demand is structurally valid but drops the semantic role or provenance. Require field-level semantic preservation.

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

`PROGRAM_NEEDS_ASSET → DEMAND_EMITTED → RESOLUTION_PENDING|SATISFIED|BLOCKED`.

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

Revert only derived contract/translator changes.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0061 and authorize M0062/M0063?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0061 — Production Asset Demand / Resolution Contract.

Authority:
M0058 evidence ledger; M10 Asset Intelligence Edroll mandate; M11 Production Semantic Program mandate; current AssetAnnotation/AssetCatalog; current VAE/Delegation boundary; current CompositionAssetPack/VideoEditProgram

Scope:
Reuse existing asset and program objects. Define or complete the derived demand/resolution boundary carrying semantic obligation, media/source requirements, time/duration constraints, rights state, workspace, provenance and resolution outcome.

Objective:
Establish the executable contract between existing semantic/production Programs and asset resolution so a Program can express exactly what physical media is required without teaching the runtime how to decide meaning.

Prohibitions:
No universal media AST, no new canonical asset ontology, no retrieval engine yet, no runtime-specific semantics in the Program.

Execution:
Prove a real existing Program can emit the demand and the downstream asset layer can accept it without semantic re-selection.

Required evidence:
False proof: a demand is structurally valid but drops the semantic role or provenance. Require field-level semantic preservation.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0061 and authorize M0062/M0063?

Do not begin the next mandate.
