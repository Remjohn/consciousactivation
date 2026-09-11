# M0088 — Evidence Receipt

## Scope
Typed, proposal-only Visual Chat over the existing Visual Asset Studio canonical projection.

## Implemented behavior
- Closed action vocabulary: EXPLAIN, FIND_ALTERNATIVES, REPLACE_SOURCE, REGENERATE_TRANSFORMATION, REGENERATE_BBOX_PROMPT, COMPOSITION_ALTERNATIVES, REDUCE_INTENSITY, MOVE_EMPHASIS, and PRESERVE_EVIDENCE.
- Deterministic classifier and content-addressed immutable proposal.
- Canonical revision/state-version binding and human/operator authorization.
- REPLACE_SOURCE fails closed to NEEDS_CANDIDATES without a governed candidate portfolio.
- COMPOSITION_ALTERNATIVES emits exactly three proposal operations.
- PRESERVE_EVIDENCE keeps source lineage and forbids semantic/source replacement.
- API persistence uses the existing repository object authority; no storyboard/VAE mutation or retrieval authority is introduced.
- Visual Asset Studio exposes typed shortcuts and proposal-only status in the existing chat surface.

## Verification
- `python -m pytest -q tests/api/test_visual_chat.py` — PASS (10/10).
- `python -m py_compile api/services/visual_chat.py api/routers/visual_studio.py` — PASS.
- Combined M0085/M0086/M0088/M0089 regression — PASS (47/47).
- Full web typecheck remains blocked by unrelated pre-existing repository errors; no new Visual Asset Studio errors were observed.

## Evidence classes
`SCHEMA`, `EXECUTABLE`, `TEST`, `OPERATOR_DECISION_REQUIRED`.

No external repository code was adopted. Final perceptual inspection and operator authorization remain required.
