"""Production gate service for locked Brand Context in TS-CMF-022."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.brand_context import BrandContextStatus
from ccp_studio.contracts.brand_context_gate import (
    BrandContextGateResult,
    BrandContextGateStatus,
    BrandContextLineageView,
    ProviderBrandContextReceipt,
    SceneSpecBrandContextBinding,
    SelectedBrandAssetRef,
    SupersededContextAction,
    SupersededContextDecision,
    new_brand_context_gate_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.brand_context_gate import InMemoryBrandContextGateRepository
from ccp_studio.services.brand_context_service import BrandContextService, BrandContextServiceError
from ccp_studio.services.command_bus import CommandBus


class BrandContextGateServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class BrandContextGateService:
    brand_context_service: BrandContextService
    repository: InMemoryBrandContextGateRepository = field(default_factory=InMemoryBrandContextGateRepository)

    def validate_production_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID | None,
        superseded_decision_id: UUID | None = None,
    ) -> BrandContextGateResult:
        if brand_context_version_id is None:
            return self._record_gate_result(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=None,
                version_hash=None,
                status=BrandContextGateStatus.blocked,
                decision_code="BRAND_CONTEXT_REQUIRED",
                selected_asset_refs=[],
            )
        try:
            version = self.brand_context_service.assert_context_selectable_for_production(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=brand_context_version_id,
            )
            return self._record_gate_result(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=brand_context_version_id,
                version_hash=version.version_hash,
                status=BrandContextGateStatus.allowed,
                decision_code="BRAND_CONTEXT_GATE_PASSED",
                selected_asset_refs=[],
            )
        except BrandContextServiceError as exc:
            if exc.code == "BRAND_CONTEXT_SUPERSEDED_REVIEW_REQUIRED":
                decision = self.repository.superseded_decisions.get(superseded_decision_id) if superseded_decision_id else None
                if decision is None:
                    version = self.brand_context_service.repository.versions.get(brand_context_version_id)
                    return self._record_gate_result(
                        organization_id=organization_id,
                        brand_id=brand_id,
                        brand_context_version_id=brand_context_version_id,
                        version_hash=version.version_hash if version else None,
                        status=BrandContextGateStatus.decision_required,
                        decision_code="BRAND_CONTEXT_DECISION_REQUIRED",
                        selected_asset_refs=[],
                    )
                if decision.action == SupersededContextAction.preserve_original:
                    version = self.brand_context_service.assert_context_selectable_for_production(
                        organization_id=organization_id,
                        brand_id=brand_id,
                        brand_context_version_id=brand_context_version_id,
                        allow_historical_superseded=True,
                    )
                    return self._record_gate_result(
                        organization_id=organization_id,
                        brand_id=brand_id,
                        brand_context_version_id=brand_context_version_id,
                        version_hash=version.version_hash,
                        status=BrandContextGateStatus.allowed,
                        decision_code="BRAND_CONTEXT_ORIGINAL_PRESERVED",
                        selected_asset_refs=[],
                    )
                if decision.replacement_brand_context_version_id is None:
                    raise BrandContextGateServiceError("REPLACEMENT_CONTEXT_REQUIRED", "Fork decision requires replacement context.")
                return self.validate_production_context(
                    organization_id=organization_id,
                    brand_id=brand_id,
                    brand_context_version_id=decision.replacement_brand_context_version_id,
                )
            return self._record_gate_result(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=brand_context_version_id,
                version_hash=None,
                status=BrandContextGateStatus.blocked,
                decision_code=exc.code,
                selected_asset_refs=[],
            )

    def bind_scene_spec_to_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        scene_spec_id: UUID,
        brand_context_version_id: UUID,
        selected_asset_refs: list[SelectedBrandAssetRef],
    ) -> SceneSpecBrandContextBinding:
        gate = self.validate_production_context(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
        )
        if gate.status != BrandContextGateStatus.allowed:
            raise BrandContextGateServiceError(gate.decision_code, "Brand Context gate did not pass.")
        for selected in selected_asset_refs:
            if selected.brand_context_version_id != brand_context_version_id:
                raise BrandContextGateServiceError("BRAND_ASSET_CONTEXT_MISMATCH", "Selected asset points to a different Brand Context Version.")
            try:
                self.brand_context_service.assert_asset_in_locked_context(
                    organization_id=organization_id,
                    brand_id=brand_id,
                    brand_context_version_id=brand_context_version_id,
                    asset_id=selected.asset_id,
                )
            except BrandContextServiceError as exc:
                code = "BRAND_ASSET_NOT_IN_CONTEXT" if exc.code == "BRAND_CONTEXT_ASSET_NOT_APPROVED" else exc.code
                raise BrandContextGateServiceError(code, exc.message) from exc
        version = self.brand_context_service.repository.versions[brand_context_version_id]
        binding = SceneSpecBrandContextBinding(
            schema_version="cmf.scene_spec_brand_context_binding.v1",
            scene_spec_id=scene_spec_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            brand_context_version_hash=version.version_hash,
            selected_asset_refs=selected_asset_refs,
            bound_at=utc_now(),
        )
        return self.repository.put_scene_binding(binding)

    def record_superseded_context_decision(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        superseded_brand_context_version_id: UUID,
        action: SupersededContextAction,
        decided_by_actor_id: UUID,
        rationale: str,
        replacement_brand_context_version_id: UUID | None = None,
    ) -> SupersededContextDecision:
        version = self.brand_context_service.repository.versions.get(superseded_brand_context_version_id)
        if version is None or version.organization_id != organization_id or version.brand_id != brand_id:
            raise BrandContextGateServiceError("BRAND_SCOPE_VIOLATION", "Superseded context is outside active brand scope.")
        if version.status != BrandContextStatus.superseded:
            raise BrandContextGateServiceError("BRAND_CONTEXT_NOT_SUPERSEDED", "Decision applies only to superseded contexts.")
        decision = SupersededContextDecision(
            schema_version="cmf.superseded_context_decision.v1",
            superseded_context_decision_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            superseded_brand_context_version_id=superseded_brand_context_version_id,
            action=action,
            replacement_brand_context_version_id=replacement_brand_context_version_id,
            decided_by_actor_id=decided_by_actor_id,
            rationale=rationale,
            decided_at=utc_now(),
        )
        return self.repository.put_superseded_decision(decision)

    def build_provider_context_receipt(
        self,
        *,
        provider_job_id: UUID,
        scene_spec_id: UUID,
    ) -> ProviderBrandContextReceipt:
        binding = self.repository.scene_bindings.get(scene_spec_id)
        if binding is None:
            raise BrandContextGateServiceError("PROVIDER_BRAND_CONTEXT_LINEAGE_REQUIRED", "Provider request requires SceneSpec Brand Context binding.")
        hashes = [selected.asset_hash for selected in binding.selected_asset_refs]
        if not hashes:
            raise BrandContextGateServiceError("PROVIDER_BRAND_CONTEXT_LINEAGE_REQUIRED", "Provider request requires selected asset hashes.")
        receipt = ProviderBrandContextReceipt(
            schema_version="cmf.provider_brand_context_receipt.v1",
            provider_brand_context_receipt_id=uuid4(),
            provider_job_id=provider_job_id,
            organization_id=binding.organization_id,
            brand_id=binding.brand_id,
            scene_spec_id=scene_spec_id,
            brand_context_version_id=binding.brand_context_version_id,
            brand_context_version_hash=binding.brand_context_version_hash,
            selected_asset_hashes=hashes,
            written_at=utc_now(),
        )
        return self.repository.put_provider_receipt(receipt)

    def generate_lineage_view(
        self,
        *,
        downstream_object_id: UUID,
        downstream_object_type: str,
        scene_spec_id: UUID,
    ) -> BrandContextLineageView:
        binding = self.repository.scene_bindings.get(scene_spec_id)
        if binding is None:
            raise BrandContextGateServiceError("BRAND_CONTEXT_LINEAGE_REQUIRED", "SceneSpec Brand Context binding is required.")
        view = BrandContextLineageView(
            schema_version="cmf.brand_context_lineage_view.v1",
            brand_context_lineage_view_id=uuid4(),
            organization_id=binding.organization_id,
            brand_id=binding.brand_id,
            downstream_object_id=downstream_object_id,
            downstream_object_type=downstream_object_type,
            brand_context_version_id=binding.brand_context_version_id,
            brand_context_version_hash=binding.brand_context_version_hash,
            selected_asset_refs=binding.selected_asset_refs,
            opened_at=utc_now(),
        )
        return self.repository.put_lineage_view(view)

    def _record_gate_result(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID | None,
        version_hash: str | None,
        status: BrandContextGateStatus,
        decision_code: str,
        selected_asset_refs: list[SelectedBrandAssetRef],
    ) -> BrandContextGateResult:
        result = BrandContextGateResult(
            schema_version="cmf.brand_context_gate_result.v1",
            brand_context_gate_result_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            requested_brand_context_version_id=brand_context_version_id,
            requested_brand_context_version_hash=version_hash,
            status=status,
            decision_code=decision_code,
            selected_asset_refs=selected_asset_refs,
            created_at=utc_now(),
        )
        self.repository.put_gate_result(result)
        self.repository.put_receipt(new_brand_context_gate_receipt(result=result, evidence_refs=[decision_code]))
        return result


@dataclass
class BrandContextGateCommandHandler:
    command_type: str
    service: BrandContextGateService
    aggregate_type: str = "brand_context_gate"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ValidateProductionBrandContextCommand":
            result = self.service.validate_production_context(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_context_version_id=UUID(payload["brand_context_version_id"]) if payload.get("brand_context_version_id") else None,
                superseded_decision_id=UUID(payload["superseded_decision_id"]) if payload.get("superseded_decision_id") else None,
            )
            return result.model_dump(mode="json")
        if self.command_type == "BindSceneSpecToBrandContextCommand":
            binding = self.service.bind_scene_spec_to_context(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                scene_spec_id=UUID(payload["scene_spec_id"]),
                brand_context_version_id=UUID(payload["brand_context_version_id"]),
                selected_asset_refs=[SelectedBrandAssetRef(**item) for item in payload["selected_asset_refs"]],
            )
            return binding.model_dump(mode="json")
        if self.command_type == "RecordSupersededContextDecisionCommand":
            decision = self.service.record_superseded_context_decision(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                superseded_brand_context_version_id=UUID(payload["superseded_brand_context_version_id"]),
                action=SupersededContextAction(payload["action"]),
                replacement_brand_context_version_id=UUID(payload["replacement_brand_context_version_id"]) if payload.get("replacement_brand_context_version_id") else None,
                decided_by_actor_id=envelope.actor.actor_id,
                rationale=payload["rationale"],
            )
            return decision.model_dump(mode="json")
        if self.command_type == "GenerateBrandContextLineageViewCommand":
            view = self.service.generate_lineage_view(
                downstream_object_id=UUID(payload["downstream_object_id"]),
                downstream_object_type=payload["downstream_object_type"],
                scene_spec_id=UUID(payload["scene_spec_id"]),
            )
            return view.model_dump(mode="json")
        raise BrandContextGateServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("brand_context_version_id") or payload.get("scene_spec_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_brand_context_gate_command_handlers(bus: CommandBus, service: BrandContextGateService) -> None:
    for command_type in [
        "ValidateProductionBrandContextCommand",
        "BindSceneSpecToBrandContextCommand",
        "RecordSupersededContextDecisionCommand",
        "GenerateBrandContextLineageViewCommand",
    ]:
        bus.register_handler(BrandContextGateCommandHandler(command_type=command_type, service=service))
