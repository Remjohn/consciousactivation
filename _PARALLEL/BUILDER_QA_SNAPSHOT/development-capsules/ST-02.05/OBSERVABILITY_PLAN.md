# Observability plan

Emit immutable Story-scoped observations through the existing sink. Success events are:

- `ST-02.05:BoundaryRatified`
- `ST-02.05:DraftModelCompiled`
- `ST-02.05:BoundaryFrozen`
- `ST-02.05:OutcomeVerified`

Decision and invalidation events are `ST-02.05:BoundaryRevisionRequested`, `ST-02.05:BoundaryRejected`, `ST-02.05:BoundaryReopened`, and `ST-02.05:DraftModelInvalidated`. Failure evidence is `ST-02.05:OutcomeRejected`.

Every observation must include `run_id`, `story_id`, `artifact_identity`, `authority_identity`, contract `version`, `provenance`, `outcome`, typed `failure_context`, `correlation_id`, `causation_id`, `command_id`, `stream_version`, target/profile identity, `source_lock_id`, declared-input hash, boundary ID/version/status, selected candidate, model ID/hash/status when assigned, ratification or decision receipt ID/hash when assigned, `HG-003` result, and invalidated artifact IDs when applicable.

The completion evidence must provide one deterministic approval trace, one revise/reject trace, one unauthorized trace, one contradiction trace, one atomic-commit-failure trace, one replay trace, and one reopen/invalidation trace. It must show that rejection and failed atomic commit produced zero authoritative mutation and that the completion receipt links to the final evidence hashes.

No personal data, content payloads, secrets, tokens, external telemetry, or production claims may be logged.
