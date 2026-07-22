"""Surface action service for TS-CMF-007."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import ActorContext, ActorType, new_command_envelope
from ccp_studio.contracts.surfaces import (
    DeepLinkTarget,
    NotificationIntent,
    ObjectStateSnapshot,
    SurfaceActionEnvelope,
    SurfaceCommandResult,
    SurfaceKey,
)
from ccp_studio.repositories.surface_state import (
    InMemoryNotificationIntentRepository,
    InMemoryObjectStateRepository,
)
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.contracts.orchestration import utc_now


ActorRolesProvider = Callable[[UUID, UUID, UUID], list[str]]


@dataclass
class SurfaceActionService:
    command_bus: CommandBus
    object_states: InMemoryObjectStateRepository = field(default_factory=InMemoryObjectStateRepository)
    actor_roles_provider: ActorRolesProvider = lambda _actor_id, _organization_id, _brand_id: []

    def submit(self, action: SurfaceActionEnvelope) -> SurfaceCommandResult:
        current = self.object_states.get(
            action.object_snapshot.object_type,
            action.object_snapshot.object_id,
        )
        if current is None:
            current = self.object_states.put(action.object_snapshot)
        if current.state_version != action.object_snapshot.state_version:
            return SurfaceCommandResult(
                schema_version="cmf.surface_command_result.v1",
                surface_action_id=action.surface_action_id,
                accepted=False,
                result_code="STALE_OBJECT_STATE",
                message="Object state changed before this action was submitted.",
                latest_state=current,
            )
        if (
            action.source_surface != SurfaceKey.pwa
            and action.command_type.lower().startswith("approve")
            and not current.evidence_sufficient_for_surface
        ):
            return SurfaceCommandResult(
                schema_version="cmf.surface_command_result.v1",
                surface_action_id=action.surface_action_id,
                accepted=False,
                result_code="PWA_REVIEW_REQUIRED",
                message="More evidence is required before this approval can proceed.",
                deep_link=self.deep_link_for(action, "evidence_required"),
                latest_state=current,
            )

        envelope = new_command_envelope(
            command_type=action.command_type,
            organization_id=action.organization_id,
            brand_id=action.brand_id,
            actor=ActorContext(
                actor_id=action.actor_id,
                actor_type=ActorType.human,
                role_ids=self.actor_roles_provider(
                    action.actor_id,
                    action.organization_id,
                    action.brand_id,
                ),
            ),
            payload={
                **action.payload,
                "surface_action_id": str(action.surface_action_id),
                "object_type": action.object_snapshot.object_type,
                "object_id": str(action.object_snapshot.object_id),
                "object_state_version": action.object_snapshot.state_version,
            },
            source_surface=action.source_surface.value,
            idempotency_key=action.idempotency_key,
        )
        command_result = self.command_bus.submit(envelope)
        if command_result.passed:
            next_state = action.payload.get("next_state", current.state)
            next_version = action.payload.get("next_state_version", str(uuid4()))
            current = self.object_states.put(
                current.model_copy(update={"state": next_state, "state_version": next_version})
            )
        return SurfaceCommandResult(
            schema_version="cmf.surface_command_result.v1",
            surface_action_id=action.surface_action_id,
            command_id=command_result.command_id,
            accepted=command_result.passed,
            result_code=command_result.status.value,
            message="Command submitted through canonical Command Bus.",
            latest_state=current,
            receipt_id=command_result.audit_receipt_id,
        )

    def deep_link_for(self, action: SurfaceActionEnvelope, reason: str) -> DeepLinkTarget:
        return DeepLinkTarget(
            schema_version="cmf.deep_link_target.v1",
            target_surface="pwa",
            route=f"/brands/{action.brand_id}/{action.object_snapshot.object_type}/{action.object_snapshot.object_id}",
            object_type=action.object_snapshot.object_type,
            object_id=action.object_snapshot.object_id,
            brand_id=action.brand_id,
            required_reason=reason,
        )


@dataclass
class NotificationIntentService:
    object_states: InMemoryObjectStateRepository
    repository: InMemoryNotificationIntentRepository = field(default_factory=InMemoryNotificationIntentRepository)

    def create_from_latest_state(
        self,
        *,
        object_type: str,
        object_id: UUID,
        target_surface: SurfaceKey,
        message_key: str,
    ) -> NotificationIntent:
        snapshot = self.object_states.get(object_type, object_id)
        if snapshot is None:
            raise ValueError("latest object state is required for notification")
        intent = NotificationIntent(
            schema_version="cmf.notification_intent.v1",
            notification_intent_id=uuid4(),
            organization_id=snapshot.organization_id,
            brand_id=snapshot.brand_id,
            object_snapshot=snapshot,
            target_surface=target_surface,
            message_key=message_key,
            created_at=utc_now(),
        )
        return self.repository.put(intent)
