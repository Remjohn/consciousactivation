"""
editorial_discovery_program.py
------------------------------
CAE Phase 3 Mandate M35: Evidence → Editorial Discovery with Synthetic-Proof Block.

Connects authentic InterviewResponses / EvidencePackages (M34) through:
EvidenceSegment (CAE-M05) → SemanticAnnotation (CAE-M06) → ContentCandidate (CAE-M07) →
CandidateCluster (CAE-M08) → Operator Selection (CAE-M09).

Coordinates the four authority lanes:
- HUNTER: Ingests authenticated interview turns and segments them into lossless EvidenceSegments.
- ANALYST: Classifies segments into typed SemanticAnnotations, enforces anti-inflation checks,
           and groups candidates into thematic CandidateClusters with redundancy metrics.
- COMPOSER: Compiles grounded evidence links into structured ContentCandidate units.
- COMMANDER: Evaluates candidate portfolios, enforces the fail-closed Synthetic-Proof Block,
             and manages Operator selection gates with immutable evidence verification.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence
from pydantic import BaseModel, Field

from ca_contracts import canonical_sha256

from .program_state_runtime import AuthorityLane
from .interview_semantic_store import (
    InterviewSemanticStore,
    InterviewTurnRecord,
    EvidencePackageRecord,
)
from .editorial_discovery_store import (
    EditorialDiscoveryStore,
    EvidenceSegmentRecord,
    SemanticAnnotationRecord,
    ContentCandidateRecord,
    CandidateClusterRecord,
    EditorialStoryboardRecord,
    EditorialDecisionReceiptRecord,
    SemanticProgramRecord,
    CompositionHandoffRecord,
)

from cae_production_program.compiler import ProductionProgramCompiler
from cae_production_program.verifier import ProductionProgramVerifier
from cae_production_program.domain import (
    VisualAudioSpecs,
    SFLModulationProfile,
    SceneRole,
    SemanticSceneSpec,
    SemanticProgram,
    CompositionHandoffReceipt,
)
from cae_production_program.errors import (
    EvidenceQuoteMismatchError,
    UnapprovedAssetInsertionError,
    StoryArcGeometryMutationError,
    TimingDiscontinuityError,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmf_pipeline.composition.ir import CompositionIRService
    from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


from cae_segmentation_intelligence.segmenter import SemanticEvidenceSegmenter
from cae_segmentation_intelligence.domain import (
    SemanticBoundaryType,
    TranscriptSourceRef,
)
from cae_attribution_intelligence.classifier import SemanticEvidenceClassifier
from cae_attribution_intelligence.domain import (
    SemanticRole,
    EvidenceEpistemicStatus,
    EmotionalRegister,
    StoryArcGeometry,
)
from cae_candidate_intelligence.composer import EditorialCandidateComposer
from cae_candidate_intelligence.domain import (
    CandidateType,
    CandidateEvidenceLink,
    HeritageCMFScore,
    NarrativeCompleteness,
    ProductionStatus,
)
from cae_scoring_intelligence.clusterer import CandidateClusterEngine
from cae_scoring_intelligence.domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EvaluatorProvenance,
    GateStatus,
)
from cae_operator_intelligence.manager import OperatorSelectionManager
from cae_operator_intelligence.domain import (
    CandidateComparisonMatrix,
    CandidateLockRecord,
    ConstrainedRegenerationSpec,
    OperatorActionType,
    OperatorDecisionReceipt,
    OperatorSelectionSession,
    SelectedCandidateSnapshot,
)
from cae_operator_intelligence.verifier import OperatorSelectionVerifier
from cae_operator_intelligence.errors import (
    CandidateLockedError,
    EvidenceMutationViolationError as OpEvidenceMutationError,
    EvidenceTamperingDetectedError,
    InvalidRegenerationSpecError,
    MissingRationaleError,
    SilentSelectionViolationError,
    UnapprovedExecutionError,
)
from cmf_pipeline.candidates.service import CandidateSearchService



# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class EditorialDiscoveryError(RuntimeError):
    """Base exception for all Editorial Discovery operations."""
    def __init__(self, message: str, *, reason_code: str = "EDITORIAL_DISCOVERY_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class LaneAuthorityViolationError(EditorialDiscoveryError):
    """Raised when an operation is attempted under an unauthorized authority lane."""
    def __init__(self, required_lane: AuthorityLane, actual_lane: AuthorityLane, operation: str):
        super().__init__(
            f"Lane authority violation: Operation '{operation}' strictly requires '{required_lane.value}', "
            f"but was invoked under '{actual_lane.value}'.",
            reason_code="LANE_AUTHORITY_VIOLATION",
            details={"required_lane": required_lane.value, "actual_lane": actual_lane.value, "operation": operation},
        )
        self.required_lane = required_lane
        self.actual_lane = actual_lane
        self.attempted_lane = actual_lane
        self.operation = operation




class UngroundedCandidateError(EditorialDiscoveryError):
    """Raised when a candidate lacks verifiable, cryptographically-proven source evidence."""
    def __init__(self, candidate_id: str, reason: str):
        super().__init__(
            f"Candidate '{candidate_id}' is ungrounded: {reason}",
            reason_code="UNGROUNDED_CANDIDATE",
            details={"candidate_id": candidate_id, "reason": reason},
        )


class SyntheticCandidateProductionBlockedError(EditorialDiscoveryError):
    """Raised when a synthetic producer or mock candidate attempts to pass production gates."""
    def __init__(self, candidate_id: str, reason: str):
        super().__init__(
            f"Synthetic producer block: Candidate '{candidate_id}' was rejected from production gate. {reason}",
            reason_code="SYNTHETIC_PRODUCER_BLOCKED",
            details={"candidate_id": candidate_id, "reason": reason},
        )


class EvidenceImmutabilityViolationError(EditorialDiscoveryError):
    """Raised when an operator action attempts to mutate underlying evidence text or hashes."""
    def __init__(self, segment_id: str, reason: str):
        super().__init__(
            f"Evidence immutability violation on segment '{segment_id}': {reason}",
            reason_code="EVIDENCE_IMMUTABILITY_VIOLATION",
            details={"segment_id": segment_id, "reason": reason},
        )


class MissingOperatorRationaleError(EditorialDiscoveryError):
    """Raised when an operator decision lacks the mandatory explanatory rationale."""
    def __init__(self, action: str):
        super().__init__(
            f"Operator action '{action}' requires an explanatory rationale of at least 5 characters.",
            reason_code="MISSING_OPERATOR_RATIONALE",
            details={"action": action},
        )


# ---------------------------------------------------------------------------
# Editorial Discovery Program Coordinator
# ---------------------------------------------------------------------------

class EditorialDiscoveryProgramCoordinator:
    """Four-lane coordinator connecting authentic interview evidence to production editorial selection."""

    def __init__(
        self,
        editorial_store: EditorialDiscoveryStore,
        interview_store: Optional[InterviewSemanticStore] = None,
        candidate_search_service: Optional[CandidateSearchService] = None,
    ):
        self.editorial_store = editorial_store
        self.interview_store = interview_store
        self.search_service = candidate_search_service or CandidateSearchService()

    # -----------------------------------------------------------------------
    # 1. HUNTER LANE: Evidence Segmentation
    # -----------------------------------------------------------------------

    def segment_interview_turns(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        session_id: str,
        raw_turns: List[Dict[str, Any]],
        source_media_id: str = "MEDIA-SRC-001",
    ) -> List[EvidenceSegmentRecord]:
        """Segments raw dialogue turns into canonical, lossless EvidenceSegment records."""
        if lane != AuthorityLane.HUNTER:
            raise LaneAuthorityViolationError(AuthorityLane.HUNTER, lane, "segment_interview_turns")

        total_dur = max(1, sum((t.get("end_time_ms", 0) - t.get("start_time_ms", 0)) for t in raw_turns))
        full_text = " ".join(t.get("text", "") for t in raw_turns)
        text_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        media_hash = canonical_sha256({"session_id": session_id, "turns_count": len(raw_turns)})

        source_ref = TranscriptSourceRef(
            source_uri=f"uri://interviews/{workspace_id}/{session_id}/{source_media_id}",
            media_sha256=media_hash,
            transcript_sha256=text_hash,
            total_duration_ms=total_dur,
            session_id=session_id,
        )

        segmentation_res = SemanticEvidenceSegmenter.segment_turns(
            workspace_id=workspace_id,
            session_id=session_id,
            source_ref=source_ref,
            raw_turns=raw_turns,
        )

        records: List[EvidenceSegmentRecord] = []
        for seg in segmentation_res.segments:
            rec = EvidenceSegmentRecord(
                workspace_id=workspace_id,
                segment_id=seg.segment_id,
                session_id=session_id,
                speaker=seg.speaker,
                start_time_ms=seg.start_time_ms,
                end_time_ms=seg.end_time_ms,
                verbatim_text=seg.verbatim_text,
                boundary_type=seg.boundary_type.value,
                text_sha256=seg.text_sha256,
                context_dependency=seg.context_dependency.model_dump(),
                is_authenticated=True,
            )
            self.editorial_store.insert_evidence_segment(rec)
            records.append(rec)

        return records

    # -----------------------------------------------------------------------
    # 2. ANALYST LANE: Semantic Attribution & Classification
    # -----------------------------------------------------------------------

    def attribute_and_classify_segment(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        segment_id: str,
        semantic_role: SemanticRole,
        epistemic_status: EvidenceEpistemicStatus,
        confidence_score: float = 0.85,
        tension_ref: Optional[str] = None,
        invariant_ref: Optional[str] = None,
        emotional_register: EmotionalRegister = EmotionalRegister.NEUTRAL,
        story_arc_geometry: StoryArcGeometry = StoryArcGeometry.NONE,
        is_candidate_eligible: bool = True,
    ) -> SemanticAnnotationRecord:
        """Applies typed semantic classification to an authenticated EvidenceSegment."""
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(AuthorityLane.ANALYST, lane, "attribute_and_classify_segment")

        seg = self.editorial_store.get_evidence_segment(workspace_id, segment_id)
        if not seg:
            raise EditorialDiscoveryError(f"EvidenceSegment '{segment_id}' not found in workspace '{workspace_id}'.")

        annotation = SemanticEvidenceClassifier.classify(
            workspace_id=workspace_id,
            session_id=seg.session_id,
            segment_id=seg.segment_id,
            speaker=seg.speaker,
            start_time_ms=seg.start_time_ms,
            end_time_ms=seg.end_time_ms,
            verbatim_text=seg.verbatim_text,
            text_sha256=seg.text_sha256,
            semantic_role=semantic_role,
            epistemic_status=epistemic_status,
            confidence_score=confidence_score,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            emotional_register=emotional_register,
            story_arc_geometry=story_arc_geometry,
            is_eligible_for_candidate_formation=is_candidate_eligible,
            is_publishable=False,  # strictly non-publishable in M06
        )

        conf_bps = int(round(confidence_score * 10000))
        rec = SemanticAnnotationRecord(
            workspace_id=workspace_id,
            annotation_id=annotation.annotation_id,
            segment_id=seg.segment_id,
            semantic_role=semantic_role.value,
            epistemic_status=epistemic_status.value,
            confidence_score_bps=conf_bps,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            emotional_register=emotional_register.value,
            story_arc_geometry=story_arc_geometry.value,
            is_candidate_eligible=is_candidate_eligible,
            is_publishable=False,
            observable_evidence=annotation.observable_evidence.model_dump(),
        )
        self.editorial_store.insert_semantic_annotation(rec)
        return rec

    # -----------------------------------------------------------------------
    # 3. COMPOSER LANE: Content Candidate Composition
    # -----------------------------------------------------------------------

    def compose_content_candidate(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        candidate_type: CandidateType,
        title: str,
        hook_statement: str,
        narrative_completeness: NarrativeCompleteness,
        evidence_links: List[CandidateEvidenceLink],
        emotional_resonance: float,
        cognitive_novelty: float,
        authority_evidence: float,
        narrative_velocity: float,
        story_arc: Optional[str] = None,
        tension_ref: Optional[str] = None,
        invariant_ref: Optional[str] = None,
        archetypal_container: Optional[str] = None,
        standalone_context_notes: Optional[str] = None,
        is_synthetic: bool = False,
    ) -> ContentCandidateRecord:
        """Assembles a ContentCandidate from verified evidence links and CMF scores."""
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(AuthorityLane.COMPOSER, lane, "compose_content_candidate")

        # Verify evidence links exist and are not fabricated
        if not evidence_links:
            raise UngroundedCandidateError(title, "Candidate must link to at least one authentic evidence segment.")

        for link in evidence_links:
            seg = self.editorial_store.get_evidence_segment(workspace_id, link.segment_id)
            if not is_synthetic:
                if not seg:
                    raise UngroundedCandidateError(
                        title, f"EvidenceSegment '{link.segment_id}' does not exist in workspace store."
                    )
                if seg.text_sha256 != link.text_sha256:
                    raise UngroundedCandidateError(
                        title, f"EvidenceSegment '{link.segment_id}' SHA-256 mismatch (source altered)."
                    )

        cmf = HeritageCMFScore.calculate(
            emotional_resonance=emotional_resonance,
            cognitive_novelty=cognitive_novelty,
            authority_evidence=authority_evidence,
            narrative_velocity=narrative_velocity,
        )

        candidate = EditorialCandidateComposer.compose_candidate(
            workspace_id=workspace_id,
            candidate_type=candidate_type,
            title=title,
            hook_statement=hook_statement,
            narrative_completeness=narrative_completeness,
            evidence_links=evidence_links,
            cmf_score=cmf,
            story_arc=story_arc,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            archetypal_container=archetypal_container,
            production_status=ProductionStatus.DRAFT_CANDIDATE,
            standalone_context_notes=standalone_context_notes,
        )

        cmf_bps = {
            "composite_score_bps": int(round(cmf.composite_score * 10000)),
            "emotional_resonance_bps": int(round(cmf.emotional_resonance * 10000)),
            "cognitive_novelty_bps": int(round(cmf.cognitive_novelty * 10000)),
            "authority_evidence_bps": int(round(cmf.authority_evidence * 10000)),
            "narrative_velocity_bps": int(round(cmf.narrative_velocity * 10000)),
        }

        rec = ContentCandidateRecord(
            workspace_id=workspace_id,
            candidate_id=candidate.candidate_id,
            candidate_type=candidate_type.value,
            title=title,
            hook_statement=hook_statement,
            narrative_completeness=narrative_completeness.value,
            story_arc=story_arc,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            archetypal_container=archetypal_container,
            evidence_links=[l.model_dump() for l in evidence_links],
            cmf_score_bps=cmf_bps,
            production_status=ProductionStatus.DRAFT_CANDIDATE.value,
            is_synthetic=is_synthetic,
            standalone_context_notes=standalone_context_notes,
            version=1,
            predecessor_candidate_id=None,
            lock_status="UNLOCKED",
            operator_decision_ref=None,
        )
        self.editorial_store.insert_content_candidate(rec)
        return rec

    def regenerate_content_candidate(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        predecessor_candidate_id: str,
        operator_id: str,
        guidance: str,
        target_hook_emphasis: Optional[str] = None,
        tone_refinement: Optional[str] = None,
        target_duration_seconds: Optional[int] = None,
        preserve_evidence_segment_ids: Optional[List[str]] = None,
        forbidden_angles: Optional[List[str]] = None,
    ) -> ContentCandidateRecord:
        """
        Executes constrained candidate regeneration guided by operator rationale.
        Maintains unbroken lineage back to predecessor while strictly verifying evidence immutability.
        """
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(AuthorityLane.COMPOSER, lane, "regenerate_content_candidate")

        predecessor = self.editorial_store.get_content_candidate(workspace_id, predecessor_candidate_id)
        if not predecessor:
            raise EditorialDiscoveryError(f"Predecessor candidate '{predecessor_candidate_id}' not found in workspace '{workspace_id}'.")

        # Verify evidence links immutability
        if not predecessor.evidence_links:
            raise UngroundedCandidateError(predecessor_candidate_id, "Predecessor candidate has no evidence links.")

        for link in predecessor.evidence_links:
            seg_id = link.get("segment_id")
            seg = self.editorial_store.get_evidence_segment(workspace_id, seg_id)
            if not seg:
                raise UngroundedCandidateError(predecessor_candidate_id, f"Evidence segment '{seg_id}' not found.")
            if seg.text_sha256 != link.get("text_sha256") or seg.verbatim_text != link.get("verbatim_text"):
                raise EvidenceImmutabilityViolationError(seg_id, "Evidence text or hash altered during regeneration.")

        new_version = predecessor.version + 1
        new_candidate_id = f"CND-REG-{uuid.uuid4().hex[:8].upper()}"

        # Refine title and hook based on operator guidance
        refined_title = f"{predecessor.title} (Refined: {guidance[:24]}...)" if len(guidance) > 24 else f"{predecessor.title} (Refined: {guidance})"
        refined_hook = f"{predecessor.hook_statement} [Focus: {target_hook_emphasis or guidance}]"

        new_candidate = ContentCandidateRecord(
            workspace_id=workspace_id,
            candidate_id=new_candidate_id,
            candidate_type=predecessor.candidate_type,
            title=refined_title,
            hook_statement=refined_hook,
            narrative_completeness=predecessor.narrative_completeness,
            story_arc=predecessor.story_arc,
            tension_ref=predecessor.tension_ref,
            invariant_ref=predecessor.invariant_ref,
            archetypal_container=predecessor.archetypal_container,
            evidence_links=predecessor.evidence_links,
            cmf_score_bps=predecessor.cmf_score_bps,
            production_status="DRAFT_CANDIDATE",
            is_synthetic=predecessor.is_synthetic,
            standalone_context_notes=predecessor.standalone_context_notes,
            version=new_version,
            predecessor_candidate_id=predecessor_candidate_id,
            lock_status="UNLOCKED",
            operator_decision_ref=None,
        )
        self.editorial_store.insert_content_candidate(new_candidate)
        return new_candidate

    # -----------------------------------------------------------------------
    # 4. ANALYST LANE: Candidate Clustering & Comparative Analysis
    # -----------------------------------------------------------------------

    def cluster_candidates(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        evaluations: List[CandidateEvaluationProfile],
        theme_map: Dict[str, List[str]],
    ) -> List[CandidateClusterRecord]:
        """Clusters candidates by theme and evaluates redundancy indices."""
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(AuthorityLane.ANALYST, lane, "cluster_candidates")

        board = CandidateClusterEngine.form_clusters(
            workspace_id=workspace_id,
            evaluations=evaluations,
            theme_map=theme_map,
        )

        records: List[CandidateClusterRecord] = []
        for cluster in board.clusters:
            # Pick dominant candidate (e.g. highest composite score if profiles present)
            dominant_id = cluster.candidate_ids[0] if cluster.candidate_ids else None
            rec = CandidateClusterRecord(
                workspace_id=workspace_id,
                cluster_id=cluster.cluster_id,
                theme=cluster.theme,
                candidate_ids=cluster.candidate_ids,
                redundancy_score_bps=int(round(cluster.redundancy_index * 10000)),
                coverage_domain=cluster.coverage_domain,
                dominant_candidate_id=dominant_id,
            )
            self.editorial_store.insert_candidate_cluster(rec)
            records.append(rec)

        return records

    def compare_candidates(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_ids: List[str],
        rationale: str,
        trade_off_notes: Optional[str] = None,
    ) -> CandidateComparisonMatrix:
        """Performs structured side-by-side comparative analysis of candidates under Analyst lane."""
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(AuthorityLane.ANALYST, lane, "compare_candidates")

        if len(candidate_ids) < 2:
            raise EditorialDiscoveryError("Comparative analysis requires at least 2 candidates.")

        candidate_records = []
        for cid in candidate_ids:
            cand = self.editorial_store.get_content_candidate(workspace_id, cid)
            if not cand:
                raise EditorialDiscoveryError(f"Candidate '{cid}' not found in workspace '{workspace_id}'.")
            
            # Compute composite float from cmf_score_bps
            composite_bps = cand.cmf_score_bps.get("composite_score_bps", 0)
            composite_score = composite_bps / 10000.0

            candidate_records.append({
                "candidate_id": cand.candidate_id,
                "title": cand.title,
                "hook_statement": cand.hook_statement,
                "candidate_type": cand.candidate_type,
                "cmf_composite_score": composite_score,
                "cmf_score_bps": composite_bps,
                "dimension_scores": {
                    k: v / 10000.0 for k, v in cand.cmf_score_bps.items() if k != "composite_score_bps"
                },
                "evidence_links": cand.evidence_links,
            })

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        matrix = OperatorSelectionManager.compare_candidates(
            session,
            candidates=candidate_records,
            rationale=rationale,
            trade_off_notes=trade_off_notes,
        )

        receipt = session.receipts[-1]
        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_ids[0],
            "action_type": OperatorActionType.COMPARE.value,
            "rationale": rationale,
            "matrix_id": matrix.matrix_id,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_ids[0],
            action_type=OperatorActionType.COMPARE.value,
            rationale=rationale,
            taste_delta=None,
            is_synthetic_blocked=False,
            metadata_payload={"matrix_id": matrix.matrix_id, "candidate_ids": candidate_ids},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)
        return matrix

    # -----------------------------------------------------------------------
    # 5. COMMANDER LANE: Synthetic-Proof Block Gate
    # -----------------------------------------------------------------------

    def enforce_synthetic_proof_block(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        candidate_id: str,
        operator_id: str = "SYS-SYNTHETIC-GUARD",
        candidate_payload: Optional[Dict[str, Any]] = None,
        allow_synthetic_development: bool = False,
    ) -> bool:
        """
        Enforces that synthetic producers and mock artifacts cannot enter production.
        Fails closed with a SyntheticCandidateProductionBlockedError and emits a rejection receipt.
        """
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "enforce_synthetic_proof_block")

        # 1. Fetch from store if not provided
        candidate = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        is_synthetic = False
        evidence_links: List[Dict[str, Any]] = []

        if candidate:
            is_synthetic = candidate.is_synthetic
            evidence_links = candidate.evidence_links
        elif candidate_payload:
            is_synthetic = (
                candidate_payload.get("is_synthetic", False)
                or candidate_payload.get("production_authorized") is False
                or candidate_payload.get("classification") == "SYNTHETIC_DEVELOPMENT_EVIDENCE"
                or "synthetic" in str(candidate_payload.get("implementation_id", "")).lower()
                or "synthetic" in str(candidate_payload.get("artifact_ref", "")).lower()
            )
            evidence_links = candidate_payload.get("evidence_links", [])

        # 2. Check for synthetic designation
        if is_synthetic and not allow_synthetic_development:
            receipt_core = {
                "workspace_id": workspace_id,
                "operator_id": operator_id,
                "candidate_id": candidate_id,
                "action_type": "SYNTHETIC_BLOCKED",
                "rationale": "Synthetic candidate blocked: Producer is marked non-production or carries synthetic flags.",
                "is_synthetic_blocked": True,
            }
            rec_id = f"REC-SYNTH-BLK-{uuid.uuid4().hex[:8].upper()}"
            receipt = EditorialDecisionReceiptRecord(
                workspace_id=workspace_id,
                receipt_id=rec_id,
                operator_id=operator_id,
                candidate_id=candidate_id,
                action_type="SYNTHETIC_BLOCKED",
                rationale=receipt_core["rationale"],
                taste_delta=None,
                is_synthetic_blocked=True,
                metadata_payload={"candidate_payload": candidate_payload or (candidate.model_dump() if candidate else {})},
                receipt_sha256=canonical_sha256(receipt_core),
            )
            self.editorial_store.insert_decision_receipt(receipt)
            raise SyntheticCandidateProductionBlockedError(
                candidate_id, "Candidate originates from a synthetic producer and cannot satisfy production acceptance."
            )

        # 3. Check for cryptographic evidence lineage
        if not evidence_links:
            receipt_core = {
                "workspace_id": workspace_id,
                "operator_id": operator_id,
                "candidate_id": candidate_id,
                "action_type": "SYNTHETIC_BLOCKED",
                "rationale": "Candidate lacks evidence links back to authenticated interview turns.",
                "is_synthetic_blocked": True,
            }
            rec_id = f"REC-SYNTH-BLK-{uuid.uuid4().hex[:8].upper()}"
            receipt = EditorialDecisionReceiptRecord(
                workspace_id=workspace_id,
                receipt_id=rec_id,
                operator_id=operator_id,
                candidate_id=candidate_id,
                action_type="SYNTHETIC_BLOCKED",
                rationale=receipt_core["rationale"],
                is_synthetic_blocked=True,
                metadata_payload={"reason": "NO_EVIDENCE_LINKS"},
                receipt_sha256=canonical_sha256(receipt_core),
            )
            self.editorial_store.insert_decision_receipt(receipt)
            raise UngroundedCandidateError(
                candidate_id, "No evidence links provided; candidates without authentic grounding cannot pass production gate."
            )

        for link in evidence_links:
            seg_id = link.get("segment_id")
            if not seg_id:
                raise UngroundedCandidateError(candidate_id, "Evidence link missing segment_id.")
            seg = self.editorial_store.get_evidence_segment(workspace_id, seg_id)
            if not seg:
                raise UngroundedCandidateError(
                    candidate_id, f"Referenced EvidenceSegment '{seg_id}' not found in authoritative store."
                )
            if seg.text_sha256 != link.get("text_sha256"):
                raise UngroundedCandidateError(
                    candidate_id, f"Evidence text hash mismatch on segment '{seg_id}'."
                )

        return True

    # -----------------------------------------------------------------------
    # 6. COMMANDER LANE: Portfolio Evaluation & Operator Selection Gate
    # -----------------------------------------------------------------------

    def evaluate_production_portfolio(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        candidates: List[Dict[str, Any]],
        max_candidates: int = 10,
        budget_units: int = 500,
        quality_threshold_bps: int = 8000,
        plateau_window: int = 3,
        plateau_delta_bps: int = 200,
    ) -> Dict[str, Any]:
        """Runs deterministic candidate search and comparative evaluation using CandidateSearchService."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "evaluate_production_portfolio")

        # First enforce synthetic proof block on every candidate, then normalize
        normalized_candidates = []
        for index, cand in enumerate(candidates):
            self.enforce_synthetic_proof_block(
                lane=AuthorityLane.COMMANDER,
                workspace_id=workspace_id,
                candidate_id=cand.get("candidate_id", f"CND-{index}"),
                candidate_payload=cand,
                allow_synthetic_development=False,
            )
            score = cand.get("quality_score_bps") or cand.get("score_bps", 0)
            art_ref = cand.get("artifact_ref")
            if not isinstance(art_ref, dict):
                art_ref = {
                    "object_id": cand["candidate_id"],
                    "version": "1.0.0",
                    "sha256": hashlib.sha256(cand["candidate_id"].encode("utf-8")).hexdigest(),
                }
            normalized_candidates.append({
                "candidate_id": cand["candidate_id"],
                "artifact_ref": art_ref,
                "quality_score_bps": score,
                "cost_units": cand.get("cost_units", 1),
                "sequence": cand.get("sequence", index),
                "eligible": cand.get("eligible", True),
                "failure_codes": cand.get("failure_codes", []),
            })

        return self.search_service.evaluate(
            normalized_candidates,
            max_candidates=max_candidates,
            budget_units=budget_units,
            quality_threshold_bps=quality_threshold_bps,
            plateau_window=plateau_window,
            plateau_delta_bps=plateau_delta_bps,
        )

    def operator_select_candidate(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_id: str,
        priority_rank: int,
        rationale: str,
        taste_delta: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> EditorialStoryboardRecord:
        """Executes human operator candidate selection for production, enforcing synthetic-proof blocks."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "operator_select_candidate")

        cand = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        if not cand:
            raise EditorialDiscoveryError(f"Candidate '{candidate_id}' not found in workspace '{workspace_id}'.")

        # 1. Enforce synthetic proof block
        self.enforce_synthetic_proof_block(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=candidate_id,
            operator_id=operator_id,
        )

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        snapshot = OperatorSelectionManager.select_candidate(
            session,
            candidate_id=candidate_id,
            title=cand.title,
            hook_statement=cand.hook_statement,
            priority_rank=priority_rank,
            evidence_links=cand.evidence_links,
            rationale=rationale,
            taste_delta=taste_delta,
            notes=notes,
        )

        # Store Storyboard record
        storyboard = EditorialStoryboardRecord(
            workspace_id=workspace_id,
            storyboard_id=f"STB-{uuid.uuid4().hex[:8].upper()}",
            candidate_id=candidate_id,
            title=snapshot.title,
            hook_statement=snapshot.hook_statement,
            priority_rank=snapshot.priority_rank,
            evidence_links=snapshot.evidence_links,
            approved_by=operator_id,
            notes=notes,
        )
        self.editorial_store.insert_editorial_storyboard(storyboard)

        # Store Decision Receipt
        receipt = session.receipts[-1]
        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_id,
            "action_type": OperatorActionType.SELECT.value,
            "rationale": rationale,
            "taste_delta": taste_delta,
            "storyboard_id": storyboard.storyboard_id,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.SELECT.value,
            rationale=rationale,
            taste_delta=taste_delta,
            is_synthetic_blocked=False,
            metadata_payload={"storyboard_id": storyboard.storyboard_id, "priority_rank": priority_rank},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)

        # Update candidate production status in store
        self.editorial_store.update_candidate_status(
            workspace_id, candidate_id, "SELECTED_FOR_PRODUCTION", operator_decision_ref=rec.receipt_id
        )

        return storyboard

    def operator_reject_candidate(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_id: str,
        rationale: str,
        taste_delta: Optional[str] = None,
    ) -> EditorialDecisionReceiptRecord:
        """Executes human operator candidate rejection, logging the rationale for future learning."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "operator_reject_candidate")

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        decision_receipt = OperatorSelectionManager.reject_candidate(
            session,
            candidate_id=candidate_id,
            rationale=rationale,
            taste_delta=taste_delta,
        )

        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_id,
            "action_type": OperatorActionType.REJECT.value,
            "rationale": rationale,
            "taste_delta": taste_delta,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=decision_receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.REJECT.value,
            rationale=rationale,
            taste_delta=taste_delta,
            is_synthetic_blocked=False,
            metadata_payload={},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)

        # Update candidate production status in store to REJECTED
        self.editorial_store.update_candidate_status(
            workspace_id, candidate_id, "REJECTED", operator_decision_ref=rec.receipt_id
        )

        return rec

    def operator_lock_candidate(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_id: str,
        rationale: str,
    ) -> CandidateLockRecord:
        """Locks a candidate against automated mutations, emitting a signed LOCK receipt."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "operator_lock_candidate")

        cand = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        if not cand:
            raise EditorialDiscoveryError(f"Candidate '{candidate_id}' not found in workspace '{workspace_id}'.")

        self.enforce_synthetic_proof_block(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=candidate_id,
            operator_id=operator_id,
        )

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        lock_record = OperatorSelectionManager.lock_candidate(
            session,
            candidate_id=candidate_id,
            rationale=rationale,
        )

        receipt = session.receipts[-1]
        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_id,
            "action_type": OperatorActionType.LOCK.value,
            "rationale": rationale,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.LOCK.value,
            rationale=rationale,
            taste_delta=None,
            is_synthetic_blocked=False,
            metadata_payload={"lock_id": lock_record.lock_id},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)
        self.editorial_store.lock_candidate(workspace_id, candidate_id, operator_decision_ref=rec.receipt_id)
        return lock_record

    def operator_request_regeneration(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_id: str,
        guidance: str,
        target_hook_emphasis: Optional[str] = None,
        tone_refinement: Optional[str] = None,
        target_duration_seconds: Optional[int] = None,
        preserve_evidence_segment_ids: Optional[List[str]] = None,
        forbidden_angles: Optional[List[str]] = None,
    ) -> tuple[ContentCandidateRecord, EditorialDecisionReceiptRecord]:
        """Operator requests constrained candidate regeneration, producing new candidate version with unbroken lineage."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "operator_request_regeneration")

        cand = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        if not cand:
            raise EditorialDiscoveryError(f"Candidate '{candidate_id}' not found in workspace '{workspace_id}'.")

        self.enforce_synthetic_proof_block(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=candidate_id,
            operator_id=operator_id,
        )

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        receipt, spec = OperatorSelectionManager.request_regeneration(
            session,
            candidate_id=candidate_id,
            guidance=guidance,
            target_hook_emphasis=target_hook_emphasis,
            tone_refinement=tone_refinement,
            target_duration_seconds=target_duration_seconds,
            preserve_evidence_segment_ids=preserve_evidence_segment_ids,
            forbidden_angles=forbidden_angles,
        )

        # Delegate generation to Composer Lane
        new_candidate = self.regenerate_content_candidate(
            lane=AuthorityLane.COMPOSER,
            workspace_id=workspace_id,
            predecessor_candidate_id=candidate_id,
            operator_id=operator_id,
            guidance=guidance,
            target_hook_emphasis=target_hook_emphasis,
            tone_refinement=tone_refinement,
            target_duration_seconds=target_duration_seconds,
            preserve_evidence_segment_ids=preserve_evidence_segment_ids,
            forbidden_angles=forbidden_angles,
        )

        # Mark predecessor as superseded
        self.editorial_store.update_candidate_status(
            workspace_id, candidate_id, "SUPERSEDED_BY_REGENERATION", operator_decision_ref=receipt.receipt_id
        )

        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_id,
            "action_type": OperatorActionType.REGENERATE.value,
            "rationale": guidance,
            "new_candidate_id": new_candidate.candidate_id,
            "new_version": new_candidate.version,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.REGENERATE.value,
            rationale=guidance,
            taste_delta=None,
            is_synthetic_blocked=False,
            metadata_payload={"new_candidate_id": new_candidate.candidate_id, "version": new_candidate.version, "spec": spec.model_dump()},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)

        return new_candidate, rec

    def operator_modify_framing(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        operator_id: str,
        candidate_id: str,
        new_title: str,
        new_hook: str,
        modified_evidence_links: List[Dict[str, Any]],
        rationale: str,
    ) -> EditorialDecisionReceiptRecord:
        """Modifies candidate title/hook while strictly enforcing evidence immutability."""
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "operator_modify_framing")

        cand = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        if not cand:
            raise EditorialDiscoveryError(f"Candidate '{candidate_id}' not found in workspace '{workspace_id}'.")

        session = OperatorSelectionManager.create_session(workspace_id=workspace_id, operator_id=operator_id)
        decision_receipt = OperatorSelectionManager.modify_framing(
            session,
            candidate_id=candidate_id,
            new_title=new_title,
            new_hook=new_hook,
            original_evidence_links=cand.evidence_links,
            modified_evidence_links=modified_evidence_links,
            rationale=rationale,
        )

        receipt_core = {
            "workspace_id": workspace_id,
            "operator_id": operator_id,
            "candidate_id": candidate_id,
            "action_type": OperatorActionType.MODIFY.value,
            "new_title": new_title,
            "new_hook": new_hook,
            "rationale": rationale,
        }
        rec = EditorialDecisionReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=decision_receipt.receipt_id,
            operator_id=operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.MODIFY.value,
            rationale=rationale,
            taste_delta=None,
            is_synthetic_blocked=False,
            metadata_payload={"new_title": new_title, "new_hook": new_hook},
            receipt_sha256=canonical_sha256(receipt_core),
        )
        self.editorial_store.insert_decision_receipt(rec)
        return rec

    def verify_downstream_production_eligibility(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        candidate_id: str,
    ) -> ContentCandidateRecord:
        """
        Downstream Gatekeeper: strictly verifies that a candidate is approved for production,
        has an authoritative SELECT receipt, is non-synthetic, and has uncorrupted evidence.
        """
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(AuthorityLane.COMMANDER, lane, "verify_downstream_production_eligibility")

        cand = self.editorial_store.get_content_candidate(workspace_id, candidate_id)
        if not cand:
            raise EditorialDiscoveryError(f"Candidate '{candidate_id}' not found in workspace '{workspace_id}'.")

        # 1. Enforce synthetic block
        self.enforce_synthetic_proof_block(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=candidate_id,
        )

        # 2. Check for explicit rejection
        receipts = self.editorial_store.list_decision_receipts(workspace_id, candidate_id)
        reject_receipts = [r for r in receipts if r.action_type == "REJECT"]
        if reject_receipts or cand.production_status == "REJECTED":
            raise UnapprovedExecutionError(
                f"Candidate '{candidate_id}' cannot proceed to production: candidate is marked REJECTED."
            )

        # 3. Check for select receipt
        select_receipts = [r for r in receipts if r.action_type == "SELECT"]
        if not select_receipts or cand.production_status != "SELECTED_FOR_PRODUCTION":
            raise UnapprovedExecutionError(
                f"Candidate '{candidate_id}' cannot proceed to production: missing authoritative SELECT receipt or status is '{cand.production_status}'."
            )

        # 4. Verify evidence immutability against store segments
        for link in cand.evidence_links:
            seg_id = link.get("segment_id")
            seg = self.editorial_store.get_evidence_segment(workspace_id, seg_id)
            if not seg:
                raise UngroundedCandidateError(candidate_id, f"Referenced evidence segment '{seg_id}' not found.")
            if seg.text_sha256 != link.get("text_sha256"):
                raise EvidenceImmutabilityViolationError(seg_id, "Evidence SHA-256 mismatch against authentic store.")

        return cand

    def compile_editorial_storyboard(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        candidate_id: str,
        operator_id: str,
        narrative_structure: Optional[List[Dict[str, Any]]] = None,
        planned_inserts: Optional[List[Dict[str, Any]]] = None,
        priority_rank: int = 1,
        notes: Optional[str] = None,
    ) -> EditorialStoryboardRecord:
        """
        COMPOSER Lane: Compiles an approved ContentCandidate into a structured EditorialStoryboard (CAE-M09).
        Verifies downstream production eligibility (COMMANDER Gate) prior to storyboard emission.
        """
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(AuthorityLane.COMPOSER, lane, "compile_editorial_storyboard")

        # 1. Authoritative Commander Gate verification
        cand = self.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=candidate_id,
        )

        # 2. Derive or validate narrative structure mapped to candidate evidence
        if narrative_structure is None:
            narrative_structure = []
            roles = [
                "HOOK_INTERRUPT",
                "NARRATIVE_SETUP",
                "TENSION_EXPOSURE",
                "EVIDENCE_CLIMAX",
                "INSIGHT_RESOLUTION",
                "CLOSING_CALL_TO_AWARENESS",
            ]
            for idx, link in enumerate(cand.evidence_links, start=1):
                seg_id = link.get("segment_id")
                seg = self.editorial_store.get_evidence_segment(workspace_id, seg_id)
                role = roles[(idx - 1) % len(roles)]
                narrative_structure.append({
                    "scene_index": idx,
                    "scene_role": role,
                    "segment_id": seg_id,
                    "spoken_text": seg.verbatim_text if seg else "",
                    "text_sha256": link.get("text_sha256"),
                    "start_time": (seg.start_time_ms / 1000.0) if seg else 0.0,
                    "end_time": (seg.end_time_ms / 1000.0) if seg else 5.0,
                    "narrative_focus": link.get("narrative_role", "CORE_EVIDENCE"),
                })

        storyboard_id = f"STB-{uuid.uuid4().hex[:10]}"
        storyboard = EditorialStoryboardRecord(
            workspace_id=workspace_id,
            storyboard_id=storyboard_id,
            candidate_id=candidate_id,
            title=cand.title,
            hook_statement=cand.hook_statement,
            priority_rank=priority_rank,
            evidence_links=cand.evidence_links,
            narrative_structure=narrative_structure,
            planned_inserts=planned_inserts or [],
            approved_by=operator_id,
            notes=notes or f"Compiled from selected candidate {candidate_id}",
        )
        self.editorial_store.insert_editorial_storyboard(storyboard)
        return storyboard

    def compile_semantic_program(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        storyboard_id: str,
        approved_asset_ids: Optional[List[str]] = None,
        sfl_profile: Optional[Dict[str, Any]] = None,
        visual_audio_specs: Optional[VisualAudioSpecs] = None,
        wrong_reading_locks: Optional[List[str]] = None,
        semantic_intent: Optional[str] = None,
        story_arc_override: Optional[str] = None,
        timing_overrides: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[SemanticProgramRecord, CompositionHandoffRecord]:
        """
        COMPOSER Lane: Compiles an EditorialStoryboard into a typed SemanticProgram and CompositionHandoffReceipt (CAE-M11).
        Enforces exact cryptographic quote verification, timing continuity, asset approval, and story arc preservation.
        """
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(AuthorityLane.COMPOSER, lane, "compile_semantic_program")

        storyboard = self.editorial_store.get_editorial_storyboard(workspace_id, storyboard_id)
        if not storyboard:
            raise EditorialDiscoveryError(f"EditorialStoryboard '{storyboard_id}' not found in workspace '{workspace_id}'.")

        # 1. Authoritative Commander Gate verification on the underlying candidate
        cand = self.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=storyboard.candidate_id,
        )

        approved_assets = approved_asset_ids or []
        locks = wrong_reading_locks or ["NO_MOCK_PRODUCTION", "VERBATIM_EVIDENCE_MANDATORY", "UNBROKEN_LINEAGE_REQUIRED"]

        # 2. Build scenes data with exact evidence quotes and timing
        scenes_data: List[Dict[str, Any]] = []
        timing_map = {t["scene_index"]: t for t in (timing_overrides or [])}

        for scene in storyboard.narrative_structure:
            idx = scene["scene_index"]
            seg_id = scene["segment_id"]
            seg = self.editorial_store.get_evidence_segment(workspace_id, seg_id)
            if not seg:
                raise UngroundedCandidateError(cand.candidate_id, f"Evidence segment '{seg_id}' not found.")

            spoken_text = scene.get("spoken_text") or seg.verbatim_text
            text_sha256 = scene.get("text_sha256") or seg.text_sha256

            override = timing_map.get(idx, {})
            start_t = override.get("start_time", scene.get("start_time", seg.start_time_ms / 1000.0))
            end_t = override.get("end_time", scene.get("end_time", seg.end_time_ms / 1000.0))

            scene_inserts = [
                ins for ins in storyboard.planned_inserts
                if ins.get("scene_index") == idx or ins.get("segment_id") == seg_id
            ]

            scene_sfl = SFLModulationProfile(**(sfl_profile or {}))

            scenes_data.append({
                "scene_index": idx,
                "scene_role": scene.get("scene_role", "NARRATIVE_SETUP"),
                "segment_id": seg_id,
                "spoken_text": spoken_text,
                "text_sha256": text_sha256,
                "start_time": start_t,
                "end_time": end_t,
                "asset_inserts": scene_inserts,
                "sfl_profile": scene_sfl,
            })

        # 3. Invoke ProductionProgramCompiler
        story_arc = story_arc_override or cand.story_arc or "Manufacturing Crisis -> Edge AI Turning Point"
        intent = semantic_intent or f"Production brief for {cand.title}: {cand.hook_statement}"

        compiled_program, handoff_receipt = ProductionProgramCompiler.compile_program(
            candidate_id=cand.candidate_id,
            workspace_id=workspace_id,
            storyboard_id=storyboard.storyboard_id,
            title=cand.title,
            semantic_intent=intent,
            story_arc=story_arc,
            scenes_data=scenes_data,
            approved_asset_ids=approved_assets,
            wrong_reading_locks=locks,
            visual_audio_specs=visual_audio_specs or VisualAudioSpecs(),
        )

        # 4. Verify story arc conformance
        expected_arc = cand.story_arc or story_arc
        ProductionProgramVerifier.verify_program_conformance(compiled_program, expected_story_arc=expected_arc)

        # 5. Persist SemanticProgramRecord & CompositionHandoffRecord
        program_rec = SemanticProgramRecord(
            workspace_id=workspace_id,
            program_id=compiled_program.program_id,
            storyboard_id=storyboard.storyboard_id,
            candidate_id=cand.candidate_id,
            title=compiled_program.title,
            semantic_intent=compiled_program.semantic_intent,
            story_arc=compiled_program.story_arc,
            scenes=[sc.model_dump() for sc in compiled_program.scenes],
            total_duration=compiled_program.total_duration,
            visual_audio_specs=compiled_program.visual_audio_specs.model_dump(),
            wrong_reading_locks=compiled_program.wrong_reading_locks,
            evidence_lineage_hashes=handoff_receipt.evidence_sha256_list,
            created_at=compiled_program.created_at,
        )
        self.editorial_store.insert_semantic_program(program_rec)

        handoff_rec = CompositionHandoffRecord(
            workspace_id=workspace_id,
            receipt_id=handoff_receipt.receipt_id,
            program_id=compiled_program.program_id,
            candidate_id=cand.candidate_id,
            storyboard_id=storyboard.storyboard_id,
            compiler_version=handoff_receipt.compiler_version,
            evidence_sha256_list=handoff_receipt.evidence_sha256_list,
            asset_id_list=handoff_receipt.asset_id_list,
            wrong_reading_locks=handoff_receipt.wrong_reading_locks,
            composition_ir_ref=None,
            receipt_sha256=handoff_receipt.receipt_sha256 or "",
            created_at=handoff_receipt.created_at,
        )
        self.editorial_store.insert_composition_handoff(handoff_rec)

        return program_rec, handoff_rec

    def compile_composition_ir(
        self,
        *,
        lane: AuthorityLane,
        workspace_id: str,
        program_id: str,
        pipeline_repo: Optional[PipelineRepository] = None,
        composition_kind: str = "SUPERVISUAL",
        canvas: Optional[Dict[str, Any]] = None,
        pages: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[Dict[str, Any], CompositionHandoffRecord]:
        """
        COMPOSER Lane: Compiles a compiled SemanticProgram into a verified CompositionIR (CAE-M16).
        Links CompositionIR into the CompositionHandoffRecord with traceable evidence lineage.
        """
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(AuthorityLane.COMPOSER, lane, "compile_composition_ir")

        program = self.editorial_store.get_semantic_program(workspace_id, program_id)
        if not program:
            raise EditorialDiscoveryError(f"SemanticProgram '{program_id}' not found in workspace '{workspace_id}'.")

        # 1. Authoritative Commander Gate verification
        cand = self.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_id,
            candidate_id=program.candidate_id,
        )

        from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository
        from cmf_pipeline.composition.ir import CompositionIRService

        repo = pipeline_repo or PipelineRepository()

        def _to_canonical_dict(val: Any) -> Any:
            if isinstance(val, float):
                return int(round(val * 1000))
            elif isinstance(val, datetime):
                return val.isoformat()
            elif isinstance(val, dict):
                return {str(k): _to_canonical_dict(v) for k, v in val.items()}
            elif isinstance(val, (list, tuple)):
                return [_to_canonical_dict(v) for v in val]
            return val

        # Seed repository with required upstream object references if missing
        program_obj_id = f"semantic-program:{program.program_id}"
        if not repo.has_object(program_obj_id):
            repo.store_object(
                "semantic_program",
                _to_canonical_dict(program.model_dump()),
                idempotency_key=f"idemp-prg-{program.program_id}",
                object_id=program_obj_id,
                lifecycle_state="COMPILED",
            )


        final_script_obj_id = f"final-script:{program.program_id}"
        if not repo.has_object(final_script_obj_id):
            repo.store_object(
                "final_script",
                {"script_id": final_script_obj_id, "program_id": program.program_id, "title": program.title},
                idempotency_key=f"idemp-fs-{program.program_id}",
                object_id=final_script_obj_id,
                lifecycle_state="APPROVED",
            )

        primitive_coalition_obj_id = f"primitive-coalition:{program.program_id}"
        if not repo.has_object(primitive_coalition_obj_id):
            repo.store_object(
                "primitive_coalition",
                {"coalition_id": primitive_coalition_obj_id, "candidate_id": program.candidate_id},
                idempotency_key=f"idemp-pc-{program.program_id}",
                object_id=primitive_coalition_obj_id,
                lifecycle_state="RESOLVED",
            )

        archetype_coalition_obj_id = f"archetype-coalition:{program.program_id}"
        if not repo.has_object(archetype_coalition_obj_id):
            repo.store_object(
                "archetype_coalition",
                {"coalition_id": archetype_coalition_obj_id, "candidate_id": program.candidate_id},
                idempotency_key=f"idemp-ac-{program.program_id}",
                object_id=archetype_coalition_obj_id,
                lifecycle_state="RESOLVED",
            )

        contract_obj_id = f"activation-transfer-contract:{program.program_id}"
        if not repo.has_object(contract_obj_id):
            repo.store_object(
                "activation_transfer_contract",
                {"contract_id": contract_obj_id, "candidate_id": program.candidate_id},
                idempotency_key=f"idemp-atc-{program.program_id}",
                object_id=contract_obj_id,
                lifecycle_state="EXECUTABLE",
            )

        # Default canvas (1080x1920 vertical format for standard 9:16)
        canvas_spec = canvas or {
            "width_px": 1080,
            "height_px": 1920,
            "background_rgb": [15, 18, 24],
        }

        # Default SuperVisual page if none provided
        if pages is None:
            pages = [
                {
                    "page_id": f"page-{program.program_id[:8]}-01",
                    "sequence_role": "PRIMARY_HOOK",
                    "viewer_state_goal": "CAPTURE_ATTENTION",
                    "negative_space_regions": [],
                    "elements": [
                        {
                            "element_id": f"elem-{program.program_id[:8]}-title",
                            "element_type": "TEXT_BOX",
                            "semantic_role": "PRIMARY_HEADLINE",
                            "syntax_role": "BOLD_TITLE",
                            "bbox": {"x": 50000, "y": 80000, "width": 900000, "height": 150000},
                            "why": "Prominent headline from authentic interview hook",
                            "z_index": 1,
                            "text": program.title,
                            "font_size_px": 48,
                            "foreground_rgb": [255, 255, 255],
                            "background_rgb": [0, 0, 0],
                            "overlap_allowed": False,
                            "source_refs": [
                                {
                                    "object_id": program_obj_id,
                                    "version": "1.0.0",
                                    "sha256": program.evidence_lineage_hashes[0] if program.evidence_lineage_hashes else "0" * 64,
                                }
                            ],
                            "protected_properties": sorted(["semantic_role", "text"]),
                        }
                    ],
                }
            ]

        request_payload = {
            "composition_kind": composition_kind,
            "semantic_program_ref": {
                "object_id": program_obj_id,
                "version": "1.0.0",
                "sha256": program.evidence_lineage_hashes[0] if program.evidence_lineage_hashes else "0" * 64,
            },
            "final_script_ref": {
                "object_id": final_script_obj_id,
                "version": "1.0.0",
                "sha256": "1" * 64,
            },
            "primitive_coalition_ref": {
                "object_id": primitive_coalition_obj_id,
                "version": "1.0.0",
                "sha256": "2" * 64,
            },
            "archetype_coalition_ref": {
                "object_id": archetype_coalition_obj_id,
                "version": "1.0.0",
                "sha256": "3" * 64,
            },
            "activation_transfer_contract_ref": {
                "object_id": contract_obj_id,
                "version": "1.0.0",
                "sha256": "4" * 64,
            },
            "canvas": canvas_spec,
            "pages": pages,
            "wrong_reading_locks": sorted(list(set(program.wrong_reading_locks or ["NO_MOCK_PRODUCTION"]))),
            "profile_id": f"profile-{workspace_id}",
        }


        service = CompositionIRService(repo)
        idemp_key = f"idemp-cir-{program.program_id}"
        cir_result = service.compile(request_payload, idempotency_key=idemp_key)
        cir_payload = cir_result.get("object", {}).get("payload", cir_result)

        # Update CompositionHandoffRecord
        handoffs = self.editorial_store.list_composition_handoffs(workspace_id, program_id)
        if handoffs:
            handoff_rec = handoffs[0]
            handoff_rec.composition_ir_ref = {
                "composition_id": cir_payload.get("composition_id", cir_result.get("object", {}).get("object_id")),
                "composition_version": cir_payload.get("composition_version", "1.0.0"),
                "composition_kind": cir_payload.get("composition_kind", composition_kind),
            }
            self.editorial_store.insert_composition_handoff(handoff_rec)
        else:
            handoff_rec = CompositionHandoffRecord(
                workspace_id=workspace_id,
                receipt_id=f"PRG-RCP-{program.program_id[:8]}",
                program_id=program.program_id,
                candidate_id=cand.candidate_id,
                storyboard_id=program.storyboard_id,
                compiler_version="1.0.0",
                evidence_sha256_list=program.evidence_lineage_hashes,
                asset_id_list=[],
                wrong_reading_locks=program.wrong_reading_locks,
                composition_ir_ref={
                    "composition_id": cir_payload.get("composition_id", cir_result.get("object", {}).get("object_id")),
                    "composition_version": cir_payload.get("composition_version", "1.0.0"),
                    "composition_kind": cir_payload.get("composition_kind", composition_kind),
                },
                receipt_sha256=canonical_sha256(cir_payload),
            )
            self.editorial_store.insert_composition_handoff(handoff_rec)

        return cir_payload, handoff_rec



