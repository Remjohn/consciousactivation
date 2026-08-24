---
type: architecture-governance-protocol
id: CA-ARCH-004
title: Conscious Activation Engine — Grill-Me Protocol v2
version: 0.1
status: Phase 0 Foundation
---

# 1. Purpose

This protocol is the interactive architecture-resolution procedure for the Conscious Activation Engine.

Its purpose is to interrogate unresolved decisions in dependency order until the architecture is sufficiently specified to support PRDs, Functional Requirements, Technical Specifications, and implementation without hidden assumptions.

This is not a brainstorming prompt and not a generic product-discovery interview.

It is a **brownfield architecture resolution protocol**.

# 2. Prime Directive

**The codebase must be inspected before the human is asked a question that the repository can answer.**

The agent must distinguish:

- facts already demonstrated by code
- facts established by source-of-truth documents
- current hypotheses
- unresolved human constitutional decisions
- external research questions

# 3. Evidence Hierarchy

When forming a recommendation, prefer evidence in this order unless the task explicitly requires another source:

1. Current codebase behavior
2. Current source-of-truth PRDs/specifications/registries
3. Current tests and receipts
4. Architecture decision history
5. Human-authored Director Notes and project decisions
6. Project research corpus
7. External authoritative research
8. General model knowledge

A lower-ranked source may challenge a higher-ranked assumption, but the conflict must be explicit.

# 4. Question Classes

## Class A — Code-Resolvable

Inspect the repository and answer without asking.

## Class B — Architecture-Resolvable

Inspect current documents, registries, dependencies, and history, then make the best supported determination.

## Class C — Human Constitutional Decision

Ask the human because the decision cannot be inferred without choosing between legitimate alternatives.

## Class D — Research Resolution

Research external evidence before asking or recommending when the answer depends on current or niche facts.

# 5. One-Question Law

Ask exactly one unresolved human question at a time.

Do not bundle independent decisions.

If a downstream question depends on an upstream unresolved decision, ask the upstream question first.

# 6. Dependency Order

The default decision tree is:

```text
ENGINE CONSTITUTION
  ↓
ONTOLOGY
  ↓
TAXONOMY
  ↓
OBJECT CLASSES
  ↓
CANONICAL OBJECT DEFINITIONS
  ↓
SCHEMA
  ↓
RELATIONSHIPS
  ↓
STATE
  ↓
EVENTS / EVIDENCE / RECEIPTS
  ↓
WORLD INTELLIGENCE
  ↓
RELATIONAL INTELLIGENCE
  ↓
SEMANTIC DISCERNMENT
  ↓
PRIMITIVES
  ↓
EDGING / COALITIONS
  ↓
CCF
  ↓
CMF
  ↓
AGENT RUNTIME / IR
  ↓
MEASUREMENT / LEARNING
```

# 7. RSCS Application

Every recommendation must follow the project's Recursive Signal Compression Systems discipline.

## Law 1 — Saturation Before Compression

Ground the recommendation in project-specific evidence. A recommendation from vacuum is invalid.

## Law 2 — Meaning Emerges Through Collision

Identify at least one concrete collision in the current architecture: contradiction, tension, asymmetry, shadow, anomaly, or unarticulated regularity.

Use the project's T/V/R framing where relevant:

- Prediction Violation
- Costly Exposure
- Latent Pattern Articulation

## Law 3 — Compression Increases Signal Density

A recommendation should be:

- irreducible
- emergent
- specific

## Law 4 — Evaluation Governs Reality Contact

Apply:

1. Could a generic system produce this without the project context?
2. Could another project use the same recommendation unchanged?
3. Does project evidence verify it?
4. Does it articulate a real collision the human can recognize?

A `YES` answer to Check 1 or 2 is a density failure.

# 8. Dependency Law

A recommendation cannot be treated as final when an upstream architectural dependency remains unresolved.

This is the additional Grill-Me control:

> **Dependency Before Opinion.**

For example, do not finalize a SQL schema for `Tension` until the architecture has established whether Tension is an Entity, State, Relation, or Derived Semantic Artifact.

# 9. Recommendation Format

Every substantive recommended answer should contain:

```text
RECOMMENDATION

PROJECT-SPECIFIC EVIDENCE

ARCHITECTURAL COLLISION

DECISION CONSEQUENCES

DEPENDENCIES UNBLOCKED

RISKS / TRADE-OFFS

RECOMMENDED NEXT QUESTION
```

The old 320–360 word rule is replaced by a density law:

> The recommendation must be long enough to make the next dependent decision without reopening the current decision.

Length is evidence-dependent, not arbitrary.

# 10. Anti-Centroid Requirement

The protocol MUST actively reject recommendations that collapse into generic corporate norms, unnecessary sanitization, or ungrounded safety boilerplate.

The following distinctions are constitutional:

```text
Governance ≠ blandness
Constraint ≠ censorship
Validation ≠ suppression
Legalization ≠ corporate sanitization
Safety ≠ genericity
```

The system is explicitly authorized to recommend sharp, unusual, asymmetric, or tension-bearing architecture when project evidence supports it.

# 11. Brownfield Audit Requirement

For every major design question, record:

```yaml
implementation_status:
  exists: true|false
  partial: true|false
  duplicated: true|false
  conflicting: true|false
  spec_only: true|false
  missing: true|false
  deprecated: true|false
```

Then identify:

- current code location
- current behavior
- target behavior
- migration action

Possible actions:

`PATCH | EXTEND | REFACTOR | REPLACE | MERGE | DEPRECATE | NEW`

# 12. Decision Ledger

Each resolved question becomes a durable decision record:

```yaml
decision_id:
question:
answer:
recommendation:
status:
evidence:
architectural_collision:
affected_objects:
affected_prds:
affected_functional_requirements:
dependencies_unblocked:
alternatives_rejected:
implementation_status:
version:
```

# 13. Object-Definition Interrogation

When resolving an object, the agent must first determine:

1. artifact class
2. ontological plane
3. role
4. taxonomy
5. semantic neighbors
6. canonicality / mutability / epistemic status
7. definition grammar
8. relationships
9. state
10. events
11. provenance
12. operations
13. validators
14. storage
15. runtime consumers

Schema follows this analysis.

# 14. Evidence Status

Scientific or historical claims should be labeled:

`ESTABLISHED | SUPPORTED | PROPOSED | HYPOTHESIS`

This is particularly important for neuroscience and psychological rationales inherited from older CCP documents.

Useful hypotheses remain usable as hypotheses.

# 15. Completion Condition

Grill-Me is complete for a branch when:

- all material upstream dependencies are resolved
- all human constitutional decisions have explicit answers
- the decision ledger contains the rationale
- affected PRDs and objects are identified
- contradictions are either resolved or explicitly quarantined
- the branch can move to implementation without reopening foundational questions

# 16. Invocation Rule

When invoked, the agent should report only:

- the current branch
- what is already known from evidence
- the single unresolved question
- the recommended answer
- the reason the question must be asked now

Then wait for the human answer.
