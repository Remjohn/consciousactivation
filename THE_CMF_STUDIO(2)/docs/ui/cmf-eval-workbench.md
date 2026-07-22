---
title: "CMF Eval Workbench"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "docs/evals/07-eval-registry-and-workbench-architecture.md"
  - "docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md"
  - "docs/tech-specs/TS-CMF-051-evidence-rich-review-surface.md"
  - "docs/tech-specs/TS-CMF-055-telegram-quick-review-with-evidence.md"
---

# CMF Eval Workbench

## 1. Product Job

The Eval Workbench is the operator surface for understanding whether an object is review-ready. It connects eval registry target selection, eval run commands, immutable receipts, blockers, and primitive-specific repair guidance.

It is not a gallery page and not a local scoring dashboard.

## 2. Primary Views

| View | Purpose |
|---|---|
| Target Selection | Shows why each eval is required for this object, route, stage, provider, and primitive obligation |
| Run Queue | Shows pending, running, completed, failed, and rerunnable eval runs |
| Receipt Inspector | Shows category scores, thresholds, evidence refs, warnings, hard failures, and receipt hash |
| Primitive Failure Inspector | Shows missing or failed primitive refs, coalition collapse, edge-product drift, anti-centroid flattening, and route mismatch |
| Blocker Panel | Shows approval blockers created from hard failures and the required repair action |
| Review Read Model | Shows the evidence-rich review state that PWA and Telegram surfaces consume |

## 3. Core Actions

- Select required eval targets.
- Run required evals.
- Rerun after revised object hash.
- Compare receipt history.
- Expand primitive failure.
- Inspect blocker evidence.
- Request revision.
- Open PWA review.
- Send Telegram quick-review notification when eligible.

Approval still goes through governed review commands. The Workbench does not create final approval by itself.

## 4. Primitive Failure Cards

Each primitive failure card must display:

- primitive ref or family;
- source evidence refs;
- expected activation;
- observed failure;
- related Matrix pass;
- related route or SceneSpec;
- approval blocker code when hard-failed;
- repair recommendation.

Failure examples:

- `primitive_evidence_missing`
- `primitive_coalition_collapsed`
- `edge_product_flattened`
- `anti_centroid_pressure_lost`
- `route_primitive_mismatch`
- `unsupported_primitive_ref`

## 5. PWA and Telegram Boundary

PWA owns complete evidence review. Telegram may show a compact status for low-risk review, but it must include preview, route, source snippet, consent, evaluation summary, required action, object version, and PWA link.

Complex evidence, hard failures, primitive failure expansion, and blocker repair stay in PWA.

