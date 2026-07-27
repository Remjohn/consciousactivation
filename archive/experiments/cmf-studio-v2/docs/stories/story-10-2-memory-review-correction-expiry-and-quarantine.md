---
story_id: "10.2"
story_title: "Memory Review, Correction, Expiry, and Quarantine"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.02"
pipeline_stage: "14"
entry_object: "memory event"
exit_object: "corrected/expired/quarantined memory"
validation_contract: "provenance and reversal gate"
required_receipt: "memory governance receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.2: Memory Review, Correction, Expiry, and Quarantine

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.02 |
| Canonical Pipeline Stage | 14 |
| Entry Object | memory event |
| Exit Object | corrected/expired/quarantined memory |
| Validation Contract | provenance and reversal gate |
| Required Receipt | memory governance receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Let CMF STUDIO learn from approved evidence, expose relationship intelligence through Neo4j, and recover workflows without hidden scripts or manual database edits.

**Covers:** FR-CMF-10.01 through FR-CMF-10.07.

**User Value:** Operators can inspect memory, relationships, queues, failures, costs, blockers, and recovery actions while canonical state remains safe and rebuildable.

**Technical Context:** `/api/v1/memory`, `/api/v1/operations`, `/api/v1/projections`, `memory_admission_candidates`, `memory_events`, `projection_checkpoints`, `operational_incidents`, `recovery_actions`, Neo4j projection, domain event outbox.

**CBAR Failure Scenario:** If memory becomes lore, it will corrupt future interviews and routes. If Neo4j becomes canonical, production decisions become unrecoverable. Evidence memory and graph projection must remain governed and rebuildable.

## Story Definition

As an Operator, I want to inspect, correct, reverse, expire, or quarantine memory admissions, so that wrong, stale, sensitive, or unsupported memory can be controlled.

**Acceptance Criteria:**

- Given memory exists, when the Memory Review surface opens, then it shows evidence, source references, route, confidence, consent compatibility, created event, and downstream usage.
- Given memory is wrong, when correction is approved, then the system writes a superseding memory event rather than mutating history.
- Given memory is stale, when expiry is approved, then future compilers cannot use it except as historical evidence.
- Given memory is sensitive, when quarantine is approved, then downstream use is blocked until resolved.
- Given memory is reversed, when future routes are compiled, then the reversal is respected.

**Technical Notes:** Memory events are append-only. Implement correction/reversal/expiry/quarantine commands and UI.

**Legacy and Primitive Mapping:** Product Brief memory doctrine and Legacy Inventory receipt chain. Active families: SAF, FBK, PER.

**Prerequisites:** Story 10.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
