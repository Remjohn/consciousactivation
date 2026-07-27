"""Batch 3 production orchestration service for TS-CMF-120 through TS-CMF-132."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.composition_runtime import RendererTarget
from ccp_studio.contracts.production_orchestration import (
    BudgetCostEstimate,
    BudgetReconciliationReceipt,
    BudgetReservationReceipt,
    CanonicalStageArtifact,
    CapabilityRecord,
    CapabilityRouteRequest,
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
    ProductionStageSpec,
    ProductionWorkspace,
    ProviderAvailabilityGateReceipt,
    ProviderCandidateScore,
    ProviderMenuSnapshot,
    ProviderRouteDecisionReceipt,
    ReferenceMediaClassificationReceipt,
    ReferenceMediaInspectionReceipt,
    ReferenceMediaIntakeRecord,
    RenderRepairCommand,
    RenderRuntimeCandidate,
    RenderRuntimeDriftReceipt,
    RenderRuntimeLock,
    RenderRuntimeSelectionRequest,
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
    production_hash,
)
from ccp_studio.repositories.production_orchestration import InMemoryProductionOrchestrationRepository


class ProductionOrchestrationServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ProductionOrchestrationService:
    repository: InMemoryProductionOrchestrationRepository = field(default_factory=InMemoryProductionOrchestrationRepository)

    def register_openmontage_reference(
        self,
        *,
        repo_url: str = "https://github.com/calesthio/OpenMontage",
        license_family: str = "MIT",
        proposed_patterns: list[str] | None = None,
        source_evidence_refs: list[str] | None = None,
        direct_import_requested: bool = False,
        guest_data_execution_requested: bool = False,
    ) -> tuple[OpenMontageReferenceCandidate, OpenMontageAdapterDecisionReceipt]:
        candidate = self.repository.put(
            OpenMontageReferenceCandidate(
                repo_url=repo_url,
                license_family=license_family,
                proposed_patterns=proposed_patterns or ["stage_graph", "timeline_manifest", "artifact_receipts"],
                source_evidence_refs=source_evidence_refs or ["TS-CMF-120", "OpenMontage:architecture-reference"],
                direct_import_requested=direct_import_requested,
                guest_data_execution_requested=guest_data_execution_requested,
            )
        )
        blocker_codes: list[str] = []
        if license_family.upper() == "AGPL":
            blocker_codes.append("OPENMONTAGE_LICENSE_IMPORT_BLOCKED")
        if direct_import_requested:
            blocker_codes.append("OPENMONTAGE_DIRECT_IMPORT_BLOCKED")
        if guest_data_execution_requested:
            blocker_codes.append("OPENMONTAGE_GUEST_DATA_EXECUTION_BLOCKED")
        decision = self.repository.put(
            OpenMontageAdapterDecisionReceipt(
                candidate_id=candidate.openmontage_reference_candidate_id,
                decision="blocked" if blocker_codes else "architectural_reference_only",
                adopted_patterns=[] if blocker_codes else candidate.proposed_patterns,
                boundary_statement="OpenMontage may inform CMF stage-manifest architecture but cannot own guest data, direct imports, final render authority, or approval policy.",
                blocker_codes=blocker_codes,
                evidence_refs=candidate.source_evidence_refs,
            )
        )
        return candidate, decision

    def default_stage_specs(self) -> list[ProductionStageSpec]:
        return [
            ProductionStageSpec(
                stage_code="STAGE-INTAKE",
                stage_name="Source and Workspace Intake",
                owner_agent_ref="AGT-OPS-AG",
                allowed_skill_refs=["SKILL:source-provenance", "SKILL:workspace-checkpoint"],
                allowed_tool_refs=["source_ingestion", "workspace_service"],
                required_output_artifact_types=["source_artifact", "workspace_checkpoint"],
                required_receipt_types=["source_provenance_receipt", "workspace_checkpoint"],
            ),
            ProductionStageSpec(
                stage_code="STAGE-COMPILE",
                stage_name="Compiler and Provider Materialization",
                owner_agent_ref="AGT-COMP-AG",
                allowed_skill_refs=["SKILL:stage-director", "SKILL:provider-router"],
                allowed_tool_refs=["asset_program_compiler", "provider_operations"],
                required_input_refs=["source_artifact", "workspace_checkpoint"],
                required_output_artifact_types=["program_manifest", "provider_plan"],
                required_receipt_types=["provider_route_decision", "runtime_lock"],
            ),
            ProductionStageSpec(
                stage_code="STAGE-QA",
                stage_name="QA Review and Approval",
                owner_agent_ref="AGT-QA-AG",
                allowed_skill_refs=["SKILL:doctrine-eval", "SKILL:approval-review"],
                allowed_tool_refs=["deterministic_rendering", "review_state", "approval_gate"],
                required_input_refs=["render_manifest", "eval_summary"],
                required_output_artifact_types=["qa_receipt", "approval_receipt"],
                required_receipt_types=["pre_compose_receipt", "post_render_qa_receipt", "human_approval_receipt"],
            ),
        ]

    def create_manifest_draft(
        self,
        *,
        manifest_code: str = "CMF-PRODUCTION-MANIFEST-V1",
        project_type: str = "interview_first_asset_pack",
        stage_specs: list[ProductionStageSpec] | None = None,
    ) -> ProductionPipelineManifestDraft:
        draft = ProductionPipelineManifestDraft(
            manifest_code=manifest_code,
            project_type=project_type,  # type: ignore[arg-type]
            stage_specs=stage_specs or self.default_stage_specs(),
            doctrine_refs=["CCP V9", "CCP V9.1", "CMF 9 Doctrines", "Primitive Triads"],
            source_policy_refs=["no_fabricated_guest_truth", "source_evidence_required", "human_approval_required"],
        )
        return self.repository.put(draft)

    def validate_manifest(self, draft: ProductionPipelineManifestDraft) -> ProductionPipelineManifestSnapshot:
        blocker_codes: list[str] = []
        for stage in draft.stage_specs:
            if not stage.allowed_skill_refs:
                blocker_codes.append("MANIFEST_STAGE_SKILL_REFS_MISSING")
            if not stage.required_receipt_types:
                blocker_codes.append("MANIFEST_STAGE_RECEIPTS_MISSING")
            if stage.approval_required is False and "STAGE-QA" in stage.stage_code:
                blocker_codes.append("MANIFEST_QA_STAGE_MUST_REQUIRE_APPROVAL")
        snapshot = ProductionPipelineManifestSnapshot(
            draft_id=draft.production_pipeline_manifest_draft_id,
            manifest_code=draft.manifest_code,
            stage_specs=draft.stage_specs,
            manifest_hash=production_hash(draft.model_dump(mode="json")),
            active=False,
            continuity_gate_passed=not blocker_codes,
            blocker_codes=sorted(set(blocker_codes)),
        )
        return self.repository.put(snapshot)

    def activate_manifest(self, snapshot: ProductionPipelineManifestSnapshot) -> ProductionManifestActivationReceipt:
        decision = "approved" if snapshot.continuity_gate_passed and not snapshot.blocker_codes else "blocked"
        active_snapshot = snapshot.model_copy(update={"active": decision == "approved"})
        self.repository.manifest_snapshots[snapshot.production_pipeline_manifest_snapshot_id] = active_snapshot
        receipt = ProductionManifestActivationReceipt(
            snapshot_id=snapshot.production_pipeline_manifest_snapshot_id,
            decision=decision,
            blocker_codes=active_snapshot.blocker_codes,
            evidence_refs=[f"manifest_snapshot:{snapshot.production_pipeline_manifest_snapshot_id}"],
        )
        return self.repository.put(receipt)

    def register_stage_skill(self, *, stage_code: str = "STAGE-COMPILE", skill_ref: str = "SKILL:stage-director") -> StageDirectorSkillSpec:
        spec = StageDirectorSkillSpec(
            skill_ref=skill_ref,
            stage_code=stage_code,
            responsibility="Convert stage manifest context into typed stage artifacts without hidden prompt authority.",
            allowed_tool_refs=["asset_program_compiler", "provider_operations", "review_state"],
            required_context_refs=["manifest_snapshot", "source_context", "workspace"],
            output_artifact_types=["stage_artifact", "stage_receipt"],
            authority_boundary="Stage Director may orchestrate registered skills and tools but cannot expand stage scope or bypass approval.",
        )
        return self.repository.put(spec)

    def invoke_stage_skill(
        self,
        *,
        skill_spec: StageDirectorSkillSpec,
        manifest_snapshot_id: UUID,
        source_context_refs: list[str],
        requested_output_artifact_type: str = "stage_artifact",
    ) -> tuple[StageDirectorContextBundle, StageSkillInvocationCommand, StageSkillOutputEnvelope | None, StageSkillInvocationReceipt]:
        context = self.repository.put(
            StageDirectorContextBundle(
                manifest_snapshot_id=manifest_snapshot_id,
                stage_code=skill_spec.stage_code,
                source_context_refs=source_context_refs,
                provider_menu_ref="provider_menu:latest",
                workspace_ref="workspace:current",
            )
        )
        command = self.repository.put(
            StageSkillInvocationCommand(
                skill_ref=skill_spec.skill_ref,
                context_bundle_id=context.stage_director_context_bundle_id,
                requested_output_artifact_type=requested_output_artifact_type,
                command_ref=f"command:stage-skill:{uuid4()}",
            )
        )
        blocker_codes = [] if requested_output_artifact_type in skill_spec.output_artifact_types else ["STAGE_SKILL_OUTPUT_TYPE_NOT_ALLOWED"]
        output = None
        if not blocker_codes:
            output = self.repository.put(
                StageSkillOutputEnvelope(
                    artifact_ref=f"artifact:{skill_spec.stage_code}:{uuid4()}",
                    artifact_type=requested_output_artifact_type,
                    source_refs=source_context_refs,
                    eval_refs=[f"eval:stage-skill:{skill_spec.stage_code}"],
                    deterministic_hash=production_hash({"skill": skill_spec.model_dump(mode="json"), "context": context.model_dump(mode="json")}),
                )
            )
        receipt = self.repository.put(
            StageSkillInvocationReceipt(
                command_id=command.stage_skill_invocation_command_id,
                output_envelope_id=output.stage_skill_output_envelope_id if output else None,
                decision="blocked" if blocker_codes else "approved",
                blocker_codes=blocker_codes,
                evidence_refs=[f"context_bundle:{context.stage_director_context_bundle_id}"],
            )
        )
        return context, command, output, receipt

    def register_capability(self, **kwargs) -> CapabilityRecord:
        record = CapabilityRecord(**kwargs)
        return self.repository.put(record)

    def build_provider_menu(self) -> ProviderMenuSnapshot:
        if not self.repository.capability_records:
            self.register_capability(
                provider_code="comfyui-gpu",
                capability_kind="rendering",
                tool_ref="comfyui:self-hosted",
                cost_class="medium",
                reproducibility_score=0.9,
                doctrine_fit_score=0.86,
                source_scope="self_hosted",
            )
            self.register_capability(
                provider_code="skia-renderer",
                capability_kind="rendering",
                tool_ref="skia:deterministic",
                cost_class="low",
                reproducibility_score=0.98,
                doctrine_fit_score=0.9,
                source_scope="internal",
            )
        records = list(self.repository.capability_records.values())
        snapshot = ProviderMenuSnapshot(
            capability_records=records,
            menu_hash=production_hash([record.model_dump(mode="json") for record in records]),
            unavailable_provider_codes=[record.provider_code for record in records if not record.available],
        )
        return self.repository.put(snapshot)

    def route_provider(self, request: CapabilityRouteRequest, menu: ProviderMenuSnapshot) -> ProviderRouteDecisionReceipt:
        cost_rank = {"low": 1, "medium": 2, "high": 3}
        candidate_scores: list[ProviderCandidateScore] = []
        for record in menu.capability_records:
            blockers: list[str] = []
            if not record.available:
                blockers.append("PROVIDER_NOT_AVAILABLE")
            if record.capability_kind != request.required_capability_kind:
                blockers.append("PROVIDER_CAPABILITY_KIND_MISMATCH")
            if record.source_scope not in request.source_scope_allowed:
                blockers.append("PROVIDER_SOURCE_SCOPE_BLOCKED")
            if cost_rank[record.cost_class] > cost_rank[request.max_cost_class]:
                blockers.append("PROVIDER_COST_CLASS_EXCEEDS_CAP")
            if record.reproducibility_score < request.minimum_reproducibility_score:
                blockers.append("PROVIDER_REPRODUCIBILITY_BELOW_THRESHOLD")
            if record.doctrine_fit_score < request.minimum_doctrine_fit_score:
                blockers.append("PROVIDER_DOCTRINE_FIT_BELOW_THRESHOLD")
            score = 0.0 if blockers else round((record.reproducibility_score + record.doctrine_fit_score + (1 - (cost_rank[record.cost_class] - 1) * 0.25)) / 3, 4)
            candidate_scores.append(
                ProviderCandidateScore(
                    capability_record_id=record.capability_record_id,
                    provider_code=record.provider_code,
                    score=score,
                    criteria_scores={
                        "reproducibility": record.reproducibility_score,
                        "doctrine_fit": record.doctrine_fit_score,
                        "cost": 1 - (cost_rank[record.cost_class] - 1) * 0.25,
                    },
                    blocker_codes=blockers,
                )
            )
        eligible = [score for score in candidate_scores if not score.blocker_codes]
        selected = max(eligible, key=lambda item: item.score, default=None)
        receipt = ProviderRouteDecisionReceipt(
            capability_route_request_id=request.capability_route_request_id,
            selected_provider_code=selected.provider_code if selected else None,
            candidate_scores=candidate_scores,
            decision="approved" if selected else "blocked",
            blocker_codes=[] if selected else ["NO_ELIGIBLE_PROVIDER"],
            evidence_refs=request.evidence_refs,
        )
        return self.repository.put(receipt)

    def create_workspace(self, *, organization_id: UUID, brand_id: UUID, manifest_snapshot_id: UUID, guest_id: UUID | None = None) -> ProductionWorkspace:
        workspace = ProductionWorkspace(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            manifest_snapshot_id=manifest_snapshot_id,
            workspace_ref=f"workspace:{brand_id}:{guest_id or 'brand'}",
            object_storage_prefix=f"cmf/{organization_id}/{brand_id}/{guest_id or 'brand'}/",
        )
        return self.repository.put(workspace)

    def checkpoint_workspace(self, *, workspace_id: UUID, stage_code: str, artifact_ref: str = "artifact:stage") -> tuple[WorkspaceArtifactSlot, WorkspaceCheckpoint]:
        slot = self.repository.put(
            WorkspaceArtifactSlot(
                workspace_id=workspace_id,
                stage_code=stage_code,
                artifact_type="stage_artifact",
                artifact_ref=artifact_ref,
                receipt_refs=[f"receipt:{stage_code}"],
            )
        )
        checkpoint = self.repository.put(
            WorkspaceCheckpoint(
                workspace_id=workspace_id,
                stage_code=stage_code,
                checkpoint_state_hash=production_hash({"workspace_id": workspace_id, "stage_code": stage_code, "artifact_ref": artifact_ref}),
            )
        )
        workspace = self.repository.workspaces[workspace_id]
        self.repository.workspaces[workspace_id] = workspace.model_copy(update={"artifact_slot_refs": [*workspace.artifact_slot_refs, f"workspace_slot:{slot.workspace_artifact_slot_id}"]})
        return slot, checkpoint

    def resume_workspace(self, *, workspace_id: UUID) -> WorkspaceResumeDecision:
        candidates = [item for item in self.repository.workspace_checkpoints.values() if item.workspace_id == workspace_id and item.valid]
        checkpoint = max(candidates, key=lambda item: item.written_at, default=None)
        decision = WorkspaceResumeDecision(
            workspace_id=workspace_id,
            checkpoint_id=checkpoint.workspace_checkpoint_id if checkpoint else None,
            decision="resume" if checkpoint else "restart",
            evidence_refs=[f"workspace_checkpoint:{checkpoint.workspace_checkpoint_id}"] if checkpoint else [],
        )
        return self.repository.put(decision)

    def intake_reference_media(
        self,
        *,
        media_ref: str,
        declared_use_mode: str,
        source_evidence_refs: list[str],
        consent_scope_ref: str | None = None,
    ) -> tuple[ReferenceMediaIntakeRecord, ReferenceMediaClassificationReceipt, ReferenceMediaInspectionReceipt]:
        record = self.repository.put(
            ReferenceMediaIntakeRecord(
                media_ref=media_ref,
                declared_use_mode=declared_use_mode,  # type: ignore[arg-type]
                source_evidence_refs=source_evidence_refs,
                consent_scope_ref=consent_scope_ref,
                media_hash=production_hash({"media_ref": media_ref, "source_evidence_refs": source_evidence_refs}),
            )
        )
        blockers = ["SOURCE_FOOTAGE_CONSENT_SCOPE_MISSING"] if declared_use_mode == "source_footage" and not consent_scope_ref else []
        classification = self.repository.put(
            ReferenceMediaClassificationReceipt(
                record_id=record.reference_media_intake_record_id,
                classified_use_mode=record.declared_use_mode,
                downstream_use_allowed=not blockers,
                blocker_codes=blockers,
                evidence_refs=source_evidence_refs,
            )
        )
        inspection = self.repository.put(
            ReferenceMediaInspectionReceipt(
                record_id=record.reference_media_intake_record_id,
                duration_seconds=61.0,
                resolution="1080x1920",
                audio_present=True,
                transcription_ready=declared_use_mode == "source_footage",
                composition_lessons=["vertical talking-head with upper proof surface", "caption-safe lower-third spacing"],
                blocker_codes=blockers,
            )
        )
        return record, classification, inspection

    def search_footage(self, *, query: str, visual_role: str, allowed_license_families: list[str]) -> tuple[FootageSearchRequest, list[FootageCandidate]]:
        request = self.repository.put(
            FootageSearchRequest(
                query=query,
                visual_role=visual_role,
                source_evidence_refs=[f"research_query:{query}"],
                allowed_license_families=allowed_license_families,
            )
        )
        candidates = [
            self.repository.put(
                FootageCandidate(
                    search_request_id=request.footage_search_request_id,
                    source_url=f"https://source.example/{query.replace(' ', '-')}/{index}",
                    license_family=allowed_license_families[0],
                    media_hash=production_hash({"query": query, "index": index}),
                    relevance_score=0.92 - index * 0.1,
                    visual_role=visual_role,
                    evidence_refs=[f"license:{allowed_license_families[0]}", f"source_url:{index}"],
                )
            )
            for index in range(2)
        ]
        return request, candidates

    def select_footage(self, candidate: FootageCandidate, allowed_license_families: list[str]) -> FootageSelectionReceipt:
        blockers = [] if candidate.license_family in allowed_license_families and candidate.evidence_refs else ["FOOTAGE_LICENSE_EVIDENCE_BLOCKED"]
        receipt = FootageSelectionReceipt(
            candidate_id=candidate.footage_candidate_id,
            selected=not blockers,
            decision="approved" if not blockers else "blocked",
            blocker_codes=blockers,
            evidence_refs=candidate.evidence_refs,
        )
        return self.repository.put(receipt)

    def select_and_lock_runtime(self, request: RenderRuntimeSelectionRequest, candidates: list[RenderRuntimeCandidate]) -> RenderRuntimeLock:
        eligible = [
            item
            for item in candidates
            if item.available and item.runtime_code in request.allowed_runtime_codes and request.output_type in item.supported_output_types and item.deterministic_replay_score >= request.minimum_replay_score
        ]
        if not eligible:
            raise ProductionOrchestrationServiceError("NO_ELIGIBLE_RENDER_RUNTIME", "No runtime candidate satisfies the render lock request.")
        selected = max(eligible, key=lambda item: item.deterministic_replay_score)
        lock = RenderRuntimeLock(
            selection_request_id=request.render_runtime_selection_request_id,
            runtime_code=selected.runtime_code,
            locked_runtime_hash=production_hash(selected.model_dump(mode="json")),
            locked_dependency_refs=[f"runtime:{selected.runtime_code}", f"source_program:{request.source_program_ref}"],
        )
        return self.repository.put(lock)

    def check_runtime_drift(self, *, lock: RenderRuntimeLock, observed_runtime_hash: str | None = None) -> RenderRuntimeDriftReceipt:
        observed = observed_runtime_hash or lock.locked_runtime_hash
        drift = observed != lock.locked_runtime_hash
        receipt = RenderRuntimeDriftReceipt(
            render_runtime_lock_id=lock.render_runtime_lock_id,
            observed_runtime_hash=observed,
            drift_detected=drift,
            decision="blocked" if drift else "approved",
            blocker_codes=["RENDER_RUNTIME_DRIFT_DETECTED"] if drift else [],
        )
        return self.repository.put(receipt)

    def run_pre_compose_gate(self, *, delivery_promise_id: UUID, risk_score: float, runtime_lock_ref: str, eval_refs: list[str]) -> tuple[PreComposeRiskGateReceipt, PreComposeRepairPlan | None]:
        blockers: list[str] = []
        if not runtime_lock_ref:
            blockers.append("PRECOMPOSE_RUNTIME_LOCK_MISSING")
        if not eval_refs:
            blockers.append("PRECOMPOSE_EVAL_REFS_MISSING")
        slideshow_risk = risk_score >= 0.65
        if slideshow_risk:
            blockers.append("PRECOMPOSE_SLIDESHOW_RISK")
        receipt = self.repository.put(
            PreComposeRiskGateReceipt(
                delivery_promise_id=delivery_promise_id,
                risk_score=risk_score,
                slideshow_risk=slideshow_risk,
                decision="blocked" if blockers else "approved",
                blocker_codes=blockers,
                evidence_refs=[runtime_lock_ref, *eval_refs],
            )
        )
        repair = None
        if blockers:
            repair = self.repository.put(
                PreComposeRepairPlan(
                    pre_compose_risk_gate_receipt_id=receipt.pre_compose_risk_gate_receipt_id,
                    repair_actions=["add_runtime_lock", "increase_motion_or_sequence_variance", "attach_missing_eval_receipts"],
                )
            )
        return receipt, repair

    def run_post_render_qa(
        self,
        *,
        render_ref: str,
        runtime_lock_ref: str,
        source_program_ref: str,
        expected_render_hash: str,
        observed_render_hash: str | None = None,
        text_overlap_detected: bool = False,
        blank_frame_detected: bool = False,
    ) -> tuple[RenderedAssetReviewRequest, MediaProbeResult, PostRenderQAReceipt, RenderRepairCommand | None]:
        review_request = self.repository.put(
            RenderedAssetReviewRequest(
                render_ref=render_ref,
                runtime_lock_ref=runtime_lock_ref,
                source_program_ref=source_program_ref,
                expected_render_hash=expected_render_hash,
            )
        )
        probe = self.repository.put(
            MediaProbeResult(
                render_ref=render_ref,
                observed_render_hash=observed_render_hash or expected_render_hash,
                duration_seconds=30.0,
                resolution="1080x1920",
                text_overlap_detected=text_overlap_detected,
                blank_frame_detected=blank_frame_detected,
            )
        )
        blockers: list[str] = []
        if probe.observed_render_hash != expected_render_hash:
            blockers.append("POST_RENDER_HASH_MISMATCH")
        if probe.text_overlap_detected:
            blockers.append("POST_RENDER_TEXT_OVERLAP")
        if probe.blank_frame_detected:
            blockers.append("POST_RENDER_BLANK_FRAME")
        qa = self.repository.put(
            PostRenderQAReceipt(
                rendered_asset_review_request_id=review_request.rendered_asset_review_request_id,
                media_probe_result_id=probe.media_probe_result_id,
                score=0.95 if not blockers else 0.35,
                decision="approved" if not blockers else "blocked",
                blocker_codes=blockers,
                repair_command_refs=[],
            )
        )
        repair = None
        if blockers:
            repair = self.repository.put(
                RenderRepairCommand(
                    post_render_qa_receipt_id=qa.post_render_qa_receipt_id,
                    repair_scope=blockers,
                    command_ref=f"command:render-repair:{qa.post_render_qa_receipt_id}",
                )
            )
            self.repository.post_render_qa_receipts[qa.post_render_qa_receipt_id] = qa.model_copy(update={"repair_command_refs": [f"render_repair_command:{repair.render_repair_command_id}"]})
        return review_request, probe, self.repository.post_render_qa_receipts[qa.post_render_qa_receipt_id], repair

    def estimate_budget(self, *, workspace_id: UUID, provider_code: str, estimated_units: float, estimated_cost_usd: float, cap_usd: float) -> BudgetCostEstimate:
        blockers = ["BUDGET_ESTIMATE_EXCEEDS_CAP"] if estimated_cost_usd > cap_usd else []
        estimate = BudgetCostEstimate(
            workspace_id=workspace_id,
            provider_code=provider_code,
            estimated_units=estimated_units,
            estimated_cost_usd=estimated_cost_usd,
            cap_usd=cap_usd,
            decision="blocked" if blockers else "approved",
            blocker_codes=blockers,
        )
        return self.repository.put(estimate)

    def reserve_budget(self, estimate: BudgetCostEstimate) -> BudgetReservationReceipt:
        receipt = BudgetReservationReceipt(
            budget_cost_estimate_id=estimate.budget_cost_estimate_id,
            reserved_cost_usd=0 if estimate.decision == "blocked" else estimate.estimated_cost_usd,
            decision=estimate.decision,
            blocker_codes=estimate.blocker_codes,
        )
        return self.repository.put(receipt)

    def reconcile_budget(self, reservation: BudgetReservationReceipt, *, actual_cost_usd: float) -> BudgetReconciliationReceipt:
        variance = actual_cost_usd - reservation.reserved_cost_usd
        blockers = ["BUDGET_ACTUAL_EXCEEDS_RESERVED"] if actual_cost_usd > reservation.reserved_cost_usd * 1.2 and reservation.reserved_cost_usd > 0 else []
        receipt = BudgetReconciliationReceipt(
            budget_reservation_receipt_id=reservation.budget_reservation_receipt_id,
            actual_cost_usd=actual_cost_usd,
            variance_usd=variance,
            decision="blocked" if blockers else "approved",
            blocker_codes=blockers,
        )
        return self.repository.put(receipt)

    def create_artifact_review(
        self,
        *,
        workspace_id: UUID,
        stage_code: str,
        artifact_ref: str,
        reviewer_id: UUID,
        source_refs: list[str],
    ) -> tuple[CanonicalStageArtifact, StageArtifactReviewRequest]:
        artifact = self.repository.put(
            CanonicalStageArtifact(
                workspace_id=workspace_id,
                stage_code=stage_code,
                artifact_type="production_stage_output",
                artifact_ref=artifact_ref,
                source_refs=source_refs,
                eval_receipt_refs=[f"eval:{artifact_ref}"],
                render_receipt_refs=[f"render:{artifact_ref}"],
            )
        )
        request = self.repository.put(
            StageArtifactReviewRequest(
                artifact_id=artifact.canonical_stage_artifact_id,
                reviewer_id=reviewer_id,
            )
        )
        return artifact, request

    def add_reviewer_finding(self, *, review_request_id: UUID, severity: str, finding_code: str, message: str, waived: bool = False) -> ReviewerFinding:
        finding = ReviewerFinding(
            review_request_id=review_request_id,
            severity=severity,  # type: ignore[arg-type]
            finding_code=finding_code,
            message=message,
            waived=waived,
        )
        return self.repository.put(finding)

    def decide_human_approval(self, *, review_request_id: UUID, reviewer_id: UUID, approve: bool = True) -> HumanApprovalReceipt:
        findings = [item for item in self.repository.reviewer_findings.values() if item.review_request_id == review_request_id]
        critical_blockers = [item.finding_code for item in findings if item.severity == "critical" and not item.waived]
        decision = "approved" if approve and not critical_blockers else "blocked"
        receipt = HumanApprovalReceipt(
            review_request_id=review_request_id,
            reviewer_id=reviewer_id,
            decision=decision,  # type: ignore[arg-type]
            blocker_codes=critical_blockers,
            evidence_refs=[f"review_request:{review_request_id}", *[f"finding:{item.reviewer_finding_id}" for item in findings]],
        )
        return self.repository.put(receipt)
