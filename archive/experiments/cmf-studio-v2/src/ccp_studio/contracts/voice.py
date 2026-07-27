"""Voice-DNA Boost contracts for TS-CMF-011."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.audio import (
    AudioMixManifest,
    AudioSegmentClassification,
    AudioSourceType,
)
from ccp_studio.contracts.orchestration import utc_now


class VoiceEligibilityStatus(str, Enum):
    eligible = "eligible"
    blocked = "blocked"
    review_required = "review_required"


class VoiceBridgeClaimCategory(str, Enum):
    bridge_context = "bridge_context"
    clarifying_connector = "clarifying_connector"
    primary_claim = "primary_claim"
    decisive_confession = "decisive_confession"
    medical_advice = "medical_advice"
    legal_advice = "legal_advice"
    financial_advice = "financial_advice"
    decisive_emotional_truth = "decisive_emotional_truth"
    sensitive_assertion = "sensitive_assertion"


class RepairHierarchyProof(BaseModel):
    schema_version: Literal["cmf.repair_hierarchy_proof.v1"]
    recut_checked: bool
    verbatim_fragment_search_checked: bool
    prior_approved_quote_checked: bool
    human_pickup_request_checked: bool
    evidence_refs: list[str] = Field(default_factory=list)

    @property
    def exhausted(self) -> bool:
        return all(
            [
                self.recut_checked,
                self.verbatim_fragment_search_checked,
                self.prior_approved_quote_checked,
                self.human_pickup_request_checked,
            ]
        )


class CalibrationReport(BaseModel):
    schema_version: Literal["cmf.calibration_report.v1"]
    calibration_report_id: UUID
    render_output_id: UUID
    semantic_continuity_score: float = Field(ge=0, le=1)
    voice_continuity_score: float = Field(ge=0, le=1)
    anti_draft_score: float = Field(ge=0, le=1)
    passed: bool
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class VoiceBoostEligibilityReport(BaseModel):
    schema_version: Literal["cmf.voice_boost_eligibility_report.v1"]
    voice_boost_eligibility_report_id: UUID
    organization_id: UUID
    brand_id: UUID
    render_output_id: UUID
    status: VoiceEligibilityStatus
    consent_record_version_id: UUID
    repair_hierarchy: RepairHierarchyProof
    max_duration_seconds: float
    requested_duration_seconds: float
    visual_covering_required: bool
    visual_covering_provided: bool
    claim_restriction_passed: bool
    evaluation_receipt_ids: list[UUID]
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class ProviderReceipt(BaseModel):
    schema_version: Literal["cmf.provider_receipt.v1"]
    provider_receipt_id: UUID
    provider_name: str
    operation: str
    artifact_uri: str
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime


class VoiceBridgeManifest(BaseModel):
    schema_version: Literal["cmf.voice_bridge_manifest.v1"]
    voice_bridge_manifest_id: UUID
    voice_boost_eligibility_report_id: UUID
    render_output_id: UUID
    provider_receipt_id: UUID
    synthetic_audio_uri: str
    requested_duration_seconds: float
    max_duration_seconds: float
    duration_cap_compliant: bool
    visual_covering_ref: str
    claim_categories: list[VoiceBridgeClaimCategory]
    created_at: datetime


class VoiceEligibilityReceipt(BaseModel):
    schema_version: Literal["cmf.voice_eligibility_receipt.v1"]
    voice_eligibility_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    render_output_id: UUID
    voice_boost_eligibility_report_id: UUID
    decision_code: str
    consent_record_version_id: UUID
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def new_repair_hierarchy_proof(
    *,
    recut_checked: bool,
    verbatim_fragment_search_checked: bool,
    prior_approved_quote_checked: bool,
    human_pickup_request_checked: bool,
    evidence_refs: list[str],
) -> RepairHierarchyProof:
    return RepairHierarchyProof(
        schema_version="cmf.repair_hierarchy_proof.v1",
        recut_checked=recut_checked,
        verbatim_fragment_search_checked=verbatim_fragment_search_checked,
        prior_approved_quote_checked=prior_approved_quote_checked,
        human_pickup_request_checked=human_pickup_request_checked,
        evidence_refs=evidence_refs,
    )


def new_calibration_report(
    *,
    render_output_id: UUID,
    semantic_continuity_score: float,
    voice_continuity_score: float,
    anti_draft_score: float,
    evidence_refs: list[str],
    pass_threshold: float = 0.85,
) -> CalibrationReport:
    return CalibrationReport(
        schema_version="cmf.calibration_report.v1",
        calibration_report_id=uuid4(),
        render_output_id=render_output_id,
        semantic_continuity_score=semantic_continuity_score,
        voice_continuity_score=voice_continuity_score,
        anti_draft_score=anti_draft_score,
        passed=min(semantic_continuity_score, voice_continuity_score, anti_draft_score) >= pass_threshold,
        evidence_refs=evidence_refs,
        created_at=utc_now(),
    )


__all__ = [
    "AudioMixManifest",
    "AudioSegmentClassification",
    "AudioSourceType",
    "CalibrationReport",
    "ProviderReceipt",
    "RepairHierarchyProof",
    "VoiceBoostEligibilityReport",
    "VoiceBridgeClaimCategory",
    "VoiceBridgeManifest",
    "VoiceEligibilityReceipt",
    "VoiceEligibilityStatus",
    "new_calibration_report",
    "new_repair_hierarchy_proof",
]
