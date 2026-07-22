"""Complete Editing Session creation service for TS-CMF-036."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.asset_package import PackageItemStatus
from ccp_studio.contracts.brand_context import BrandContextStatus
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.complete_editing_session import (
    CompleteEditingSession,
    CompleteEditingSessionReadModel,
    CompleteEditingSessionStatus,
    EditingSessionBrandContextBinding,
    EditingSessionRouteBinding,
    EditingSessionSourceBinding,
    EditingSessionStatusEvent,
    new_editing_session_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.complete_editing_session import InMemoryCompleteEditingSessionRepository
from ccp_studio.services.asset_package_service import AssetPackageService
from ccp_studio.services.brand_context_service import BrandContextService
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.expression_review_service import ExpressionReviewService
from ccp_studio.services.routing_service import RoutingService


class CompleteEditingSessionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CompleteEditingSessionService:
    expression_review_service: ExpressionReviewService
    routing_service: RoutingService
    brand_context_service: BrandContextService
    asset_package_service: AssetPackageService | None = None
    repository: InMemoryCompleteEditingSessionRepository = field(default_factory=InMemoryCompleteEditingSessionRepository)

    def create_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        source_expression_moment_id: UUID,
        asset_route_receipt_id: UUID,
        brand_context_version_id: UUID,
        actor_id: UUID,
        asset_package_item_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> CompleteEditingSession:
        try:
            moment = self.expression_review_service.assert_can_route_expression_moment(source_expression_moment_id)
            route_receipt = self.routing_service.repository.receipts.get(asset_route_receipt_id)
            if route_receipt is None:
                raise CompleteEditingSessionServiceError("ASSET_ROUTE_RECEIPT_REQUIRED", "Accepted route receipt is required.")
            if route_receipt.expression_moment_id != source_expression_moment_id:
                raise CompleteEditingSessionServiceError("ROUTE_MOMENT_MISMATCH", "Route receipt does not belong to the source moment.")
            if route_receipt.decision_code != "ASSET_ROUTE_ACCEPTED" or not route_receipt.accepted_route_ids:
                raise CompleteEditingSessionServiceError("ASSET_ROUTE_NOT_ACCEPTED", "Editing requires an accepted route receipt.")
            package_item = self._package_item(asset_package_item_id)
            if package_item is not None:
                if package_item.expression_moment_id != source_expression_moment_id:
                    raise CompleteEditingSessionServiceError("PACKAGE_ITEM_SOURCE_MISMATCH", "Package item source moment mismatch.")
                if package_item.asset_route_receipt_id != asset_route_receipt_id:
                    raise CompleteEditingSessionServiceError("PACKAGE_ITEM_ROUTE_MISMATCH", "Package item route receipt mismatch.")
                if package_item.production_readiness != PackageItemStatus.ready_for_editing_session:
                    raise CompleteEditingSessionServiceError("PACKAGE_ITEM_NOT_READY", "Package item is not ready for editing.")
            brand_context = self.brand_context_service.assert_context_selectable_for_production(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=brand_context_version_id,
            )
            if brand_context.status != BrandContextStatus.locked:
                raise CompleteEditingSessionServiceError("BRAND_CONTEXT_NOT_LOCKED", "Editing requires an active locked Brand Context Version.")
        except Exception as exc:
            self.repository.put_receipt(
                new_editing_session_receipt(
                    organization_id=organization_id,
                    brand_id=brand_id,
                    actor_id=actor_id,
                    command_id=command_id,
                    source_expression_moment_id=source_expression_moment_id,
                    asset_route_receipt_id=asset_route_receipt_id,
                    asset_package_item_id=asset_package_item_id,
                    brand_context_version_id=brand_context_version_id,
                    decision_code="EDITING_SESSION_CREATION_BLOCKED",
                    evidence_refs=[str(exc)],
                )
            )
            raise
        session_id = uuid4()
        session = CompleteEditingSession(
            schema_version="cmf.complete_editing_session.v1",
            complete_editing_session_id=session_id,
            organization_id=organization_id,
            brand_id=brand_id,
            source_expression_session_id=moment.expression_session_id,
            source_expression_moment_id=source_expression_moment_id,
            asset_route_receipt_id=asset_route_receipt_id,
            asset_package_item_id=asset_package_item_id,
            brand_context_version_id=brand_context.brand_context_version_id,
            brand_context_version_hash=brand_context.version_hash,
            registry_bundle_version=route_receipt.registry_bundle_version,
            created_by_user_id=actor_id,
            status=CompleteEditingSessionStatus.created,
            production_readiness="scene_spec_pending",
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.repository.put_session(session)
        self.repository.put_source_binding(
            EditingSessionSourceBinding(
                schema_version="cmf.editing_session_source_binding.v1",
                editing_session_source_binding_id=uuid4(),
                complete_editing_session_id=session_id,
                source_expression_session_id=moment.expression_session_id,
                source_expression_moment_id=source_expression_moment_id,
                source_refs=[f"expression_moment:{source_expression_moment_id}", *[f"candidate:{item}" for item in moment.source_candidate_ids]],
            )
        )
        self.repository.put_route_binding(
            EditingSessionRouteBinding(
                schema_version="cmf.editing_session_route_binding.v1",
                editing_session_route_binding_id=uuid4(),
                complete_editing_session_id=session_id,
                asset_route_receipt_id=asset_route_receipt_id,
                accepted_route_ids=route_receipt.accepted_route_ids,
                registry_bundle_version=route_receipt.registry_bundle_version,
                registry_refs=route_receipt.registry_entry_refs,
            )
        )
        self.repository.put_brand_context_binding(
            EditingSessionBrandContextBinding(
                schema_version="cmf.editing_session_brand_context_binding.v1",
                editing_session_brand_context_binding_id=uuid4(),
                complete_editing_session_id=session_id,
                brand_context_version_id=brand_context.brand_context_version_id,
                brand_context_version_hash=brand_context.version_hash,
                clearance_certificate_id=brand_context.clearance_certificate_id,
            )
        )
        self.repository.put_receipt(
            new_editing_session_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                command_id=command_id,
                complete_editing_session_id=session_id,
                source_expression_moment_id=source_expression_moment_id,
                asset_route_receipt_id=asset_route_receipt_id,
                asset_package_item_id=asset_package_item_id,
                brand_context_version_id=brand_context.brand_context_version_id,
                brand_context_version_hash=brand_context.version_hash,
                registry_bundle_version=route_receipt.registry_bundle_version,
                decision_code="COMPLETE_EDITING_SESSION_CREATED",
                evidence_refs=[
                    f"expression_moment:{source_expression_moment_id}",
                    f"asset_route_receipt:{asset_route_receipt_id}",
                    f"brand_context_version:{brand_context.brand_context_version_id}",
                    brand_context.version_hash,
                ],
            )
        )
        self.repository.put_status_event(
            EditingSessionStatusEvent(
                schema_version="cmf.editing_session_status_event.v1",
                editing_session_status_event_id=uuid4(),
                complete_editing_session_id=session_id,
                previous_status=None,
                next_status=CompleteEditingSessionStatus.created,
                reason="Complete Editing Session created after source, route, and brand-context validation.",
                actor_id=actor_id,
                occurred_at=utc_now(),
            )
        )
        return session

    def start_workflow(self, *, complete_editing_session_id: UUID, actor_id: UUID) -> EditingSessionStatusEvent:
        session = self._session(complete_editing_session_id)
        return self.repository.put_status_event(
            EditingSessionStatusEvent(
                schema_version="cmf.editing_session_status_event.v1",
                editing_session_status_event_id=uuid4(),
                complete_editing_session_id=session.complete_editing_session_id,
                previous_status=session.status,
                next_status=CompleteEditingSessionStatus.scene_spec_pending,
                reason="Complete Editing Session workflow started.",
                actor_id=actor_id,
                occurred_at=utc_now(),
            )
        )

    def read_model(self, complete_editing_session_id: UUID) -> CompleteEditingSessionReadModel:
        session = self._session(complete_editing_session_id)
        source = next(item for item in self.repository.source_bindings.values() if item.complete_editing_session_id == complete_editing_session_id)
        route = next(item for item in self.repository.route_bindings.values() if item.complete_editing_session_id == complete_editing_session_id)
        return CompleteEditingSessionReadModel(
            schema_version="cmf.complete_editing_session_read_model.v1",
            complete_editing_session_id=session.complete_editing_session_id,
            source_expression_moment_id=session.source_expression_moment_id,
            asset_route_receipt_id=session.asset_route_receipt_id,
            asset_package_item_id=session.asset_package_item_id,
            brand_context_version_id=session.brand_context_version_id,
            brand_context_version_hash=session.brand_context_version_hash,
            registry_bundle_version=session.registry_bundle_version,
            status=session.status,
            production_readiness=session.production_readiness,
            source_refs=source.source_refs,
            registry_refs=route.registry_refs,
        )

    def block_creation(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        reason: str,
        command_id: UUID | None = None,
    ):
        return self.repository.put_receipt(
            new_editing_session_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                command_id=command_id,
                decision_code="EDITING_SESSION_CREATION_BLOCKED",
                evidence_refs=[reason],
            )
        )

    def _package_item(self, asset_package_item_id: UUID | None):
        if asset_package_item_id is None:
            return None
        if self.asset_package_service is None:
            raise CompleteEditingSessionServiceError("ASSET_PACKAGE_SERVICE_REQUIRED", "Asset package service is required.")
        for spec in self.asset_package_service.repository.specs.values():
            for item in spec.items:
                if item.package_item_id == asset_package_item_id:
                    return item
        raise CompleteEditingSessionServiceError("ASSET_PACKAGE_ITEM_REQUIRED", "Asset package item is required.")

    def _session(self, complete_editing_session_id: UUID) -> CompleteEditingSession:
        session = self.repository.sessions.get(complete_editing_session_id)
        if session is None:
            raise CompleteEditingSessionServiceError("COMPLETE_EDITING_SESSION_REQUIRED", "Complete Editing Session is required.")
        return session


@dataclass
class CompleteEditingSessionCommandHandler:
    command_type: str
    service: CompleteEditingSessionService
    aggregate_type: str = "complete_editing_session"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateCompleteEditingSessionCommand":
            return self.service.create_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                source_expression_moment_id=UUID(payload["source_expression_moment_id"]),
                asset_route_receipt_id=UUID(payload["asset_route_receipt_id"]),
                asset_package_item_id=UUID(payload["asset_package_item_id"]) if payload.get("asset_package_item_id") else None,
                brand_context_version_id=UUID(payload["brand_context_version_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateEditingSessionSourceCommand":
            moment = self.service.expression_review_service.assert_can_route_expression_moment(UUID(payload["source_expression_moment_id"]))
            return {"source_expression_moment_id": str(moment.expression_moment_id), "validated": True}
        if self.command_type == "ValidateLockedBrandContextForEditingCommand":
            context = self.service.brand_context_service.assert_context_selectable_for_production(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_context_version_id=UUID(payload["brand_context_version_id"]),
            )
            return {"brand_context_version_id": str(context.brand_context_version_id), "version_hash": context.version_hash}
        if self.command_type == "StartCompleteEditingSessionWorkflowCommand":
            return self.service.start_workflow(
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockEditingSessionCreationCommand":
            return self.service.block_creation(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise CompleteEditingSessionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("complete_editing_session_id") or payload.get("source_expression_moment_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_complete_editing_session_command_handlers(bus: CommandBus, service: CompleteEditingSessionService) -> None:
    for command_type in [
        "CreateCompleteEditingSessionCommand",
        "ValidateEditingSessionSourceCommand",
        "ValidateLockedBrandContextForEditingCommand",
        "StartCompleteEditingSessionWorkflowCommand",
        "BlockEditingSessionCreationCommand",
    ]:
        bus.register_handler(CompleteEditingSessionCommandHandler(command_type=command_type, service=service))
