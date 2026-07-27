# Observability plan

Required events:

- `ST-03.05:ConstitutionalValidationCompleted`
- `ST-03.05:CrossArtifactCompletenessValidated`
- `ST-03.05:ConstitutionalPrecedenceValidated`
- `ST-03.05:OutcomeVerified`
- `ST-03.05:ValidationReplayReturned`
- `ST-03.05:ConstitutionalConflictDetected`
- `ST-03.05:ConstitutionalValidationInvalidated`
- `ST-03.05:OutcomeRejected`

Each observation includes run, Story, HarnessIR, artifact set, manifest, policy, report, receipt, authority, version, correlation, causation, command, stream, outcome, finding codes, affected artifact paths and IR nodes, completeness count, semantic-lineage disposition, compatibility, invalidation, and typed failure context.

Do not log artifact payloads, source content, personal data, secrets, tokens, model prompts, external telemetry, or production claims.
