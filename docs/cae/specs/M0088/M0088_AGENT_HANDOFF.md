# AGENT_HANDOFF — M0088 Visual Chat and Typed Composition Proposal Interface

## Decision state
`OPERATOR_DECISION_REQUIRED`

Requested operator decision: `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.

## Implementation summary
M0088 is implemented as a bounded Visual Chat proposal surface over the existing canonical Visual Asset Studio projection. Chat classification is deterministic and bounded. Proposals are immutable records bound to the current canonical revision digest and state version. The new chat route does not directly mutate storyboard/VAE state or bypass validators/promotion gates.

Supported typed actions:
`EXPLAIN`, `FIND_ALTERNATIVES`, `REPLACE_SOURCE`, `REGENERATE_TRANSFORMATION`, `REGENERATE_BBOX_PROMPT`, `COMPOSITION_ALTERNATIVES`, `REDUCE_INTENSITY`, `MOVE_EMPHASIS`, `PRESERVE_EVIDENCE`.

Source replacement without an eligible governed candidate set is explicitly held in `NEEDS_CANDIDATES`. Three composition alternatives are emitted as proposals only. Rejected candidates are not silently promoted.

## Files added/modified
- `api/services/visual_chat.py` — added bounded typed Visual Chat compiler and immutable proposal model.
- `api/routers/visual_studio.py` — added `/campaigns/{campaign_id}/chat/proposals` route with operator, stale-version, canonical revision identity and digest checks; persists proposal objects.
- `apps/web/src/api/visualStudio.ts` — added typed client contract and request call.
- `apps/web/src/components/visual-studio/VisualAssetStudio.tsx` — wired the existing Studio chat surface to typed proposals and added bounded operation shortcuts.
- `tests/api/test_visual_chat.py` — focused positive, negative, replay and good-looking-but-wrong coverage.

## Rationale
The repository already had canonical storyboard/VAE projections, immutable operator feedback, stale-state checks, and direct transformation proposal infrastructure. M0088 therefore extends those existing seams instead of introducing a duplicate storyboard, VAE state model, retrieval system, or semantic authority.

## Exact commands/results
- `python -m pytest -q tests/api/test_visual_chat.py` → **5 passed**.
- `python -m py_compile api/services/visual_chat.py api/routers/visual_studio.py` → **pass**.
- `npm run build` in `apps/web/` → **blocked: `vite: not found`**.
- Broad legacy test collection → **blocked by missing `psycopg` dependency** in supplied environment.

## Verification properties
- happy path: typed proposal generation for all supported classes.
- contrastive wrong case: preserve-evidence request explicitly prohibits source swap and semantic rewrite.
- negative authorization: non-human/non-operator actor is rejected by schema validation.
- lineage: missing canonical source, target mismatch and stale/digest mismatch fail closed.
- replay: identical request produces identical proposal digest and operations.

## Evidence classes
`EXECUTABLE`, `SCHEMA`, `TEST`, `DOCUMENT`, `OPERATOR_DECISION_REQUIRED`.

## External source / license
No external repository code was extracted or adopted in M0088. Existing CAE native behavior was extended only.

## Commit
`24a5d89050a68ff20e885b554d859785b065e9aa`

This is a newly created local Git snapshot commit because the supplied archive contained no Git metadata. It is an exact identifier for the completed supplied snapshot, not an upstream-history claim.

## Limitations / acceptance ceiling
The implementation is proposal-only and intentionally does not self-promote. Full browser build and full API runtime proof require the environment dependencies `vite` and `psycopg`. Real preview inspection, perceptual quality, source fitness and final creative judgment remain operator evidence. A green focused unit suite does not establish those properties.

## Operator decision requested
`APPROVE` / `APPROVE-WITH-LIMITATIONS` / `REJECT`
