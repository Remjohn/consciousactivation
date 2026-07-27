# Observability plan

Required events: `ST-04.02:ResponsibilityModulesCompiled`, `ST-04.02:CapabilityPartitionValidated`, `ST-04.02:ModuleContractsValidated`, `ST-04.02:TestSeamsValidated`, `ST-04.02:OutcomeVerified`, `ST-04.02:CompilationReplayReturned`, `ST-04.02:ResponsibilityModulesInvalidated`, and `ST-04.02:OutcomeRejected`.

Each observation includes run, Story, Harness IR, constitutional report, capability graph, module graph, receipt, authority, version, provenance, module count, capability coverage, dependency count, contract/test-seam coverage, correlation, causation, command, stream, outcome, invalidation, and typed failure context. Do not log source payloads, contract payload values, artifact bytes, personal data, secrets, prompts, or external telemetry.
