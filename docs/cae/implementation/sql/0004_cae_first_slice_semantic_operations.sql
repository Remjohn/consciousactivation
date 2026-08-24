-- WP-03: first-slice typed semantic operations and their allowed transitions.

INSERT INTO cae.semantic_operation(
  operation_id, operation_version, owning_layer, input_contract_ref, output_contract_ref
) VALUES
  ('cae.evidence.capture', '1.0.0', 'interview.source',
   'cae://contracts/evidence-capture/1.0.0', 'cae://contracts/evidence-item/1.0.0'),
  ('cae.evidence.authenticate', '1.0.0', 'interview.source',
   'cae://contracts/evidence-authenticate/1.0.0', 'cae://contracts/evidence-authentication/1.0.0'),
  ('cae.air.propose-assessment', '1.0.0', 'air.context',
   'cae://contracts/semantic-assessment-propose/1.0.0', 'cae://contracts/semantic-assessment/1.0.0'),
  ('cae.air.validate-assessment', '1.0.0', 'air.context',
   'cae://contracts/semantic-assessment-validate/1.0.0', 'cae://contracts/semantic-assessment/1.0.0'),
  ('cae.air.confirm-assessment', '1.0.0', 'human.decision',
   'cae://contracts/semantic-assessment-confirm/1.0.0', 'cae://contracts/semantic-assessment/1.0.0');

INSERT INTO cae.state_transition_contract(
  contract_id, contract_version, aggregate_type, from_state, to_state,
  semantic_operation_id, semantic_operation_version,
  requires_operator_decision, requires_independent_evidence, active
) VALUES
  ('STC-EVID-000', '1.0.0', 'evidence_item', 'CREATED', 'CAPTURED',
   'cae.evidence.capture', '1.0.0', false, true, true),
  ('STC-EVID-001', '1.0.0', 'evidence_item', 'CAPTURED', 'AUTHENTICATED',
   'cae.evidence.authenticate', '1.0.0', false, true, true),
  ('STC-AIR-000', '1.0.0', 'semantic_assessment', 'CREATED', 'PROPOSED',
   'cae.air.propose-assessment', '1.0.0', false, true, true),
  ('STC-AIR-001', '1.0.0', 'semantic_assessment', 'PROPOSED', 'VALIDATED',
   'cae.air.validate-assessment', '1.0.0', false, true, true),
  ('STC-AIR-002', '1.0.0', 'semantic_assessment', 'VALIDATED', 'OPERATOR_CONFIRMED',
   'cae.air.confirm-assessment', '1.0.0', true, true, true);

