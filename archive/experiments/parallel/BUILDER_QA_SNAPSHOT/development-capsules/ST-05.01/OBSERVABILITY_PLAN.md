# Observability Plan

Emit deterministic in-memory development/test observations for:

- `synthetic_skill_registry_compilation_started`;
- `synthetic_skill_registry_validated`;
- `synthetic_skill_registry_snapshot_committed`;
- `synthetic_skill_registry_replayed`;
- `synthetic_skill_registry_rejected`;
- `synthetic_skill_registry_invalidated`.

Every observation includes the exact `run_id`, `story_id`, `command_id`, snapshot and registry identities and hashes, policy/schema/validation-receipt hashes, Minimum Complete Context graph identity, capability count, skill/adaptation/experiment counts, authority identity, provenance, version, outcome, failure code, and replay/idempotency status where applicable.

Observations must be deterministic, payload-safe, secret-free, path-free, and committed atomically with their governed state. Failures before commit may produce only the typed returned rejection; they must not leave partial persisted observations.

Completion evidence records representative success, repeat, drift, authority, invalidation, and injected-failure observations plus their hashes.
