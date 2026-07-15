---
title: Delegation Architecture Baseline Manifest
product: CMF Content Harness Visual Asset Editor Delegation Protocol
stage: 1
status: baseline_with_open_deltas
created: 2026-07-14
---

# Architecture Baseline Manifest

## Authority hierarchy

1. The Delegation Sharded PRD and decisions `D001` through `D016` govern the shared boundary.
2. The Atomic Harness Builder and Visual Asset Editor PRDs are read-only product-boundary authorities.
3. This repository owns shared public contract schemas, protocol versions and compatibility semantics.
4. The Content Harness owns demand meaning, Activative purpose, sequence and asset roles, composition intent, identity and continuity constraints, wrong-reading locks, delivery requirements and budget authorization.
5. The Visual Asset Editor owns Visual Production Plans, workflow/model/provider selection, candidate generation, evaluation and repair, production acceptance, production receipts and asset lineage.
6. The Delegation Protocol owns contract validation, field-authority validation, compatibility negotiation, external lifecycle rules, idempotency/replay controls, routing semantics, audit receipts and shared Control Tower projections. It owns no creative or visual-production decisions.

## Current local baseline

| Baseline capability | Repository evidence | Verified state |
|---|---|---|
| Product requirements | `prd/`, `governance/REQUIREMENTS_REGISTRY.yaml` | 16 features, 128 FRs, 60 NFRs and 14 journeys registered |
| Locked decisions | `governance/DECISION_REGISTER.json` | 16 locked decisions |
| Architecture constraints | `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`, `governance/ARCHITECTURAL_PROHIBITIONS.json` | Declarative and binding for specification work |
| Shared contract family | `contracts/schemas/`, `contracts/examples/` | 25 draft schemas and examples; syntactically valid, semantically underconstrained |
| Message registry | `governance/MESSAGE_TYPE_REGISTRY.yaml` | Draft inventory exists; producer naming and ownership ambiguities remain |
| Field authority | `governance/AUTHORITY_MATRIX.yaml`, `governance/PRINCIPAL_AUTHORITY_REGISTRY.yaml` | Domain-level map exists; field-level register added in Stage 1 |
| Lifecycle | `governance/LIFECYCLE_MACHINE.yaml` | 19 states and 32 transitions declared; no executable engine |
| Failure taxonomy | `governance/FAILURE_TAXONOMY.yaml` | Stable draft families/codes declared; no runtime classifier |
| Compatibility | `governance/COMPATIBILITY_POLICY.yaml` | Verdicts and policy declared; no negotiator, adapters or migration execution |
| Integrity/audit | Envelope and audit-receipt schemas | Data shape exists; no canonicalization, signing, replay or durable chain implementation |
| Conformance | `conformance/` | Declarative cases only |
| Release 1 reference | `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/` | Local fixtures exist; no product adapters or cross-repository run |
| Readiness governance | `governance/READINESS_HARD_GATES.yaml` | Gate model exists; evidence is insufficient for implementation authorization |

## Preserved upstream architecture

The following boundaries are binding and require no replacement architecture in this repository:

- three independent products and compilation targets;
- Builder-owned Harness IR, Capability Ownership Map, Phase/Context Graphs, Typed Contract Graph, Skill Ecology, deterministic JIT compiler and Development Capsule;
- Content Harness-owned semantic, Activative, sequence, composition, identity and continuity authority;
- VAE-owned Visual Production Plan IR, production workflows, compute fabric, candidate generation, VLM evaluation, repair, production acceptance and visual memory;
- existing Harness Control Tower as the projection host and source-of-truth boundary;
- smallest-responsible repair and selective invalidation principles;
- formal implementation authorization based on executable evidence.

The local checkout contains declarative preservation rules but not the upstream code or product PRD bodies needed to prove that proposed interfaces fit their actual adapter surfaces.

## Target component baseline

The technical specifications must define a transport-neutral reference architecture with these responsibility boundaries:

| Component | Owned responsibility | Explicit exclusions |
|---|---|---|
| Contract registry | Canonical schema IDs, message versions, producers/consumers, authority scopes and change policy | Product-internal models |
| Envelope validator | Canonical encoding, schema/hash/signature/reference validation and validation order | Credential issuance and creative interpretation |
| Authority policy engine | Principal permissions and field-level mutation authorization | Human/product authority decisions |
| Compatibility service | Manifest validation, negotiation, pinning, adapter selection and migration evidence | Best-effort semantic coercion |
| Lifecycle engine | Deterministic external states, transitions, precedence and terminal/post-completion behavior | Product-internal state machines |
| Idempotency/replay service | Duplicate resolution, nonce/replay rejection and durable key state | Transport delivery guarantees |
| Delegation coordinator | Transactional validation, persistence, routing and correlation | VAE scheduling or Content Harness sequencing |
| Audit ledger | Append-only chained receipts and historical verification | Mutable operational source of truth |
| Projection adapter | Delegation views in the existing Harness Control Tower | A second Control Tower or authority store |
| Conformance runtime | Producer, consumer, authority, lifecycle, compatibility, resilience and Format 02 execution | Product-quality evaluation |

No target component is implemented locally.

## Persistence and transaction baseline

No data store, event store, idempotency store, nonce store, audit store, object-store contract, transaction boundary, consistency model, partition key, retention policy, recovery procedure or migration mechanism exists. Stage 2 must define:

- atomic acceptance of message, authority result, lifecycle transition and audit receipt;
- ordering and race precedence per delegation correlation;
- durable idempotency and replay records with separate semantics and retention;
- append-only audit sequencing and safe behavior during audit-store interruption;
- immutable contract/resource storage through stable references and hashes;
- reconstruction checkpoints and replay-safe projection recovery;
- historical retention for superseded, invalidated, revoked and replaced facts.

## Security baseline

The envelope declares signer, signature algorithm, signature, issuance/expiry and nonce, and the principal registry names allowed actions. No canonical byte representation, key identity format, trust root, KMS/HSM boundary, algorithm suite, rotation/revocation model, nonce scope, clock-skew policy, incident sink or historical verification design exists.

## Delivery and operations baseline

There is no deployment topology, service ownership map, environment model, release pipeline, contract publication registry, observability implementation, dashboard, alerting integration, rollback process or disaster-recovery design. SLO targets are draft and explicitly architecture-tunable.

## Missing technical specifications

The minimum specification set is the ten `TS-DLG` documents named in the Stage 2 plan. Cross-cutting decisions that must be resolved across those specifications are:

- canonical schema identity, payload versioning and generated binding policy;
- field-level and conditional authority, especially admission receipts and result authorization;
- closed nested schemas and governed extension points;
- canonical serialization, hashing and signing;
- idempotency versus hostile replay behavior;
- lifecycle ordering, race precedence, persistence and reconstruction;
- transport-neutral ports and routing guarantees;
- adapter/migration equivalence evidence;
- Control Tower projection contract;
- retention, privacy, negative evidence and historical truth;
- measurable SLO budgets and benchmark design.

## Cross-repository blockers

- The Builder and VAE PRD/source packages referenced by hashes are absent, so exact architecture and provisional-schema diffs cannot be reproduced.
- Content Harness and VAE implementation repositories and adapter surfaces are absent.
- The existing Harness Control Tower schema/API is absent.
- Product identity, key management and governed storage infrastructure are unspecified.
- No pinned product releases exist for executable Format 02 integration.
- No contract publication target or release mechanism is configured.

These blockers do not prevent careful Stage 2 specification authoring. They do prevent contract freeze, implementation authorization and claims of cross-product conformance.

## Constitutional alignment overlay — 2026-07-14

The historical Stage 1 inventory above is preserved as discovery evidence.
The current local architecture now includes the transport-neutral reference
engine, closed generated contract family, deterministic validators, executable
Format 02 fixtures, and compatibility/migration runner under package candidate
`1.1.0-rc.1`. The Constitution `1.1.0` and Delegation PRD V1.1 control
Activative and visual meaning. This overlay does not change the target
component boundaries, lifecycle, transport neutrality, or external production
blockers, and it does not authorize production.

## Historical Stage 1 baseline verdict

`CONCERNS` for proceeding to specification authoring. The requirements, decisions and local draft contract family are coherent enough to specify, but specifications must carry the unresolved ownership and cross-repository deltas as blocking acceptance criteria. Stage 3 and Stage 5 remain blocked.
