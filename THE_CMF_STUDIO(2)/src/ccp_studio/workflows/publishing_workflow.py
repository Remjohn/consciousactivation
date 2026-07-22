"""Publishing workflow adapters for TS-CMF-054."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.publishing import PublerJob
from ccp_studio.contracts.telegram_review import QuickReviewReceipt
from ccp_studio.services.publishing_service import PublishingService
from ccp_studio.services.telegram_review_service import TelegramReviewService


@dataclass
class PublishingWorkflow:
    publishing_service: PublishingService
    telegram_review_service: TelegramReviewService | None = None

    def stage14_publish_intent(self, publishing_intent_id: UUID, *, idempotency_key: str) -> PublerJob:
        return self.publishing_service.stage14_publish_intent(
            publishing_intent_id,
            idempotency_key=idempotency_key,
        )

    def stage14_telegram_confirmation_handoff(self, **kwargs: Any) -> QuickReviewReceipt:
        if self.telegram_review_service is None:
            raise RuntimeError("TelegramReviewService is required for Telegram confirmation handoff.")
        return self.telegram_review_service.stage14_telegram_confirmation_handoff(**kwargs)
