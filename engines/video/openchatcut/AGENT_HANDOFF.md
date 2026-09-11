# AGENT_HANDOFF — M0094 Native OpenChatCut Storyboard Handoff and Bidirectional Inspection

## Status

`OPERATOR_DECISION_REQUIRED`

Implementation is complete within the allowed boundary. Focused verification passes. Final promotion is blocked because the uploaded source archive has no Git metadata (so the exact M0094 CAE commit SHA cannot be honestly supplied) and the real OpenChatCut runtime was not reachable from this execution environment.

## Decision / objective

Bind resolved CAE video-program output to the native OpenChatCut runtime while preserving CAE semantic authority, source/media hashes, timeline lineage, operator edits and human-resolution persistence. Prove one-way compile and safe bidirectional inspection/update boundaries.

## Brownfield findings

- Existing one-way adapter: `services/pipeline/src/cmf_pipeline/media/openchatcut.py` (`OpenChatCutRuntimeAdapter.handoff`).
- Existing canonical executable program: `VideoEditProgramService` and `video_edit_program.schema.json` under `services/pipeline/`.
- Existing format-specific storyboard authority: `packages/ca_runtime/src/ca_runtime/storyboard_programs.py` (`VideoStoryboardProgram`), consumed but not modified because it is outside the M0094 boundary.
- Existing operator/human persistence boundary: `api/services/human_resolution.py` (`compile_native_edit_program`, `apply_native_edit`, `commit_native_edit`), already covered by M0066 tests; not modified because it is outside the M0094 boundary.
- Existing one-way tests: `tests/phase6/test_m065_openchatcut_runtime.py`.
- Existing M0066 immutable human-resolution tests: `tests/cae/test_m066_human_resolution.py`.

## Files added / modified

### Modified

- `services/pipeline/src/cmf_pipeline/media/openchatcut.py`
  - Added deterministic native timeline inspection invariant `INV-VIDEO-RUNTIME-002`.
  - Added topology/timing/source-window/asset/text divergence classification.
  - Added operator-gated `ADJUST_TIMING` reconciliation request generation.
  - Added native inspection through a discarded manual edit session.
  - No direct runtime-to-CAE mutation is performed.

- `tests/phase6/test_m065_openchatcut_runtime.py`
  - Added deterministic replay, good-looking-but-wrong asset contrast, safe timing update boundary, topology divergence, runtime inspection/disposal, and missing-discard negative coverage.

### Added

- `engines/video/openchatcut/UPSTREAM_TO_CAE_MAPPING.md`
- `engines/video/openchatcut/AGENT_HANDOFF.md`
- `services/pipeline/evidence/M0094_IMPLEMENTATION_RECEIPT.json`
- `services/pipeline/evidence/M0094.patch`

## Rationale

The smallest compatible change was to extend the existing OpenChatCut adapter rather than create a second adapter or modify the canonical storyboard/human-resolution authorities. Native reads are treated as observations. Only a bounded timing delta can become a proposed CAE human-resolution action; no native edit is auto-promoted into canonical state.

## Evidence classes

- `EXECUTABLE`: existing and modified `OpenChatCutRuntimeAdapter`, existing M0065/M0066 paths.
- `SCHEMA`: existing `video_edit_program` contract and inspected OpenChatCut `read_timeline` / edit-session schemas.
- `TEST`: 33 focused CAE/M0065/M0066/M0080/M0092 tests pass.
- `DOCUMENT`: required authority and brownfield documents read from the archive; path substitutions recorded below.
- `OPERATOR_DECISION_REQUIRED`: real OpenChatCut runtime reachability and exact Git commit identity remain unproven.
- `HYPOTHESIS`: none promoted to an implementation claim.

## Exact upstream source and license evidence

Upstream source repository: `https://github.com/0xsline/OpenChatCut`

Observed application version/license from local vendored source:
- `engines/video/openchatcut/upstream/package.json`: version `0.2.14`, license `AGPL-3.0-or-later`.
- `engines/video/openchatcut/upstream/LICENSE`: AGPLv3 text.

Exact upstream symbols inspected:
- `server/external-agent/mcp.ts`
- `src/agent/external-tool-shape.ts`
- `src/agent/tools/schemas/core-tools.ts`
- `src/agent/tools/timeline-item-projection.ts`
- `src/agent/tools/schemas/edit-item-tools.ts`

Exact upstream commit/tag:
- Exact Git commit SHA is unavailable from the accessible metadata.
- Tag for `0.2.14` was not asserted because the accessible release metadata did not establish a matching immutable tag.

See `UPSTREAM_TO_CAE_MAPPING.md` for adopted and excluded behavior.

## Mandatory-reading path reconciliation

The archive does not contain these mandate paths verbatim:
- `docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/...`

Equivalent authoritative files were found at:
- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/...`

The constitution SHA exactly matches the precedence contract's pinned hash: `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b`.

Additional phase-owned references named by `services/pipeline/AGENTS.md` were present under `services/pipeline/`, while the repository-root `PHASE_08_START_HERE.md` and `CURRENT_PROJECT_STATUS.md` named by that local instruction were not present at the repository root. The pipeline-specific `CURRENT_PROJECT_STATUS.md` was read.

## Exact commands and observed results

1. Archive identity
   - `sha256sum /mnt/data/codebase_clean(4).zip`
   - Result: `39049c349f471e09d7ed7017a1fd962eaf97274831c9f712cd74d094465edce1`

2. Syntax verification
   - `python -m py_compile services/pipeline/src/cmf_pipeline/media/openchatcut.py tests/phase6/test_m065_openchatcut_runtime.py`
   - Result: PASS

3. Focused suite
   - `python -m pytest -p no:asyncio -q tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py tests/cae/test_m0080_storyboard_program_contracts.py tests/cae/test_m0092_final_hit_storyboard_validation.py`
   - Result: `33 passed, 16 warnings`
   - Warnings are pre-existing Pydantic V1 validator deprecations in `packages/ca_runtime/src/ca_runtime/storyboard_session.py`.

4. Native runtime reachability
   - `curl -i --max-time 3 -sS http://localhost:5199/api/external-mcp/mcp`
   - Result: exit `7`; `Failed to connect to localhost port 5199 ... Could not connect to server`.
   - This is real environment probing, not mock evidence.

## What the tests prove

- Existing M0065 compile/handoff behavior still passes.
- Native inspection is deterministic and replay-stable for the same timeline/program.
- A plausible wrong asset with correct timing is classified as blocking rather than accepted.
- Timing-only divergence can produce a human-resolution request, but `direct_runtime_write` is false and operator approval is required.
- Topology divergence fails closed.
- Runtime inspection requires `discard_edit_session` and disposes the inspection session.
- Existing M0066 tests prove canonical CAS, immutable human-resolution persistence and idempotent replay.

## What the tests do not prove

- They do not prove real OpenChatCut reachability in this sandbox.
- They do not prove production/native UI visual quality or operator perceptual acceptance.
- They do not prove an end-to-end live CAE Storyboard-to-OpenChatCut round trip against a running external desktop/server runtime.
- They do not establish an exact immutable upstream Git commit for the vendored source tree.
- Native `read_timeline` does not expose a CAE source SHA, so reverse inspection can preserve/verify CAE `source_media_sha256` only as the sovereign program hash, not as a runtime-reported native hash.

## Rollback

Rollback only the M0094 changes in the three changed/added paths above. Preserve the pre-existing M0065/M0066 adapter, receipts, source evidence, and rejected artifacts.

## Exact commit SHA

`UNAVAILABLE — uploaded source archive contains no .git directory or alternate exact current commit metadata.`

## Operator decision requested

Select exactly one:

- `APPROVE`
- `APPROVE-WITH-LIMITATIONS`
- `REJECT`

The recommended evidence-safe disposition is `APPROVE-WITH-LIMITATIONS` only if the operator accepts the runtime/commit limitations explicitly; otherwise `REJECT` until native reachability and immutable Git identity are established.

## Active checkout integration note

The archive status above describes the supplied handoff snapshot. In the active CAE checkout, M0094 was integrated over the existing OpenChatCut adapter and human-resolution boundary. The focused suite passed 33/33, source compilation passed, and a live probe of the configured localhost endpoint remained unreachable; this limitation is recorded in the updated evidence receipt.
