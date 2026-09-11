# M0094 — OpenChatCut upstream → CAE mapping

Evidence classes used below: `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`.

## Upstream identity

- Upstream: https://github.com/0xsline/OpenChatCut
- Observed upstream branch: `main`
- Observed upstream application version: `0.2.14` (`package.json`)
- License: `AGPL-3.0-or-later` (`package.json`, `LICENSE`)
- Exact upstream Git commit SHA: **UNAVAILABLE** from the accessible source checkout. The CAE archive contains a vendored source tree without `.git`, and network Git metadata was not available in the execution environment.
- Exact CAE repository commit SHA: **UNAVAILABLE** because the uploaded archive has no `.git` metadata. `docs/PRD/CURRENT.md` records historical M72 synchronization at `8fb3733cc6a750560532f87f98af2fe24c229528`; that is not asserted as the M0094 source commit.

## Adopted implementation behavior

| Upstream exact path / symbol | Evidence class | CAE adoption | Explicit exclusion |
|---|---|---|---|
| `server/external-agent/mcp.ts` — Streamable HTTP MCP handler and tool dispatch | EXECUTABLE | CAE continues to bind through Streamable HTTP MCP using `initialize`, `tools/list`, and `tools/call`; runtime identity remains downstream of CAE. | OpenChatCut session/project state is not semantic authority; no wholesale server extraction. |
| `src/agent/tools/schemas/core-tools.ts` — `read_timeline` | SCHEMA / EXECUTABLE | Native inspection consumes `fps`, track identity, item timing, media linkage and source-window fields exposed by the tool. | CAE does not inherit OpenChatCut's semantic meaning or tool registry as its contract authority. |
| `src/agent/tools/timeline-item-projection.ts` — `projectTimelineItem` | EXECUTABLE | Reverse inspection relies on `startFrame`, `durationInFrames`, `srcInFrame`, `sourceStartFrame`, `sourceDurationInFrames`, `sourceEndFrameExclusive`, `sourceAssetId`, and linkage status. | Unexposed or ambiguous native fields are not guessed or synthesized as CAE truth. |
| `src/agent/external-tool-shape.ts` — `begin_edit_session`, `get_edit_session`, `discard_edit_session` | SCHEMA / EXECUTABLE | Native inspection opens a manual edit session only to read state, then explicitly discards it. | No direct runtime-to-CAE mutation is performed. |
| `src/agent/tools/schemas/edit-item-tools.ts` — `edit_item` | SCHEMA | Existing M0065 handoff remains the one-way compiler path from CAE `VideoEditProgram` to native timeline. | Reverse edits do not call OpenChatCut `edit_item`; safe updates are converted into CAE human-resolution requests. |

## CAE canonical boundary

- Canonical semantic/program authority remains the existing `VideoStoryboardProgram` → `VideoEditProgram` path. The M0094 adapter does not create a second storyboard/program model.
- Canonical timeline authority remains `CANONICAL_VIDEO_EDIT_PROGRAM`.
- Native inspection is read-only and deterministic.
- Timing-only runtime divergence within the existing M0066 bound is emitted as an operator-gated `ADJUST_TIMING` request.
- Asset substitutions, item moves, topology changes, source-window divergence, invalid durations and unverifiable text are blocking and are not auto-applied.
- The update boundary explicitly routes through `api.services.human_resolution.compile_native_edit_program -> commit_native_edit`; M0094 does not modify that canonical service because it is outside the allowed file boundary.
- Source-media hash sovereignty remains CAE's `source_media_sha256`; OpenChatCut native timeline identity does not manufacture a native source hash.

## Excluded behavior

The following are deliberately not adopted into CAE authority: OpenChatCut semantic prompts/skills, external agent planning, OpenChatCut project state as canonical state, automatic promotion of native edits, runtime-specific visual meaning, or unsupported native metadata as identity.
