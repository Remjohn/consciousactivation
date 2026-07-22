"""Ideogram 4 composition lineage service for TS-CMF-038."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.composition import (
    CompositionAnalysis,
    CompositionConstraints,
    CompositionJob,
    CompositionLineageAudit,
    CompositionOutputRequirements,
    CompositionPlate,
    CompositionReceipt,
    CompositionUsageState,
    DownstreamCompositionEdit,
    FinalTextPlan,
    IdeogramCompositionProviderResponse,
    IdeogramProviderReceipt,
    new_composition_receipt,
    stable_hash,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.scene_spec import SceneSpec
from ccp_studio.providers.ideogram import Ideogram4Adapter
from ccp_studio.repositories.composition import InMemoryCompositionRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


class CompositionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CompositionService:
    scene_spec_compiler: SceneSpecCompiler
    provider: Ideogram4Adapter = field(default_factory=Ideogram4Adapter)
    repository: InMemoryCompositionRepository = field(default_factory=InMemoryCompositionRepository)

    def compile_composition_job(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        constraints: dict[str, Any] | None = None,
        output_requirements: dict[str, Any] | None = None,
        final_text_plan: dict[str, Any] | None = None,
        command_id: UUID | None = None,
    ) -> CompositionJob:
        scene_spec = self._scene_spec(scene_spec_id)
        render_contract = self.scene_spec_compiler.render_contract_for_scene(scene_spec_id)
        composed_constraints = self._constraints(scene_spec, constraints)
        if not composed_constraints.text_area:
            self._blocked_receipt(scene_spec, actor_id, "TEXT_SPACE_REQUIRED", command_id)
            raise CompositionServiceError("TEXT_SPACE_REQUIRED", "Ideogram CompositionJob requires explicit text-space constraints.")
        output = self._output_requirements(scene_spec, output_requirements)
        job_id = uuid4()
        prompt = self._compiled_prompt(scene_spec, composed_constraints)
        prompt_hash = stable_hash({"compiled_prompt": prompt})
        job_hash_payload = {
            "composition_job_id": job_id,
            "scene_spec_id": scene_spec.scene_spec_id,
            "prompt_hash": prompt_hash,
            "constraints": composed_constraints.model_dump(mode="json"),
            "output_requirements": output.model_dump(mode="json"),
            "render_contract_id": render_contract.render_contract_id,
        }
        job = CompositionJob(
            schema_version="cmf.composition_job.v1",
            composition_job_id=job_id,
            complete_editing_session_id=scene_spec.complete_editing_session_id,
            scene_spec_id=scene_spec.scene_spec_id,
            compiled_prompt=prompt,
            prompt_hash=prompt_hash,
            constraints=composed_constraints,
            output_requirements=output,
            selected_brand_layer_refs=[str(item) for item in scene_spec.asset_selection_ids],
            job_json_hash=stable_hash(job_hash_payload),
            created_at=utc_now(),
        )
        text_plan = self.repository.put_final_text_plan(
            self._final_text_plan(
                composition_job_id=job.composition_job_id,
                scene_spec=scene_spec,
                request=final_text_plan,
            )
        )
        job = job.model_copy(update={"final_text_plan_id": text_plan.final_text_plan_id})
        self.repository.put_composition_job(job)
        self.repository.put_receipt(
            new_composition_receipt(
                organization_id=self._organization_id(scene_spec),
                brand_id=self._brand_id(scene_spec),
                actor_id=actor_id,
                complete_editing_session_id=scene_spec.complete_editing_session_id,
                scene_spec_id=scene_spec.scene_spec_id,
                composition_job_id=job.composition_job_id,
                composition_job_json_hash=job.job_json_hash,
                prompt_hash=job.prompt_hash,
                final_text_plan_id=text_plan.final_text_plan_id,
                decision_code="COMPOSITION_JOB_COMPILED",
                evidence_refs=[
                    f"scene_spec:{scene_spec.scene_spec_id}",
                    f"render_contract:{render_contract.render_contract_id}",
                    job.job_json_hash,
                    job.prompt_hash,
                ],
                command_id=command_id,
            )
        )
        return job

    def submit_ideogram_composition_job(
        self,
        *,
        composition_job_id: UUID,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> CompositionPlate:
        job = self._job(composition_job_id)
        scene_spec = self._scene_spec(job.scene_spec_id)
        response = self.provider.submit_composition_job(job)
        receipt = self.repository.put_provider_receipt(
            IdeogramProviderReceipt(
                schema_version="cmf.ideogram_provider_receipt.v1",
                provider_receipt_id=uuid4(),
                composition_job_id=job.composition_job_id,
                operation="submit_composition_plate",
                provider_correlation_id=response.provider_correlation_id,
                model_version=response.model_version,
                request_hash=job.job_json_hash,
                response_metadata=response.response_metadata,
                created_at=utc_now(),
            )
        )
        job = job.model_copy(
            update={
                "provider_correlation_id": response.provider_correlation_id,
                "provider_metadata": {"model_version": response.model_version, **response.response_metadata},
            }
        )
        self.repository.put_composition_job(job)
        analysis = self.repository.put_analysis(self._analysis(job, response))
        usage_state, usage_reason = self._usage_state(analysis)
        plate = self.repository.put_plate(
            CompositionPlate(
                schema_version="cmf.composition_plate.v1",
                composition_plate_id=uuid4(),
                composition_job_id=job.composition_job_id,
                plate_uri=response.plate_uri,
                plate_hash=response.plate_hash,
                provider_receipt_id=receipt.provider_receipt_id,
                composition_analysis_id=analysis.composition_analysis_id,
                usage_state=usage_state,
                usage_reason=usage_reason,
                created_at=utc_now(),
            )
        )
        self.repository.put_receipt(
            self._plate_receipt(
                scene_spec=scene_spec,
                job=job,
                plate=plate,
                analysis=analysis,
                provider_receipt=receipt,
                actor_id=actor_id,
                decision_code="COMPOSITION_PLATE_RECORDED",
                command_id=command_id,
            )
        )
        return plate

    def record_composition_plate(
        self,
        *,
        composition_job_id: UUID,
        plate_uri: str,
        plate_hash: str,
        analysis: dict[str, Any],
        provider_correlation_id: str,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> CompositionPlate:
        job = self._job(composition_job_id)
        response = IdeogramCompositionProviderResponse(
            schema_version="cmf.ideogram_composition_provider_response.v1",
            provider_correlation_id=provider_correlation_id,
            plate_uri=plate_uri,
            plate_hash=plate_hash,
            analysis=analysis,
        )
        original_provider = self.provider
        self.provider = Ideogram4Adapter(analysis_override=response.analysis)
        try:
            return self.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id, command_id=command_id)
        finally:
            self.provider = original_provider

    def evaluate_composition_boundary(
        self,
        *,
        composition_plate_id: UUID,
        actor_id: UUID,
        analysis_update: dict[str, Any] | None = None,
        command_id: UUID | None = None,
    ) -> CompositionPlate:
        plate = self._plate(composition_plate_id)
        analysis = self.repository.analyses[plate.composition_analysis_id]
        if analysis_update:
            analysis = analysis.model_copy(update=analysis_update | {"created_at": utc_now()})
            self.repository.put_analysis(analysis)
        usage_state, usage_reason = self._usage_state(analysis)
        updated = plate.model_copy(update={"usage_state": usage_state, "usage_reason": usage_reason})
        self.repository.put_plate(updated)
        job = self._job(updated.composition_job_id)
        scene_spec = self._scene_spec(job.scene_spec_id)
        provider_receipt = self.repository.provider_receipts[updated.provider_receipt_id]
        self.repository.put_receipt(
            self._plate_receipt(
                scene_spec=scene_spec,
                job=job,
                plate=updated,
                analysis=analysis,
                provider_receipt=provider_receipt,
                actor_id=actor_id,
                decision_code="COMPOSITION_BOUNDARY_EVALUATED",
                command_id=command_id,
            )
        )
        return updated

    def restrict_composition_plate_use(
        self,
        *,
        composition_plate_id: UUID,
        usage_state: CompositionUsageState,
        reason: str,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> CompositionPlate:
        if usage_state == CompositionUsageState.approved_composition_plate:
            raise CompositionServiceError("RESTRICTION_STATE_REQUIRED", "Restriction command requires a non-approved usage state.")
        plate = self._plate(composition_plate_id).model_copy(update={"usage_state": usage_state, "usage_reason": reason})
        self.repository.put_plate(plate)
        job = self._job(plate.composition_job_id)
        scene_spec = self._scene_spec(job.scene_spec_id)
        self.repository.put_receipt(
            new_composition_receipt(
                organization_id=self._organization_id(scene_spec),
                brand_id=self._brand_id(scene_spec),
                actor_id=actor_id,
                complete_editing_session_id=scene_spec.complete_editing_session_id,
                scene_spec_id=scene_spec.scene_spec_id,
                composition_job_id=job.composition_job_id,
                composition_job_json_hash=job.job_json_hash,
                prompt_hash=job.prompt_hash,
                composition_plate_id=plate.composition_plate_id,
                plate_uri=plate.plate_uri,
                plate_hash=plate.plate_hash,
                provider_receipt_id=plate.provider_receipt_id,
                composition_analysis_id=plate.composition_analysis_id,
                usage_state=plate.usage_state,
                final_text_plan_id=job.final_text_plan_id,
                decision_code="COMPOSITION_PLATE_USE_RESTRICTED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )
        return plate

    def link_downstream_composition_edit(
        self,
        *,
        composition_plate_id: UUID,
        downstream_object_id: UUID,
        downstream_object_type: str,
        edit_type: str,
        reason: str,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> DownstreamCompositionEdit:
        plate = self._plate(composition_plate_id)
        job = self._job(plate.composition_job_id)
        scene_spec = self._scene_spec(job.scene_spec_id)
        edit = self.repository.put_downstream_edit(
            DownstreamCompositionEdit(
                schema_version="cmf.downstream_composition_edit.v1",
                downstream_composition_edit_id=uuid4(),
                composition_job_id=job.composition_job_id,
                composition_plate_id=plate.composition_plate_id,
                downstream_object_id=downstream_object_id,
                downstream_object_type=downstream_object_type,
                edit_type=edit_type,
                reason=reason,
                created_at=utc_now(),
            )
        )
        self.repository.put_receipt(
            new_composition_receipt(
                organization_id=self._organization_id(scene_spec),
                brand_id=self._brand_id(scene_spec),
                actor_id=actor_id,
                complete_editing_session_id=scene_spec.complete_editing_session_id,
                scene_spec_id=scene_spec.scene_spec_id,
                composition_job_id=job.composition_job_id,
                composition_job_json_hash=job.job_json_hash,
                prompt_hash=job.prompt_hash,
                composition_plate_id=plate.composition_plate_id,
                plate_uri=plate.plate_uri,
                plate_hash=plate.plate_hash,
                downstream_edit_ids=[edit.downstream_composition_edit_id],
                final_text_plan_id=job.final_text_plan_id,
                decision_code="DOWNSTREAM_COMPOSITION_EDIT_LINKED",
                evidence_refs=[f"downstream:{downstream_object_type}:{downstream_object_id}", reason],
                command_id=command_id,
            )
        )
        return edit

    def audit_composition_lineage(self, composition_job_id: UUID) -> CompositionLineageAudit:
        job = self._job(composition_job_id)
        plate = next((item for item in self.repository.plates.values() if item.composition_job_id == job.composition_job_id), None)
        analysis = self.repository.analyses.get(plate.composition_analysis_id) if plate else None
        edits = [item for item in self.repository.downstream_edits.values() if item.composition_job_id == job.composition_job_id]
        text_plan = self.repository.final_text_plans.get(job.final_text_plan_id) if job.final_text_plan_id else None
        return CompositionLineageAudit(
            schema_version="cmf.composition_lineage_audit.v1",
            composition_job=job,
            composition_plate=plate,
            composition_analysis=analysis,
            downstream_edits=edits,
            final_text_plan=text_plan,
        )

    def _constraints(self, scene_spec: SceneSpec, request: dict[str, Any] | None) -> CompositionConstraints:
        if request:
            return CompositionConstraints(schema_version="cmf.composition_constraints.v1", **request)
        text_area = scene_spec.subject.text_space or "upper_third_reserved_for_downstream_text"
        return CompositionConstraints(
            schema_version="cmf.composition_constraints.v1",
            aspect_ratio=scene_spec.aspect_ratio,
            subject_position=scene_spec.subject.position,
            text_area=text_area,
            visual_flow="source expression hook to visual hierarchy to downstream final text layer",
            style=scene_spec.visual_style,
            identity_boundary="Ideogram may suggest composition only; final identity is rebuilt from locked Brand Context assets downstream.",
            final_text_policy="Ideogram must leave text space; final editable text is rendered downstream.",
            micro_semiotic_anchor_ids=[],
        )

    def _output_requirements(self, scene_spec: SceneSpec, request: dict[str, Any] | None) -> CompositionOutputRequirements:
        if request:
            return CompositionOutputRequirements(schema_version="cmf.composition_output_requirements.v1", **request)
        brand_id = self._brand_id(scene_spec)
        return CompositionOutputRequirements(
            schema_version="cmf.composition_output_requirements.v1",
            storage_prefix=f"brands/{brand_id}/composition-plates",
            plate_format="png",
            layerability_required=True,
            composition_analysis_required=True,
            final_text_must_be_downstream=True,
            identity_must_be_rebuilt_downstream=True,
        )

    def _final_text_plan(self, *, composition_job_id: UUID, scene_spec: SceneSpec, request: dict[str, Any] | None) -> FinalTextPlan:
        request = request or {}
        return FinalTextPlan(
            schema_version="cmf.final_text_plan.v1",
            final_text_plan_id=uuid4(),
            composition_job_id=composition_job_id,
            text_content_ref=request.get("text_content_ref", f"source_expression_moment:{scene_spec.source_expression_moment_id}"),
            text_layer_strategy=request.get("text_layer_strategy", "render_downstream_editable_text_in_remotion_or_motion_canvas"),
            renderer_route=request.get("renderer_route", "remotion_text_layer"),
            editable_text_required=bool(request.get("editable_text_required", True)),
            approved_for_downstream_render=bool(request.get("approved_for_downstream_render", False)),
        )

    def _compiled_prompt(self, scene_spec: SceneSpec, constraints: CompositionConstraints) -> str:
        return (
            f"Create a composition plate for SceneSpec {scene_spec.scene_spec_id}. "
            f"Use {constraints.aspect_ratio}, place subject {constraints.subject_position}, reserve {constraints.text_area}. "
            f"Style: {constraints.style}. Visual flow: {constraints.visual_flow}. "
            f"Boundary: composition guidance only, no final identity render, no final baked text."
        )

    def _analysis(self, job: CompositionJob, response: IdeogramCompositionProviderResponse) -> CompositionAnalysis:
        data = response.analysis
        return CompositionAnalysis(
            schema_version="cmf.composition_analysis.v1",
            composition_analysis_id=uuid4(),
            composition_job_id=job.composition_job_id,
            text_space_score=float(data.get("text_space_score", 0.0)),
            identity_drift_score=float(data.get("identity_drift_score", 1.0)),
            baked_final_text_detected=bool(data.get("baked_final_text_detected", True)),
            layerability_score=float(data.get("layerability_score", 0.0)),
            style_fit_score=float(data.get("style_fit_score", 0.0)),
            visual_flow_score=float(data.get("visual_flow_score", 0.0)),
            boundary_notes=data.get("boundary_notes", []),
            created_at=utc_now(),
        )

    def _usage_state(self, analysis: CompositionAnalysis) -> tuple[CompositionUsageState, str]:
        if analysis.identity_drift_score >= 0.7:
            return CompositionUsageState.rejected, "Identity drift is too high for composition use."
        if analysis.baked_final_text_detected:
            return CompositionUsageState.background_only, "Plate contains final-looking text; downstream text remains authoritative."
        if analysis.text_space_score < 0.65 or analysis.layerability_score < 0.6 or analysis.style_fit_score < 0.6:
            return CompositionUsageState.repair_required, "Composition plate requires repair before downstream use."
        return CompositionUsageState.approved_composition_plate, "Composition plate approved as layout guidance only."

    def _plate_receipt(
        self,
        *,
        scene_spec: SceneSpec,
        job: CompositionJob,
        plate: CompositionPlate,
        analysis: CompositionAnalysis,
        provider_receipt: IdeogramProviderReceipt,
        actor_id: UUID,
        decision_code: str,
        command_id: UUID | None,
    ) -> CompositionReceipt:
        return new_composition_receipt(
            organization_id=self._organization_id(scene_spec),
            brand_id=self._brand_id(scene_spec),
            actor_id=actor_id,
            complete_editing_session_id=scene_spec.complete_editing_session_id,
            scene_spec_id=scene_spec.scene_spec_id,
            composition_job_id=job.composition_job_id,
            composition_job_json_hash=job.job_json_hash,
            prompt_hash=job.prompt_hash,
            composition_plate_id=plate.composition_plate_id,
            plate_uri=plate.plate_uri,
            plate_hash=plate.plate_hash,
            provider_receipt_id=provider_receipt.provider_receipt_id,
            composition_analysis_id=analysis.composition_analysis_id,
            usage_state=plate.usage_state,
            final_text_plan_id=job.final_text_plan_id,
            decision_code=decision_code,
            evidence_refs=[
                f"composition_job:{job.composition_job_id}",
                job.job_json_hash,
                job.prompt_hash,
                plate.plate_uri,
                plate.plate_hash,
                f"provider_receipt:{provider_receipt.provider_receipt_id}",
                f"analysis:{analysis.composition_analysis_id}",
            ],
            command_id=command_id,
        )

    def _blocked_receipt(self, scene_spec: SceneSpec, actor_id: UUID, reason: str, command_id: UUID | None) -> CompositionReceipt:
        return self.repository.put_receipt(
            new_composition_receipt(
                organization_id=self._organization_id(scene_spec),
                brand_id=self._brand_id(scene_spec),
                actor_id=actor_id,
                complete_editing_session_id=scene_spec.complete_editing_session_id,
                scene_spec_id=scene_spec.scene_spec_id,
                decision_code="COMPOSITION_JOB_BLOCKED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )

    def _scene_spec(self, scene_spec_id: UUID) -> SceneSpec:
        scene_spec = self.scene_spec_compiler.repository.scene_specs.get(scene_spec_id)
        if scene_spec is None:
            raise CompositionServiceError("SCENE_SPEC_REQUIRED", "SceneSpec is required for composition.")
        return scene_spec

    def _job(self, composition_job_id: UUID) -> CompositionJob:
        job = self.repository.composition_jobs.get(composition_job_id)
        if job is None:
            raise CompositionServiceError("COMPOSITION_JOB_REQUIRED", "CompositionJob is required.")
        return job

    def _plate(self, composition_plate_id: UUID) -> CompositionPlate:
        plate = self.repository.plates.get(composition_plate_id)
        if plate is None:
            raise CompositionServiceError("COMPOSITION_PLATE_REQUIRED", "CompositionPlate is required.")
        return plate

    def _organization_id(self, scene_spec: SceneSpec) -> UUID:
        if self.scene_spec_compiler.editing_session_service is None:
            raise CompositionServiceError("EDITING_SESSION_SERVICE_REQUIRED", "Editing Session service is required for organization scope.")
        return self.scene_spec_compiler.editing_session_service.repository.sessions[scene_spec.complete_editing_session_id].organization_id

    def _brand_id(self, scene_spec: SceneSpec) -> UUID:
        if self.scene_spec_compiler.editing_session_service is None:
            raise CompositionServiceError("EDITING_SESSION_SERVICE_REQUIRED", "Editing Session service is required for brand scope.")
        return self.scene_spec_compiler.editing_session_service.repository.sessions[scene_spec.complete_editing_session_id].brand_id


@dataclass
class CompositionCommandHandler:
    command_type: str
    service: CompositionService
    aggregate_type: str = "composition"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompileCompositionJobCommand":
            return self.service.compile_composition_job(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                constraints=payload.get("constraints"),
                output_requirements=payload.get("output_requirements"),
                final_text_plan=payload.get("final_text_plan"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "SubmitIdeogramCompositionJobCommand":
            return self.service.submit_ideogram_composition_job(
                composition_job_id=UUID(payload["composition_job_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RecordCompositionPlateCommand":
            return self.service.record_composition_plate(
                composition_job_id=UUID(payload["composition_job_id"]),
                plate_uri=payload["plate_uri"],
                plate_hash=payload["plate_hash"],
                analysis=payload["analysis"],
                provider_correlation_id=payload["provider_correlation_id"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "EvaluateCompositionBoundaryCommand":
            return self.service.evaluate_composition_boundary(
                composition_plate_id=UUID(payload["composition_plate_id"]),
                actor_id=envelope.actor.actor_id,
                analysis_update=payload.get("analysis_update"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RestrictCompositionPlateUseCommand":
            return self.service.restrict_composition_plate_use(
                composition_plate_id=UUID(payload["composition_plate_id"]),
                usage_state=CompositionUsageState(payload["usage_state"]),
                reason=payload["reason"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "LinkDownstreamCompositionEditCommand":
            return self.service.link_downstream_composition_edit(
                composition_plate_id=UUID(payload["composition_plate_id"]),
                downstream_object_id=UUID(payload["downstream_object_id"]),
                downstream_object_type=payload["downstream_object_type"],
                edit_type=payload["edit_type"],
                reason=payload["reason"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise CompositionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("composition_job_id") or payload.get("composition_plate_id") or payload.get("scene_spec_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_composition_command_handlers(bus: CommandBus, service: CompositionService) -> None:
    for command_type in [
        "CompileCompositionJobCommand",
        "SubmitIdeogramCompositionJobCommand",
        "RecordCompositionPlateCommand",
        "EvaluateCompositionBoundaryCommand",
        "RestrictCompositionPlateUseCommand",
        "LinkDownstreamCompositionEditCommand",
    ]:
        bus.register_handler(CompositionCommandHandler(command_type=command_type, service=service))
