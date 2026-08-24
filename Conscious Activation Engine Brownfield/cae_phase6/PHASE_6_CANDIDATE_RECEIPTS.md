# Phase 6 Candidate Receipts

Every candidate generation run must produce durable traceability.

## CandidateReceipt

```yaml
receipt_type: CandidateReceipt
candidate_id:
compilation_run_id:
evidence_ids:
primitive_id:
candidate_text:
semantic_operation:
survival_scores:
eligibility_verdict:
rejection_code:
validator_results:
anti_centroid_result:
created_at:
model_context_hash:
registry_version:
```

## CoalitionReceipt

```yaml
receipt_type: CoalitionReceipt
coalition_id:
compilation_run_id:
candidate_ids:
primitive_weights:
compatibility_matrix:
routeability:
edge_product_id:
validator_results:
fatality_flags:
created_at:
```

## SemanticCompilationReceipt

```yaml
receipt_type: SemanticCompilationReceipt
run_id:
input_packet_ids:
invariant_field_version:
geometry_packet_ids:
candidate_ids:
selected_coalition_id:
edge_product_id:
handoff_charge:
anti_centroid_status:
directional_integrity_status:
hard_negative_status:
error_codes:
output_status:
timestamp:
```

These receipts are the debugging and learning substrate. They must make it possible to answer why an Edge Product existed without rereading every agent transcript.
