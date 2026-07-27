from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover
    APIRouter = None  # type: ignore
    HTTPException = Exception  # type: ignore

from ccp_studio.contracts.supervisual_runtime import (
    ApproveSuperVisualVariantRequest,
    CreateSuperVisualCompositionHypothesesRequest,
    CreateSuperVisualProjectRequest,
    CreateSuperVisualVariantRequest,
    ExportSuperVisualVariantRequest,
    LockSuperVisualCompositionRequest,
    RecordProviderBlueprintRequest,
    RecordReceiptRequest,
    RunSuperVisualStepRequest,
    StartSuperVisualBuildRunRequest,
    SubmitSuperVisualRevisionRequest,
    SuperVisualCommand,
    SuperVisualCommandRequest,
    SuperVisualVariantStatus,
    UpdateSuperVisualProjectRequest,
    reject_delivery_frame_profile,
)
from ccp_studio.repositories.supervisual_runtime import JsonFileSuperVisualRuntimeRepository
from ccp_studio.services.supervisual_runtime_service import SuperVisualRuntimeService


def create_supervisual_runtime_router(service: SuperVisualRuntimeService | None = None):
    if APIRouter is None:
        raise RuntimeError("FastAPI is required to create the SuperVisual runtime router")

    runtime = service or SuperVisualRuntimeService(JsonFileSuperVisualRuntimeRepository())
    router = APIRouter(prefix="/api/v1/supervisual", tags=["supervisual-runtime"])

    def handle(fn):
        try:
            return fn()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    def run_runtime_step(variant_id: str, step_name: str, request, *, output_refs: list[str] | None = None, receipt_refs: list[str] | None = None):
        active_runs = runtime.repository.list_active_build_runs(variant_id)
        run = active_runs[0] if active_runs else runtime.start_build_run(
            variant_id,
            requested_steps=[step_name],
            actor_id=getattr(request, "actor_id", None),
        )
        return runtime.run_step(
            run.supervisual_build_run_id,
            step_name,
            output_refs=output_refs or [],
            receipt_refs=receipt_refs or [],
            actor_id=getattr(request, "actor_id", None),
        )

    @router.post("/projects")
    def create_project(request: CreateSuperVisualProjectRequest):
        return handle(lambda: runtime.create_project(
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
            title=request.title,
            source_context_refs=request.source_context_refs,
            target_platforms=request.target_platforms,
            default_frame_profile=request.default_frame_profile,
            created_by_actor_id=request.created_by_actor_id or request.actor_id,
            create_initial_variant=request.create_initial_variant,
        ))

    @router.get("/projects")
    def list_projects(brand_id: str | None = None):
        return handle(lambda: runtime.list_projects(brand_id=brand_id))

    @router.get("/projects/{project_id}")
    def get_project_detail(project_id: str):
        return handle(lambda: runtime.get_project_detail(project_id))

    @router.patch("/projects/{project_id}")
    def update_project(project_id: str, request: UpdateSuperVisualProjectRequest):
        def _update():
            project = runtime.repository.get_project(project_id)
            if request.brand_context_version_id and request.brand_context_version_id != project.brand_context_version_id:
                raise ValueError("brand_context_version_id is immutable after project creation")
            if request.default_frame_profile:
                reject_delivery_frame_profile(request.default_frame_profile)
                project.default_frame_profile = request.default_frame_profile
            if request.title is not None:
                project.title = request.title
            if request.source_context_refs is not None:
                project.source_context_refs = request.source_context_refs
            if request.target_platforms is not None:
                project.target_platforms = request.target_platforms
            runtime.repository.update_project(project)
            runtime.append_event(project_id, None, project.brand_id, project.brand_context_version_id, "project.updated", request.actor_id, {"title": project.title})
            return project
        return handle(_update)

    @router.post("/projects/{project_id}/variants")
    def create_variant(project_id: str, request: CreateSuperVisualVariantRequest):
        return handle(lambda: runtime.create_variant(
            project_id,
            variant_label=request.variant_label,
            frame_profile=request.frame_profile,
            actor_id=request.actor_id,
            clone_from_variant_id=request.clone_from_variant_id,
        ))

    @router.get("/projects/{project_id}/variants")
    def list_variants(project_id: str):
        return handle(lambda: runtime.list_variants(project_id))

    @router.get("/variants/{variant_id}")
    def get_variant_detail(variant_id: str):
        return handle(lambda: runtime.get_variant_detail(variant_id))

    @router.post("/variants/{variant_id}/clone")
    def clone_variant(variant_id: str, request: CreateSuperVisualVariantRequest):
        def _clone():
            source = runtime.repository.get_variant(variant_id)
            return runtime.create_variant(
                source.supervisual_project_id,
                variant_label=request.variant_label,
                frame_profile=request.frame_profile or source.frame_profile,
                actor_id=request.actor_id,
                clone_from_variant_id=variant_id,
            )
        return handle(_clone)

    @router.post("/variants/{variant_id}/build-runs")
    def start_build_run(variant_id: str, request: StartSuperVisualBuildRunRequest):
        return handle(lambda: runtime.start_build_run(
            variant_id,
            run_mode=request.run_mode,
            requested_steps=request.requested_steps,
            actor_id=request.actor_id,
        ))

    @router.get("/build-runs/{build_run_id}")
    def get_build_run(build_run_id: str):
        return handle(lambda: runtime.get_build_run(build_run_id))

    @router.post("/build-runs/{build_run_id}/steps/{step_name}/run")
    def run_step(build_run_id: str, step_name: str, request: RunSuperVisualStepRequest):
        return handle(lambda: runtime.run_step(
            build_run_id,
            step_name,
            input_refs=request.input_refs,
            output_refs=request.output_refs,
            receipt_refs=request.receipt_refs,
            target_status=request.target_status,
            actor_id=request.actor_id,
        ))

    @router.get("/variants/{variant_id}/snapshot")
    def get_latest_snapshot(variant_id: str):
        return handle(lambda: runtime.repository.get_latest_snapshot(variant_id))

    @router.get("/variants/{variant_id}/events")
    def list_events(variant_id: str):
        return handle(lambda: runtime.list_events(variant_id))

    @router.post("/variants/{variant_id}/composition/hypotheses")
    def create_composition_hypotheses(variant_id: str, request: CreateSuperVisualCompositionHypothesesRequest):
        def _create():
            step = run_runtime_step(variant_id, "composition_hypotheses", request)
            options = request.composition_options or [
                {
                    "composition_hypothesis_id": f"composition_decision:{variant_id}",
                    "title": "Runtime composition option",
                    "description": "Generated by the SuperVisual runtime shell for operator locking.",
                    "step_run_id": step.supervisual_step_run_id,
                }
            ]
            runtime.save_snapshot(variant_id, step="composition.hypotheses", display_payload={"composition_options": options})
            return runtime.get_variant_detail(variant_id)
        return handle(_create)

    @router.post("/variants/{variant_id}/composition/lock")
    def lock_composition(variant_id: str, request: LockSuperVisualCompositionRequest):
        return handle(lambda: runtime.lock_composition(
            variant_id,
            composition_decision_receipt_id=request.composition_decision_receipt_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/provider-blueprints")
    def record_provider_blueprint(variant_id: str, request: RecordProviderBlueprintRequest):
        return handle(lambda: runtime.record_provider_blueprint(
            variant_id,
            request.provider_job_blueprint_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/materialize")
    def materialize_variant(variant_id: str, request: RecordReceiptRequest):
        return handle(lambda: runtime.record_provider_receipt(
            variant_id,
            request.receipt_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/render-contract")
    def record_render_contract(variant_id: str, request: RecordReceiptRequest):
        def _record():
            variant = runtime.repository.get_variant(variant_id)
            runtime.assert_mutable(variant)
            if not runtime.status_at_least(variant.status, SuperVisualVariantStatus.COMPOSITION_LOCKED):
                raise ValueError("Cannot compile render contract before composition lock")
            variant.lineage.render_contract_id = request.receipt_id
            variant.status = SuperVisualVariantStatus.RENDER_READY
            runtime.repository.update_variant(variant)
            runtime.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "render.contract.created", request.actor_id, {"render_contract_id": request.receipt_id})
            runtime.save_snapshot(variant_id, step="render_contract", display_payload={"render_contract_id": request.receipt_id})
            return variant
        return handle(_record)

    @router.post("/variants/{variant_id}/render")
    def record_render(variant_id: str, request: RecordReceiptRequest):
        return handle(lambda: runtime.record_render_receipt(
            variant_id,
            request.receipt_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/evaluate")
    def record_eval(variant_id: str, request: RecordReceiptRequest):
        return handle(lambda: runtime.record_eval_receipt(
            variant_id,
            request.receipt_id,
            passed=request.passed,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/revisions")
    def submit_revision(variant_id: str, request: SubmitSuperVisualRevisionRequest):
        return handle(lambda: runtime.apply_revision(
            variant_id,
            revision_note=request.revision_note,
            actor_id=request.actor_id,
        ))

    @router.get("/variants/{variant_id}/revisions")
    def list_revisions(variant_id: str):
        def _list():
            return [
                event
                for event in runtime.list_events(variant_id)
                if event.event_type == "revision.requested"
            ]
        return handle(_list)

    @router.post("/variants/{variant_id}/approve")
    def approve_variant(variant_id: str, request: ApproveSuperVisualVariantRequest):
        return handle(lambda: runtime.approve_variant(
            variant_id,
            approval_receipt_id=request.approval_receipt_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/export")
    def export_variant(variant_id: str, request: ExportSuperVisualVariantRequest):
        return handle(lambda: runtime.create_export_pack(
            variant_id,
            export_pack_id=request.export_pack_id,
            actor_id=request.actor_id,
        ))

    @router.post("/variants/{variant_id}/commands")
    def execute_command(variant_id: str, request: SuperVisualCommandRequest):
        variant = runtime.repository.get_variant(variant_id)
        command = SuperVisualCommand(
            command_type=request.command_type,
            target_type=request.target_type,
            target_id=request.target_id,
            supervisual_project_id=variant.supervisual_project_id,
            supervisual_variant_id=variant_id,
            actor_id=request.actor_id,
            idempotency_key=request.idempotency_key,
            payload=request.payload,
        )
        return handle(lambda: runtime.execute_command(command))

    return router


router = create_supervisual_runtime_router()
