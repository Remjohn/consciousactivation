---
tech_spec_id: "TS-CMF-017"
title: "Intentional Orchestration Migration Contracts"
story_id: "3.6"
story_title: "Intentional Orchestration Migration Contracts"
epic_id: 3
epic_title: "Legacy Intelligence and JIT Skill Governance"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-3-6-intentional-orchestration-migration-contracts.md"
fr_ids:
  - "FR-CMF-03.09"
pipeline_stage: "0"
entry_object: "orchestration-bearing module"
exit_object: "LegacyOrchestrationIntentRecord"
validation_contract: "organism layer and proof obligations"
required_receipt: "orchestration intent receipt"
runtime_target: "Python / Pydantic v2 / migration workflow / registry and spec governance"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-017: Intentional Orchestration Migration Contracts

**Status:** Ready for Development  
**Story:** `3.6 - Intentional Orchestration Migration Contracts`  
**Implementation Boundary:** Legacy orchestration intent records, organism-layer classification, input/output packet references, gates, downstream consumers, failure modes, proof obligations, and downstream inheritance.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for CRAL/SCRE, Context Premise, Emotional DNA, Voice DNA, Matrix of Edging, SVRE/Aurore, scene intelligence, and JIT compilers as intentional orchestration. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-03.09 source authority. |
| `docs/architecture.md` | Architecture authority for the organism model and `LegacyOrchestrationIntentRecord`. |
| `docs/cmf-studio-pipeline-map.md` | Stage 0 migration trace and downstream pipeline inheritance. |
| `docs/migration/legacy-inventory.md` | Legacy source families and migration ledger context. |
| `docs/stories/story-3-6-intentional-orchestration-migration-contracts.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-013-migration-ledger-inventory-and-hashing.md` | Ledger dependency. |
| `docs/tech-specs/TS-CMF-014-registry-conversion-fixtures-and-evals.md` | Registry activation dependency. |
| `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | JIT skill dependency. |

## 2. Overview

### Problem Statement

The most valuable legacy modules are not only assets or prompts. They encode intentional order: why a signal is researched, induced, extracted, routed, rendered, validated, learned from, or rejected. If migration records reduce CRAL, Context Premise, Emotional DNA, Voice DNA, primitive coalitions, SVRE, scene containers, creative subsystems, or asset roles to style advice, CMF loses the reason those modules existed.

### Solution

Implement `LegacyOrchestrationIntentRecord` for every orchestration-bearing module. The record must preserve product purpose, organism layer, upstream inputs, emitted packets, downstream consumers, gates, failure modes, source documents, proof obligations, reviewer status, and inheritance rules for downstream stories/specs.

### Scope

In scope:

- Organism layer enum: DNA/truth, RNA/contextual transcription, force, delivery, variation, phenotype, evaluation, outer learning.
- Intent records for orchestration-bearing modules.
- Source citation and typed contract/registry target requirement.
- Authority overlap resolution.
- Downstream inheritance of gates by stories and tech specs.

Out of scope:

- Full implementation of CRAL, SVRE, scene intelligence, or brand genesis algorithms.
- Runtime execution of migrated modules.
- Visual UI for migration review.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-03.09 | System preserves intentional orchestration rationale for migrated CCF/CMF modules: purpose, organism layer, inputs, emitted packets, gates, downstream consumers, failures, and proof. | `LegacyOrchestrationIntentRecord`, organism layer validation, source citation requirement, authority overlap review, and orchestration intent receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `0 - Legacy inventory and migration` |
| Entry Object | Orchestration-bearing module |
| Exit Object | `LegacyOrchestrationIntentRecord` |
| Allowed Actors / Services | Migration Steward, Architecture Reviewer, Spec Governance Agent, RegistryService |
| Validation Contract | Organism layer and proof obligations |
| Required Receipt | Orchestration intent receipt |
| Forbidden Shortcut | Style-only summaries, vibe labels, prompt snippets, authority overlap without resolution, downstream spec reference without intent record |

### Legacy Intelligence Mapping

This spec exists because the user explicitly identified legacy modules as carrying intentional orchestration. The record preserves the "why" of PRD-02 CCF, PRD-03 CMF, PRD-08 Conscious Primitives, CCP Biological Orchestration Model, CSIP v3, CRAL, SVRE, CMF Master Scene Intelligence, scene containers, scene components, creative subsystems, and asset engines.

Target modules:

- `ccp_studio.contracts.legacy_orchestration`
- `ccp_studio.services.orchestration_intent_service`
- `ccp_studio.repositories.legacy_orchestration_intent_records`
- `ccp_studio.workflows.migration_workflow`
- `ccp_studio.services.spec_governance_service`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `LegacyOrchestrationIntentRecord` | Captures product purpose, organism layer, inputs, packets, consumers, gates, failures, proof, and reviewer status. |
| `OrganismLayer` | DNA/truth, RNA/contextual transcription, force, delivery, variation, phenotype, evaluation, outer learning. |
| `OrchestrationPacketRef` | Upstream input and emitted packet reference. |
| `GateRef` | Required validation gate inherited downstream. |
| `AuthorityOverlapReview` | Resolves overlapping module authority. |
| `OrchestrationIntentReceipt` | Approval receipt for downstream reference. |

## 4. Implementation Plan

### Workstream A: Intent Contracts

Define intent record, organism layer, packet refs, gate refs, failure modes, proof obligations, authority overlap review, and receipt contracts.

### Workstream B: Migration Workflow Gate

Require an intent record when a ledger entry is marked orchestration-bearing.

### Workstream C: Source and Target Validation

Require source document citations and typed target contract or registry target for modules claiming CRAL, Context Premise, Emotional DNA, Voice DNA, primitive coalitions, SVRE, scene containers, creative subsystems, or asset roles.

### Workstream D: Authority Overlap Review

When two modules claim overlapping authority, require reviewer resolution of organism layer and downstream boundary.

### Workstream E: Downstream Inheritance

Expose intent records to stories and tech specs so downstream docs can inherit gates and proof obligations.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class OrganismLayer(str, Enum):
    dna_truth = "dna_truth"
    rna_contextual_transcription = "rna_contextual_transcription"
    force = "force"
    delivery = "delivery"
    variation = "variation"
    phenotype = "phenotype"
    evaluation = "evaluation"
    outer_learning = "outer_learning"


class OrchestrationPacketRef(BaseModel):
    schema_version: Literal["cmf.orchestration_packet_ref.v1"]
    packet_name: str
    packet_contract: str
    required: bool = True


class LegacyOrchestrationIntentRecord(BaseModel):
    schema_version: Literal["cmf.legacy_orchestration_intent_record.v1"]
    legacy_orchestration_intent_record_id: UUID
    migration_ledger_entry_id: UUID
    product_purpose: str
    organism_layer: OrganismLayer
    upstream_inputs: list[OrchestrationPacketRef]
    emitted_packets: list[OrchestrationPacketRef]
    downstream_consumers: list[str]
    required_gates: list[str]
    failure_modes: list[str]
    proof_obligations: list[str]
    source_document_refs: list[str]
    typed_contract_or_registry_target: str
    reviewer_actor_id: UUID
    approved_at: datetime | None = None


class AuthorityOverlapReview(BaseModel):
    schema_version: Literal["cmf.authority_overlap_review.v1"]
    authority_overlap_review_id: UUID
    intent_record_ids: list[UUID]
    resolved_layer_assignments: dict[str, OrganismLayer]
    reviewer_actor_id: UUID
    decision: str
    decided_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `CreateOrchestrationIntentRecordCommand`, `ValidateOrchestrationIntentCommand`, `ResolveAuthorityOverlapCommand`, `ApproveOrchestrationIntentCommand`, `InheritOrchestrationGatesCommand` |
| Events | `OrchestrationIntentRecordCreated`, `OrchestrationIntentBlocked`, `AuthorityOverlapResolved`, `OrchestrationIntentApproved`, `OrchestrationGatesInherited` |
| Workflows | Orchestration intent migration workflow, authority overlap workflow, downstream inheritance workflow |
| Receipts | `OrchestrationIntentReceipt`, `AuthorityOverlapReceipt`, `SpecAuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Orchestration-bearing modules without intent records remain source doctrine and cannot activate production registries, JIT compilers, or downstream gates. Style-only summaries are blocked.

Fallback behavior:

- Missing purpose returns `ORCHESTRATION_PURPOSE_REQUIRED`.
- Missing organism layer returns `ORGANISM_LAYER_REQUIRED`.
- Missing packet refs returns `ORCHESTRATION_PACKETS_REQUIRED`.
- Missing source document returns `SOURCE_DOCUMENT_REQUIRED`.
- Style-only summary returns `ORCHESTRATION_INTENT_FLATTENED`.
- Authority overlap returns `AUTHORITY_OVERLAP_REVIEW_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Migration wants compact summaries; CMF value depends on preserving causal order and proof obligations. |
| UX / Ops Failure Scenario | CRAL or scene intelligence is reduced to a prompt label, so downstream agents invoke it without source discipline, gates, or downstream proof. |
| Resolution Demand | Intent record authority takes precedence. Orchestration-bearing modules cannot activate or be cited downstream until their role, gates, packets, failures, and proof are explicit. |
| Downstream Proof | Tests must block style-only summaries, require source citations and typed targets, resolve overlaps, and allow downstream specs to inherit gates from intent records. |

## 9. Tasks

- Define orchestration intent contracts.
- Add persistence for intent records and authority reviews.
- Integrate with MigrationWorkflow.
- Implement source/target validation.
- Implement authority overlap workflow.
- Implement downstream gate inheritance.
- Add tests for style-only blocking and overlap resolution.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Migrated orchestration module record includes purpose, organism layer, inputs, packets, consumers, gates, failures, and proof. | Record says "used for better storytelling." |
| AC2 | CRAL/Context/Emotional DNA/Voice DNA/SVRE/scene modules cite source doc and typed target. | CRAL listed as "research vibe" with no contract. |
| AC3 | Style advice or prompt snippet summary blocks activation. | Prompt snippet activates as compiler guidance. |
| AC4 | Overlapping module authority is resolved into organism layers. | Two modules both own final evaluation authority. |
| AC5 | Downstream story/spec can cite intent record and inherit gates. | Spec references SVRE without proof obligations. |

## 11. Dependencies

Internal:

- TS-CMF-013 Migration ledger
- TS-CMF-014 Registry conversion
- TS-CMF-015 JIT skill compiler
- TS-CMF-016 Greenfield gates
- TS-CMF-003 Spec workflow

External:

- Pydantic v2
- PostgreSQL
- Spec governance/eval runner

## 12. Testing Strategy

Unit tests:

- Organism layer validation.
- Required packet/gate/proof fields.
- Style-only summary rejection.
- Authority overlap schema.

Integration tests:

- Create intent record for CRAL-like module.
- Block missing typed target.
- Resolve overlap.
- Approve intent and inherit gates into spec audit.

Safety tests:

- Downstream specs cannot cite orchestration-bearing module without intent record.
- Migration activation blocks missing proof obligations.
- Authority overlap blocks activation until resolved.

## 13. Observability, Recovery, and Rollback

- Logs include `legacy_orchestration_intent_record_id`, `migration_ledger_entry_id`, `organism_layer`, reviewer, and status.
- Metrics track intent records created, blocked, approved, overlap reviews, and downstream inheritances.
- Recovery rebuilds intent index from ledger and receipts.
- Rollback deprecates intent record with receipt and blocks downstream activation until replacement is approved.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-03.09 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Intentional orchestration preserved as first-class migration record |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python contracts, Pi inherits gates through orchestration records |
| TypeScript Boundary | No orchestration authority in UI |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

