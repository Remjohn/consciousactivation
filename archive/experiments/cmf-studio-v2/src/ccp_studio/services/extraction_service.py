"""Anchor hit and Expression Moment candidate extraction service for TS-CMF-031."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.extraction import (
    CandidateStatus,
    ExpressionMomentCandidate,
    ExtractionRunStatus,
    SkillExtractionContribution,
    new_extraction_receipt,
    new_extraction_run,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.skills import SaturationContextBundle, SkillUseMode
from ccp_studio.dspy_programs.extraction_compilers import AnchorHitDetector, ExpressionMomentCandidateCompiler
from ccp_studio.repositories.extraction import InMemoryExtractionRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.jit_skill_compiler_service import JITSkillCompilerService
from ccp_studio.services.source_provenance_service import SourceProvenanceService


class ExtractionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ExtractionService:
    source_provenance_service: SourceProvenanceService
    interview_contract_service: InterviewContractService
    jit_skill_service: JITSkillCompilerService | None = None
    repository: InMemoryExtractionRepository = field(default_factory=InMemoryExtractionRepository)
    anchor_detector: AnchorHitDetector = field(default_factory=AnchorHitDetector)
    candidate_compiler: ExpressionMomentCandidateCompiler = field(default_factory=ExpressionMomentCandidateCompiler)

    def detect_anchor_hits(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
    ):
        transcript = self.source_provenance_service.selected_transcript_for_extraction(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
        )
        contracts = self._contracts_for_session(expression_session_id)
        artifacts = self._source_artifacts(transcript.source_artifact_ids)
        hits = self.anchor_detector.detect(
            expression_session_id=expression_session_id,
            transcript=transcript,
            contracts=contracts,
            source_artifacts=artifacts,
        )
        for hit in hits:
            self.repository.put_anchor_hit(hit)
        return hits

    def invoke_jit_extraction_skill(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        skill_key: str,
        actor_id: UUID,
    ) -> SkillExtractionContribution:
        if self.jit_skill_service is None:
            raise ExtractionServiceError("JIT_SKILL_SERVICE_REQUIRED", "JIT skill service is required.")
        transcript = self.source_provenance_service.selected_transcript_for_extraction(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
        )
        artifacts = self._source_artifacts(transcript.source_artifact_ids)
        source_refs = [f"source:{artifact.recording_artifact_id}:{artifact.content_hash}" for artifact in artifacts.values()]
        segment_refs = [f"transcript:{segment.segment_id}" for segment in transcript.segments]
        context = SaturationContextBundle(
            schema_version="cmf.saturation_context_bundle.v1",
            source_doc_refs=source_refs,
            transcript_segment_refs=segment_refs,
            primitive_candidate_ids=[],
            prior_evaluation_receipt_ids=[receipt.ingestion_receipt_id for receipt in self.source_provenance_service.repository.receipts.values()],
            failure_corpus_refs=["failure:generic-clip", "failure:unsupported-emotional-label"],
        )
        guest_text = next((segment.text for segment in transcript.segments if segment.speaker_role.value == "guest"), transcript.segments[0].text)
        receipt = self.jit_skill_service.invoke(
            skill_key=skill_key,
            use_mode=SkillUseMode.transcript_extraction,
            saturation_context=context,
            candidate_texts=[guest_text],
            contrast_texts=["A weaker extraction would summarize the topic without the timestamped source pressure."],
            evidence_refs=[*source_refs, *segment_refs],
            confidence=0.91,
            eval_score=0.9,
            reviewer_state="candidate_review_required",
        )
        candidate_set = next(reversed(self.jit_skill_service.repository.candidate_sets.values()))
        calibration = next(reversed(self.jit_skill_service.repository.calibration_reports.values()))
        contribution = SkillExtractionContribution(
            schema_version="cmf.skill_extraction_contribution.v1",
            skill_invocation_receipt_id=receipt.skill_invocation_receipt_id,
            skill_key=skill_key,
            saturation_context_hash=context.stable_hash(),
            contrast_output=[item.text for item in candidate_set.contrast_candidates],
            anti_draft_passed=calibration.passed,
        )
        return self.repository.put_skill_contribution(contribution)

    def run_extraction(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        skill_key: str | None = None,
        retry_of_run_id: UUID | None = None,
    ):
        transcript = self.source_provenance_service.selected_transcript_for_extraction(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
        )
        run = self.repository.put_extraction_run(
            new_extraction_run(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                transcript_revision_id=transcript.transcript_revision_id,
                retry_of_run_id=retry_of_run_id,
            )
        )
        skill_contribution_ids: list[UUID] = []
        if skill_key:
            contribution = self.invoke_jit_extraction_skill(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                skill_key=skill_key,
                actor_id=actor_id,
            )
            skill_contribution_ids.append(contribution.skill_invocation_receipt_id)
        hits = self.detect_anchor_hits(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
        )
        contracts = self._contracts_for_session(expression_session_id)
        artifacts = self._source_artifacts(transcript.source_artifact_ids)
        cues, candidates = self.candidate_compiler.compile(
            expression_session_id=expression_session_id,
            transcript=transcript,
            anchor_hits=hits,
            contracts=contracts,
            source_artifacts=artifacts,
            skill_contribution_ids=skill_contribution_ids,
        )
        for cue in cues:
            self.repository.put_source_cue(cue)
        for candidate in candidates:
            self.repository.put_candidate(candidate)
        completed = run.model_copy(update={"status": ExtractionRunStatus.completed, "completed_at": utc_now()})
        self.repository.put_extraction_run(completed)
        evaluator_results = self._evaluate_candidates(candidates)
        receipt = new_extraction_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            extraction_run_id=run.extraction_run_id,
            selected_transcript_revision_id=transcript.transcript_revision_id,
            source_artifact_hashes={artifact.recording_artifact_id: artifact.content_hash for artifact in artifacts.values()},
            anchor_hit_ids=[hit.anchor_hit_id for hit in hits],
            candidate_ids=[candidate.candidate_id for candidate in candidates],
            skill_invocation_receipt_ids=skill_contribution_ids,
            evaluator_results=evaluator_results,
            decision_code="EXPRESSION_MOMENT_CANDIDATES_CREATED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def reject_unsupported_candidate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        actor_id: UUID,
        reason: str,
    ) -> ExpressionMomentCandidate:
        candidate = self._candidate_for_brand(organization_id, brand_id, candidate_id)
        rejected = candidate.model_copy(update={"status": CandidateStatus.rejected_unsupported})
        self.repository.put_candidate(rejected)
        return rejected

    def queue_candidate_for_review(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        actor_id: UUID,
    ) -> ExpressionMomentCandidate:
        candidate = self._candidate_for_brand(organization_id, brand_id, candidate_id)
        queued = candidate.model_copy(update={"status": CandidateStatus.ready_for_review})
        self.repository.put_candidate(queued)
        return queued

    def _contracts_for_session(self, expression_session_id: UUID):
        deck = next(
            (
                item
                for item in self.interview_contract_service.repository.decks.values()
                if item.status.value == "bound_to_session"
                and any(
                    binding.expression_session_id == expression_session_id
                    for binding in self.interview_contract_service.repository.bindings.values()
                    if binding.interview_deck_id == item.interview_deck_id
                )
            ),
            None,
        )
        if deck is None:
            raise ExtractionServiceError("BOUND_INTERVIEW_DECK_REQUIRED", "Extraction requires a deck bound to the session.")
        return [self.interview_contract_service.repository.contracts[item] for item in deck.contract_ids]

    def _source_artifacts(self, artifact_ids: list[UUID]):
        artifacts = {
            item: self.source_provenance_service.repository.recording_artifacts[item]
            for item in artifact_ids
        }
        if any(item.corrupted for item in artifacts.values()):
            raise ExtractionServiceError("SOURCE_ARTIFACT_CORRUPTED", "Corrupted source cannot feed extraction.")
        return artifacts

    def _candidate_for_brand(self, organization_id: UUID, brand_id: UUID, candidate_id: UUID):
        candidate = self.repository.candidates.get(candidate_id)
        if candidate is None:
            raise ExtractionServiceError("EXPRESSION_MOMENT_CANDIDATE_REQUIRED", "Candidate is required.")
        artifact = self.source_provenance_service.repository.recording_artifacts[candidate.source_artifact_id]
        if artifact.organization_id != organization_id or artifact.brand_id != brand_id:
            raise ExtractionServiceError("BRAND_SCOPE_VIOLATION", "Candidate is outside active brand scope.")
        return candidate

    @staticmethod
    def _evaluate_candidates(candidates: list[ExpressionMomentCandidate]) -> list[str]:
        results: list[str] = []
        for candidate in candidates:
            if candidate.status == CandidateStatus.rejected_unsupported:
                results.append(f"candidate rejected unsupported:{candidate.candidate_id}")
            elif not candidate.emotional_shift_evidence:
                results.append(f"candidate needs emotional evidence:{candidate.candidate_id}")
            else:
                results.append(f"candidate ready for review:{candidate.candidate_id}")
        return results


@dataclass
class ExtractionCommandHandler:
    command_type: str
    service: ExtractionService
    aggregate_type: str = "expression_moment_candidate"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "DetectTimestampedAnchorHitsCommand":
            hits = self.service.detect_anchor_hits(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
            )
            return {"anchor_hit_ids": [str(item.anchor_hit_id) for item in hits]}
        if self.command_type == "RunExpressionExtractionCommand":
            return self.service.run_extraction(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                skill_key=payload.get("skill_key"),
                retry_of_run_id=UUID(payload["retry_of_run_id"]) if payload.get("retry_of_run_id") else None,
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "InvokeJITExtractionSkillCommand":
            return self.service.invoke_jit_extraction_skill(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                skill_key=payload["skill_key"],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RejectUnsupportedCandidateCommand":
            return self.service.reject_unsupported_candidate(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                reason=payload["reason"],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "QueueExpressionMomentCandidateForReviewCommand":
            return self.service.queue_candidate_for_review(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise ExtractionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("candidate_id") or payload.get("expression_session_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_extraction_command_handlers(bus: CommandBus, service: ExtractionService) -> None:
    for command_type in [
        "DetectTimestampedAnchorHitsCommand",
        "RunExpressionExtractionCommand",
        "InvokeJITExtractionSkillCommand",
        "RejectUnsupportedCandidateCommand",
        "QueueExpressionMomentCandidateForReviewCommand",
    ]:
        bus.register_handler(ExtractionCommandHandler(command_type=command_type, service=service))
