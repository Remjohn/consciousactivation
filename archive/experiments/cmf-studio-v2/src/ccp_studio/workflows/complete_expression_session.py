"""Complete Expression Session workflow adapter for TS-CMF-029."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.expression_session import CompleteExpressionSession
from ccp_studio.contracts.expression_review import ExpressionReviewReceipt
from ccp_studio.contracts.extraction import ExtractionReceipt
from ccp_studio.contracts.asset_package import AssetPackageSpec
from ccp_studio.contracts.rejection_memory import RejectionCategory, RejectionReceipt
from ccp_studio.contracts.routing import AssetRouteReceipt
from ccp_studio.contracts.source_provenance import (
    IngestedRecordingArtifact,
    RecordingArtifactType,
    TranscriptAlignmentMap,
    TranscriptRevision,
    TranscriptSegment,
    TranscriptSource,
)
from ccp_studio.services.expression_session_service import CompleteExpressionSessionService
from ccp_studio.services.expression_review_service import ExpressionReviewService
from ccp_studio.services.extraction_service import ExtractionService
from ccp_studio.services.asset_package_service import AssetPackageService
from ccp_studio.services.rejection_memory_service import RejectionMemoryService
from ccp_studio.services.routing_service import RoutingService
from ccp_studio.services.source_provenance_service import SourceProvenanceService


@dataclass
class CompleteExpressionSessionWorkflow:
    service: CompleteExpressionSessionService
    source_provenance_service: SourceProvenanceService | None = None
    extraction_service: ExtractionService | None = None
    expression_review_service: ExpressionReviewService | None = None
    routing_service: RoutingService | None = None
    asset_package_service: AssetPackageService | None = None
    rejection_memory_service: RejectionMemoryService | None = None

    def __post_init__(self) -> None:
        if self.source_provenance_service is None:
            self.source_provenance_service = SourceProvenanceService(self.service)

    def stage5_start_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
    ) -> CompleteExpressionSession:
        return self.service.start_session(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
        )

    def stage5_ingest_and_align(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        filename: str,
        content: str,
        retention_policy_id: UUID,
        segments: list[TranscriptSegment],
    ) -> TranscriptAlignmentMap:
        assert self.source_provenance_service is not None
        artifact: IngestedRecordingArtifact = self.source_provenance_service.ingest_recording_artifact(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            artifact_type=RecordingArtifactType.master_audio,
            source_label="master source",
            filename=filename,
            content=content,
            upload_route="operator_upload",
            retention_policy_id=retention_policy_id,
            actor_id=actor_id,
        )
        revision: TranscriptRevision = self.source_provenance_service.generate_transcript_revision(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            source_artifact_ids=[artifact.recording_artifact_id],
            segments=segments,
            transcript_source=TranscriptSource.operator_upload,
            actor_id=actor_id,
        )
        return self.source_provenance_service.align_transcript_to_source(
            organization_id=organization_id,
            brand_id=brand_id,
            transcript_revision_id=revision.transcript_revision_id,
            actor_id=actor_id,
        )

    def stage6_extract_candidates(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        skill_key: str | None = None,
    ) -> ExtractionReceipt:
        if self.extraction_service is None:
            raise RuntimeError("ExtractionService must be configured for candidate extraction.")
        return self.extraction_service.run_extraction(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            skill_key=skill_key,
            actor_id=actor_id,
        )

    def stage6_review_expression_moments(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_ids: list[UUID],
        actor_id: UUID,
        rationale: str,
    ) -> list[ExpressionReviewReceipt]:
        if self.expression_review_service is None:
            raise RuntimeError("ExpressionReviewService must be configured for moment review.")
        return [
            self.expression_review_service.approve_expression_moment(
                organization_id=organization_id,
                brand_id=brand_id,
                candidate_id=candidate_id,
                reviewer_actor_id=actor_id,
                rationale=rationale,
            )
            for candidate_id in candidate_ids
        ]

    def stage7_route_expression_moments(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_ids: list[UUID],
        actor_id: UUID,
        requested_format: str | None = None,
    ) -> list[AssetRouteReceipt]:
        if self.routing_service is None:
            raise RuntimeError("RoutingService must be configured for archetype routing.")
        return [
            self.routing_service.route_expression_moment(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_moment_id=expression_moment_id,
                requested_format=requested_format,
                actor_id=actor_id,
            )
            for expression_moment_id in expression_moment_ids
        ]

    def stage8_generate_asset_package_spec(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        asset_route_receipt_ids: list[UUID],
        actor_id: UUID,
    ) -> AssetPackageSpec:
        if self.asset_package_service is None:
            raise RuntimeError("AssetPackageService must be configured for package planning.")
        return self.asset_package_service.generate_trial_guest_asset_pack_spec(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            asset_route_receipt_ids=asset_route_receipt_ids,
            actor_id=actor_id,
        )

    def stage6_7_record_rejections(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        actor_id: UUID,
        category: RejectionCategory,
        reason: str,
        route_attempt_receipt_id: UUID | None = None,
    ) -> RejectionReceipt:
        if self.rejection_memory_service is None:
            raise RuntimeError("RejectionMemoryService must be configured for rejection memory.")
        return self.rejection_memory_service.record_rejected_expression_candidate(
            organization_id=organization_id,
            brand_id=brand_id,
            candidate_id=candidate_id,
            category=category,
            reason=reason,
            reviewer_id=actor_id,
            route_attempt_receipt_id=route_attempt_receipt_id,
        )
