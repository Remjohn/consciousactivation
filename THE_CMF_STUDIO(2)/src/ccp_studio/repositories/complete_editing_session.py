"""Complete Editing Session repositories for TS-CMF-036."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.complete_editing_session import (
    CompleteEditingSession,
    EditingSessionBrandContextBinding,
    EditingSessionReceipt,
    EditingSessionRouteBinding,
    EditingSessionSourceBinding,
    EditingSessionStatusEvent,
)


@dataclass
class InMemoryCompleteEditingSessionRepository:
    sessions: dict[UUID, CompleteEditingSession] = field(default_factory=dict)
    source_bindings: dict[UUID, EditingSessionSourceBinding] = field(default_factory=dict)
    route_bindings: dict[UUID, EditingSessionRouteBinding] = field(default_factory=dict)
    brand_context_bindings: dict[UUID, EditingSessionBrandContextBinding] = field(default_factory=dict)
    status_events: dict[UUID, EditingSessionStatusEvent] = field(default_factory=dict)
    receipts: dict[UUID, EditingSessionReceipt] = field(default_factory=dict)

    def put_session(self, session: CompleteEditingSession) -> CompleteEditingSession:
        self.sessions[session.complete_editing_session_id] = session
        return session

    def put_source_binding(self, binding: EditingSessionSourceBinding) -> EditingSessionSourceBinding:
        self.source_bindings[binding.editing_session_source_binding_id] = binding
        return binding

    def put_route_binding(self, binding: EditingSessionRouteBinding) -> EditingSessionRouteBinding:
        self.route_bindings[binding.editing_session_route_binding_id] = binding
        return binding

    def put_brand_context_binding(
        self,
        binding: EditingSessionBrandContextBinding,
    ) -> EditingSessionBrandContextBinding:
        self.brand_context_bindings[binding.editing_session_brand_context_binding_id] = binding
        return binding

    def put_status_event(self, event: EditingSessionStatusEvent) -> EditingSessionStatusEvent:
        self.status_events[event.editing_session_status_event_id] = event
        return event

    def put_receipt(self, receipt: EditingSessionReceipt) -> EditingSessionReceipt:
        self.receipts[receipt.editing_session_receipt_id] = receipt
        return receipt
