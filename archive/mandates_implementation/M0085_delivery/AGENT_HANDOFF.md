# AGENT_HANDOFF — M0085 Evidence-First Visual Asset Studio

## Status
EXECUTED — OPERATOR REVIEW REQUIRED. No self-promotion performed.

## Exact commits
- Archive baseline commit: `91ef5adae9b53de32e504d566a8143cfeaf2c9f1`
- M0085 implementation commit: `9ba3b0e684f602bb4ef8e0a08444e4ddf14cebbc`
- Current upstream reference inspected: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`

The uploaded archive had no usable pre-existing Git history, so the first SHA is a local immutable archive-baseline commit and the second is the exact bounded M0085 change commit derived from it. The upstream SHA is a source-reference, not the M0085 implementation SHA.

## Authority audit
Mandatory authority materials were read from their current repository locations. Two literal mandate paths were not present at repository root and were resolved to the current equivalent hierarchy:
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`

The visual-production authority pack is present under `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/`.

No authority was moved or rewritten.

## Brownfield decision
The archive already contained the backend Studio bridge and consumers but was missing the `services/studio` implementation referenced by the bridge, frontend alias and API types. Existing canonical storyboard/timeline state was reused; no second storyboard/VAE state model was introduced.

The implementation therefore repairs the existing `services/studio` seam with a small CAE-native package and adds only the bounded Visual Asset Studio route/UI surface.

## Implemented behavior
- Evidence/source panel with canonical source reference and SHA display.
- Real video playback only when a canonical artifact with a browser-reachable video URI exists; no mock preview fallback.
- Composition canvas as a canonical timeline projection. The UI explicitly labels it as a projection, not render-proof semantics.
- Layer inspector with source range, lineage, editable operations and validation state.
- Transform controls for move/resize/trim that compile deterministic proposal programs; they do not directly mutate canonical state.
- Keyframe inspection when keyframes exist in the canonical timeline/motion-plan projection; otherwise explicit non-observation state is shown.
- Visual Chat produces typed `ChangeRequestProgram` proposals only.
- GOOD / NEEDS_EDIT / REJECT feedback is stored as immutable `studio_visual_feedback` content-addressed objects against the current canonical revision.
- REGENERATE is a governed prompt affordance, not an automatic generation bypass.
- COMPILE remains review-oriented; this foundation does not promote or execute a visual proposal directly.
- Studio RPC has fail-closed missing-entrypoint, timeout and malformed-JSON handling.
- Studio health explicitly reports `candidate_not_current`, `production_authorized=false`, `certified=false`.

## Changed/new repository paths
See `CHANGED_PATHS.txt` for the exact Git name-status list. Material paths are:

- `api/main.py`
- `api/routers/visual_studio.py`
- `api/services/studio_bridge.py`
- `api/services/visual_studio_contracts.py`
- `apps/web/src/api/visualStudio.ts`
- `apps/web/src/components/visual-studio/VisualAssetStudio.tsx`
- `apps/web/src/pages/CampaignDetail.tsx`
- `services/studio/package.json`
- `services/studio/tsconfig.json`
- `services/studio/src/*`
- `services/studio/src/generated/contracts.ts`
- `services/studio/dist/*`
- `tests/api/test_studio_bridge.py`
- `tests/api/test_visual_studio_pure.py`

Generated `services/studio/dist/*` is intentionally included because the existing API bridge is configured to execute that built entrypoint and the mandate requires an executable handoff.

## Tests and exact commands
1. Contract byte identity:
`cmp -s services/studio/src/generated/contracts.ts governance/program-control/02_CROSS_REPO_CONTRACTS/activative-production-spine/0.1.0-dev.1/generated/typescript/contracts.ts`
Observed: `contracts-byte-identical`.

2. Studio build + health:
`cd services/studio && tsc -p tsconfig.json --pretty false && node dist/index.js health --json`
Observed: build succeeded; health reported candidate-not-current, development authorized, production unauthorized, not certified.

3. Focused tests:
`python -m pytest tests/api/test_visual_studio_pure.py tests/api/test_studio_bridge.py tests/phase1/test_studio.py -q`
Observed: `8 passed in 0.44s`.

4. API syntax:
`python -m py_compile api/routers/visual_studio.py api/services/visual_studio_contracts.py`
Observed: `python-api-syntax-ok`.

5. Deterministic replay:
The same natural-language compile RPC input was executed twice and stdout compared with `cmp`.
Observed: `replay-identical` and identical deterministic program identifiers/hashes.

6. Negative stale/authorization proofs:
- stale state => `STALE_STATE_VERSION`
- model actor => `OPERATOR_REQUIRED`

7. Good-looking-but-wrong counterexample:
A selected layer with no source lineage is reported `source_lineage=BLOCKED` and `semantic_correctness=OPERATOR_REVIEW_REQUIRED`; the UI does not invent a source or substitute a mock artifact.

8. Bridge fail-closed proofs:
Focused bridge tests cover missing entrypoint, timeout, malformed JSON and normal RPC success.

## External/upstream reference
Repository consulted: `https://github.com/Remjohn/consciousactivation`
Reference commit: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`
Exact paths inspected:
- `services/studio/src/domain.ts`
- `services/studio/src/revision.ts`
- `services/studio/src/timeline.ts`

No external repository code was copied/adopted. No root LICENSE was found at the consulted upstream path, so no external license was asserted. See `evidence/M0085_UPSTREAM_REFERENCE.md`.

## Evidence class summary
- `EXECUTABLE`: Studio build, health, RPC happy paths.
- `SCHEMA`: generated release contract byte identity; RPC response compatibility with the live Python bridge.
- `DOCUMENT`: constitutional/current PRD/M72 and Visual Production authority materials.
- `TEST`: focused Python suite, replay/idempotence, stale/unauthorized, bridge fail-closed.
- `REGISTRY_SOURCE`: upstream source-file inspection and repository-reference record.
- `HYPOTHESIS`: schematic composition canvas is a projection and is not evidence of rendered visual semantics.
- `OPERATOR_DECISION_REQUIRED`: perceptual quality, semantic correctness, real preview/media lineage, and any production promotion.

## Limitations / non-claims
- Full frontend verification could not be established because the uploaded archive contains incomplete Node dependencies; missing `vite/client` types and placeholder React/TanStack packages prevented a meaningful whole-web typecheck.
- The broader Python API suite was not claimed green because `psycopg` is missing in the environment.
- No real campaign video artifact was available for browser playback/render proof.
- Source quality and geometry remain `NOT_OBSERVED`; semantic correctness remains operator review.
- No external runtime reachability or native render fidelity was established.

## Rollback / recovery
Revert only commit `9ba3b0e684f602bb4ef8e0a08444e4ddf14cebbc` or use `M0085.patch`. Preserve all pre-existing archive changes and source evidence. Because `services/studio/dist` is an executable handoff artifact, rebuild it from `services/studio/src` after any source modification.

## Operator decision requested
Select exactly one:

`APPROVE`

`APPROVE-WITH-LIMITATIONS`

`REJECT`

For approval, inspect the real Visual Asset Studio preview, confirm source lineage, assess that transformation serves meaning without gratuitous attention, and verify that downstream runtime remains subordinate to CAE authority and independently replaceable.
