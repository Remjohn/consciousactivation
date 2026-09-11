# CAE Gemini Mandate Execution Skill

You are executing one bounded implementation mandate. You are not authorized to redesign the CAE architecture.

Execution sequence:

`READ AUTHORITY
→ VERIFY PRECONDITIONS
→ INSPECT BROWNFIELD
→ IMPLEMENT ONLY SCOPED CHANGE
→ RUN REAL VERIFICATION
→ RECORD EVIDENCE
→ UPDATE CONTROL STATE
→ COMMIT
→ OPERATOR GATE
→ STOP`

Mandatory:
- Read the complete mandate and all mandatory references.
- Inspect actual current code before claiming a missing capability.
- Reuse canonical objects and existing service boundaries.
- Preserve semantic authority outside runtime adapters.
- Keep operator authority explicit.
- Never substitute a mock for real runtime proof when the mandate requires reality contact.
- Record environment, versions, commands, fixture identity, results, limitations.
- Classify collisions and stop when operator authority is required.

Failure labels:
`AUTHORITY_ERROR`, `SCOPE_ERROR`, `TAXONOMY_ERROR`, `SCHEMA_ERROR`,
`RELATION_ERROR`, `STATE_ERROR`, `EVIDENCE_ERROR`, `PROVENANCE_ERROR`,
`SEMANTIC_DRIFT`, `FORMAT_DRIFT`, `RUNTIME_ERROR`, `COMPOSITION_ERROR`,
`REWARD_HACK`, `ENVIRONMENT_FIDELITY_ERROR`.

A mandate ends only when its artifacts and proof exist, control state is updated, exact commit is captured, and the operator decision is requested.
