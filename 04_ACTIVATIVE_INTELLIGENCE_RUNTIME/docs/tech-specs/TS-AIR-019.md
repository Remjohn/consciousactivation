---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-019
title: Failure Attribution, Selective Repair, and JIT Role Capsules
product: Activative Intelligence Runtime
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 12
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
  - AIR-FR-109
  - AIR-FR-111
  - FR-098
controlling_stories:
  - AIR-ST-19.01
  - AIR-ST-19.02
  - ST-10.01
upstream_draft_dependencies:
  - spec_id: TS-AIR-001
    edge_id: SDE-050
    dependency_class: AUTHORITY_DEPENDENCY
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-005
    edge_id: SDE-051
    dependency_class: WRITE_INTERFACE_DEPENDENCY
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-017
    edge_id: SDE-052
    dependency_class: WRITE_INTERFACE_DEPENDENCY
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-019 - Failure Attribution, Selective Repair, and JIT Role Capsules

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`. This document does not ratify that package, authorize implementation, create contract or schema release bytes, issue a Development Capsule, make a product production-eligible, or grant certification.

`TS-AIR-001`, `TS-AIR-005`, and `TS-AIR-017` are exact hash-pinned upstream drafts in `WRITTEN_PENDING_AUDIT`. Each is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their public interfaces are admitted only for dependency-safe specification writing and are not represented as accepted or current authority.

## 1. Files and authorities read

### 1.1 Workflow, authority, packet, and ownership inputs

| Class | Exact path | State / bytes / SHA-256 | Specific use |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten-section structure, evidence law, draft-dependency labels, and claim ceiling. |
| Recovery writer packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery authorized; 316,012; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-AIR-019-RECOVERY` freezes the output path, three FRs, three Stories, and three upstream edges. |
| Wave dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_12_DISPATCH_LOCK.yaml` | `DISPATCHED`; 2,678; `96f655bbf67a40a38a5cf233cfa9ad3f954466a8dae80ff68dfa87a2a5c9e5a7` | Freezes the exact admitted upstream draft bytes. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending; 1,221; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Writing and later technical review are allowed; build and capsules are prohibited. |
| Specification-work authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification only; 1,462; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Source of the pre-ratification writing authority and quality ceiling. |
| Dependency classification | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | current; 107,141; `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | SDE-050 is an authority dependency; SDE-051 and SDE-052 are write-interface dependencies. |
| Path authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | current; 18,768; `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | This exact target is a `DIRECT_PRODUCT_SPEC_PATH`; no nearer `AGENTS.md` applies. |
| Highest current authority | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; 40,830; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Current constitutional precedence, semantic lineage, wrong-reading locks, and product boundary law. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION`; 1,288; `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Confirms the candidate is not current authority. |
| Candidate Constitution | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`; 51,243; `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate AIR lifecycle, epistemic, repair, replay, and human-authority constraints. |
| Product authority matrix | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification; 4,289; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic programs; Pipeline owns runtime execution, JIT state, receipts, evaluation control, and selective-repair execution without semantic reinterpretation. |
| Semantic ownership matrix | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification; 4,263; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Pipeline owns runtime execution state and selective-repair plan; AIR retains semantic lifecycle and program meaning. |
| Canonical ledgers | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv`; `CANONICAL_FR_LEDGER.csv`; `FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen; `acb0bd4b...`, `bb631307...`, `5c3a8dda...` | Fix this spec's identity, owning FRs, Stories, gate, traceability, and claim ceiling. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | current; 134,201; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | The three feature sources are `REQUIRED_UNIQUE_EVIDENCE`, byte-available, and hash-locked. |
| Source-package instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | current bundle instructions; 1,911; `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Models, tools, Pipeline, renderers, and external products may not become semantic authority. |

### 1.2 Controlling feature, Stories, sources, contracts, and Primitives

| Class / ID | Exact path | Bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| F19 feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F19-failure-attribution-selective-repair-and-jit-role-capsules.md` | 40,492; `74322093f712dbf11c76403d05cd0538a622a89104776e333afc126347a74e53` | Attribute before repair, preserve valid upstream objects, use explicit bounded roles, and prove exact replay. |
| AIR Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-19.01 and AIR-ST-19.02 entry, terminal, adversarial, CBAR, supersession, and evidence requirements. |
| AHP Story | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-10.01 requires complete episode capture, causal attribution, ambiguity preservation, replay, and selective recovery. |
| Donor full draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-019-failure-attribution-selective-repair-and-jit-role-capsules.md` | 28,579; `2dbd25575606f15176e04c555a2b8c745f859710b38d8edfd83eafd88ae067e4` | Structural baseline; corrected here for current packet identity, ownership, strict interfaces, repository behavior, and V3.3 evidence. |
| `SRC-AI2-REPAIR-001` | `.../sources/ai_v2_predecessor/contracts/11_FAILURE_ATTRIBUTION_AND_REPAIR_PROGRAM.md` | 274; `b25670847d79678eb0d269656afe38cd45d0a9244b47d5051dea931379ec2ae7` | Failure object/layer, cause evidence, frozen upstream refs, exact change target, affected descendants, invalidation graph, rerun plan, evaluation, and ambiguous-human escalation. |
| `SRC-AHP-F16-001` | `.../sources/doctrine/AHP_F16_EVALUATION_REPAIR.md` | 18,469; `0a247a2025ef803df09e8bfc97b9456d73a64cf2f867598135b3c8ba03a668e2` | Deterministic facts precede independent judgment; producer cannot approve itself; repair changes declared units only; human-owned conflicts escalate. |
| `SRC-AHP-F03-001` | `.../sources/doctrine/AHP_F03_BOUNDED_ROLE_TAXONOMY.md` | 17,889; `1d50940d7313b89331e872b63393276267e698cb5908254479e216a234f3ec77` | Actor, capability owner, role, and product are independent; Pipeline owns node scheduling, handoffs, JIT state, and immutable execution receipts. |
| Predecessor failure schema | `.../contracts/schemas/failure_attribution.schema.json` | 2,111; `b0f14dc46cc7e51e15d3d6c5587dc928e4177843a36df62aa2b39fe66ce521d0` | Useful frozen-ref seed; free strings and missing ownership/epistemic fields require adaptation. |
| Predecessor repair schema | `.../contracts/schemas/repair_program.schema.json` | 1,925; `759a0497482ccf839f1707a3da936491256ed6fae893cfb4fd81a28c129f172d` | Useful bounded-target/evaluation/stop seed; permitted changes, preserved properties, authority, and escalation require strengthening. |
| Predecessor JIT schema/example | `.../contracts/schemas/jit_context_capsule.schema.json`; `.../examples/23_jit_context_capsule.json` | 2,282 / 1,570; `0644912e...` / `3181972f...` | Role-specific object refs, allowed/forbidden actions, output/evaluation refs; open rendered context and runtime ownership require correction. |
| `EXP-FBK-001` | `.../sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | 6,981; `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Feedback must explain the specific consequence and next action; no vanity score or disruptive spam. |
| `PRM-BUS-006` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-006.yaml` | 6,533; `6abfae7c921e5768d459ceeb57b073ba9ba2865ad03e907bcb3361a72b391133` | Repair must preserve semantic priority and prevent arbitrary emphasis or inverted hierarchy. |
| `PRM-VSG-001` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | 5,040; `568cd44028280d169316748ee58268e76ea3222423339eb6990b344268234698` | Visual repair evidence must preserve intended eye path without forcing visual doctrine onto nonvisual artifacts. |

The `...` prefix above abbreviates only the repeated AIR bundle root shown in full in preceding rows. Complete paths are preserved in the files-read receipt.

### 1.3 Admitted upstream draft interfaces and revision impact

| Edge | Exact draft | Frozen state / bytes / SHA-256 | Interface consumed | Sections reopened by hash or accepted-interface change |
|---|---|---|---|---|
| SDE-050 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `WRITTEN_PENDING_AUDIT`; 31,425; `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Authority/actor refs, field epistemic assertions, semantic object versions, immutable history, typed blockers, canonical serialization, atomic command/receipt behavior, and descendant-only invalidation law. | Governing decisions; architecture/workflows; models/contracts/APIs; failure/migration/rollback/recovery/observability; acceptance; testing/evidence. |
| SDE-051 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-005.md` | `WRITTEN_PENDING_AUDIT`; 44,990; `5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact Primitive bindings, coalition/Edge Product lineage, semantic constraint preservation, Steering Recipe identity, evaluation, and selective invalidation boundaries. | Governing decisions; architecture/workflows; models/contracts/APIs; failure/migration/rollback/recovery/observability; acceptance; testing/evidence. |
| SDE-052 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md` | `WRITTEN_PENDING_AUDIT`; 67,346; `0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Visual semantic/narrative/Composition Intent/Feature Contract identity, visual reparse evidence, wrong-reading locks, result observation, and AIR/Pipeline/VAE repair boundaries. | Governing decisions; architecture/workflows; models/contracts/APIs; failure/migration/rollback/recovery/observability; acceptance; testing/evidence. |

These dependencies are read-only. This spec does not copy their objects into local forks. Any change to a frozen hash, quality state, owner, field meaning, or consumed public interface reopens every listed impact area before this spec can advance.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem and user outcome

“Rewrite the prompt” is not a failure model. A polished output can fail because its source authority is absent, an inferred field was treated as observed, the Matrix or Primitive coalition was wrong, retrieval admitted irrelevant evidence, a Programmed Model exceeded its claim, a renderer violated Composition Intent, an evaluator used the wrong profile, or a human-owned decision was missing. Treating all of these as one prompt defect destroys valid work, hides responsibility, weakens learning evidence, and transfers authority to whichever runtime happens to retry.

The operator needs a deterministic, inspectable answer to five questions before repair:

1. Which exact object version failed, and what evidence establishes the failure?
2. Which authoritative layer owns the suspected defect, including contested or multi-causal cases?
3. Which upstream objects remain valid and frozen?
4. What semantic change is permitted, what must survive, and when must the system stop or escalate?
5. Which product executes the repair, which role receives what minimum context, and what evidence proves that unrelated work was not regenerated?

The outcome is a versioned AIR `FailureAttribution` and, when AIR-owned semantic repair is lawful, a bounded `SemanticRepairProgram`. Pipeline consumes these objects as constraints, computes its own exact dependency/invalidation and execution plans, assembles role-specific JIT runtime capsules, executes approved work, and emits receipts. Neither execution convenience nor role naming gives Pipeline semantic authority.

### 2.2 Bounded solution

AIR provides strict contracts and services to:

- admit exact failure signals, source/semantic objects, evaluation receipts, operator commands, and execution/production observations;
- distinguish symptom from supported root cause and represent `ATTRIBUTED`, `MULTI_CAUSAL`, `CONTESTED`, and `UNRESOLVED` honestly;
- classify every candidate cause through a governed failure-layer registry rather than free text;
- preserve exact upstream semantic refs, field-level epistemic states, owner, lifecycle-at-use, wrong-reading locks, and limitations;
- compile a semantic repair boundary only when AIR owns the target meaning and the attribution permits mutation;
- emit a typed `RepairReferral` when the target belongs to Pipeline, VAE, Interview Expression, Delegation, Studio, an evaluator owner, Program Control, or attributable human authority;
- declare semantic minimum-context requirements for Hunter, Analyst, Composer, or Commander work while leaving runtime JIT capsule assembly, actor binding, scheduling, tools, and execution receipts to Pipeline;
- issue a `LearningAttributionDisposition` before an episode may enter any learning queue, without automatically promoting it;
- preserve immutable failed attempts, alternatives, decisions, repairs, and historical replay.

### 2.3 In scope

- `FailureSignal`, `FailureAttributionCandidate`, `FailureAttribution`, `SemanticRepairProgram`, `RepairReferral`, `RoleSemanticContextRequirement`, and `LearningAttributionDisposition` contracts;
- exact owner, authority, epistemic, lineage, lifecycle, evaluator, and lock checks;
- deterministic validation followed by independent judgment where causal interpretation is not mechanical;
- multi-causal, contested, ambiguous, stale, superseded, and insufficient-evidence outcomes;
- immutable persistence, optimistic concurrency, idempotency, atomic commit, cancellation, replay, supersession, and descendant-impact handoff;
- AIR-to-Pipeline, AIR-to-VAE, AIR-to-Interview-Expression, AIR-to-Studio, evaluator, and Program Control repair referrals;
- role-specific semantic context requirements and their conformance against Pipeline-owned JIT runtime capsules;
- scoped learning admission and rejection evidence required by FR-098;
- migration of eligible predecessor records as new immutable candidates, lossless or blocked.

### 2.4 Out of scope and non-goals

- computing Pipeline's authoritative runtime dependency traversal, invalidation set, checkpoint selection, rerun schedule, actor binding, tool grants, or `RuntimeSelectiveRepairPlan`;
- executing Workflow Nodes, model calls, retrieval, renders, edits, provider jobs, VAE repairs, or Studio commands;
- letting AIR mutate VAE production state, Pipeline execution state, Interview Expression evidence, Program Control authority, or human-owned source/identity values;
- treating a role name, model, evaluator, UI, Studio projection, transport envelope, or provider as product or semantic authority;
- deriving source classification, observed reaction, missing human approval, policy exception, or semantic meaning from probability or convenience;
- updating a Steering Recipe, Skill, Programmed Model, evaluator rule, Identity/Voice/Visual DNA, Primitive, archetype, or global weight directly from one episode;
- manufacturing a generic creative-safety or content-rights approval authority. Operator-supplied source authority, provenance, lineage, approvals, and product sovereignty remain explicit; technical security remains operational;
- implementation, code, generated schemas, release bytes, Development Capsules, product adoption, production, publication, or certification.

## 3. Governing decisions and constraints

### 3.1 Product and object ownership

| Concern or object | Authoritative owner | Consumer or executor | Prohibition |
|---|---|---|---|
| Semantic failure taxonomy and attribution over AIR meaning | Activative Intelligence Runtime | Pipeline, Studio, Independent Evaluation, owning product | Pipeline, evaluator, and Studio may supply evidence but may not rewrite the attributed semantic meaning. |
| Source admission, live reaction evidence, Reaction Receipts, Expression Moments | Interview Expression / attributable source authority | AIR | AIR may detect a gap and refer it; it may not reconstruct or amend live-source truth. |
| `SemanticRepairProgram` for AIR-owned object fields | Activative Intelligence Runtime under the controlling human/semantic authority | Pipeline executes the approved program | Pipeline cannot broaden permitted fields, relax preservation constraints, or create new meaning. |
| Runtime dependency graph, `RuntimeInvalidationPlan`, checkpoints, rerun nodes, and `RuntimeSelectiveRepairPlan` | Atomic Harness Pipeline | AIR and Studio receive receipts | AIR supplies semantic constraints; it does not fabricate runtime reachability or execution state. |
| Runtime `JITContextCapsule`, actor binding, node-local tools, scheduling, execution, and `RoleExecutionReceipt` | Atomic Harness Pipeline | bounded role actor | AIR declares required semantic refs and forbidden semantic mutations; it does not schedule or execute the role. |
| VAE candidate generation, production diagnosis/repair, production acceptance, lineage, and delivery | Visual Asset Editor | Pipeline | AIR may attribute an upstream semantic mismatch or refer a production issue; it may not select providers or perform production repair. |
| Deterministic and calibrated judgment receipts | Independent Evaluation owner for the bound profile | AIR/Pipeline/VAE | Evaluation evidence does not own the object being evaluated or its repair. Producer cannot approve itself. |
| Human-owned new meaning, identity/source authority, unresolved taste, policy exception, and promotion | Attributable human authority | Studio captures typed commands/evidence | No automated service may synthesize or silently default the decision. |
| Typed transport, routing, compatibility, retries, and transport receipts | Delegation Protocol | all products | Delegation transports and enforces envelopes without interpreting cause or meaning. |
| Cross-product authority, issue, release, and claim truth | Program Control | all products | A local status or issue record cannot redefine Program Control authority. |

`Activative Contract Compiler != Activative Intelligence Runtime`. Builder declares requirements and dependencies in an `AtomicHarnessDefinition`; it does not perform AIR semantic attribution. Pipeline executing a repair does not become the owner of semantic repair meaning. AIR attributing an execution or production defect does not become the owner of that product's local state.

### 3.2 Attribution laws

1. Attribution precedes mutation, invalidation, rerun, learning admission, or promotion.
2. A failed evaluation is evidence of a symptom until the causal layer and evidence are established. Evaluator disagreement cannot be relabeled as a target-product defect without evidence.
3. `UNRESOLVED` is a valid terminal attribution state for the current attempt. The system must not guess to obtain a repairable label.
4. More than one cause may be material. `MULTI_CAUSAL` preserves ordered causal relations and cannot be flattened to one convenient owner.
5. A contested attribution preserves each candidate, its evidence, excluded alternatives, evaluator identities, and the authority needed to resolve it.
6. Failure language names an object, assertion, transition, contract, binding, or evidence gap; it does not diagnose or blame a person.
7. A confidence value, if supplied by a bound profile, is evidence only. This spec invents no universal threshold. The profile version and decision rule must be hash-pinned.
8. Unknown failure-layer, owner, schema, profile, role, lifecycle, or epistemic values fail closed.
9. Parsing without behavioral enforcement fails. A consumer that preserves fields but ignores owner, mutation boundary, or escalation law is incompatible.

### 3.3 Semantic repair laws

- A repair may begin only from an immutable `FailureAttribution` whose status and owner permit that repair class.
- AIR may compile an authoritative `SemanticRepairProgram` only for AIR-owned semantic fields and only under the actual value/approval owner. For non-AIR objects, AIR emits a `RepairReferral` plus preservation constraints; the owning product decides and records its local repair.
- Every repair program identifies one target version, permitted JSON Pointers or typed field selectors, forbidden selectors, preserved-property assertions, frozen upstream refs, required evidence, evaluator profile, stopping law, and escalation route.
- Absence from `permitted_change_set` means forbidden. Descendants are not permitted mutation targets merely because they will be invalidated or rerun.
- A repair cannot remove, weaken, or omit inherited wrong-reading locks. Relaxation requires a new authorized upstream semantic object version.
- Valid source lineage, Matrix, Primitive coalition, Edge Product, psychological role/tension, archetype, Identity/Voice/Visual DNA, Final Script, Activation Transfer, Composition Intent, Feature Contract, and lock relationships remain exact unless the repair explicitly targets an AIR-owned member and carries the required authority.
- Human-owned new meaning, unresolved taste, source/identity approval, policy exception, and promotion cannot be placed in an automated permitted-change set.
- Successful repair creates a new immutable object version. The failed and prior versions remain replayable.

### 3.4 Role and JIT capsule laws

`hunter`, `analyst`, `composer`, and `commander` are workflow roles, not personas, product owners, or authority classes. Every execution separately records actor identity/type, capability owner, workflow role, product boundary, task, input refs, output schema, evaluation profile, allowed/forbidden actions, tool grants, and handoff.

AIR owns the semantic context requirements for an AIR semantic task: which source/Matrix/coalition/role/archetype/DNA/script/transfer/visual/lock refs are required, what meaning must survive, which facts remain epistemically unresolved, and which semantic mutations are forbidden. Pipeline owns construction and delivery of the exact runtime `JITContextCapsule`, context-budget enforcement, retrieval, node-local tool grants, actor binding, expiry, scheduling, and execution receipt.

Minimum Complete Context means sufficient and no broader than necessary. It never means copying the unrestricted case record into every role:

| Role | Required semantic purpose | Typical admitted context | Forbidden authority inference |
|---|---|---|---|
| Hunter | discover missing or conflicting evidence without deciding canonical meaning | failure signal, exact search question, admissible source classes, source gaps, known exclusions, output schema | may not approve source truth, change meaning, or select repair authority |
| Analyst | compare evidence, contradictions, causal candidates, and excluded alternatives | immutable refs, evaluator findings, epistemic assertions, dependency evidence, candidate causes | may not mutate the target, choose production strategy, or resolve human-owned ambiguity |
| Composer | propose a bounded change from approved ingredients and constraints | attributed cause, permitted/forbidden field sets, frozen refs, preserved properties, lock set, evaluation contract | may not expand scope, weaken locks, invent source meaning, or self-accept |
| Commander | select an admissible next transition within existing authority | candidates, receipts, owner matrix, gates, stopping law, escalation route, resource envelope | may not ratify authority, grant build/production, override a human gate, or reinterpret semantics |

### 3.5 Epistemic, lineage, feedback, and claim constraints

- `planned`, `observed`, `inferred`, `operator_confirmed`, `rejected`, and `superseded` remain field-level states under the TS-AIR-001 draft interface. A high score cannot turn inference into observation.
- Failure evidence cites immutable source, object, span/locator, transformation, evaluation, execution, and human-decision refs. Generic notes cannot replace required lineage.
- A result explains why the attribution matters, what state changed or did not change, the responsible owner, and the next admissible action. It does not emit arbitrary progress points or interrupt a protected live-recording context.
- Visual repair preserves the TS-AIR-017 semantic hierarchy and intended reading path. `PRM-VSG-001` is applied only when a visual artifact or visual-semantic relation is in scope; audio-only or nonvisual artifacts carry an evidenced `NOT_APPLICABLE` decision rather than a fake visual test.
- This spec finishes at `WRITTEN_PENDING_AUDIT`. Candidate authority is not current, build authority is false, production and certification are false, and the maximum later pre-ratification state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

## 4. Current brownfield architecture

### 4.1 Artifact disposition

| Artifact | Useful behavior | Disposition | Required correction |
|---|---|---|---|
| `contracts/schemas/failure_attribution.schema.json` | Closed top-level schema, immutable refs, frozen upstreams, affected descendants, rerun nodes, and escalation flag. | `ADAPT` | Replace free-string layer/cause with governed typed structures; add owner, authority, epistemic, lifecycle, candidates, alternatives, status, evaluator, limitations, and canonical identity. Separate AIR semantic attribution from Pipeline invalidation/rerun ownership. |
| `contracts/schemas/repair_program.schema.json` | Exact target, attribution ref, frozen refs, evaluation ref, descendants, rerun nodes, and stop condition. | `ADAPT` | Add typed permitted/forbidden changes, preserved assertions, value authority, applicability, escalation, issue/receipt refs, and a separate Pipeline execution-plan interface. |
| `contracts/schemas/jit_context_capsule.schema.json` | Role, task, immutable object refs, actions, output/evaluation refs, optional expiry. | `ADAPT` | Replace open `rendered_context` with typed entries and a context manifest; record actor/capability/product/authority separately; make Pipeline runtime ownership explicit. |
| `examples/23_jit_context_capsule.json` | Concrete minimal-context and forbidden-action example. | `REUSE_AS_TEST_EVIDENCE` | Preserve as a migration fixture only; it cannot prove current schema conformance or grant live-source authority. |
| `SRC-AI2-REPAIR-001` | Compact required repair evidence list. | `REUSE_AS_CONTRACT_SEED` | Split semantic attribution/repair meaning from Pipeline dependency and execution plans. |
| Donor `TS-AIR-019` | Ten-part planning baseline and broad failure categories. | `SUPERSEDE_WITH_CURRENT_SPEC` | Correct the overbroad six-FR claim to the packet's three FRs, correct object ownership, close schemas, specify exact runtime boundaries, and add FR-098 learning admission. |
| Historical prompt-rewrite or retry patterns | May show prior operational attempts. | `ARCHIVE_AS_HISTORICAL` | Never promote an untyped prompt, latest-model output, or broad retry into an authoritative repair. |

The predecessor schemas are evidence, not released V2.1 contract bytes. No schema in the source bundle is modified by this writing task.

### 4.2 Brownfield defects this specification must prevent

1. `responsible_layer: string` accepts misspellings, aliases, and invented owners.
2. `root_cause: string` cannot distinguish observed fact, inferred cause, human confirmation, rejected alternative, or unresolved status.
3. Embedding `invalidated_descendant_refs` and `rerun_nodes` inside AIR attribution can falsely make AIR the owner of Pipeline graph truth.
4. A boolean human-escalation field cannot identify the exact decision owner, reason, deadline/expiry if any, or next lawful command.
5. Free-form required-change and stop-condition strings cannot prove bounded mutation or deterministic enforcement.
6. An open rendered-context map permits omitted lineage, accidental secrets, mutable defaults, nondeterministic ordering, and context fields with no authority classification.
7. Role labels without actor/capability/product/authority fields become hidden autonomous agents.
8. A retry can overwrite the failed path or replay against latest state instead of the original versions.
9. One production episode can be placed in a learning queue without causal attribution or can be generalized beyond its evidence.

### 4.3 Compatibility rule

V2.1 implementations may read eligible predecessor records only through a versioned adapter. The adapter preserves exact source bytes and known refs, maps only explicit values, marks missing fields `UNAVAILABLE_FROM_PREDECESSOR`, and either emits a new immutable candidate plus migration receipt or blocks. It cannot infer source classification, epistemic state, owner, causal layer, preserved property, role authority, human decision, wrong-reading lock, or learning scope.

## 5. Proposed architecture and workflows

### 5.1 Logical components and authority

| Component | Product / responsibility | Must not do |
|---|---|---|
| `FailureIntakeService` | AIR; normalize exact signals and refs without causal closure. | Treat evaluator failure, exception type, or operator rejection as proven root cause. |
| `FailureLayerRegistry` | AIR contract surface; resolve governed layer IDs and owning products. | Use free-text aliases or mutate Program Control ownership. |
| `FailureAttributionService` | AIR; validate candidates, evidence, epistemic state, alternatives, and compile immutable attribution. | Mutate target objects, execute repair, self-evaluate, or guess ambiguity. |
| `SemanticRepairProgramService` | AIR; compile bounded repair meaning for eligible AIR-owned fields under exact authority. | Traverse Pipeline runtime state, schedule nodes, choose tools/models/providers, or repair another product's canonical object. |
| `RepairReferralPort` | AIR outbound port; deliver attribution and preservation constraints to the actual owner. | Represent referral acceptance as repair completion. |
| `RoleSemanticContextRequirementService` | AIR; declare exact semantic refs, limitations, epistemic gaps, must-survive constraints, and forbidden semantic actions. | Build runtime context, retrieve arbitrary documents, bind actors/tools, or execute a role. |
| `PipelineRepairPort` | Typed adapter to Pipeline-owned invalidation, JIT, execution, evaluation-control, and receipt interfaces. | Import Pipeline internals or reinterpret a Pipeline receipt as semantic authority. |
| `LearningAttributionService` | AIR; classify episode learning opportunity and evidence scope before queue admission. | Promote a recipe/model/rule/profile or update live weights. |
| `FailureRepairRepository` | AIR; atomic immutable append of AIR objects/events/edges/commands/receipts/idempotency records. | Store Pipeline execution state as AIR state or rewrite history. |
| `FailureRepairEvaluator` | Independent identity; evaluate causal adequacy, owner fit, semantic preservation, and boundedness. | Produce the object it evaluates or authorize another product's repair. |
| Studio projection/command adapter | Read projections and capture attributable human resolution commands. | Write canonical AIR state directly or hide a human decision in UI state. |

### 5.2 End-to-end state machine

| State | Required entry evidence | Allowed next state | Persisted evidence |
|---|---|---|---|
| `SIGNAL_RECORDED` | Exact failed/result object, signal type, source/evaluator/operator/exception evidence, lifecycle-at-observation. | `ATTRIBUTION_OPEN`, `SIGNAL_REJECTED` | `FailureSignal` and intake receipt. |
| `ATTRIBUTION_OPEN` | Current refs resolve; owner/lifecycle/epistemic gates pass. | `ATTRIBUTED`, `MULTI_CAUSAL`, `CONTESTED`, `UNRESOLVED` | Candidate set, evidence, excluded alternatives, deterministic gates, evaluator request. |
| `ATTRIBUTED` | One supported primary cause and owner; independent receipt where judgment is used. | `REPAIR_PROGRAMMED`, `REFERRED`, `NO_REPAIR_REQUIRED` | Immutable `FailureAttribution`. |
| `MULTI_CAUSAL` | Multiple supported causes with typed relation/order and owners. | `REPAIR_PROGRAMMED`, `REFERRED`, `HUMAN_RESOLUTION_REQUIRED` | Attribution plus separable repair/referral branches. |
| `CONTESTED` | Conflicting supported candidates or evaluator/owner dispute. | `HUMAN_RESOLUTION_REQUIRED`, `ATTRIBUTION_OPEN`, `CLOSED_UNRESOLVED` | All candidates, disagreements, required authority. |
| `UNRESOLVED` | Evidence cannot lawfully choose a cause. | `ATTRIBUTION_OPEN`, `HUMAN_RESOLUTION_REQUIRED`, `CLOSED_UNRESOLVED` | Missing evidence, attempted analyses, prohibited guesses, next action. |
| `REPAIR_PROGRAMMED` | AIR-owned target, valid attribution, exact mutation authority, complete bounded program. | Pipeline/local executor acceptance or `REPAIR_REJECTED` | `SemanticRepairProgram` and independent boundedness receipt. |
| `REFERRED` | Target is owned outside AIR or requires human/Program Control decision. | Owner-local lifecycle only; AIR observes receipts. | `RepairReferral` and acknowledgement/refusal refs. |
| `REPAIR_EXECUTED_OBSERVED` | Exact owner execution receipt and result refs; no inference from transport success. | `REPAIR_EVALUATED`, `REPAIR_REJECTED` | Observation record; Pipeline/VAE state remains external. |
| `REPAIR_EVALUATED` | Deterministic checks and independent judgment for the exact result hash. | `CLOSED_REPAIRED`, `ATTRIBUTION_OPEN`, `HUMAN_RESOLUTION_REQUIRED` | Evaluation, preservation diff, invalidation/reuse evidence. |
| `CLOSED_REPAIRED` | New immutable target version, accepted owner receipt, replay equivalence, no unresolved hard gate. | Additive successor only. | Closure and learning-attribution disposition. |
| `CLOSED_UNRESOLVED` | No lawful repair available in current evidence/authority envelope. | New evidence opens a new attribution attempt. | Typed blocker; history remains intact. |

A state transition never implies product acceptance beyond the object explicitly named. In particular, transport acknowledgement is not owner acceptance; VAE production acceptance is not Pipeline consumption; Pipeline repair execution is not AIR semantic acceptance; AIR repair evaluation is not publication or production authorization.

### 5.3 Attribution workflow

1. **Record signal.** Validate the exact failed object/result, signal source, submitted actor, authority, event time, and payload hash. Unknown or stale refs produce a denial receipt only.
2. **Freeze observation context.** Freeze exact upstream semantic refs, execution/result refs, evaluator profiles/results, source spans, current lifecycle-at-use, and dependency snapshot refs. Do not copy mutable “latest” aliases.
3. **Enumerate governed candidates.** Candidate layers come only from the registry in section 6. Each candidate names owner, target ref, evidence for, evidence against, excluded alternatives, causal relation, epistemic state, and limitations.
4. **Run deterministic gates.** Verify schema, hashes, lifecycle, owner, allowed layer-target relation, source/epistemic claims, evaluator identity, wrong-reading lock inheritance, and required evidence. Deterministic failure cannot be overridden by a model score.
5. **Run independent causal evaluation where needed.** The evaluator receives the frozen candidate set, not an unrestricted prompt. Producer/evaluator identities must differ. Disagreement remains visible.
6. **Commit attribution atomically.** Store attribution, candidates, evidence edges, command record, event, evaluation refs, receipt, and idempotency record in one transaction.
7. **Choose lawful continuation.** AIR semantic target plus valid authority may enter semantic repair compilation. External target emits a referral. Ambiguous human-owned cases emit `HUMAN_RESOLUTION_REQUIRED`.

### 5.4 Semantic repair and Pipeline execution workflow

1. AIR compiles a `SemanticRepairProgram` only for an exact AIR-owned target field set and exact value/approval authority.
2. Deterministic boundedness validation proves that permitted selectors are nonempty, forbidden selectors do not overlap, every preserved assertion cites an immutable value/evidence ref, all inherited locks are present, and a stopping/escalation law is bound.
3. An independent evaluator verifies cause-to-change fit and that the program preserves valid semantic relationships. The producer cannot accept itself.
4. AIR publishes the immutable program to Pipeline through `PipelineRepairPort`. Publication does not mean acceptance or execution.
5. Pipeline validates its own Harness, graph, active versions, runtime compatibility, and repair authority. It computes `RuntimeInvalidationPlan`, `RuntimeSelectiveRepairPlan`, checkpoint reuse, rerun nodes, role execution graph, and JIT runtime capsules. Pipeline may reject an infeasible or stale program with a typed receipt; it may not broaden semantic scope.
6. Each role execution receives a Pipeline-owned `JITContextCapsule` conforming to AIR's semantic context requirements. A context manifest proves exact refs, hash, omissions, redactions, tool grants, output schema, evaluation profile, and expiry/cancellation state.
7. Pipeline executes and atomically records commands, node attempts, artifacts, dependency edges, invalidation projections, receipts, and outbox state. It returns exact result and execution refs.
8. AIR observes the result through an immutable adapter, verifies the exact semantic target/version and preservation evidence, and requests independent evaluation. VAE or other products separately evaluate their own local acceptance.
9. Failure, disagreement, exhausted stopping law, or a human boundary creates a new attempt/referral; no blind retry rewrites the prior attempt.

### 5.5 FR-098 learning attribution workflow

Before any production episode or correction enters a learning queue, `LearningAttributionService` must classify whether it evidences a source, knowledge artifact, retrieval, context assembly, Skill, Steering Recipe, Programmed Model, tool, runtime binding, Pipeline, VAE, evaluator, or human-policy opportunity. The disposition includes exact episode/result/repair refs, supported candidates, responsible-owner confidence evidence from the bound profile, excluded alternatives, ambiguity state, human-review requirement, applicability envelope, prohibited generalizations, and proposed queue destination.

Allowed disposition decisions are `ELIGIBLE_FOR_SCOPED_REVIEW`, `INSUFFICIENT_ATTRIBUTION`, `HUMAN_REVIEW_REQUIRED`, `DUPLICATE_EVIDENCE`, and `INELIGIBLE_FOR_LEARNING`. `ELIGIBLE_FOR_SCOPED_REVIEW` is not promotion. Promotion to a dataset, recipe, model, evaluator rule, Primitive, archetype, or DNA observation requires its separately owned lifecycle, comparisons, regression evidence, rollback, and attributable approval.

### 5.6 Concurrency, atomicity, replay, and cancellation

- Commands carry `command_id`, canonical `payload_sha256`, `expected_stream_version`, and exact prior object refs. Exact retry returns the original receipt. The same ID with different bytes fails `AIR_REPAIR_IDEMPOTENCY_CONFLICT`.
- The AIR transaction commits every new AIR object, event, edge, command record, receipt, idempotency record, projection mutation, and durable outbox item or none. External product state is never included in the AIR transaction; cross-product completion uses explicit saga receipts.
- Optimistic concurrency allows only one writer against the expected stream/object head. Losing commands produce conflict receipts and no artifacts.
- Cancellation before AIR commit records `CANCELLED_NO_COMMIT`. Cancellation after commit cannot erase state and returns the committed receipt. Pipeline/VAE cancellation follows those products' contracts and is observed by ref.
- Replay uses the historical object versions, contract/profile versions, context manifests, candidates, decisions, execution receipts, model/tool bindings, and human authority that were active at the time. It never substitutes current/latest refs or synthesizes unavailable authority.

## 6. Data models, contracts, schemas, and APIs

All proposed contracts are strict, immutable, and versioned. Unknown fields are rejected. Arrays preserve semantic order; set-semantics arrays are sorted and deduplicated by their declared canonical key before hashing. No field uses an untyped `Any`, an open extension map, a mutable default, or a free-string substitute for a governed enum/ref.

Canonical serialization is I-JSON UTF-8 with Unicode NFC, lexicographically sorted object keys, schema-declared array behavior, normalized RFC 3339 UTC timestamps ending in `Z`, no insignificant whitespace, and no NaN/Infinity. Semantic content hashes omit only the object's self hash and fields explicitly declared receipt-only; caller-supplied event time remains evidence in receipt identity. SHA-256 values are lowercase hexadecimal.

### 6.1 Shared strict types

| Type | Required fields / law |
|---|---|
| `ImmutableRef` | `object_id`, `version`, lowercase `sha256`, `owner_product_id`, `lifecycle_state_at_use`, `schema_id`, `schema_version`. Empty values, latest aliases, and owner mismatch fail. |
| `AuthorityRef` | `authority_id`, `authority_version`, `authority_sha256`, `authority_state: CURRENT | CANDIDATE_NOT_CURRENT`, `scope`. Candidate state remains visible. |
| `ActorRef` | `actor_id`, `actor_type: DETERMINISTIC_MODULE | MODEL_PROGRAM | AGENT_PROGRAM | HUMAN`, `product_id`, optional bounded `workflow_role`. Role never replaces actor/product. |
| `EvidenceRef` | immutable evidence ref plus `evidence_kind`, `locator`, `epistemic_state`, `supports_claim_ids`, and source/value authority where applicable. |
| `TypedBlocker` | `code`, `responsible_owner`, `failed_invariant`, nonempty `evidence_refs`, `next_admissible_action`, and optional `required_authority_ref`. |
| `FieldSelector` | validated JSON Pointer or registered typed selector bound to exact schema ID/version. Wildcards and parent-object shortcuts are prohibited. |
| `PreservedPropertyAssertion` | `selector`, `expected_value_sha256`, `evidence_refs`, `reason_code`, `wrong_reading_lock_refs`, `verification_method`. |
| `EvaluationProfileRef` | immutable profile ref, owner, claimed dimensions, applicability, and decision-rule ref. No default universal threshold. |

### 6.2 Governed failure-layer registry

`FailureLayerId` is a closed, versioned registry. At minimum the candidate registry contains:

| Family | Layer IDs | Default authority route |
|---|---|---|
| Source and human evidence | `SOURCE_AUTHORITY`, `SOURCE_EVIDENCE`, `SOURCE_CLASSIFICATION`, `REACTION_RECEIPT`, `EXPRESSION_MOMENT`, `OPERATOR_RESOLUTION`, `HUMAN_POLICY_AUTHORITY` | Interview Expression, source/value authority, Studio capture, or attributable human. |
| Epistemic and semantic lifecycle | `EPISTEMIC_STATE`, `CONTEXT_PREMISE`, `MATRIX_OF_EDGING`, `ACTIVATION_HYPOTHESIS`, `PRIMITIVE_BINDING`, `PRIMITIVE_COALITION`, `EDGE_PRODUCT`, `ARCHETYPE_COALITION`, `IDENTITY_DNA`, `VOICE_DNA`, `VISUAL_DNA`, `FINAL_SCRIPT`, `ACTIVATION_TRANSFER` | AIR under the exact value/approval owner. |
| Visual semantic program | `VISUAL_SEMANTIC_PACK`, `VISUAL_NARRATIVE_PROGRAM`, `COMPOSITION_INTENT`, `FEATURE_CONTRACT`, `WRONG_READING_LOCK` | AIR semantic owner; Pipeline/VAE evidence may trigger referral. |
| Knowledge and orchestration | `KNOWLEDGE_ARTIFACT`, `RETRIEVAL`, `CONTEXT_ASSEMBLY`, `SKILL`, `STEERING_RECIPE`, `PROGRAMMED_MODEL`, `WORKFLOW_NODE`, `ATOMIC_HARNESS_DEFINITION` | Exact registry/product owner; Pipeline for runtime state, Builder for Harness definition, AIR for AIR semantic recipes. |
| Execution and production | `RUNTIME_BINDING`, `TOOL`, `PIPELINE_EXECUTION`, `VISUAL_ASSET_DEMAND`, `VAE_PRODUCTION`, `DELEGATION_TRANSPORT` | Pipeline, VAE, or Delegation respectively. |
| Evaluation | `EVALUATOR_PROFILE`, `EVALUATOR_EXECUTION`, `EVALUATION_EVIDENCE` | Independent evaluator/profile owner. |
| Unresolved | `UNRESOLVED` | No repair mutation; route to evidence acquisition or attributable authority. |

Registry entries require `layer_id`, `registry_version`, `canonical_name`, `family`, `authoritative_owner_product`, `allowed_target_schema_ids`, `allowed_evidence_kinds`, `repair_route`, `human_escalation_conditions`, `supersedes`, and `content_sha256`. Adding or reassigning a layer is a governed registry version, not a local code constant.

### 6.3 `FailureSignal` - `ca.air.failure-signal/2.1.0-candidate`

Required fields are `signal_id`, `signal_version`, `failed_object_ref`, `observed_result_refs`, `signal_kind`, `submitted_by`, `authority_ref`, `observed_at_utc`, `evidence_refs`, `claimed_layer_ids`, `limitations`, `content_sha256`. `signal_kind` is `DETERMINISTIC_VALIDATION_FAILURE`, `INDEPENDENT_EVALUATION_FAILURE`, `OPERATOR_REJECTION`, `SOURCE_CONTRADICTION`, `SUPERSESSION`, `EXECUTION_FAILURE`, `PRODUCTION_FAILURE`, `CONSUMPTION_REJECTION`, or `POST_COMPLETION_INVALIDATION`.

A signal is not an attribution. `claimed_layer_ids` may be empty and may contain multiple registered candidates; it cannot authorize mutation.

### 6.4 `FailureAttributionCandidate` and `FailureAttribution`

`FailureAttributionCandidate` requires:

- `candidate_id`, `failure_layer_ref`, `suspected_target_ref`, `authoritative_owner_product_id`;
- `causal_relation: PRIMARY | CONTRIBUTING | DOWNSTREAM_SYMPTOM | EXCLUDED`;
- nonempty `evidence_for_refs`, `evidence_against_refs`, `alternative_candidate_refs`, and `exclusion_reason_refs` as applicable;
- `epistemic_state`, `evaluation_profile_ref`, optional profile-produced `confidence_measurement`, `limitations`, and `content_sha256`.

`FailureAttribution` - `ca.air.failure-attribution/2.1.0-candidate` - requires:

| Field | Type / rule |
|---|---|
| `attribution_id`, `version`, `content_sha256` | Stable identity and immutable version. |
| `signal_ref`, `failed_object_ref` | Exact signal and failed version. |
| `status` | `ATTRIBUTED | MULTI_CAUSAL | CONTESTED | UNRESOLVED`. |
| `candidate_refs` | Nonempty ordered candidate refs; all candidates preserved. |
| `primary_candidate_refs` | One for `ATTRIBUTED`, two or more for `MULTI_CAUSAL`, empty for `UNRESOLVED`; contested set is explicit. |
| `frozen_upstream_refs` | Exact valid upstream semantic refs; no latest aliases. |
| `observation_context_refs` | Execution/result/evaluation/dependency-snapshot refs active when signal was observed. |
| `root_cause_evidence_refs` | Nonempty for attributed states; direct or properly labeled inferred evidence. |
| `excluded_alternative_refs` | Evidence-backed exclusions; empty only when none can lawfully be excluded, with limitation. |
| `semantic_preservation_refs` | Source, Matrix, coalition, role/tension, archetype, DNA, script, transfer, visual intent, Feature Contract, and lock refs that remain valid/applicable. |
| `repair_route` | `AIR_SEMANTIC_REPAIR | OWNER_REFERRAL | HUMAN_RESOLUTION_REQUIRED | EVIDENCE_ACQUISITION_REQUIRED | NO_REPAIR_REQUIRED`. |
| `owner_product_id`, `authority_ref`, `produced_by` | Separate semantic owner, governing authority, and actual producer identity. |
| `deterministic_validation_receipt_ref`, `independent_evaluation_receipt_refs` | Judgment receipt is required when attribution is not mechanically decidable. |
| `lifecycle_state`, `supersedes_ref`, `created_at_utc`, `limitations` | Additive lifecycle and explicit limits. |

The AIR repository does not store Pipeline's computed invalidated descendants or rerun nodes as AIR-authored facts. It stores immutable refs to Pipeline `RuntimeInvalidationPlan` and execution receipts after they exist.

### 6.5 `SemanticRepairProgram` and `RepairReferral`

`SemanticRepairProgram` - `ca.air.semantic-repair-program/2.1.0-candidate` - requires:

- `repair_program_id`, `version`, `failure_attribution_ref`, `target_object_ref`, `target_schema_ref`;
- `semantic_owner_product_id: ActivativeIntelligenceRuntime`, exact `value_authority_ref`, `requested_by`, and `approved_transition`;
- nonempty `permitted_change_set`; nonempty `forbidden_change_set`; nonempty `preserved_property_assertions`;
- `frozen_upstream_refs`, `required_source_evidence_refs`, `inherited_wrong_reading_lock_refs`, and `required_output_schema_ref`;
- `required_evaluation_profile_ref`, `deterministic_postcondition_refs`, `independent_judgment_dimension_refs`;
- `stopping_law` containing an exact attempt/resource envelope ref, terminal success conditions, terminal failure conditions, and no-progress rule. The envelope is supplied by authority/configuration; this spec invents no number;
- `escalation_route` containing blocker class, responsible owner, required evidence/authority, and next admissible command;
- `pipeline_execution_constraints` containing allowed node capability classes, required checkpoint preservation, forbidden semantic reinterpretation, and required receipt types, but no runtime node IDs or provider choices;
- lifecycle, evaluation, supersession, limitations, and content hash.

The program cannot target an external-owner object. `RepairReferral` is used instead and requires `referral_id`, attribution ref, target owner/product, suspected target ref, evidence refs, semantic preservation constraints, requested outcome, response contract ref, limitations, and content hash. A referral is `REQUESTED`, `ACKNOWLEDGED`, `DECLINED`, `SUPERSEDED`, or `CLOSED`; acknowledgement does not mean repair success.

### 6.6 `RoleSemanticContextRequirement` and Pipeline JIT conformance

AIR's `RoleSemanticContextRequirement` requires `requirement_id`, repair/attribution ref, workflow role, task purpose, required semantic object refs by role, required epistemic assertions, required preservation/lock refs, allowed semantic action classes, forbidden semantic actions, required output schema ref, evaluation profile ref, source redaction constraints, limitations, and hash.

Pipeline's external `JITContextCapsule` is expected to expose at least `capsule_id`, version/hash, role, actual actor, capability owner, product boundary, Workflow Node ref, task, immutable object refs, typed context entries, context-manifest ref, allowed/forbidden actions, node-local tool grants, output schema ref, evaluation profile ref, repair-program/referral ref, created/expiry/cancellation evidence, and limitations. It remains Pipeline-owned runtime state.

`JITCapsuleConformanceReceipt` records AIR requirement ref, Pipeline capsule ref, exact required/present/missing/extra semantic refs, forbidden-action result, role/actor/product separation result, redaction result, stale-ref result, evaluator result, verdict, and hash. AIR may reject a capsule that changes or omits semantic constraints, but it does not take ownership of the capsule or execute it.

### 6.7 `LearningAttributionDisposition`

Required fields are `disposition_id`, `episode_ref`, `attribution_ref`, `responsible_layer_refs`, `candidate_learning_class`, `decision`, `evidence_refs`, `excluded_alternative_refs`, `applicability_envelope_ref`, `human_review_requirement`, `prohibited_generalizations`, `proposed_queue_ref`, `owner_product_id`, `evaluation_receipt_refs`, `limitations`, and hash.

`candidate_learning_class` is `SOURCE`, `KNOWLEDGE`, `RETRIEVAL`, `CONTEXT`, `SKILL`, `STEERING_RECIPE`, `PROGRAMMED_MODEL`, `TOOL`, `RUNTIME`, `PIPELINE`, `VAE`, `EVALUATOR`, or `HUMAN_POLICY`. A disposition cannot change a registry, dataset, model, recipe, profile, DNA object, or production binding. It is admission evidence for a later owner-controlled review.

### 6.8 Commands, receipts, and public ports

Commands are `RecordFailureSignal`, `ProposeFailureAttribution`, `ResolveFailureAttribution`, `CompileSemanticRepairProgram`, `ReferRepairToOwner`, `RegisterExternalRepairObservation`, `CloseRepairAttempt`, and `ClassifyLearningOpportunity`. Each command requires ID/payload hash, expected stream/object version, exact inputs, actor, authority, submitted time, and desired transition.

Receipts include command/payload hashes, prior/result refs, transition, deterministic gates, evaluator refs, staged/committed members, external publication status, typed blocker or null, authority, actor, stream version, and receipt hash. An external outbox delivery receipt is distinct from owner acknowledgement, execution, evaluation, and closure.

Public interfaces are typed ports:

```text
FailureAttributionCommandPort.handle(CommandEnvelope) -> CommandReceipt
FailureAttributionReadPort.get(ImmutableRef) -> FailureAttribution
FailureRepairHistoryPort.replay(case_id, through_stream_version) -> ReplayPackage
RepairReferralPort.publish(RepairReferral) -> TransportSubmissionReceipt
PipelineRepairPort.submit(SemanticRepairProgram) -> PipelineAdmissionReceipt
PipelineRepairObservationPort.register(ExternalRepairObservation) -> CommandReceipt
JITCapsuleConformancePort.evaluate(requirement_ref, capsule_ref) -> JITCapsuleConformanceReceipt
LearningAttributionPort.classify(episode_ref, attribution_ref) -> LearningAttributionDisposition
```

Cross-product adapters depend on released external contracts or exact candidate contract seeds permitted at implementation time. They do not import another product's internal modules or create local schema forks.

## 7. Implementation stages and exact target paths

Every path in this section is a future implementation target, not an authorized write in Prompt 03. Ratification/adoption as required, independent audit and re-audit, a separately issued Development Capsule, and explicit build authorization must precede creation.

| Stage | Future exact target paths | Required completion evidence |
|---|---|---|
| 0. Source and authority lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-019/SOURCE_LOCK.yaml`; `.../PATH_ALLOWLIST.yaml` | Ratified/adopted authority, accepted upstream interfaces, exact source/Primitive hashes, product contract pins, and no unresolved owner. |
| 1. Strict domain models | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/failure_attribution.py`; `.../domain/semantic_repair.py`; `.../domain/repair_context.py`; `.../domain/learning_attribution.py` | Closed types, schema/model parity, canonical hash vectors, no mutable defaults/open maps. |
| 2. Registry and validation | `.../registries/failure_layer_registry.py`; `.../validation/failure_attribution_validator.py`; `.../validation/semantic_repair_validator.py`; `.../validation/jit_capsule_conformance.py` | Unknown layer/owner/profile rejection, exact selector/lock/preservation checks, parsing-plus-enforcement tests. |
| 3. Repository and lifecycle | `.../repositories/failure_repair_repository.py`; `.../services/failure_repair_lifecycle_service.py` | Atomic parity, optimistic concurrency, idempotency, cancellation, replay, supersession, outbox and orphan detection. |
| 4. Attribution compiler | `.../services/failure_attribution_service.py`; `.../evaluation/failure_attribution_evaluator.py` | Deterministic gates, independent judgment, multi-causal/contested/unresolved fixtures, producer/evaluator separation. |
| 5. Semantic repair compiler | `.../services/semantic_repair_program_service.py`; `.../evaluation/semantic_repair_evaluator.py` | Permitted/forbidden/preserved sets, human boundary, stopping/escalation, cause-to-change fit, no external mutation. |
| 6. Pipeline and owner adapters | `.../adapters/atomic_harness_pipeline_repair.py`; `.../adapters/visual_asset_editor_repair.py`; `.../adapters/interview_expression_repair.py`; `.../adapters/studio_human_resolution.py` | Producer/consumer contract tests; AIR semantic constraints preserved; Pipeline/VAE/Interview/Studio ownership unchanged. |
| 7. JIT semantic requirement and conformance | `.../services/role_semantic_context_requirement_service.py`; `.../services/jit_capsule_conformance_service.py` | Role-specific positive/negative context manifests, forbidden-action denial, stale/ref/redaction tests, Pipeline ownership proof. |
| 8. Learning attribution | `.../services/learning_attribution_service.py`; `.../evaluation/learning_attribution_evaluator.py` | FR-098 class coverage, ambiguity and excluded alternatives, no automatic promotion, scope/human-review receipts. |
| 9. Contracts, fixtures, and migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/failure-repair/*.schema.json`; `.../contracts/examples/failure-repair/`; `.../src/cmf_activative_intelligence/migrations/ai2_failure_repair_to_v2_1.py` | Separately governed generated artifacts, positive/adversarial fixtures, lossless-or-blocked migration receipts. |
| 10. Integration and recovery proof | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/failure_repair/`; `.../tests/architecture/test_failure_repair_product_boundaries.py`; `.../tests/recovery/test_failure_repair_replay.py` | Full FR/Story, cross-product, fault-injection, replay, rollback, historical reproducibility, and claim-ceiling evidence. |

Suggested test modules are exact future targets:

- `tests/unit/failure_repair/test_failure_layer_registry.py`
- `tests/unit/failure_repair/test_failure_attribution.py`
- `tests/unit/failure_repair/test_semantic_repair_program.py`
- `tests/unit/failure_repair/test_role_context_requirement.py`
- `tests/unit/failure_repair/test_learning_attribution.py`
- `tests/contract/failure_repair/test_schema_model_parity.py`
- `tests/contract/failure_repair/test_pipeline_repair_handoff.py`
- `tests/contract/failure_repair/test_jit_capsule_conformance.py`
- `tests/integration/failure_repair/test_attribution_to_repair.py`
- `tests/integration/failure_repair/test_owner_referrals.py`
- `tests/integration/failure_repair/test_atomic_repository.py`
- `tests/recovery/test_failure_repair_replay.py`
- `tests/architecture/test_failure_repair_product_boundaries.py`
- `tests/adversarial/test_failure_repair_denials.py`

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures and owning response

| Code | Condition | Owner / required response |
|---|---|---|
| `AIR_REPAIR_SIGNAL_INVALID` | Failed object, result, actor, authority, or evidence ref is absent/invalid. | Submitter/AIR intake; deny with no attribution artifact. |
| `AIR_REPAIR_LAYER_UNKNOWN` | Candidate layer is absent from the pinned registry. | AIR contract owner; fail closed, never coerce to nearest string. |
| `AIR_REPAIR_OWNER_MISMATCH` | Layer/target owner conflicts with authority registry. | Program Control/declared owner; emit referral/blocker, no mutation. |
| `AIR_REPAIR_EPISTEMIC_OVERCLAIM` | Inference/model/evaluation is represented as observation or human confirmation. | AIR; reject attribution/repair. |
| `AIR_REPAIR_CAUSE_UNSUPPORTED` | Root-cause claim lacks adequate evidence under bound profile. | AIR/evaluator; remain `UNRESOLVED` or `CONTESTED`. |
| `AIR_REPAIR_ALTERNATIVES_HIDDEN` | Material alternatives or evaluator disagreement were discarded. | AIR; deny closure and preserve full candidate set. |
| `AIR_REPAIR_SELF_EVALUATION` | Producer and required independent evaluator identities overlap. | Evaluator control; no eligibility/closure. |
| `AIR_REPAIR_TARGET_EXTERNAL` | AIR semantic program attempts to mutate a non-AIR-owned object. | AIR; replace with `RepairReferral`. |
| `AIR_REPAIR_SCOPE_UNBOUNDED` | Missing/wildcard/overlapping permitted, forbidden, or preserved selectors. | AIR; deny program. |
| `AIR_REPAIR_PRESERVATION_GAP` | Valid semantic lineage or relation lacks a preserved assertion. | AIR; reacquire evidence or recompile. |
| `AIR_REPAIR_LOCK_WEAKENED` | Inherited wrong-reading lock is removed, weakened, or omitted. | AIR/upstream authority; reject; require authorized successor demand/program. |
| `AIR_REPAIR_HUMAN_AUTHORITY_REQUIRED` | New meaning, unresolved taste, identity/source approval, policy exception, or promotion is requested. | Attributable human; Studio may capture but not decide. |
| `AIR_REPAIR_PIPELINE_SCOPE_BROADENED` | Pipeline plan or JIT capsule expands semantic change/actions beyond program. | Pipeline; reject plan/capsule; AIR object remains unchanged. |
| `AIR_REPAIR_JIT_CONTEXT_INCOMPLETE` | Required semantic ref/epistemic gap/lock/evaluation constraint is absent. | Pipeline context compiler; rebuild or block node. |
| `AIR_REPAIR_JIT_AUTHORITY_LEAK` | Role, actor, or tool is represented as semantic/product authority. | Pipeline/AIR conformance; deny execution. |
| `AIR_REPAIR_STALE_EXPECTED_VERSION` | Command expected version is not current. | Caller; refresh exact state and submit a new command. |
| `AIR_REPAIR_IDEMPOTENCY_CONFLICT` | Same command ID carries different canonical payload bytes. | Caller; no commit. |
| `AIR_REPAIR_ATOMIC_COMMIT_FAILED` | Any AIR artifact/event/edge/receipt/idempotency/outbox member fails. | AIR repository; rollback all staged members. |
| `AIR_REPAIR_REPLAY_DIVERGENCE` | Rebuilt bytes/decisions differ from historical evidence. | AIR; stop at first divergence and open incident. |
| `AIR_REPAIR_MIGRATION_AMBIGUOUS` | Predecessor lacks required layer/owner/epistemic/preservation/authority. | Migration owner; emit blocked receipt, never infer. |
| `AIR_REPAIR_LEARNING_ATTRIBUTION_MISSING` | Episode is submitted to learning without causal disposition. | Queue owner; reject admission. |
| `AIR_REPAIR_LEARNING_SCOPE_OVERCLAIM` | Local evidence is generalized beyond applicability or human approval. | Learning owner/human; reject promotion and preserve episode. |

Deterministic validation failures are not blindly retried. Transient storage or transport failures may retry only with the same idempotency identity and exact payload. A causal/quality failure uses a new command and preserves the old receipt. Provider retry belongs to VAE; execution retry belongs to Pipeline; transport retry belongs to Delegation.

### 8.2 Migration and compatibility

Compatibility is semantic, not parse-only. Adapters must preserve required field meaning, owner, epistemic state, authority, exact ref/version/hash, preservation constraints, limitations, lifecycle, and claim ceiling. An adapter that drops candidate alternatives, turns free text into a governed layer without evidence, inserts empty locks, expands permitted fields, or maps an external execution plan to AIR state is incompatible.

Migration creates new immutable candidate artifacts and a receipt containing source bytes/hash, adapter version/hash, mapping decisions, unavailable fields, blockers, target hash, and authority. Historical V2/AI2 objects remain byte-reproducible. Active historical runs remain pinned to their negotiated versions; deprecation does not rewrite them.

The predecessor `responsible_layer` free string maps only when an exact governed alias and owner exist in the migration table. Otherwise it becomes `UNAVAILABLE_FROM_PREDECESSOR` and blocks attributed status. `root_cause` prose is imported as historical assertion evidence, never direct truth. Predecessor invalidated-descendant/rerun values are observed historical execution evidence, not AIR-authored current graph state.

### 8.3 Rollback, cancellation, recovery, and invalidation

Rollback changes active service, adapter, registry, evaluator-profile, or model bindings for future commands; it never deletes or edits artifacts produced under the failed binding. The last known-good binding is itself hash-pinned and a rollback receipt records the decision authority and affected command range.

Recovery rebuilds streams, object heads, attribution/repair state, idempotency records, outbox delivery state, and projections from immutable artifacts/events. It verifies all hashes and compares the rebuilt checkpoint hash. External Pipeline/VAE/Delegation state is reconstructed from exact external receipts, not mutable API “current” state.

AIR emits dependency-impact constraints and observes Pipeline's typed invalidation receipt. Pipeline traverses the authoritative runtime graph and invalidates reachable current descendants only. Derivatives may add stricter locks but cannot remove inherited locks. Historical outputs and the context accepted at the time remain replayable after supersession, cancellation, rejection, or revocation. A stale target, semantic program, context capsule, execution plan, result, or evaluation cannot be consumed as current.

### 8.4 Upstream draft revision impact

Any change to the frozen TS-AIR-001 interface reopens authority/actor/epistemic models, canonical identity, command/receipt behavior, repository atomicity, invalidation, replay, acceptance, and tests. Any change to TS-AIR-005 reopens Primitive/coalition/Edge Product/Steering Recipe evidence, preservation, failure-layer mapping, repair scope, learning classification, and tests. Any change to TS-AIR-017 reopens visual failure layers, Composition Intent/Feature Contract/lock preservation, AIR/Pipeline/VAE referral boundaries, visual reparse evidence, acceptance, and tests.

Acceptance of an upstream draft does not automatically accept this spec. A byte or public-interface change requires an attributable revision-impact decision and, if material, a revised draft followed by independent re-audit.

### 8.5 Observability

Structured logs record command, case, signal, attribution, target, owner, authority, actor, layer, candidate, evaluator, semantic program, referral, Pipeline plan/capsule/execution refs, learning disposition, stream version, idempotency, commit, and blocker codes. Raw private source content, unrestricted prompts, secrets, and full JIT context are excluded; logs use refs and approved locators.

Metrics include signal/attribution status, layer/owner, unresolved/contested/multi-causal rate, excluded-alternative count, self-evaluation denials, repair-scope denials, lock/preservation gaps, external referrals, Pipeline conformance denials, JIT missing/extra context, rerun/reuse receipt observations, human escalation, learning disposition, atomic rollback, concurrency conflict, idempotent replay, outbox delivery, late evidence, and replay divergence. Metrics are operational evidence, not semantic truth, causal proof, user value, production readiness, or certification.

Alerts fire on orphan object/receipt pairs, hash mismatch, unknown layer, owner drift, an observed assertion without direct evidence, semantic mutation outside permitted selectors, lock weakening, execution without conforming JIT context, queue admission without attribution, or replay divergence.

## 9. Behavior-specific acceptance criteria

### AC-01 - AIR-FR-109 / AIR-ST-19.01: attribute the authoritative failure layer

**Given** an exact failure signal for an AIR semantic, transfer, visual-semantic, execution, production, evaluation, or operator-resolution result, **when** attribution runs, **then** candidates distinguish source, epistemic state, Matrix, hypothesis, Primitive, coalition/Edge Product, archetype, brand/DNA, script, transfer, retrieval, context, Skill, Steering Recipe, Programmed Model, composition, tool, runtime, Pipeline, VAE, evaluator, and operator/human-policy layers using governed IDs and exact owners. **And** the immutable result contains source/evidence refs, alternatives, exclusions, lifecycle, epistemic states, evaluator identity, limitations, and repair route. **Evidence:** candidate set, registry resolution, validation/evaluation receipts. **Layer:** contract/integration.

### AC-02 - AIR-FR-109 / AIR-ST-19.01: ambiguity and multi-causality are not guessed away

**Given** evidence supports both a stale retrieval result and a model-context omission, or cannot distinguish them, **when** attribution runs, **then** it emits `MULTI_CAUSAL`, `CONTESTED`, or `UNRESOLVED` with all candidates and next evidence/authority action. Choosing a convenient single owner, inventing a confidence threshold, or rewriting the prompt fails. **Evidence:** adversarial candidate corpus and immutable denial/contested receipt. **Layer:** domain/evaluation.

### AC-03 - AIR-FR-109 / AIR-ST-19.01: owner attribution does not transfer authority

**Given** a VAE-produced image violates an AIR Composition Intent, **when** the cause is analyzed, **then** an AIR semantic-input defect, Pipeline demand/execution defect, VAE realization defect, or unresolved cross-layer cause is distinguished by evidence. AIR cannot change the VAE production plan; VAE cannot change Composition Intent; Pipeline cannot reinterpret the semantic requirement. **Evidence:** owner matrix, three candidate fixtures, referral receipts. **Layer:** architecture/contract.

### AC-04 - AIR-FR-109 / AIR-ST-19.01: valid history and upstream meaning remain frozen

**Given** an exact failed version and valid upstream semantic objects, **when** an attribution commits, **then** frozen refs preserve exact versions/hashes and no upstream object is rewritten or globally invalidated. A latest alias, missing epistemic assertion, flattened lineage note, or changed historical byte fails. **Evidence:** before/after hash matrix and replay proof. **Layer:** repository/recovery.

### AC-05 - AIR-FR-111 / AIR-ST-19.02: compile a bounded AIR semantic repair

**Given** an attributed AIR-owned target and exact mutation authority, **when** repair compilation runs, **then** the program states the exact target, permitted and forbidden selectors, preserved properties, frozen refs, inherited locks, required evidence/output, evaluation profile, stopping law, and escalation route. Missing field-level bounds, wildcard mutation, or a free-text “improve prompt” instruction fails `AIR_REPAIR_SCOPE_UNBOUNDED`. **Evidence:** program fixture, selector validator, independent boundedness receipt. **Layer:** domain/integration.

### AC-06 - AIR-FR-111 / AIR-ST-19.02: external-owner defects are referred, not repaired by AIR

**Given** attribution identifies Pipeline execution, VAE production, Interview Expression evidence, Delegation transport, evaluator-profile, Program Control, or human-policy ownership, **when** continuation is selected, **then** AIR emits a typed referral with evidence and semantic preservation constraints and creates no external mutation. **Evidence:** per-owner referral conformance receipts and forbidden-import/command tests. **Layer:** architecture/security.

### AC-07 - AIR-FR-111 / AIR-ST-19.02: Pipeline executes without semantic reinterpretation

**Given** an eligible AIR `SemanticRepairProgram`, **when** Pipeline admits it, **then** Pipeline computes its own dependency traversal, invalidation set, checkpoint reuse, rerun graph, actor/tool bindings, JIT state, and execution receipts while preserving AIR permitted/forbidden/preserved/lock constraints. A Pipeline plan that broadens fields, changes the Edge Product, weakens locks, or fabricates meaning is rejected. **Evidence:** AIR/Pipeline producer-consumer contract and negative scope-diff fixture. **Layer:** contract/architecture.

### AC-08 - AIR-ST-19.02 interface: JIT roles remain bounded and explicit

**Given** a repair task assigned to Hunter, Analyst, Composer, or Commander, **when** Pipeline creates its JIT capsule, **then** actor, role, capability owner, product boundary, exact context refs, allowed/forbidden actions, tool grants, output schema, evaluation profile, and stopping law are separate and hash-pinned. The same unrestricted context for every role, hidden actor identity, or role-derived authority fails conformance. **Evidence:** four role manifests, semantic-context requirements, denial receipts. **Layer:** contract/security.

### AC-09 - AIR-ST-19.02 CBAR: repair preserves hierarchy and valid semantic relationships

**Given** a local semantic repair to a composition or script-dependent object, **when** preserved-property validation runs, **then** applicable hierarchy, role/tension, coalition, Edge Product, source/DNA, Final Script, transfer, Feature Contract, and wrong-reading relationships remain exact unless explicitly and lawfully targeted. Arbitrary emphasis, inverted hierarchy, or broad regeneration fails. **Evidence:** preserved-property diff and PRM-BUS-006 misuse fixtures. **Layer:** CBAR/integration.

### AC-10 - FR-098 / ST-10.01: learning opportunity is attributed before queue admission

**Given** a complete production episode or operator correction, **when** learning admission is requested, **then** AIR distinguishes source, knowledge, retrieval, context, Skill, Steering Recipe, Programmed Model, tool, runtime, Pipeline, VAE, evaluator, or human-policy opportunity; records evidence, profile-produced confidence basis, excluded alternatives, applicability, and human-review need; and emits one controlled disposition. Missing or ambiguous attribution cannot enter the learning queue as eligible. **Evidence:** all-class table, ambiguous fixture, queue rejection receipt. **Layer:** domain/integration.

### AC-11 - FR-098 / ST-10.01: scoped review is not promotion

**Given** one accepted operator correction, **when** the disposition is `ELIGIBLE_FOR_SCOPED_REVIEW`, **then** no Skill, recipe, model, evaluator rule, Primitive, archetype, DNA profile, or live weight changes. A universal rule inferred from one rejection fails `AIR_REPAIR_LEARNING_SCOPE_OVERCLAIM`. **Evidence:** no-mutation architecture test, applicability envelope, later-owner handoff. **Layer:** governance/architecture.

### AC-12 - deterministic and independent evaluation separation

**Given** attribution or repair uses judgment, **when** eligibility/closure is requested, **then** deterministic schema/hash/owner/lifecycle/lineage/scope/lock gates pass first and an independent evaluator identity assesses causal adequacy or semantic preservation. Producer self-approval, evaluator override of a hard gate, or an evaluator becoming target owner fails. **Evidence:** identity matrix and hard-gate disagreement fixtures. **Layer:** evaluation/architecture.

### AC-13 - exact `NOT_APPLICABLE` behavior

**Given** `PRM-VSG-001` or a visual repair check is claimed not applicable to a strictly audio-only target, **when** applicability validation runs, **then** the exact target/profile, condition, evidence, limitation, and owner support `NOT_APPLICABLE`. Source lineage, owner, repair scope, human authority, and required locks can never be waived as N/A. A bare boolean or absent evidence fails. **Evidence:** positive audio-only and negative visual-target fixtures. **Layer:** contract/CBAR.

### AC-14 - wrong-reading-lock monotonicity

**Given** a generative, composited, restyled, or semantically transformative descendant, **when** repair compiles and Pipeline plans reruns, **then** all parent locks are present and descendants may only add stricter locks. Relaxation requires a new authorized upstream semantic version. **Evidence:** parent/child lock diff and denial receipt. **Layer:** contract/integration.

### AC-15 - idempotency, concurrency, atomic rollback, and cancellation

**Given** exact retry, byte-different command-ID reuse, two writers at one expected version, injected failure at every transaction member, and cancellation racing with commit, **when** commands execute, **then** exact retry returns one stored outcome; collision fails; one writer wins; all AIR members commit or none; and cancellation cannot erase a commit. **Evidence:** fault matrix, transaction parity, command/receipt counts. **Layer:** repository/integration.

### AC-16 - replay and historical reproducibility

**Given** a closed repair followed by superseded objects, changed model/profile bindings, or revoked current eligibility, **when** historical replay runs, **then** exact prior object/context/candidate/decision/program/execution/evaluation/human refs reproduce the historical bytes and outcome without current/latest substitution. Missing human authority remains missing. **Evidence:** historical hash vectors and first-divergence test. **Layer:** recovery.

### AC-17 - visual result attribution preserves production and consumption semantics

**Given** a VAE production-accepted result and an AIR visual reparse failure, **when** attribution runs, **then** production acceptance remains VAE-owned, Pipeline consumption remains a separate acknowledgement, and AIR's semantic repair/referral remains separate. No state is inferred from another. **Evidence:** three-receipt lifecycle fixture. **Layer:** lifecycle/integration.

### AC-18 - feedback is meaningful without vanity or interruption

**Given** an attribution, denial, repair result, or learning disposition, **when** an operator projection renders it, **then** it states what exact object/invariant was affected, why it matters, owner, and next admissible action. It does not award arbitrary scores or interrupt a protected live recording. **Evidence:** projection fixtures and EXP-FBK-001 misuse denials. **Layer:** CBAR/UX contract.

### AC-19 - no implementation or authority overclaim

**Given** all structural and synthetic specification tests pass, **when** lifecycle status is reported, **then** the document remains `WRITTEN_PENDING_AUDIT`, authority remains `CANDIDATE_NOT_CURRENT`, build/production/certification remain false, and the next action is independent audit by a different agent. `ACCEPTED_FOR_BUILD`, a Development Capsule, or product-adoption claim fails. **Evidence:** metadata and receipt assertion. **Layer:** governance.

## 10. Testing and completion evidence

### 10.1 Test layers and mandatory cases

| Layer | Mandatory evidence |
|---|---|
| Schema/model parity | Positive/negative fixtures for every contract; missing/unknown fields; enum/layer/owner/profile mismatch; canonical serialize/deserialize/hash vectors; no open maps or mutable defaults. |
| Domain | All attribution statuses, every failure-layer family, target-owner relation, causal alternatives/exclusions, field epistemology, repair applicability, permitted/forbidden selectors, preserved properties, lock monotonicity, referrals, role context, and learning dispositions. |
| Deterministic validation | Exact ref/hash/lifecycle/owner/authority, source/epistemic, selector, preservation, lock, profile, actor/role/product separation, stale state, and N/A enforcement. |
| Independent evaluation | Producer/evaluator separation, causal adequacy, disputed/multi-causal cases, cause-to-change fit, semantic preservation, calibration/version pin, disagreement, and unavailable evaluator behavior. |
| Repository | Atomic artifact/event/edge/command/receipt/idempotency/outbox parity; exact retry; collision; optimistic concurrency; cancellation races; rollback; orphan detection. |
| Cross-product contract | Pipeline accepts/rejects without semantic reinterpretation; VAE/Interview/Studio/Delegation/Program Control referrals preserve owner; transport receipt is not owner acceptance; production acceptance is not consumption. |
| JIT conformance | Four roles, minimum context, missing/extra/stale refs, hidden actor, unauthorized tools/actions, output/evaluation binding, cancellation/expiry, redaction, and Pipeline ownership. |
| Learning | Every FR-098 class, ambiguous/no-reason rejection, excluded alternatives, human review, applicability, duplicate evidence, ineligible queue admission, and no automatic promotion. |
| Migration | Eligible exact mapping, unknown alias, missing owner/epistemic/layer, free-text cause, historical descendants/reruns, lossless round trip, and blocked receipts. |
| Replay/recovery | Historical context and model/profile bindings, successor/referral branches, lock/invalidation fan-out, current/latest substitution denial, hash divergence, and revoked-current but reproducible-history cases. |
| Architecture/import | AIR does not import Pipeline/VAE internals; Pipeline owns runtime JIT/repair plan; AIR owns semantic attribution/program meaning; evaluator/Studio/Delegation do not become semantic owners. |
| Security/operations | Schema/size limits, path/ref validation, context redaction, secret exclusion, node-local tools, transport authenticity, replay protection, and structured-log privacy. Technical security does not create creative/source approval authority. |
| Clean environment | Tests and examples run from declared dependencies without absolute machine paths, traversal-order dependence, wall-clock/random/environment-dependent semantic output, hidden caches, or undeclared files. |

### 10.2 Required evidence matrix by controlling requirement

| Requirement / Story | Primary evidence | Adversarial evidence | Completion ceiling |
|---|---|---|---|
| AIR-FR-109 / AIR-ST-19.01 | Governed layer registry, exact candidate/evidence/owner/epistemic set, immutable attribution and independent receipt. | Unknown layer, hidden alternative, unsupported cause, multi-causal/contested/unresolved cases, external-owner boundary, broad regeneration denial. | Structural/synthetic conformance only. |
| AIR-FR-111 / AIR-ST-19.02 | Exact target, bounded change/preservation/lock sets, stopping/escalation, referral or Pipeline handoff, JIT conformance and replay refs. | Wildcard scope, external mutation, lock weakening, semantic reinterpretation, same-context roles, human-boundary bypass, self-evaluation. | Structural/synthetic conformance only. |
| FR-098 / ST-10.01 | Complete episode ref, causal class, evidence/confidence basis, excluded alternatives, applicability, human-review and queue disposition. | No-reason rejection, ambiguous cause, universal promotion, missing attribution, hidden UI mutation, learning queue bypass. | Scoped learning-review admission contract only; no promotion claim. |

### 10.3 Determinism and portability proof

Run each canonical fixture in two clean processes and at least two supported filesystem roots. Assert byte-identical semantic objects and hashes from identical inputs. Inject time, IDs, model/profile choice, and external results as explicit inputs; do not read wall clock, global random state, dictionary insertion order, filesystem traversal order, absolute path, locale, timezone, or process environment during deterministic compilation. Set-semantics inputs are normalized by declared keys; order-sensitive evidence remains ordered.

Artifacts and receipts store workspace-relative logical paths or immutable content refs, never developer-machine absolute paths. Archives and migration inputs reject traversal, drive-qualified members, symlinks escaping extraction root, duplicate normalized paths, case collisions, and undeclared members. Context manifests record included content hashes rather than local cache paths.

### 10.4 Completion evidence and stop law

Implementation completion, if later authorized, requires:

1. exact source and accepted-interface locks;
2. schema/model parity and canonical hash vectors;
3. all AC-01 through AC-19 positive and adversarial evidence;
4. cross-product producer/consumer conformance without local schema forks;
5. atomicity, replay, migration, rollback, cancellation, and historical-reproduction proof;
6. independent evaluator calibration and separation evidence;
7. clean-environment and portability proof;
8. no unresolved source, authority, owner, human decision, or product-boundary blocker;
9. a truthful claim ceiling and separate ratification/adoption/build receipts.

Stop and emit a typed blocker if a required source or upstream draft is missing/drifted; authority/owner/layer is ambiguous; the target path collides; the operation would write code/schema/release bytes; a role would receive hidden authority or unrestricted context; a repair would mutate an external/human-owned object, weaken locks, or broaden scope; independent evaluation cannot distinguish success from polished failure; replay diverges; or a build/production/certification claim is requested without its separate authority.

The writing-factory completion state for this document is exactly:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
next_lifecycle_action: INDEPENDENT_AUDIT_BY_DIFFERENT_AGENT
```

