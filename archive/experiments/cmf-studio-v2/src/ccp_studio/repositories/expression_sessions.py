"""Complete Expression Session repositories for TS-CMF-029."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.expression_session import (
    CompleteExpressionSession,
    ExpressionSessionStatusEvent,
    SessionStartReceipt,
)


@dataclass
class InMemoryExpressionSessionRepository:
    sessions: dict[UUID, CompleteExpressionSession] = field(default_factory=dict)
    status_events: dict[UUID, ExpressionSessionStatusEvent] = field(default_factory=dict)
    receipts: dict[UUID, SessionStartReceipt] = field(default_factory=dict)

    def put_session(self, session: CompleteExpressionSession) -> CompleteExpressionSession:
        self.sessions[session.expression_session_id] = session
        return session

    def put_status_event(self, event: ExpressionSessionStatusEvent) -> ExpressionSessionStatusEvent:
        self.status_events[event.status_event_id] = event
        return event

    def put_receipt(self, receipt: SessionStartReceipt) -> SessionStartReceipt:
        self.receipts[receipt.session_start_receipt_id] = receipt
        return receipt

    def sessions_for_brand(self, organization_id: UUID, brand_id: UUID) -> list[CompleteExpressionSession]:
        return [
            session
            for session in self.sessions.values()
            if session.organization_id == organization_id and session.brand_id == brand_id
        ]
