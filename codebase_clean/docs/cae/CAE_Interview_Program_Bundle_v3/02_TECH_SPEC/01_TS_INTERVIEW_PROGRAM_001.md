---
spec_id: TS-APP-INTERVIEW-PROGRAM-001
title: Interview Program Integration

document_class: TECH_SPEC
product: Conscious Activations
module: interview-program
quality_state: WRITTEN_PENDING_AUDIT
authority_state: PROPOSED
build_authority: false
prepared: 2026-08-30
---

# TS-APP-INTERVIEW-PROGRAM-001 — Interview Program Integration

## 0. What this spec is

This spec defines the brownfield extension that turns the existing Interview Composer boundary into a hypothesis-driven, semantic-acquisition Interview Program while preserving existing service ownership.

It is **not** a replacement for `TS-APP-COMPOSER-001`. It is a dependent/integrating spec. The Composer spec remains authoritative for the existing Guest Research Package, Activative Interview Brief, Composer Session, and their current HTTP/storage contracts unless a later accepted spec explicitly changes them.

## 1. Existing repository authority

The live repository establishes:

- `services/interview-composer` as the Composer boundary;
- existing Guest Research Package, Activative Interview Brief, and Composer Session ownership;
- upstream AIR ownership for Matrix of Edging / Activation Hypothesis related objects;
- `TS-APP-COMPOSER-001` as the current Composer service integration specification.

The repository's `services/interview-composer/AGENTS.md` must be re-read during every implementation pass. Do not rely on this document's copy if the current branch differs.

## 2. Product outcome

The Operator can move from a grounded set of upstream intelligence to a diversified hypothesis portfolio, review candidate question geometry, compile a valid existing Activative Interview Brief, conduct a bounded adaptive interview, and obtain traceable human evidence suitable for downstream production.

## 3. System flow

`World/Audience/Guest intelligence`
`→ coordinate/collision candidate field`
`→ existing AIR activation-hypothesis/portfolio authority where applicable`
`→ Interview Program derived hypothesis adapter`
`→ Operator portfolio selection`
`→ question objective + mechanism coalition`
`→ derived Question IR`
`→ existing Activative Interview Brief`
`→ Composer Session / existing interview runtime boundary`
`→ answer observation + state transition`
`→ authenticated evidence lineage`
`→ downstream content candidate readiness.

## 4. Scope

### In scope

- integration with existing hypothesis/portfolio references;
- derived hypothesis candidate representation;
- diversified portfolio selection;
- Question Intelligence resolution from accepted candidate mechanisms;
- derived Question IR and answer-state routing;
- Brief compilation using the existing Composer boundary;
- bounded adaptive frontier;
- semantic acquisition observation;
- question-to-format/archetype compatibility;
- evidence lineage handoff;
- Operator Studio selection/regeneration/approval controls;
- tests and runtime evidence for the above.

### Out of scope

- replacing AIR's canonical objects;
- creating a second Composer;
- inventing a second Matrix of Edging;
- canonizing Question Primitives in this program bundle;
- changing downstream rendering/CMF semantics beyond the minimum handoff;
- automatic production publication without Operator approval.

## 5. Architecture invariants

1. **One Composer boundary.** No parallel Interview Engine is introduced.
2. **Existing object ownership wins.** Adapters reference existing canonical objects; they do not silently clone them.
3. **Hypothesis before question.** The strategic unit is the hypothesis/collision, not the final natural-language question.
4. **Format/archetype participates upstream.** Intended downstream experience can constrain acquisition requirements, but cannot override evidence reality.
5. **Bounded adaptation.** A deterministic coverage spine coexists with a bounded 3–5 next-move frontier.
6. **Evidence/inference separation.** Guest-stated evidence, system inference, and Guest-validated interpretation remain distinguishable.
7. **Operator authorization.** Selection/approval occurs through an authoritative path and is required for launch.
8. **No quota gaming.** 96, 16–24, and ~32 are planning targets, not correctness constraints.

## 6. Functional requirements

### FR-IP-001 Hypothesis candidate assembly
Create a derived candidate field from available upstream references and coordinate/collision data without claiming a new canonical hypothesis object.

### FR-IP-002 Portfolio selection
Provide a diversity-aware selection process and persist/compile only the Operator-approved working set.

### FR-IP-003 Question resolution
Resolve each selected hypothesis into a question objective, evidence requirement, candidate mechanism coalition, and response shape.

### FR-IP-004 Question IR
Represent the executable properties of a candidate question independently from its final natural-language rendering.

### FR-IP-005 Adaptive frontier
At each eligible runtime state, maintain a bounded set of candidate next moves and choose among them based on the latest answer observation and unresolved requirements.

### FR-IP-006 Semantic acquisition observation
Record the state changes needed to explain why the next move was chosen and whether the hypothesis gained sufficient evidence/resolution.

### FR-IP-007 Brief compilation
Compile selected working material into the existing `activative_interview_brief` representation using the existing Composer owner/path.

### FR-IP-008 Content compatibility
Expose downstream archetype/format/narrative-role compatibility for question planning and candidate review.

### FR-IP-009 Authenticated handoff
Preserve traceable evidence lineage from hypothesis/question attempt through response observation and downstream content candidate.

### FR-IP-010 Operator Studio
Support inspect/select/reject/edit/regenerate/defer/lock/approve behavior using real brownfield persistence and authorization boundaries.

## 7. Proposed derived runtime structures

The derived model is intentionally non-canonical:

`HypothesisCandidate`
`QuestionObjective`
`QuestionPrimitiveRef`
`QuestionCoalition`
`QuestionIR`
`QuestionCandidate`
`QuestionAttempt`
`AnswerObservation`
`QuestionStateTransition`
`ContentCompatibilityView`

These names are conceptual schema labels. Implementation must map them onto current repository types/modules where possible rather than creating all of them as persistent classes/tables.

## 8. Brief compilation contract

The existing Activative Interview Brief remains the outward compilation boundary. Its currently documented fields include the tension hypothesis, Matrix of Edging seed, planned question sequence, expression targets, and relevant upstream references. The implementation must inspect the current branch and use the exact live schema.

The new Interview Program may enrich the provenance/rationale of each planned question only through fields or nested data the existing contract actually supports. If the current schema cannot represent required metadata without changing its canonical contract, stop and surface a change request; do not silently overload or fork the object.

## 9. Runtime adaptive contract

At a high level:

`brief coverage state`
`+ unresolved evidence requirements`
`+ latest AnswerObservation`
`→ eligible next QuestionCandidates (bounded 3–5 when enough valid alternatives exist)`
`→ deterministic selection policy`
`→ QuestionAttempt`
`→ response`
`→ AnswerObservation`
`→ state transition.

A runtime implementation must define deterministic tie-breaking, invalidation conditions, and stop/close behavior in code/tests.

## 10. Evidence contract

Minimum lineage:

`upstream hypothesis refs`
`→ `question candidate id/version`
`→ `question attempt id`
`→ `raw response/source reference`
`→ `observation`
`→ `accepted evidence reference`
`→ `downstream candidate reference`.

The system must not infer “authenticated evidence” from the mere presence of a receipt or successful API response.

## 11. Content compatibility contract

Question planning should expose, where supplied by upstream intent:

- intended archetype(s);
- format(s);
- narrative role(s);
- desired response shape;
- acquisition requirements.

Compatibility is advisory/selection-guiding unless the existing canonical contract states otherwise. It cannot convert weak or absent Guest evidence into evidence.

## 12. API/persistence expectations

Use existing Composer route/dependency/repository patterns. The implementation spec does not authorize arbitrary new persistence. Any new durable state must identify:

- current owner;
- lifecycle;
- versioning;
- idempotency key;
- concurrency semantics;
- deletion/retention behavior;
- migration;
- API authority.

If the requirement can remain a derived view, prefer that over a new table/object.

## 13. Acceptance

A build-authoritative implementation must demonstrate:

1. brownfield authority reconciliation;
2. real hypothesis references or a documented no-source case;
3. diversified selection behavior;
4. real compilation into the existing Brief;
5. bounded adaptive routing driven by a real answer observation;
6. distinction between evidence and inference;
7. operator-controlled regeneration with lock preservation;
8. authoritative launch approval;
9. downstream compatibility visibility;
10. adversarial false-proof tests;
11. PRD/spec maintenance completed in the same session when durable semantics change.

## 14. Open decisions requiring operator/spec ratification

- exact final mapping of the 12 coordinate dimensions to current CAE canonical objects;
- final canonicalization decision for any Question Primitive family;
- exact persistence strategy for Operator feedback/versioning if existing Composer structures cannot represent it;
- exact runtime API for answer observations if the current interview runtime does not expose an extension point;
- exact downstream content-menu consumer.

No implementation agent may silently decide these questions by creating a new parallel architecture.
