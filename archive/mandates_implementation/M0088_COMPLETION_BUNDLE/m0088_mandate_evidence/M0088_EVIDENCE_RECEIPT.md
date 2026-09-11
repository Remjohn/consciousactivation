# M0088 Evidence Receipt

## Status
`EXECUTABLE` implementation completed; `OPERATOR_DECISION_REQUIRED` for final promotion/acceptance.

## Evidence classes
- `SCHEMA`: `api/services/visual_chat.py` typed request/proposal models and bounded action enum.
- `EXECUTABLE`: `api/services/visual_chat.py`, `api/routers/visual_studio.py`, `apps/web/src/api/visualStudio.ts`, `apps/web/src/components/visual-studio/VisualAssetStudio.tsx`.
- `TEST`: `tests/api/test_visual_chat.py` — 5 passed.
- `DOCUMENT`: Visual Production authority pack under `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/`.
- `HYPOTHESIS`: none asserted as production evidence.
- `OPERATOR_DECISION_REQUIRED`: final visual inspection, acceptance/promotion, browser-runtime verification.

## Exact commands and observed results
1. `python -m pytest -q tests/api/test_visual_chat.py` → **5 passed in 0.04s**.
2. `python -m py_compile api/services/visual_chat.py api/routers/visual_studio.py` → **exit 0**.
3. `npm run build` in `apps/web/` → **blocked, exit 127: `vite: not found`**.
4. Broad legacy convergence tests were attempted; collection is blocked by **`ModuleNotFoundError: psycopg`** in the supplied environment. This is pre-existing environment/setup debt, not introduced by M0088.

## Covered properties
- Deterministic replay/idempotent proposal content.
- Human-operator authorization requirement.
- Canonical source-lineage requirement.
- Stale/current revision digest binding is enforced at the API route.
- Source replacement without a governed candidate set fails closed into `NEEDS_CANDIDATES`.
- Three composition alternatives preserve the same evidence and remain review-only.
- “Good-looking but wrong” presentation requests cannot swap source or rewrite semantic evidence when the request is in preserve-evidence mode.
- Chat emits proposals only; no chat endpoint directly mutates canonical storyboard/VAE state.

## Authority mapping
The supplied authority pack was used despite its path differing from the original mandate wording. Relevant sources:
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/07_PRODUCTION_OPERATOR_GATES/M72_final_production_gate_current_sync.md`

Key adopted rule: chat creates typed proposals; CAE validators and the operator decide application. Evidence-first order remains `RETRIEVE → TRANSFORM → COMPOSE → GENERATE` where justified.

## External source information
No external repository behavior was extracted or merged for M0088. No external source license/commit is therefore claimed as adopted behavior.

## Limitations
- The supplied archive has no upstream Git ancestry metadata. A local Git snapshot was created solely to provide an exact resulting commit identifier; it is **not** an assertion of the original upstream commit history.
- Frontend production build was not proven because `vite` is unavailable in the supplied environment.
- Full API/runtime import was not proven because `psycopg` is unavailable in the supplied environment.
- No real media preview was inspected in this environment; semantic/perceptual visual correctness remains an operator responsibility.
