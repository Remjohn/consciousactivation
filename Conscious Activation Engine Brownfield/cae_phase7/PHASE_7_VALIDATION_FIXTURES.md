# Phase 7 Validation Fixtures

## Fixture A — Same Edge, two valid archetypes
Purpose: confirm the selector can choose between carriers based on state/capacity without changing the Edge.

## Fixture B — Popular archetype, invalid edge fit
Expected: reject despite historical performance.

## Fixture C — SFL stack over-activation
Expected: `SFL_STACK_OVERLOAD` and targeted sparsification.

## Fixture D — SFL changes meaning
Expected: `SFL_SEMANTIC_OVERRIDE`.

## Fixture E — Human Director Note
Input prose:
> “Keep the tension sharp. Do not turn this into a motivational lesson. I want recognition first.”

Expected: typed directive set with recognition as desired effect and motivational framing as forbidden effect.

## Fixture F — RLHF-style centroid drift
Input edge is highly specific, output program becomes generic.  
Expected: `CENTROID_DRIFT` and source-specific repair.

## Fixture G — False-depth SFL
Program adds symbols, ambiguity and repetition without increasing semantic signal.  
Expected: `SFL_FALSE_DEPTH`.

## Fixture H — Phase boundary violation
SemanticProgram contains concrete shot IDs or frame coordinates.  
Expected: `PHASE_BOUNDARY_ERROR`.

## Fixture I — Missing registry lineage
A runtime SFL function has no canonical function ID.  
Expected: `SFL_UNKNOWN_FUNCTION`.

## Fixture J — Reproducibility
Re-running Phase 7 with the same snapshots and directives should reproduce the same structural decision within the declared probabilistic exploration tolerance.
