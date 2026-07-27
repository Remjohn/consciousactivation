---
story_id: "3.1"
story_title: "Migration Ledger Inventory and Hashing"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-03.01"
  - "FR-CMF-03.08"
pipeline_stage: "0"
entry_object: "legacy source path"
exit_object: "`MigrationLedgerEntry`"
validation_contract: "hash and migration target"
required_receipt: "migration receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 3.1: Migration Ledger Inventory and Hashing

**Epic:** 3 - Legacy Intelligence and JIT Skill Governance
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-03.01, FR-CMF-03.08 |
| Canonical Pipeline Stage | 0 |
| Entry Object | legacy source path |
| Exit Object | `MigrationLedgerEntry` |
| Validation Contract | hash and migration target |
| Required Receipt | migration receipt |
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

As a Migration Steward, I want to inventory, classify, hash, and map legacy assets, so that every reused idea has provenance and an approved migration destination.

**Acceptance Criteria:**

- Given a legacy asset is proposed, when it is added to the ledger, then the system records source path, legacy type, registry family/domain, canonicality confidence, owner, runtime language, valuable mechanics, defects, content hash, and status.
- Given an asset is mapped, when the Steward saves the record, then it includes target Python package, Pydantic contract target, DSPy program target when applicable, TypeScript leaf target if applicable, fixture target, eval target, and reviewer.
- Given a hash changes, when the ledger is refreshed, then the system flags the asset for review rather than silently updating the canonical source.
- Given an asset is blocked, when an agent references it, then the system returns the approved reason and replacement target if available.
- Given ledger changes are approved, when the command completes, then a migration receipt is written.

**Technical Notes:** Implement `LegacyAssetInventoryItem`, `MigrationLedgerEntry`, `/api/v1/legacy-migration`, and `MigrationWorkflow` steps through review.

**Legacy and Primitive Mapping:** Directly uses Legacy Inventory ledger fields and content hashes. Active families: STR, SAF, PER.

**Prerequisites:** Epic 1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
