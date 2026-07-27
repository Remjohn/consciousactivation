# Observability plan

The branch reuses the completed `ST-01.01` event and audit seams. Each authoritative command must correlate one command decision with any resulting transition and event.

Required evidence fields:

- `run_id`, `command_id`, and `event_id`;
- compilation target `atomic_content_harness`;
- profile ID, version, and exact profile hash;
- empty-registry ID, version, and exact registry hash;
- actor ID, actor role, authority rule, and authorization result;
- prior state, requested transition, resulting state, and transition result;
- checkpoint ID and replay/idempotency disposition;
- `synthetic`, `repository_owned`, `non_production`, `non_certified`, and `builder_core_validation_only` markers;
- deterministic timestamp supplied by the test clock;
- failure type and no-mutation proof for denied operations.

Completion evidence must contain one successful start/resume trace, one replay trace with no duplicate event, one unauthorized-transition trace, one fixture-drift rejection, and one undeclared-skill rejection. The evidence serialization must have a recorded SHA-256 digest and must contain no payload from Format 02 or an external runtime.
