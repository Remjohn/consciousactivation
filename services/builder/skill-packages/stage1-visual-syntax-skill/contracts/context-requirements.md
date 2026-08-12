# Context Requirements — Visual Syntax Reconstruction Analyst

## Context Classification Matrix

| Context Element                  | Requirement Status | Description                                                        |
|-----------------------------------|---------------------|----------------------------------------------------------------------|
| `harness_id`                      | REQUIRED            | The single harness the operator has selected for this invocation.   |
| `source_zip_path`                 | REQUIRED            | Path to the specimen bytes to be observed.                          |
| `operator_selected`               | REQUIRED            | Must be `true`. This Skill does not run without it.                 |
| `selected_by` / `selected_at`     | REQUIRED            | Identifies who selected this harness and when.                      |
| `source_zip_sha256_recorded`      | REQUIRED            | Used for the integrity check in execution Step 1.                   |
| `licensing_status`                | FORBIDDEN           | This Skill has no field for licensing/provenance disposition. Do not add one. |
| `provenance_completeness`         | FORBIDDEN           | Same boundary as above — this determination belongs to the operator, made before invocation, not represented in this system at all. |
| `exclusion_reason` / `admission_reason` | FORBIDDEN     | This Skill does not read or write any admission/exclusion register. |
| `next_harness_id`                 | FORBIDDEN           | This Skill never queues or chains to another harness.                |
| `provider_credentials`            | FORBIDDEN           | Skill is provider-neutral; model/tool identity is recorded for disclosure only, not selected by this contract. |
| `runtime_copy`                    | FORBIDDEN           | Out of scope for Stage 1 — this Skill produces structural syntax, not content. |
