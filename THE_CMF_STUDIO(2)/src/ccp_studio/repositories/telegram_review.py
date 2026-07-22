"""Telegram quick review repositories for TS-CMF-055."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.telegram_review import (
    EvidenceSufficiencyDecision,
    QuickActionToken,
    QuickReviewReceipt,
    TelegramQuickActionType,
    TelegramReviewDomainEvent,
    TelegramReviewNotification,
)


@dataclass
class InMemoryTelegramReviewRepository:
    decisions: dict[UUID, EvidenceSufficiencyDecision] = field(default_factory=dict)
    tokens: dict[UUID, QuickActionToken] = field(default_factory=dict)
    notifications: dict[UUID, TelegramReviewNotification] = field(default_factory=dict)
    receipts: dict[UUID, QuickReviewReceipt] = field(default_factory=dict)
    events: list[TelegramReviewDomainEvent] = field(default_factory=list)
    token_notification_index: dict[UUID, UUID] = field(default_factory=dict)
    idempotency_index: dict[tuple[UUID, TelegramQuickActionType, str], UUID] = field(default_factory=dict)

    def put_decision(self, decision: EvidenceSufficiencyDecision) -> EvidenceSufficiencyDecision:
        self.decisions[decision.decision_id] = decision
        return decision

    def put_token(self, token: QuickActionToken) -> QuickActionToken:
        self.tokens[token.token_id] = token
        return token

    def put_notification(self, notification: TelegramReviewNotification) -> TelegramReviewNotification:
        self.notifications[notification.notification_id] = notification
        self.token_notification_index[notification.quick_action_token_id] = notification.notification_id
        return notification

    def put_receipt(
        self,
        receipt: QuickReviewReceipt,
        *,
        idempotency_key: str | None = None,
    ) -> QuickReviewReceipt:
        self.receipts[receipt.quick_review_receipt_id] = receipt
        if receipt.token_id and idempotency_key:
            self.idempotency_index[(receipt.token_id, receipt.action_type, idempotency_key)] = receipt.quick_review_receipt_id
        return receipt

    def receipt_for_idempotency(
        self,
        *,
        token_id: UUID,
        action_type: TelegramQuickActionType,
        idempotency_key: str,
    ) -> QuickReviewReceipt | None:
        receipt_id = self.idempotency_index.get((token_id, action_type, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def append_event(self, event: TelegramReviewDomainEvent) -> TelegramReviewDomainEvent:
        self.events.append(event)
        return event
