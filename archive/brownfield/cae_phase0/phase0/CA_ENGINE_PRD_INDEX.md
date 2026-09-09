---
type: prd-index
document_id: CA-PRD-INDEX-001
title: Conscious Activation Engine — Modular PRD Index
version: 0.1
status: Phase 0 Foundation
---

# 1. Purpose

This index is the master router for the nine-module Conscious Activation Engine development specification.

The new PRDs are intentionally organized around the **causal architecture of intelligence**, not around the historical product surface structure of the earlier CCP PRD set.

The previous nine CCP modules remain historical/product lineage and should not be treated as automatically obsolete.

# 2. Canonical PRD Registry

| Module | ID | Purpose | Primary Plane |
|---|---|---|---|
| 01 | `PRD-CA-01` | Engine Constitution & Canonical Architecture | Governance |
| 02 | `PRD-CA-02` | World Intelligence & Dynamic Context | World / State |
| 03 | `PRD-CA-03` | Guest Intelligence, Relational Intelligence & Interview Compiler | Relational |
| 04 | `PRD-CA-04` | Semantic Discernment & SFL Intelligence | Semantic / Perceptual |
| 05 | `PRD-CA-05` | Primitive Registry, Coalition Engine & Matrix of Edging | Transformation |
| 06 | `PRD-CA-06` | CCF Semantic Composition & Content Compiler | Semantic Realization |
| 07 | `PRD-CA-07` | CMF Composition, Visual Grammar & Executable Media IR | Media Realization |
| 08 | `PRD-CA-08` | Agent Runtime, Legalized Harnesses, Programs & IR Execution | Runtime |
| 09 | `PRD-CA-09` | Measurement, Receipts, Fatality, Outcomes & Evolution | Learning |

# 3. Module Definitions

## PRD-CA-01 — Engine Constitution & Canonical Architecture

Owns: ontology, taxonomy, artifact classes, architecture laws, authority hierarchy, brownfield doctrine, canonical data philosophy, legal/constitutional framework.

Functional requirement prefix: `FR-CA-01-*`

## PRD-CA-02 — World Intelligence & Dynamic Context

Owns: Audience World, Context Premise, audience schema, DHD, cultural memory, research intelligence, context state, affective state, media motive, maturity, active tension/webhooks, performance context.

Functional requirement prefix: `FR-WI-*`

## PRD-CA-03 — Guest Intelligence / Relational Intelligence / Interview Compiler

Owns: Guest World, Voice DNA, Negative Space, story archive, belief/state model, Guest–Audience congruence, Trigger Matching, activation events, interview compilation, authentication of human evidence.

Functional requirement prefix: `FR-RI-*`

## PRD-CA-04 — Semantic Discernment & SFL

Owns: SDA ontology, structural grammar, semantic dynamics, hard negatives, directional integrity, SFL taxonomy, SFL registry, perceptual evaluation.

Functional requirement prefix: `FR-SD-*`

## PRD-CA-05 — Primitives / Coalitions / Edging

Owns: Meaning and Experience primitive registries, basis, geometry, crosswalks, candidate survival, coalition formation, Edge Products, Matrix of Edging, coalition receipts, fatality, anti-centroid patrol.

Functional requirement prefix: `FR-PR-*`

## PRD-CA-06 — CCF Semantic Composition

Owns: archetype containers, semantic programs, content IR, narrative composition, export governance, source lineage, semantic validation.

Functional requirement prefix: `FR-CCF-*`

## PRD-CA-07 — CMF Composition & Media IR

Owns: formats, scenes, scene instances, compositions, composition instances, media roles, visual primitives, sonic grammar, visual syntax, executable video IR, Director Note translation.

Functional requirement prefix: `FR-CMF-*`

## PRD-CA-08 — Agent Runtime / Legalized Harnesses

Owns: agent roles, skills, object-definition skills, SQL/JSONB governance, authorized functions/views, query planning, programs, directives, contracts, IR execution, error taxonomy, repair, quarantine, receipts.

Functional requirement prefix: `FR-RT-*`

## PRD-CA-09 — Measurement / Memory / Evolution

Owns: events, receipts, evaluations, fatality, outcomes, benchmark memory, Context Performance Registry, state evolution, schema evolution, skill/program evolution, learning governance.

Functional requirement prefix: `FR-ML-*`

# 4. Dependency Graph

```text
PRD-CA-01
    ↓
┌──────────────┬──────────────┐
↓              ↓              ↓
PRD-CA-02    PRD-CA-03     PRD-CA-04
   │             │             │
   └──────┬──────┴──────┬──────┘
          ↓             ↓
       PRD-CA-05 ← semantic context
          ↓
       PRD-CA-06
          ↓
       PRD-CA-07
          ↓
       PRD-CA-08
          ↓
       PRD-CA-09
          └──────────────→ architecture evolution
```

PRD-CA-09 feeds benchmark and state updates back into PRD-CA-02 through PRD-CA-08, but must not rewrite immutable evidence.

# 5. Functional Requirement Conventions

Every FR should define at minimum:

- requirement identity
- purpose
- problem
- actors / consumers
- inputs
- outputs
- entities
- relations
- states
- events
- provenance
- contracts
- validators
- error taxonomy
- acceptance criteria
- implementation status
- source lineage

The FR should explain **what must be true**. It should avoid premature implementation detail unless the implementation choice is itself an architectural constraint.

# 6. Technical Specification Convergence

Functional Requirements later converge into Technical Specifications through:

```text
FR
 ↓
acceptance criteria
 ↓
data dependencies
 ↓
state/event model
 ↓
API / function boundary
 ↓
implementation design
 ↓
SQL / JSONB / vector / graph strategy
 ↓
test strategy
 ↓
deployment / migration
```

# 7. Brownfield Coverage Registry

Every FR MUST eventually include:

```yaml
implementation_status:
  exists: false
  partial: false
  duplicated: false
  conflicting: false
  spec_only: false
  missing: false
  deprecated: false

current_code_locations: []
current_behavior: ""
target_behavior: ""
migration_action: "PATCH | EXTEND | REFACTOR | REPLACE | MERGE | DEPRECATE | NEW"
```

The codebase is the source for determining current implementation state.

# 8. Historical Module Lineage

The previous CCP modular PRD system remains valuable historical/product lineage:

- PRD-01 Platform Strategy
- PRD-02 CCF Content Factory
- PRD-03 CMF Media Factory
- PRD-04 CVE Experience Design
- PRD-05 CBCS Law28
- PRD-06 Conscious Reactions
- PRD-07 V2WS Webinar
- PRD-08 Conscious Primitives
- PRD-09 CPSC Silent Referral

These documents should be mapped into the new PRDs using:

`RETAIN | REFRAME | REPLACE | DEPRECATE | TRACE-ONLY`

No historical mechanism should be removed merely because the module number changed.

# 9. Cross-System Object Router

Primary objects currently identified for canonical modeling include:

```text
Audience
AudienceSchema
ContextPremise
AudienceState
Guest
GuestSchema
GuestState
VoiceDNA
NegativeSpace
ResearchSignal
CulturalMemory
ContextualState
Tension/Webhook
ExistentialInvariant
ArchetypalGeometry
RepresentationGeometry
Primitive
PrimitiveActivation
PrimitiveCandidate
Coalition
EdgeProduct
SFLFunction
SFLFunctionStack
Archetype
Format
Scene
SceneInstance
Composition
CompositionInstance
MediaRole
VisualPrimitive
SemanticProgram
CompositionIR
VideoEditProgram
Receipt
Fatality
Outcome
```

This list is a working canonical candidate set, not permission to implement every object immediately. Each object must pass the Object Constitution protocol.

# 10. Development Sequence

### Phase 0

Create and ratify:

- `CA_ENGINE_ARCHITECTURE.md`
- `CA_ENGINE_OBJECT_CONSTITUTION.md`
- `CA_ENGINE_ARCHITECTURE_LAWS.md`
- `CA_ENGINE_GRILL_ME.md`
- `CA_ENGINE_PRD_INDEX.md`

### Phase 1

Write PRD-CA-01.

### Phase 2

Write PRD-CA-02 and PRD-CA-03.

### Phase 3

Write PRD-CA-04 and PRD-CA-05.

### Phase 4

Write PRD-CA-06 and PRD-CA-07.

### Phase 5

Write PRD-CA-08.

### Phase 6

Write PRD-CA-09.

### Phase 7

Converge FRs into technical specifications and implementation plans.

# 11. Phase Gate

No PRD may introduce a new global object category, ontological plane, artifact class, or architecture law without updating the Phase 0 foundation artifacts and recording the change in the decision ledger.
