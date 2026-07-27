"""Telegram quick review contracts for TS-CMF-055."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.surfaces import DeepLinkTarget


class TelegramQuickActionType(str, Enum):
    approve = "approve"
    reject = "reject"
    request_revision = "request_revision"
    open_pwa_review = "open_pwa_review"


class TelegramQuickReviewResultCode(str, Enum):
    notification_sent = "notification_sent"
    quick_action_succeeded = "quick_action_succeeded"
    pwa_handoff_required = "pwa_handoff_required"
    stale_action_rejected = "stale_action_rejected"
    tamper_rejected = "tamper_rejected"
    token_expired = "token_expired"
    action_not_allowed = "action_not_allowed"
    command_rejected = "command_rejected"
    command_failed = "command_failed"


class EvidenceSufficiencyDecision(BaseModel):
    schema_version: Literal["cmf.telegram_evidence_sufficiency_decision.v1"]
    decision_id: UUID
    object_id: UUID
    quick_actions_allowed: bool
    required_pwa_review: bool
    reasons: list[str] = Field(default_factory=list)
    review_state_id: UUID
    approval_policy_report_id: UUID | None = None
    created_at: datetime


class QuickActionToken(BaseModel):
    schema_version: Literal["cmf.quick_action_token.v1"]
    token_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    user_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    allowed_actions: list[TelegramQuickActionType] = Field(min_length=1)
    evidence_sufficiency_decision_id: UUID
    approval_policy_report_id: UUID | None = None
    expires_at: datetime
    idempotency_key: str = Field(min_length=1)
    issued_at: datetime
    revoked_at: datetime | None = None

    @model_validator(mode="after")
    def open_pwa_must_remain_available(self):
        if TelegramQuickActionType.open_pwa_review not in self.allowed_actions:
            raise ValueError("quick action tokens must include open_pwa_review")
        return self


class TelegramReviewNotification(BaseModel):
    schema_version: Literal["cmf.telegram_review_notification.v1"]
    notification_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    preview_uri: str = Field(min_length=1)
    route_summary: str = Field(min_length=1)
    source_snippet: str = Field(min_length=1)
    consent_status: str = Field(min_length=1)
    evaluation_summary: str = Field(min_length=1)
    required_action: str = Field(min_length=1)
    pwa_review_url: str = Field(min_length=1)
    quick_action_token_id: UUID
    quick_actions: list[TelegramQuickActionType] = Field(min_length=1)
    evidence_sufficiency_decision_id: UUID
    sent_at: datetime


class TelegramQuickAction(BaseModel):
    schema_version: Literal["cmf.telegram_quick_action.v1"]
    quick_action_id: UUID
    token_id: UUID
    user_id: UUID
    action_type: TelegramQuickActionType
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    submitted_at: datetime


class QuickReviewReceipt(BaseModel):
    schema_version: Literal["cmf.quick_review_receipt.v1"]
    quick_review_receipt_id: UUID
    notification_id: UUID | None = None
    token_id: UUID | None = None
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    review_state_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    object_version_hash: str = Field(min_length=1)
    action_type: TelegramQuickActionType
    evidence_sufficiency_decision_id: UUID | None = None
    quick_actions_allowed: bool
    result_code: TelegramQuickReviewResultCode
    command_id: UUID | None = None
    command_status: str | None = None
    command_receipt_id: UUID | None = None
    review_decision_receipt_id: UUID | None = None
    pwa_handoff_required: bool
    pwa_deep_link: DeepLinkTarget | None = None
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class TelegramReviewDomainEvent(BaseModel):
    schema_version: Literal["cmf.telegram_review_domain_event.v1"]
    telegram_review_event_id: UUID
    event_type: str = Field(min_length=1)
    review_state_id: UUID | None = None
    object_type: str | None = None
    object_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def telegram_review_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_quick_review_receipt(
    *,
    actor_id: UUID,
    organization_id: UUID,
    brand_id: UUID,
    review_state_id: UUID,
    object_type: str,
    object_id: UUID,
    object_version_hash: str,
    action_type: TelegramQuickActionType,
    quick_actions_allowed: bool,
    result_code: TelegramQuickReviewResultCode,
    notification_id: UUID | None = None,
    token_id: UUID | None = None,
    evidence_sufficiency_decision_id: UUID | None = None,
    command_id: UUID | None = None,
    command_status: str | None = None,
    command_receipt_id: UUID | None = None,
    review_decision_receipt_id: UUID | None = None,
    pwa_handoff_required: bool = False,
    pwa_deep_link: DeepLinkTarget | None = None,
    blocker_codes: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> QuickReviewReceipt:
    payload = {
        "notification_id": notification_id,
        "token_id": token_id,
        "actor_id": actor_id,
        "organization_id": organization_id,
        "brand_id": brand_id,
        "review_state_id": review_state_id,
        "object_type": object_type,
        "object_id": object_id,
        "object_version_hash": object_version_hash,
        "action_type": action_type.value,
        "evidence_sufficiency_decision_id": evidence_sufficiency_decision_id,
        "quick_actions_allowed": quick_actions_allowed,
        "result_code": result_code.value,
        "command_id": command_id,
        "command_status": command_status,
        "command_receipt_id": command_receipt_id,
        "review_decision_receipt_id": review_decision_receipt_id,
        "pwa_handoff_required": pwa_handoff_required,
        "pwa_deep_link": pwa_deep_link.model_dump(mode="json") if pwa_deep_link else None,
        "blocker_codes": blocker_codes or [],
        "evidence_refs": evidence_refs or [],
    }
    return QuickReviewReceipt(
        schema_version="cmf.quick_review_receipt.v1",
        quick_review_receipt_id=uuid4(),
        notification_id=notification_id,
        token_id=token_id,
        actor_id=actor_id,
        organization_id=organization_id,
        brand_id=brand_id,
        review_state_id=review_state_id,
        object_type=object_type,
        object_id=object_id,
        object_version_hash=object_version_hash,
        action_type=action_type,
        evidence_sufficiency_decision_id=evidence_sufficiency_decision_id,
        quick_actions_allowed=quick_actions_allowed,
        result_code=result_code,
        command_id=command_id,
        command_status=command_status,
        command_receipt_id=command_receipt_id,
        review_decision_receipt_id=review_decision_receipt_id,
        pwa_handoff_required=pwa_handoff_required,
        pwa_deep_link=pwa_deep_link,
        blocker_codes=blocker_codes or [],
        evidence_refs=evidence_refs or [],
        receipt_hash=telegram_review_hash(payload),
        written_at=utc_now(),
    )
