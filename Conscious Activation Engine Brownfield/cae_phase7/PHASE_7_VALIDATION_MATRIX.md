# Phase 7 Validation Matrix

| Layer | Question | Primary validator | Failure |
|---|---|---|---|
| Edge preservation | Is the same force still present? | EdgePreservationValidator | EDGE_PRESERVATION_ERROR |
| Archetype | Is the structural carrier valid? | ArchetypeEligibilityValidator | ARCHETYPE_ERROR |
| SFL | Are functions canonical and appropriate? | SFLRegistryValidator | SFL_REGISTRY_ERROR |
| Alignment | Is perceptual use aligned? | SFLAlignmentValidator | SFL_ALIGNMENT_ERROR |
| Depth | Is added depth meaningful? | DepthProfileValidator | SFL_FALSE_DEPTH / DEPTH_PROFILE_ERROR |
| Directive | Did human intent survive compilation? | DirectiveValidator | DIRECTIVE_ERROR |
| Program | Is downstream IR complete and bounded? | SemanticProgramValidator | SEMANTIC_PROGRAM_ERROR |
| Anti-centroid | Was specificity preserved? | AntiCentroidValidator | CENTROID_DRIFT |
| Phase boundary | Is realization deferred? | DownstreamContractValidator | PHASE_BOUNDARY_ERROR |
