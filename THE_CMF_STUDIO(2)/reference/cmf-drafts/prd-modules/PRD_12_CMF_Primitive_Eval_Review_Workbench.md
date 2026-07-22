---
type: modular-prd
module: PRD-12
title: CMF Primitive Evaluation Registry and Review Workbench
author: John (Product Manager)
date: 2026-06-22
status: Draft Source of Truth
version: 1.0
dependencies:
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
  - docs/prd/modules/PRD_10_CMF_Interview_Intelligence.md
  - docs/prd/modules/PRD_11_CMF_JIT_Interview_Brief_Compiler.md
  - docs/evals/07-eval-registry-and-workbench-architecture.md
source_documents:
  - THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
  - docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md
  - docs/tech-specs/TS-CMF-051-evidence-rich-review-surface.md
  - docs/tech-specs/TS-CMF-053-approval-blockers.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
active_primitives:
  meaning_plane: [STR, PRS, CON, PSY, VOC, VSG, ACT, BUS]
  experience_plane: [TRG, FRC, FBK, SAF, PER]
capability_areas: [CMF-EVAL, CMF-REVIEW, CMF-PRIMITIVE-QA]
---

# PRD-12: CMF Primitive Evaluation Registry and Review Workbench

**Version:** 1.0 | **Status:** Draft Source of Truth | **Date:** 2026-06-22

## 1. Purpose and Architectural Claim

CMF evaluation must be registry-backed and primitive-aware. The system cannot treat quality as a generic model score or a reviewer vibe. Primitives are the production quality standard because they define the transformation operators that make outputs distinctive, non-generic, source-grounded, and emotionally legible.

The canonical chain is:

```text
Eval registries
-> eval target selection
-> eval run command
-> EvaluationReceipt
-> approval blocker
-> review read model
-> Review Workbench
```

The Review Workbench makes this chain visible to humans. It shows why an object must be evaluated, which primitive obligations it carries, what failed, what evidence supports the failure, which blocker prevents approval, and what repair is required.

## 2. Evaluation Registry Families

| Registry | Product role |
|---|---|
| EvalDefinitionRegistry | Defines evaluators, evidence requirements, category coverage, primitive obligations, and thresholds |
| EvalTargetBindingRegistry | Binds evals to object types, stages, route refs, primitive refs, and risk flags |
| ThresholdProfileRegistry | Stores threshold sets by object type, route, risk, and brand context |
| FixtureCounterexampleRegistry | Stores golden examples, counterexamples, hard negatives, and legacy fixtures |
| BenchmarkProfileRegistry | Stores primitive, route, and asset benchmark expectations |
| EvalRunPolicyRegistry | Defines required, optional, blocking, rerunnable, and human-review-only evals |

## 3. Primitive-Aware Evaluation

Primitive evals answer:

- Did the intended primitive activate?
- Did activation have source evidence?
- Did the primitive coalition survive into the artifact?
- Did the edge product survive?
- Did the route match the primitive and source expression?
- Did the asset flatten into generic centroid language or visuals?
- Did the output over-activate too many primitives at once?

Primitive failures must produce review-visible detail, not only a low score.

## 4. Functional Requirements

### FR-CMF-EVAL-01 Eval Definition Registry

The system shall maintain eval definitions with category coverage, evidence requirements, evaluator version, primitive obligations, fixture refs, thresholds, and hard-failure policies.

### FR-CMF-EVAL-02 Eval Target Selection

The system shall select required evals by object type, pipeline stage, route refs, primitive refs, primitive families, risk flags, and review surface.

### FR-CMF-EVAL-03 Eval Run Command

The system shall run evals through governed commands that select active definitions, collect evidence, normalize category inputs, and delegate immutable receipt creation.

### FR-CMF-EVAL-04 EvaluationReceipt

The system shall create immutable EvaluationReceipts with scores, thresholds, evidence, warnings, hard failures, receipt hash, prior receipt link when rerun, and decision.

### FR-CMF-EVAL-05 Approval Blockers

The system shall create approval blockers when hard failures occur, including primitive failure blockers such as primitive evidence missing, coalition collapsed, edge product flattened, route mismatch, or anti-centroid pressure lost.

### FR-CMF-EVAL-06 Review Read Model

The system shall expose review read models that join receipts, blockers, evidence refs, primitive failures, source truth, consent state, route, Brand Context, revision history, and repair recommendations.

### FR-CMF-EVAL-07 Review Workbench UI

The Review Workbench shall allow Operators and Reviewers to inspect target selection, run status, receipt history, primitive failure expansion, blockers, repair actions, and PWA/Telegram handoff without local scoring.

## 5. Epics and Stories

### Epic EVAL-1: Eval Registry

**Outcome:** The system knows which evals are required before a human has to guess.

- Story EVAL-1.1: Create EvalDefinition registry.
- Story EVAL-1.2: Create EvalTargetBinding registry.
- Story EVAL-1.3: Add primitive obligations to eval definitions.
- Story EVAL-1.4: Add benchmark and fixture/counterexample references.
- Story EVAL-1.5: Validate missing eval targets as blockers.

### Epic EVAL-2: Eval Execution and Receipts

**Outcome:** Required evals create immutable receipts and blockers when needed.

- Story EVAL-2.1: Select eval targets for object, stage, route, and primitives.
- Story EVAL-2.2: Submit eval run command.
- Story EVAL-2.3: Generate EvaluationReceipt.
- Story EVAL-2.4: Create approval blockers for hard failures.
- Story EVAL-2.5: Rerun evals after revision without overwriting receipt history.

### Epic EVAL-3: Review Workbench

**Outcome:** Reviewers can see quality failures clearly enough to repair or reject.

- Story EVAL-3.1: Show eval target selection and required evals.
- Story EVAL-3.2: Show receipt inspector and receipt comparison.
- Story EVAL-3.3: Show primitive failure cards.
- Story EVAL-3.4: Show approval blockers and repair actions.
- Story EVAL-3.5: Route simple review summaries to Telegram and complex review to PWA.

## 6. Non-Goals and Forbidden Drift

- No evaluator output creates approval by itself.
- No local UI scoring.
- No generic quality score hiding primitive failures.
- No mutable EvaluationReceipt history.
- No object enters approval without required eval target selection.
- No primitive quality standard outside active primitive registries and accepted fixtures.

