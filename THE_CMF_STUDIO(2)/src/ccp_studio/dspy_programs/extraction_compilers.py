"""DSPy-style extraction compilers for TS-CMF-031."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ccp_studio.contracts.extraction import (
    AnchorType,
    CandidateStatus,
    ExpressionMomentCandidate,
    SourceCue,
    TimestampedAnchorHit,
)
from ccp_studio.contracts.interview_contracts import InterviewAssetContract
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.source_provenance import IngestedRecordingArtifact, TranscriptRevision, VoiceRole


@dataclass(frozen=True)
class AnchorHitDetector:
    compiler_version: str = "anchor-hit-detector-v1"

    def detect(
        self,
        *,
        expression_session_id,
        transcript: TranscriptRevision,
        contracts: list[InterviewAssetContract],
        source_artifacts: dict,
    ) -> list[TimestampedAnchorHit]:
        hits: list[TimestampedAnchorHit] = []
        guest_segments = [segment for segment in transcript.segments if segment.speaker_role == VoiceRole.guest]
        if not guest_segments:
            return hits
        for contract in contracts:
            segment = guest_segments[0]
            source_artifact_id = segment.source_artifact_id or transcript.source_artifact_ids[0]
            quote = segment.text
            anchor_type = AnchorType.first_line
            confidence = min(segment.confidence, 0.92)
            if any(term in quote.lower() for term in ["cost", "pressure", "exposure", "problem"]):
                anchor_type = AnchorType.depth_anchor
            hits.append(
                TimestampedAnchorHit(
                    schema_version="cmf.timestamped_anchor_hit.v1",
                    anchor_hit_id=uuid4(),
                    expression_session_id=expression_session_id,
                    interview_asset_contract_id=contract.contract_id,
                    anchor_type=anchor_type,
                    transcript_segment_ids=[segment.segment_id],
                    source_artifact_id=source_artifact_id,
                    start_ms=segment.start_ms,
                    end_ms=segment.end_ms,
                    confidence=confidence,
                    evidence_text=quote,
                )
            )
        return hits


@dataclass(frozen=True)
class ExpressionMomentCandidateCompiler:
    compiler_version: str = "expression-moment-candidate-compiler-v1"

    def compile(
        self,
        *,
        expression_session_id,
        transcript: TranscriptRevision,
        anchor_hits: list[TimestampedAnchorHit],
        contracts: list[InterviewAssetContract],
        source_artifacts: dict,
        skill_contribution_ids: list,
    ) -> tuple[list[SourceCue], list[ExpressionMomentCandidate]]:
        cues: list[SourceCue] = []
        candidates: list[ExpressionMomentCandidate] = []
        contract_by_id = {contract.contract_id: contract for contract in contracts}
        segment_by_id = {segment.segment_id: segment for segment in transcript.segments}
        for hit in anchor_hits:
            segment = segment_by_id[hit.transcript_segment_ids[0]]
            cue = SourceCue(
                schema_version="cmf.source_cue.v1",
                source_cue_id=uuid4(),
                expression_session_id=expression_session_id,
                transcript_revision_id=transcript.transcript_revision_id,
                source_artifact_id=hit.source_artifact_id,
                transcript_segment_ids=hit.transcript_segment_ids,
                cue_type="emotional_shift",
                description=f"Shift evidenced by transcript text: {segment.text}",
                start_ms=segment.start_ms,
                end_ms=segment.end_ms,
                confidence=segment.confidence,
            )
            cues.append(cue)
            contract = contract_by_id.get(hit.interview_asset_contract_id)
            induction_ids = contract.induction_rationale_ids if contract else []
            confidence = min(hit.confidence, segment.confidence)
            status = CandidateStatus.ready_for_review if induction_ids and segment.text else CandidateStatus.needs_review
            source_truth_score = 1.0 if segment.text == hit.evidence_text else 0.6
            if source_truth_score < 0.85:
                status = CandidateStatus.rejected_unsupported
            candidates.append(
                ExpressionMomentCandidate(
                    schema_version="cmf.expression_moment_candidate.v1",
                    candidate_id=uuid4(),
                    expression_session_id=expression_session_id,
                    transcript_revision_id=transcript.transcript_revision_id,
                    source_artifact_id=hit.source_artifact_id,
                    timestamp_start_ms=segment.start_ms,
                    timestamp_end_ms=segment.end_ms,
                    transcript_segment_ids=[segment.segment_id],
                    source_quote=segment.text,
                    induction_context_ids=induction_ids,
                    interview_asset_contract_id=hit.interview_asset_contract_id,
                    anchor_hit_ids=[hit.anchor_hit_id],
                    emotional_shift_evidence=[cue.description],
                    primitive_candidate_ids=[],
                    route_rationale="Candidate follows the Interview Asset Contract, source timestamp, and induction context; reviewer must approve before routing.",
                    skill_contribution_ids=skill_contribution_ids,
                    source_truth_score=source_truth_score,
                    confidence=confidence,
                    status=status,
                    created_at=utc_now(),
                )
            )
        return cues, candidates
