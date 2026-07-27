---
title: F03 — Canonical Asset Ontology and Reference/Production Separation
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F03
governing_decisions:
- D005
- D006
- D007
- D025
- D026
- D027
user_journeys:
- UJ-01
- UJ-03
- UJ-09
- UJ-14
functional_requirement_count: 8
---


# F03 — Canonical Asset Ontology and Reference/Production Separation

**User outcome:** A caller and the editor can describe asset production needs with reusable families while preserving one harness-specific role and Activative purpose.

## Description

This feature defines canonical asset families, subtypes, role bindings, Reference Evidence, Production Assets, and explicit promotion.

## Brownfield baseline

V2.1 distinguishes reference evidence from production assets and defines broad asset responsibilities. The product requires a formal shared ontology that supports routing and evaluation without flattening harness-specific meaning.

## Required product delta

Create a versioned ontology for eight families, extendable subtypes, harness roles, asset classes, typed relationships, promotion rules, and certification scope.

## Traceability

- **Decisions:** D005, D006, D007, D025, D026, D027
- **User journeys:** UJ-01, UJ-03, UJ-09, UJ-14
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-017 — Maintain eight canonical asset families

**Requirement:** The ontology must initially define documentary/photographic evidence, human/character assets, illustrated/generated scenes, UI/screen surfaces, diagrammatic/informational assets, typography/graphic elements, compositing/scene components, and motion/temporal assets.

**Consequences (testable):

- Every demand selects one registered family and compatible subtype.

- Unknown families cannot route to production until governed ontology extension.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-018 — Bind harness-specific roles and Activative functions

**Requirement:** A canonical family record must be combined with a requesting harness role, sequence or scene position, visual-syntax function, and Activative function.

**Consequences (testable):

- Two demands may share an asset family while retaining distinct semantic and composition roles.

- The ontology may not replace or generalize away the harness-specific role.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-019 — Represent Reference Evidence explicitly

**Requirement:** Material used for understanding, conditioning, identity, pose, environment, composition, continuity, evaluation, or inspiration must be stored as Reference Evidence unless explicitly promoted.

**Consequences (testable):

- Reference records state relationships to demands and production plans.

- Reference Evidence cannot be emitted as an authorized final asset by default.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-020 — Represent Production Assets explicitly

**Requirement:** A Production Asset must be an immutable, evaluated artifact authorized for one or more declared downstream uses and linked to its demand, plan, lineage, geometry, and receipts.

**Consequences (testable):

- Downstream composition can verify production authorization from the asset record.

- An unpromoted candidate or reference cannot satisfy an Asset Result Contract.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-021 — Require explicit reference-to-production promotion

**Requirement:** When a reference is reused or transformed into production, the system must record the promotion event, transformation, evaluator results, source policy, and new immutable Production Asset identity.

**Consequences (testable):

- Promotion preserves the original reference record and creates a distinct production lineage.

- Folder movement or filename change alone cannot promote an asset.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-022 — Publish subtype capability requirements

**Requirement:** Each subtype must declare eligible routes, required controls, compatible workflows/models, evaluator dimensions, geometry needs, continuity rules, and delivery types.

**Consequences (testable):

- The router can determine whether certified capabilities exist before plan execution.

- A subtype without capability requirements remains structurally represented but uncertified.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-023 — Version and migrate ontology records

**Requirement:** Asset-family and subtype changes must be versioned, compatibility-scoped, and migration-tested against dependent demands, plans, memory records, and results.

**Consequences (testable):

- Existing assets preserve the ontology version used at production time.

- A taxonomy rename cannot silently reinterpret historical records.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-024 — Expose certified scope separately from represented scope

**Requirement:** The ontology and UI must mark each family/subtype as represented, experimental, limited-production, production-certified, deprecated, or retired.

**Consequences (testable):

- Release 1 reports Format 02 character-and-scene capabilities as certified scope only after benchmarks pass.

- Structurally defined families cannot be marketed or routed as production-ready.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
