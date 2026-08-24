---
type: modular-prd
document_id: PRD-CA-01
title: Conscious Activation Engine — Engine Constitution & Canonical Architecture
version: 0.1
status: Draft for Phase 1
owner: Conscious Activation Engine Architecture
phase: 1
---

# 1. Purpose

PRD-CA-01 defines the canonical architectural and data-modeling foundation against which the remaining eight Conscious Activation Engine PRDs shall be designed.

The purpose is not to implement the entire engine. The purpose is to establish a stable semantic constitution so that later systems—World Intelligence, Relational Intelligence, SDA/SFL, Primitives, CCF, CMF, Runtime, and Measurement—share one coherent vocabulary, object model, lifecycle model, authority model, and lineage model.

This PRD is explicitly brownfield. Existing code, registries, YAML assets, schemas, skills, and pipelines must be inspected and classified before replacement or duplication is proposed.

# 2. Architectural Claim

The Conscious Activation Engine is a human-first intelligence and editing system. It organizes reality-grounded human evidence into progressively more structured representations and executable programs.

Canonical causal spine:

`WORLD → CONTEXT/STATE → RELATIONAL INTELLIGENCE → ACTIVE PRESSURE → PROVOCATION → HUMAN RESPONSE → AUTHENTICATED EVIDENCE → TRANSFORMATION → COMPOSITION → REALIZATION → RUNTIME → OUTCOME → MEMORY`

The engine therefore treats editing as the common operation across layers: selection, exclusion, combination, ordering, emphasis, and preservation.

# 3. Scope

PRD-CA-01 governs:

- ontology and taxonomy architecture
- artifact-class discipline
- canonical object constitution
- multidimensional object classification
- canonical/dynamic/evidence/derived separation
- relationship and state-model conventions
- provenance and lineage requirements
- architecture authority hierarchy
- legal/conversational/typed/executable representation boundaries
- brownfield reconciliation rules
- anti-centroid governance
- Phase 1 functional requirements and convergence rules

PRD-CA-01 does not implement the detailed runtime behavior of the eight downstream modules.

# 4. Canonical Data Philosophy

## 4.1 Logical schema is not physical storage

The logical schema remains conceptual and implementation-independent. PostgreSQL, JSONB, Pydantic/SQLModel, views, graph-like relations, vectors, and indexes are implementation mechanisms.

## 4.2 Storage policy

Stable semantics belong in typed columns and canonical relations. Important relationships must remain relational and addressable. Evolving hypotheses and optional attributes may use JSONB. Fuzzy semantic retrieval may use vectors. Temporal facts belong in event/state structures.

## 4.3 Evolution pattern

`JSONB hypothesis → validated concept → canonical object/column/relation`

This permits discovery without allowing experimental fields to silently become permanent ontology.

# 5. Multidimensional Object Classification

Every canonical object specification SHALL classify the object across independent dimensions:

1. artifact class
2. ontological plane
3. canonicality status
4. mutability mode
5. epistemic status
6. authority status
7. lifecycle
8. storage representation
9. runtime role

No single label such as "dynamic" or "canonical" is sufficient to define the object.

# 6. Ontological Planes

The canonical planes are:

### A — World / Context
Audience, Guest, Culture, Research Signal, Context Premise, Contextual State, Audience State, Guest State, Tension/Webhook, Cultural Memory.

### B — Semantic Discernment
Existential Invariant, Representation Geometry, Archetypal Geometry, Species Composition Grammar, Content Species, Recursive Pattern, Emergent Contextual Invariant, Feedback Loop, Directional Integrity Policy, Hard Negative.

### C — Transformation
Meaning Primitive, Experience Primitive, Primitive Candidate, Primitive Activation, Coalition, Edge Product.

### D — Perceptual / Delivery
SFL Function Family, SFL Function, SFL Function Stack, Perceptual Effect Metric, Influence Alignment Policy, Perceptual Failure Asset, Composition Depth Profile, Variation Profile.

### E — Realization
Format, Archetype Container, Scene, SceneInstance, Composition, CompositionInstance, Media Role, Visual Primitive, Sonic Primitive, Visual Syntax, Executable Video IR.

### F — Runtime / Governance
Agent Role, Skill, Program, Contract, Directive, Query Plan, Error Taxonomy, Repair Plan, Receipt, Evaluation, Fatality.

# 7. Canonical Object Constitution

Every canonical object SHALL be specified using the Phase 0 Object Constitution, with class-specific grammar:

1. Canonical Identity
2. Artifact Class
3. Ontological Plane
4. Architectural Role
5. Definition
6. Semantic Boundary
7. Nearest Neighbors
8. Taxonomic Position
9. Lifecycle / Canonicity
10. Attributes
11. Relationships
12. State Model
13. Events
14. Provenance
15. Invariants
16. Authority / Owner
17. Authorized Operations
18. Prohibited Operations
19. Validators
20. Error Taxonomy
21. Storage Representation
22. Runtime Consumers
23. Questions This Object Answers
24. Examples
25. Hard Negatives
26. Version History

The object-specific definition grammar is determined by artifact class; it must not be flattened into one universal prose pattern.

# 8. Brownfield Rule

Before introducing or changing an object, registry, schema, agent, or runtime component, the repository must be inspected and the current behavior classified as:

`EXISTS | PARTIAL | DUPLICATED | CONFLICTING | SPEC-ONLY | MISSING | DEPRECATED`

The target action must then be:

`PATCH | EXTEND | REFACTOR | REPLACE | MERGE | DEPRECATE | NEW`

A spec cannot declare an existing feature "new" without repository evidence.

# 9. Anti-Centroid Constitutional Requirement

The architecture exists to increase precision, not to introduce generic safety-language, permission inflation, corporate neutrality, unnecessary hedging, or sterilization of meaningful tension.

A dedicated Anti-Centroid Patrol must detect:

- statistical mean-reversion
- abstract substitutions for concrete evidence
- unnecessary moralizing
- irrelevant authorization language
- over-sanitization
- dilution of contradiction or tension
- institutionalized prose replacing native language

The patrol may emit `PASS | WARN | REPAIR | ESCALATE | BLOCK`, but BLOCK requires an actual architectural violation rather than merely an unconventional creative choice.

# 10. Human-First Evidence Law

Research and models may surface hypotheses, pressures, or prompts. They do not constitute authenticated guest evidence.

When a workflow requires guest-specific lived evidence:

`Hypothesis → Provocation → Human Response → Authentication → Downstream Right to Render`

No authenticated response means downstream generation has not earned the right to represent that guest-specific truth as authenticated evidence.

# 11. Functional Requirement Registry

Phase 1 defines the following FRs:

- FR-CA-01-001 Canonical Architecture Registry
- FR-CA-01-002 Multidimensional Object Classification
- FR-CA-01-003 Object Constitution Conformance
- FR-CA-01-004 Ontology and Taxonomy Registry
- FR-CA-01-005 Relationship Model Governance
- FR-CA-01-006 Dynamic State and Temporal Model Governance
- FR-CA-01-007 Evidence and Provenance Model
- FR-CA-01-008 Derived Artifact Lineage
- FR-CA-01-009 Brownfield Inventory and Reconciliation
- FR-CA-01-010 Storage Strategy: SQL + JSONB + Vector + Event Model
- FR-CA-01-011 Agent Query Governance and Authorized Semantic Functions
- FR-CA-01-012 Architecture Error Taxonomy
- FR-CA-01-013 Anti-Centroid Patrol and Density Preservation
- FR-CA-01-014 Director Note / Prose-to-Directive Translation
- FR-CA-01-015 Architecture Change Control and Versioning

# 12. Acceptance Criteria for PRD-CA-01

PRD-CA-01 is ready for convergence only when:

- every Phase 1 object has a primary artifact class;
- each object has a canonical plane and architectural role;
- canonical/dynamic/evidence/derived distinctions are explicit;
- class-specific definition grammars are mapped;
- relationships and state families are named before tables are finalized;
- brownfield evidence exists for current-code status;
- anti-centroid governance is explicit and non-sanitizing;
- data storage strategy is derived from object role rather than convenience;
- all proposed agent-accessible operations have authority boundaries;
- error taxonomy exists for object/schema/relation/state/evidence/semantic/composition/runtime failure;
- every FR contains acceptance criteria and source lineage.

# 13. Convergence to Technical Specifications

Functional Requirements SHALL converge later through:

`FR → acceptance criteria → data dependencies → state/event model → API/function boundaries → SQL/JSONB/vector/graph strategy → tests → migration → runtime observability`

No FR should become a technical specification merely by adding implementation jargon. The semantic contract must remain primary.
