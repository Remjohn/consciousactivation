---
type: modular-prd
module: PRD-CA-03
title: Conscious Activation Engine — Relational Intelligence, Congruence & Context Reasoning
author: CAE Architecture Team
date: 2026-08-22
status: Proposed Source of Truth
version: 0.1
phase: 3
dependencies:
  - PRD-CA-01_Engine_Constitution_and_Canonical_Architecture
  - PRD-CA-02_World_Intelligence_and_Contextual_State
  - Conscious_Activation_Definition_Grammar_Bundle_v2
  - CA_WORLD_INTELLIGENCE_AUTHORIZED_FUNCTIONS
  - CA_WORLD_INTELLIGENCE_ERROR_TAXONOMY
---

# 1. Purpose

Phase 3 defines the **Relational Intelligence Layer** of the Conscious Activation Engine (CAE).

The World Intelligence layer established the principal domains:

- Audience World
- Guest World
- Cultural / Research World
- contextual and dynamic state
- evidence and historical memory

Relational Intelligence exists because none of those domains becomes intelligent merely by being well modeled. The system becomes operationally intelligent when it can reason over the *relationships between* those domains without collapsing them into one profile.

The core question is:

> **Where does the Guest's lived semantic map intersect the Audience's currently relevant semantic map, and what is the evidential strength and temporal validity of that intersection?**

This is the layer in which the old Trigger Matching architecture, Context Reasoning, resonance, affinity, schema crossings, and the handoff toward Matrix of Edging become one governed system.

# 2. Architectural Role

CAE shall treat Relational Intelligence as a dedicated plane between World Intelligence and activation selection.

```text
WORLD INTELLIGENCE
      ↓
RELATIONAL INTELLIGENCE
      ↓
CONTEXT REASONING
      ↓
PRESSURE FIELD
      ↓
MATRIX OF EDGING
      ↓
BROAD PRIMARY SIGNAL
```

Relational Intelligence is neither content generation nor final semantic execution.

It is the **hypothesis and congruence layer** that determines what relationships are sufficiently supported to influence downstream selection.

# 3. Core Principles

## 3.1 Objects remain distinct

Audience, Guest, Context Premise, State, Tension, Invariant, and Research Signal remain distinct objects. Relations describe connections between them.

## 3.2 Congruence is multidimensional

A single resonance score is insufficient. The system must retain the component dimensions used to derive it.

## 3.3 Relation is not identity

A GuestExperiencedTension relation does not mutate the Guest into a Tension or the Tension into a Guest attribute.

## 3.4 Historical truth is not current truth

A historically valid relation must not be silently projected into present state.

## 3.5 Inference must remain identifiable

Observed evidence, derived relation, and planner hypothesis must remain distinguishable.

## 3.6 No permission-by-schema

The relational layer MUST NOT introduce artificial authorization or censorship semantics that are absent from the underlying domain model. A relation may describe experience, relevance, congruence, or evidence strength. Whether an output may be publicly used is a separate policy question and cannot be smuggled into relational definitions.

## 3.7 Anti-centroid preservation

The engine must preserve meaningful disagreement and asymmetry. A conflict between Guest and Audience models can itself be a high-value finding. The system must not erase it merely because a harmonious relation is easier to generate.

# 4. Relational Object Taxonomy

| Class | Purpose |
|---|---|
| Relation | Assert a typed connection between objects |
| Assessment | Evaluate a relationship along explicit dimensions |
| State | Represent the current condition of a relationship |
| Observation | Record an immutable occurrence about a relationship |
| Candidate | Represent a derived but not-yet-accepted relational possibility |
| Plan | Describe a procedural reasoning path used to derive or evaluate relations |
| Receipt | Preserve execution lineage and decisions |

# 5. Core Relation Families

### 5.1 Identity / Experience relations

- GuestExperiencedTension
- GuestNavigatedTension
- GuestTransformedThroughTension
- AudienceExhibitsTension
- AudienceResolvedTension

### 5.2 Schema relations

- GuestSchemaExpressesPattern
- AudienceSchemaContainsPattern
- SchemaCrossingObserved
- SchemaCrossingHypothesized

### 5.3 Congruence relations

- GuestAudienceCongruence
- GuestAudienceAdjacency
- GuestAudienceDivergence
- ResonanceCandidate

### 5.4 Context relations

- SignalRelevantToGuest
- SignalRelevantToAudience
- SignalIntersectsTension
- ContextSupportsRelation

### 5.5 Selection relations

- PressureFieldCandidateDerivedFromRelation
- EdgeCandidateSupportedByRelation

The engine must distinguish **relation existence** from **relation strength** and from **downstream eligibility**.

# 6. Congruence Model

The historical Trigger Matching model supplied four useful dimensions:

1. Moral Foundation / Value Conflict
2. Coping Pattern
3. Agency Attribution
4. Temporal Position

Phase 3 retains these as a configurable **Congruence Dimension Set**, not as permanently universal truth.

The architecture must permit additional dimensions when first-party evidence demonstrates their necessity, including:

- identity structure
- status structure
- belonging structure
- mechanism similarity
- transformation distance
- language congruence
- contextual proximity

A CongruenceAssessment records each dimension separately, then derives any aggregate score from the typed components.

# 7. Context Reasoning

Context Reasoning is a planner, not a prose summary.

Its canonical procedure is:

```text
Human / Agent Intent
→ Schema Identification
→ Relevant Entity Retrieval
→ Relevant Relation Retrieval
→ Subproblem Decomposition
→ Retrieval / Composition Plan
→ Candidate Reasoning
→ Typed Result
→ Validation
→ Error Classification
→ Repair / Escalation
```

This structure is intentionally parallel to the SQL-of-Thought pattern and the CAE legalized-harness doctrine.

# 8. Pressure Field

The Pressure Field is the relationally grounded set of currently meaningful tensions that may be worth exposing to the Matrix of Edging.

It is not equivalent to the Audience Tension Registry.

It is a derived field produced by combining:

- current Audience state
- Guest state/history
- Context Premise evidence
- relevant invariants
- Cultural / Research signals
- relation assessments
- maturity/capacity
- contradictions and asymmetries

The Pressure Field must retain provenance to the underlying relationships.

# 9. Matrix of Edging Handoff

Matrix of Edging consumes the Pressure Field to select or sharpen the broad primary signal.

The handoff must specify:

- candidate pressure
- evidence density
- relation support
- current state relevance
- freshness
- collision type
- expected audience recognition
- known contradiction
- downstream routeability

Matrix of Edging must not invent relational facts that were absent from the upstream model.

# 10. Anti-Centroid Patrol

Relational Intelligence shall include an explicit patrol against semantic flattening.

The patrol searches for:

- generic compatibility language
- unexplained averaging of conflicting evidence
- unjustified softening of strong tensions
- relation scores that conceal contradictory dimensions
- removal of high-charge evidence without a declared reason
- conversion of a live asymmetry into generic consensus

A violation creates a typed error rather than silently rewriting the relation.

# 11. Human-First Boundary

Relational Intelligence creates hypotheses. The Interview creates authenticated evidence.

```text
WORLD MODEL
→ RELATIONAL HYPOTHESIS
→ PROVOCATION
→ HUMAN RESPONSE
→ AUTHENTICATED EVIDENCE
```

A strong relation can justify a question. It does not constitute the Guest's answer.

# 12. Data Model Requirements

Relational data must support:

- explicit source and target IDs
- relation type
- directionality
- temporal scope
- evidence links
- confidence
- derivation method
- state
- version
- contradiction flags
- decision lineage

PostgreSQL should host authoritative relational records. JSONB may carry evolving relation metadata and structured examples. Vectors may support candidate retrieval. Immutable observations and receipts preserve temporal reality.

# 13. Authorized Query Functions

The relational layer should expose controlled semantic functions such as:

- `find_guest_audience_resonances(guest_id, audience_id, context_id)`
- `find_schema_crossings(guest_id, audience_id, constraints)`
- `assess_congruence(relation_candidate_id, profile)`
- `find_supported_pressure_candidates(audience_id, guest_id, context_id)`
- `get_relation_evidence(relation_id)`
- `get_relation_history(relation_id)`
- `get_unresolved_relational_conflicts(guest_id, audience_id)`

Agents should consume authorized views/functions rather than arbitrary database state.

# 14. Functional Quality Bar

A relational result is acceptable only when an operator can inspect:

- what relates
- why it relates
- which dimensions matched
- which dimensions did not
- which evidence supports each dimension
- whether the relation is observed or inferred
- what state it is in
- what downstream decisions it is allowed to influence

# 15. Brownfield Requirement

The current codebase must be treated as the implementation reality. The build MUST distinguish:

- already implemented
- partially implemented
- specified but absent
- duplicated
- conflicting
- unreachable
- implemented without state
- implemented without provenance
- implemented without validation

No new relational subsystem should be assumed to be greenfield until the repository audit proves the corresponding capability does not already exist.

# 16. Phase Exit Criteria

Phase 3 exits only when:

1. relation classes are canonicalized;
2. relation states and temporal semantics are defined;
3. CongruenceAssessment is decomposed and traceable;
4. ContextReasoningPlan is typed;
5. PressureFieldCandidate is lineage-preserving;
6. Matrix of Edging has a formal input contract;
7. anti-centroid patrol can identify flattening;
8. relational query functions are authorized and testable;
9. the brownfield gap map is complete enough to schedule implementation;
10. FRs can be translated into technical specifications without semantic ambiguity.
