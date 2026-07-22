# Operator Web Missing Backend Endpoints

This file groups endpoint gaps by feature area. Some backend services/contracts already exist; the gap is often a screen-shaped read model route rather than core domain logic.

## Client Workspace

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| POST `/api/v1/workspaces` create workspace | high | Guests/Workspace evolution | `ClientWorkspaceService` | `ClientWorkspace` | API route design | Client Workspace UI/backend wiring prompt |
| GET `/api/v1/workspaces` list workspaces | high | Workspace selector | `ClientWorkspaceService` | workspace summary list | API route design | Client Workspace UI/backend wiring prompt |
| GET `/api/v1/workspaces/{workspace_id}` | high | Workspace detail | `ClientWorkspaceService` | workspace detail | API route design | Client Workspace UI/backend wiring prompt |
| POST `/api/v1/workspaces/{workspace_id}/materialize` | medium | Setup/status | `ClientWorkspaceService` | `WorkspaceMaterializationReceipt` | path policy/read model | Client Workspace UI/backend wiring prompt |
| GET `/api/v1/workspaces/{workspace_id}/artifacts` | high | Artifact browser | `ArtifactStoreService`, `ArtifactManifestService` | artifact list/read model | workspace IDs and manifest policy | Artifact Browser prompt |
| POST `/api/v1/workspaces/{workspace_id}/references` | high | Reference upload/register | `ArtifactStoreService`, source ingestion | reference artifact receipt | upload policy | Reference Library prompt |

## References

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| POST `/api/v1/references/register` | high | Reference Library | source ingestion + artifact store | `ArtifactRef`, source receipt | workspace route | Reference Library prompt |
| POST `/api/v1/references/{reference_id}/approve` | medium | Approval workflow | review/approval services | approval receipt | review decision model | Reference Library prompt |
| POST `/api/v1/references/{reference_id}/reject` | medium | Approval workflow | review services | rejection receipt | review decision model | Reference Library prompt |
| POST `/api/v1/references/{reference_id}/tags` | medium | Organization/search | artifact metadata service | tag receipt | tag schema | Reference Library prompt |
| GET `/api/v1/references` | high | List/search | source/artifact services | reference read model | workspace scoping | Reference Library prompt |

## Pipeline

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| GET `/api/v1/pipeline-runs` | high | Pipeline screen | Orchestration / Golden Path services | pipeline run summary | run persistence/read model | Pipeline Run Monitor prompt |
| GET `/api/v1/pipeline-runs/{run_id}` | high | Pipeline detail | Orchestration service | run detail with stages | run persistence | Pipeline Run Monitor prompt |
| GET `/api/v1/pipeline-runs/{run_id}/stage-receipts` | high | Stage visibility | Orchestration service | stage receipt list | stage receipt mapping | Pipeline Run Monitor prompt |
| POST `/api/v1/pipeline-runs/{run_id}/gates/{gate_id}/approve` | medium | Gate action | approval/orchestration services | approval receipt | gate model | Pipeline Run Monitor prompt |
| POST `/api/v1/pipeline-runs/{run_id}/steps/{step_id}/retry` | medium | Recovery action | workflow recovery/orchestration | recovery receipt | retry policy | Pipeline Run Monitor prompt |

## Golden Path

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| POST `/api/v1/golden-path/format02/run` | high | Demo/Golden Path visibility | `Format02GoldenPathOrchestratorService` | run receipt/read model | API route policy | Golden Path Run API/UI prompt |
| GET `/api/v1/golden-path/runs/{run_id}` | high | Run detail | Golden Path repository/service | `GoldenPathRun` read model | repository access | Golden Path Run API/UI prompt |
| GET `/api/v1/golden-path/runs/{run_id}/output` | high | Output preview | Golden Path service | `Format02GoldenPathOutput` summary | output read model | Golden Path Run API/UI prompt |

## Capability Preflight

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| POST `/api/v1/capability-preflight/run` | high | Provider/readiness screen | `CapabilityPreflightService` | `CapabilityPreflightReport` | API route | Capability Preflight UI prompt |
| GET `/api/v1/capability-preflight/provider-menu` | high | Provider Menu | `ProviderMenuService` | `ProviderMenuSummary` | runtime config policy | Capability Preflight UI prompt |
| GET `/api/v1/capability-preflight/setup-offers` | medium | Setup offers | preflight services | setup offer list | offer registry | Capability Preflight UI prompt |

## Template Atlas

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| GET `/api/v1/templates` | medium | Template Atlas | template migration/libraries | template summary list | product decision | Template Atlas bundle |
| POST `/api/v1/templates/{template_id}/preview` | medium | Template Preview | deterministic render/template service | preview receipt/read model | template preview contracts | Template Atlas bundle |
| POST `/api/v1/templates/{template_id}/versions/{version_id}/approve` | medium | Approval | review/approval services | approval receipt | template version model | Template Atlas bundle |

## Avatar Library

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| POST `/api/v1/avatar-library/runs` | medium | Avatar builder | Avatar Performance / Acting Library services | library run summary | avatar asset production contracts | Avatar Library UI prompt |
| GET `/api/v1/avatar-library/runs/{run_id}/grid` | medium | 64-state grid | Acting library service | state grid read model | asset refs | Avatar Library UI prompt |
| POST `/api/v1/avatar-library/states/{state_id}/approve` | medium | State approval | approval service | approval receipt | approval policy | Avatar Library UI prompt |
| POST `/api/v1/avatar-library/states/{state_id}/regenerate` | low | Regeneration | provider/preflight later | typed command receipt | provider preflight | Later provider-enabled prompt |

## SuperVisual

Committed runtime routes already cover list/get/create project, variants, build runs, steps, snapshot/events, revision, approval, and export. Remaining implementation work is primarily:

- Verify the runtime router is mounted in the served API app.
- Decide whether SuperVisual Studio should have offline/demo fallback.
- Resolve untracked duplicate `/api/v1/supervisual` project API before adding more routes.

## Carousel

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| GET `/api/v1/carousel/drafts` | medium | Future Carousel Studio | `CarouselEngineService` | draft summary | Carousel runtime API | Carousel Runtime API bundle |
| GET `/api/v1/carousel/drafts/{draft_id}` | medium | Draft detail | `CarouselEngineService` | draft detail/read model | runtime persistence | Carousel Runtime API bundle |
| POST `/api/v1/carousel/drafts/{draft_id}/preview` | medium | Slide preview | Carousel render service | preview pack | fake render route | Carousel Runtime API bundle |
| POST `/api/v1/carousel/drafts/{draft_id}/revisions` | medium | Revisions | Carousel engine service | typed revision receipt | revision commands | Carousel Runtime API bundle |
| POST `/api/v1/carousel/drafts/{draft_id}/export` | medium | Export | Carousel engine service | export pack | approval state | Carousel Runtime API bundle |

## Video Timeline

Backend route and frontend client already exist for:

- GET `/api/v1/video-edit-programs/current/timeline-workbench`
- POST `/api/v1/video-edit-programs/{program_id}/timeline-edits/propose`
- POST `/api/v1/video-edit-programs/{program_id}/timeline-edits/submit`
- POST `/api/v1/video-edit-programs/{program_id}/proxy-renders`
- POST `/api/v1/video-edit-programs/{program_id}/otio-exports`

Remaining work:

- Verify app-level router mounting.
- Decide when to set `VITE_CMF_TIMELINE_FIXTURE_MODE=false`.
- Persist read models beyond in-memory/demo service when ready.

## Review

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| GET `/api/v1/review-packets/{packet_id}` | high | Review Workbench | Review state/evidence services | review packet read model | route decision | Review Workbench wiring prompt |
| POST `/api/v1/review-packets/{packet_id}/approve` | high | Approval action | ReviewDecisionService | `ReviewDecisionReceipt` | action mapping | Review Workbench wiring prompt |
| POST `/api/v1/review-packets/{packet_id}/reject` | high | Rejection action | ReviewDecisionService | `ReviewDecisionReceipt` | action mapping | Review Workbench wiring prompt |
| POST `/api/v1/review-packets/{packet_id}/revisions` | high | Revision command | ReviewDecisionService | typed revision receipt | command schema | Review Workbench wiring prompt |

## Render Worker

| Endpoint | Priority | Existing Frontend Need | Backend Service Candidate | Required Read Model | Blocking Dependency | Recommended Prompt/Bundle |
|---|---|---|---|---|---|---|
| GET `/api/v1/render-workers` | low | Render dashboard | GPU/local worker services | worker list | local worker registry | Local Render Worker prompt |
| GET `/api/v1/render-workers/{worker_id}/capabilities` | low | Capability check | worker services | worker capability read model | capability registry | Local Render Worker prompt |
| POST `/api/v1/render-jobs` | low | Real render queue | render services | render job receipt | real render policy | Later render worker bundle |
| GET `/api/v1/render-jobs/{job_id}` | low | Job detail | render services | render job read model | persistence | Later render worker bundle |
| GET `/api/v1/render-jobs/{job_id}/receipt` | low | Receipt visibility | render services | render receipt | persistence | Later render worker bundle |

## Provider Jobs

Routes exist for provider capabilities/jobs/receipts, but no frontend client was found. Missing UI-shaped endpoints may include sample approval and batch controls once real provider execution is approved.
