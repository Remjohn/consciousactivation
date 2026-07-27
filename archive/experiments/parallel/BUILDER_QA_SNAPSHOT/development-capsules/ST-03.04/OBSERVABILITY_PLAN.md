# Observability plan

Emit immutable Story observations through the existing sink:

- `ST-03.04:ArtifactSetCompiled`
- `ST-03.04:ArtifactManifestCommitted`
- `ST-03.04:CrossArtifactConsistencyValidated`
- `ST-03.04:OutcomeVerified`
- `ST-03.04:CompilationReplayReturned`
- `ST-03.04:ArtifactDriftDetected`
- `ST-03.04:ArtifactSetInvalidated`
- `ST-03.04:OutcomeRejected`

Each observation includes run/Story/artifact-set/manifest/authority identity; IR ID/hash/schema/revision; compiler ID/version/config hash; generation timestamp; target/profile/source-lock refs; artifact count/bytes; dependency selectors; reproducibility, drift, quarantine, compatibility, and nondeterminism dispositions; correlation, causation, command, stream, outcome, receipt, and typed failure context.

Completion evidence must capture one deterministic compile, replay, manual drift, unauthorized attempt, altered-IR rejection, atomic failure, and upstream invalidation trace. It must prove zero partial authoritative mutation on failure.

Do not log artifact payloads, source content, personal data, secrets, tokens, external telemetry, model prompts, or production claims.
