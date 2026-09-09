---
type: modular-prd
module: CA-02
title: Conscious Activation Engine — World Intelligence & Contextual State
version: 0.1
status: Draft for Phase 2
owner: Conscious Activation Engine Architecture
phase: 2
depends_on:
  - PRD-CA-01_Engine_Constitution_and_Canonical_Architecture
---

# 1. Purpose

PRD-CA-02 defines the upstream World Intelligence layer of the Conscious Activation Engine. It establishes how the system represents, updates, retrieves, and evaluates the reality surrounding a Guest and an Audience before relational congruence or content activation occurs.

The module is deliberately human-first. It does not manufacture guest truth. It does not equate audience inference with authenticated human evidence. It organizes evidence, schemas, states, cultural context, and derived semantic pressures so later engines can ask precise questions against an explicit world model.

# 2. Architectural Claim

The world model is not a static profile. It is a stateful semantic system.

The canonical structure is:

```text
WORLD
├── AUDIENCE WORLD
│   ├── Audience
│   ├── Audience Schema
│   ├── Context Premise
│   ├── Audience State
│   ├── Audience Maturity
│   └── Audience History
│
├── GUEST WORLD
│   ├── Guest
│   ├── Guest Schema
│   ├── Voice DNA
│   ├── Negative Space
│   ├── Story Archive
│   ├── Guest State
│   └── Guest History
│
└── CULTURAL / RESEARCH WORLD
    ├── Cultural Memory
    ├── Research Signal
    ├── Current Context
    └── Evidence History
```

The module's principal responsibility is to ensure that later reasoning operates against this substrate instead of a prose blob, an unbounded retrieval context, or an unsupported model assumption.

# 3. Human-First Evidence Law

The module distinguishes three epistemic categories:

- **Authenticated human evidence** — directly supplied by the Guest, operator, interview, transcript, or other authorized first-party source.
- **External evidence** — research, cultural material, market signals, public sources, and observations with provenance.
- **Derived inference** — model-generated hypotheses, schema candidates, state estimates, or webhook/tension candidates derived from available evidence.

Derived inference MUST NOT silently overwrite immutable evidence.

A guest-specific statement becomes authenticated source truth only when supported by an authorized human source.

# 4. Context Premise Doctrine

Context Premise is a canonical evidence-bearing subsystem inside Audience World. It is not the Audience ontology and is not merely a static phrase table.

Its historical twelve-category language is retained as a structured evidence surface:

- Wants
- Frustrations
- Dreams
- Fears
- Suspicions
- Insecurities
- Envy Feelings
- Enemies
- Coping Mechanisms
- Hidden Beliefs
- Emotional Triggers
- Success Markers

These observations can feed downstream schema inference, state estimation, tension/webhook detection, maturity modeling, semantic affinity, and later relational reasoning.

# 5. Audience State Model

Audience identity and Audience State are distinct.

Audience is persistent continuity.
Audience State is temporal configuration.

The state model should support, at minimum:

### Semantic State
- active tensions
- semantic load
- schema activations
- current pressure domains

### Affective State
- arousal
- valence
- affective register

### Media Motive
- escape
- discovery
- processing
- status
- future additions only through versioned taxonomy change

### Capacity / Maturity
- new
- developing
- loyal
- evidence-backed advancement rather than calendar time alone

States MUST preserve observation time, provenance, confidence, and transition history.

# 6. Guest State Model

Guest is the persistent person modeled by the engine. Guest State captures temporal conditions relevant to the engine's work, including:

- current concerns
- current convictions
- current unresolved tensions
- current energy / affective register where available
- contextual availability
- current narrative focus
- transformation position

Guest State MUST NOT rewrite the underlying Guest identity or Voice DNA.

# 7. Tension / Webhook Model

A Webhook is a derived, activatable semantic pressure object. It is not a social-media hook and not merely a topic.

A valid Webhook/Tension candidate must be traceable to sufficient evidence and represent an unresolved, meaningful pressure that could become activation-worthy under appropriate conditions.

Lifecycle examples:

```text
latent → corroborating → active → saturated → resolved
                         ↘ blocked
                         ↘ superseded
```

The system must support confirmation by multiple independent signals. The default implementation should permit configurable evidence thresholds, including a project policy for multi-signal confirmation, rather than treating a single source as automatically sufficient.

# 8. World Intelligence Resolution

The World Intelligence layer should support progressive resolution:

```text
raw evidence
→ normalized observation
→ schema candidate
→ corroborated state
→ active tension/webhook
→ contextual intelligence object
```

The system should retain weaker candidates as hypotheses rather than forcing premature canonicalization.

# 9. Provenance and Evidence Weighting

Every observation, Context Premise entry, Research Signal, state inference, and webhook candidate MUST carry provenance metadata sufficient to reconstruct:

- source
- source type
- observed_at
- ingested_at
- evidence lineage
- confidence
- corroboration count
- contradiction count where measured
- epistemic status

The architecture should support weighted evidence without reducing truth to a single opaque score.

# 10. Brownfield Principle

Before implementing replacements, the current `consciousactivation-main` repository must be inspected for:

- existing Audience schemas
- Guest/Coach/Client representations
- Context Premise artifacts
- Voice DNA and Negative Space registries
- research schemas and ingestion tools
- mood/routing state structures
- audience maturity logic
- existing webhooks/tension-like entities
- historical archives
- PostgreSQL/JSONB/vector/event implementations

Each implementation must be classified under the Phase 1 status vocabulary.

# 11. Agent Reasoning Boundary

Agents operating in this module must not retrieve the entire world model indiscriminately.

The preferred interaction pattern is:

```text
Human / Agent Intent
→ Schema identification
→ Relevant entities
→ Relevant relations
→ State/time filters
→ Evidence retrieval
→ Query / composition plan
→ Structured result
→ Validation
→ Typed output
```

Authorized semantic functions should include operations such as:

- `get_audience_context_premise(audience_id, scope)`
- `get_current_audience_state(audience_id)`
- `get_guest_state(guest_id)`
- `get_active_audience_tensions(audience_id)`
- `get_research_signals(context_scope)`
- `get_corroborating_evidence(observation_id)`
- `estimate_contextual_state(entity_id, interval)`
- `find_webhook_candidates(audience_id, context_scope)`

Functions MUST expose controlled results rather than unrestricted database access.

# 12. Storage Strategy

The logical model may be realized through:

- PostgreSQL tables for stable entities and typed state
- relational tables for important relationships
- JSONB for evolving hypotheses and less-stable attributes
- vector indexes for fuzzy semantic retrieval
- immutable event tables for observations and state transitions
- views/functions for authorized agent access

JSONB MUST remain structured and addressable. It may contain carefully scoped prose evidence, examples, or hypotheses where that material improves retrieval and later reasoning, but it MUST NOT become an unbounded substitute for the canonical schema.

# 13. Dynamic Evolution

World Intelligence is intentionally adaptive.

The engine may evolve through:

```text
JSONB hypothesis
→ corroboration
→ validated schema candidate
→ canonical concept or relation
```

Derived tension/webhook objects may be recalculated when upstream evidence, schema, or state assumptions change.

Immutable evidence must remain immutable.

# 14. Quality and Anti-Centroid Requirements

World Intelligence must not flatten lived language into institutional abstractions when the original language carries useful signal.

The Anti-Centroid Patrol should detect:

- generic paraphrase replacing tribal language
- unsupported audience generalization
- single-source overconfidence
- tension dilution
- mood/tension collapse
- over-sanitized wording
- premature normalization of dissenting or unusual evidence

The patrol exists to preserve signal, not to impose corporate tone.

# 15. Phase 2 Functional Requirement Registry

1. FR-CA-02-001 Audience Entity and Continuity Model
2. FR-CA-02-002 Guest Entity and Continuity Model
3. FR-CA-02-003 Context Premise Evidence Model
4. FR-CA-02-004 Audience Schema and Semantic Representation
5. FR-CA-02-005 Guest Schema and Semantic Representation
6. FR-CA-02-006 Audience Dynamic State Model
7. FR-CA-02-007 Guest Dynamic State Model
8. FR-CA-02-008 Contextual State Model
9. FR-CA-02-009 Research Signal and Cultural Context Ingestion
10. FR-CA-02-010 Evidence Corroboration and Signal-vs-Noise Resolution
11. FR-CA-02-011 Tension/Webhook Candidate Derivation
12. FR-CA-02-012 Audience Affective / Media Motive / Maturity Model
13. FR-CA-02-013 World Intelligence Authorized Query Functions
14. FR-CA-02-014 World Intelligence Memory and State Evolution
15. FR-CA-02-015 World Intelligence Brownfield Migration and Observability

# 16. Acceptance Criteria

Phase 2 is ready for technical specification convergence when:

- Audience and Guest have persistent canonical identity models;
- Context Premise is represented as evidence-bearing data rather than a single opaque document;
- state is temporal and append-history-preserving;
- semantic tension, affective state, media motive, and maturity remain separate dimensions;
- Research Signal provenance is immutable and queryable;
- webhook/tension candidates include evidence and lifecycle state;
- evidence corroboration rules distinguish hypothesis from sufficiently supported activation;
- authorized semantic query functions are defined;
- repository status for Phase 2 objects is audited;
- all major objects have Object Constitutions or explicit pending status.

# 17. Downstream Handoff

Phase 2 provides the input substrate for Phase 3 Relational Intelligence:

```text
Audience World
+
Guest World
+
Cultural / Research World
+
Contextual State
↓
Relational Intelligence
↓
Guest ↔ Audience Congruence
↓
Trigger Matching
↓
Matrix of Edging
```

The World Intelligence module should therefore remain descriptive, stateful, evidence-grounded, and queryable. It should not absorb the decision doctrine of relational matching or edge selection prematurely.
