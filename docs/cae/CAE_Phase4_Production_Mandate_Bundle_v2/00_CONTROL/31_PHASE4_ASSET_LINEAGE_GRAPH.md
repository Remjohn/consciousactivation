# Phase 4 Asset Lineage Graph

Every production derivative must be traceable:

Source / Interview Evidence
  ↓
EvidenceSegment / SemanticAnnotation
  ↓
ContentCandidate
  ↓
Editorial selection
  ↓
EditorialStoryboard
  ↓
SemanticProgram
  ↓
AssetAnnotation / Script
  ↓
CompositionIR / VideoEditProgram
  ↓
Rendered Artifact
  ↓
QA
  ↓
Approved Release

For each edge record:
- source object
- transformation/program
- state transition
- agent/team/lane where applicable
- Skill/operation used
- receipt
- version
- operator decision where applicable

A derived artifact must never become the source of truth for upstream meaning.
