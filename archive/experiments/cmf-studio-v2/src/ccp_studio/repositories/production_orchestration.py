"""In-memory repository for Batch 3 production orchestration objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.production_orchestration import (
    BudgetCostEstimate,
    BudgetReconciliationReceipt,
    BudgetReservationReceipt,
    CanonicalStageArtifact,
    CapabilityRecord,
    FootageCandidate,
    FootageSearchRequest,
    FootageSelectionReceipt,
    HumanApprovalReceipt,
    MediaProbeResult,
    OpenMontageAdapterDecisionReceipt,
    OpenMontageReferenceCandidate,
    PostRenderQAReceipt,
    PreComposeRepairPlan,
    PreComposeRiskGateReceipt,
    ProductionManifestActivationReceipt,
    ProductionPipelineManifestDraft,
    ProductionPipelineManifestSnapshot,
    ProductionWorkspace,
    ProviderAvailabilityGateReceipt,
    ProviderMenuSnapshot,
    ProviderRouteDecisionReceipt,
    ReferenceMediaClassificationReceipt,
    ReferenceMediaInspectionReceipt,
    ReferenceMediaIntakeRecord,
    RenderRepairCommand,
    RenderRuntimeDriftReceipt,
    RenderRuntimeLock,
    RenderedAssetReviewRequest,
    ReviewerFinding,
    StageArtifactReviewRequest,
    StageDirectorContextBundle,
    StageDirectorSkillSpec,
    StageSkillInvocationCommand,
    StageSkillInvocationReceipt,
    StageSkillOutputEnvelope,
    WorkspaceArtifactSlot,
    WorkspaceCheckpoint,
    WorkspaceResumeDecision,
)


@dataclass
class InMemoryProductionOrchestrationRepository:
    openmontage_candidates: dict[UUID, OpenMontageReferenceCandidate] = field(default_factory=dict)
    openmontage_decisions: dict[UUID, OpenMontageAdapterDecisionReceipt] = field(default_factory=dict)
    manifest_drafts: dict[UUID, ProductionPipelineManifestDraft] = field(default_factory=dict)
    manifest_snapshots: dict[UUID, ProductionPipelineManifestSnapshot] = field(default_factory=dict)
    manifest_activation_receipts: dict[UUID, ProductionManifestActivationReceipt] = field(default_factory=dict)
    stage_skill_specs: dict[UUID, StageDirectorSkillSpec] = field(default_factory=dict)
    stage_context_bundles: dict[UUID, StageDirectorContextBundle] = field(default_factory=dict)
    stage_skill_commands: dict[UUID, StageSkillInvocationCommand] = field(default_factory=dict)
    stage_skill_outputs: dict[UUID, StageSkillOutputEnvelope] = field(default_factory=dict)
    stage_skill_receipts: dict[UUID, StageSkillInvocationReceipt] = field(default_factory=dict)
    capability_records: dict[UUID, CapabilityRecord] = field(default_factory=dict)
    provider_menu_snapshots: dict[UUID, ProviderMenuSnapshot] = field(default_factory=dict)
    provider_availability_gate_receipts: dict[UUID, ProviderAvailabilityGateReceipt] = field(default_factory=dict)
    provider_route_decisions: dict[UUID, ProviderRouteDecisionReceipt] = field(default_factory=dict)
    workspaces: dict[UUID, ProductionWorkspace] = field(default_factory=dict)
    artifact_slots: dict[UUID, WorkspaceArtifactSlot] = field(default_factory=dict)
    workspace_checkpoints: dict[UUID, WorkspaceCheckpoint] = field(default_factory=dict)
    workspace_resume_decisions: dict[UUID, WorkspaceResumeDecision] = field(default_factory=dict)
    reference_media_records: dict[UUID, ReferenceMediaIntakeRecord] = field(default_factory=dict)
    reference_media_classifications: dict[UUID, ReferenceMediaClassificationReceipt] = field(default_factory=dict)
    reference_media_inspections: dict[UUID, ReferenceMediaInspectionReceipt] = field(default_factory=dict)
    footage_search_requests: dict[UUID, FootageSearchRequest] = field(default_factory=dict)
    footage_candidates: dict[UUID, FootageCandidate] = field(default_factory=dict)
    footage_selection_receipts: dict[UUID, FootageSelectionReceipt] = field(default_factory=dict)
    runtime_locks: dict[UUID, RenderRuntimeLock] = field(default_factory=dict)
    runtime_drift_receipts: dict[UUID, RenderRuntimeDriftReceipt] = field(default_factory=dict)
    pre_compose_receipts: dict[UUID, PreComposeRiskGateReceipt] = field(default_factory=dict)
    pre_compose_repair_plans: dict[UUID, PreComposeRepairPlan] = field(default_factory=dict)
    rendered_review_requests: dict[UUID, RenderedAssetReviewRequest] = field(default_factory=dict)
    media_probe_results: dict[UUID, MediaProbeResult] = field(default_factory=dict)
    post_render_qa_receipts: dict[UUID, PostRenderQAReceipt] = field(default_factory=dict)
    render_repair_commands: dict[UUID, RenderRepairCommand] = field(default_factory=dict)
    budget_estimates: dict[UUID, BudgetCostEstimate] = field(default_factory=dict)
    budget_reservations: dict[UUID, BudgetReservationReceipt] = field(default_factory=dict)
    budget_reconciliations: dict[UUID, BudgetReconciliationReceipt] = field(default_factory=dict)
    canonical_artifacts: dict[UUID, CanonicalStageArtifact] = field(default_factory=dict)
    artifact_review_requests: dict[UUID, StageArtifactReviewRequest] = field(default_factory=dict)
    reviewer_findings: dict[UUID, ReviewerFinding] = field(default_factory=dict)
    human_approval_receipts: dict[UUID, HumanApprovalReceipt] = field(default_factory=dict)

    def put(self, item):
        stores = {
            OpenMontageReferenceCandidate: self.openmontage_candidates,
            OpenMontageAdapterDecisionReceipt: self.openmontage_decisions,
            ProductionPipelineManifestDraft: self.manifest_drafts,
            ProductionPipelineManifestSnapshot: self.manifest_snapshots,
            ProductionManifestActivationReceipt: self.manifest_activation_receipts,
            StageDirectorSkillSpec: self.stage_skill_specs,
            StageDirectorContextBundle: self.stage_context_bundles,
            StageSkillInvocationCommand: self.stage_skill_commands,
            StageSkillOutputEnvelope: self.stage_skill_outputs,
            StageSkillInvocationReceipt: self.stage_skill_receipts,
            CapabilityRecord: self.capability_records,
            ProviderMenuSnapshot: self.provider_menu_snapshots,
            ProviderAvailabilityGateReceipt: self.provider_availability_gate_receipts,
            ProviderRouteDecisionReceipt: self.provider_route_decisions,
            ProductionWorkspace: self.workspaces,
            WorkspaceArtifactSlot: self.artifact_slots,
            WorkspaceCheckpoint: self.workspace_checkpoints,
            WorkspaceResumeDecision: self.workspace_resume_decisions,
            ReferenceMediaIntakeRecord: self.reference_media_records,
            ReferenceMediaClassificationReceipt: self.reference_media_classifications,
            ReferenceMediaInspectionReceipt: self.reference_media_inspections,
            FootageSearchRequest: self.footage_search_requests,
            FootageCandidate: self.footage_candidates,
            FootageSelectionReceipt: self.footage_selection_receipts,
            RenderRuntimeLock: self.runtime_locks,
            RenderRuntimeDriftReceipt: self.runtime_drift_receipts,
            PreComposeRiskGateReceipt: self.pre_compose_receipts,
            PreComposeRepairPlan: self.pre_compose_repair_plans,
            RenderedAssetReviewRequest: self.rendered_review_requests,
            MediaProbeResult: self.media_probe_results,
            PostRenderQAReceipt: self.post_render_qa_receipts,
            RenderRepairCommand: self.render_repair_commands,
            BudgetCostEstimate: self.budget_estimates,
            BudgetReservationReceipt: self.budget_reservations,
            BudgetReconciliationReceipt: self.budget_reconciliations,
            CanonicalStageArtifact: self.canonical_artifacts,
            StageArtifactReviewRequest: self.artifact_review_requests,
            ReviewerFinding: self.reviewer_findings,
            HumanApprovalReceipt: self.human_approval_receipts,
        }
        store = stores[type(item)]
        key = next(value for name, value in item.__dict__.items() if name.endswith("_id"))
        store[key] = item
        return item
