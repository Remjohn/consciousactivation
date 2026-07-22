---
title: "CMF Eval Registry and Workbench Architecture"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "docs/tech-specs/TS-CMF-014-registry-conversion-fixtures-and-evals.md"
  - "docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md"
  - "docs/tech-specs/TS-CMF-051-evidence-rich-review-surface.md"
  - "docs/tech-specs/TS-CMF-053-approval-blockers.md"
  - "CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md"
  - "CCP_Creative_Pipeline_Architecture_V2.md"
  - "CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md"
  - "reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md"
  - "src/ccp_studio/contracts/evaluation_receipts.py"
  - "src/ccp_studio/contracts/doctrine_evals.py"
  - "src/ccp_studio/services/doctrine_evaluation_service.py"
---

# CMF Eval Registry and Workbench Architecture

## 1. Purpose

Evaluation in CMF Studio must be registry-backed. The current receipt layer records the result of an evaluation, but the system also needs registries that decide which evaluations are required for a given object, stage, route, primitive obligation, and review surface.

## 2. Canonical Chain

```text
Eval registries
-> eval target selection
-> eval run command
-> EvaluationReceipt
-> approval blocker
-> review read model
```

## 3. Registry Families

| Registry | Purpose | Example records |
|---|---|---|
| `EvalDefinitionRegistry` | Defines an evaluator, category coverage, evidence requirements, primitive obligations, and default threshold profile | source truth critic, primitive coalition critic, route fit critic |
| `EvalTargetBindingRegistry` | Binds eval definitions to object types, pipeline stages, route refs, provider outputs, and primitive refs | expression moment requires source truth and expression depth |
| `ThresholdProfileRegistry` | Stores threshold sets by route, risk tier, brand context, and object type | default CMF thresholds, identity-sensitive thresholds |
| `FixtureCounterexampleRegistry` | Stores golden examples, counterexamples, failure cases, and legacy migration fixtures | anti-centroid failure cases, coalition collapse examples |
| `BenchmarkProfileRegistry` | Stores route and primitive performance benchmarks | primitive family win/loss memory, route conversion baseline |
| `EvalRunPolicyRegistry` | Defines when evals are required, optional, rerunnable, blocking, or human-review-only | render output must pass before approval |

## 4. Primitive Quality Standard

Primitive obligations are first-class in eval definitions. Required fields:

- `required_primitive_refs`
- `required_primitive_families`
- `expected_coalition_refs`
- `expected_edge_products`
- `matrix_passes`
- `anti_centroid_pressure`
- `route_implications`
- `hard_negative_refs`

Evaluation must answer:

- Did the intended primitive activate?
- Did the primitive activation have evidence?
- Did the coalition survive into the output?
- Did the output preserve the edge product?
- Did the route match the primitive and source expression?
- Did the asset flatten into a centroid or generic artifact?

## 4.1 Doctrine Eval Registry

The first canonical doctrine evals are registered under `registries/evals/doctrine/`.

| Eval ID | Registry file | Blocks when missing |
|---|---|---|
| `EVL-DOCTRINE-IAC-001` | `cmf_interview_brief_doctrine_eval.v1.json` | CRAL/SCRE signal, audience conversation, Context Premise, trigger map, interviewer resonance, Matrix of Edging, primitive registry, First-Line Anchors, Depth Anchor, landing targets, repair followups, route targets, hard negatives, or CCP V9/V9.1/Claude/legacy primitive source refs |
| `EVL-DOCTRINE-BGN-001` | `cmf_brand_genesis_doctrine_eval.v1.json` | client intake, explicit consent, source media QC, business intelligence, Tribe Soul, Character Lexicon, Voice DNA/Negative Space, visual constitution, identity pack, 64 acting plan, PaperCut rig plan, micro-semiotic library, clearance certificate, or required identity/audience/voice/visual/safety primitive families |
| `EVL-DOCTRINE-ACT-064-001` | `cmf_64_state_acting_library_doctrine_eval.v1.json` | Identity Pack, human approval before generation, full 8 x 8 acting matrix, provider receipts, cell metadata, QC scores, human review grid, Negative Space update route, library lock receipt, or ACT/IDN/NEG/VSG/SAF primitive families |
| `EVL-DOCTRINE-PPR-RIG-001` | `cmf_papercut_rig_doctrine_eval.v1.json` | approved acting library lineage, required avatar asset set, layer decomposition, hidden-region repair, canonical rig manifest, editor independence, preview tests, motion constitution, PaperCut style constitution, Ideogram 4 composition JSON, micro-semiotic anchor refs, rig lock receipt, or RIG/MOT/VSG/MSA/SAF primitive families |

These evals convert the previously under-specified source doctrine into executable approval gates. They are not generic quality checks. They enforce the exact CMF substrate needed before the operator can trust interview briefs, guest workspaces, asset libraries, rigged actors, animation plans, and review surfaces.

## 5. Eval Target Selection

Input:

- organization and brand;
- object type and object ID;
- pipeline stage;
- route refs;
- primitive refs;
- primitive families;
- risk flags;
- required review surface.

Output:

- required eval definitions;
- optional eval definitions;
- threshold profile;
- run command payloads;
- UI suggestions;
- blocking reasons when no matching eval exists.

Selection rule:

```text
object_type + stage + route refs + primitive obligations + risk flags
-> active eval target bindings
-> run policy
-> required eval set
```

## 6. Eval Run Command

The run command does not let the UI score. It selects active eval definitions, invokes the approved evaluator or DSPy program, normalizes category inputs, then delegates immutable receipt creation to the existing EvaluationReceipt service.

Required command outputs:

- `eval_run_id`
- selected eval definition IDs;
- target binding IDs;
- generated `evaluation_receipt_id`;
- approval blocker IDs;
- review read-model link.

## 7. Review Workbench Requirements

The Workbench must show:

- selected target bindings;
- required evals and skipped optional evals;
- receipt history and supersession;
- primitive failures;
- approval blockers;
- evidence refs;
- repair actions;
- PWA/Telegram routing.

The Workbench must not:

- score locally;
- approve from evaluator output alone;
- hide source truth, consent, route, primitive, or evidence failures behind a preview.


