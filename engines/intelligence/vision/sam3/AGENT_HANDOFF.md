# M0090 — SAM3 Visual Tracking Session — Agent Handoff

**Operator decision requested:** `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.

## Scope outcome

Implemented the smallest bounded CAE tracking layer needed to make SAM3 a downstream, operator-controlled visual-intelligence capability without moving semantic identity authority into SAM3 or OpenChatCut.

### Added files

- `packages/ca_runtime/src/ca_runtime/tracking_session.py`
- `engines/intelligence/vision/sam3/adapter.py`
- `engines/intelligence/vision/sam3/UPSTREAM_MAPPING.md`
- `engines/intelligence/vision/sam3/AGENT_HANDOFF.md`
- `tests/cae/test_m0090_sam3_tracking_session.py`
- `engines/intelligence/vision/sam3/evidence/M0090_IMPLEMENTATION_RECEIPT.json`

## Canonical objects

`TrackingSession`, `TrackingTarget`, `TrackingPrompt`, `TrackSegment`, `TrackRevision`, `TrackingFeedback`, and `TrackingTransitionReceipt` are first-class CAE runtime objects. The session stores a `canonical_context_ref`, source URI/media hash, source dimensions/rate, selected target, latest revision, and fail-closed status. Revisions are immutable candidate records; operator feedback is append-only. Accepted geometry is projected to Storyboard/BBOX normalized geometry and deterministic OpenChatCut pixel regions.

## Authority/state controls

- Operator authority is injected through an existing CAE-owned authorization callback; this module does not create a second identity/permission authority.
- Revision writes use an SQLite compare-and-set condition on `latest_revision_id` and fail closed on stale writers.
- Every mutation receipt names actor, operation, precondition revision, postcondition revision/status, validator result, error route, and recovery path.
- A track cannot be projected to downstream consumers until the current revision has explicit operator `GOOD` feedback.
- `NEEDS_EDIT` and `REJECT` preserve the candidate revision in `PROPOSED` state and append immutable feedback; session status records the operator disposition.

## External upstream mapping

Pinned SAM3 source: `facebookresearch/sam3` at `660a5e9e1b8b4c02c0ad97229b88a09a6e4ff5b7`.

Inspected exact source files:
- `sam3/model/sam3_base_predictor.py`
- `sam3/model/sam3_video_predictor.py`
- `sam3/model/sam3_tracking_predictor.py`
- `LICENSE`

License: **SAM License**, last updated 2025-11-19. The license is recorded as source-available/custom and redistribution/use remains subject to its stated terms. CAE does not vendor or redistribute SAM3 source/weights in this change.

## Tests / evidence

The focused M0090 test suite covers:
- successful operator session → seed → propose → `GOOD` → consumer projection;
- high-confidence but wrong target mutation is rejected without promotion;
- unauthorized operator mutation fails closed;
- stale revision write fails closed with no extra revision;
- malformed source hash / geometry is rejected;
- missing source-frame hash is rejected by the runtime adapter;
- identical idempotent replay returns the same immutable revision;
- feedback remains append-only and rejected candidates remain inspectable;
- consumer projection is blocked before explicit operator acceptance;
- native SAM3 dependency is not imported implicitly by the CAE domain.

## Environment fidelity / limitations

1. The uploaded repository snapshot is not a Git checkout, so its original upstream CAE commit cannot be proven from `.git` metadata. The visible CURRENT/M72 records identify `8fb3733cc6a750560532f87f98af2fe24c229528` as the M72 documentation synchronization commit, but this archive does not contain that Git history.
2. Native SAM3 execution was **not** claimed or proved. The current upstream repository requires a CUDA-capable environment and authenticated checkpoints; this test run only proves CAE-side contracts and the replaceable runtime adapter boundary.
3. No API router/UI change was made because the mandate's allowed boundary does not include `api/` and the existing Studio gateway needs a separately authorized cross-boundary change. Operator control is fully represented in the domain contract, but the browser control surface is not wired by this bounded change. No separate SuperVisual adapter was added because no pre-existing governed tracking input contract was found within the allowed boundary; the accepted normalized Storyboard/BBOX geometry is the downstream composition handoff.
4. Perceptual correctness and target identity remain operator decisions. A visually plausible or high-confidence track is not semantic proof.
5. Full repository regression is not a M0090 acceptance claim; only the focused M0090 suite and import/type checks are evidence here.

## Exact commands/results

- `python -m py_compile packages/ca_runtime/src/ca_runtime/tracking_session.py engines/intelligence/vision/sam3/adapter.py tests/cae/test_m0090_sam3_tracking_session.py` → PASS
- `PYTHONPATH=packages/ca_runtime/src:. python -m pytest -p no:asyncio tests/cae/test_m0090_sam3_tracking_session.py -q` → PASS, 10 passed
- `python scratch/run_single_test.py tests/cae/test_m0090_sam3_tracking_session.py` → PASS, 10 passed
- Native environment probe → `sam3` not installed; `torch 2.10.0+cpu`; CUDA unavailable

Machine-readable receipt: `engines/intelligence/vision/sam3/evidence/M0090_IMPLEMENTATION_RECEIPT.json`.

## Exact implementation commit

`3da928a0c7e79aca4a84995400aad55147865b60` — local M0090 implementation commit. The uploaded snapshot has no original Git history; this SHA is evidence provenance, not a claim about the upstream CAE branch.
