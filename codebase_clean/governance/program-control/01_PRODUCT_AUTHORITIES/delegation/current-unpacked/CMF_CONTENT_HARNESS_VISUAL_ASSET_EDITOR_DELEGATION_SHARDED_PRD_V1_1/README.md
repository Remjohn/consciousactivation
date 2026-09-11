# CMF Content Harness ↔ Visual Asset Editor Delegation Protocol — Sharded PRD V1.1

**Product version:** `0.2.0-draft`  
**Artifact status:** `draft_for_review`  
**Mechanical validation:** `PASS`  
**Implementation authorization:** `NOT YET AUTHORIZED`

This package compiles the 16 locked delegation decisions into a complete, sharded product definition for the shared boundary between an Atomic Content Harness and the CMF Visual Asset Editor.

## Product boundary

```text
Content Harness
→ immutable Visual Asset Demand
→ deterministic Delegation Protocol validation and negotiation
→ Visual Asset Editor production
→ production-accepted Asset Result
→ deterministic result validation
→ Content Harness consumption acknowledgement
→ downstream composition
```

The protocol owns shared contracts, authority enforcement, compatibility, lifecycle, idempotency, integrity, routing, supersession, cancellation, amendment exchange, acknowledgement, post-completion governance and audit. It owns no visual meaning or production strategy.

## Package counts

```text
Locked decisions:                  16
Behavioral feature shards:         16
Functional Requirements:          128
Non-Functional Requirements:       60
User and system journeys:          14
Contract schemas:                  25
Representative contract examples: 25
Format 02 scenarios:               10
```

## Constitutional amendment

The binding [`Delegation V1.1 Semantic Contract Preservation Amendment`](amendments/DELEGATION_V1_1_SEMANTIC_CONTRACT_PRESERVATION_AMENDMENT.md) expands the canonical shared demand so compatibility and adapters preserve the complete Activative visual contract.

## Start here

- [Sharded PRD index](prd/index.md)
- [Combined PRD](prd/PRD_COMBINED.md)
- [Decision Register](governance/DECISION_REGISTER.md)
- [Requirements Registry](governance/REQUIREMENTS_REGISTRY.yaml)
- [Traceability Matrix](governance/TRACEABILITY_MATRIX.csv)
- [Protocol Constitution](governance/PROTOCOL_CONSTITUTION.yaml)
- [Authority Matrix](governance/AUTHORITY_MATRIX.yaml)
- [Lifecycle Machine](governance/LIFECYCLE_MACHINE.yaml)
- [Failure Taxonomy](governance/FAILURE_TAXONOMY.yaml)
- [Compatibility Policy](governance/COMPATIBILITY_POLICY.yaml)
- [Readiness Hard Gates](governance/READINESS_HARD_GATES.yaml)
- [Contract family](contracts/README.md)
- [Format 02 reference slice](reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/README.md)
- [Conformance suites](conformance/README.md)
- [Validation report](validation/PRD_VALIDATION_REPORT.md)

## Canonical feature shards

- [F01 — Governed Protocol Boundary and Deterministic Boundary Services](prd/05-features/F01-protocol-boundary.md)
- [F02 — Visual Asset Demand Ownership, Immutability, and Authority](prd/05-features/F02-demand-ownership.md)
- [F03 — Immutable Contract Family and Common Delegation Envelope](prd/05-features/F03-contract-family.md)
- [F04 — Stable External Lifecycle and Deterministic Projection](prd/05-features/F04-external-lifecycle.md)
- [F05 — Demand Supersession, Impact Analysis, and Selective Invalidation](prd/05-features/F05-supersession-invalidation.md)
- [F06 — Production Acceptance and Downstream Consumption Acknowledgement](prd/05-features/F06-result-acknowledgement.md)
- [F07 — Budget Authorization, Allocation, Escalation, and Cost Receipts](prd/05-features/F07-budget-authority.md)
- [F08 — Cancellation, Deadlines, Safe Checkpointing, and Race Resolution](prd/05-features/F08-cancellation-deadlines.md)
- [F09 — Protocol Failure Taxonomy, Responsibility, and Recovery Semantics](prd/05-features/F09-failure-taxonomy.md)
- [F10 — Delegation Sets, Shared Continuity, Dependencies, and Group Evaluation](prd/05-features/F10-delegation-sets.md)
- [F11 — Semantic Compatibility, Negotiation, Adapters, Migration, and Deprecation](prd/05-features/F11-compatibility-migration.md)
- [F12 — Typed Amendment Proposals and Authority-Governed Resolution](prd/05-features/F12-amendment-protocol.md)
- [F13 — Post-Completion Invalidation, Revocation, Supersession, and Replacement](prd/05-features/F13-post-completion-governance.md)
- [F14 — Principal Identity, Message Integrity, Replay Protection, and Audit Chain](prd/05-features/F14-trust-integrity.md)
- [F15 — Delegation Observability, SLOs, Conformance, and Resilience](prd/05-features/F15-observability-conformance.md)
- [F16 — Delegation Readiness, Development Capsule, and Production Certification](prd/05-features/F16-implementation-readiness.md)

## Shared contract family

The package defines the common Delegation Envelope and 24 domain payload/message schemas for demand, submission, events, Delegation Sets, budgets, cancellation, conflicts, amendments, supersession, selective invalidation, results, acknowledgements, post-completion notices, failures, audit, compatibility and migration.

The schemas are product requirements and validated reference fixtures. Architecture must still bind them to concrete storage, transport, authentication, signing, event processing, availability and deployment mechanisms.

## Format 02 reference slice

Release 1 is proven through **Format 02 — Minimal Coach Theatre** in the `2d_character_animation` category. Ten reference scenarios cover the happy path, Delegation Sets, supersession, budgets, amendments, cancellation, acknowledgement, invalidation/replacement, authority violations, compatibility migration and replay resilience.

## What happens next

1. Review and approve this PRD.
2. Produce the Delegation Protocol Architecture and ADR package.
3. Finalize the contract family and execute shared schema/authority/lifecycle fixtures.
4. Implement producer and consumer adapters for the Format 02 reference products.
5. Build the Control Tower projection and append-only audit chain.
6. Run conformance, resilience and cross-product end-to-end suites.
7. Issue `IMPLEMENTATION_AUTHORIZED` only after every readiness hard gate passes.

## Validation commands

```bash
python scripts/rebuild_combined_prd.py
python scripts/rebuild_manifest.py
python scripts/validate_package.py
```
