# Baseline Authority Read Set

Every mandate MUST read these in full before action, then read the mandate-specific set.

## CAE product and governance

- `docs/PRD/CURRENT.md`
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/constitutions/` — all constitution files relevant to the mandate's objects/scope
- `governance/program-control/` — current control-state and current reconciliation ledger
- `docs/cae/editorial_intelligence/` — authority/object/plane/dependency material relevant to the mandate

## Builder / Harness governance

- `docs/HARNESS_AUTHORING_MASTER_PROMPTS.md`
- `docs/HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md`
- `docs/Harness Compilation Task.md`
- `services/builder/AGENTS.md`
- `services/builder/CURRENT_PROJECT_STATUS.md`
- `services/builder/MANIFEST.json`
- `services/builder/PROGRAM_STATUS_EXPORT.yaml`
- `services/builder/skill-packages/` relevant Skill packages
- `services/builder/src/cmf_builder/` relevant implementation paths

## Pipeline / state governance

- `services/pipeline/AGENTS.md`
- `services/pipeline/CURRENT_PROJECT_STATUS.md`
- `services/pipeline/PROGRAM_STATUS_EXPORT.yaml`
- `services/pipeline/src/cmf_pipeline/workflow/`
- `services/pipeline/src/cmf_pipeline/intake/`
- `services/pipeline/src/cmf_pipeline/bindings/`
- `services/pipeline/src/cmf_pipeline/reasoning/`
- `services/pipeline/src/cmf_pipeline/evaluation/`
- relevant `services/pipeline/docs/tech-specs/`

## State

- `docs/cae/state/`
- `packages/ca_runtime/` relevant state/authority implementation
- relevant SQL migrations/schema
- relevant tests under `tests/cae/`

## App / product surfaces

- relevant `docs/tech-specs/TS-APP-*.md`
- relevant `api/routers/`
- relevant `api/services/`
- `apps/web/` affected surface

## Reading rule

A directory name is not evidence that its contents were read. The executing agent must list
the relevant files, read each required file in full, and report the files actually read.
For code work, inspect exact symbols/callers with repository search before editing.

Do not rely on old bundle summaries if the current repository has moved.
