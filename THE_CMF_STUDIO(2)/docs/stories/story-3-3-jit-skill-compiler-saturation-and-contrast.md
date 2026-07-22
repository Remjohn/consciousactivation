---
story_id: "3.3"
story_title: "JIT Skill Compiler Saturation and Contrast"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.04"
  - "FR-CMF-03.05"
pipeline_stage: "3 / 4 / 6 / 7"
entry_object: "saturation context"
exit_object: "`SkillInvocationRecord` and proposals"
validation_contract: "grounded context and anti-draft gate"
required_receipt: "skill invocation receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.3: JIT Skill Compiler Saturation and Contrast

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.04, FR-CMF-03.05 |
| Canonical Pipeline Stage | 3 / 4 / 6 / 7 |
| Entry Object | saturation context |
| Exit Object | `SkillInvocationRecord` and proposals |
| Validation Contract | grounded context and anti-draft gate |
| Required Receipt | skill invocation receipt |
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

As an Operator or agent, I want migrated JIT Skill compilers to use saturation context, drafting, contrast, calibration, and evaluation, so that extraction and routing exceed generic script prompting.

**Acceptance Criteria:**

- Given a JIT Skill compiler runs, when it receives input, then it must include source docs, transcript segments, guest dossier, audience reality, brand context, primitive candidates, prior evaluation history, and failure corpus where relevant.
- Given the compiler drafts candidate outputs, when it returns results, then it also returns contrast candidates, anti-draft calibration, evidence references, and confidence.
- Given a compiler output cannot cite saturation context, when it tries to influence routing or extraction, then it is rejected.
- Given a compiler identifies narrative induction material, when it emits guidance, then it distinguishes live guest extraction support from transcript/source extraction.
- Given a compiler output passes, when it is stored, then the receipt includes DSPy program version, input hashes, output schema, eval score, and reviewer state if required.

**Technical Notes:** Implement `JITSkillCompiler`, `DSPyProgramSpec`, `ccp_studio.dspy_programs.jit_skill_compilers`, eval tests, and receipt writing. DSPy owns reasoning, not canonical state.

**Legacy and Primitive Mapping:** Legacy skills modules, anti-draft calibrator, Narrative Intelligence, RSCS saturation/collision/compression/evaluation, CBAR. Active families: STR, PSY, TRG, VOC, FBK.

**Prerequisites:** Stories 3.1 and 3.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
