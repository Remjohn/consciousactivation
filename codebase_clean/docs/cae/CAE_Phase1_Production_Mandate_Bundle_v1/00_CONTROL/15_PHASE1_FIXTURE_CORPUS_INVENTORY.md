# Phase 1 Fixture / Test Corpus Inventory

Required positive fixture classes:
Workspace, Guest, Audience, Research source, Knowledge node, Research signal,
CollisionHypothesis, InterviewBrief, InterviewResponse, EvidenceSegment, SemanticAnnotation,
ContentCandidate, EditorialStoryboard, AssetAnnotation, SemanticProgram, CompositionIR,
VideoEditProgram, Outcome.

Required negative fixtures:
wrong Workspace, missing provenance, invalid transition, missing receipt, receipt/artifact mismatch,
unsupported semantic claim, Skill nesting, lane violation, duplicate/replay, interrupted/resumed run,
operator bypass, stale package/hash mismatch.

Every fixture records authority, creation method, stable IDs, reset strategy, invariant and cleanup.
