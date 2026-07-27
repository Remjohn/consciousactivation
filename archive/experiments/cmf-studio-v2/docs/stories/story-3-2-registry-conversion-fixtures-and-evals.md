---
story_id: "3.2"
story_title: "Registry Conversion, Fixtures, and Evals"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.02"
  - "FR-CMF-03.03"
  - "FR-CMF-03.08"
pipeline_stage: "0"
entry_object: "approved legacy asset"
exit_object: "registry, fixture, eval target"
validation_contract: "schema/eval activation gate"
required_receipt: "registry activation receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.2: Registry Conversion, Fixtures, and Evals

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.02, FR-CMF-03.03, FR-CMF-03.08 |
| Canonical Pipeline Stage | 0 |
| Entry Object | approved legacy asset |
| Exit Object | registry, fixture, eval target |
| Validation Contract | schema/eval activation gate |
| Required Receipt | registry activation receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Preserve the high-value legacy intelligence and its intentional orchestration logic as typed, evaluated, Python-first assets while blocking direct legacy runtime dependency and stale stack assumptions.

**Covers:** FR-CMF-03.01 through FR-CMF-03.09.

**User Value:** Migration Stewards and AI agents can recover the depth of CCP/CMF intelligence while production remains clean, typed, testable, and greenfield.

**Technical Context:** `/api/v1/legacy-migration`, `/api/v1/registries`, MigrationWorkflow, `legacy_inventory_items`, `migration_ledger_entries`, `legacy_orchestration_intent_records`, `migrated_registry_entries`, `fixture_sets`, `evaluation_targets`, DSPy programs, CI import gate.

**CBAR Failure Scenario:** If legacy intelligence is flattened into prompts, CMF loses its edge. If legacy runtime is imported directly, the greenfield architecture inherits fragmentation. The resolution is typed migration plus explicit compiler/eval targets.

## Story Definition

As a Migration Steward, I want to convert archetypes, primitives, SDA/SFL assets, CBAR gates, TTT profiles, creative subsystem rules, Voice DNA logic, and CMF references into typed registries and test assets, so that production intelligence is reusable and verifiable.

**Acceptance Criteria:**

- Given a legacy archetype prompt is approved, when migration runs, then it produces a typed registry entry with examples, counterexamples, source hash, route constraints, and eval target.
- Given a cognitive primitive is migrated, when validation runs, then schema, source examples, failure cases, and registry family are required before activation.
- Given SDA/SFL assets are migrated, when fixtures are created, then downstream extraction, audio, compression, and evaluation tests can reference them.
- Given a CMF engine reference is migrated, when it is not approved as production code, then it is recorded as reference behavior or fixture only.
- Given a registry entry lacks eval coverage, when activation is requested, then it is blocked.

**Technical Notes:** Implement `RegistryEntry`, `FixtureSet`, `EvaluationTarget`, `tests/fixtures`, and `tests/evals` targets. Registry activation is a command with receipt.

**Legacy and Primitive Mapping:** 244 primitives, 44 SDA/SFL files, 96 archetype prompts, 34 creative subsystems, CBAR gates, TTT profiles, Voice DNA, CMF references. Active families: PSY, STR, VOC, VSG, FBK.

**Prerequisites:** Story 3.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
