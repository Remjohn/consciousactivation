---
tech_spec_id: "TS-CMF-062"
title: "Persona Code Registry and Validation"
story_id: "11.1"
story_title: "Persona Code Registry and Validation"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-1-persona-code-registry-and-validation.md"
fr_ids:
  - "PRD-CMF-10.00"
module_requirement_ids:
  - "PRD-CMF-10.00"
pipeline_stage: "agent-factory overlay"
entry_object: "department and entity naming request"
exit_object: "persona code registry"
validation_contract: "`DDD-XXXXXXX-TT` code validation"
required_receipt: "persona registry receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Agent Factory registry"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-062: Persona Code Registry and Validation

**Status:** Ready for Development  
**Story:** `11.1 - Persona Code Registry and Validation`  
**Implementation Boundary:** Persona code schema, department code registry, entity type registry, canonical persona records, uniqueness checks, validation receipts, and read models for agent UI/spec workflows.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-1-persona-code-registry-and-validation.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | PRD-CMF-10.00 persona code authority. |
| `docs/cmf-studio-agent-factory-registry.md` | Canonical department/type codes and 63 initial persona codes. |
| `docs/cmf-studio-agent-factory-architecture.md` | Agent Factory architecture and runtime identity model. |
| `docs/cmf-studio-agent-intelligence-contract.md` | Entity code usage in role specs and runtime contracts. |
| `docs/cmf-studio-pipeline-map.md` | Pipeline stage and department map. |
| `docs/migration/legacy-inventory.md` | Legacy orchestration traceability context. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Signal-density quality filter for non-generic persona codes. |

## 2. Overview

The persona code registry gives every Factory entity a stable operational identity. Codes must follow `DDD-XXXXXXX-TT`: three-character department, exactly seven-character service role, and two-character entity type. The code must reveal what the entity serves, not merely provide a poetic persona.

The registry is used by `AgentRoleSpec`, `SubAgentRoleSpec`, hooks, extensions, skills, evals, receipts, handoff packets, UI filters, logs, stories, tech specs, and generated ADK/Agents CLI adapters. It is the first guard against agent drift because it ties an entity name to department, service, type, lifecycle, and source proof.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.00 | Every Factory entity uses `DDD-XXXXXXX-TT`, with service-revealing identity and stable traceability. | Pydantic schema, department/type enums, uniqueness checks, registry receipts, UI/read model, tests. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | agent-factory overlay |
| Entry Object | department and entity naming request |
| Exit Object | persona code registry |
| Validation Contract | `DDD-XXXXXXX-TT` code validation |
| Required Receipt | persona registry receipt |

### Legacy Intelligence Mapping

- Legacy CCF/CMF modules often used evocative names, but CMF Studio needs service-revealing operational identity.
- The registry preserves intentional orchestration by requiring department, service, entity type, source refs, and downstream use.
- Active primitive families SAF, BUS, and FBK govern safety, operational clarity, and feedback.

## 4. Implementation Plan

1. Add `DepartmentCode`, `EntityTypeCode`, `PersonaCode`, `PersonaRegistryEntry`, and `PersonaRegistryReceipt` contracts.
2. Implement code parser and validator for `DDD-XXXXXXX-TT`.
3. Seed canonical department codes and entity type codes from `docs/cmf-studio-agent-factory-registry.md`.
4. Seed the initial 63 persona records.
5. Add uniqueness checks for `entity_code` and duplicate department/service/type collisions.
6. Add service-name quality check that rejects code bodies that do not map to a role/service description.
7. Add read model for UI/spec usage and API endpoints for list/inspect/validate.
8. Emit `PersonaRegistryReceipt` for create/update/reject actions.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class EntityTypeCode(str, Enum):
    AG = "AG"
    SA = "SA"
    HK = "HK"
    EX = "EX"
    SK = "SK"
    JS = "JS"
    EV = "EV"
    RG = "RG"


class PersonaRegistryEntry(BaseModel):
    schema_version: Literal["cmf.persona_registry_entry.v1"]
    persona_registry_entry_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-[A-Z]{2}$")
    department_code: str = Field(min_length=3, max_length=3)
    service_code: str = Field(min_length=7, max_length=7)
    entity_type: EntityTypeCode
    display_name: str = Field(min_length=1)
    persona_name: str | None = None
    service_scope: str = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    active: bool

    @field_validator("service_code")
    @classmethod
    def service_code_is_exactly_seven(cls, value: str) -> str:
        if len(value) != 7:
            raise ValueError("service_code must be exactly seven characters")
        return value


class PersonaRegistryReceipt(BaseModel):
    schema_version: Literal["cmf.persona_registry_receipt.v1"]
    receipt_id: UUID
    entity_code: str
    decision_code: Literal["accepted", "rejected", "updated"]
    evidence_refs: list[str]
    failure_reasons: list[str] = []
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterPersonaCodeCommand`, `UpdatePersonaCodeCommand`, `ValidatePersonaCodeCommand`, `DeactivatePersonaCodeCommand` |
| Events | `PersonaCodeRegistered`, `PersonaCodeRejected`, `PersonaCodeUpdated`, `PersonaCodeDeactivated` |
| Workflow | `AgentFactoryWorkflow.persona_registry_validation` |
| Receipt | `PersonaRegistryReceipt` with code, decision, evidence refs, and failure reasons |

## 7. Backward Compatibility and Migration Fallback

Legacy names remain display or lineage fields only. Any existing agent/document name without a valid persona code must be migrated into a `PersonaRegistryEntry` before runtime activation. If no service-revealing seven-character code can be assigned, the entity remains reference-only.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Expressive personas vs. operational traceability | Display names may be expressive, but `entity_code` must reveal department, service, and type. | Registry validation rejects malformed or non-service codes. |
| Legacy names vs. CMF runtime contracts | Legacy names become lineage/display fields, not runtime authority. | Persona receipts link source refs and service scope. |
| Agent sprawl vs. readable Factory | Uniqueness and type validation prevent duplicate or vague roles. | List/read API exposes department and service grouping. |

## 9. Tasks

- Add persona registry contracts.
- Add department and entity type enums.
- Implement parser/validator.
- Seed canonical persona entries.
- Add repository and service methods.
- Add API read/validate endpoints.
- Add receipt writer.
- Add tests for valid/invalid codes and duplicate detection.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | All registered entities match `DDD-XXXXXXX-TT`. | `RES-VIS-AG` is accepted despite a short service code. |
| AC2 | Middle segment is exactly seven characters. | `RES-VISRCH-AG` passes with six characters. |
| AC3 | Type segment belongs to known entity types. | `RES-VISRSCH-XX` is accepted. |
| AC4 | Service code maps to a service-revealing role. | `RES-AUROREX-AG` is accepted without service scope. |
| AC5 | `RES-VISRSCH-AG` resolves to Visual Research Agent / Aurore. | Registry returns only a display name with no service scope. |

## 11. Dependencies

- TS-CMF-001 Command Spine.
- TS-CMF-002 Pipeline Stage Orchestration Records.
- TS-CMF-003 Spec Governance.
- Agent Factory docs and PRD-CMF-10.

## 12. Testing Strategy

Unit tests:

- Valid code parsing for all 63 seed codes.
- Invalid department length, service length, and entity type cases.
- Duplicate code and duplicate service collision tests.
- Receipt emission for accepted and rejected registrations.

Integration tests:

- API validates a new persona request and persists registry entry.
- AgentRoleSpec creation refuses unregistered persona code.
- Story/spec source refs can resolve a persona code.

Eval and recovery tests:

- RSCS signal-density test rejects purely poetic service codes.
- Recovery test deactivates an invalid seed while preserving history and receipt.

## 13. Observability, Recovery, and Rollback

- Metrics: persona registrations, rejections, duplicate attempts, active codes by type.
- Logs include `entity_code`, department, service, type, decision code, and receipt ID.
- Rollback deactivates registry entries; it does not delete prior receipts.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-062 |
| Story | 11.1 |
| Requirement Trace | PRD-CMF-10.00 |
| Pipeline Trace | agent-factory overlay, naming request to persona code registry |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No poetic-only codes, no malformed service codes, no unregistered runtime entity |
