# Operator Web Backend Read Model Audit

## Read Model And Contract Inventory

| Contract File | Read Model / Contract | Related Service | Related API Route | Related Frontend Screen | Missing Frontend Wiring | Missing Backend Endpoint / Gap |
|---|---|---|---|---|---|---|
| `src/ccp_studio/contracts/operator_ui.py` | `OperatorShellState` | `OperatorUiService.build_shell_state` | POST `/api/v1/operator-ui/shell` | Shell / Control Tower | Frontend does not call shell read model. | Mount status unclear. |
| `operator_ui.py` | `WorkspaceControlTowerState` | `OperatorUiService.build_control_tower_state` | POST `/api/v1/operator-ui/control-tower` | Control Tower | Control Tower uses `data.js`, not backend read model. | Mount status unclear. |
| `operator_ui.py` | `GuestWorkspaceState` | `OperatorUiService` | no direct route found | Guests / Workspace | Guest screen uses `data.js`. | Add route or workspace-specific read model after product decision. |
| `operator_ui.py` | `ContentAssetFormatRegistryState` | `OperatorUiService.content_format_registry` | GET `/api/v1/operator-ui/content-formats` | Shell status / future format selector | Only used as connectivity check. | None for basic call; app mount unclear. |
| `operator_ui.py` | `AssetPackageBoardState` | `OperatorUiService` | no direct route found | Pipeline / package board | Not wired. | Add board endpoint or map through operations. |
| `operator_ui.py` | `ReviewEvidenceState` | `OperatorUiService` | no direct operator-ui route found | Review | Review uses `data.js`. | Review has separate backend routes; choose owner. |
| `operator_ui.py` | `AgentFactoryState` | `OperatorUiService.build_agent_factory_state` | GET `/api/v1/operator-ui/agent-factory/{brand_workspace_id}` | Agents | Agents screen uses `data.js`. | App mount unclear. |
| `src/ccp_studio/contracts/video_timeline_workbench.py` | `VideoTimelineWorkbenchReadModel` and nested program/scene/track/layer/render/eval summaries | `VideoTimelineWorkbenchService` | `/api/v1/video-edit-programs/*` | Video Timeline Workbench | Frontend client exists; fixture mode defaults on. | App mount unclear; persistence is in-memory/demo. |
| `video_timeline_workbench.py` | `VideoTimelineEditProposal`, `VideoTimelineEditSubmission`, `VideoTimelineEditReceipt` | `VideoTimelineWorkbenchService` | timeline edit propose/submit endpoints | Video Timeline Workbench | Frontend client exists. | App mount unclear; fake apply only. |
| `video_timeline_workbench.py` | `ProxyRenderResponse`, `OTIOExportResponse` | `VideoTimelineWorkbenchService` | proxy render and OTIO endpoints | Video Timeline Workbench | Frontend client exists. | App mount unclear; fake/read-model only. |
| `src/ccp_studio/contracts/supervisual_runtime.py` | `SuperVisualProject`, `SuperVisualVariant`, `SuperVisualSnapshot`, `SuperVisualEvent`, `SuperVisualProjectDetailResponse`, `SuperVisualVariantDetailResponse` | `SuperVisualRuntimeService` | `/api/v1/supervisual/*` runtime router | SuperVisual Studio | Frontend hooks and view model exist. | App mount unclear; no fixture fallback. |
| `src/ccp_studio/contracts/composition_runtime.py` | `ReviewReadModel`, `CompositionApprovalReadModel`, runtime receipts/manifests | `CompositionRuntimeService` | `/api/v1/composition-runtime/review-read-model`, related endpoints | Composition Studio / Review | No frontend client. | Need Composition Studio read model route/client decision. |
| `src/ccp_studio/contracts/review_state.py` | `ReviewEvidenceState`, `ReviewStateReceipt`, `ReviewStateDomainEvent` | `ReviewStateService` | `/api/v1/review-states/*` | Review Workbench | No frontend client. | Need list/get review packet endpoint aligned with UI. |
| `src/ccp_studio/contracts/evaluation_receipts.py` | `EvaluationReceipt`, `EvaluationReviewReadModel` | `EvaluationReceiptService` | `/api/v1/evaluations/*` | Evals / Review | No frontend client. | Need list receipts/read model aggregation endpoint. |
| `src/ccp_studio/contracts/operations_board.py` | `OperationsBoardState`, `BlockerSummary`, `IncidentSummary`, `OperationsReceipt` | `OperationsBoardService` | `/api/v1/operations/*` | Operations | No frontend client. | Need operations board read model wiring. |
| `src/ccp_studio/contracts/golden_path_orchestrator.py` | `GoldenPathRun`, `GoldenPathStageResult`, `GoldenPathObjectSpineMap`, `Format02GoldenPathOutput`, `GoldenPathReceipt` | `Format02GoldenPathOrchestratorService`, `GoldenPathOrchestrationSpineAdapterService` | no direct API route found | Golden Path / Pipeline | No frontend screen/client. | Add run/get/read model endpoints when approved. |
| `src/ccp_studio/contracts/capability_preflight.py` | `CapabilityPreflightReport`, `ProviderMenuSummary`, `PipelineCapabilityStatus`, availability reports | `CapabilityPreflightService`, `ProviderMenuService` | no direct API route found | Capability / Provider Menu | No frontend screen/client. | Add preflight/provider menu API and screen. |
| `src/ccp_studio/contracts/project_workspace_artifact_store.py` | `ClientWorkspace`, `WorkspaceFolderMap`, `RunArtifactDirectory`, `ArtifactRef`, `ArtifactManifest`, `ArtifactReceipt` | `ClientWorkspaceService`, `ArtifactStoreService`, `ArtifactManifestService` | no direct API route found | Workspace / Artifact Browser | No frontend screen/client. | Add workspace/artifact read model endpoints. |
| `src/ccp_studio/contracts/acting_library.py` and `avatar_performance.py` | `ActingLibraryVersion`, `AvatarPerformancePlan`, `AudienceProxyPerformancePlan`, acting/rig contracts | `ActingLibraryService`, Avatar Performance services | `/api/v1/acting-library/*` for acting grid | Avatar Library / Builder | No frontend screen/client. | Avatar 64-state builder read model still needed. |
| `src/ccp_studio/contracts/provider_jobs.py` and `provider_adapters.py` | `ProviderJob`, `ProviderReceipt`, `ProviderJobReceipt`, adapter receipts | `ProviderOperationsService`, provider orchestration services | `/api/v1/provider-jobs/*`, provider recovery routes | Provider Jobs | No frontend screen/client. | Provider job dashboard/sample approval UI needed. |
| `src/ccp_studio/contracts/publishing.py` | `PublishingIntent`, `PublerJob`, `PublishingOutcome` | `PublishingService` | `/api/v1/publishing-intents/*` | Publishing / Publer | No frontend screen/client. | Publishing queue/read model UI needed if in scope. |

## Data Gaps By Screen

- Control Tower: backend `WorkspaceControlTowerState` exists, but frontend still composes static `data.js` cards.
- Pipeline: orchestration and Golden Path contracts exist, but no pipeline run list/read model endpoint was found.
- Composition: multiple composition contracts exist, but current screen is not connected to any read model.
- Review/Evals: review and evaluation read models exist, but no frontend client or screen binding was found.
- Workspace/Artifact: contracts/services exist, but no API route or UI screen was found.
- Capability Provider Menu: contracts/services exist, but no API route or UI screen was found.
- Golden Path: backend service and orchestration spine adapter exist, but no API route or UI screen was found.
