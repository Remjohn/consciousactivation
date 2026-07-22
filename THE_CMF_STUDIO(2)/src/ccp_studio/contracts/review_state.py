"""Evidence-rich review state contracts for TS-CMF-051."""

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


class EvidencePanelType(str, Enum):
    preview = "preview"
    source_quote = "source_quote"
    transcript = "transcript"
    archetype_route = "archetype_route"
    brand_context = "brand_context"
    selected_assets = "selected_assets"
    render_output = "render_output"
    evaluation = "evaluation"
    revision_history = "revision_history"
    consent_state = "consent_state"


class EvidenceCompleteness(str, Enum):
    complete = "complete"
    missing = "missing"
    conflicting = "conflicting"


class TelegramComplexity(str, Enum):
    quick_allowed = "quick_allowed"
    pwa_required = "pwa_required"


class EvidencePanel(BaseModel):
    schema_version: Literal["cmf.evidence_panel.v1"] = "cmf.evidence_panel.v1"
    panel_type: EvidencePanelType
    object_refs: list[str] = Field(default_factory=list)
    summary: str = Field(min_length=1)
    completeness: EvidenceCompleteness
    blocker_codes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def complete_panels_need_refs(self):
        if self.completeness == EvidenceCompleteness.complete and not self.object_refs:
            raise ValueError("complete evidence panels require object refs")
        return self


class EvaluationFailureView(BaseModel):
    schema_version: Literal["cmf.evaluation_failure_view.v1"] = "cmf.evaluation_failure_view.v1"
    evaluation_receipt_id: UUID
    category: str = Field(min_length=1)
    failure_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    repair_recommendation: str = Field(min_length=1)


class RevisionHistoryItem(BaseModel):
    schema_version: Literal["cmf.revision_history_item.v1"] = "cmf.revision_history_item.v1"
    revision_request_id: UUID | None = None
    revision_version_id: UUID | None = None
    target_object_type: str = Field(min_length=1)
    target_object_id: UUID
    prior_version_id: UUID | None = None
    reason: str = Field(min_length=1)
    decision_code: str | None = None
    created_at: datetime


class ConsentCompatibilitySnapshot(BaseModel):
    schema_version: Literal["cmf.consent_compatibility_snapshot.v1"]
    consent_record_version_id: UUID
    status: str = Field(min_length=1)
    compatible: bool
    changed_after_render: bool
    blocker_codes: list[str] = Field(default_factory=list)


class ReviewEvidenceState(BaseModel):
    schema_version: Literal["cmf.review_evidence_state.v1"]
    review_state_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    approval_evidence_view_id: UUID
    panels: list[EvidencePanel] = Field(min_length=1)
    evaluation_failures: list[EvaluationFailureView] = Field(default_factory=list)
    revision_history: list[RevisionHistoryItem] = Field(default_factory=list)
    consent_snapshot: ConsentCompatibilitySnapshot
    brand_context_version_id: UUID | None = None
    selected_asset_refs: list[str] = Field(default_factory=list)
    render_output_refs: list[str] = Field(default_factory=list)
    pwa_route: str = Field(min_length=1)
    telegram_complexity: TelegramComplexity
    pwa_deep_link: DeepLinkTarget | None = None
    generated_at: datetime


class ReviewStateReceipt(BaseModel):
    schema_version: Literal["cmf.review_state_receipt.v1"]
    review_state_receipt_id: UUID
    review_state_id: UUID
    organization_id: UUID
    brand_id: UUID
    object_type: str = Field(min_length=1)
    object_id: UUID
    panel_completeness: dict[str, str]
    consent_compatible: bool
    evaluation_failure_ids: list[str] = Field(default_factory=list)
    revision_history_hash: str = Field(min_length=1)
    surface_route: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    command_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class ReviewStateDomainEvent(BaseModel):
    schema_version: Literal["cmf.review_state_domain_event.v1"]
    review_state_event_id: UUID
    event_type: str = Field(min_length=1)
    review_state_id: UUID | None = None
    object_type: str | None = None
    object_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def review_state_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_review_state_receipt(
    *,
    state: ReviewEvidenceState,
    command_id: UUID | None = None,
) -> ReviewStateReceipt:
    revision_payload = [item.model_dump(mode="json") for item in state.revision_history]
    revision_history_hash = review_state_hash(revision_payload)
    panel_completeness = {panel.panel_type.value: panel.completeness.value for panel in state.panels}
    evaluation_failure_ids = [
        f"{failure.evaluation_receipt_id}:{failure.category}:{failure.failure_code}"
        for failure in state.evaluation_failures
    ]
    evidence_refs = [
        str(state.approval_evidence_view_id),
        *[ref for panel in state.panels for ref in panel.object_refs],
        *[ref for failure in state.evaluation_failures for ref in failure.evidence_refs],
    ]
    payload = {
        "review_state_id": state.review_state_id,
        "organization_id": state.organization_id,
        "brand_id": state.brand_id,
        "object_type": state.object_type,
        "object_id": state.object_id,
        "panel_completeness": panel_completeness,
        "consent_compatible": state.consent_snapshot.compatible,
        "evaluation_failure_ids": evaluation_failure_ids,
        "revision_history_hash": revision_history_hash,
        "surface_route": state.pwa_route,
        "evidence_refs": evidence_refs,
    }
    return ReviewStateReceipt(
        schema_version="cmf.review_state_receipt.v1",
        review_state_receipt_id=uuid4(),
        review_state_id=state.review_state_id,
        organization_id=state.organization_id,
        brand_id=state.brand_id,
        object_type=state.object_type,
        object_id=state.object_id,
        panel_completeness=panel_completeness,
        consent_compatible=state.consent_snapshot.compatible,
        evaluation_failure_ids=evaluation_failure_ids,
        revision_history_hash=revision_history_hash,
        surface_route=state.pwa_route,
        evidence_refs=evidence_refs,
        command_id=command_id,
        receipt_hash=review_state_hash(payload),
        written_at=utc_now(),
    )

