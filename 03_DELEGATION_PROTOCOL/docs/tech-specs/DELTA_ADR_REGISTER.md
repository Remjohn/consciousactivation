---
title: Delegation Delta ADR Register
product: CMF Content Harness Visual Asset Editor Delegation Protocol
stage: 1
status: proposed_for_stage_2
created: 2026-07-14
---

# Delta ADR Register

This register contains architecture decisions still needed to turn the locked product decisions into implementable contracts. It does not reopen `D001` through `D016` or the upstream product boundaries.

| ADR | Status | Delta requiring a decision | Primary spec | Blocking effect |
|---|---|---|---|---|
| ADR-DLG-001 | Accepted input | This repository is the sole publisher of shared public schemas and compatibility versions; product repositories consume pinned releases and do not fork them | TS-DLG-01 | Governs all Stage 3 packaging |
| ADR-DLG-002 | Proposed | Define canonical schema IDs, payload-version placement, semantic version rules, generated binding targets and extension namespaces | TS-DLG-01 | Contract freeze |
| ADR-DLG-003 | Proposed | Define canonical serialization, hash coverage, reference resolution and signature bytes for envelope plus payload | TS-DLG-01, TS-DLG-02 | Integrity implementation |
| ADR-DLG-004 | Proposed | Resolve `submission-receipt` ambiguity by separating VAE admission authority from protocol validation/audit receipt authority or by defining a single protocol-issued receipt over a signed VAE admission fact | TS-DLG-02, TS-DLG-03 | Field-owner gate |
| ADR-DLG-005 | Proposed | Remove `downstream_consumption_authorized` from the VAE-produced Asset Result Contract; establish it only through Result Acknowledgement | TS-DLG-06 | Field-owner gate and D006 |
| ADR-DLG-006 | Proposed | Introduce one exact demand identity reference shape containing request ID, version, payload hash and canonical reference for every related message | TS-DLG-01, TS-DLG-03 | FR-015 and traceability |
| ADR-DLG-007 | Proposed | Replace open nested public objects with typed closed definitions or versioned governed extension points | TS-DLG-01 | Schema authority and compatibility |
| ADR-DLG-008 | Proposed | Separate idempotent duplicate resolution from security replay detection, including key scopes, nonce scopes, retention and response receipts | TS-DLG-03, TS-DLG-09 | Security and reliability gates |
| ADR-DLG-009 | Proposed | Select the lifecycle persistence model, per-correlation ordering, transaction boundary, race-precedence rules, reconstruction strategy and audit-store failure behavior | TS-DLG-03 | Executable lifecycle gate |
| ADR-DLG-010 | Proposed | Define manifest signing, negotiation algorithm, pinned profile representation, adapter registry, immutable migration artifact and semantic-equivalence proof | TS-DLG-04 | Compatibility gate |
| ADR-DLG-011 | Proposed | Define budget and cancellation race precedence, hard-ceiling enforcement, safe checkpoint contract and immutable compute disposition | TS-DLG-05 | Budget/cancellation conformance |
| ADR-DLG-012 | Proposed | Define amendment, supersession and selective-invalidation authority at JSON Pointer field granularity and the minimum reusable-work evidence | TS-DLG-05, TS-DLG-06 | Authority and reuse gates |
| ADR-DLG-013 | Proposed | Define result, acknowledgement, invalidation, revocation and replacement history without mutating completed facts | TS-DLG-06 | Post-completion governance |
| ADR-DLG-014 | Proposed | Define Delegation Set member graph semantics, cycle rules, set status derivation, atomic/partial policy and selective invalidation | TS-DLG-07 | Multi-asset conformance |
| ADR-DLG-015 | Proposed | Define transport-neutral inbound/outbound ports, routing guarantees, callback/event semantics and transport conformance fixtures | TS-DLG-01, TS-DLG-08 | Cross-transport equivalence |
| ADR-DLG-016 | Proposed | Extend the existing Harness Control Tower with a read-model contract, freshness/error semantics and no independent authority store | TS-DLG-08 | PRES-012 and GATE-08 |
| ADR-DLG-017 | Proposed | Select principal identity format, trust roots, signature suite, key rotation/revocation, clock skew and historical verification behavior | TS-DLG-02, TS-DLG-09 | Integrity gate |
| ADR-DLG-018 | Proposed | Define retention, privacy classification, access-controlled resource references, negative-evidence quarantine and deletion/legal-hold behavior | TS-DLG-08, TS-DLG-09 | Data governance |
| ADR-DLG-019 | Empirical decision | Benchmark validation overhead, durable receipt latency, projection freshness and duplicate resolution before freezing SLOs | TS-DLG-08, TS-DLG-09 | Performance certification |
| ADR-DLG-020 | Proposed | Define contract publication, package signing, changelog, compatibility manifest, release pinning and rollback mechanics | TS-DLG-04, TS-DLG-09 | Stage 3 release baseline |
| ADR-DLG-021 | Accepted | Keep envelope protocol `1.0`, advance Visual Asset Demand to `1.1`, and version the package as `1.1.0-rc.1` | TS-DLG-01, TS-DLG-04 | Separates wire and message version axes |
| ADR-DLG-022 | Accepted | Nest Activative Call, Reaction Receipt, and Expression Moment references under `activative_semantic_lineage` using exact resource identity tuples | TS-DLG-01, TS-DLG-02 | Canonical lineage shape |
| ADR-DLG-023 | Accepted | Require per-domain behavioral preservation/enforcement and evaluator evidence; parse-only support is incompatible | TS-DLG-04, TS-DLG-09 | Compatibility admission gate |
| ADR-DLG-024 | Accepted | Reject legacy aliases in the closed V1.1 schema and allow them only through the explicit lossless owner-context migration | TS-DLG-04, TS-DLG-05 | Migration and anti-defaulting rule |

## Proposed technical-specification plan

| Order | Specification | Purpose and exit evidence |
|---:|---|---|
| 1 | `TS-DLG-01-CONTRACT-REGISTRY-AND-COMMON-ENVELOPE.md` | Close the public ABI, schema/version identity, exact demand reference, canonical encoding, routing ports and generated-binding policy |
| 2 | `TS-DLG-02-AUTHORITY-POLICY-AND-PRINCIPAL-IDENTITY.md` | Resolve every field owner, admission authority, principal permission, signature identity and prohibited mutation |
| 3 | `TS-DLG-03-LIFECYCLE-IDEMPOTENCY-AND-REPLAY.md` | Specify executable transition rules, ordering, persistence, idempotency, replay rejection, recovery and audit atomicity |
| 4 | `TS-DLG-04-COMPATIBILITY-NEGOTIATION-ADAPTERS-AND-MIGRATION.md` | Define signed manifests, negotiation, pinning, lossless adapters, migration evidence, deprecation and rollback |
| 5 | `TS-DLG-05-BUDGET-CANCELLATION-AMENDMENTS-AND-SUPERSESSION.md` | Resolve budget ceilings, checkpoints, deadlines, races, amendments, supersession and selective invalidation |
| 6 | `TS-DLG-06-RESULT-ACKNOWLEDGEMENT-AND-POST-COMPLETION-GOVERNANCE.md` | Correct result authority, acknowledgement, rejection, invalidation, revocation, replacement and historical truth |
| 7 | `TS-DLG-07-DELEGATION-SETS-AND-MULTI-ASSET-COORDINATION.md` | Specify dependency graph, member independence, set status, composition evidence and set-level invalidation |
| 8 | `TS-DLG-08-AUDIT-OBSERVABILITY-AND-CONTROL-TOWER-PROJECTIONS.md` | Define audit ledger, read models, metrics, incidents, retention and existing Control Tower integration |
| 9 | `TS-DLG-09-CONFORMANCE-RESILIENCE-AND-SECURITY-TESTING.md` | Define executable test harnesses, fault model, threat model, certification evidence, release and rollback gates |
| 10 | `TS-DLG-10-FORMAT02-REFERENCE-INTEGRATION.md` | Pin product versions and prove the complete Release 1 path against executable cross-repository fixtures |

Specs 1 through 3 establish the contract/authority/lifecycle foundation. Specs 4 through 8 may then proceed in parallel with shared decisions pinned. Spec 9 consolidates executable gate evidence, and Spec 10 closes the Release 1 cross-product proof.

## Stage 2 ADR disposition

| ADRs | Stage 2 disposition |
|---|---|
| ADR-DLG-001 | Accepted as the contract-publication ownership rule in TS-DLG-01. |
| ADR-DLG-002, ADR-DLG-003, ADR-DLG-006, ADR-DLG-007, ADR-DLG-015 | Normative target specified in TS-DLG-01; contract/schema changes remain for Stage 3. |
| ADR-DLG-004, ADR-DLG-017 | Normative target specified in TS-DLG-02; upstream security/product ratification remains required. |
| ADR-DLG-008, ADR-DLG-009 | Normative target specified in TS-DLG-03; persistence ownership and executable proof remain required. |
| ADR-DLG-010 | Normative target specified in TS-DLG-04; executable adapters/migrations remain required. |
| ADR-DLG-011, ADR-DLG-012 | Normative target specified in TS-DLG-05; product checkpoint/impact adapters remain required. |
| ADR-DLG-005, ADR-DLG-013 | Normative target specified in TS-DLG-06; next-major schema correction remains for Stage 3. |
| ADR-DLG-014 | Normative target specified in TS-DLG-07; product set-evaluation adapters remain required. |
| ADR-DLG-016, ADR-DLG-018 | Normative target specified in TS-DLG-08; actual Control Tower/storage interfaces remain required. |
| ADR-DLG-019 | Benchmark plan specified in TS-DLG-08/09; empirical decision remains open. |
| ADR-DLG-020 | Release, evidence and rollback requirements specified in TS-DLG-04/09; Stage 3 publication remains unexecuted. |

`Specified` means the technical decision is written for review. It does not mean schemas are published, runtime behavior exists, upstream owners have ratified it or readiness evidence has passed.

## Stage 1 verdict

`CONCERNS` for proceeding to Stage 2. Specification authoring is justified and necessary, but no contract baseline should be published and no reference protocol implementation should begin until ADR-DLG-002 through ADR-DLG-018 have explicit resolutions and the cross-repository inputs are available.
