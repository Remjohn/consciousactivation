"""Scene intelligence service for TS-CMF-041."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.registry import RegistryStatus
from ccp_studio.contracts.scene_intelligence import (
    AssetRollItem,
    AssetRollPlan,
    AssetRollRole,
    BiologicalArcContainer,
    CreativeSubsystemDecision,
    SceneComponentSelection,
    SceneContainerPlan,
    SceneIntelligenceAuditView,
    SceneIntelligenceReceipt,
    new_scene_intelligence_receipt,
)
from ccp_studio.repositories.scene_intelligence import InMemorySceneIntelligenceRepository
from ccp_studio.services.assembly_planner import AssemblyPlanner
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.composition_service import CompositionService
from ccp_studio.services.registry_service import RegistryService
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


DEFAULT_REGISTRY_VERSION = "legacy-cmf-scene-intelligence:v1"


class SceneIntelligenceServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SceneIntelligenceService:
    scene_spec_compiler: SceneSpecCompiler
    composition_service: CompositionService | None = None
    assembly_planner: AssemblyPlanner | None = None
    registry_service: RegistryService | None = None
    repository: InMemorySceneIntelligenceRepository = field(default_factory=InMemorySceneIntelligenceRepository)

    def run_scene_intelligence(self, *, scene_spec_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> SceneIntelligenceReceipt:
        container = self.select_scene_container(
            scene_spec_id=scene_spec_id,
            actor_id=actor_id,
            container=BiologicalArcContainer.hook,
            selection_rationale="The scene opens with source-backed recognition before any cinematic flourish.",
            constraints=["container:hook", "source_expression_first", "caption_safe_negative_space"],
            registry_ref="legacy-cmf:scene-container:hook",
        )
        self.select_scene_component(
            scene_container_plan_id=container.scene_container_plan_id,
            actor_id=actor_id,
            component_registry_ref="legacy-cmf:scene-component:first-frame-imprint",
            satisfied_constraints=["container:hook", "first_frame_readable", "text_space_preserved"],
            violated_constraints=[],
            selection_rationale="First-frame imprint gives the audience a clear perceptual anchor for the source expression.",
        )
        self.evaluate_creative_subsystem_gates(
            scene_spec_id=scene_spec_id,
            actor_id=actor_id,
            decisions=[
                {
                    "subsystem_registry_ref": "legacy-cmf:creative-subsystem:first-frame-imprint",
                    "decision": "approved",
                    "rationale": "Opening frame has a readable hook and subject hierarchy.",
                    "evidence_refs": [f"scene_spec:{scene_spec_id}"],
                },
                {
                    "subsystem_registry_ref": "legacy-cmf:creative-subsystem:recognition-window",
                    "decision": "approved",
                    "rationale": "Caption timing and visual hierarchy preserve recognition before abstraction.",
                    "evidence_refs": [f"scene_spec:{scene_spec_id}"],
                },
            ],
        )
        self.compile_asset_roll_plan(scene_spec_id=scene_spec_id, actor_id=actor_id)
        return self.validate_scene_orchestration(scene_spec_id=scene_spec_id, actor_id=actor_id, command_id=command_id)

    def select_scene_container(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        container: BiologicalArcContainer,
        selection_rationale: str,
        constraints: list[str],
        registry_ref: str,
    ) -> SceneContainerPlan:
        scene_spec = self._scene_spec(scene_spec_id)
        self._require_registry_ref(registry_ref)
        return self.repository.put_container_plan(
            SceneContainerPlan(
                schema_version="cmf.scene_container_plan.v1",
                scene_container_plan_id=uuid4(),
                scene_spec_id=scene_spec.scene_spec_id,
                container=container,
                source_expression_moment_id=scene_spec.source_expression_moment_id,
                selection_rationale=selection_rationale,
                constraints=constraints,
                registry_ref=registry_ref,
                created_at=utc_now(),
            )
        )

    def select_scene_component(
        self,
        *,
        scene_container_plan_id: UUID,
        actor_id: UUID,
        component_registry_ref: str,
        satisfied_constraints: list[str],
        violated_constraints: list[str],
        selection_rationale: str,
    ) -> SceneComponentSelection:
        container = self.repository.container_plans.get(scene_container_plan_id)
        if container is None:
            raise SceneIntelligenceServiceError("SCENE_CONTAINER_REQUIRED", "Container must be selected before component.")
        self._require_registry_ref(component_registry_ref)
        return self.repository.put_component_selection(
            SceneComponentSelection(
                schema_version="cmf.scene_component_selection.v1",
                scene_component_selection_id=uuid4(),
                scene_container_plan_id=container.scene_container_plan_id,
                scene_spec_id=container.scene_spec_id,
                component_registry_ref=component_registry_ref,
                valid_for_container=not violated_constraints,
                satisfied_constraints=satisfied_constraints,
                violated_constraints=violated_constraints,
                selection_rationale=selection_rationale,
                created_at=utc_now(),
            )
        )

    def evaluate_creative_subsystem_gates(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        decisions: list[dict[str, Any]],
    ) -> list[CreativeSubsystemDecision]:
        self._scene_spec(scene_spec_id)
        stored: list[CreativeSubsystemDecision] = []
        for item in decisions:
            active = self._registry_ref_active(item["subsystem_registry_ref"])
            if not active and item["decision"] == "approved":
                raise SceneIntelligenceServiceError("UNMIGRATED_SUBSYSTEM_REF", "Approved subsystem decisions require migrated active registry refs.")
            stored.append(
                self.repository.put_subsystem_decision(
                    CreativeSubsystemDecision(
                        schema_version="cmf.creative_subsystem_decision.v1",
                        creative_subsystem_decision_id=uuid4(),
                        scene_spec_id=scene_spec_id,
                        subsystem_registry_ref=item["subsystem_registry_ref"],
                        decision=item["decision"],
                        rationale=item["rationale"],
                        evidence_refs=item["evidence_refs"],
                        created_at=utc_now(),
                    )
                )
            )
        return stored

    def compile_asset_roll_plan(
        self,
        *,
        scene_spec_id: UUID,
        actor_id: UUID,
        items: list[dict[str, Any]] | None = None,
    ) -> AssetRollPlan:
        scene_spec = self._scene_spec(scene_spec_id)
        items = items or self._default_asset_roll_items(scene_spec)
        parsed = [
            AssetRollItem(
                schema_version="cmf.asset_roll_item.v1",
                asset_roll_item_id=uuid4(),
                role=AssetRollRole(item["role"]),
                asset_ref=item.get("asset_ref"),
                function=item["function"],
                source_or_license_state=item["source_or_license_state"],
                rationale=item["rationale"],
            )
            for item in items
        ]
        roles = {item.role for item in parsed}
        missing = set(AssetRollRole) - roles
        if missing:
            raise SceneIntelligenceServiceError("ASSET_ROLL_ROLE_REQUIRED", f"Asset roll plan is missing roles: {sorted(item.value for item in missing)}")
        if any(not item.function or not item.source_or_license_state or not item.rationale for item in parsed):
            raise SceneIntelligenceServiceError("ASSET_ROLL_FUNCTION_REQUIRED", "Every asset roll item requires function, source/license state, and rationale.")
        return self.repository.put_asset_roll_plan(
            AssetRollPlan(
                schema_version="cmf.asset_roll_plan.v1",
                asset_roll_plan_id=uuid4(),
                scene_spec_id=scene_spec.scene_spec_id,
                items=parsed,
                created_at=utc_now(),
            )
        )

    def validate_scene_orchestration(self, *, scene_spec_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> SceneIntelligenceReceipt:
        scene_spec = self._scene_spec(scene_spec_id)
        session = self._session(scene_spec.complete_editing_session_id)
        container = self._container(scene_spec_id)
        component = self._component(scene_spec_id)
        decisions = [item for item in self.repository.subsystem_decisions.values() if item.scene_spec_id == scene_spec_id]
        asset_roll = self._asset_roll(scene_spec_id)
        if not component.valid_for_container:
            return self._blocked_receipt(session.organization_id, session.brand_id, actor_id, scene_spec_id, "SCENE_COMPONENT_INVALID_FOR_CONTAINER", command_id)
        if not decisions:
            return self._blocked_receipt(session.organization_id, session.brand_id, actor_id, scene_spec_id, "CREATIVE_SUBSYSTEM_DECISION_REQUIRED", command_id)
        receipt = new_scene_intelligence_receipt(
            organization_id=session.organization_id,
            brand_id=session.brand_id,
            actor_id=actor_id,
            scene_spec_id=scene_spec_id,
            scene_container_plan_id=container.scene_container_plan_id,
            scene_component_selection_id=component.scene_component_selection_id,
            creative_subsystem_decision_ids=[item.creative_subsystem_decision_id for item in decisions],
            asset_roll_plan_id=asset_roll.asset_roll_plan_id,
            registry_versions=self._registry_versions(),
            validation_passed=True,
            decision_code="SCENE_ORCHESTRATION_VALIDATED",
            evidence_refs=[
                f"scene_spec:{scene_spec_id}",
                f"source_expression_moment:{scene_spec.source_expression_moment_id}",
                container.registry_ref,
                component.component_registry_ref,
                *[item.subsystem_registry_ref for item in decisions],
            ],
            command_id=command_id,
        )
        return self.repository.put_receipt(receipt)

    def reconstruct_scene_intelligence(self, scene_spec_id: UUID) -> SceneIntelligenceAuditView:
        scene_spec = self._scene_spec(scene_spec_id)
        container = self._container(scene_spec_id)
        component = self._component(scene_spec_id)
        asset_roll = self._asset_roll(scene_spec_id)
        decisions = [item.creative_subsystem_decision_id for item in self.repository.subsystem_decisions.values() if item.scene_spec_id == scene_spec_id]
        composition_jobs = []
        if self.composition_service is not None:
            composition_jobs = [
                item.composition_job_id
                for item in self.composition_service.repository.composition_jobs.values()
                if item.scene_spec_id == scene_spec_id
            ]
        assembly_plans = []
        sonic_plans = []
        if self.assembly_planner is not None:
            for plan in self.assembly_planner.repository.assembly_plans.values():
                if plan.scene_spec_id == scene_spec_id:
                    assembly_plans.append(plan.assembly_plan_id)
                    sonic_plans.append(plan.audio_mix_manifest_id)
        return self.repository.put_audit_view(
            SceneIntelligenceAuditView(
                schema_version="cmf.scene_intelligence_audit_view.v1",
                scene_spec_id=scene_spec_id,
                source_expression_moment_id=scene_spec.source_expression_moment_id,
                asset_route_receipt_id=scene_spec.asset_route_receipt_id,
                scene_container_plan_id=container.scene_container_plan_id,
                scene_component_selection_id=component.scene_component_selection_id,
                creative_subsystem_decision_ids=decisions,
                asset_roll_plan_id=asset_roll.asset_roll_plan_id,
                composition_job_ids=composition_jobs,
                assembly_plan_ids=assembly_plans,
                sonic_plan_ids=sonic_plans,
                approval_event_ids=[],
            )
        )

    def _default_asset_roll_items(self, scene_spec) -> list[dict[str, Any]]:
        return [
            {
                "role": AssetRollRole.a_roll.value,
                "asset_ref": f"source_expression_moment:{scene_spec.source_expression_moment_id}",
                "function": "narrative and emotional anchor",
                "source_or_license_state": "approved_source_expression",
                "rationale": "A-roll carries the guest's source-backed expression.",
            },
            {
                "role": AssetRollRole.b_roll.value,
                "asset_ref": "composition_plate:ideogram_layout_guidance",
                "function": "cinematic and emotional layer",
                "source_or_license_state": "composition_plate_restricted_to_layout",
                "rationale": "B-roll supports feeling without becoming identity or final text authority.",
            },
            {
                "role": AssetRollRole.c_roll.value,
                "asset_ref": "scene_component:first_frame_imprint",
                "function": "visual explanation layer",
                "source_or_license_state": "migrated_registry_ref",
                "rationale": "C-roll clarifies the idea with a typed scene component.",
            },
            {
                "role": AssetRollRole.d_roll.value,
                "asset_ref": "source_context:lived_reality",
                "function": "authentic lived-reality layer",
                "source_or_license_state": "source_context_only",
                "rationale": "D-roll keeps lived reality distinct from stock atmosphere.",
            },
            {
                "role": AssetRollRole.e_roll.value,
                "asset_ref": "cultural_pattern:recognition_window",
                "function": "cultural/status/pattern-interrupt layer",
                "source_or_license_state": "migrated_registry_ref",
                "rationale": "E-roll creates recognition without generic spectacle.",
            },
        ]

    def _require_registry_ref(self, registry_ref: str) -> None:
        if not self._registry_ref_active(registry_ref):
            raise SceneIntelligenceServiceError("REGISTRY_REF_NOT_ACTIVE", "Scene intelligence registry ref is not active or migrated.")

    def _registry_ref_active(self, registry_ref: str) -> bool:
        if registry_ref.startswith("legacy-cmf:"):
            return True
        if self.registry_service is None:
            return False
        if registry_ref.startswith("registry_entry:"):
            raw = registry_ref.split(":", 1)[1]
            try:
                entry_id = UUID(raw)
            except ValueError:
                return False
            entry = self.registry_service.repository.registry_entries.get(entry_id)
            return entry is not None and entry.status == RegistryStatus.active
        return any(
            entry.status == RegistryStatus.active and entry.payload.get("registry_ref") == registry_ref
            for entry in self.registry_service.repository.registry_entries.values()
        )

    def _registry_versions(self) -> dict[str, str]:
        return {
            "scene_container_registry": DEFAULT_REGISTRY_VERSION,
            "scene_component_registry": DEFAULT_REGISTRY_VERSION,
            "creative_subsystem_registry": DEFAULT_REGISTRY_VERSION,
            "asset_roll_registry": DEFAULT_REGISTRY_VERSION,
        }

    def _scene_spec(self, scene_spec_id: UUID):
        scene_spec = self.scene_spec_compiler.repository.scene_specs.get(scene_spec_id)
        if scene_spec is None:
            raise SceneIntelligenceServiceError("SCENE_SPEC_REQUIRED", "SceneSpec is required for scene intelligence.")
        return scene_spec

    def _session(self, complete_editing_session_id: UUID):
        if self.scene_spec_compiler.editing_session_service is None:
            raise SceneIntelligenceServiceError("EDITING_SESSION_SERVICE_REQUIRED", "Editing session service is required.")
        return self.scene_spec_compiler.editing_session_service.repository.sessions[complete_editing_session_id]

    def _container(self, scene_spec_id: UUID) -> SceneContainerPlan:
        container = next((item for item in self.repository.container_plans.values() if item.scene_spec_id == scene_spec_id), None)
        if container is None:
            raise SceneIntelligenceServiceError("SCENE_CONTAINER_REQUIRED", "Scene container is required.")
        return container

    def _component(self, scene_spec_id: UUID) -> SceneComponentSelection:
        component = next((item for item in self.repository.component_selections.values() if item.scene_spec_id == scene_spec_id), None)
        if component is None:
            raise SceneIntelligenceServiceError("SCENE_COMPONENT_REQUIRED", "Scene component is required.")
        return component

    def _asset_roll(self, scene_spec_id: UUID) -> AssetRollPlan:
        plan = next((item for item in self.repository.asset_roll_plans.values() if item.scene_spec_id == scene_spec_id), None)
        if plan is None:
            raise SceneIntelligenceServiceError("ASSET_ROLL_PLAN_REQUIRED", "Asset roll plan is required.")
        return plan

    def _blocked_receipt(
        self,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        scene_spec_id: UUID,
        reason: str,
        command_id: UUID | None,
    ) -> SceneIntelligenceReceipt:
        return self.repository.put_receipt(
            new_scene_intelligence_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                scene_spec_id=scene_spec_id,
                validation_passed=False,
                decision_code="SCENE_ORCHESTRATION_BLOCKED",
                evidence_refs=[reason],
                command_id=command_id,
            )
        )


@dataclass
class SceneIntelligenceCommandHandler:
    command_type: str
    service: SceneIntelligenceService
    aggregate_type: str = "scene_intelligence"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "SelectSceneContainerCommand":
            return self.service.select_scene_container(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                container=BiologicalArcContainer(payload["container"]),
                selection_rationale=payload["selection_rationale"],
                constraints=payload["constraints"],
                registry_ref=payload["registry_ref"],
            ).model_dump(mode="json")
        if self.command_type == "SelectSceneComponentCommand":
            return self.service.select_scene_component(
                scene_container_plan_id=UUID(payload["scene_container_plan_id"]),
                actor_id=envelope.actor.actor_id,
                component_registry_ref=payload["component_registry_ref"],
                satisfied_constraints=payload["satisfied_constraints"],
                violated_constraints=payload.get("violated_constraints", []),
                selection_rationale=payload["selection_rationale"],
            ).model_dump(mode="json")
        if self.command_type == "EvaluateCreativeSubsystemGatesCommand":
            return {
                "decisions": [
                    item.model_dump(mode="json")
                    for item in self.service.evaluate_creative_subsystem_gates(
                        scene_spec_id=UUID(payload["scene_spec_id"]),
                        actor_id=envelope.actor.actor_id,
                        decisions=payload["decisions"],
                    )
                ]
            }
        if self.command_type == "CompileAssetRollPlanCommand":
            return self.service.compile_asset_roll_plan(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                items=payload.get("items"),
            ).model_dump(mode="json")
        if self.command_type in {"ValidateSceneOrchestrationCommand", "WriteSceneIntelligenceReceiptCommand"}:
            return self.service.validate_scene_orchestration(
                scene_spec_id=UUID(payload["scene_spec_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise SceneIntelligenceServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("scene_spec_id") or payload.get("scene_container_plan_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_scene_intelligence_command_handlers(bus: CommandBus, service: SceneIntelligenceService) -> None:
    for command_type in [
        "SelectSceneContainerCommand",
        "SelectSceneComponentCommand",
        "EvaluateCreativeSubsystemGatesCommand",
        "CompileAssetRollPlanCommand",
        "ValidateSceneOrchestrationCommand",
        "WriteSceneIntelligenceReceiptCommand",
    ]:
        bus.register_handler(SceneIntelligenceCommandHandler(command_type=command_type, service=service))
