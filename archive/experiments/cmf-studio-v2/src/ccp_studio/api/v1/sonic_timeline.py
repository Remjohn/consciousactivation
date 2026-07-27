"""FastAPI adapter for TS-CMF-047 sonic timeline assembly."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.sonic_timeline import (
    DuckingDecision,
    SonicAudioMixManifest,
    SonicCaptionManifest,
    SonicTimelineManifest,
    SonicTimelineReceipt,
    SonicTimelineReviewReadModel,
    VoiceBridgePolicyValidation,
)
from ccp_studio.contracts.voice import VoiceBoostEligibilityReport
from ccp_studio.services.sonic_timeline_service import SonicTimelineService


router = APIRouter(prefix="/api/v1/sonic-timeline", tags=["sonic-timeline"])
_sonic_timeline_service: SonicTimelineService | None = None


class CompileAudioMixRequest(BaseModel):
    render_output_id: UUID
    components: list[dict[str, Any]]
    actor_id: UUID


class CompileCaptionManifestRequest(BaseModel):
    render_output_id: UUID
    platform_variant: str
    caption_segments: list[dict[str, Any]]
    style_constraints: dict[str, Any] = Field(default_factory=dict)
    actor_id: UUID


class CompileTimelineManifestRequest(BaseModel):
    render_output_id: UUID
    duration_ms: int
    segments: list[dict[str, Any]]
    actor_id: UUID


class EvaluateDuckingRequest(BaseModel):
    audio_mix_manifest_id: UUID
    ducking_rules: list[dict[str, Any]]
    actor_id: UUID


class ValidateVoiceBridgePolicyRequest(BaseModel):
    audio_mix_manifest_id: UUID
    actor_id: UUID
    voice_boost_report: VoiceBoostEligibilityReport | None = None
    voice_bridge_manifest_id: UUID | None = None


class WriteSonicTimelineReceiptRequest(BaseModel):
    render_output_id: UUID
    audio_mix_manifest_id: UUID
    caption_manifest_id: UUID
    timeline_manifest_id: UUID
    actor_id: UUID
    ducking_decision_ids: list[UUID] = Field(default_factory=list)
    voice_bridge_policy_validation_id: UUID | None = None


def set_sonic_timeline_service(service: SonicTimelineService) -> None:
    global _sonic_timeline_service
    _sonic_timeline_service = service


def get_sonic_timeline_service() -> SonicTimelineService:
    if _sonic_timeline_service is None:
        raise RuntimeError("SonicTimelineService must be configured by the application.")
    return _sonic_timeline_service


@router.post("/audio-mixes", response_model=SonicAudioMixManifest)
def compile_audio_mix_manifest(
    request: CompileAudioMixRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> SonicAudioMixManifest:
    return service.compile_audio_mix_manifest(**request.model_dump())


@router.post("/captions", response_model=SonicCaptionManifest)
def compile_caption_manifest(
    request: CompileCaptionManifestRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> SonicCaptionManifest:
    return service.compile_caption_manifest(**request.model_dump())


@router.post("/timelines", response_model=SonicTimelineManifest)
def compile_timeline_manifest(
    request: CompileTimelineManifestRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> SonicTimelineManifest:
    return service.compile_timeline_manifest(**request.model_dump())


@router.post("/ducking", response_model=list[DuckingDecision])
def evaluate_audio_ducking(
    request: EvaluateDuckingRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> list[DuckingDecision]:
    return service.evaluate_audio_ducking(**request.model_dump())


@router.post("/voice-bridge-policy", response_model=VoiceBridgePolicyValidation)
def validate_voice_bridge_policy(
    request: ValidateVoiceBridgePolicyRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> VoiceBridgePolicyValidation:
    return service.validate_voice_bridge_policy(**request.model_dump())


@router.post("/receipts", response_model=SonicTimelineReceipt)
def write_sonic_timeline_receipt(
    request: WriteSonicTimelineReceiptRequest,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> SonicTimelineReceipt:
    return service.write_sonic_timeline_receipt(**request.model_dump())


@router.get("/receipts/{sonic_timeline_receipt_id}/review", response_model=SonicTimelineReviewReadModel)
def review_sonic_timeline_receipt(
    sonic_timeline_receipt_id: UUID,
    service: SonicTimelineService = Depends(get_sonic_timeline_service),
) -> SonicTimelineReviewReadModel:
    return service.build_review_read_model(sonic_timeline_receipt_id)
