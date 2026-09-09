---
type: canonical-object-model
id: CA-ARCH-002
title: Conscious Activation Engine — Object Constitution Protocol
version: 0.1
status: Phase 0 Foundation
---

# 1. Purpose

This document defines the universal constitutional frame used to describe objects in the Conscious Activation Engine.

It does **not** make every object semantically identical. The constitutional dimensions are shared; the definition grammar, required fields, lifecycle, validators, and operational permissions vary by artifact class.

# 2. Global Object Constitution

Every canonical object specification SHOULD be written using these dimensions, in this order:

I. CANONICAL IDENTITY  
II. ARTIFACT CLASS  
III. ONTOLOGICAL PLANE  
IV. ARCHITECTURAL ROLE  
V. DEFINITION  
VI. SEMANTIC BOUNDARY  
VII. NEAREST NEIGHBORS  
VIII. TAXONOMIC POSITION  
IX. LIFECYCLE / CANONICITY  
X. ATTRIBUTES  
XI. RELATIONSHIPS  
XII. STATE MODEL  
XIII. EVENTS  
XIV. PROVENANCE  
XV. INVARIANTS  
XVI. AUTHORITY / OWNER  
XVII. AUTHORIZED OPERATIONS  
XVIII. PROHIBITED OPERATIONS  
XIX. VALIDATORS  
XX. ERROR TAXONOMY  
XXI. STORAGE REPRESENTATION  
XXII. RUNTIME CONSUMERS  
XXIII. QUESTIONS THIS OBJECT ANSWERS  
XXIV. EXAMPLES  
XXV. HARD NEGATIVES  
XXVI. VERSION HISTORY

# 3. Mandatory Meta-Law

**Role must be established before schema convenience.**

If an artifact cannot be assigned to one primary class, it is not ready for canonicalization.

# 4. Artifact Class Registry

Allowed primary classes:

1. Entity
2. Value Object
3. Relation
4. State
5. Event
6. Immutable Evidence
7. Canonical Ontology
8. Canonical Structural Grammar
9. Transformation Operator
10. Experience / Perceptual Function
11. Policy / Contract
12. Derived Semantic Artifact
13. Execution Packet
14. Intermediate Representation
15. Adversarial Evaluation Asset
16. Receipt / Evaluation Record
17. Crosswalk / Mapping Object
18. Longitudinal Memory Record

A single artifact may participate in multiple planes but MUST have one primary artifact class.

# 5. Canonicality Dimensions

Canonically classify objects across independent axes rather than forcing one lifecycle label to do every job.

## 5.1 Canonicality

- `canonical`
- `contextual`
- `runtime`
- `derived`
- `experimental`

## 5.2 Mutability

- `immutable`
- `versioned`
- `stateful`
- `recomputable`
- `ephemeral`

## 5.3 Epistemic Status

- `established`
- `supported`
- `proposed`
- `hypothesis`

## 5.4 Authority Status

- `constitutional`
- `registry-governed`
- `program-governed`
- `runtime-observed`
- `human-authored`

These axes are independent. For example, a canonical ontology object may be versioned, constitutional, and evidence-backed. A runtime state may be stateful, derived, and observed.

# 6. Definition Grammar Law

Definitions do NOT use one universal grammar.

Every definition MUST express, appropriate to its artifact class:

- **Genus:** what larger kind of thing it is.
- **Differentia:** what distinguishes it from its nearest neighbors.
- **Function:** why the system needs it.
- **Boundary:** what it must not be confused with.

The amount of text is determined by semantic complexity, not a fixed word count.

Target ranges are guidance only:

| Class | Target range |
|---|---:|
| Value Object | 30–70 words |
| Entity | 70–130 |
| Relation | 60–120 |
| State | 70–140 |
| Event | 50–110 |
| Evidence | 60–120 |
| Ontology Object | 120–220 |
| Structural Grammar | 150–300 |
| Transformation Operator | 150–300 |
| Policy / Contract | 150–350 |
| Derived Artifact | 100–200 |
| Execution Packet | 80–160 |
| IR Object | 100–200 |
| Adversarial Asset | 100–220 |

The controlling rule is:

> A definition is sufficiently long when identity, function, boundary, and semantic distinction are explicit without requiring the reader to infer them.

# 7. Object-Specific Definition Grammar Protocols

## 7.1 Entity

An Entity definition MUST establish persistent identity, continuity, system purpose, distinguishing characteristics, and relation to state/event records.

Pattern:

> `[Entity] is a [genus] representing [persistent identity] for [system purpose]. Unlike [nearest neighbor], it [differentia]. Runtime conditions are represented separately as [state type]; observations are represented as [event/evidence type].`

## 7.2 Value Object

A Value Object is defined by semantic content rather than independent identity.

Pattern:

> `[Value Object] is a [descriptive semantic value] used to represent [purpose]. Its identity is determined by its value and context rather than by an independent lifecycle identity.`

## 7.3 Relation

A Relation MUST define subject, object, direction, semantics, temporal behavior where relevant, and evidentiary meaning.

Pattern:

> `[Relation] asserts that [subject] bears [typed relationship] to [object] under [conditions]. It exists to establish [system use]. The relation does / does not imply [critical distinction].`

No generic authorization language shall be inserted unless authorization is genuinely part of the relation's ontology.

## 7.4 State

A State definition MUST establish the underlying thing whose condition is represented, the temporal boundary, transition semantics, observation basis, and non-overwrite rule.

Pattern:

> `[State] is a temporally bounded representation of [entity/relationship/field] under [condition]. It records [relevant dimensions] at [observation interval]. It may transition through [states] and MUST preserve prior observations.`

## 7.5 Event

An Event definition MUST specify occurrence, trigger, payload, temporal identity, and effect on state or lineage.

## 7.6 Immutable Evidence

Evidence definitions MUST specify origin, acquisition context, authenticity boundary, immutability, and allowed derivative use.

## 7.7 Canonical Ontology Object

Ontology objects MUST define semantic identity, scope, stable boundaries, neighboring concepts, and evidence status. They change slowly and must not be inferred solely from runtime convenience.

## 7.8 Structural Grammar

Structural grammar definitions MUST define components, topology, valid composition, invalid composition, and transformation invariants.

## 7.9 Transformation Operator / Primitive

A Primitive MUST specify:

- transformation performed
- substrate acted upon
- activation conditions
- expected directional effect
- admissible operating range
- coalition relations
- failure patterns
- evidence basis

Runtime activation MUST create a separate `PrimitiveActivation` object and MUST NOT mutate the Primitive definition.

## 7.10 Experience / Perceptual Function

The definition must specify perceptual or behavioral modulation, target state, delivery conditions, positive-space intent, negative-space boundary, and measurable effects.

## 7.11 Policy / Contract

A Policy or Contract MUST state subject, jurisdiction, obligations/permissions/prohibitions where applicable, precedence, exceptions, failure handling, and validation.

Normative language SHALL protect architectural properties and declared quality standards. It SHALL NOT introduce generic sanitization merely because a statement could sound safer.

## 7.12 Derived Semantic Artifact

A derived artifact MUST specify inputs, derivation basis, provenance, confidence, reproducibility, expiry/recomputation conditions, and non-canonical status unless separately promoted.

## 7.13 Execution Packet

Must be purpose-built for runtime transfer. Schema SHALL favor typed fields, lineage identifiers, statuses, measurements, and compact machine-readable payloads.

## 7.14 Intermediate Representation

An IR MUST specify source abstractions, normalized form, target assumptions, semantic invariants, transformation rules, and execution eligibility.

## 7.15 Adversarial Evaluation Asset

A hard negative or mutation suite MUST be contrastive. It must specify positive anchor, deceptive variant, divergence axes, expected failure, and test conditions.

## 7.16 Receipt / Evaluation Record

A receipt MUST answer: what happened, under which inputs, under which program/contract version, what decisions occurred, what measurements resulted, and whether fatality or repair occurred.

# 8. Positive-Space / Anti-Centroid Requirement

Every object constitution involving content generation, editing, composition, or runtime reasoning SHOULD identify:

- desired positive-space properties
- known centroid failure patterns
- relevant hard negatives

The purpose is to preserve meaningful distinction, not suppress legitimate creative variance.

# 9. Storage Law

Logical schema precedes physical storage.

Preferred representations:

- typed relational columns for stable semantics
- explicit join tables for important relations
- JSONB for evolving or experimental attributes
- vector indexes for fuzzy retrieval
- event tables for temporal observations
- views/functions for governed access
- immutable evidence stores for primary evidence

JSONB SHALL NOT become an unbounded prose warehouse.
Structured prose may be stored when it has a declared role, provenance, retrieval purpose, and bounded schema context.

# 10. Validator Law

Every object class must define validators appropriate to its risk.

A generic `validation failed` outcome is insufficient when a typed error can be produced.

Examples:

- `SCHEMA_ERROR`
- `RELATION_ERROR`
- `STATE_ERROR`
- `EVIDENCE_ERROR`
- `TAXONOMY_ERROR`
- `PRIMITIVE_ERROR`
- `COALITION_ERROR`
- `SEMANTIC_DRIFT`
- `FORMAT_DRIFT`
- `COMPOSITION_ERROR`
- `RUNTIME_ERROR`

# 11. Skill Requirement

Every object-specific canonicalization task MUST eventually have an object-specific Skill/Protocol that contains:

- definition grammar
- required constitutional dimensions
- forbidden ambiguities
- examples
- hard negatives
- validation rules
- escalation conditions

These skills are the future **legalized ontology compiler**.

# 12. Versioning

Object definitions, taxonomy, relations, validators, and storage contracts SHALL be versioned independently where their evolution rates differ.

# 13. Global Boundary Law

If an object cannot be assigned a coherent artifact class and role, it is not ready for implementation. Do not create a schema merely to make an ambiguous concept look structured.
