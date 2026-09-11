# Object Authority Map — M65–M72

- Agent identity: `AgentRegistry`
- Agent execution boundary: `AgentInvocation` / `AgentInvocationCompiler` / `AgentInvocationRuntime`
- Context/package: `CompiledAgentPackage` / `JITContextCapsule`
- Program definition: `ProgramRegistry`
- Program operator: `ProgramOperatorRuntimeService`
- Program state: `UniversalProgramStateRuntime`
- Program persistence: existing `IProgramStateStore` implementations
- Workflow compilation: `RuntimeWorkflowCompiler`
- Workflow execution state: `WorkflowRunService`
- Skills: `SkillRegistry`
- Retrieval: `AuthorityFirstRetrievalService`
- Operator/observability command surface: `UnifiedFactoryCommandEngine` as dispatch/projection only
- Certification: `FactoryCertificationRunner`, but only after evidence-derivation repair

A new canonical object may be introduced only when brownfield evidence proves an existing object cannot express the required contract and the Operator explicitly accepts the change.
