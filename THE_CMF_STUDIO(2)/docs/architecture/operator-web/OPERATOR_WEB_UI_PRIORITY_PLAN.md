# Operator Web UI Priority Plan

This plan ranks next UI/backend wiring work based on the current audit. It is intentionally conservative: extend existing screens first, add screen-shaped read models second, and avoid duplicate UI.

## Priority 1

| Work Item | Why First | Existing Owner | Recommended Form | Notes |
|---|---|---|---|---|
| Video Timeline Workbench backend source rollout | Screen, client, fixture fallback, backend route, and read model already exist. | `VideoTimelineWorkbench.jsx`, `videoTimeline.js`, `VideoTimelineWorkbenchService` | prompt | Verify router mounting and environment flag behavior. This is the shortest path from fixture to backend. |
| Pipeline Run Monitor / Golden Path visibility | Pipeline screen exists but is fixture-only; Golden Path backend exists. | inline `PipelineView`, orchestration and Golden Path services | prompt + small backend route bundle | Add run/get/read model endpoint and extend existing Pipeline view. |
| Client Workspace / Artifact Store visibility | Workspace/artifact backbone exists but has no UI/API route. | `GuestWorkspace`, workspace/artifact services | bundle | Add safe read-only workspace/artifact routes before building upload flows. |

## Priority 2

| Work Item | Why | Existing Owner | Recommended Form | Notes |
|---|---|---|---|---|
| Reference Library upload/register/approve | Needed before provider and asset-heavy workflows. | source ingestion, artifact store, review services | prompt + bundle | Should extend Workspace/Guest area or add a subview, not a disconnected app. |
| Capability Preflight / Provider Menu view | Needed before real provider/render execution. | capability preflight services | prompt + bundle | Backend services exist; add route and UI panel. |
| Template Atlas preview | Helpful before template production and render queue work. | template migration/render contracts | bundle | Needs read model/product decision. |

## Priority 3

| Work Item | Why | Existing Owner | Recommended Form | Notes |
|---|---|---|---|---|
| Avatar 64-state Library Builder | Backend acting/avatar contracts exist; UI absent. | acting library/avatar performance services | bundle | Keep no-lipsync laws visible in read model. |
| Provider job sample approval | Provider jobs routes exist; UI absent. | provider operations/recovery services | prompt + bundle | Should depend on Capability Preflight UI. |
| Local Render Worker dashboard | Useful after fake render path stabilizes. | render/GPU worker services | bundle | Avoid real render calls in initial UI. |

## Priority 4

| Work Item | Why Later | Existing Owner | Recommended Form | Notes |
|---|---|---|---|---|
| Full video workbench editing | The base workbench exists; deeper editing should follow backend source rollout. | Timeline Workbench | prompt | Keep fixture fallback. |
| Real render queue | Requires capability preflight, local worker, and safety policies. | render worker services | bundle | Do not wire real Remotion/FFmpeg before preflight. |
| Advanced template editor | Needs Template Atlas and approval/versioning first. | template services | bundle | Avoid building before template read model exists. |

## Recommended Next Implementation Prompt

`PROMPT_02_CONNECT_VIDEO_TIMELINE_WORKBENCH_BACKEND` remains the cleanest next implementation target if it has not already been fully served from an app-mounted API. If it has already landed, the next highest-value prompt is:

`PROMPT_CONNECT_PIPELINE_AND_GOLDEN_PATH_RUN_MONITOR_V1`

Goal: extend the existing `PipelineView` with Golden Path / OrchestrationRun read models while preserving `data.js` fallback.
