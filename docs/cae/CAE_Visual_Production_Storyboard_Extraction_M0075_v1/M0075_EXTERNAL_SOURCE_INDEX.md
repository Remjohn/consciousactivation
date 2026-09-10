# M0075 External Source Index

**Evidence class:** REGISTRY_SOURCE

## Jellyfish

Repository: `https://github.com/Forget-C/Jellyfish`

License file: `https://raw.githubusercontent.com/Forget-C/Jellyfish/main/LICENSE`

License: Apache-2.0. The current public repository describes the project as an end-to-end production workspace covering structured storyboarding, shot preparation, consistency management, video generation and export.

Current exact files inspected read-only through current raw-source endpoints:

| Exact path | Relevant symbols | CAE extraction use |
|---|---|---|
| `backend/app/services/studio/shot_preparation_state.py` | `build_shot_preparation_state`, `link_existing_asset_for_preparation` | readiness aggregate; reusable asset linking |
| `backend/app/services/studio/shot_extracted_candidates.py` | `replace_for_shot`, `mark_linked`, `mark_linked_by_name`, `mark_pending_by_name`, `mark_pending_by_linked_entity` | candidate refresh / confirmation lifecycle |
| `backend/app/services/studio/shot_assets.py` | `create_project_asset_link`, `list_shot_linked_assets` | reusable asset resolution and deterministic presentation |
| `backend/app/models/studio_shots.py` | `Shot`, `ShotCharacterLink`, `ShotExtractedCandidate`, `ShotFrameImage`, `ShotDialogLine` | shot/context/frame decomposition |
| `backend/app/services/studio/shots.py` | `_build_extraction_state` | explicit extraction lifecycle states |

### Source fidelity limitation

The exact 40-character commit SHA for the current `main` tip could not be verified from the execution environment. A current GitHub Actions page exposed the abbreviated reference `a967819`, but the bundle does not promote that abbreviation to an exact source commit. No upstream source was copied into CAE.

### Source behavior summary

The current Jellyfish repository README describes a flow of `script breakdown → shot preparation → candidate confirmation → shot ready → generation workspace`, including candidate accept/ignore, reusable character/scene/prop/costume context, and media preview/link/reuse. These are adopted only as bounded behavioral patterns.

## CAE sources

- `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py::EditorialStoryboardRecord`
- `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py::ContentCandidateRecord`
- `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py::EditorialDecisionReceiptRecord`
- `packages/ca_runtime/src/ca_runtime/preparation_graph_store.py::PreparationGraphStore`
- `packages/ca_runtime/src/ca_runtime/preparation_graph_store.py::GraphRevisionRecord`
- `packages/ca_runtime/src/ca_runtime/preparation_graph_store.py::StaleBaseRevisionError`
- `tests/phase4/test_m39_storyboard_semantic_compile.py`
- `tests/cae/test_m009_preparation_graph.py`
