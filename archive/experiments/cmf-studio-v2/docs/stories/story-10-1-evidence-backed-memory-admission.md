---
story_id: "10.1"
story_title: "Evidence-Backed Memory Admission"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.01"
pipeline_stage: "14"
entry_object: "approved event or rejected pattern"
exit_object: "`MemoryAdmission`"
validation_contract: "evidence and consent compatibility"
required_receipt: "memory admission receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.1: Evidence-Backed Memory Admission

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.01 |
| Canonical Pipeline Stage | 14 |
| Entry Object | approved event or rejected pattern |
| Exit Object | `MemoryAdmission` |
| Validation Contract | evidence and consent compatibility |
| Required Receipt | memory admission receipt |
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

As an Operator, I want memory admissions proposed only from evidence-backed source, route, approval, publishing, or rejection events, so that the system learns without inventing brand lore.

**Acceptance Criteria:**

- Given an approved asset, route, rejection, or publishing outcome exists, when memory admission is proposed, then it includes source references, provenance, confidence, consent compatibility, originating route, and evidence.
- Given a memory candidate lacks evidence, when admission is requested, then it is rejected.
- Given consent is incompatible, when admission is proposed, then it is blocked or quarantined.
- Given a memory candidate is approved, when saved, then a `MemoryAdmissionApproved` event and memory receipt are written.
- Given a JIT compiler later uses memory, when it cites the memory, then it must reference evidence and memory event ID.

**Technical Notes:** Implement `MemoryAdmissionCandidate`, `MemoryEvent`, memory admission policy, and receipts.

**Legacy and Primitive Mapping:** Brand Memory, Interviewer Memory, Route Memory, rejected-pattern memory, RSCS reality-contact gate. Active families: FBK, SAF, PER.

**Prerequisites:** Epics 1 through 9.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
