# Observability plan

Required events: `ST-04.03:PhaseGraphCompiled`, `ST-04.03:TopologyValidated`, `ST-04.03:RunnableStateDerived`, `ST-04.03:ParallelismValidated`, `ST-04.03:OutcomeVerified`, `ST-04.03:CompilationReplayReturned`, `ST-04.03:PhaseGraphInvalidated`, and `ST-04.03:OutcomeRejected`.

Each observation includes run, Story, Harness IR, constitutional report, capability graph, module graph, phase graph, receipt, authority, version, provenance, phase/module/dependency/gate/runnable/blocked/parallel counts, correlation, causation, command, stream, outcome, invalidation, and typed failure context. Do not log source payloads, artifact bytes, personal data, secrets, prompts, or external telemetry.
