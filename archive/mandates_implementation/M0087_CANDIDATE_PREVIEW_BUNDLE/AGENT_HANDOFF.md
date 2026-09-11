# AGENT_HANDOFF — M0087 Candidate Preview, Swipe Selection and Governed Promotion

## Status
EXECUTED AS BOUNDED IMPLEMENTATION — OPERATOR REVIEW REQUIRED.

## Objective delivered
Implemented a CAE-native candidate preview/selection projection over authoritative retrieval candidates. The implementation provides immutable candidate portfolio snapshots, playable preview metadata, previous/next navigation, touch/keyboard inspection, human accept/reject decisions, deterministic gated auto-acceptance, rejection lineage, source provenance receipts, search-again session replacement, and promotion through the existing canonical `SUBSTITUTE_ASSET` native edit path.

No second retrieval system or competing storyboard/VAE authority was introduced. Candidate data must come from the upstream retrieval path; the UI does not synthesize mock candidates.

## Brownfield / authority mapping
- `EXECUTABLE`: `services/asset-intelligence/src/cae_asset_intelligence/candidate_preview.py` — M0087 session/portfolio/receipt state machine and deterministic policy.
- `EXECUTABLE`: `api/routers/candidate_preview.py` — governed API persistence and promotion boundary.
- `EXECUTABLE`: `apps/web/src/components/visual-studio/CandidatePreviewPanel.tsx` — candidate inspection/selection UI; playable media only when a real preview URI is supplied.
- `EXECUTABLE`: `apps/web/src/api/candidatePreview.ts` — client contract.
- `EXECUTABLE`: `apps/web/src/components/visual-studio/VisualAssetStudio.tsx` — embeds candidate preview into the existing Studio surface.
- `REGISTRY_SOURCE`: current CAE retrieval behavior from `services/asset-intelligence/src/cae_asset_intelligence/retrieval.py`; no external code adopted.
- `EXECUTABLE`: current CAE native edit/promotion behavior from `api/services/human_resolution.py` via `SUBSTITUTE_ASSET`.

## Exact changed/new paths
- `api/main.py`
- `api/routers/candidate_preview.py`
- `services/asset-intelligence/src/cae_asset_intelligence/candidate_preview.py`
- `services/asset-intelligence/src/cae_asset_intelligence/__init__.py`
- `apps/web/src/api/candidatePreview.ts`
- `apps/web/src/components/visual-studio/CandidatePreviewPanel.tsx`
- `apps/web/src/components/visual-studio/VisualAssetStudio.tsx`
- `tests/asset_intelligence/test_m0087_candidate_preview.py`
- `tests/api/test_candidate_preview.py`

## Contract behavior
- Candidate card requires source object/version/SHA, source interval, rights state, ranking, confidence, semantic fit, quality, eligibility, provenance, transcript/context, and preview URI when available.
- Automatic acceptance is registered under `visual-candidate-auto-accept-v1` and requires eligibility, confidence >= 9000 bps, semantic fit >= 9000 bps, cleared rights, complete provenance including scene id, and quality >= 8000 bps.
- Human accept/reject requires an operator actor. Rejection requires rationale. Rejected candidates remain in the session receipt lineage and cannot be silently re-accepted without a new search.
- Candidate session revisions are optimistic-concurrency guarded. Decision receipts are content-addressed and include request, candidate set, selected/rejected snapshots, actor/policy, source identity/range, rights, storyboard target, and canonical campaign revision reference.
- Promotion requires a human operator and uses the existing canonical campaign/VAE-native `SUBSTITUTE_ASSET` path rather than directly mutating state.

## Tests / exact commands / results
### PASS
`python -m pytest -q tests/asset_intelligence/test_m0087_candidate_preview.py tests/api/test_visual_studio_pure.py tests/asset_intelligence/test_cinematic_retrieval_m063.py tests/production_program/test_m0064_asset_selection_binding_lineage.py`

Observed: **35 passed in 0.47s**.

`python -m py_compile api/routers/candidate_preview.py services/asset-intelligence/src/cae_asset_intelligence/candidate_preview.py`
Observed: PASS.

`python -m compileall -q api/routers/candidate_preview.py services/asset-intelligence/src/cae_asset_intelligence/candidate_preview.py services/asset-intelligence/src/cae_asset_intelligence/__init__.py`
Observed: PASS.

### BLOCKED / limitation
`python -m pytest -q tests/api/test_candidate_preview.py`
Observed: collection blocked by `ModuleNotFoundError: No module named 'psycopg'`. This prevents honest API integration proof in the supplied environment.

`tsc -p apps/web/tsconfig.json --noEmit`
Observed: blocked by `TS2688: Cannot find type definition file for 'vite/client'`; the supplied source snapshot has no `apps/web/node_modules`.

M0079/M0080 full runtime tests were also not executable in this environment for the same missing `psycopg` dependency; the pre-existing focused M0063/M0064/M0087 suite remained green.

## Contrastive / negative coverage
- Good-looking but semantically wrong candidate: deterministic auto-accept blocks on low semantic-fit score.
- Restricted-rights candidate: automatic acceptance blocks.
- Non-operator decision: blocked.
- Stale candidate session version: blocked.
- Missing candidate id: blocked.
- Malformed provenance: blocked by model validation.
- Rejected candidate re-acceptance without search-again: blocked.
- Canonical receipt stability/idempotent hashing: tested.

## External source information
No external repository content was cloned, extracted, vendored, or copied into this change. Therefore external source commit/license adoption is **N/A**.

Current upstream CAE `main` source inspected for brownfield alignment at commit:
`1238dda04cc89e16ed7ac96ac79417c7c321f8a8`.

The supplied zip omits `.git`, so an implementation commit SHA for this working tree **cannot be truthfully supplied**. The bundle contains a unified patch and changed-file SHA-256 manifest instead.

## Evidence files
- `evidence/M0087_EVIDENCE_RECEIPT.json`
- `evidence/changed_file_sha256.json`
- `M0087.patch`

## Limitations
1. API integration tests could not execute because `psycopg` is unavailable.
2. Browser TypeScript verification could not execute because Vite/React dependencies are not installed in the supplied snapshot.
3. No real retrieval session was present in the snapshot to prove media-byte playback against a live source. The UI is explicitly fail-closed when no real playable URI is supplied.
4. A local implementation commit SHA is unavailable because the archive has no Git metadata.
5. Visual semantic quality and final creative judgment remain operator validation requirements; a passing policy/test does not establish perceptual correctness.

## Rollback / recovery
Rollback only the nine listed changed paths. Do not delete or mutate existing source receipts or rejected candidate artifacts. Because no migration was introduced, no database migration rollback is required. Disable the candidate preview surface at its route/component boundary if runtime verification fails.

## Operator decision requested
**APPROVE / APPROVE-WITH-LIMITATIONS / REJECT**

Operator must inspect the actual candidate previews and provenance, confirm the selected candidate serves the intended semantic need without gratuitous attention, and verify promotion remains downstream of CAE canonical state.
