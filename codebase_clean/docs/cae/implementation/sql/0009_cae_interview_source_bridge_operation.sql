-- WP-09: one typed CAE-side bridge operation for an existing Interview
-- Expression source package. The legacy source remains read-only authority.

INSERT INTO cae.semantic_operation(
  operation_id, operation_version, owning_layer, input_contract_ref, output_contract_ref
) VALUES (
  'cae.bridge.register-interview-source', '1.0.0', 'interview.source.bridge',
  'cae://contracts/interview-source-bridge/1.0.0',
  'cae://contracts/verified-source-registration/1.0.0'
);

INSERT INTO cae.state_transition_contract(
  contract_id, contract_version, aggregate_type, from_state, to_state,
  semantic_operation_id, semantic_operation_version,
  requires_operator_decision, requires_independent_evidence, active
) VALUES (
  'STC-BRIDGE-000', '1.0.0', 'source_package', 'CREATED', 'VERIFIED',
  'cae.bridge.register-interview-source', '1.0.0', false, true, true
);
