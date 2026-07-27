"""Publishing Intent and Publer adapter contracts for TS-CMF-054."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from ccp_studio.contracts.orchestration import utc_now


class PublishingIntentStatus(str, Enum):
    draft = "draft"
    validated = "validated"
    confirmed = "confirmed"
    submitted = "submitted"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"
    blocked = "blocked"


class PublerJobStatus(str, Enum):
    pending = "pending"
    submitted = "submitted"
    scheduled = "scheduled"
    published = "published"
    failed = "failed"
    cancelled = "cancelled"
    pending_retry = "pending_retry"


class PublishingPlatformVariant(BaseModel):
    schema_version: Literal["cmf.publishing_platform_variant.v1"] = "cmf.publishing_platform_variant.v1"
    platform_variant_id: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    asset_uri: str = Field(min_length=1)
    caption_manifest_id: UUID
    platform_format_key: str = Field(min_length=1)
    account_mapping_id: str = Field(min_length=1)


class PublishingSchedule(BaseModel):
    schema_version: Literal["cmf.publishing_schedule.v1"] = "cmf.publishing_schedule.v1"
    schedule_at: datetime
    time_zone: str = Field(min_length=1)

    @field_validator("schedule_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("schedule_at must be timezone-aware")
        return value


class PublishingIntent(BaseModel):
    schema_version: Literal["cmf.publishing_intent.v1"]
    publishing_intent_id: UUID
    organization_id: UUID
    brand_id: UUID
    approved_asset_id: UUID
    approval_event_id: UUID
    consent_record_version_id: UUID
    approver_user_id: UUID
    platform_variants: list[PublishingPlatformVariant] = Field(min_length=1)
    schedule: PublishingSchedule
    confirmed_by_user_id: UUID | None = None
    status: PublishingIntentStatus
    idempotency_key: str = Field(min_length=1)
    compliance_notes: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class PublerJob(BaseModel):
    schema_version: Literal["cmf.publer_job.v1"]
    publer_job_id: UUID
    publishing_intent_id: UUID
    external_job_id: str | None = None
    request_receipt_id: UUID
    status: PublerJobStatus
    idempotency_key: str = Field(min_length=1)
    created_at: datetime
    updated_at: datetime


class PublishingOutcome(BaseModel):
    schema_version: Literal["cmf.publishing_outcome.v1"]
    publishing_outcome_id: UUID
    publishing_intent_id: UUID
    publer_job_id: UUID | None = None
    external_status: PublerJobStatus
    external_url: str | None = None
    failure_reason: str | None = None
    source: Literal["webhook", "poll", "adapter"]
    received_at: datetime


class PublerWebhookEnvelope(BaseModel):
    schema_version: Literal["cmf.publer_webhook_envelope.v1"]
    publer_webhook_id: UUID
    publishing_intent_id: UUID
    external_job_id: str
    external_status: PublerJobStatus
    external_url: str | None = None
    failure_reason: str | None = None
    idempotency_key: str = Field(min_length=1)
    received_at: datetime


class PublishingReceipt(BaseModel):
    schema_version: Literal["cmf.publishing_receipt.v1"]
    publishing_receipt_id: UUID
    publishing_intent_id: UUID | None = None
    organization_id: UUID
    brand_id: UUID
    approved_asset_id: UUID | None = None
    approval_event_id: UUID | None = None
    consent_record_version_id: UUID | None = None
    platform_variant_ids: list[str] = Field(default_factory=list)
    caption_manifest_ids: list[UUID] = Field(default_factory=list)
    schedule_at: datetime | None = None
    time_zone: str | None = None
    publer_job_id: UUID | None = None
    publishing_outcome_id: UUID | None = None
    idempotency_key: str | None = None
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class PublishingDomainEvent(BaseModel):
    schema_version: Literal["cmf.publishing_domain_event.v1"]
    publishing_event_id: UUID
    event_type: str = Field(min_length=1)
    publishing_intent_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def publishing_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_publishing_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    decision_code: str,
    publishing_intent: PublishingIntent | None = None,
    publer_job: PublerJob | None = None,
    outcome: PublishingOutcome | None = None,
    blocker_codes: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    idempotency_key: str | None = None,
) -> PublishingReceipt:
    payload = {
        "organization_id": organization_id,
        "brand_id": brand_id,
        "decision_code": decision_code,
        "publishing_intent_id": publishing_intent.publishing_intent_id if publishing_intent else None,
        "publer_job_id": publer_job.publer_job_id if publer_job else None,
        "outcome_id": outcome.publishing_outcome_id if outcome else None,
        "blocker_codes": blocker_codes or [],
        "evidence_refs": evidence_refs or [],
        "idempotency_key": idempotency_key or (publishing_intent.idempotency_key if publishing_intent else None),
    }
    variants = publishing_intent.platform_variants if publishing_intent else []
    return PublishingReceipt(
        schema_version="cmf.publishing_receipt.v1",
        publishing_receipt_id=uuid4(),
        publishing_intent_id=publishing_intent.publishing_intent_id if publishing_intent else None,
        organization_id=organization_id,
        brand_id=brand_id,
        approved_asset_id=publishing_intent.approved_asset_id if publishing_intent else None,
        approval_event_id=publishing_intent.approval_event_id if publishing_intent else None,
        consent_record_version_id=publishing_intent.consent_record_version_id if publishing_intent else None,
        platform_variant_ids=[variant.platform_variant_id for variant in variants],
        caption_manifest_ids=[variant.caption_manifest_id for variant in variants],
        schedule_at=publishing_intent.schedule.schedule_at if publishing_intent else None,
        time_zone=publishing_intent.schedule.time_zone if publishing_intent else None,
        publer_job_id=publer_job.publer_job_id if publer_job else None,
        publishing_outcome_id=outcome.publishing_outcome_id if outcome else None,
        idempotency_key=idempotency_key or (publishing_intent.idempotency_key if publishing_intent else None),
        decision_code=decision_code,
        blocker_codes=blocker_codes or [],
        evidence_refs=evidence_refs or [],
        receipt_hash=publishing_hash(payload),
        written_at=utc_now(),
    )

