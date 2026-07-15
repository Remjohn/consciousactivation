---
title: Cross-Cutting Non-Functional Requirements
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 6. Cross-Cutting Non-Functional Requirements

These requirements apply across all protocol features and product implementations.

## NFR-AUTH — Authority and sovereignty

### NFR-AUTH-001

Every authority-bearing field and action shall map to exactly one owning product or protocol service.

### NFR-AUTH-002

Authority validation shall be deterministic and complete before any lifecycle mutation.

### NFR-AUTH-003

Budget, cancellation, amendment, result, and revocation actions shall require an authenticated permitted principal.

### NFR-AUTH-004

Automatic policy decisions shall be bounded by explicit fields, ranges, versions, and owning authority.

### NFR-AUTH-005

No adapter, migration, projection, or transport shall transfer creative or production authority implicitly.

## NFR-CONTRACT — Contract quality and schema discipline

### NFR-CONTRACT-001

All state-changing payloads shall be immutable, versioned, schema-validatable, and hash-addressable.

### NFR-CONTRACT-002

Every authoritative reference shall identify its exact version and content hash.

### NFR-CONTRACT-003

Failure and exception contracts shall contain stable classification, ownership, recovery, and invalidation semantics.

### NFR-CONTRACT-004

Delegation Set schemas shall preserve member-level identity and lifecycle while expressing shared constraints.

### NFR-CONTRACT-005

Compatibility and migration shall preserve all mandatory semantics, not merely syntactic parseability.

## NFR-LIFE — Lifecycle correctness

### NFR-LIFE-001

The shared lifecycle shall be represented by an executable deterministic transition machine.

### NFR-LIFE-002

Supersession shall prevent stale result promotion and preserve valid reusable work.

### NFR-LIFE-003

COMPLETED shall require valid production acceptance and downstream consumption acknowledgement.

### NFR-LIFE-004

Cancellation shall stop new work promptly, checkpoint safely, and prevent later stale promotion.

### NFR-LIFE-005

Delegation Set status shall be derived from member state and declared completion policy.

## NFR-REL — Reliability, idempotency, and consistency

### NFR-REL-001

Every accepted state change shall be idempotent under legitimate duplicate delivery.

### NFR-REL-002

Shared lifecycle projection shall be reconstructible from accepted immutable messages and receipts.

### NFR-REL-003

Selective invalidation shall preserve unaffected evidence and outputs with explicit lineage.

### NFR-REL-004

Automatic result acknowledgement shall be deterministic for identical current dependencies.

### NFR-REL-005

Message races shall resolve through accepted order, causation, precedence, and lifecycle state rather than network timing.

## NFR-COMPAT — Compatibility and evolution

### NFR-COMPAT-001

Products shall publish signed machine-readable compatibility manifests for every release.

### NFR-COMPAT-002

Negotiation shall verify required behaviors, authority, profiles, and receipts in addition to schema versions.

### NFR-COMPAT-003

Running delegations shall pin negotiated versions and shall not silently upgrade.

### NFR-COMPAT-004

Adapters and migrations shall be deterministic, versioned, fixture-tested, and semantically lossless for required fields.

### NFR-COMPAT-005

Deprecation shall preserve accepted in-flight delegations and publish replacement and retirement timelines.

## NFR-SEC — Security and integrity

### NFR-SEC-001

Every state-changing principal shall be authenticated and authorized for the exact requested action.

### NFR-SEC-002

Message and payload integrity shall be verifiable before persistence or routing.

### NFR-SEC-003

Replay protection shall distinguish benign idempotent retry from unauthorized message replay.

### NFR-SEC-004

Credentials shall support issuance, rotation, revocation, and historical verification.

### NFR-SEC-005

Integrity and authority failures shall block state change and emit a security incident without ordinary retry.

## NFR-TRACE — Traceability and auditability

### NFR-TRACE-001

Every protocol action shall trace to source decision, requirement, message, principal, and resulting lifecycle effect.

### NFR-TRACE-002

Demand-owned values shall retain evidence of owner, version, hash, and supersession lineage.

### NFR-TRACE-003

Correlation and causation shall connect every message and receipt in a delegation.

### NFR-TRACE-004

Lifecycle projections shall identify the authoritative message and transition rule.

### NFR-TRACE-005

Selective invalidation shall explain field changes, preserved artifacts, invalidated artifacts, and resume point.

## NFR-OBS — Observability and operations

### NFR-OBS-001

Delegation state shall be visible through the validated Harness Control Tower, not a second source of truth.

### NFR-OBS-002

Every non-terminal failure shall expose responsible owner, next action, retry class, and remaining quality rounds.

### NFR-OBS-003

Control Tower projections shall expose compatibility, authority, budget, timing, latest event, exceptions, and acknowledgements.

### NFR-OBS-004

Stalled, orphaned, superseded-but-producing, and unacknowledged delegations shall be detectable.

### NFR-OBS-005

Critical invalidation, revocation, integrity, and audit-chain incidents shall trigger operational escalation.

## NFR-PERF — Performance and service levels

### NFR-PERF-001

Budget validation and escalation shall prevent unapproved work from exceeding hard ceilings.

### NFR-PERF-002

The protocol shall define measurable SLOs for acceptance, event delivery, projection freshness, acknowledgement, and critical notice propagation.

### NFR-PERF-003

Boundary validation shall add bounded overhead independent of asset-generation duration.

### NFR-PERF-004

Large media shall be referenced rather than copied through protocol messages.

## NFR-RES — Resilience and recovery

### NFR-RES-001

Cancellation, restart, and transport interruption shall preserve safe checkpoints and immutable receipts.

### NFR-RES-002

Infrastructure failures shall be recoverable without consuming visual quality-repair rounds.

### NFR-RES-003

Duplicate, delayed, out-of-order, and temporarily undeliverable messages shall not create duplicate production or illegal transitions.

### NFR-RES-004

Boundary-service restart shall restore projections and idempotency state from durable records.

### NFR-RES-005

Audit-store interruption shall fail safely and prevent unaudited state-changing acceptance.

## NFR-DATA — Data retention, privacy, and historical truth

### NFR-DATA-001

Delegation Sets and member contracts shall retain independent lineage and exact consumed versions.

### NFR-DATA-002

Invalidated, revoked, superseded, and replaced artifacts shall remain historically reproducible under retention policy.

### NFR-DATA-003

Protocol messages shall minimize data and exclude secrets, large media, and unnecessary private reasoning traces.

### NFR-DATA-004

Large resources shall use access-controlled stable references and hashes with retention and availability policies.

### NFR-DATA-005

Negative and revoked evidence may support diagnosis and evaluation but shall be excluded from ordinary production reuse.

## NFR-GOV — Governance, quality, and certification

### NFR-GOV-001

The protocol shall preserve the validated Builder, Content Harness, and Visual Asset Editor architectures.

### NFR-GOV-002

Semantic, Activative, sequence, composition, identity, and continuity authority shall not be silently weakened.

### NFR-GOV-003

Cost, latency, or convenience shall never override constitutional quality or authority gates.

### NFR-GOV-004

Compatibility claims shall require executable evidence against declared fixtures.

### NFR-GOV-005

Constitutional amendments shall route upstream and cannot be approved through ordinary delegation.

### NFR-GOV-006

Production certification shall declare exact product versions, contract versions, profile scope, limitations, rollback, and conformance evidence.
