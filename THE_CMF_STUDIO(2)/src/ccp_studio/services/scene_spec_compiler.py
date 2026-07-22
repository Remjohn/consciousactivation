"""SceneSpec compiler for TS-CMF-022 and TS-CMF-037."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.brand_context_gate import SceneSpecBrandContextBinding, SelectedBrandAssetRef
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.complete_editing_session import CompleteEditingSessionStatus, EditingSessionStatusEvent
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.scene_spec import (
    AssetSelection,
    AssetSourceKind,
    CreativeState,
    CreativeStateStage,
    EvaluationRequirement,
    PlatformVariant,
    RenderContract,
    RevisionPolicy,
    SceneSpec,
    SceneSpecReceipt,
    SceneSubjectSpec,
    new_scene_spec_receipt,
    scene_input_hash,
)
from ccp_studio.repositories.scene_spec import InMemorySceneSpecRepository
from ccp_studio.services.brand_context_gate_service import BrandContextGateService, BrandContextGateServiceError
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.complete_editing_session_service import CompleteEditingSessionService


class SceneSpecCompilerError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SceneSpecCompiler:
    gate_service: BrandContextGateService
    editing_session_service: CompleteEditingSessionService | None = None
    repository: InMemorySceneSpecRepository = field(default_factory=InMemorySceneSpecRepository)

    def bind_brand_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        scene_spec_id: UUID,
        brand_context_version_id: UUID,
        selected_asset_refs: list[SelectedBrandAssetRef],
    ) -> SceneSpecBrandContextBinding:
        return self.gate_service.bind_scene_spec_to_context(
            organization_id=organization_id,
            brand_id=brand_id,
            scene_spec_id=scene_spec_id,
            brand_context_version_id=brand_context_version_id,
            selected_asset_refs=selected_asset_refs,
        )

    def compile_scene_spec(
        self,
        *,
        complete_editing_session_id: UUID,
        actor_id: UUID,
        selected_asset_refs: list[SelectedBrandAssetRef],
        platform_variants: list[dict[str, Any]],
        revision_policy: dict[str, Any] | None,
        subject: SceneSubjectSpec | dict[str, Any] | None = None,
        format: str = "short_video",
        aspect_ratio: str = "9:16",
        duration_seconds: float = 45.0,
        content_type: str = "interview_first_short_video",
        visual_style: str = "cmf_paper_cut_expression_engine",
        platform_targets: list[str] | None = None,
        message_role: str = "source_backed_expression",
        emotional_intent: str = "recognition_without_overstatement",
        composition_requirements: dict[str, Any] | None = None,
        negative_constraints: dict[str, Any] | None = None,
        evaluation_requirements: list[dict[str, Any]] | None = None,
        renderer_route: str = "deterministic_scene_renderer",
        reaction_template_route_id: UUID | None = None,
        reaction_template_code: str | None = None,
        command_id: UUID | None = None,
    ) -> SceneSpec:
        session = self._session(complete_editing_session_id)
        scene_spec_id = uuid4()
        if not revision_policy:
            self._write_blocked_receipt(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                actor_id=actor_id,
                complete_editing_session_id=session.complete_editing_session_id,
                scene_spec_id=scene_spec_id,
                source_expression_moment_id=session.source_expression_moment_id,
                asset_route_receipt_id=session.asset_route_receipt_id,
                brand_context_version_id=session.brand_context_version_id,
                brand_context_version_hash=session.brand_context_version_hash,
                command_id=command_id,
                reason="REVISION_POLICY_REQUIRED",
            )
            raise SceneSpecCompilerError("REVISION_POLICY_REQUIRED", "SceneSpec compilation requires a revision policy before provider queue.")
        try:
            if not selected_asset_refs:
                raise SceneSpecCompilerError("SCENE_ASSET_SELECTION_REQUIRED", "SceneSpec requires at least one selected asset.")
            self.bind_brand_context(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                scene_spec_id=scene_spec_id,
                brand_context_version_id=session.brand_context_version_id,
                selected_asset_refs=selected_asset_refs,
            )
            parsed_subject = self._subject(subject, selected_asset_refs)
            variants = self._platform_variants(
                scene_spec_id=scene_spec_id,
                requests=platform_variants,
                fallback_aspect_ratio=aspect_ratio,
                fallback_duration_seconds=duration_seconds,
            )
            asset_selections = [
                self.repository.put_asset_selection(
                    AssetSelection(
                        schema_version="cmf.asset_selection.v1",
                        asset_selection_id=uuid4(),
                        scene_spec_id=scene_spec_id,
                        asset_id=asset.asset_id,
                        asset_type=asset.asset_type,
                        asset_ref=f"{asset.asset_type}:{asset.asset_id}",
                        asset_hash=asset.asset_hash,
                        source_kind=AssetSourceKind.brand_context,
                        brand_context_version_id=asset.brand_context_version_id,
                        source_ref=f"brand_context_version:{asset.brand_context_version_id}",
                        approved_for_scene=True,
                    )
                )
                for asset in selected_asset_refs
            ]
            stored_variants = [self.repository.put_platform_variant(item) for item in variants]
            requirements = [
                self.repository.put_evaluation_requirement(item)
                for item in self._evaluation_requirements(scene_spec_id, evaluation_requirements)
            ]
            policy = self.repository.put_revision_policy(self._revision_policy(scene_spec_id, revision_policy))
            input_hash = scene_input_hash(
                {
                    "complete_editing_session_id": session.complete_editing_session_id,
                    "source_expression_moment_id": session.source_expression_moment_id,
                    "asset_route_receipt_id": session.asset_route_receipt_id,
                    "reaction_template_route_id": reaction_template_route_id,
                    "reaction_template_code": reaction_template_code,
                    "brand_context_version_hash": session.brand_context_version_hash,
                    "selected_asset_hashes": [item.asset_hash for item in selected_asset_refs],
                    "platform_variants": [item.model_dump(mode="json") for item in stored_variants],
                    "revision_policy": policy.model_dump(mode="json"),
                }
            )
            scene_spec = self.repository.put_scene_spec(
                SceneSpec(
                    schema_version="cmf.scene_spec.v1",
                    scene_spec_id=scene_spec_id,
                    complete_editing_session_id=session.complete_editing_session_id,
                    format=format,
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration_seconds,
                    content_type=content_type,
                    visual_style=visual_style,
                    platform_targets=platform_targets or [item.platform for item in stored_variants],
                    message_role=message_role,
                    emotional_intent=emotional_intent,
                    subject=parsed_subject,
                    composition_requirements=composition_requirements or {"composition_json_required": True, "source_lineage_required": True},
                    negative_constraints=negative_constraints or {"no_hidden_prompt_strings": True, "no_unapproved_brand_assets": True},
                    source_expression_moment_id=session.source_expression_moment_id,
                    asset_route_receipt_id=session.asset_route_receipt_id,
                    reaction_template_route_id=reaction_template_route_id,
                    reaction_template_code=reaction_template_code,
                    brand_context_version_id=session.brand_context_version_id,
                    brand_context_version_hash=session.brand_context_version_hash,
                    input_hash=input_hash,
                    asset_selection_ids=[item.asset_selection_id for item in asset_selections],
                    platform_variant_ids=[item.platform_variant_id for item in stored_variants],
                    evaluation_requirement_ids=[item.evaluation_requirement_id for item in requirements],
                    revision_policy_id=policy.revision_policy_id,
                    created_at=utc_now(),
                )
            )
            render_contract = self.repository.put_render_contract(
                RenderContract(
                    schema_version="cmf.render_contract.v1",
                    render_contract_id=uuid4(),
                    scene_spec_id=scene_spec.scene_spec_id,
                    complete_editing_session_id=session.complete_editing_session_id,
                    renderer_route=renderer_route,
                    platform_variant_ids=scene_spec.platform_variant_ids,
                    selected_asset_ids=[item.asset_id for item in asset_selections],
                    evaluation_requirement_ids=scene_spec.evaluation_requirement_ids,
                    revision_policy_id=policy.revision_policy_id,
                    reaction_template_code=scene_spec.reaction_template_code,
                    renderer_props=self._renderer_props(scene_spec, asset_selections, stored_variants, policy),
                    created_at=utc_now(),
                )
            )
            source_refs = self._source_refs(session.complete_editing_session_id)
            receipt = self.repository.put_receipt(
                new_scene_spec_receipt(
                    organization_id=session.organization_id,
                    brand_id=session.brand_id,
                    actor_id=actor_id,
                    complete_editing_session_id=session.complete_editing_session_id,
                    scene_spec_id=scene_spec.scene_spec_id,
                    render_contract_id=render_contract.render_contract_id,
                    source_expression_moment_id=session.source_expression_moment_id,
                    asset_route_receipt_id=session.asset_route_receipt_id,
                    reaction_template_route_id=reaction_template_route_id,
                    reaction_template_code=reaction_template_code,
                    brand_context_version_id=session.brand_context_version_id,
                    brand_context_version_hash=session.brand_context_version_hash,
                    input_hash=input_hash,
                    selected_asset_hashes=[item.asset_hash for item in asset_selections],
                    platform_variant_ids=scene_spec.platform_variant_ids,
                    revision_policy_id=policy.revision_policy_id,
                    decision_code="SCENE_SPEC_COMPILED",
                    evidence_refs=[
                        f"complete_editing_session:{session.complete_editing_session_id}",
                        f"source_expression_moment:{session.source_expression_moment_id}",
                        f"asset_route_receipt:{session.asset_route_receipt_id}",
                        *([f"reaction_template_route:{reaction_template_route_id}", f"reaction_template_code:{reaction_template_code}"] if reaction_template_route_id and reaction_template_code else []),
                        f"brand_context_version:{session.brand_context_version_id}",
                        session.brand_context_version_hash,
                        *source_refs,
                    ],
                    command_id=command_id,
                )
            )
            creative_state = self.repository.put_creative_state(
                CreativeState(
                    schema_version="cmf.creative_state.v1",
                    creative_state_id=uuid4(),
                    complete_editing_session_id=session.complete_editing_session_id,
                    scene_spec_id=scene_spec.scene_spec_id,
                    stage=CreativeStateStage.render_contract_ready,
                    source_lineage_refs=source_refs,
                    state_payload_hash=scene_input_hash({"scene_spec": scene_spec.model_dump(mode="json"), "render_contract": render_contract.model_dump(mode="json")}),
                    latest_scene_spec_receipt_id=receipt.scene_spec_receipt_id,
                    status_reason="SceneSpec, Creative State, and Render Contract compiled from approved source lineage.",
                    updated_at=utc_now(),
                )
            )
            receipt = receipt.model_copy(update={"creative_state_id": creative_state.creative_state_id})
            self.repository.put_receipt(receipt)
            self._mark_session_ready_for_composition(session.complete_editing_session_id, actor_id)
            return scene_spec
        except Exception as exc:
            if not isinstance(exc, SceneSpecCompilerError):
                code = getattr(exc, "code", "SCENE_SPEC_COMPILATION_FAILED")
                message = str(exc)
            else:
                code = exc.code
                message = exc.message
            self._write_blocked_receipt(
                organization_id=session.organization_id,
                brand_id=session.brand_id,
                actor_id=actor_id,
                complete_editing_session_id=session.complete_editing_session_id,
                scene_spec_id=scene_spec_id,
                source_expression_moment_id=session.source_expression_moment_id,
                asset_route_receipt_id=session.asset_route_receipt_id,
                brand_context_version_id=session.brand_context_version_id,
                brand_context_version_hash=session.brand_context_version_hash,
                command_id=command_id,
                reason=code,
            )
            raise SceneSpecCompilerError(code, message) from exc

    def render_contract_for_scene(self, scene_spec_id: UUID) -> RenderContract:
        for contract in self.repository.render_contracts.values():
            if contract.scene_spec_id == scene_spec_id:
                if contract.revision_policy_id not in self.repository.revision_policies:
                    raise SceneSpecCompilerError("REVISION_POLICY_REQUIRED", "Render Contract revision policy is missing.")
                return contract
        raise SceneSpecCompilerError("RENDER_CONTRACT_REQUIRED", "Render Contract is required.")

    def block_provider_queue_without_revision_policy(self, *, scene_spec_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> SceneSpecReceipt:
        scene_spec = self.repository.scene_specs.get(scene_spec_id)
        if scene_spec is None:
            raise SceneSpecCompilerError("SCENE_SPEC_REQUIRED", "SceneSpec is required.")
        contract = next((item for item in self.repository.render_contracts.values() if item.scene_spec_id == scene_spec_id), None)
        if contract is not None and contract.revision_policy_id in self.repository.revision_policies:
            raise SceneSpecCompilerError("REVISION_POLICY_ALREADY_PRESENT", "Provider queue is not blocked because revision policy exists.")
        return self._write_blocked_receipt(
            organization_id=self._session(scene_spec.complete_editing_session_id).organization_id,
            brand_id=self._session(scene_spec.complete_editing_session_id).brand_id,
            actor_id=actor_id,
            complete_editing_session_id=scene_spec.complete_editing_session_id,
            scene_spec_id=scene_spec.scene_spec_id,
            source_expression_moment_id=scene_spec.source_expression_moment_id,
            asset_route_receipt_id=scene_spec.asset_route_receipt_id,
            brand_context_version_id=scene_spec.brand_context_version_id,
            brand_context_version_hash=scene_spec.brand_context_version_hash,
            command_id=command_id,
            reason="REVISION_POLICY_REQUIRED",
        )

    def _session(self, complete_editing_session_id: UUID):
        if self.editing_session_service is None:
            raise SceneSpecCompilerError("EDITING_SESSION_SERVICE_REQUIRED", "Complete Editing Session service is required for compilation.")
        session = self.editing_session_service.repository.sessions.get(complete_editing_session_id)
        if session is None:
            raise SceneSpecCompilerError("COMPLETE_EDITING_SESSION_REQUIRED", "Complete Editing Session is required.")
        return session

    def _subject(self, subject: SceneSubjectSpec | dict[str, Any] | None, selected_asset_refs: list[SelectedBrandAssetRef]) -> SceneSubjectSpec:
        if isinstance(subject, SceneSubjectSpec):
            return subject
        if isinstance(subject, dict):
            return SceneSubjectSpec(**subject)
        first = selected_asset_refs[0]
        return SceneSubjectSpec(
            identity_asset_ref=f"{first.asset_type}:{first.asset_id}",
            emotion="contained conviction",
            gesture="measured emphasis",
            position="center frame with reserved caption space",
            text_space="upper_third_reserved",
        )

    def _platform_variants(
        self,
        *,
        scene_spec_id: UUID,
        requests: list[dict[str, Any]],
        fallback_aspect_ratio: str,
        fallback_duration_seconds: float,
    ) -> list[PlatformVariant]:
        if not requests:
            requests = [
                {
                    "platform": "instagram_reels",
                    "aspect_ratio": fallback_aspect_ratio,
                    "duration_seconds": fallback_duration_seconds,
                    "captions_required": True,
                    "caption_plan": "burned_in_captions_from_transcript_alignment",
                    "negative_space_required": True,
                    "text_space": "upper_third_reserved",
                    "safe_zone": "center_safe_9x16",
                }
            ]
        variants: list[PlatformVariant] = []
        for item in requests:
            captions_required = bool(item.get("captions_required", False))
            negative_space_required = bool(item.get("negative_space_required", False))
            if captions_required and not item.get("caption_plan"):
                raise SceneSpecCompilerError("CAPTION_PLAN_REQUIRED", "Caption-required platform variants need an explicit caption plan.")
            if negative_space_required and not item.get("text_space"):
                raise SceneSpecCompilerError("TEXT_SPACE_REQUIRED", "Negative-space platform variants need an explicit text-space rule.")
            variants.append(
                PlatformVariant(
                    schema_version="cmf.platform_variant.v1",
                    platform_variant_id=uuid4(),
                    scene_spec_id=scene_spec_id,
                    platform=item["platform"],
                    aspect_ratio=item.get("aspect_ratio", fallback_aspect_ratio),
                    duration_seconds=float(item.get("duration_seconds", fallback_duration_seconds)),
                    captions_required=captions_required,
                    caption_plan=item.get("caption_plan"),
                    negative_space_required=negative_space_required,
                    text_space=item.get("text_space"),
                    safe_zone=item.get("safe_zone", "center_safe"),
                )
            )
        return variants

    def _evaluation_requirements(self, scene_spec_id: UUID, requests: list[dict[str, Any]] | None) -> list[EvaluationRequirement]:
        requests = requests or [
            {
                "requirement_type": "source_lineage",
                "success_criteria": "Reviewer can trace scene to source expression, route receipt, and Brand Context Version.",
                "evidence_required": ["scene_spec_receipt", "source_expression_moment", "brand_context_version_hash"],
            },
            {
                "requirement_type": "visual_constraint_fit",
                "success_criteria": "Caption, negative-space, asset, and platform constraints are present before rendering.",
                "evidence_required": ["platform_variant", "asset_selection", "render_contract"],
            },
        ]
        return [
            EvaluationRequirement(
                schema_version="cmf.evaluation_requirement.v1",
                evaluation_requirement_id=uuid4(),
                scene_spec_id=scene_spec_id,
                requirement_type=item["requirement_type"],
                success_criteria=item["success_criteria"],
                evidence_required=item["evidence_required"],
            )
            for item in requests
        ]

    def _revision_policy(self, scene_spec_id: UUID, request: dict[str, Any]) -> RevisionPolicy:
        return RevisionPolicy(
            schema_version="cmf.revision_policy.v1",
            revision_policy_id=uuid4(),
            scene_spec_id=scene_spec_id,
            max_revision_cycles=int(request.get("max_revision_cycles", 2)),
            requires_human_review=bool(request.get("requires_human_review", True)),
            allowed_change_scope=request.get("allowed_change_scope", ["caption_timing", "layout_spacing", "asset_substitution_within_locked_context"]),
            rollback_strategy=request.get("rollback_strategy", "supersede_scene_spec_and_invalidate_downstream_jobs"),
        )

    def _renderer_props(
        self,
        scene_spec: SceneSpec,
        asset_selections: list[AssetSelection],
        variants: list[PlatformVariant],
        policy: RevisionPolicy,
    ) -> dict[str, Any]:
        return {
            "scene_spec_id": str(scene_spec.scene_spec_id),
            "complete_editing_session_id": str(scene_spec.complete_editing_session_id),
            "format": scene_spec.format,
            "aspect_ratio": scene_spec.aspect_ratio,
            "duration_seconds": scene_spec.duration_seconds,
            "source_expression_moment_id": str(scene_spec.source_expression_moment_id),
            "asset_route_receipt_id": str(scene_spec.asset_route_receipt_id),
            "reaction_template_route_id": str(scene_spec.reaction_template_route_id) if scene_spec.reaction_template_route_id else None,
            "reaction_template_code": scene_spec.reaction_template_code,
            "brand_context_version_id": str(scene_spec.brand_context_version_id),
            "brand_context_version_hash": scene_spec.brand_context_version_hash,
            "selected_assets": [item.model_dump(mode="json") for item in asset_selections],
            "platform_variants": [item.model_dump(mode="json") for item in variants],
            "revision_policy": policy.model_dump(mode="json"),
        }

    def _source_refs(self, complete_editing_session_id: UUID) -> list[str]:
        if self.editing_session_service is None:
            return [f"complete_editing_session:{complete_editing_session_id}"]
        binding = next(
            (
                item
                for item in self.editing_session_service.repository.source_bindings.values()
                if item.complete_editing_session_id == complete_editing_session_id
            ),
            None,
        )
        return binding.source_refs if binding else [f"complete_editing_session:{complete_editing_session_id}"]

    def _mark_session_ready_for_composition(self, complete_editing_session_id: UUID, actor_id: UUID) -> None:
        if self.editing_session_service is None:
            return
        session = self.editing_session_service.repository.sessions.get(complete_editing_session_id)
        if session is None:
            return
        self.editing_session_service.repository.put_session(
            session.model_copy(
                update={
                    "status": CompleteEditingSessionStatus.composition_pending,
                    "production_readiness": "render_contract_ready",
                    "updated_at": utc_now(),
                }
            )
        )
        self.editing_session_service.repository.put_status_event(
            EditingSessionStatusEvent(
                schema_version="cmf.editing_session_status_event.v1",
                editing_session_status_event_id=uuid4(),
                complete_editing_session_id=complete_editing_session_id,
                previous_status=session.status,
                next_status=CompleteEditingSessionStatus.composition_pending,
                reason="SceneSpec and Render Contract compiled.",
                actor_id=actor_id,
                occurred_at=utc_now(),
            )
        )

    def _write_blocked_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        reason: str,
        complete_editing_session_id: UUID | None = None,
        scene_spec_id: UUID | None = None,
        source_expression_moment_id: UUID | None = None,
        asset_route_receipt_id: UUID | None = None,
        brand_context_version_id: UUID | None = None,
        brand_context_version_hash: str | None = None,
        command_id: UUID | None = None,
    ) -> SceneSpecReceipt:
        return self.repository.put_receipt(
            new_scene_spec_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                complete_editing_session_id=complete_editing_session_id,
                scene_spec_id=scene_spec_id,
                source_expression_moment_id=source_expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                brand_context_version_id=brand_context_version_id,
                brand_context_version_hash=brand_context_version_hash,
                decision_code="SCENE_SPEC_COMPILATION_BLOCKED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )


@dataclass
class SceneSpecCommandHandler:
    command_type: str
    service: SceneSpecCompiler
    aggregate_type: str = "scene_spec"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompileSceneSpecCommand":
            scene_spec = self.service.compile_scene_spec(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                actor_id=envelope.actor.actor_id,
                selected_asset_refs=[SelectedBrandAssetRef(**item) for item in payload["selected_asset_refs"]],
                platform_variants=payload["platform_variants"],
                revision_policy=payload.get("revision_policy"),
                subject=payload.get("subject"),
                format=payload.get("format", "short_video"),
                aspect_ratio=payload.get("aspect_ratio", "9:16"),
                duration_seconds=float(payload.get("duration_seconds", 45.0)),
                content_type=payload.get("content_type", "interview_first_short_video"),
                visual_style=payload.get("visual_style", "cmf_paper_cut_expression_engine"),
                platform_targets=payload.get("platform_targets"),
                message_role=payload.get("message_role", "source_backed_expression"),
                emotional_intent=payload.get("emotional_intent", "recognition_without_overstatement"),
                composition_requirements=payload.get("composition_requirements"),
                negative_constraints=payload.get("negative_constraints"),
                evaluation_requirements=payload.get("evaluation_requirements"),
                renderer_route=payload.get("renderer_route", "deterministic_scene_renderer"),
                reaction_template_route_id=UUID(payload["reaction_template_route_id"]) if payload.get("reaction_template_route_id") else None,
                reaction_template_code=payload.get("reaction_template_code"),
                command_id=envelope.command_id,
            )
            return scene_spec.model_dump(mode="json")
        if self.command_type == "InitializeCreativeStateCommand":
            scene_spec_id = UUID(payload["scene_spec_id"])
            state = next((item for item in self.service.repository.creative_states.values() if item.scene_spec_id == scene_spec_id), None)
            if state is None:
                raise SceneSpecCompilerError("CREATIVE_STATE_REQUIRED", "Creative State is initialized by SceneSpec compilation.")
            return state.model_dump(mode="json")
        if self.command_type == "CompileRenderContractCommand":
            return self.service.render_contract_for_scene(UUID(payload["scene_spec_id"])).model_dump(mode="json")
        if self.command_type == "ValidateSceneAssetsCommand":
            for item in [SelectedBrandAssetRef(**raw) for raw in payload["selected_asset_refs"]]:
                try:
                    self.service.gate_service.brand_context_service.assert_asset_in_locked_context(
                        organization_id=envelope.organization_id,
                        brand_id=envelope.brand_id,
                        brand_context_version_id=UUID(payload["brand_context_version_id"]),
                        asset_id=item.asset_id,
                    )
                except BrandContextGateServiceError:
                    raise
            return {"validated": True, "asset_count": len(payload["selected_asset_refs"])}
        if self.command_type == "ValidatePlatformVariantsCommand":
            variants = self.service._platform_variants(
                scene_spec_id=UUID(payload.get("scene_spec_id", str(uuid4()))),
                requests=payload["platform_variants"],
                fallback_aspect_ratio=payload.get("aspect_ratio", "9:16"),
                fallback_duration_seconds=float(payload.get("duration_seconds", 45.0)),
            )
            return {"validated": True, "platform_variant_count": len(variants)}
        if self.command_type == "BlockProviderQueueWithoutRevisionPolicyCommand":
            return self.service.block_provider_queue_without_revision_policy(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise SceneSpecCompilerError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("scene_spec_id") or payload.get("complete_editing_session_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_scene_spec_command_handlers(bus: CommandBus, service: SceneSpecCompiler) -> None:
    for command_type in [
        "CompileSceneSpecCommand",
        "InitializeCreativeStateCommand",
        "CompileRenderContractCommand",
        "ValidateSceneAssetsCommand",
        "ValidatePlatformVariantsCommand",
        "BlockProviderQueueWithoutRevisionPolicyCommand",
    ]:
        bus.register_handler(SceneSpecCommandHandler(command_type=command_type, service=service))
