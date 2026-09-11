# CAE-M0062 — Cinematic Corpus Ingestion and Scene Organization

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Prepared: 2026-09-09
Program: CAE Operational Product Campaign M0058–M0068

## Mandate Summary

Mandate ID: CAE-M0062
Mandate Title: Cinematic Corpus Ingestion and Scene Organization
Requirement / Invariant: INV-CINEMA-CORPUS-001
Model Recommendation: ChatGPT / Grok
Target Subsystem / Files: `services/asset-intelligence/` and derived retrieval/index storage

## 1. Decision / Objective

Turn explicitly authorized cinematic/archival/owned media into a governed, timestamped, searchable scene corpus compatible with the existing AssetAnnotation doctrine.

This mandate is intentionally narrow. It establishes one executable product boundary without authorizing unrelated architecture work.

## 2. Governing Doctrine and Authority

The agent SHALL treat the following as governing inputs for this phase:

- M0061 accepted contract
- M10 Asset Intelligence Edroll mandate
- existing `services/asset-intelligence/`
- legal/licensing records
- workspace isolation/storage

Authority is separated into three axes:
- Definition authority: the artifact/version that defines what an object means.
- Runtime authority: the verified representation actually used by typed operations.
- Change/promotion authority: the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory Reading Before Action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is present in the repository or supplied execution bundle. Missing sources become `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, API, Program, Harness or runtime.

## 4. Exact Scope

Implement bounded ingest for approved media sources. Generate stable media identity, scene/time boundaries, contextual captions, semantic/insert roles where available, transcript/dialogue metadata where available, rights/provenance state and derived index records.

Inputs:
- accepted upstream artifacts;
- current repository implementation;
- current product control state;
- only governed runtime/data available to the mandate.

Outputs:
Ingest pipeline; scene records/index projection; deterministic reindex; sample governed corpus; verification/rights tests; ingest receipts.

Operators:
- execution agent for bounded implementation;
- operator only for explicit approval, promotion, exception or authority decision.

## 5. Explicit Prohibitions

No unbounded scraping, no legal conclusion from metadata, no rights upgrade, no second canonical asset ontology.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision SHALL be recorded and routed to the correct authority.

## 6. Required Artifacts and Semantic Obligations

Ingest pipeline; scene records/index projection; deterministic reindex; sample governed corpus; verification/rights tests; ingest receipts.

Every generated artifact SHALL preserve applicable workspace, source/version, provenance, authority and receipt information.

## 7. Required Work / Implementation Behavior

Use real media fixtures. Reindex must be idempotent. Verify exact source hash/time ranges and workspace isolation.

The implementation sequence is:

`READ → INSPECT → PLAN → IMPLEMENT → TEST → EVIDENCE → CONTROL STATE → COMMIT → OPERATOR GATE → STOP`

No adjacent mandate begins during execution.

## 8. Verification and Evidence Standard

False proof: duplicate or stale scene record points to plausible but wrong media bytes/timestamp. Reject on hash/time mismatch.

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

`SOURCE_ACCEPTED → INGESTED → INDEXED|QUARANTINED`.

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

Remove only derived corpus/index records in controlled namespace; preserve source and canonical annotations.

Failed evidence SHALL be preserved. Never delete a failed receipt to manufacture a clean result.

## 12. Operator Decision

Do you accept M0062 and authorize M0064?

The operator SHALL choose:
`ACCEPT → AUTHORIZE NEXT`
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`
`REPAIR → RETURN TO CURRENT MANDATE`
`BLOCK → DO NOT PROCEED`

## 13. 200–300 Word Activation Prompt

Execute only CAE-M0062 — Cinematic Corpus Ingestion and Scene Organization.

Authority:
M0061 accepted contract; M10 Asset Intelligence Edroll mandate; existing `services/asset-intelligence/`; legal/licensing records; workspace isolation/storage

Scope:
Implement bounded ingest for approved media sources. Generate stable media identity, scene/time boundaries, contextual captions, semantic/insert roles where available, transcript/dialogue metadata where available, rights/provenance state and derived index records.

Objective:
Turn explicitly authorized cinematic/archival/owned media into a governed, timestamped, searchable scene corpus compatible with the existing AssetAnnotation doctrine.

Prohibitions:
No unbounded scraping, no legal conclusion from metadata, no rights upgrade, no second canonical asset ontology.

Execution:
Use real media fixtures. Reindex must be idempotent. Verify exact source hash/time ranges and workspace isolation.

Required evidence:
False proof: duplicate or stale scene record points to plausible but wrong media bytes/timestamp. Reject on hash/time mismatch.

Do not widen scope because an adjacent issue is discovered. Inspect the actual brownfield implementation before making claims. Reuse existing canonical objects, Programs, Harnesses, services and state machines wherever they already provide the required boundary. Keep source-of-meaning authority, runtime authority and change/promotion authority separate. Do not treat a schema, UI state, import, mock, score or green unit test as proof beyond its declared fidelity.

The verification must defeat the stated false-proof case and must record environment, command, fixture/state identity, result and limitation. Where the mandate changes state, record actor, preconditions, validators, postconditions, receipt, error route and recovery path. Preserve failed evidence; never weaken the verifier to manufacture PASS.

When the scoped artifact and proof are complete, update control state, record the exact commit and stop. Request only this operator decision:

Do you accept M0062 and authorize M0064?

Do not begin the next mandate.
