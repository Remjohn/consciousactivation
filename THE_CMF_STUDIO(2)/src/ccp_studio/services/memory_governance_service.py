"""Memory governance service for TS-CMF-057."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.memory_admission import MemoryEvent, MemoryEventStatus
from ccp_studio.contracts.memory_governance import (
    MemoryGovernanceAction,
    MemoryGovernanceActionType,
    MemoryGovernanceDomainEvent,
    MemoryGovernanceEvent,
    MemoryGovernanceReceipt,
    MemoryGovernanceStatus,
    MemoryProjectionUpdateEvent,
    MemoryReviewState,
    MemoryUsagePolicy,
    MemoryUsagePolicyDecision,
    new_memory_governance_action,
    new_memory_governance_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.memory_admission import InMemoryMemoryAdmissionRepository
from ccp_studio.repositories.memory_governance import InMemoryMemoryGovernanceRepository
from ccp_studio.services.command_bus import CommandBus


MEMORY_GOVERNANCE_ROLES = {"owner", "admin", "reviewer", "production_steward", "operator"}


class MemoryGovernanceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class MemoryGovernanceService:
    memory_repository: InMemoryMemoryAdmissionRepository
    repository: InMemoryMemoryGovernanceRepository = field(default_factory=InMemoryMemoryGovernanceRepository)

    def build_memory_review_state(self, memory_event_id: UUID) -> MemoryReviewState:
        event = self._memory_event(memory_event_id)
        status, superseding = self._current_status(event.memory_event_id)
        history = self.repository.history_for_memory(event.memory_event_id)
        evidence_refs = self._evidence_ref_strings(event)
        usage_refs = [
            f"{citation.compiler_or_agent}:{citation.citing_object_ref}:{citation.memory_usage_citation_id}"
            for citation in self.memory_repository.usage_citations.values()
            if citation.memory_event_id == event.memory_event_id
        ]
        state = MemoryReviewState(
            schema_version="cmf.memory_review_state.v1",
            memory_event_id=event.memory_event_id,
            evidence_refs=evidence_refs,
            source_refs=self._source_refs(event),
            route_refs=[event.originating_route_ref] if event.originating_route_ref else [],
            confidence=event.confidence,
            consent_compatible=event.consent_record_version_id is not None,
            created_event_id=event.memory_event_id,
            downstream_usage_refs=usage_refs,
            governance_status=status,
            superseding_memory_event_id=superseding,
            governance_history=history,
        )
        self._domain_event("MemoryReviewStateBuilt", event.memory_event_id, None, {"status": status.value})
        return state

    def correct_memory(
        self,
        *,
        memory_event_id: UUID,
        requested_by_user_id: UUID,
        role_ids: list[str],
        reason: str,
        evidence_refs: list[str],
        corrected_statement: str,
        idempotency_key: str,
    ) -> MemoryGovernanceReceipt:
        return self._apply_governance_action(
            memory_event_id=memory_event_id,
            action_type=MemoryGovernanceActionType.correct,
            requested_by_user_id=requested_by_user_id,
            role_ids=role_ids,
            reason=reason,
            evidence_refs=evidence_refs,
            idempotency_key=idempotency_key,
            corrected_statement=corrected_statement,
        )

    def reverse_memory(self, **kwargs: Any) -> MemoryGovernanceReceipt:
        return self._apply_governance_action(action_type=MemoryGovernanceActionType.reverse, **kwargs)

    def expire_memory(self, **kwargs: Any) -> MemoryGovernanceReceipt:
        return self._apply_governance_action(action_type=MemoryGovernanceActionType.expire, **kwargs)

    def quarantine_memory(self, **kwargs: Any) -> MemoryGovernanceReceipt:
        return self._apply_governance_action(action_type=MemoryGovernanceActionType.quarantine, **kwargs)

    def release_memory_from_quarantine(self, **kwargs: Any) -> MemoryGovernanceReceipt:
        return self._apply_governance_action(action_type=MemoryGovernanceActionType.release_from_quarantine, **kwargs)

    def validate_memory_usage(
        self,
        *,
        memory_event_id: UUID,
        compiler_or_agent: str,
        usage_purpose: str,
    ) -> MemoryUsagePolicyDecision:
        event = self._memory_event(memory_event_id)
        status, superseding = self._current_status(event.memory_event_id)
        allowed = status == MemoryGovernanceStatus.active and event.status == MemoryEventStatus.approved
        decision = MemoryUsagePolicyDecision(
            schema_version="cmf.memory_usage_policy_decision.v1",
            memory_event_id=event.memory_event_id,
            policy=MemoryUsagePolicy.allowed if allowed else MemoryUsagePolicy.blocked,
            governance_status=status,
            active_memory_event_id=event.memory_event_id if allowed else superseding,
            reason="memory_active" if allowed else f"memory_{status.value}_blocks_active_use",
            checked_at=utc_now(),
        )
        if not allowed:
            self._domain_event(
                "MemoryUsageBlocked",
                event.memory_event_id,
                None,
                {"compiler_or_agent": compiler_or_agent, "usage_purpose": usage_purpose, "status": status.value},
            )
        return decision

    def stage14_govern_memory(self, *, action_type: MemoryGovernanceActionType | str, **kwargs: Any) -> MemoryGovernanceReceipt:
        action = MemoryGovernanceActionType(action_type)
        if action == MemoryGovernanceActionType.correct:
            return self.correct_memory(**kwargs)
        if action == MemoryGovernanceActionType.reverse:
            return self.reverse_memory(**kwargs)
        if action == MemoryGovernanceActionType.expire:
            return self.expire_memory(**kwargs)
        if action == MemoryGovernanceActionType.quarantine:
            return self.quarantine_memory(**kwargs)
        return self.release_memory_from_quarantine(**kwargs)

    def _apply_governance_action(
        self,
        *,
        memory_event_id: UUID,
        action_type: MemoryGovernanceActionType,
        requested_by_user_id: UUID,
        role_ids: list[str],
        reason: str,
        evidence_refs: list[str],
        idempotency_key: str,
        corrected_statement: str | None = None,
    ) -> MemoryGovernanceReceipt:
        memory_event_id = UUID(str(memory_event_id))
        prior = self.repository.receipt_for_idempotency(memory_event_id, action_type.value, idempotency_key)
        if prior:
            return prior
        self._assert_role(role_ids)
        event = self._memory_event(memory_event_id)
        prior_status, _prior_superseding = self._current_status(memory_event_id)
        action = self.repository.put_action(
            new_memory_governance_action(
                memory_event_id=memory_event_id,
                action_type=action_type,
                reason=reason,
                evidence_refs=evidence_refs,
                requested_by_user_id=requested_by_user_id,
                corrected_statement=corrected_statement,
            )
        )
        superseding_memory_event_id: UUID | None = None
        if action_type == MemoryGovernanceActionType.correct:
            if not corrected_statement:
                raise MemoryGovernanceError("CORRECTED_STATEMENT_REQUIRED", "Correction requires a corrected statement.")
            superseding = self._superseding_event(event, corrected_statement, requested_by_user_id)
            self.memory_repository.put_memory_event(superseding)
            superseding_memory_event_id = superseding.memory_event_id
            resulting_status = MemoryGovernanceStatus.corrected
            domain_event_type = "MemoryCorrected"
        elif action_type == MemoryGovernanceActionType.reverse:
            resulting_status = MemoryGovernanceStatus.reversed
            domain_event_type = "MemoryReversed"
        elif action_type == MemoryGovernanceActionType.expire:
            resulting_status = MemoryGovernanceStatus.expired
            domain_event_type = "MemoryExpired"
        elif action_type == MemoryGovernanceActionType.quarantine:
            resulting_status = MemoryGovernanceStatus.quarantined
            domain_event_type = "MemoryQuarantined"
        else:
            resulting_status = MemoryGovernanceStatus.active
            domain_event_type = "MemoryReleasedFromQuarantine"
        governance_event = self.repository.put_governance_event(
            MemoryGovernanceEvent(
                schema_version="cmf.memory_governance_event.v1",
                event_id=uuid4(),
                action_id=action.action_id,
                memory_event_id=memory_event_id,
                resulting_status=resulting_status,
                superseding_memory_event_id=superseding_memory_event_id,
                reason=reason,
                evidence_refs=evidence_refs,
                created_at=utc_now(),
            )
        )
        projection = self.repository.put_projection_event(
            MemoryProjectionUpdateEvent(
                schema_version="cmf.memory_projection_update_event.v1",
                projection_event_id=uuid4(),
                memory_event_id=memory_event_id,
                governance_event_id=governance_event.event_id,
                resulting_status=resulting_status,
                rebuild_required=True,
                created_at=utc_now(),
            )
        )
        receipt = self.repository.put_receipt(
            new_memory_governance_receipt(
                action=action,
                prior_status=prior_status,
                resulting_status=resulting_status,
                downstream_usage_effect=self._downstream_effect(resulting_status, superseding_memory_event_id),
                superseding_memory_event_id=superseding_memory_event_id,
                projection_event_id=projection.projection_event_id,
            ),
            idempotency_key=idempotency_key,
        )
        self._domain_event(
            domain_event_type,
            memory_event_id,
            governance_event.event_id,
            {"receipt_id": str(receipt.memory_governance_receipt_id), "resulting_status": resulting_status.value},
        )
        return receipt

    def _current_status(self, memory_event_id: UUID) -> tuple[MemoryGovernanceStatus, UUID | None]:
        event = self._memory_event(memory_event_id)
        if event.status != MemoryEventStatus.approved:
            return MemoryGovernanceStatus.quarantined, None
        history = self.repository.history_for_memory(memory_event_id)
        if not history:
            return MemoryGovernanceStatus.active, None
        latest = history[-1]
        return latest.resulting_status, latest.superseding_memory_event_id

    def _superseding_event(self, event: MemoryEvent, corrected_statement: str, actor_id: UUID) -> MemoryEvent:
        return event.model_copy(
            update={
                "memory_event_id": uuid4(),
                "approved_by": actor_id,
                "proposed_statement": corrected_statement,
                "created_at": utc_now(),
            }
        )

    @staticmethod
    def _downstream_effect(status: MemoryGovernanceStatus, superseding_memory_event_id: UUID | None) -> str:
        if status == MemoryGovernanceStatus.active:
            return "active_memory_usage_allowed"
        if status == MemoryGovernanceStatus.corrected:
            return f"original_memory_blocked_use_superseding:{superseding_memory_event_id}"
        if status == MemoryGovernanceStatus.expired:
            return "active_memory_usage_blocked_historical_only"
        if status == MemoryGovernanceStatus.quarantined:
            return "active_memory_usage_blocked_until_release"
        return "active_memory_usage_blocked_reversed"

    @staticmethod
    def _evidence_ref_strings(event: MemoryEvent) -> list[str]:
        refs: list[str] = []
        for ref in event.evidence_refs:
            refs.append(f"{ref.source_type}:{ref.source_id}")
            if ref.receipt_id:
                refs.append(f"receipt:{ref.receipt_id}")
            if ref.transcript_segment_id:
                refs.append(f"transcript_segment:{ref.transcript_segment_id}")
        return sorted(set(refs))

    @staticmethod
    def _source_refs(event: MemoryEvent) -> list[str]:
        return sorted({f"{ref.source_type}:{ref.source_id}" for ref in event.evidence_refs})

    @staticmethod
    def _assert_role(role_ids: list[str]) -> None:
        if not set(role_ids).intersection(MEMORY_GOVERNANCE_ROLES):
            raise MemoryGovernanceError("ROLE_PERMISSION_DENIED", "Actor lacks a memory governance role.")

    def _memory_event(self, memory_event_id: UUID) -> MemoryEvent:
        event = self.memory_repository.memory_events.get(UUID(str(memory_event_id)))
        if event is None:
            raise MemoryGovernanceError("MEMORY_EVENT_REQUIRED", "Memory event is required.")
        return event

    def _domain_event(
        self,
        event_type: str,
        memory_event_id: UUID | None,
        governance_event_id: UUID | None,
        payload: dict[str, Any],
    ) -> MemoryGovernanceDomainEvent:
        return self.repository.append_event(
            MemoryGovernanceDomainEvent(
                schema_version="cmf.memory_governance_domain_event.v1",
                memory_governance_domain_event_id=uuid4(),
                event_type=event_type,
                memory_event_id=memory_event_id,
                governance_event_id=governance_event_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class MemoryGovernanceCommandHandler:
    command_type: str
    service: MemoryGovernanceService
    aggregate_type: str = "memory_governance"
    allowed_roles: set[str] = field(default_factory=lambda: MEMORY_GOVERNANCE_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "BuildMemoryReviewStateCommand":
            return self.service.build_memory_review_state(UUID(payload["memory_event_id"])).model_dump(mode="json")
        if self.command_type == "ValidateMemoryUsageCommand":
            return self.service.validate_memory_usage(
                memory_event_id=UUID(payload["memory_event_id"]),
                compiler_or_agent=payload["compiler_or_agent"],
                usage_purpose=payload["usage_purpose"],
            ).model_dump(mode="json")
        kwargs = {
            "memory_event_id": UUID(payload["memory_event_id"]),
            "requested_by_user_id": envelope.actor.actor_id,
            "role_ids": envelope.actor.role_ids,
            "reason": payload["reason"],
            "evidence_refs": payload["evidence_refs"],
            "idempotency_key": envelope.idempotency_key,
        }
        if self.command_type == "CorrectMemoryCommand":
            return self.service.correct_memory(
                **kwargs,
                corrected_statement=payload["corrected_statement"],
            ).model_dump(mode="json")
        if self.command_type == "ReverseMemoryCommand":
            return self.service.reverse_memory(**kwargs).model_dump(mode="json")
        if self.command_type == "ExpireMemoryCommand":
            return self.service.expire_memory(**kwargs).model_dump(mode="json")
        if self.command_type == "QuarantineMemoryCommand":
            return self.service.quarantine_memory(**kwargs).model_dump(mode="json")
        if self.command_type == "ReleaseMemoryFromQuarantineCommand":
            return self.service.release_memory_from_quarantine(**kwargs).model_dump(mode="json")
        raise MemoryGovernanceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("memory_event_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_memory_governance_command_handlers(bus: CommandBus, service: MemoryGovernanceService) -> None:
    for command_type in [
        "BuildMemoryReviewStateCommand",
        "CorrectMemoryCommand",
        "ReverseMemoryCommand",
        "ExpireMemoryCommand",
        "QuarantineMemoryCommand",
        "ReleaseMemoryFromQuarantineCommand",
        "ValidateMemoryUsageCommand",
    ]:
        bus.register_handler(MemoryGovernanceCommandHandler(command_type=command_type, service=service))
