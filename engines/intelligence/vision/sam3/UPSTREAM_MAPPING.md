# M0090 SAM3 upstream → CAE mapping

**Evidence class:** `REGISTRY_SOURCE` for the external runtime mapping; `DOCUMENT` for the CAE scope interpretation.

## Pinned upstream source

- Repository: `https://github.com/facebookresearch/sam3`
- Source commit: `660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7`
- License file: `LICENSE`
- License: **SAM License**, last updated 2025-11-19.
- Pinned upstream files inspected:
  - `sam3/model/sam3_base_predictor.py`
  - `sam3/model/sam3_video_predictor.py`
  - `sam3/model/sam3_tracking_predictor.py`

## Exact source URLs

- `sam3/model/sam3_base_predictor.py`: `https://github.com/facebookresearch/sam3/blob/660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7/sam3/model/sam3_base_predictor.py`
- `sam3/model/sam3_video_predictor.py`: `https://github.com/facebookresearch/sam3/blob/660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7/sam3/model/sam3_video_predictor.py`
- `sam3/model/sam3_tracking_predictor.py`: `https://github.com/facebookresearch/sam3/blob/660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7/sam3/model/sam3_tracking_predictor.py`
- `LICENSE`: `https://github.com/facebookresearch/sam3/blob/660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7/LICENSE`

No upstream release tag was claimed; the behavior is pinned directly to the exact source commit above.

## Adopted behavior

| Upstream behavior | CAE adoption | CAE owner |
|---|---|---|
| Video inference session lifecycle | Runtime-local state only; CAE session remains canonical | `Sam3TrackingAdapter` |
| Point prompting | Operator `TrackingPrompt(kind=POINT)` → SAM3 point prompt | CAE validates prompt/provenance |
| Box prompting | Operator `TrackingPrompt(kind=BOX)` → SAM3 relative box | CAE validates geometry |
| Mask prompting | Operator `TrackingPrompt(kind=MASK)` → `add_new_mask()` with resolved immutable artifact | CAE owns mask reference and source lineage |
| Interactive correction | New CAE revision with a new prompt/segment payload | `TrackingSessionStore` |
| Video propagation | SAM3 `propagate_in_video()` output → frame geometry | CAE validates source hashes/confidence/gaps |
| Multi-object runtime slots | One selected CAE target maps to runtime object id `1` within an isolated SAM3 state | CAE target remains authoritative |

## Face-seed interpretation

SAM3's inspected tracker surface accepts geometric point/box prompts; CAE therefore treats **FACE** as an operator selection record (`face_ref`) plus its geometric box or point. No face identity embedding or semantic speaker decision is delegated to SAM3.

## Explicit exclusions

- No SAM3 source code or model weights are vendored into CAE.
- No SAM3 README, model output, or prompt text is treated as CAE semantic identity authority.
- No external tracker state is used as the canonical CAE revision/state store.
- No automatic promotion of a high-confidence track is allowed; operator feedback is required.
- No native CUDA/checkpoint execution is claimed by this artifact. Native runtime reachability remains an environment-fidelity requirement.
