# M0091 — SuperVisual Composition Editor and Primitive Stack

## Outcome

Bounded implementation completed to the extent supportable by the supplied source snapshot. The implementation adds a governed SuperVisual editor/projection facade, exposes the four primitive roles in the existing Visual Asset Studio surface, and adds focused deterministic tests. No canonical semantic/state/provenance authority was duplicated.

Final disposition: **APPROVE-WITH-LIMITATIONS requested**.

## Evidence classes

- `EXECUTABLE` — `engines/visual/supervisual/editor.py`; deterministic proposal/review behavior.
- `EXECUTABLE` — `apps/web/src/components/visual-studio/SuperVisualPrimitiveStack.tsx`; visible primitive-role surface.
- `TEST` — `tests/cae/test_m0091_supervisual_editor.py`; 6 focused tests passed.
- `TEST` — `tests/api/test_visual_studio_pure.py`; existing pure Visual Studio tests passed.
- `DOCUMENT` — `engines/visual/supervisual/README.md`; binding and authority boundary.
- `REGISTRY_SOURCE` — `engines/visual/supervisual/UPSTREAM_TO_CAE_MAPPING.md`; upstream mapping and license posture.
- `OPERATOR_DECISION_REQUIRED` — source snapshot has no `.git`, so this execution cannot establish the exact CAE commit SHA or collision ownership.
- `OPERATOR_DECISION_REQUIRED` — Python baseline composition tests cannot collect because the supplied environment is missing `psycopg`; web dependencies are absent, so native React/Vite tests cannot run.

## Brownfield findings

Existing canonical CAE composition services were found at:

- `services/pipeline/src/cmf_pipeline/composition/geometry.py` — `BBox`, `GeometryValidator` (`EXECUTABLE`)
- `services/pipeline/src/cmf_pipeline/composition/pretext.py` — `PretextEngine` (`EXECUTABLE`)
- `services/pipeline/src/cmf_pipeline/composition/skia_renderer.py` — `SkiaStaticRenderer` (`EXECUTABLE`)
- `services/pipeline/src/cmf_pipeline/composition/ir.py` — `CompositionIRService` (`EXECUTABLE`)
- `services/pipeline/src/cmf_pipeline/composition/products.py` — `SuperVisualService` (`EXECUTABLE`)
- `packages/ca_runtime/src/ca_runtime/storyboard_programs.py` — `SuperVisualStoryboardProgram` (`EXECUTABLE`)
- `apps/web/src/components/visual-studio/VisualAssetStudio.tsx` — existing operator surface (`EXECUTABLE`)

The new editor uses `SuperVisualEditor.from_cae()` to bind to the existing CAE BBOX/Pretext/Skia services rather than creating competing implementations.

## Files added/modified

- `engines/visual/supervisual/__init__.py` — package export surface.
- `engines/visual/supervisual/editor.py` — bounded editor/projection facade; typed Rough Notation proposals, operator revisions, deterministic geometry review, and four-role projection.
- `engines/visual/supervisual/README.md` — implementation/authority boundary.
- `engines/visual/supervisual/UPSTREAM_TO_CAE_MAPPING.md` — upstream-to-CAE mapping, licenses, adopted/excluded behavior.
- `apps/web/src/components/visual-studio/SuperVisualPrimitiveStack.tsx` — visible BBOX / PRETEXT / SKIA / ROUGH_NOTATION stack surface.
- `apps/web/src/components/visual-studio/VisualAssetStudio.tsx` — adds primitive stack and typed annotation-proposal entry points; canonical state is not mutated directly.
- `apps/web/src/components/visual-studio/SuperVisualPrimitiveStack.test.tsx` — UI behavior tests (not runnable in supplied snapshot because `node_modules` is absent).
- `tests/cae/test_m0091_supervisual_editor.py` — focused engine tests.

## Exact commands and observed results

### Focused Python tests

Command:
`python -m pytest -q tests/cae/test_m0091_supervisual_editor.py tests/api/test_visual_studio_pure.py`

Observed:
`8 passed in 0.18s`

### Python syntax

Command:
`python -m py_compile engines/visual/supervisual/*.py tests/cae/test_m0091_supervisual_editor.py`

Observed:
`PY_COMPILE_PASS`

### Broad pre-existing composition/storystate test collection

Command:
`python -m pytest -q tests/phase6/test_composition_products.py tests/api/test_visual_studio_pure.py tests/cae/test_m0080_storyboard_program_contracts.py`

Observed blocker:
`ModuleNotFoundError: No module named 'psycopg'`

Interpretation: environment/dependency collection failure; not converted into a product failure claim.

### Web test

Command:
`cd apps/web && npm test -- --run src/components/visual-studio/SuperVisualPrimitiveStack.test.tsx`

Observed blocker:
`sh: 1: vitest: not found`

Interpretation: `apps/web/node_modules` is absent in the supplied snapshot.

### Web typecheck

Command:
`tsc -p apps/web/tsconfig.json --noEmit`

Observed blocker:
`TS2688: Cannot find type definition file for 'vite/client'`

Interpretation: installed dependency set is incomplete.

## Contrastive / negative coverage

- A visually plausible layer with no authoritative BBOX is rejected (`test_m0091_good_looking_but_wrong_layer_without_bbox_is_blocked`).
- Unauthorized model actors cannot create operator revisions.
- Deterministic revision identity is stable across replay.
- Geometry collision fails closed.
- Annotation proposals are typed and explicitly non-mutating.

## Upstream source verification

Current web-visible source evidence was inspected read-only:

- Pretext: `https://github.com/chenglou/pretext`, `src/layout.ts`; current main was web-visible at commit `ac49b09`; MIT. The current API separates preparation/measurement from layout arithmetic. Full 40-character SHA was not exposed in the accessible web evidence.
- Rough Notation: `https://github.com/rough-stuff/rough-notation`, `src/rough-notation.ts` and `README.md`; MIT. Public API includes `annotate()` and a bounded annotation type vocabulary. Exact current tip SHA was not exposed in the accessible history.
- Skia: `https://github.com/google/skia`, `include/core/SkCanvas.h`, `SkSurface.h`, `SkPaint.h`; BSD-3-Clause in source headers. Current main history exposed commit `b5465d7`; full 40-character SHA was not exposed.

No upstream source code was copied into CAE.

## Rollback / recovery

Rollback is limited to the listed added/modified files. No database migration, canonical state migration, or source-runtime replacement was introduced.

## Limitations

1. The supplied archive contains no `.git` directory. The historical M72 SHA `8fb3733cc6a750560532f87f98af2fe24c229528` is not substituted for the current mandate commit.
2. The literal mandatory authority paths requested by M0091 are absent, but exact current equivalents were found under `governance/program-control/00_CONSTITUTION/current-v1.1/`. This was treated as a relocated equivalent rather than creating new authority files.
3. The dated authority pack exists at `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/` rather than the literal `AUTHORITY_PACK/...` paths named by the mandate.
4. Native web tests/typecheck and broad Python composition tests are blocked by absent dependencies in the supplied snapshot.
5. The implementation proves deterministic editor/proposal behavior only. It does not prove external runtime availability, browser render fidelity, perceptual visual quality, or final semantic correctness.
6. Final visual acceptance still requires an operator to inspect the real preview, verify source lineage, and choose the final decision.

## Exact CAE commit SHA

`UNAVAILABLE_IN_SUPPLIED_SNAPSHOT`

## Operator decision requested

Please select exactly one:

`APPROVE` / `APPROVE-WITH-LIMITATIONS` / `REJECT`

Recommended evidence disposition: **APPROVE-WITH-LIMITATIONS**, pending execution in the real Git worktree with complete dependency installation and operator visual review.
