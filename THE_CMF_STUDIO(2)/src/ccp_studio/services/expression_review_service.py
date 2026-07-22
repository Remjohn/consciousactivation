"""Expression Moment review and boundary-control service for TS-CMF-032."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.extraction import CandidateStatus, ExpressionMomentCandidate
from ccp_studio.contracts.expression_review import (
    ExpressionMoment,
    ExpressionMomentBoundary,
    ExpressionMomentReviewDecision,
    ExpressionMomentReviewSurfaceItem,
    ExpressionMomentStatus,
    ExpressionReviewReceipt,
    ReviewDecisionType,
    ReviewRejectionCode,
    SensitivityHold,
    SourceBoundaryRange,
    boundary_from_candidate,
    new_expression_moment,
    new_expression_review_receipt,
    new_review_decision,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.expression_review import InMemoryExpressionReviewRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.extraction_service import ExtractionService


class ExpressionReviewServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ExpressionReviewService:
    extraction_service: ExtractionService
    repository: InMemoryExpressionReviewRepository = field(default_factory=InMemoryExpressionReviewRepository)

    def review_surface_for_candidate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
    ) -> ExpressionMomentReviewSurfaceItem:
        candidate = self._candidate_for_review(organization_id, brand_id, candidate_id)
        artifact = self.extraction_service.source_provenance_service.repository.recording_artifacts[candidate.source_artifact_id]
        transcript = self.extraction_service.source_provenance_service.repository.transcript_revisions[
            candidate.transcript_revision_id
        ]
        segment_text = " ".join(
            segment.text
            for segment in transcript.segments
            if segment.segment_id in candidate.transcript_segment_ids
        )
        source_playback_ref = (
            f"{artifact.object_uri}#t={candidate.timestamp_start_ms / 1000:.3f},"
            f"{candidate.timestamp_end_ms / 1000:.3f}"
        )
        return ExpressionMomentReviewSurfaceItem(
            schema_version="cmf.expression_moment_review_surface_item.v1",
            candidate_id=candidate.candidate_id,
            expression_session_id=candidate.expression_session_id,
            brand_id=brand_id,
            source_playback_ref=source_playback_ref,
            transcript_revision_id=candidate.transcript_revision_id,
            transcript_segment_ids=candidate.transcript_segment_ids,
            transcript_excerpt=segment_text or candidate.source_quote,
            timestamp_start_ms=candidate.timestamp_start_ms,
            timestamp_end_ms=candidate.timestamp_end_ms,
            induction_context_ids=candidate.induction_context_ids,
            route_rationale=candidate.route_rationale,
            sensitivity_flags=self._sensitivity_flags(candidate),
            source_truth_score=candidate.source_truth_score,
        )

    def approve_expression_moment(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        reviewer_actor_id: UUID,
        rationale: str,
        boundary: ExpressionMomentBoundary | None = None,
        annotations: list[str] | None = None,
    ) -> ExpressionReviewReceipt:
        candidate = self._candidate_for_review(organization_id, brand_id, candidate_id)
        if candidate.status == CandidateStatus.rejected_unsupported:
            raise ExpressionReviewServiceError("CANDIDATE_REJECTED", "Rejected candidates cannot be approved.")
        if candidate.source_truth_score < 0.85:
            raise ExpressionReviewServiceError("SOURCE_TRUTH_INSUFFICIENT", "Candidate source truth is too weak.")
        moment = new_expression_moment(
            source_candidate_ids=[candidate.candidate_id],
            expression_session_id=candidate.expression_session_id,
            brand_id=brand_id,
            boundary=boundary or self._boundary_from_candidate(candidate),
            source_quote=candidate.source_quote,
            induction_context_ids=candidate.induction_context_ids,
            route_rationale=candidate.route_rationale,
            annotations=annotations,
            status=ExpressionMomentStatus.approved,
        )
        self.repository.put_moment(moment)
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.approve,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=candidate.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=self._candidate_evidence_refs(candidate),
            source_candidate_ids=[candidate.candidate_id],
            new_expression_moment_ids=[moment.expression_moment_id],
            source_ranges=moment.boundary.normalized_ranges(),
            decision_code="EXPRESSION_MOMENT_APPROVED",
        )

    def reject_expression_moment_candidate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        reviewer_actor_id: UUID,
        rationale: str,
        rejection_code: ReviewRejectionCode,
    ) -> ExpressionReviewReceipt:
        candidate = self._candidate_for_review(organization_id, brand_id, candidate_id, allow_rejected=True)
        rejected = candidate.model_copy(update={"status": CandidateStatus.rejected_unsupported})
        self.extraction_service.repository.put_candidate(rejected)
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.reject,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=candidate.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=self._candidate_evidence_refs(candidate),
            source_candidate_ids=[candidate.candidate_id],
            rejection_code=rejection_code,
            decision_code="EXPRESSION_MOMENT_REJECTED",
        )

    def adjust_expression_moment_boundary(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        reviewer_actor_id: UUID,
        boundary: ExpressionMomentBoundary,
        rationale: str,
    ) -> ExpressionReviewReceipt:
        candidate = self._candidate_for_review(organization_id, brand_id, candidate_id)
        adjusted = new_expression_moment(
            source_candidate_ids=[candidate.candidate_id],
            expression_session_id=candidate.expression_session_id,
            brand_id=brand_id,
            boundary=boundary,
            source_quote=candidate.source_quote,
            induction_context_ids=candidate.induction_context_ids,
            route_rationale=candidate.route_rationale,
            status=ExpressionMomentStatus.candidate,
        )
        self.repository.put_moment(adjusted)
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.adjust_boundary,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=candidate.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=self._candidate_evidence_refs(candidate),
            source_candidate_ids=[candidate.candidate_id],
            new_expression_moment_ids=[adjusted.expression_moment_id],
            source_ranges=boundary.normalized_ranges(),
            decision_code="EXPRESSION_MOMENT_BOUNDARY_ADJUSTED",
        )

    def split_expression_moment_candidate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        reviewer_actor_id: UUID,
        boundaries: list[ExpressionMomentBoundary],
        quotes: list[str],
        rationale: str,
    ) -> ExpressionReviewReceipt:
        candidate = self._candidate_for_review(organization_id, brand_id, candidate_id)
        if len(boundaries) < 2 or len(boundaries) != len(quotes):
            raise ExpressionReviewServiceError("SPLIT_PARTS_REQUIRED", "Split requires matching boundaries and quotes.")
        moments: list[ExpressionMoment] = []
        for boundary, quote in zip(boundaries, quotes):
            moment = new_expression_moment(
                source_candidate_ids=[candidate.candidate_id],
                expression_session_id=candidate.expression_session_id,
                brand_id=brand_id,
                boundary=boundary,
                source_quote=quote,
                induction_context_ids=candidate.induction_context_ids,
                route_rationale=candidate.route_rationale,
                status=ExpressionMomentStatus.candidate,
            )
            moments.append(self.repository.put_moment(moment))
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.split,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=candidate.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=self._candidate_evidence_refs(candidate),
            source_candidate_ids=[candidate.candidate_id],
            new_expression_moment_ids=[moment.expression_moment_id for moment in moments],
            source_ranges=[item for moment in moments for item in moment.boundary.normalized_ranges()],
            decision_code="EXPRESSION_MOMENT_SPLIT",
        )

    def merge_expression_moment_candidates(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_ids: list[UUID],
        reviewer_actor_id: UUID,
        rationale: str,
        approve: bool = True,
    ) -> ExpressionReviewReceipt:
        if len(candidate_ids) < 2:
            raise ExpressionReviewServiceError("MERGE_CANDIDATES_REQUIRED", "Merge requires at least two candidates.")
        candidates = [self._candidate_for_review(organization_id, brand_id, item) for item in candidate_ids]
        expression_session_id = candidates[0].expression_session_id
        if any(candidate.expression_session_id != expression_session_id for candidate in candidates):
            raise ExpressionReviewServiceError("SESSION_MISMATCH", "Merged candidates must come from one session.")
        ranges = [self._boundary_from_candidate(candidate).normalized_ranges()[0] for candidate in candidates]
        start_ms = min(item.start_ms for item in ranges)
        end_ms = max(item.end_ms for item in ranges)
        boundary = boundary_from_candidate(
            source_artifact_id=ranges[0].source_artifact_id,
            transcript_revision_id=ranges[0].transcript_revision_id,
            start_ms=start_ms,
            end_ms=end_ms,
            transcript_segment_ids=[segment for item in ranges for segment in item.transcript_segment_ids],
            source_ranges=ranges,
        )
        moment = new_expression_moment(
            source_candidate_ids=candidate_ids,
            expression_session_id=expression_session_id,
            brand_id=brand_id,
            boundary=boundary,
            source_quote=" ".join(candidate.source_quote for candidate in candidates),
            induction_context_ids=list({item for candidate in candidates for item in candidate.induction_context_ids}),
            route_rationale="Merged review boundary: " + " | ".join(candidate.route_rationale for candidate in candidates),
            status=ExpressionMomentStatus.approved if approve else ExpressionMomentStatus.candidate,
        )
        self.repository.put_moment(moment)
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.merge,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=[ref for candidate in candidates for ref in self._candidate_evidence_refs(candidate)],
            source_candidate_ids=candidate_ids,
            new_expression_moment_ids=[moment.expression_moment_id],
            source_ranges=boundary.normalized_ranges(),
            decision_code="EXPRESSION_MOMENTS_MERGED",
        )

    def annotate_expression_moment(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        reviewer_actor_id: UUID,
        annotation: str,
        rationale: str,
    ) -> ExpressionReviewReceipt:
        moment = self._moment_for_brand(brand_id, expression_moment_id)
        if moment.status == ExpressionMomentStatus.approved:
            replacement = moment.model_copy(
                update={
                    "expression_moment_id": uuid4(),
                    "annotations": [*moment.annotations, annotation],
                    "supersedes_expression_moment_ids": [moment.expression_moment_id],
                    "created_at": utc_now(),
                }
            )
            self.repository.put_moment(replacement)
            self._mark_superseded(moment, replacement.expression_moment_id)
            new_ids = [replacement.expression_moment_id]
            prior_ids = [moment.expression_moment_id]
        else:
            updated = moment.model_copy(update={"annotations": [*moment.annotations, annotation]})
            self.repository.put_moment(updated)
            new_ids = [updated.expression_moment_id]
            prior_ids = []
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.annotate,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=moment.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=[f"expression_moment:{moment.expression_moment_id}", f"annotation:{annotation}"],
            prior_expression_moment_ids=prior_ids,
            new_expression_moment_ids=new_ids,
            source_ranges=moment.boundary.normalized_ranges(),
            decision_code="EXPRESSION_MOMENT_ANNOTATED",
        )

    def place_sensitivity_hold(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        reviewer_actor_id: UUID,
        reason: str,
        consent_record_version_id: UUID | None = None,
    ) -> ExpressionReviewReceipt:
        moment = self._moment_for_brand(brand_id, expression_moment_id)
        hold = self.repository.put_hold(
            SensitivityHold(
                schema_version="cmf.sensitivity_hold.v1",
                sensitivity_hold_id=uuid4(),
                expression_moment_id=expression_moment_id,
                reason=reason,
                consent_record_version_id=consent_record_version_id,
                placed_by_user_id=reviewer_actor_id,
                placed_at=utc_now(),
            )
        )
        if moment.status != ExpressionMomentStatus.approved:
            self.repository.put_moment(
                moment.model_copy(
                    update={
                        "status": ExpressionMomentStatus.sensitivity_hold,
                        "sensitivity_hold_id": hold.sensitivity_hold_id,
                    }
                )
            )
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.place_hold,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=moment.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=reason,
            evidence_refs=[f"expression_moment:{expression_moment_id}", f"sensitivity_hold:{hold.sensitivity_hold_id}"],
            prior_expression_moment_ids=[expression_moment_id],
            source_ranges=moment.boundary.normalized_ranges(),
            sensitivity_hold_id=hold.sensitivity_hold_id,
            decision_code="EXPRESSION_MOMENT_SENSITIVITY_HELD",
        )

    def release_sensitivity_hold(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        reviewer_actor_id: UUID,
        rationale: str,
    ) -> ExpressionReviewReceipt:
        moment = self._moment_for_brand(brand_id, expression_moment_id)
        hold = self.repository.active_hold_for_moment(expression_moment_id)
        if hold is None:
            raise ExpressionReviewServiceError("ACTIVE_HOLD_REQUIRED", "An active hold is required.")
        released = hold.model_copy(update={"released_by_user_id": reviewer_actor_id, "released_at": utc_now()})
        self.repository.put_hold(released)
        if moment.status == ExpressionMomentStatus.sensitivity_hold:
            self.repository.put_moment(
                moment.model_copy(update={"status": ExpressionMomentStatus.candidate, "sensitivity_hold_id": None})
            )
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.release_hold,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=moment.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=[f"expression_moment:{expression_moment_id}", f"sensitivity_hold:{hold.sensitivity_hold_id}"],
            prior_expression_moment_ids=[expression_moment_id],
            source_ranges=moment.boundary.normalized_ranges(),
            sensitivity_hold_id=hold.sensitivity_hold_id,
            decision_code="EXPRESSION_MOMENT_SENSITIVITY_RELEASED",
        )

    def supersede_expression_moment(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_moment_id: UUID,
        reviewer_actor_id: UUID,
        boundary: ExpressionMomentBoundary,
        source_quote: str,
        rationale: str,
    ) -> ExpressionReviewReceipt:
        prior = self._moment_for_brand(brand_id, expression_moment_id)
        replacement = new_expression_moment(
            source_candidate_ids=prior.source_candidate_ids,
            expression_session_id=prior.expression_session_id,
            brand_id=brand_id,
            boundary=boundary,
            source_quote=source_quote,
            induction_context_ids=prior.induction_context_ids,
            route_rationale=prior.route_rationale,
            annotations=prior.annotations,
            status=ExpressionMomentStatus.approved,
            supersedes_expression_moment_ids=[prior.expression_moment_id],
        )
        self.repository.put_moment(replacement)
        self._mark_superseded(prior, replacement.expression_moment_id)
        return self._record_decision_and_receipt(
            decision_type=ReviewDecisionType.supersede,
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=prior.expression_session_id,
            reviewer_actor_id=reviewer_actor_id,
            rationale=rationale,
            evidence_refs=[f"expression_moment:{prior.expression_moment_id}", f"expression_moment:{replacement.expression_moment_id}"],
            prior_expression_moment_ids=[prior.expression_moment_id],
            new_expression_moment_ids=[replacement.expression_moment_id],
            source_ranges=replacement.boundary.normalized_ranges(),
            decision_code="EXPRESSION_MOMENT_SUPERSEDED",
        )

    def can_route_expression_moment(self, expression_moment_id: UUID) -> bool:
        moment = self.repository.moments.get(expression_moment_id)
        if moment is None:
            return False
        if moment.status != ExpressionMomentStatus.approved:
            return False
        return self.repository.active_hold_for_moment(expression_moment_id) is None

    def assert_can_route_expression_moment(self, expression_moment_id: UUID) -> ExpressionMoment:
        moment = self.repository.moments.get(expression_moment_id)
        if moment is None:
            raise ExpressionReviewServiceError("EXPRESSION_MOMENT_REQUIRED", "Expression Moment is required.")
        if moment.status != ExpressionMomentStatus.approved:
            raise ExpressionReviewServiceError("EXPRESSION_MOMENT_NOT_APPROVED", "Only approved Expression Moments can route.")
        if self.repository.active_hold_for_moment(expression_moment_id) is not None:
            raise ExpressionReviewServiceError("SENSITIVITY_HOLD_BLOCKS_ROUTING", "Sensitivity hold blocks routing.")
        return moment

    def _record_decision_and_receipt(
        self,
        *,
        decision_type: ReviewDecisionType,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        reviewer_actor_id: UUID,
        rationale: str,
        evidence_refs: list[str],
        decision_code: str,
        source_candidate_ids: list[UUID] | None = None,
        prior_expression_moment_ids: list[UUID] | None = None,
        new_expression_moment_ids: list[UUID] | None = None,
        source_ranges: list[SourceBoundaryRange] | None = None,
        sensitivity_hold_id: UUID | None = None,
        rejection_code: ReviewRejectionCode | None = None,
    ) -> ExpressionReviewReceipt:
        decision: ExpressionMomentReviewDecision = self.repository.put_decision(
            new_review_decision(
                decision_type=decision_type,
                organization_id=organization_id,
                brand_id=brand_id,
                reviewer_actor_id=reviewer_actor_id,
                expression_session_id=expression_session_id,
                rationale=rationale,
                evidence_refs=evidence_refs,
                source_candidate_ids=source_candidate_ids,
                prior_expression_moment_ids=prior_expression_moment_ids,
                new_expression_moment_ids=new_expression_moment_ids,
                sensitivity_hold_id=sensitivity_hold_id,
                rejection_code=rejection_code,
            )
        )
        return self.repository.put_receipt(
            new_expression_review_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                reviewer_actor_id=reviewer_actor_id,
                decision_type=decision_type,
                review_decision_id=decision.review_decision_id,
                source_candidate_ids=source_candidate_ids,
                prior_expression_moment_ids=prior_expression_moment_ids,
                new_expression_moment_ids=new_expression_moment_ids,
                source_ranges=source_ranges,
                sensitivity_hold_id=sensitivity_hold_id,
                rejection_code=rejection_code,
                decision_code=decision_code,
                evidence_refs=evidence_refs,
            )
        )

    def _candidate_for_review(
        self,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        *,
        allow_rejected: bool = False,
    ) -> ExpressionMomentCandidate:
        candidate = self.extraction_service.repository.candidates.get(candidate_id)
        if candidate is None:
            raise ExpressionReviewServiceError("EXPRESSION_MOMENT_CANDIDATE_REQUIRED", "Candidate is required.")
        artifact = self.extraction_service.source_provenance_service.repository.recording_artifacts[candidate.source_artifact_id]
        if artifact.organization_id != organization_id or artifact.brand_id != brand_id:
            raise ExpressionReviewServiceError("BRAND_SCOPE_VIOLATION", "Candidate is outside active brand scope.")
        if not allow_rejected and candidate.status == CandidateStatus.rejected_unsupported:
            raise ExpressionReviewServiceError("CANDIDATE_REJECTED", "Rejected candidates cannot be reviewed for approval.")
        return candidate

    def _moment_for_brand(self, brand_id: UUID, expression_moment_id: UUID) -> ExpressionMoment:
        moment = self.repository.moments.get(expression_moment_id)
        if moment is None:
            raise ExpressionReviewServiceError("EXPRESSION_MOMENT_REQUIRED", "Expression Moment is required.")
        if moment.brand_id != brand_id:
            raise ExpressionReviewServiceError("BRAND_SCOPE_VIOLATION", "Expression Moment is outside active brand scope.")
        return moment

    @staticmethod
    def _boundary_from_candidate(candidate: ExpressionMomentCandidate) -> ExpressionMomentBoundary:
        return boundary_from_candidate(
            source_artifact_id=candidate.source_artifact_id,
            transcript_revision_id=candidate.transcript_revision_id,
            start_ms=candidate.timestamp_start_ms,
            end_ms=candidate.timestamp_end_ms,
            transcript_segment_ids=candidate.transcript_segment_ids,
        )

    @staticmethod
    def _candidate_evidence_refs(candidate: ExpressionMomentCandidate) -> list[str]:
        return [
            f"candidate:{candidate.candidate_id}",
            f"source_artifact:{candidate.source_artifact_id}",
            f"transcript_revision:{candidate.transcript_revision_id}",
            *[f"transcript_segment:{item}" for item in candidate.transcript_segment_ids],
            *[f"anchor_hit:{item}" for item in candidate.anchor_hit_ids],
        ]

    @staticmethod
    def _sensitivity_flags(candidate: ExpressionMomentCandidate) -> list[str]:
        flags: list[str] = []
        lower_quote = candidate.source_quote.lower()
        if candidate.source_truth_score < 0.9:
            flags.append("source_truth_review")
        if any(token in lower_quote for token in ["pressure", "exposure", "private", "trauma", "risk"]):
            flags.append("dignity_or_sensitivity_review")
        if not candidate.induction_context_ids:
            flags.append("missing_induction_context")
        return flags

    def _mark_superseded(self, prior: ExpressionMoment, replacement_id: UUID) -> ExpressionMoment:
        superseded = prior.model_copy(
            update={
                "status": ExpressionMomentStatus.superseded,
                "superseded_by_expression_moment_id": replacement_id,
            }
        )
        return self.repository.put_moment(superseded)


@dataclass
class ExpressionReviewCommandHandler:
    command_type: str
    service: ExpressionReviewService
    aggregate_type: str = "expression_moment"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ApproveExpressionMomentCommand":
            return self.service.approve_expression_moment(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                rationale=payload["rationale"],
            ).model_dump(mode="json")
        if self.command_type == "RejectExpressionMomentCommand":
            return self.service.reject_expression_moment_candidate(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                rationale=payload["rationale"],
                rejection_code=ReviewRejectionCode(payload["rejection_code"]),
            ).model_dump(mode="json")
        if self.command_type == "AdjustExpressionMomentBoundaryCommand":
            return self.service.adjust_expression_moment_boundary(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                boundary=ExpressionMomentBoundary.model_validate(payload["boundary"]),
                rationale=payload["rationale"],
            ).model_dump(mode="json")
        if self.command_type == "SplitExpressionMomentCommand":
            return self.service.split_expression_moment_candidate(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                boundaries=[ExpressionMomentBoundary.model_validate(item) for item in payload["boundaries"]],
                quotes=payload["quotes"],
                rationale=payload["rationale"],
            ).model_dump(mode="json")
        if self.command_type == "MergeExpressionMomentsCommand":
            return self.service.merge_expression_moment_candidates(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_ids=[UUID(item) for item in payload["candidate_ids"]],
                reviewer_actor_id=envelope.actor.actor_id,
                rationale=payload["rationale"],
                approve=payload.get("approve", True),
            ).model_dump(mode="json")
        if self.command_type == "PlaceSensitivityHoldCommand":
            return self.service.place_sensitivity_hold(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
                consent_record_version_id=UUID(payload["consent_record_version_id"]) if payload.get("consent_record_version_id") else None,
            ).model_dump(mode="json")
        if self.command_type == "ReleaseSensitivityHoldCommand":
            return self.service.release_sensitivity_hold(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                rationale=payload["rationale"],
            ).model_dump(mode="json")
        if self.command_type == "SupersedeExpressionMomentCommand":
            return self.service.supersede_expression_moment(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_moment_id=UUID(payload["expression_moment_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                boundary=ExpressionMomentBoundary.model_validate(payload["boundary"]),
                source_quote=payload["source_quote"],
                rationale=payload["rationale"],
            ).model_dump(mode="json")
        raise ExpressionReviewServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("expression_moment_id") or payload.get("candidate_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_expression_review_command_handlers(bus: CommandBus, service: ExpressionReviewService) -> None:
    for command_type in [
        "ApproveExpressionMomentCommand",
        "RejectExpressionMomentCommand",
        "AdjustExpressionMomentBoundaryCommand",
        "SplitExpressionMomentCommand",
        "MergeExpressionMomentsCommand",
        "PlaceSensitivityHoldCommand",
        "ReleaseSensitivityHoldCommand",
        "SupersedeExpressionMomentCommand",
    ]:
        bus.register_handler(ExpressionReviewCommandHandler(command_type=command_type, service=service))
