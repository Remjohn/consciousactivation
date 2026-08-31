# Mandate Report

Mandate ID: M10
Title: Builder → Harness → Pipeline Binding Contract
Commit SHA: 1b65889723e0eda405543e74a43304703307abca

## Files read
- `docs/PRD/CURRENT.md`
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/00_BUNDLE_MANIFEST.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/03_PARALLELISM_MATRIX.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/05_PROGRAM_PACKAGE_AND_AGENT_CONVENTION.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/06_STATE_AND_HOOKS_MODEL.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/07_PRODUCTION_DEFINITION_OF_DONE.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/08_INITIAL_PROGRAM_INVENTORY.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/10_PHASE1_RUNTIME_TRACEABILITY_MATRIX.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/12_PHASE1_HARNESS_READINESS_LADDER.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M10_builder_harness_pipeline_binding_contract.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M10_GEMINI_ACTIVATION.md`
- `docs/HARNESS_AUTHORING_MASTER_PROMPTS.md`
- `docs/Harness Compilation Task.md`
- `services/builder/AGENTS.md`
- `services/builder/PROGRAM_STATUS_EXPORT.yaml`
- `services/builder/MANIFEST.json`
- `services/builder/src/cmf_builder/domain/operator_manifest.py`
- `services/builder/src/cmf_builder/domain/portable_export.py`
- `services/builder/src/cmf_builder/domain/capability_ownership.py`
- `services/builder/src/cmf_builder/domain/atomic_harness_definition.py`
- `services/builder/src/cmf_builder/domain/skill_registry.py`
- `services/pipeline/AGENTS.md`
- `services/pipeline/PROGRAM_STATUS_EXPORT.yaml`
- `services/pipeline/src/cmf_pipeline/intake/definition_intake.py`
- `services/pipeline/src/cmf_pipeline/intake/harness_compiler.py`
- `services/pipeline/src/cmf_pipeline/bindings/compiler.py`
- `services/pipeline/src/cmf_pipeline/workflow/domain/models.py`
- `services/pipeline/src/cmf_pipeline/domain/enums.py`
- `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py`
- `services/pipeline/src/cmf_pipeline/demo.py`
- `tests/pipeline/test_harness_compiler.py`

## Changed files
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M10_MANDATE_REPORT.md`

## Authority mapping
- Reconciled field-level runtime contract across 4 authoritative representations: Authoring Manifest (`OperatorManifestDocument`), Distribution Package (`PortableAtomicHarnessDefinition`), Pipeline Intake (`AtomicHarnessDefinitionIntake`), and Execution Workflow (`RuntimeWorkflowCompiler` / `validate_runtime_workflow` / `Pi Substrate`).
- Defined explicit 1:1 mapping across 21 critical fields covering definition identity, SemVer validation, category binding, execution profile, semantic lineage, capability metadata, workflow DAG (nodes & edges), actor kinds, authority lanes, product boundaries, side effect classes, state machine progression, skill immutability, tool bindings, pre/post-step hooks, cryptographic receipts, repair laws, wrong-reading locks, and non-production certification ceilings.
- Preserved strict lane sovereignty: 4 Authority Lanes (`HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`) without lane collapsing.
- Guaranteed skills remain flat and passive without recursive or unmonitored skill invocations.
- Enforced typed CAE operations (`cae.harness_run`, `cae.receipt`) as the immutable state mutation boundary.

## Tests
- command: `pytest tests/pipeline -q`
- environment: Windows, Python 3.12 (venv `consciousactivation`)
- fixture/data: Full pipeline harness compiler & intake test suites (`test_harness_compiler.py`)
- result: 17 passed
- limitation: Validates in-memory and SQLite repository pipeline transformations; live cloud orchestration mocked.

- command: `pytest tests/cae -q`
- environment: Windows, Python 3.12 (venv `consciousactivation`)
- fixture/data: Full CAE test suites (tenancy RLS, state machine coverage, mutation operations, receipts, hooks)
- result: 121 passed
- limitation: Offline test suite.

- command: `pytest tests/productization tests/release tests/corrections tests/stories/st_07_02 -q` (in `services/builder`)
- environment: Windows, Python 3.12 (venv `consciousactivation`)
- fixture/data: Builder domain contracts, portable export verification, operator manifest parsing, synthetic proofs
- result: 220 passed
- limitation: Pure Python domain models; file system packaging tested via in-memory structures and fixtures.

## Runtime evidence
- 17 / 17 Pipeline tests passing, validating all 7 compiler intake blockers and complete round-trip conversion from portable export to executable intake.
- 121 / 121 CAE core contract tests passing.
- 220 / 220 Builder domain and release tests passing.
- Full contract formalized and ratified in `14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`.

## Contrastive / false-proof test
- `tests/pipeline/test_harness_compiler.py::TestBlocker1SemanticDependencies::test_blocker_1_missing_semantic_dependencies_raises` (missing cryptographic dependency lineage rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker2CapabilityMetadata::test_blocker_2_missing_capability_metadata_raises` (untyped or missing capability metadata rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker3GenericMode::test_blocker_3_generic_mode_raises` (generic non-activative harness rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker4Semver::test_blocker_4_invalid_semver_raises` (invalid semantic versioning rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker5Workflow::test_blocker_5_missing_workflow_raises` (missing execution DAG rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker6EvaluationAndRepair::test_blocker_6_missing_evaluation_raises` (missing evaluation requirements rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker6EvaluationAndRepair::test_blocker_6_missing_repair_laws_raises` (missing recovery laws rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker7InvalidationState::test_blocker_7_invalid_state_raises` (invalid or corrupted invalidation states rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker9ProductionGates::test_blocker_9_production_eligible_raises` (premature production eligibility claims rejected)
- `tests/pipeline/test_harness_compiler.py::TestBlocker9ProductionGates::test_blocker_9_certified_raises` (premature certification claims rejected)

## Open issues
- Async Pi runtime execution and actor dispatching across distributed worker nodes scheduled for Phase 2 Mandate `M21`.

## PRD section updated
- None. Phase 1 inventory and contracts are staged in bundle-local control ledgers; full PRD update consolidated at Phase 1 close (M12).

## Operator decision requested
- Operator approval of Mandate `M10: Builder → Harness → Pipeline Binding Contract` and ratification of `14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`.
