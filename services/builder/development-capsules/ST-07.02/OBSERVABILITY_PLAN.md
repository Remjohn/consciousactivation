# Observability Plan

Emit deterministic development/test observations for:

- `synthetic_atomic_harness_definition_started`;
- `synthetic_atomic_harness_definition_validated`;
- `synthetic_atomic_harness_definition_committed`;
- `synthetic_atomic_harness_definition_replayed`;
- `synthetic_atomic_harness_definition_rejected`;
- `synthetic_atomic_harness_definition_invalidated`.

Every observation includes run, Story, command, definition and receipt identities/hashes; target/profile and synthetic classification; Source Lock, boundary, ratification, Draft Model, Harness IR, artifact-set, precedence, capability, module, phase, handoff, context, registry snapshot, necessity-decision references; authority, provenance, version, compatibility, certification marker, outcome, failure context, and replay state.

Payloads are deterministic, path-free, secret-free, and contain no protected examples. Failure before commit leaves no persisted repository observation or partial state.

