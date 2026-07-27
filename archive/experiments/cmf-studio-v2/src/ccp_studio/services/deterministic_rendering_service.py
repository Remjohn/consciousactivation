"""Deterministic Remotion and Motion Canvas rendering service for TS-CMF-043."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.assembly import AssemblyPlan
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.deterministic_rendering import (
    DeterministicRenderer,
    DeterministicRenderJob,
    DeterministicRenderStatus,
    RendererPropsBundle,
    RendererRouteDecision,
    RenderOutput,
    RenderReceipt,
    deterministic_render_hash,
    deterministic_renderer_typescript_contract,
    new_render_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.scene_spec import RenderContract, SceneSpec
from ccp_studio.repositories.deterministic_rendering import InMemoryDeterministicRenderRepository
from ccp_studio.services.assembly_planner import AssemblyPlanner
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.composition_service import CompositionService
from ccp_studio.services.provider_operations_service import ProviderOperationsService
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


class DeterministicRenderError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class DeterministicRenderService:
    scene_spec_compiler: SceneSpecCompiler
    assembly_planner: AssemblyPlanner
    composition_service: CompositionService
    provider_operations: ProviderOperationsService
    repository: InMemoryDeterministicRenderRepository = field(default_factory=InMemoryDeterministicRenderRepository)

    def __post_init__(self) -> None:
        if not self.provider_operations.repository.capabilities:
            self.provider_operations.seed_current_cmf_capabilities()

    def select_renderer(
        self,
        *,
        render_contract_id: UUID,
        assembly_plan_id: UUID,
        preferred_renderer: DeterministicRenderer | str | None = None,
    ) -> RendererRouteDecision:
        render_contract = self._render_contract(render_contract_id)
        assembly_plan = self._assembly_plan(assembly_plan_id)
        if assembly_plan.scene_spec_id != render_contract.scene_spec_id:
            raise DeterministicRenderError("ASSEMBLY_RENDER_CONTRACT_MISMATCH", "Assembly plan must belong to the RenderContract scene.")
        renderer = self._renderer(render_contract, preferred_renderer)
        decision = RendererRouteDecision(
            schema_version="cmf.renderer_route_decision.v1",
            renderer_route_decision_id=uuid4(),
            render_contract_id=render_contract.render_contract_id,
            renderer=renderer,
            decision_reason=f"{renderer.value} selected from Python RenderContract route {render_contract.renderer_route}.",
            input_manifest_ids=[
                assembly_plan.layer_manifest_id,
                assembly_plan.animation_plan_id,
                assembly_plan.timeline_manifest_id,
                assembly_plan.caption_manifest_id,
                assembly_plan.audio_mix_manifest_id,
            ],
            created_at=utc_now(),
        )
        return self.repository.put_route_decision(decision)

    def build_renderer_props_bundle(
        self,
        *,
        render_contract_id: UUID,
        assembly_plan_id: UUID,
        actor_id: UUID,
        preferred_renderer: DeterministicRenderer | str | None = None,
        command_id: UUID | None = None,
    ) -> RendererPropsBundle:
        render_contract = self._render_contract(render_contract_id)
        scene_spec = self._scene_spec(render_contract.scene_spec_id)
        assembly_plan = self._assembly_plan(assembly_plan_id)
        decision = self.select_renderer(
            render_contract_id=render_contract.render_contract_id,
            assembly_plan_id=assembly_plan.assembly_plan_id,
            preferred_renderer=preferred_renderer,
        )
        try:
            session = self._session(scene_spec)
            brand_context = self.scene_spec_compiler.gate_service.brand_context_service.assert_context_selectable_for_production(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                brand_context_version_id=scene_spec.brand_context_version_id,
            )
            layer_manifest = self.assembly_planner.repository.layer_manifests[assembly_plan.layer_manifest_id]
            animation_plan = self.assembly_planner.repository.animation_plans[assembly_plan.animation_plan_id]
            timeline = self.assembly_planner.repository.timeline_manifests[assembly_plan.timeline_manifest_id]
            captions = self.assembly_planner.repository.caption_manifests[assembly_plan.caption_manifest_id]
            audio = self.assembly_planner.repository.audio_mix_manifests[assembly_plan.audio_mix_manifest_id]
            final_text_plan = self._final_text_plan(scene_spec)
            self._validate_brand_layers(scene_spec, layer_manifest.layers)
            variants = [self.scene_spec_compiler.repository.platform_variants[item] for item in scene_spec.platform_variant_ids]
            props_payload = {
                "domain_authority": "python_pydantic_contracts",
                "renderer_boundary": f"{decision.renderer.value}_typescript_leaf_runtime",
                "render_contract": render_contract.model_dump(mode="json"),
                "layer_manifest": layer_manifest.model_dump(mode="json"),
                "animation_plan": animation_plan.model_dump(mode="json"),
                "timeline_manifest": timeline.model_dump(mode="json"),
                "caption_manifest": captions.model_dump(mode="json"),
                "audio_mix_manifest": audio.model_dump(mode="json"),
                "final_text": {
                    "final_text_plan_id": str(final_text_plan.final_text_plan_id),
                    "text_content_ref": final_text_plan.text_content_ref,
                    "text_layer_strategy": final_text_plan.text_layer_strategy,
                    "renderer_route": final_text_plan.renderer_route,
                    "rendered_by": decision.renderer.value,
                    "provider_image_text_allowed": False,
                },
                "platform_variants": [item.model_dump(mode="json") for item in variants],
                "brand_context": {
                    "brand_context_version_id": str(brand_context.brand_context_version_id),
                    "brand_context_version_hash": brand_context.version_hash,
                    "rig_manifest_id": str(brand_context.asset_bundle.rig_manifest_id),
                    "motion_recipe_ids": [str(item) for item in brand_context.asset_bundle.motion_recipe_ids],
                    "sfx_asset_ids": [str(item) for item in brand_context.asset_bundle.sfx_asset_ids],
                },
            }
            ts_contract = deterministic_renderer_typescript_contract()
            props_hash = deterministic_render_hash(props_payload)
            bundle = self.repository.put_props_bundle(
                RendererPropsBundle(
                    schema_version="cmf.renderer_props_bundle.v1",
                    renderer_props_bundle_id=uuid4(),
                    render_contract_id=render_contract.render_contract_id,
                    assembly_plan_id=assembly_plan.assembly_plan_id,
                    renderer=decision.renderer,
                    layer_manifest_id=layer_manifest.layer_manifest_id,
                    animation_plan_id=animation_plan.animation_plan_id,
                    timeline_manifest_id=timeline.timeline_manifest_id,
                    caption_manifest_id=captions.caption_manifest_id,
                    audio_mix_manifest_id=audio.audio_mix_manifest_id,
                    final_text_plan_id=final_text_plan.final_text_plan_id,
                    brand_context_version_id=scene_spec.brand_context_version_id,
                    rig_manifest_id=brand_context.asset_bundle.rig_manifest_id,
                    selected_brand_layer_ids=[item for item in assembly_plan.selected_asset_ids],
                    motion_recipe_ids=brand_context.asset_bundle.motion_recipe_ids,
                    sfx_asset_ids=brand_context.asset_bundle.sfx_asset_ids,
                    platform_variant_ids=scene_spec.platform_variant_ids,
                    props_payload=props_payload,
                    props_hash=props_hash,
                    generated_typescript_contract_ref="src/ccp_studio/generated/typescript/deterministic_renderer_props.ts",
                    generated_typescript_contract_hash=deterministic_render_hash(ts_contract),
                    built_at=utc_now(),
                )
            )
            self.repository.put_receipt(
                new_render_receipt(
                    actor_id=actor_id,
                    render_contract_id=render_contract.render_contract_id,
                    renderer_props_bundle_id=bundle.renderer_props_bundle_id,
                    renderer=bundle.renderer,
                    props_hash=bundle.props_hash,
                    input_manifest_hashes=list(assembly_plan.manifest_hashes.values()),
                    final_text_plan_id=bundle.final_text_plan_id,
                    decision_code="RENDERER_PROPS_BUNDLE_BUILT",
                    evidence_refs=[bundle.props_hash, bundle.generated_typescript_contract_ref],
                    command_id=command_id,
                )
            )
            return bundle
        except Exception as exc:
            code = getattr(exc, "code", "RENDERER_PROPS_INVALID")
            self.repository.put_receipt(
                new_render_receipt(
                    actor_id=actor_id,
                    render_contract_id=render_contract.render_contract_id,
                    renderer=decision.renderer,
                    retry_count=0,
                    decision_code="DETERMINISTIC_RENDER_BLOCKED",
                    evidence_refs=[code],
                    command_id=command_id,
                )
            )
            if isinstance(exc, DeterministicRenderError):
                raise
            raise DeterministicRenderError(code, str(exc)) from exc

    def validate_renderer_inputs(self, renderer_props_bundle_id: UUID) -> RendererPropsBundle:
        bundle = self._props_bundle(renderer_props_bundle_id)
        scene_spec = self._scene_spec(self._render_contract(bundle.render_contract_id).scene_spec_id)
        layer_manifest = self.assembly_planner.repository.layer_manifests[bundle.layer_manifest_id]
        self._validate_brand_layers(scene_spec, layer_manifest.layers)
        if bundle.props_payload["final_text"].get("provider_image_text_allowed") is not False:
            raise DeterministicRenderError("FINAL_TEXT_DETERMINISTIC_RENDER_REQUIRED", "Final text must be rendered by deterministic renderer.")
        return bundle

    def start_deterministic_render(
        self,
        *,
        renderer_props_bundle_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        retry_count: int = 0,
        command_id: UUID | None = None,
    ) -> RenderOutput:
        bundle = self.validate_renderer_inputs(renderer_props_bundle_id)
        existing_output = self.repository.output_for_props_bundle(bundle.renderer_props_bundle_id)
        if existing_output is not None:
            self.repository.put_receipt(
                new_render_receipt(
                    actor_id=actor_id,
                    render_contract_id=bundle.render_contract_id,
                    renderer_props_bundle_id=bundle.renderer_props_bundle_id,
                    deterministic_render_job_id=existing_output.deterministic_render_job_id,
                    render_output_id=existing_output.render_output_id,
                    provider_receipt_id=existing_output.provider_receipt_id,
                    renderer=bundle.renderer,
                    props_hash=bundle.props_hash,
                    input_manifest_hashes=existing_output.manifest_hashes,
                    renderer_version=existing_output.renderer_version,
                    output_hashes=[existing_output.output_hash],
                    final_text_plan_id=bundle.final_text_plan_id,
                    retry_count=retry_count,
                    decision_code="DETERMINISTIC_RENDER_REPLAYED",
                    evidence_refs=["completed_artifact_preserved_across_retry", existing_output.output_hash],
                    command_id=command_id,
                )
            )
            return existing_output
        prior = self.repository.job_for_idempotency(idempotency_key)
        if prior is not None:
            prior_output = next((item for item in self.repository.outputs.values() if item.deterministic_render_job_id == prior.deterministic_render_job_id), None)
            if prior_output is not None:
                return prior_output
        session = self._session(self._scene_spec(self._render_contract(bundle.render_contract_id).scene_spec_id))
        capability_id = self._provider_capability_id(bundle.renderer)
        manifest_hashes = self._manifest_hashes(bundle)
        provider_receipt = self.provider_operations.execute_provider_job(
            provider_capability_id=capability_id,
            organization_id=session.organization_id,
            brand_id=session.brand_id,
            requested_by_actor_id=actor_id,
            complete_editing_session_id=session.complete_editing_session_id,
            scene_spec_id=self._render_contract(bundle.render_contract_id).scene_spec_id,
            input_artifact_hashes=[bundle.props_hash, *manifest_hashes],
            input_types=self._provider_input_types(bundle.renderer),
            parameters={"estimated_cost_amount": 0.0, "deterministic_renderer": bundle.renderer.value},
            idempotency_key=f"provider:{idempotency_key}",
        )
        job = self.repository.put_job(
            DeterministicRenderJob(
                schema_version="cmf.deterministic_render_job.v1",
                deterministic_render_job_id=uuid4(),
                renderer_props_bundle_id=bundle.renderer_props_bundle_id,
                render_contract_id=bundle.render_contract_id,
                renderer=bundle.renderer,
                status=DeterministicRenderStatus.running,
                idempotency_key=idempotency_key,
                retry_count=retry_count,
                provider_job_id=provider_receipt.provider_job_id,
                started_at=utc_now(),
            )
        )
        output_hash = deterministic_render_hash(
            {
                "renderer": bundle.renderer.value,
                "props_hash": bundle.props_hash,
                "manifest_hashes": manifest_hashes,
                "final_text_plan_id": bundle.final_text_plan_id,
                "retry_count": retry_count,
            }
        )
        output = self.repository.put_output(
            RenderOutput(
                schema_version="cmf.render_output.v1",
                render_output_id=uuid4(),
                deterministic_render_job_id=job.deterministic_render_job_id,
                render_contract_id=bundle.render_contract_id,
                renderer=bundle.renderer,
                preview_uri=f"object://renders/{bundle.render_contract_id}/{bundle.renderer.value}/{job.deterministic_render_job_id}.preview.mp4",
                final_uri=f"object://renders/{bundle.render_contract_id}/{bundle.renderer.value}/{job.deterministic_render_job_id}.final.mp4",
                output_hash=output_hash,
                renderer_version=self._renderer_version(bundle.renderer),
                manifest_hashes=manifest_hashes,
                final_text_plan_id=bundle.final_text_plan_id,
                platform_variant_ids=bundle.platform_variant_ids,
                provider_receipt_id=provider_receipt.provider_receipt_id,
                completed_at=utc_now(),
            )
        )
        job = job.model_copy(update={"status": DeterministicRenderStatus.succeeded, "completed_at": output.completed_at})
        self.repository.put_job(job)
        self.repository.put_receipt(
            new_render_receipt(
                actor_id=actor_id,
                render_contract_id=bundle.render_contract_id,
                renderer_props_bundle_id=bundle.renderer_props_bundle_id,
                deterministic_render_job_id=job.deterministic_render_job_id,
                render_output_id=output.render_output_id,
                provider_receipt_id=provider_receipt.provider_receipt_id,
                renderer=bundle.renderer,
                props_hash=bundle.props_hash,
                input_manifest_hashes=manifest_hashes,
                renderer_version=output.renderer_version,
                output_hashes=[output.output_hash],
                final_text_plan_id=bundle.final_text_plan_id,
                duration_seconds=self._scene_spec(self._render_contract(bundle.render_contract_id).scene_spec_id).duration_seconds,
                cost_amount=provider_receipt.cost_amount,
                retry_count=retry_count,
                decision_code="DETERMINISTIC_RENDER_OUTPUT_RECORDED",
                evidence_refs=[output.preview_uri or "", output.final_uri, output.output_hash, str(provider_receipt.provider_receipt_id)],
                command_id=command_id,
            )
        )
        return output

    def fail_deterministic_render(
        self,
        *,
        deterministic_render_job_id: UUID,
        actor_id: UUID,
        failure_code: str,
        command_id: UUID | None = None,
    ) -> RenderReceipt:
        job = self.repository.jobs.get(deterministic_render_job_id)
        if job is None:
            raise DeterministicRenderError("DETERMINISTIC_RENDER_JOB_REQUIRED", "Render job is required.")
        failed = job.model_copy(update={"status": DeterministicRenderStatus.failed, "completed_at": utc_now()})
        self.repository.put_job(failed)
        bundle = self._props_bundle(job.renderer_props_bundle_id)
        return self.repository.put_receipt(
            new_render_receipt(
                actor_id=actor_id,
                render_contract_id=job.render_contract_id,
                renderer_props_bundle_id=job.renderer_props_bundle_id,
                deterministic_render_job_id=job.deterministic_render_job_id,
                renderer=job.renderer,
                props_hash=bundle.props_hash,
                retry_count=job.retry_count,
                decision_code="DETERMINISTIC_RENDER_FAILED",
                evidence_refs=[failure_code],
                command_id=command_id,
            )
        )

    def stage12_deterministic_render(
        self,
        *,
        render_contract_id: UUID,
        assembly_plan_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        preferred_renderer: DeterministicRenderer | str | None = None,
    ) -> RenderOutput:
        bundle = self.build_renderer_props_bundle(
            render_contract_id=render_contract_id,
            assembly_plan_id=assembly_plan_id,
            actor_id=actor_id,
            preferred_renderer=preferred_renderer,
        )
        return self.start_deterministic_render(
            renderer_props_bundle_id=bundle.renderer_props_bundle_id,
            actor_id=actor_id,
            idempotency_key=idempotency_key,
        )

    def _renderer(self, render_contract: RenderContract, preferred_renderer: DeterministicRenderer | str | None) -> DeterministicRenderer:
        if preferred_renderer is not None:
            return DeterministicRenderer(preferred_renderer)
        route = render_contract.renderer_route.lower()
        if "motion_canvas" in route or "motion-canvas" in route:
            return DeterministicRenderer.motion_canvas
        return DeterministicRenderer.remotion

    def _validate_brand_layers(self, scene_spec: SceneSpec, layers: list[Any]) -> None:
        session = self._session(scene_spec)
        for layer in layers:
            if layer.brand_context_asset_id is None:
                continue
            try:
                self.scene_spec_compiler.gate_service.brand_context_service.assert_asset_in_locked_context(
                    organization_id=session.organization_id,
                    brand_id=session.brand_id,
                    brand_context_version_id=scene_spec.brand_context_version_id,
                    asset_id=layer.brand_context_asset_id,
                )
            except Exception as exc:
                code = getattr(exc, "code", "BRAND_CONTEXT_ASSET_NOT_APPROVED")
                raise DeterministicRenderError(code, str(exc)) from exc

    def _final_text_plan(self, scene_spec: SceneSpec):
        for job in self.composition_service.repository.composition_jobs.values():
            if job.scene_spec_id == scene_spec.scene_spec_id and job.final_text_plan_id:
                plan = self.composition_service.repository.final_text_plans[job.final_text_plan_id]
                if not plan.editable_text_required:
                    raise DeterministicRenderError("FINAL_TEXT_EDITABLE_LAYER_REQUIRED", "Final text must remain editable for deterministic rendering.")
                return plan
        raise DeterministicRenderError("FINAL_TEXT_PLAN_REQUIRED", "Final text plan is required before deterministic rendering.")

    def _manifest_hashes(self, bundle: RendererPropsBundle) -> list[str]:
        assembly_plan = self._assembly_plan(bundle.assembly_plan_id)
        return [bundle.props_hash, *assembly_plan.manifest_hashes.values()]

    @staticmethod
    def _renderer_version(renderer: DeterministicRenderer) -> str:
        return {
            DeterministicRenderer.remotion: "remotion:deterministic_props_v1",
            DeterministicRenderer.motion_canvas: "motion_canvas:deterministic_props_v1",
        }[renderer]

    @staticmethod
    def _provider_capability_id(renderer: DeterministicRenderer) -> str:
        return {
            DeterministicRenderer.remotion: "remotion.video_render.v1",
            DeterministicRenderer.motion_canvas: "motion_canvas.programmatic_animation.v1",
        }[renderer]

    @staticmethod
    def _provider_input_types(renderer: DeterministicRenderer) -> list[str]:
        if renderer == DeterministicRenderer.motion_canvas:
            return ["animation_plan", "layer_manifest"]
        return ["assembly_plan", "layer_manifest", "caption_manifest", "audio_mix_manifest"]

    def _render_contract(self, render_contract_id: UUID) -> RenderContract:
        contract = self.scene_spec_compiler.repository.render_contracts.get(render_contract_id)
        if contract is None:
            raise DeterministicRenderError("RENDER_CONTRACT_REQUIRED", "RenderContract is required.")
        return contract

    def _scene_spec(self, scene_spec_id: UUID) -> SceneSpec:
        scene_spec = self.scene_spec_compiler.repository.scene_specs.get(scene_spec_id)
        if scene_spec is None:
            raise DeterministicRenderError("SCENE_SPEC_REQUIRED", "SceneSpec is required.")
        return scene_spec

    def _assembly_plan(self, assembly_plan_id: UUID) -> AssemblyPlan:
        plan = self.assembly_planner.repository.assembly_plans.get(assembly_plan_id)
        if plan is None:
            raise DeterministicRenderError("ASSEMBLY_PLAN_REQUIRED", "Assembly plan is required.")
        return plan

    def _props_bundle(self, renderer_props_bundle_id: UUID) -> RendererPropsBundle:
        bundle = self.repository.props_bundles.get(renderer_props_bundle_id)
        if bundle is None:
            raise DeterministicRenderError("RENDERER_PROPS_BUNDLE_REQUIRED", "Renderer props bundle is required.")
        return bundle

    def _session(self, scene_spec: SceneSpec):
        if self.scene_spec_compiler.editing_session_service is None:
            raise DeterministicRenderError("EDITING_SESSION_SERVICE_REQUIRED", "Editing session service is required.")
        session = self.scene_spec_compiler.editing_session_service.repository.sessions.get(scene_spec.complete_editing_session_id)
        if session is None:
            raise DeterministicRenderError("COMPLETE_EDITING_SESSION_REQUIRED", "Complete Editing Session is required.")
        return session


@dataclass
class DeterministicRenderCommandHandler:
    command_type: str
    service: DeterministicRenderService
    aggregate_type: str = "render"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "SelectDeterministicRendererCommand":
            return self.service.select_renderer(
                render_contract_id=UUID(payload["render_contract_id"]),
                assembly_plan_id=UUID(payload["assembly_plan_id"]),
                preferred_renderer=payload.get("preferred_renderer"),
            ).model_dump(mode="json")
        if self.command_type == "BuildRendererPropsBundleCommand":
            return self.service.build_renderer_props_bundle(
                render_contract_id=UUID(payload["render_contract_id"]),
                assembly_plan_id=UUID(payload["assembly_plan_id"]),
                actor_id=envelope.actor.actor_id,
                preferred_renderer=payload.get("preferred_renderer"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateRendererInputsCommand":
            return self.service.validate_renderer_inputs(UUID(payload["renderer_props_bundle_id"])).model_dump(mode="json")
        if self.command_type == "StartDeterministicRenderCommand":
            return self.service.start_deterministic_render(
                renderer_props_bundle_id=UUID(payload["renderer_props_bundle_id"]),
                actor_id=envelope.actor.actor_id,
                idempotency_key=payload.get("render_idempotency_key", envelope.idempotency_key),
                retry_count=int(payload.get("retry_count", 0)),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RecordDeterministicRenderOutputCommand":
            return self.service.start_deterministic_render(
                renderer_props_bundle_id=UUID(payload["renderer_props_bundle_id"]),
                actor_id=envelope.actor.actor_id,
                idempotency_key=payload.get("render_idempotency_key", envelope.idempotency_key),
                retry_count=int(payload.get("retry_count", 0)),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "FailDeterministicRenderCommand":
            return self.service.fail_deterministic_render(
                deterministic_render_job_id=UUID(payload["deterministic_render_job_id"]),
                actor_id=envelope.actor.actor_id,
                failure_code=payload["failure_code"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise DeterministicRenderError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("render_contract_id") or payload.get("renderer_props_bundle_id") or payload.get("deterministic_render_job_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_deterministic_render_command_handlers(bus: CommandBus, service: DeterministicRenderService) -> None:
    for command_type in [
        "SelectDeterministicRendererCommand",
        "BuildRendererPropsBundleCommand",
        "ValidateRendererInputsCommand",
        "StartDeterministicRenderCommand",
        "RecordDeterministicRenderOutputCommand",
        "FailDeterministicRenderCommand",
    ]:
        bus.register_handler(DeterministicRenderCommandHandler(command_type=command_type, service=service))
