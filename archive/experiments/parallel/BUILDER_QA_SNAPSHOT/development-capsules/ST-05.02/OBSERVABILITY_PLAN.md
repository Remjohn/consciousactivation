# Observability Plan

Emit deterministic development/test observations for:

- `synthetic_skill_necessity_started`;
- `synthetic_skill_alternatives_assessed`;
- `synthetic_no_skill_decision_committed`;
- `synthetic_skill_necessity_replayed`;
- `synthetic_skill_necessity_rejected`;
- `synthetic_skill_necessity_invalidated`.

Every observation includes run, Story, command, decision and receipt identities/hashes, ST-05.01 snapshot/registry/policy identities, Minimum Complete Context identity, capability count, target-failure count, alternative-assessment count, selected-owner counts, new-skill/adaptation/brief counts, brief disposition, authority, provenance, version, outcome, failure context, and replay state.

Payloads are deterministic, path-free, secret-free, and contain no protected examples. Failure before commit leaves no persisted repository observation or partial state.
