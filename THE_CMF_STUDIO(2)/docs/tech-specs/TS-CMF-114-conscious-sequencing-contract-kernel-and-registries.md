---
tech_spec_id: "TS-CMF-114"
title: "Conscious Sequencing Contract Kernel and Registries"
story_id: "12.1"
story_title: "Conscious Sequencing Contract Kernel"
epic_id: 12
epic_title: "Conscious Sequencing and Expression Acquisition"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle"
pipeline_stage: "4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13"
entry_object: "Brand Context, Doctrine Bundle, Guest Dossier, Audience Reality Brief, Context Premises, Matrix of Edging, route intent"
exit_object: "Normalized sequencing registry snapshot, kernel contracts, registry receipt, generated schema adapters"
validation_contract: "registry normalization, role coverage, source-truth invariants, primitive binding, schema parity, receipt emission"
required_receipt: "SequencingRegistryNormalizationReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / Pi harness / FastAPI / TypeScript consumers"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-114: Conscious Sequencing Contract Kernel and Registries

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Local Phase 4 CBAR mandates for pipeline and rendering gates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Local Phase 5 CBAR mandates for verifiable artifact and package trust rules. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail. |
| `THE CMF STUDIO/docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` | Phase 5 adversarial audit trail. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` | Product owner for FR-CMF-12.01 and Epic 12 sequencing requirements. |
| `THE CMF STUDIO/docs/audits/CMF_CONSCIOUS_SEQUENCING_ENGINE_MCDA_SWOT_2026-06-25.md` | Accepts the sequencing bundle as canonical integration layer after normalization. |
| `THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/ccp_conscious_sequence_engine_v1/00_AGENT_START_HERE.md` | Mission, runtime authority, boot order, core law, and forbidden shortcuts. |
| `.../01_MASTER_SPEC.md` | Core architecture, ingredient system, Interview Brief V2, sequence patterns, adapters, package sequencing. |
| `.../02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Contracts, state machines, invariants, events. |
| `.../03_RUNTIME_WORKFLOWS.md` | Pre-interview, live, extraction, compilation, composition handoff, learning workflows. |
| `.../04_REGISTRIES_AND_FORMAT_ADAPTERS.md` | Five added registry families and format adapter principle. |
| `.../05_EVALUATION_GOVERNANCE_AND_LEARNING.md` | Readiness, coverage, inventory, sequence, ethical, and approval gates. |
| `.../models/sequence_engine_models.py` | Existing Pydantic model spine. |
| `.../registries/*.json` | Expression ingredient, acquisition instrument, pattern, adapter, and eval gate registries. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | JIT compiler and saturation context dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine and primitive test harness dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition lineage and source-timing dependency. |

## 2. Overview

This spec promotes the Conscious Sequencing bundle into the canonical CMF contract kernel. It does not replace Interview Asset Contracts, Complete Expression Sessions, Expression Moments, route selection, composition, rendering, or approval systems. It adds the missing sequencing and procurement layer that tells CMF what expression ingredients must be acquired, how they are tracked, and how approved ingredients later become viewer-state content programs.

The kernel owns three separate sequencing scales:

| Sequence Scale | Runtime Responsibility | Must Not Be Confused With |
|---|---|---|
| Interview-state sequence | Guides the guest through safety, memory, vulnerability, authority, teaching, humor, and invitation. | Final asset order. |
| Viewer-state sequence | Guides the audience through perceptual entry, relevant open question, active prediction, truthful payoff, human affinity, and future value. | Interview question order. |
| Package/series sequence | Orders multiple assets to build recognition, trust, category ownership, participation, and future expectation. | One clip or one carousel. |

The non-negotiable law is that a final sequence may only use captured, approved, sourced, retrieved, or explicitly requested ingredients. The compiler may not fabricate missing human truth to complete a content recipe.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-114-001 | `InterviewBriefV2` | Must become the procurement-plan upgrade to Conscious Interview Brief. |
| DEP-CMF-114-002 | `SequenceHypothesis` | Must describe provisional viewer-state recipes before the interview. |
| DEP-CMF-114-003 | `ExpressionAcquisitionPlan` | Must dedupe required ingredients and bind acquisition instruments. |
| DEP-CMF-114-004 | `InterviewAssetContractV2` | Must extend the existing Interview Asset Contract without bypassing it. |
| DEP-CMF-114-005 | `LiveIngredientCoverageState` | Must attach to Complete Expression Session events. |
| DEP-CMF-114-006 | `ExpressionIngredientInventory` | Must store source-grounded approved expression ingredients after extraction. |
| DEP-CMF-114-007 | `ContentSequenceProgram` | Must become the viewer-state program handed to composition and rendering. |
| DEP-CMF-114-008 | `PackageSequenceProgram` | Must order multiple approved assets for relationship-level progression. |
| DEP-CMF-114-009 | `SequenceEvaluationReceipt` | Must wrap or emit standard CMF evaluation receipts and approval blockers. |
| DEP-CMF-114-010 | `SequenceRegistryItem` | Canonical normalized registry row for one role, pattern, adapter, instrument, or gate. |
| DEP-CMF-114-011 | `SequenceRegistrySnapshot` | Immutable active registry snapshot consumed by child specs. |
| DEP-CMF-114-012 | `SequencingRegistryNormalizationReceipt` | Receipt proving registry normalization, validation, approval, and activation. |

### Registry Families

| Registry | Bundle Source | CMF Canonical Role |
|---|---|---|
| Expression Ingredient Registry | `expression_ingredient_registry_v1.json` | Declares roles like `clean_first_line`, `sensory_scene`, `disturbance`, `hidden_mechanism`, `usable_next_step`, `proof_object`, and `next_question`. |
| Acquisition Instrument Registry | `acquisition_instrument_registry_v1.json` | Declares question and follow-up instruments used to procure ingredient roles. |
| Sequence Pattern Registry | `sequence_pattern_registry_v1.json` | Declares viewer-state and information-release grammars. |
| Format Sequence Adapter Registry | `format_sequence_adapters_v1.json` | Maps semantic sequence beats into temporal/spatial behavior for videos, carousels, and single images. |
| Sequence Eval Gate Registry | `sequence_eval_gates_v1.json` | Declares procurement, sequence, package, and doctrine gates. |

### Required Normalization

Every registry item must be normalized into the CMF registry contract:

```text
id
version
status
description
required_inputs
compatible_archetypes
compatible_formats
rules
anti_patterns
evaluation_hooks
examples
source_bundle_ref
registry_sha256
```

Registry IDs are immutable. Any behavior change creates a new version, not an in-place mutation.

### Existing Backend Integration

| Python Owner | Database Table(s) | API Route(s) | Migration / Backfill Behavior |
|---|---|---|---|
| `src/ccp_studio/contracts/conscious_sequencing.py` | n/a | n/a | New Pydantic contract module. No data backfill. |
| `src/ccp_studio/services/conscious_sequencing_registry_service.py` | `sequencing_registry_snapshots`, `sequencing_registry_items` | `POST /api/cmf/sequencing/registries/normalize`, `GET /api/cmf/sequencing/registries/active` | New migration creates versioned registry tables; bundle JSON imported as snapshot `v1`. |
| `src/ccp_studio/services/conscious_sequencing_contract_kernel.py` | `sequencing_kernel_events`, `approval_blockers` | `POST /api/cmf/sequencing/registries/{snapshot_id}/validate` | New migration creates kernel event table keyed by registry snapshot and brand context. |
| `src/ccp_studio/services/registry_service.py` | `sequencing_registry_snapshots`, `sequencing_registry_items` | `POST /api/cmf/sequencing/registries/{snapshot_id}/activate` | Extends existing registry owner; does not replace current primitive or eval registries. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | `receipt_chain`, `evaluation_receipts`, `approval_blockers` | shared receipt writer | Adds receipt adapter for `SequencingRegistryNormalizationReceipt`. |
| `src/ccp_studio/api/main.py` | n/a | all `/api/cmf/sequencing/*` routes | Registers routes through existing FastAPI app. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-PER-003` | Phase4-M01 and Phase1-M06 | Registry activation must be review-gated and operator-visible before production use. |
| `EXP-TRS-004` | Phase4-M02 and Phase5-M03 | Format adapters must preserve cinematic meaning and reject bland/corporate visual collapse. |
| `EXP-FBK-001` | Phase4-M05 | Registry and gate rejection messages must name exact failing item IDs and repair actions. |
| `EXP-SOC-001` | Phase5-M01 | Activated registry snapshots and receipts must be verifiable artifacts, not informal notes. |
| `EXP-PRG-001` | Phase4-M03 and Phase5-M04 | Registry resolution for runtime consumers must be inline and deterministic. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Registry activation requires operator review of validation failures and source hashes before activation. |
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Format adapters must declare visual grammar constraints and cannot activate if they remove meaning-preservation hooks. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Validation failures return exact registry ID, item ID, missing field, and repair path. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Active snapshots and normalization receipts include hashes and receipt-chain rows. |

### Receipt Chain Guard

| Receipt | Table | Action | Idempotency Key | Required Hashes |
|---|---|---|---|---|
| `SequencingRegistryNormalizationReceipt` | `receipt_chain` | `sequencing.registry_snapshot.activated` | `snapshot_id + snapshot_sha256` | registry snapshot hash, source bundle hash, normalized item hashes |

### Doctrine and Primitive Binding

The kernel must bind every sequencing object to:

| Obligation | Runtime Check |
|---|---|
| Doctrine bundle | Every brief, inventory, program, and package stores `doctrine_bundle_id`. |
| Brand Context | Every object stores immutable `brand_context_version_id`. |
| Primitive triad | Every composition-bearing sequence beat must prove at least meaning, delivery, and format/material primitive roles. |
| Source law | Human expression ingredients require source segment, external source, approved brand memory, pickup, or non-human contextual type. |
| Approval law | Registry normalization and kernel objects require receipt-backed operator review before production use. |

### Gate Thresholds

| Gate ID | Threshold | Hard Fail | Consequence |
|---|---:|---|---|
| `registry_schema_valid` | 1.00 | Yes | Registry snapshot cannot load. |
| `registry_role_coverage` | 1.00 | Yes | Patterns/adapters referencing undefined roles are blocked. |
| `registry_eval_hook_coverage` | 0.95 | Yes | Gate registry cannot become active. |
| `source_law_invariant` | 1.00 | Yes | Sequence compiler and composition handoff blocked. |
| `primitive_binding_ready` | 0.90 | Yes | Composition-bearing programs blocked. |
| `schema_parity_python_ts` | 1.00 | Yes | TypeScript consumers cannot promote generated contracts. |

### Gate Verdict Semantics

| Verdict | Rule | Receipt Behavior |
|---|---|---|
| `PASS` | Score meets threshold and no hard blocker exists. | Write evaluation receipt and allow next state. |
| `PROVISIONAL` | Non-hard gate is within 0.08 below threshold. | Write evaluation receipt, require operator review before activation. |
| `FAIL` | Score misses threshold or validation is incomplete. | Write approval blocker with actionable rejection fields. |
| `BLOCKED` | Source law, schema parity, or role coverage hard gate fails. | Stop activation and require revised registry snapshot. |

## 4. Implementation Plan

1. Add `src/ccp_studio/contracts/conscious_sequencing.py` with canonical Pydantic models and wrappers for bundle schemas.
2. Add `src/ccp_studio/services/conscious_sequencing_registry_service.py` to load and normalize all five registry families.
3. Add `src/ccp_studio/services/conscious_sequencing_contract_kernel.py` for invariant checks, ID policy, state-machine guards, and receipt emission.
4. Add migration adapters from bundle examples and schemas to CMF IDs, timestamps, receipt refs, and brand/guest workspace scoping.
5. Add registry validation for missing role references, missing eval hooks, invalid format adapters, undefined primitive obligations, and duplicate IDs.
6. Add generated TypeScript contracts for PWA, Telegram, composition, and renderer consumers.
7. Add read models for registry snapshots, role definitions, sequence patterns, adapter compatibility, and eval gate profiles.
8. Emit `SequencingRegistryNormalizationReceipt` for every registry load, migration, and activation.
9. Add approval blockers for undefined roles, unscoped IDs, unsupported format targets, missing doctrine binding, and schema parity failure.
10. Add regression fixtures using bundle examples and current CMF doctrine/primitive eval fixtures.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class SequenceRegistryItem(BaseModel):
    schema_version: Literal["cmf.sequence_registry_item.v1"]
    registry_id: str
    item_id: str
    version: str
    status: Literal["draft", "active", "deprecated", "blocked"]
    description: str
    required_inputs: list[str] = Field(default_factory=list)
    compatible_archetypes: list[str] = Field(default_factory=list)
    compatible_formats: list[str] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)
    evaluation_hooks: list[str] = Field(default_factory=list)
    examples: list[dict] = Field(default_factory=list)
    source_bundle_ref: str
    registry_sha256: str


class SequenceRegistrySnapshot(BaseModel):
    schema_version: Literal["cmf.sequence_registry_snapshot.v1"]
    snapshot_id: str
    activated_at: str
    expression_ingredient_registry_version: str
    acquisition_instrument_registry_version: str
    sequence_pattern_registry_version: str
    format_sequence_adapter_registry_version: str
    sequence_eval_gate_registry_version: str
    item_count: int
    snapshot_sha256: str


class SequencingRegistryNormalizationReceipt(BaseModel):
    schema_version: Literal["cmf.sequencing_registry_normalization_receipt.v1"]
    receipt_id: str
    snapshot_id: str
    source_bundle_path: str
    normalized_registry_refs: list[str]
    undefined_role_refs: list[str] = Field(default_factory=list)
    schema_parity_passed: bool
    primitive_binding_passed: bool
    activated_by_operator_id: str | None = None
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. State Machine and Invariants

```text
bundle_imported
-> registry_normalized
-> schema_validated
-> role_coverage_validated
-> primitive_bound
-> operator_review
-> active
-> superseded
```

Hard invariants:

- Undefined roles cannot be referenced by sequence patterns or format adapters.
- Eval gates must map to CMF `EvaluationReceipt` and approval blocker semantics.
- Format adapters may change spatial/temporal behavior, but may not remove required payoff obligations.
- TypeScript contracts are consumers only; Python/Pydantic remains semantic source of truth.
- Registry snapshots are immutable after activation.

## 7. API, Service, and Event Contracts

| Contract | Shape |
|---|---|
| `POST /api/cmf/sequencing/registries/normalize` | Creates a draft normalized snapshot from bundle or registry source. |
| `POST /api/cmf/sequencing/registries/{snapshot_id}/validate` | Runs schema, role, eval, primitive, and parity checks. |
| `POST /api/cmf/sequencing/registries/{snapshot_id}/activate` | Operator activation; emits receipt. |
| `GET /api/cmf/sequencing/registries/active` | Returns active registry snapshot and version refs. |
| `GET /api/cmf/sequencing/adapters/{format_target}` | Returns compatible patterns, roles, and composition functions. |

Events:

```text
SequencingRegistryImported
SequencingRegistryNormalized
SequencingRegistryValidationFailed
SequencingRegistryActivated
SequencingRegistrySuperseded
```

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate / Test Evidence |
|---|---|---|---|
| AC1 | The five bundle registries load into normalized CMF registry snapshots with DEP-CMF-114-010 through DEP-CMF-114-012 assigned. | A pattern item loads without a version or normalized hash and is still marked active. | Phase5-M01, `EXP-SOC-001`; registry fixture test must fail activation. |
| AC2 | Registry activation is blocked when a pattern or adapter references an undefined role. | `sequence_pattern_registry_v1.json` references `meaning_landing` while no role registry item exists, and activation still succeeds. | Phase4-M05, `EXP-FBK-001`; blocker must name exact missing role and registry item. |
| AC3 | Every active registry item has status, version, required inputs, compatible formats, rules, anti-patterns, eval hooks, examples, source ref, and hash. | An adapter is active with no anti-patterns or evaluation hook. | Phase4-M01, `EXP-PER-003`; schema validation test. |
| AC4 | Source-truth invariants block any sequence path that would fabricate missing human expression. | A downstream sequence compiler fills a missing guest quote with synthetic text to close a loop. | Phase5-M01, `EXP-SOC-001`; source-law invariant test. |
| AC5 | Registry activation emits `SequencingRegistryNormalizationReceipt` into `receipt_chain`. | Snapshot is visible in PWA but no receipt-chain row exists for `sequencing.registry_snapshot.activated`. | Phase5-M01, `EXP-SOC-001`; receipt persistence test. |
| AC6 | TypeScript, PWA, Telegram, and render consumers may read active registries but cannot mutate semantic registry state. | A PWA adapter edits a registry item without creating a new snapshot. | Phase4-M01, `EXP-PER-003`; API authorization test. |

## 9. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Registry fixtures | All bundle registry JSON files load, normalize, and hash deterministically. |
| Missing-role negative tests | Undefined roles in sequence patterns or adapters produce approval blockers. |
| Schema parity tests | Pydantic and generated TypeScript contracts agree on required fields and enums. |
| Invariant tests | Source law blocks fabricated guest truth and synthetic claims. |
| Primitive tests | Composition-bearing adapters require at least three primitive roles. |
| Receipt tests | Activation produces immutable receipt with hashes and operator state. |

## 10. Doctrine-Driven Test Harness Binding

The test harness must execute:

```text
registry_schema_valid
registry_role_coverage
registry_eval_hook_coverage
source_law_invariant
primitive_binding_ready
schema_parity_python_ts
```

Every failure must create an actionable approval blocker with the exact registry ID, item ID, version, and repair recommendation.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Extends existing CMF backend rather than greenfield replacement | Pass |
| Preserves Python/Pydantic runtime authority | Pass |
| Separates interview-state, viewer-state, and package-state sequencing | Pass |
| Requires source-truth and no-fabricated-human-meaning invariant | Pass |
| Requires doctrine, primitive, eval, and approval receipts | Pass |
| Keeps renderers and TypeScript consumers downstream of frozen contracts | Pass |
