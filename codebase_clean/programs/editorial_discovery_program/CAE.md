# Editorial Discovery Program Package

Governed by Phase 3 Mandate M35, Phase 1 M05–M09, and the Editorial Object Register Contracts.
Authority Lanes: HUNTER, ANALYST, COMPOSER, COMMANDER.
Typed Operations:
- segment_interview_turns (HUNTER)
- attribute_and_classify_segment (ANALYST)
- compose_content_candidate (COMPOSER)
- cluster_candidates (ANALYST)
- enforce_synthetic_proof_block (COMMANDER)
- evaluate_production_portfolio (COMMANDER)
- operator_select_candidate (COMMANDER)

Mutation Boundary: CAE PostgreSQL state only via typed operations.
Filesystem contents are composition metadata, not canonical state.
Synthetic candidate producers can never satisfy production gates.
