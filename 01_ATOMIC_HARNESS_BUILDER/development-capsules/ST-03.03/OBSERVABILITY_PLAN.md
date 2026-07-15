# Observability plan

Emit immutable Story observations through the existing sink:

- `ST-03.03:HarnessIRCompiled`
- `ST-03.03:HarnessIRSnapshotCommitted`
- `ST-03.03:CompatibilityValidated`
- `ST-03.03:OutcomeVerified`
- `ST-03.03:CompilationReplayReturned`
- `ST-03.03:HarnessIRInvalidated`
- `ST-03.03:OutcomeRejected`

Every observation must include run/Story/artifact/authority identity; schema ID/version/revision; IR ID/hash/status; target/profile identity; Source Lock, boundary, ratification, model, and constitution refs; knowledge/authority summary; Activative lineage disposition; compatibility/migration/deprecation disposition; dependency-impact refs; correlation, causation, command, and stream identity; outcome and typed failure context; invalidated identities when applicable.

Completion evidence must provide one deterministic compile trace, one replay trace, one missing-provenance or forbidden-field rejection, one unauthorized-write rejection, one injected atomic-failure trace, and one upstream-reopen/IR-invalidation trace. It must prove zero partial authoritative mutation for failed commands.

No source content payloads, personal data, secrets, tokens, external telemetry, model prompts, or production claims may be logged.
