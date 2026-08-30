# M06 — Adaptive Question Frontier

**Status:** PROPOSED
**Depends on:** M04, M07 runtime observation contract
**Primary requirement:** FR-IP-005

## Objective

Implement bounded adaptive planning: a deterministic coverage spine plus a bounded set of eligible next-question candidates selected from observed state.

## Runtime rule

The system must never choose the next question from unconstrained model improvisation alone.

Required conceptual state:

`coverage spine + unresolved requirements + latest answer observation + locks`
`→ eligible candidates (preferred 3, max 5)`
`→ deterministic selection`
`→ next QuestionAttempt`.

## Allowed next actions

`deepen | broaden | reconcile | verify | reframe | advance | close`

## Deterministic tie breaking

At minimum, define and test a stable ordering using requirement coverage, hypothesis/evidence fit, interactional fit, composition compatibility, semantic novelty, Operator preferences, and final candidate order.

## Required behavior

- generic answer can trigger specificity escalation;
- contradiction can trigger reconciliation;
- incomplete coverage can trigger breadth expansion;
- verified/sufficient evidence can allow advance/close;
- invalid candidate is removed from frontier;
- operator lock constraints remain enforced at runtime.

## Tests

Use scripted answer observations to prove that different answer states select different next moves while the same state produces deterministic output.

## Stop conditions

Stop if the live interview runtime has no safe extension point. Document the exact missing seam and owner rather than creating a second runtime engine.
