# Authorized World Intelligence Functions

The following semantic functions are the initial governance surface for agent access.

## Retrieval
- `get_audience_context_premise(audience_id, scope, as_of)`
- `get_audience_schema(audience_id, version)`
- `get_current_audience_state(audience_id, as_of)`
- `get_audience_state_history(audience_id, interval)`
- `get_guest_schema(guest_id, version)`
- `get_guest_state(guest_id, as_of)`
- `get_guest_state_history(guest_id, interval)`
- `get_research_signals(scope, interval)`
- `get_corroborating_evidence(observation_id)`
- `get_active_audience_tensions(audience_id, as_of)`

## Derivation
- `estimate_contextual_state(entity_id, interval)`
- `derive_webhook_candidates(audience_id, scope)`
- `score_signal_corroboration(observation_id)`
- `propose_schema_hypotheses(audience_id, scope)`

## Governance
- `validate_world_object(object_id)`
- `classify_world_error(error_payload)`
- `request_world_repair(object_id, error_code)`

These functions are controlled interfaces, not permission to issue arbitrary SQL.
