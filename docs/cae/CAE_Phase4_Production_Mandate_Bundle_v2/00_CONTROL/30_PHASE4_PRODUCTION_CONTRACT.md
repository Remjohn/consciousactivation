# Phase 4 Production Contract

Phase 4 is the last implementation/acceptance phase. Its job is to turn already-built semantic
and runtime capabilities into a real supervised production path.

## Production chain

Authenticated evidence
→ editorial candidate
→ operator selection
→ EditorialStoryboard / SemanticProgram
→ Script
→ Visual Demand / AssetAnnotation
→ Carousel / SuperVisual / Animation / VideoEdit
→ CompositionIR
→ VAE / visual realization where required
→ Render / QA
→ Operator approval
→ Ship
→ Outcome
→ learning

## Production truth rules

- No synthetic candidate can become a production artifact.
- No production artifact can be accepted without evidence lineage.
- No artifact can ship without the required operator gate.
- No rendering success alone proves semantic correctness.
- No semantic plan may silently change protected source meaning.
- Production derivatives are downstream projections; source evidence remains authoritative.

## Status distinction

BUILD_EXISTS
RUNTIME_EXECUTED
SEMANTICALLY_VALIDATED
PRODUCTION_VALIDATED
OPERATOR_ACCEPTED
SHIPPED

A Program is only a production candidate when the relevant level has evidence.
