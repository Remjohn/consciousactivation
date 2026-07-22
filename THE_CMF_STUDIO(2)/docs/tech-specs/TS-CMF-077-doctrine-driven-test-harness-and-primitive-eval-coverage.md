---
tech_spec_id: "TS-CMF-077"
title: "Doctrine-Driven Test Harness and Primitive Eval Coverage"
story_id: "qa-1"
story_title: "Doctrine-Driven Test Harness and Primitive Eval Coverage"
epic_id: "quality"
epic_title: "Doctrine, Primitive, Eval, and Approval Quality Spine"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved testing spine after TS-CMF-076"
fr_ids:
  - "FR-CMF-09.01"
  - "FR-CMF-09.02"
  - "FR-CMF-09.03"
  - "FR-CMF-10.05"
pipeline_stage: "cross-stage quality governance"
entry_object: "spec, contract, command, workflow, render, UI, registry, or adapter target"
exit_object: "DoctrineTestRunReceipt and approval blocker state"
validation_contract: "doctrine invariants, primitive obligations, evidence pointers, negative fixtures, receipt chain"
required_receipt: "DoctrineTestRunReceipt"
runtime_target: "Python / pytest / DSPy evals / registry evals / generated read models / UI test runner"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-077: Doctrine-Driven Test Harness and Primitive Eval Coverage

**Status:** Ready for Development  
**Implementation Boundary:** A testing spine that turns CMF internal doctrine, primitives, registries, gate packs, and workflow invariants into executable tests, evaluation receipts, and approval blockers.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md` | Existing EvaluationReceipt and doctrine eval foundation. |
| `docs/evals/07-eval-registry-and-workbench-architecture.md` | Eval registry and workbench structure. |
| `registries/evals/doctrine/cmf_interview_brief_doctrine_eval.v1.json` | Interview Brief doctrine eval source. |
| `registries/evals/doctrine/cmf_brand_genesis_doctrine_eval.v1.json` | Brand Genesis doctrine eval source. |
| `registries/evals/doctrine/cmf_64_state_acting_library_doctrine_eval.v1.json` | Acting library doctrine eval source. |
| `registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json` | PaperCut rig doctrine eval source. |
| `registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Canonical composition primitive triad source for route-specific visual gates. |
| `registries/primitives/**` | Primitive registry source for executable primitive obligations. |
| `docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Legacy audit lens discipline. |
| `docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Legacy revision discipline. |
| `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md` | Signal distillation quality filter and anti-shallow-output discipline. |

## 2. Overview

CMF testing must prove that implementation respects the depth of the documented system. Random unit tests are not enough. The test harness must translate internal doctrine into executable invariants:

```text
documented principle
-> operational invariant
-> required evidence
-> fixture or negative fixture
-> evaluator
-> receipt
-> approval blocker when failed
```

Every important production object must be testable against the doctrine it claims to implement. A test that only proves code executes is insufficient when the product object carries interview-first, Context Premise, Matrix of Edging, primitive, scene-template, Brand Genesis, PaperCut, or evaluation obligations.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.01 | Generate evidence-backed evaluation receipts. | Doctrine test receipts extend evaluation receipts for specs, code, and production objects. |
| FR-CMF-09.02 | Review surfaces must expose evidence and blockers. | Test receipts produce review-readable blocker state. |
| FR-CMF-09.03 | Approval must be blocked by hard failures. | Failed doctrine tests emit approval blockers. |
| FR-CMF-10.05 | Agent/runtime tools must be governed by standards and evals. | Agent, tool, hook, skill, extension, and adapter specs bind to doctrine tests. |

## 4. Test Taxonomy

| Test Class | Purpose | Example |
|---|---|---|
| Contract Tests | Prove Pydantic/JSON/TypeScript contracts include required fields and states. | `CompositionTemplateJson` requires zones, binding, hash, eval obligations. |
| Doctrine Eval Tests | Prove output respects documented doctrine. | Interview Brief passes CCP V9/V9.1 and Context Premise requirements. |
| Primitive Obligation Tests | Prove required primitives are declared, evidenced, and scored. | Scene output cites exact primitive IDs and passes VSG/NEG/MOT checks. |
| Composition Primitive Minimum Tests | Prove composition objects carry at least three validated primitives before build, preview, render, or approval. | `VisualFeelContract` for a Paper-Cut Explainer validates meaning, delivery, and material primitives before preview generation. |
| Legacy Fixture Tests | Prove migrated old CMF/CCF intelligence is actually used. | Reaction clip binds to scene-builder runtime template and effect stack. |
| Pipeline Trace Tests | Prove source lineage and receipt chain are complete. | Expression Moment to RenderOutput to ApprovalEvent is reconstructable. |
| Negative/Drift Tests | Prove forbidden shortcuts are blocked. | Rendering without approved composition JSON fails. |
| Visual/Render Tests | Prove composition, captions, faces, timing, and background removal are valid. | Caption does not cover guest face or selected option. |
| UI Governance Tests | Prove operator cannot approve blind or cross-guest. | Approval disabled without blocker-free receipt set. |
| Adapter Boundary Tests | Prove open-source tools cannot own domain truth. | React video editor cannot replace canonical composition JSON. |

## 5. Primary Contracts

```python
class DoctrineInvariant(BaseModel):
    invariant_id: str
    source_doc_refs: list[str]
    applies_to_object_types: list[str]
    statement: str
    required_evidence_types: list[str]
    hard_failure_codes: list[str]


class PrimitiveObligation(BaseModel):
    primitive_id: str
    target_object_type: str
    required_when: str
    evidence_requirement: str
    evaluator_ref: str


class DoctrineTestTarget(BaseModel):
    target_type: str
    target_id: str
    spec_id: str | None = None
    pipeline_stage: str | None = None
    lineage_refs: list[str]
    object_hash: str | None = None


class DoctrineTestRunReceipt(BaseModel):
    schema_version: Literal["cmf.doctrine_test_run_receipt.v1"]
    doctrine_test_run_receipt_id: str
    target: DoctrineTestTarget
    invariant_results: list[dict[str, Any]]
    primitive_results: list[dict[str, Any]]
    negative_fixture_results: list[dict[str, Any]]
    evidence_refs: list[str]
    hard_failures: list[str]
    approval_blocker_codes: list[str]
    decision: Literal["pass", "needs_revision", "blocked"]
    created_at: str
```

## 6. Doctrine Source Registry

The harness must load doctrine sources from a versioned registry. Initial source families:

| Source Family | Purpose |
|---|---|
| CCP V9 / V9.1 | Interview-first expression engine and routeability doctrine. |
| Product Brief | Full-system north star and stage expectations. |
| Brand Genesis V3 | Brand context, micro-semiotic, 64-state, PaperCut rig requirements. |
| Creative Pipeline V2 | SceneSpec, composition, layer, renderer, and animation doctrine. |
| Legacy Scene Builder Runtime | Containers, components, scene templates, effects, cognitive load, attention mode. |
| Primitive Registry | Exact primitive IDs and quality standards. |
| SDA/SFL/Failure Corpora | Negative fixtures and semantic/perceptual failure tests. |
| MCDA Audits | Documentation repair criteria and quality scorecards. |

## 7. Required Invariant Families

| Family | Examples |
|---|---|
| Interview-First | Monthly Interview Brief is first artifact unless using existing interview transcript/video fallback. |
| Evidence Spine | Every claim, route, render, memory, and approval object keeps source refs. |
| Primitive Fidelity | Primitive references use exact registry IDs and evidence, not fuzzy names. |
| Composition Primitive Triad | Every composition, prompt, JSON template, generated keyframe, renderer template, and approval preview validates at least three primitives covering meaning, delivery, and format/material roles. |
| Context Premise | Audience conversation, comments, and cultural resonance appear before question compilation. |
| Matrix of Edging | Interview questions preserve tension, risk, and specificity instead of safe generic prompts. |
| Scene Intelligence | Reaction templates bind to scene-builder runtime before composition approval. |
| Composition JSON | JSON is canonical; previews and renderer props derive from it. |
| Brand Genesis | Brand context, 64-state acting library, PaperCut rig, and micro-semiotics are lock-gated. |
| Approval Governance | Evaluators cannot approve; hard failures create blockers. |
| Workspace Isolation | Brand and guest scope cannot leak across UI, storage, workers, or memory. |
| Adapter Sovereignty | Open-source integrations require adapter decision receipts before production use. |

## 8. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterDoctrineInvariantCommand`, `RunDoctrineTestSuiteCommand`, `RunPrimitiveObligationEvalCommand`, `RecordDoctrineTestReceiptCommand`, `EmitApprovalBlockerFromDoctrineTestCommand` |
| Events | `DoctrineInvariantRegistered`, `DoctrineTestSuiteStarted`, `DoctrineTestReceiptRecorded`, `ApprovalBlockedFromDoctrineTest` |
| Workflow | Cross-stage quality workflow before build, before approval, before render, and before adapter import |
| Receipt | `DoctrineTestRunReceipt` |

## 9. Test Runner Modes

| Mode | Use |
|---|---|
| `spec_audit` | Runs against tech specs before implementation. |
| `contract_ci` | Runs against Pydantic and generated TypeScript contracts. |
| `workflow_ci` | Runs against command bus and pipeline workflow fixtures. |
| `render_ci` | Runs against composition JSON, previews, frames, captions, and outputs. |
| `ui_ci` | Runs against operator workbench, blockers, scope, and commands. |
| `adapter_ci` | Runs against open-source adapter candidates and approved adapters. |
| `approval_gate` | Runs before human approval can be enabled. |

## 10. Audit and Revision Policy

Every spec must include either:

1. a specific doctrine-driven test harness binding, or
2. an explicit reason why the spec has no doctrine/primitive/eval obligations beyond baseline contract tests.

Conditional spec revision is required when a spec:

- has a testing section with only generic unit/integration tests;
- touches interview, research, primitives, scene, brand, render, UI, agent, memory, adapter, approval, or publishing behavior;
- names legacy inventory without a fixture/eval path;
- references primitives without exact registry/evidence testing;
- emits receipts without receipt-chain tests;
- allows approval or render progression without blocker tests.

## 11. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast implementation vs internal depth | Every major object carries doctrine/primitive test obligations. | DoctrineTestRunReceipt links target, invariants, evidence, and blockers. |
| Unit tests vs meaning preservation | Tests include doctrine, primitive, negative fixture, and pipeline trace layers. | CI output reports invariant and primitive result sets. |
| Evaluator authority vs human approval | Test failures can block approval, but tests cannot approve alone. | Approval still requires review command and approval receipt. |

## 12. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Each spec declares doctrine-driven test obligations or an explicit baseline-only rationale. | A rendering spec only says "add unit tests." |
| AC2 | Doctrine tests emit receipts with target, evidence, hard failures, and blocker codes. | Test report has pass/fail text with no receipt. |
| AC3 | Primitive obligations reference exact registry IDs or registered primitive family refs. | Test says "voice feels authentic" with no primitive ref. |
| AC4 | Composition targets cannot pass with fewer than three validated primitive obligations. | Paper-Cut preview is generated after only declaring "Analogy Bridge". |
| AC5 | Composition primitive obligations cover meaning, delivery, and format/material roles. | Three persuasion primitives pass, but no PaperCut material primitive is validated. |
| AC6 | Negative fixtures exist for documented forbidden shortcuts. | Renderer accepts unapproved composition JSON. |
| AC7 | UI approval is disabled when doctrine test blockers exist. | Operator approves object with failed doctrine receipt. |

## 13. Composition Primitive Minimum Invariant

Composition-bearing objects have a stricter primitive floor than ordinary implementation objects because they are the visible phenotype of CMF intelligence.

The canonical route-specific source is:

```text
registries/evals/composition/cmf_composition_primitive_triads.v1.json
```

Applies to:

- `VisualFeelContract`;
- `SceneSpec`;
- `CompositionPlan`;
- composition JSON templates;
- Ideogram `CompositionJob`;
- preview keyframes;
- Remotion / Motion Canvas renderer templates;
- Operator approval previews.

The invariant is:

```text
No composition-bearing object may advance unless at least three primitive validations pass.
```

The three required roles are:

| Role | Required purpose |
|---|---|
| `meaning_transform` | Proves the selected source pressure, Matrix primitive, analogy, contrast, story, or recognition trigger survived. |
| `delivery_shape` | Proves the pressure is delivered through the right audience experience, emotional pacing, teaching structure, or interaction pattern. |
| `format_material` | Proves the route-specific visual/material language is obeyed, such as PaperCut materiality, reaction UI/human proof, or cinematic documentary pacing. |

Hard-failure blocker codes:

```text
COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET
COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING
COMPOSITION_PRIMITIVE_EVIDENCE_MISSING
COMPOSITION_PRIMITIVE_SCORE_BELOW_THRESHOLD
```

Negative fixtures must include:

- one primitive only;
- two primitives only;
- three primitives with missing evidence;
- three primitives all in the same role;
- three vague labels with no exact primitive IDs or approved family refs;
- route material primitive missing, such as PaperCut without paper materiality validation.

## 14. Dependencies

- TS-CMF-001 command spine.
- TS-CMF-014 registry conversion fixtures and evals.
- TS-CMF-050 evaluation receipt generation.
- TS-CMF-053 approval blockers.
- TS-CMF-067 agent readiness evals.
- TS-CMF-075 operator composition and template approval workbench.

## 15. Testing Strategy

Unit tests:

- Doctrine invariant schema validation.
- Primitive obligation schema validation.
- Doctrine test target hashing and lineage validation.
- Receipt immutability and blocker code validation.

Integration tests:

- Spec audit mode over all tech specs.
- Contract CI over representative Pydantic models.
- Workflow CI proving receipt-chain and hard-failure blocker emission.
- Render CI proving composition JSON, scene binding, preview hash, and output hash linkage.
- UI CI proving blocker-aware approval actions.

Eval and fixture tests:

- Positive and negative fixtures for Interview Brief, Brand Genesis, 64-state acting library, PaperCut rig, reaction clip scene binding, composition JSON, and open-source adapter decisions.
- Golden audit report fixture for a deliberately shallow spec.

## 16. Observability, Recovery, and Rollback

- Metrics: doctrine tests run, invariant failures, primitive failures, negative fixture failures, approval blockers emitted, spec audit defects, and stale doctrine source versions.
- Logs include target ID, target type, spec ID, doctrine source version, invariant ID, primitive ID, evidence refs, and blocker code.
- Recovery reruns doctrine tests when target hash or doctrine source version changes.
- Rollback supersedes receipts but does not delete failed doctrine-test history.

## 17. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-077 |
| Requirement Trace | FR-CMF-09.01, FR-CMF-09.02, FR-CMF-09.03, FR-CMF-10.05 |
| Pipeline Trace | Cross-stage quality governance |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No random-only testing, no doctrine-free approval, no primitive-free evals, no receipt-free quality reports |
