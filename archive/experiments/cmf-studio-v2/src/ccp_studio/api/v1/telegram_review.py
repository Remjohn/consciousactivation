"""FastAPI adapter for TS-CMF-055 Telegram quick review."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.telegram_review import (
    EvidenceSufficiencyDecision,
    QuickReviewReceipt,
    TelegramQuickActionType,
    TelegramReviewNotification,
)
from ccp_studio.services.telegram_review_service import TelegramReviewService


router = APIRouter(prefix="/api/v1/webhooks/telegram", tags=["telegram-review"])
_telegram_review_service: TelegramReviewService | None = None


class TelegramReviewNotificationRequest(BaseModel):
    review_state_id: UUID
    user_id: UUID
    object_version_hash: str
    approval_policy_report_id: UUID | None = None


class TelegramEvidenceSufficiencyRequest(BaseModel):
    review_state_id: UUID
    approval_policy_report_id: UUID | None = None


class TelegramQuickActionRequest(BaseModel):
    token_id: UUID
    user_id: UUID
    action_type: TelegramQuickActionType
    object_version_hash: str
    role_ids: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    action_idempotency_key: str | None = None


def set_telegram_review_service(service: TelegramReviewService) -> None:
    global _telegram_review_service
    _telegram_review_service = service


def get_telegram_review_service() -> TelegramReviewService:
    if _telegram_review_service is None:
        raise RuntimeError("TelegramReviewService must be configured by the application.")
    return _telegram_review_service


@router.post("/notifications", response_model=TelegramReviewNotification)
def send_review_notification(
    request: TelegramReviewNotificationRequest,
    service: TelegramReviewService = Depends(get_telegram_review_service),
) -> TelegramReviewNotification:
    return service.send_review_notification(**request.model_dump())


@router.post("/evidence-sufficiency", response_model=EvidenceSufficiencyDecision)
def evaluate_evidence_sufficiency(
    request: TelegramEvidenceSufficiencyRequest,
    service: TelegramReviewService = Depends(get_telegram_review_service),
) -> EvidenceSufficiencyDecision:
    return service.evaluate_evidence_sufficiency(**request.model_dump())


@router.post("", response_model=QuickReviewReceipt)
def submit_quick_action(
    request: TelegramQuickActionRequest,
    service: TelegramReviewService = Depends(get_telegram_review_service),
) -> QuickReviewReceipt:
    return service.submit_quick_action(**request.model_dump())
