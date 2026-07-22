"""SuperVisual project service.

This is the operator-facing façade for single-image SuperVisual production. It
uses the canonical ontology/convergence contracts for frame profiles, style
routes, primitive binding, provider preconditions, deterministic fake provider
receipts, eval blocking, and export handoff.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.composition_runtime import ApprovalStatus
from ccp_studio.contracts.creative_ingredients import CompositionRole, SourceReference, SourceReferenceKind
from ccp_studio.contracts.frame_profiles import FrameProfile, FrameProfileCode
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.style_routes import DEFAULT_STYLE_ROUTES, SourceReferenceMode, StyleRoute
from ccp_studio.contracts.supervisual_projects import (
    SuperVisualApprovalReceipt,
    SuperVisualCompositionReceipt,
    SuperVisualContext,
    SuperVisualEvalReceipt,
    SuperVisualExportArtifact,
    SuperVisualLayerEntry,
    SuperVisualLayerPlan,
    SuperVisualPrimitiveBinding,
    SuperVisualProject,
    SuperVisualProviderReceipt,
    SuperVisualRenderContract,
    SuperVisualTimelineEvent,
    SuperVisualTimelineReadModel,
    SuperVisualVariant,
    supervisual_hash,
)
from ccp_studio.repositories.supervisual_projects import InMemorySuperVisualProjectRepository
from ccp_studio.services.contract_convergence_service import ContractConvergenceService, ContractConvergenceServiceError


class SuperVisualProjectServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SuperVisualProjectService:
    repository: InMemorySuperVisualProjectRepository = field(default_factory=InMemorySuperVisualProjectRepository)
    convergence: ContractConvergenceService = field(default_factory=ContractConvergenceService)

    def create_project(
        self,
        *,
        project_name: str,
        workspace_id: UUID,
        brand_context_version_ref: str,
        source_evidence_refs: list[str],
        brand_id: UUID | None = None,
        context_type: str = "manual_context",
        interview_brief_ref: str | None = None,
        transcript_ref: str | None = None,
        context_payload: dict | None = None,
        frame_profile_code: str = "4:5_FEED_POSTER",
        style_route_code: str = "GMG_EXPERT_05_EDITORIAL_SCRIBE",
    ) -> SuperVisualProject:
        context = SuperVisualContext(
            context_type=context_type,  # type: ignore[arg-type]
            workspace_id=workspace_id,
            brand_id=brand_id,
            brand_context_version_ref=brand_context_version_ref,
            interview_brief_ref=interview_brief_ref,
            transcript_ref=transcript_ref,
            source_evidence_refs=source_evidence_refs,
            context_payload=context_payload or {},
        )
        project = self.repository.put_project(
            SuperVisualProject(
                project_name=project_name,
                context=context,
                requested_frame_profile_code=frame_profile_code,
                requested_style_route_code=style_route_code,
            )
        )
        self._event(
            project_id=project.supervisual_project_id,
            event_kind="project_created",
            object_ref=f"supervisual_project:{project.supervisual_project_id}",
            summary="SuperVisual project persisted.",
            evidence_refs=source_evidence_refs,
        )
        return project

    def get_project(self, *, project_id: UUID) -> SuperVisualProject:
        try:
            return self.repository.projects[project_id]
        except KeyError as exc:
            raise SuperVisualProjectServiceError("SUPERVISUAL_PROJECT_NOT_FOUND", str(project_id)) from exc

    def build_project(
        self,
        *,
        project_id: UUID,
        frame_profile_code: str | None = None,
        style_route_code: str | None = None,
        primitive_score: float = 0.92,
        doctrine_score: float = 0.91,
        source_truth_score: float = 0.94,
        frame_profile_score: float = 0.95,
        style_route_score: float = 0.93,
    ) -> SuperVisualVariant:
        project = self.get_project(project_id=project_id)
        return self._create_variant(
            project=project,
            frame_profile_code=frame_profile_code or project.requested_frame_profile_code,
            style_route_code=style_route_code or project.requested_style_route_code,
            revision_instruction=None,
            revision_number=len(project.variant_ids),
            primitive_score=primitive_score,
            doctrine_score=doctrine_score,
            source_truth_score=source_truth_score,
            frame_profile_score=frame_profile_score,
            style_route_score=style_route_score,
            event_kind="variant_built",
        )

    def revise_project(
        self,
        *,
        project_id: UUID,
        revision_instruction: str,
        frame_profile_code: str | None = None,
        style_route_code: str | None = None,
        primitive_score: float = 0.92,
        doctrine_score: float = 0.91,
        source_truth_score: float = 0.94,
        frame_profile_score: float = 0.95,
        style_route_score: float = 0.93,
    ) -> SuperVisualVariant:
        project = self.get_project(project_id=project_id)
        return self._create_variant(
            project=project,
            frame_profile_code=frame_profile_code or project.requested_frame_profile_code,
            style_route_code=style_route_code or project.requested_style_route_code,
            revision_instruction=revision_instruction,
            revision_number=len(project.variant_ids),
            primitive_score=primitive_score,
            doctrine_score=doctrine_score,
            source_truth_score=source_truth_score,
            frame_profile_score=frame_profile_score,
            style_route_score=style_route_score,
            event_kind="revision_built",
        )

    def approve_project(self, *, project_id: UUID, operator_id: UUID, variant_id: UUID | None = None) -> SuperVisualApprovalReceipt:
        project = self.get_project(project_id=project_id)
        variant = self._active_variant(project, variant_id=variant_id)
        blockers = list(variant.eval_receipt.blocker_codes)
        decision = "approved" if variant.eval_receipt.decision == "approved" and not blockers else "blocked"
        receipt = self.repository.put_approval_receipt(
            SuperVisualApprovalReceipt(
                project_id=project_id,
                variant_id=variant.supervisual_variant_id,
                operator_id=operator_id,
                decision=decision,
                approval_status=ApprovalStatus.approved if decision == "approved" else ApprovalStatus.blocked,
                blocker_codes=[] if decision == "approved" else blockers,
                evidence_refs=[
                    f"supervisual_variant:{variant.supervisual_variant_id}",
                    f"eval_receipt:{variant.eval_receipt.eval_receipt_id}",
                ],
            )
        )
        variant_status = "approved" if decision == "approved" else "blocked"
        self.repository.variants[variant.supervisual_variant_id] = variant.model_copy(update={"status": variant_status})
        self.repository.projects[project_id] = project.model_copy(
            update={
                "status": "approved" if decision == "approved" else "blocked",
                "blocker_codes": receipt.blocker_codes,
                "updated_at": utc_now(),
            }
        )
        self._event(
            project_id=project_id,
            event_kind="approval_decided",
            object_ref=f"supervisual_approval_receipt:{receipt.supervisual_approval_receipt_id}",
            summary=f"Operator approval {decision}.",
            evidence_refs=receipt.evidence_refs,
            blocker_codes=receipt.blocker_codes,
        )
        return receipt

    def reject_project(
        self,
        *,
        project_id: UUID,
        operator_id: UUID,
        reason: str,
        variant_id: UUID | None = None,
    ) -> SuperVisualApprovalReceipt:
        project = self.get_project(project_id=project_id)
        variant = self._active_variant(project, variant_id=variant_id)
        receipt = self.repository.put_approval_receipt(
            SuperVisualApprovalReceipt(
                project_id=project_id,
                variant_id=variant.supervisual_variant_id,
                operator_id=operator_id,
                decision="blocked",
                approval_status=ApprovalStatus.blocked,
                blocker_codes=["SUPERVISUAL_OPERATOR_REJECTED"],
                evidence_refs=[
                    reason,
                    f"supervisual_variant:{variant.supervisual_variant_id}",
                    f"eval_receipt:{variant.eval_receipt.eval_receipt_id}",
                ],
            )
        )
        self.repository.variants[variant.supervisual_variant_id] = variant.model_copy(update={"status": "blocked"})
        self.repository.projects[project_id] = project.model_copy(
            update={
                "status": "blocked",
                "blocker_codes": receipt.blocker_codes,
                "updated_at": utc_now(),
            }
        )
        self._event(
            project_id=project_id,
            event_kind="approval_decided",
            object_ref=f"supervisual_approval_receipt:{receipt.supervisual_approval_receipt_id}",
            summary="Operator rejected SuperVisual variant.",
            evidence_refs=receipt.evidence_refs,
            blocker_codes=receipt.blocker_codes,
        )
        return receipt

    def export_project(self, *, project_id: UUID, variant_id: UUID | None = None) -> SuperVisualExportArtifact:
        project = self.get_project(project_id=project_id)
        variant = self._active_variant(project, variant_id=variant_id)
        approvals = [
            receipt
            for receipt in self.repository.approval_receipts.values()
            if receipt.project_id == project_id and receipt.variant_id == variant.supervisual_variant_id and receipt.decision == "approved"
        ]
        if not approvals:
            raise SuperVisualProjectServiceError("SUPERVISUAL_APPROVAL_REQUIRED", "SuperVisual export requires an approved variant.")
        artifact_hash = supervisual_hash({"project_id": project_id, "variant_id": variant.supervisual_variant_id, "render_hash": variant.render_contract.render_hash})
        artifact = self.repository.put_export_artifact(
            SuperVisualExportArtifact(
                project_id=project_id,
                variant_id=variant.supervisual_variant_id,
                artifact_ref=f"artifact://supervisual/{project_id}/{artifact_hash[:20]}.png",
                render_ref=variant.render_contract.render_ref,
                approval_receipt_ref=f"supervisual_approval_receipt:{approvals[-1].supervisual_approval_receipt_id}",
            )
        )
        next_project = project.model_copy(
            update={
                "status": "exported",
                "export_artifact_refs": [*project.export_artifact_refs, artifact.artifact_ref],
                "updated_at": utc_now(),
            }
        )
        self.repository.projects[project_id] = next_project
        self.repository.variants[variant.supervisual_variant_id] = variant.model_copy(update={"status": "exported"})
        self._event(
            project_id=project_id,
            event_kind="export_created",
            object_ref=f"supervisual_export_artifact:{artifact.supervisual_export_artifact_id}",
            summary="Stored SuperVisual export artifact reference.",
            evidence_refs=[artifact.render_ref, artifact.approval_receipt_ref],
        )
        return artifact

    def get_timeline(self, *, project_id: UUID) -> SuperVisualTimelineReadModel:
        project = self.get_project(project_id=project_id)
        events = self.repository.timeline_events.get(project_id, [])
        approval_blockers: list[str] = []
        if project.active_variant_id and project.active_variant_id in self.repository.variants:
            approval_blockers = self.repository.variants[project.active_variant_id].eval_receipt.blocker_codes
        return SuperVisualTimelineReadModel(
            project_id=project_id,
            active_variant_id=project.active_variant_id,
            events=events,
            variant_refs=[f"supervisual_variant:{variant_id}" for variant_id in project.variant_ids],
            export_artifact_refs=project.export_artifact_refs,
            approval_blockers=approval_blockers,
        )

    def _create_variant(
        self,
        *,
        project: SuperVisualProject,
        frame_profile_code: str,
        style_route_code: str,
        revision_instruction: str | None,
        revision_number: int,
        primitive_score: float,
        doctrine_score: float,
        source_truth_score: float,
        frame_profile_score: float,
        style_route_score: float,
        event_kind: str,
    ) -> SuperVisualVariant:
        frame_profile = self._delivery_frame(frame_profile_code)
        style_route = self._style_route(style_route_code)
        primitive_binding = self._primitive_binding(project)
        self._validate_provider_preconditions(project=project, primitive_binding=primitive_binding, frame_profile=frame_profile, style_route=style_route)
        composition_receipt, layer_plan = self._composition_and_layers(
            project=project,
            frame_profile=frame_profile,
            style_route=style_route,
            primitive_binding=primitive_binding,
            revision_instruction=revision_instruction,
        )
        provider_receipts = [
            self._fake_provider_receipt(
                provider_code=provider_code,
                project=project,
                frame_profile=frame_profile,
                style_route=style_route,
                revision_number=revision_number,
                revision_instruction=revision_instruction,
            )
            for provider_code in ("ideogram_4", "qwen_layered", "sam3", "skia_renderer")
        ]
        render_contract = self._render_contract(project=project, frame_profile=frame_profile, provider_receipts=provider_receipts)
        eval_receipt = self._eval_receipt(
            project_id=project.supervisual_project_id,
            revision_number=revision_number,
            primitive_score=primitive_score,
            doctrine_score=doctrine_score,
            source_truth_score=source_truth_score,
            frame_profile_score=frame_profile_score,
            style_route_score=style_route_score,
        )
        variant_hash = supervisual_hash(
            {
                "project_id": project.supervisual_project_id,
                "revision_number": revision_number,
                "composition_hash": composition_receipt.composition_hash,
                "render_hash": render_contract.render_hash,
                "eval_hash": eval_receipt.eval_receipt_hash,
            }
        )
        variant = self.repository.put_variant(
            SuperVisualVariant(
                project_id=project.supervisual_project_id,
                revision_number=revision_number,
                revision_instruction=revision_instruction,
                status="built" if eval_receipt.decision == "approved" else "eval_failed",
                context=project.context,
                primitive_binding=primitive_binding,
                frame_profile=frame_profile,
                style_route=style_route,
                composition_receipt=composition_receipt,
                layer_plan=layer_plan,
                provider_receipts=provider_receipts,
                render_contract=render_contract,
                eval_receipt=eval_receipt,
                deterministic_variant_hash=variant_hash,
            )
        )
        next_project = project.model_copy(
            update={
                "status": "built" if eval_receipt.decision == "approved" else "blocked",
                "variant_ids": [*project.variant_ids, variant.supervisual_variant_id],
                "active_variant_id": variant.supervisual_variant_id,
                "blocker_codes": eval_receipt.blocker_codes,
                "updated_at": utc_now(),
            }
        )
        self.repository.projects[project.supervisual_project_id] = next_project
        self._event(
            project_id=project.supervisual_project_id,
            event_kind=event_kind,  # type: ignore[arg-type]
            object_ref=f"supervisual_variant:{variant.supervisual_variant_id}",
            summary="SuperVisual variant built from canonical context, primitive binding, frame profile, and style route.",
            evidence_refs=[composition_receipt.composition_id, render_contract.render_ref, f"eval_receipt:{eval_receipt.eval_receipt_id}"],
            blocker_codes=eval_receipt.blocker_codes,
        )
        return variant

    def _delivery_frame(self, frame_profile_code: str) -> FrameProfile:
        try:
            return self.convergence.validate_frame_profile_for_short_form(frame_profile_code)
        except (ContractConvergenceServiceError, ValueError) as exc:
            raise SuperVisualProjectServiceError("SUPERVISUAL_FRAME_PROFILE_REJECTED", str(exc)) from exc

    @staticmethod
    def _style_route(style_route_code: str) -> StyleRoute:
        try:
            return next(route for route in DEFAULT_STYLE_ROUTES if route.route_code == style_route_code)
        except StopIteration as exc:
            raise SuperVisualProjectServiceError("SUPERVISUAL_STYLE_ROUTE_NOT_FOUND", style_route_code) from exc

    def _primitive_binding(self, project: SuperVisualProject) -> SuperVisualPrimitiveBinding:
        coalition = self.convergence.project_primitive_triad_to_coalition(
            meaning_transform="PRM-SOURCE-TRUTH",
            delivery_shape="PRM-VISUAL-TENSION",
            format_material="PRM-EDITABLE-LAYER-PLAN",
            coalition_intent="Build a SuperVisual that transforms source context into an inspectable single-image composition.",
            source_context_refs={
                "brand_context_version_ref": project.context.brand_context_version_ref,
                "primary_source_evidence_ref": project.context.source_evidence_refs[0],
            },
        )
        primitive_refs = [binding.primitive_id for binding in coalition.primary_bindings]
        payload = {
            "coalition": str(coalition.primitive_coalition_contract_id),
            "primitive_refs": primitive_refs,
            "project_id": str(project.supervisual_project_id),
        }
        return SuperVisualPrimitiveBinding(
            primitive_coalition_contract_id=str(coalition.primitive_coalition_contract_id),
            primitive_refs=primitive_refs,
            evaluation_target_refs=[
                f"eval_target:primitive:{project.supervisual_project_id}",
                f"eval_target:doctrine:{project.supervisual_project_id}",
                f"eval_target:source_truth:{project.supervisual_project_id}",
            ],
            source_context_refs=coalition.source_context_refs,
            binding_hash=supervisual_hash(payload),
        )

    def _validate_provider_preconditions(
        self,
        *,
        project: SuperVisualProject,
        primitive_binding: SuperVisualPrimitiveBinding,
        frame_profile: FrameProfile,
        style_route: StyleRoute,
    ) -> None:
        source_reference = SourceReference(
            kind=SourceReferenceKind.transcript_quote if project.context.transcript_ref else SourceReferenceKind.source_language,
            source_ref=project.context.source_evidence_refs[0],
            rights_status="direct_use_allowed",
            description="Source-backed SuperVisual production reference.",
        )
        mode = SourceReferenceMode.direct_real_reference if style_route.requires_real_reference else SourceReferenceMode.source_language_reference
        self.convergence.validate_provider_job_preconditions(
            source_reference=source_reference,
            style_route=style_route,
            frame_profile=FrameProfileCode(frame_profile.code.value),
            composition_role=CompositionRole.proof_insert,
            evaluation_requirements={"primitive_fit": 0.84, "source_truth": 0.84, "style_route_fit": 0.84},
            primitive_coalition_contract_id=primitive_binding.primitive_coalition_contract_id,
            source_reference_mode=mode,
        )

    def _composition_and_layers(
        self,
        *,
        project: SuperVisualProject,
        frame_profile: FrameProfile,
        style_route: StyleRoute,
        primitive_binding: SuperVisualPrimitiveBinding,
        revision_instruction: str | None,
    ) -> tuple[SuperVisualCompositionReceipt, SuperVisualLayerPlan]:
        source_ref = project.context.source_evidence_refs[0]
        layers = [
            SuperVisualLayerEntry(layer_id="background", role="premium_background", source_ref=f"style_route:{style_route.route_code}", z_index=0, editable=True),
            SuperVisualLayerEntry(layer_id="source-anchor", role="source_truth_anchor", source_ref=source_ref, z_index=10, editable=False, primitive_ref=primitive_binding.primitive_refs[0]),
            SuperVisualLayerEntry(layer_id="headline", role="claim_headline", source_ref="context_payload:primary_claim", z_index=20, editable=True, primitive_ref=primitive_binding.primitive_refs[1]),
            SuperVisualLayerEntry(layer_id="proof-detail", role="proof_or_contrast_detail", source_ref="context_payload:proof_detail", z_index=30, editable=True, primitive_ref=primitive_binding.primitive_refs[2]),
            SuperVisualLayerEntry(layer_id="brand-signature", role="brand_signature", source_ref=project.context.brand_context_version_ref, z_index=40, editable=True),
        ]
        layer_plan = SuperVisualLayerPlan(
            frame_profile_code=frame_profile.code.value,
            editable_fields=["headline", "proof-detail", "brand-signature", "style_route", "frame_profile"],
            layers=layers,
            composition_semantics={
                "meaning_transform": "source context becomes one inspectable visual claim",
                "delivery_shape": frame_profile.display_name,
                "format_material": "layered Skia-ready single-image SuperVisual",
            },
        )
        composition_json = {
            "frame_profile": frame_profile.model_dump(mode="json"),
            "style_route_code": style_route.route_code,
            "zones": [
                {"zone_id": "headline", "x": 0.08, "y": 0.08, "width": 0.84, "height": 0.22},
                {"zone_id": "source_anchor", "x": 0.08, "y": 0.32, "width": 0.84, "height": 0.42},
                {"zone_id": "signature", "x": 0.08, "y": 0.78, "width": 0.84, "height": 0.12},
            ],
            "layers": [layer.model_dump(mode="json") for layer in layers],
            "revision_instruction": revision_instruction,
        }
        composition_hash = supervisual_hash(composition_json)
        receipt = SuperVisualCompositionReceipt(
            composition_id=f"composition:supervisual:{project.supervisual_project_id}:{composition_hash[:12]}",
            composition_json=composition_json,
            source_lineage_refs=project.context.source_evidence_refs,
            decision_code="SUPERVISUAL_COMPOSITION_READY",
            composition_hash=composition_hash,
        )
        return receipt, layer_plan

    def _fake_provider_receipt(
        self,
        *,
        provider_code: str,
        project: SuperVisualProject,
        frame_profile: FrameProfile,
        style_route: StyleRoute,
        revision_number: int,
        revision_instruction: str | None,
    ) -> SuperVisualProviderReceipt:
        payload = {
            "provider_code": provider_code,
            "project_id": str(project.supervisual_project_id),
            "context": project.context.model_dump(mode="json"),
            "frame_profile": frame_profile.code.value,
            "style_route": style_route.route_code,
            "revision_number": revision_number,
            "revision_instruction": revision_instruction,
        }
        request_hash = supervisual_hash(payload)
        deterministic_seed = supervisual_hash({"request_hash": request_hash, "provider_code": provider_code})
        return SuperVisualProviderReceipt(
            provider_code=provider_code,  # type: ignore[arg-type]
            request_hash=request_hash,
            deterministic_seed=deterministic_seed,
            output_ref=f"fake-provider://{provider_code}/{deterministic_seed[:24]}",
            receipt_ref=f"provider_receipt:{provider_code}:{deterministic_seed[:24]}",
        )

    def _render_contract(
        self,
        *,
        project: SuperVisualProject,
        frame_profile: FrameProfile,
        provider_receipts: list[SuperVisualProviderReceipt],
    ) -> SuperVisualRenderContract:
        render_hash = supervisual_hash(
            {
                "project_id": project.supervisual_project_id,
                "frame_profile": frame_profile.code.value,
                "provider_outputs": [receipt.output_ref for receipt in provider_receipts],
                "runtime": "skia",
            }
        )
        return SuperVisualRenderContract(
            runtime_lock_ref="runtime_lock:skia:supervisual-v1",
            frame_profile_code=frame_profile.code.value,
            render_ref=f"render://supervisual/{project.supervisual_project_id}/{render_hash[:20]}.png",
            render_hash=render_hash,
        )

    @staticmethod
    def _eval_receipt(
        *,
        project_id: UUID,
        revision_number: int,
        primitive_score: float,
        doctrine_score: float,
        source_truth_score: float,
        frame_profile_score: float,
        style_route_score: float,
    ) -> SuperVisualEvalReceipt:
        threshold = 0.84
        scores = {
            "primitive_score": primitive_score,
            "doctrine_score": doctrine_score,
            "source_truth_score": source_truth_score,
            "frame_profile_score": frame_profile_score,
            "style_route_score": style_route_score,
        }
        blockers = [key.upper() + "_BELOW_THRESHOLD" for key, score in scores.items() if score < threshold]
        decision = "approved" if not blockers else "blocked"
        receipt_hash = supervisual_hash({"project_id": project_id, "revision_number": revision_number, **scores, "blockers": blockers})
        return SuperVisualEvalReceipt(
            target_variant_ref=f"supervisual_project:{project_id}:revision:{revision_number}",
            primitive_score=primitive_score,
            doctrine_score=doctrine_score,
            source_truth_score=source_truth_score,
            frame_profile_score=frame_profile_score,
            style_route_score=style_route_score,
            decision=decision,
            blocker_codes=blockers,
            eval_receipt_hash=receipt_hash,
        )

    def _active_variant(self, project: SuperVisualProject, *, variant_id: UUID | None = None) -> SuperVisualVariant:
        resolved_variant_id = variant_id or project.active_variant_id
        if resolved_variant_id is None:
            raise SuperVisualProjectServiceError("SUPERVISUAL_VARIANT_REQUIRED", "Project has no active SuperVisual variant.")
        try:
            return self.repository.variants[resolved_variant_id]
        except KeyError as exc:
            raise SuperVisualProjectServiceError("SUPERVISUAL_VARIANT_NOT_FOUND", str(resolved_variant_id)) from exc

    def _event(
        self,
        *,
        project_id: UUID,
        event_kind: str,
        object_ref: str,
        summary: str,
        evidence_refs: list[str],
        blocker_codes: list[str] | None = None,
    ) -> SuperVisualTimelineEvent:
        return self.repository.append_timeline_event(
            SuperVisualTimelineEvent(
                project_id=project_id,
                event_kind=event_kind,  # type: ignore[arg-type]
                object_ref=object_ref,
                summary=summary,
                evidence_refs=evidence_refs,
                blocker_codes=blocker_codes or [],
            )
        )
