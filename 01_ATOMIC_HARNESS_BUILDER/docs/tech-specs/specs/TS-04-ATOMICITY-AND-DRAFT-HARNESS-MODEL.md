# TS-04: Atomicity And Draft Harness Model

Status: `EMPIRICAL_SPEC_COMPLETE_PENDING_BD-004_BD-007`

## Traceability

- Owned: FR-032 through FR-040.
- Decisions: D002, D003, D008, D009, D010, D011, D027, D033.
- Supporting NFRs: NFR-CAT-001, NFR-CAT-002, NFR-EVAL-003, NFR-TRACE-001, NFR-TRACE-004.

## Responsibility And Authority

Own candidate-boundary comparison, typed atomicity status, split/merge alternatives, wrong-boundary risk, ratification packet, Draft Harness Model, and boundary freeze. Agents investigate and recommend. Deterministic code validates evidence/graph completeness and compiles packets. A human category steward ratifies the boundary; no model may self-ratify.

## Modules And Components

`domain/atomicity.py`, `atomicity/candidates.py`, `atomicity/risk.py`, `atomicity/draft_model.py`, `application/atomicity_commands.py`, and `evaluation/atomicity.py`.

## Canonical Data Structures

`AtomicityCandidate { candidate_id, included_specimens, excluded_specimens, invariant_claims, variation_axes, category_ref, evidence_refs }`

`AtomicityAssessment { candidates, recommended_id, status, merge_split_options, wrong_boundary_risks, confidence, gaps, evaluator_receipts }`

Allowed status: `ATOMIC`, `VARIANT`, `DISH_FAMILY`, `FORMAT_FAMILY`, `NEEDS_CLUSTERING`, `NEEDS_PARTITION`, `INSUFFICIENT_EVIDENCE`.

`DraftHarnessModel { model_id, boundary_ref, category_ref, product_promise_draft, inputs, outputs, invariants, legal_variation, capability_hypotheses, phase_hypotheses, unresolved_gaps, status=UNRATIFIED }`

`AtomicityRatification { assessment_hash, selected_candidate, human_id, rationale, accepted_risks, signed_at }`

## APIs, Commands, Events, Persistence

- Commands: `CompareBoundaries`, `AssessAtomicity`, `CompileDraftHarnessModel`, `RatifyAtomicity`, `RejectAtomicity`, `ReopenBoundary`.
- Events: `BoundaryCandidatesCompared`, `AtomicityAssessed`, `DraftHarnessModelCompiled`, `AtomicityRatified`, `AtomicityRejected`, `BoundaryReopened`.
- Persistence: assessment and model revisions in Harness IR; signed ratification receipt in ledger/CAS.
- Idempotency: same source lock, visual grammar, ontology, policy, and candidate set yield the same packet identity, excluding agent recommendation content which carries exact model/capsule identity.

## Dependency, Invalidation, And Resume

Requires saturated evidence and visual grammar. Ratification freezes the selected boundary for Genesis. New contradictory evidence reopens atomicity, invalidates Genesis descendants and compiled artifacts, but preserves unrelated source and parse work. Resume returns the pending packet; it never interprets silence as approval.

## Security, Isolation, Observability, Cost, And Performance

Only declared evidence and category references enter the assessment sandbox. Record candidate count, evidence coverage, evaluator agreement, model cost, human decision latency, reopened-boundary rate, and downstream wrong-boundary incidents. Candidate comparison budgets are explicit and bounded.

## Failures And Recovery

Missing evidence yields `INSUFFICIENT_EVIDENCE`. Conflicting evaluators retain alternatives for human review. An invalid category/boundary pairing blocks ratification. Rejection returns typed missing work to evidence, visual parsing, or candidate generation.

## Acceptance Tests

1. Every status is schema-valid and evidence-linked.
2. Merge/split recommendations identify affected specimens and consequences.
3. Draft Harness Model is always explicitly `UNRATIFIED` before human action.
4. An agent cannot create a ratification receipt.
5. Atomicity cannot pass without Visual Syntax artifacts.
6. Reopening invalidates Genesis descendants and preserves source-lock history.
7. Wrong-boundary adversarial cases fail or produce human-visible alternatives.
8. Format 02 is distinguishable from a generic short-form editing family.

## Implementation Tasks

1. Define schemas, status enum, and boundary graph.
2. Implement deterministic packet compiler and dependency checks.
3. Implement bounded recommendation/evaluator nodes.
4. Implement human ratification commands and receipts.
5. Build Format 02 positive, merge, split, and near-miss prototype cases.
6. Add invalidation and authority tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Classify Conversational Activation / Human Expression as a distinct atomic category | atomicity_owner | Atomicity classifies; category constitution owns grammar; profile does not flatten visual categories | category ID, profile ID, call/reaction/turn evidence summary | Block unsupported category or mixed-surface flattening | merge/split/variant fixtures including ReelCast and Interview Expression | Candidate maps to one of five categories and one declared profile, or blocks with evidence | D031 is preserved historically and expanded through V1.2 current-effect metadata |

## Non-Goals And Migration

No universal clustering engine, category invention, final harness implementation, or V2.1 status migration is included.
