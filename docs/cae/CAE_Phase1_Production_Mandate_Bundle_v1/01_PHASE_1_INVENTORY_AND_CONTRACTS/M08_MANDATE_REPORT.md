# Mandate Report

Mandate ID: M08
Title: Programs + Artifacts + Chat Operator Contract
Commit SHA: 4ddc2e1d2ed2877ae50a4fe46516d5603fa25b8e

## Files read
- `docs/PRD/CURRENT.md`
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/00_BUNDLE_MANIFEST.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/05_PROGRAM_PACKAGE_AND_AGENT_CONVENTION.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/06_STATE_AND_HOOKS_MODEL.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/07_PRODUCTION_DEFINITION_OF_DONE.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/08_INITIAL_PROGRAM_INVENTORY.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/17_PHASE1_AGENT_SKILL_OPERATION_OWNERSHIP_GRAPH.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M08_programs_artifacts_chat_operator_contract.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M08_GEMINI_ACTIVATION.md`
- `api/main.py`
- `api/routers/revisions.py`
- `api/routers/ship.py`
- `api/routers/campaigns.py`
- `api/routers/v1_tenancy.py`
- `services/studio/dist/rpc.js`

## Changed files
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/00_CONTROL/18_PHASE1_PROGRAMS_ARTIFACTS_CHAT_OPERATOR_CONTRACT.md`
- `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M08_MANDATE_REPORT.md`

## Authority mapping
- Defined authoritative Program Lifecycle state machine (`DISCOVERED` -> `INITIALIZED` -> `RUNNING` -> `PAUSED` -> `AWAITING_APPROVAL` -> `COMPLETED` / `FAILED` / `UNDER_REPAIR`).
- Defined 8 operator control actions (`DISCOVER`, `RUN`, `INSPECT`, `PAUSE`, `RESUME`, `APPROVE`, `REJECT`, `REPAIR`).
- Established Anti-Stale UI Compare-And-Swap (CAS) Concurrency Protocol (`If-Match-State-Version`, `If-Match-State-SHA256`).
- Bound cryptographic artifact lineage and receipt tracing schemas.
- Mapped Chat commands and natural language supervision grammar to backend routes and Studio tools.

## Tests
- command: `pytest tests/interview_intelligence tests/interview_composer tests/cae -q`
- environment: Windows, Python 3.12 (venv `consciousactivation`)
- fixture/data: Full CAE test suites (tenancy RLS, interview engine, brief composer, adaptive frontier)
- result: 217 passed
- limitation: Offline test suite; live LLM/cloud provider inference mocked/simulated.

- command: `pytest tests/world_intelligence tests/relational_intelligence tests/collision_intelligence tests/segmentation_intelligence tests/attribution_intelligence tests/candidate_intelligence tests/scoring_intelligence tests/operator_intelligence tests/asset_intelligence tests/outcome_intelligence tests/production_program -q`
- environment: Windows, Python 3.12 (venv `consciousactivation`)
- fixture/data: 11 Editorial Intelligence test suites (M01–M11)
- result: 81 passed
- limitation: Offline test suite.

## Runtime evidence
- Total test count: 298 / 298 passing tests verifying tenancy RLS, interview engine, brief compiler, and all 11 Editorial Intelligence services.
- Contract document created at `18_PHASE1_PROGRAMS_ARTIFACTS_CHAT_OPERATOR_CONTRACT.md`.

## Contrastive / false-proof test
- `tests/relational_intelligence/test_workspace_isolation_and_anti_merge.py` (cross-workspace data leakage rejected)
- `tests/segmentation_intelligence/test_segmentation_adversarial_cases.py` (provenance tampering and invalid timecodes rejected)
- `tests/interview_intelligence/test_interview_adversarial_cases.py` (unauthenticated sessions, false proofs rejected)

## Open issues
- Studio web frontend UI is currently decoupled from compiled `services/studio/dist/rpc.js` bridge. Wiring is scheduled for Phase 4 operator UI mandates.

## PRD section updated
- None. Phase 1 inventory and contracts are staged in bundle-local control ledgers; full PRD update consolidated at Phase 1 close (M12).

## Operator decision requested
- Operator approval of Mandate `M08: Programs + Artifacts + Chat Operator Contract` and ratification of `18_PHASE1_PROGRAMS_ARTIFACTS_CHAT_OPERATOR_CONTRACT.md`.
