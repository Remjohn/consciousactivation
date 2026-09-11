"""
semantic_acquisition.py
-----------------------
Semantic Acquisition Observation and Evidence Lineage Distinction (CAE-M07).

Implements FR-IP-006 and FR-IP-007:
1. Minimum derived observation model for answer-driven routing and evidence lineage.
2. Strict type-safe boundary separating:
   - GUEST_STATED_EVIDENCE: direct empirical lived statements from the Guest.
   - SYSTEM_INFERENCE: interpretations, predictions, sentiment, or classifications from the system.
   - GUEST_VALIDATED_INTERPRETATION: system interpretations explicitly confirmed/corrected by the Guest.
3. Invariant checks ensuring receipt existence alone does not authenticate evidence.
4. Non-canonical derived projection preserving upstream AIR hypothesis immutability.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, field_validator, model_validator

from conscious_activations_interview_composer.errors import ValidationError

from .domain import QuestionStage
from .errors import InterviewIntelligenceError
from .hypothesis_adapter import Provenance, SemanticRef
from .question_resolver import (
    AnswerResolution,
    EvidenceMode,
    InformationCompleteness,
    SocialReferenceFrame,
    TemporalOrientation,
)


class EvidenceLineageKind(str, Enum):
    """
    Strict category of evidentiary lineage ensuring system inference is never conflated
    with guest-stated empirical facts.
    """
    GUEST_STATED_EVIDENCE = "guest_stated_evidence"
    SYSTEM_INFERENCE = "system_inference"
    GUEST_VALIDATED_INTERPRETATION = "guest_validated_interpretation"


class AcquisitionEvidenceRecord(BaseModel):
    """
    Individual evidence record extracted or derived during an interview turn.
    Maintains provenance, authentication status, and validation lineage.
    """
    record_id: str = Field(default_factory=lambda: f"evr:{uuid.uuid4().hex[:10]}")
    kind: EvidenceLineageKind = Field(...)
    turn_id: str = Field(..., min_length=1)
    statement_text: str = Field(..., min_length=1)
    
    # Direct reference to raw source turn response or audio transcript segment
    source_ref: SemanticRef = Field(...)
    
    # Authentication state
    is_authenticated: bool = Field(False)
    authentication_method: Optional[str] = Field(
        None,
        description="Method used for authentication: direct_spoken_testimony, guest_explicit_confirmation, unauthenticated_receipt, etc."
    )
    
    # Associated hypothesis and requirement references
    hypothesis_refs: List[SemanticRef] = Field(default_factory=list)
    requirement_refs: List[SemanticRef] = Field(default_factory=list)
    
    # Confidence and timing
    confidence_score: float = Field(1.0, ge=0.0, le=1.0)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Lineage for validated interpretations
    validated_from_inference_ref: Optional[SemanticRef] = Field(
        None,
        description="Reference to prior system inference if this record was confirmed by guest."
    )

    @model_validator(mode="after")
    def validate_authentication_integrity(self) -> AcquisitionEvidenceRecord:
        """
        Enforce invariant: An unverified receipt or API 200 alone cannot produce authenticated evidence.
        """
        if self.is_authenticated:
            if self.authentication_method == "unauthenticated_receipt":
                raise ValueError("Receipt existence alone cannot authenticate evidence.")
            if self.kind == EvidenceLineageKind.SYSTEM_INFERENCE:
                raise ValueError("System inference cannot be marked as authenticated guest evidence.")
        return self


class DiscrepancyRecord(BaseModel):
    """
    Structured record of a factual contradiction or discrepancy discovered in an interview turn.
    Must be recorded before reconciliation action is initiated.
    """
    discrepancy_id: str = Field(default_factory=lambda: f"disc:{uuid.uuid4().hex[:10]}")
    prior_claim_or_doc_ref: SemanticRef = Field(...)
    observed_claim_ref: SemanticRef = Field(...)
    nature_of_contradiction: str = Field(..., min_length=5)
    turn_id: str = Field(...)
    is_reconciled: bool = Field(False)
    reconciled_by_attempt_id: Optional[str] = Field(None)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SemanticAcquisitionObservation(BaseModel):
    """
    Comprehensive derived observation structure representing the semantic and evidentiary state
    of an interview turn response. Conforms strictly to 03_DERIVED_SCHEMAS.yaml.
    """
    observation_id: str = Field(default_factory=lambda: f"obs:{uuid.uuid4().hex[:10]}")
    question_attempt_ref: SemanticRef = Field(...)
    observed_response_ref: SemanticRef = Field(...)
    turn_id: str = Field(..., min_length=1)
    transcript_text: str = Field(..., min_length=1)
    
    # Semantic dimensions per FR-IP-006
    resolution: AnswerResolution = Field(default=AnswerResolution.GENERAL)
    completeness: InformationCompleteness = Field(default=InformationCompleteness.PARTIAL)
    evidence_modes: List[EvidenceMode] = Field(default_factory=lambda: [EvidenceMode.STORY])
    temporal_orientation: List[TemporalOrientation] = Field(
        default_factory=lambda: [TemporalOrientation.PAST_RECONSTRUCTION]
    )
    social_reference_frame: List[SocialReferenceFrame] = Field(
        default_factory=lambda: [SocialReferenceFrame.SELF]
    )
    interactional_fit: Optional[str] = Field("standard")
    
    # Reference collections
    discrepancy_refs: List[SemanticRef] = Field(default_factory=list)
    missing_requirement_refs: List[SemanticRef] = Field(default_factory=list)
    new_branch_refs: List[SemanticRef] = Field(default_factory=list)
    unresolved_requirement_ids: List[str] = Field(default_factory=list)
    new_branch_discovered: bool = Field(False)
    
    # Lineage tracking collections per FR-IP-007
    guest_stated_evidence_refs: List[SemanticRef] = Field(default_factory=list)
    system_inference_refs: List[SemanticRef] = Field(default_factory=list)
    guest_validated_interpretation_refs: List[SemanticRef] = Field(default_factory=list)
    
    # Concrete evidence records
    evidence_records: List[AcquisitionEvidenceRecord] = Field(default_factory=list)
    discrepancies: List[DiscrepancyRecord] = Field(default_factory=list)
    
    # Quality metrics
    has_contradiction: bool = Field(False)
    is_generic_slop: bool = Field(False)
    specificity_score: float = Field(0.7, ge=0.0, le=1.0)
    authenticity_score: float = Field(0.8, ge=0.0, le=1.0)
    
    # Non-canonical boundary flag
    is_canonical: bool = Field(False, description="Derived observations remain non-canonical.")
    provenance: Provenance = Field(default_factory=Provenance)

    @model_validator(mode="before")
    @classmethod
    def populate_refs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            qid = data.get("question_attempt_id")
            if qid and not data.get("question_attempt_ref"):
                data["question_attempt_ref"] = SemanticRef(object_id=qid, object_type="question_attempt")
            tid = data.get("turn_id")
            if tid and not data.get("observed_response_ref"):
                data["observed_response_ref"] = SemanticRef(object_id=f"turn_resp:{tid}", object_type="interview_turn_response")
        return data

    @property
    def question_attempt_id(self) -> str:
        return self.question_attempt_ref.object_id


class SemanticAcquisitionObserver:
    """
    Evaluator engine for semantic acquisition observations.
    Analyzes turn transcripts, classifies evidence vs inference, tracks discrepancies,
    and constructs typed SemanticAcquisitionObservation instances.
    """

    def observe_turn_response(
        self,
        question_attempt_id: str,
        turn_id: str,
        transcript_text: str,
        resolution: AnswerResolution = AnswerResolution.SPECIFIC,
        completeness: InformationCompleteness = InformationCompleteness.PARTIAL,
        evidence_modes: Optional[List[EvidenceMode]] = None,
        temporal_orientation: Optional[List[TemporalOrientation]] = None,
        social_reference_frame: Optional[List[SocialReferenceFrame]] = None,
        interactional_fit: Optional[str] = "standard",
        guest_statements: Optional[List[str]] = None,
        inferred_statements: Optional[List[str]] = None,
        validated_interpretations: Optional[List[Dict[str, Any]]] = None,
        discrepancies: Optional[List[DiscrepancyRecord]] = None,
        missing_requirement_refs: Optional[List[SemanticRef]] = None,
        new_branch_refs: Optional[List[SemanticRef]] = None,
        hypothesis_refs: Optional[List[SemanticRef]] = None,
        specificity_score: Optional[float] = None,
        authenticity_score: Optional[float] = None,
    ) -> SemanticAcquisitionObservation:
        """
        Constructs a complete SemanticAcquisitionObservation while strictly enforcing
        lineage segregation and invariant checks.
        """
        ev_modes = evidence_modes or [EvidenceMode.STORY]
        temp_orient = temporal_orientation or [TemporalOrientation.PAST_RECONSTRUCTION]
        soc_frame = social_reference_frame or [SocialReferenceFrame.SELF]
        hyp_refs = hypothesis_refs or []
        
        # Determine specificity & slop flags
        spec_score = specificity_score if specificity_score is not None else (
            0.25 if resolution in (AnswerResolution.ABSTRACT, AnswerResolution.GENERAL) else 0.85
        )
        auth_score = authenticity_score if authenticity_score is not None else 0.85
        is_slop = spec_score < 0.40 or resolution == AnswerResolution.ABSTRACT

        # Build evidence records
        evidence_records: List[AcquisitionEvidenceRecord] = []
        guest_stated_refs: List[SemanticRef] = []
        sys_inference_refs: List[SemanticRef] = []
        guest_val_refs: List[SemanticRef] = []

        turn_resp_ref = SemanticRef(
            object_id=f"turn_resp:{turn_id}",
            object_type="interview_turn_response",
        )

        # 1. Guest-Stated Evidence (Verbatim/Empirical)
        if guest_statements:
            for idx, stmt in enumerate(guest_statements):
                rec = AcquisitionEvidenceRecord(
                    kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
                    turn_id=turn_id,
                    statement_text=stmt,
                    source_ref=turn_resp_ref,
                    is_authenticated=True,
                    authentication_method="direct_spoken_testimony",
                    hypothesis_refs=hyp_refs,
                    confidence_score=1.0,
                )
                evidence_records.append(rec)
                guest_stated_refs.append(
                    SemanticRef(object_id=rec.record_id, object_type="guest_stated_evidence")
                )
        elif not is_slop and transcript_text and not validated_interpretations and not inferred_statements:
            # Default to full transcript as guest-stated evidence if no specific categories provided
            rec = AcquisitionEvidenceRecord(
                kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
                turn_id=turn_id,
                statement_text=transcript_text,
                source_ref=turn_resp_ref,
                is_authenticated=True,
                authentication_method="direct_spoken_testimony",
                hypothesis_refs=hyp_refs,
                confidence_score=auth_score,
            )
            evidence_records.append(rec)
            guest_stated_refs.append(
                SemanticRef(object_id=rec.record_id, object_type="guest_stated_evidence")
            )

        # 2. System Inference (Unconfirmed model derivations)
        if inferred_statements:
            for stmt in inferred_statements:
                rec = AcquisitionEvidenceRecord(
                    kind=EvidenceLineageKind.SYSTEM_INFERENCE,
                    turn_id=turn_id,
                    statement_text=stmt,
                    source_ref=turn_resp_ref,
                    is_authenticated=False,
                    authentication_method=None,
                    hypothesis_refs=hyp_refs,
                    confidence_score=0.75,
                )
                evidence_records.append(rec)
                sys_inference_refs.append(
                    SemanticRef(object_id=rec.record_id, object_type="system_inference")
                )

        # 3. Guest-Validated Interpretations
        if validated_interpretations:
            for vi in validated_interpretations:
                prior_inf_ref = (
                    SemanticRef(object_id=vi["prior_inference_id"], object_type="system_inference")
                    if "prior_inference_id" in vi
                    else None
                )
                rec = AcquisitionEvidenceRecord(
                    kind=EvidenceLineageKind.GUEST_VALIDATED_INTERPRETATION,
                    turn_id=turn_id,
                    statement_text=vi.get("statement_text", ""),
                    source_ref=turn_resp_ref,
                    is_authenticated=True,
                    authentication_method="guest_explicit_confirmation",
                    hypothesis_refs=hyp_refs,
                    validated_from_inference_ref=prior_inf_ref,
                    confidence_score=1.0,
                )
                evidence_records.append(rec)
                guest_val_refs.append(
                    SemanticRef(object_id=rec.record_id, object_type="guest_validated_interpretation")
                )

        # Discrepancy handling
        disc_list = discrepancies or []
        disc_refs = [
            SemanticRef(object_id=d.discrepancy_id, object_type="discrepancy_record")
            for d in disc_list
        ]
        has_contra = len(disc_list) > 0

        obs = SemanticAcquisitionObservation(
            question_attempt_ref=SemanticRef(
                object_id=question_attempt_id,
                object_type="question_attempt",
            ),
            observed_response_ref=turn_resp_ref,
            turn_id=turn_id,
            transcript_text=transcript_text,
            resolution=resolution,
            completeness=completeness,
            evidence_modes=ev_modes,
            temporal_orientation=temp_orient,
            social_reference_frame=soc_frame,
            interactional_fit=interactional_fit,
            discrepancy_refs=disc_refs,
            missing_requirement_refs=missing_requirement_refs or [],
            new_branch_refs=new_branch_refs or [],
            guest_stated_evidence_refs=guest_stated_refs,
            system_inference_refs=sys_inference_refs,
            guest_validated_interpretation_refs=guest_val_refs,
            evidence_records=evidence_records,
            discrepancies=disc_list,
            has_contradiction=has_contra,
            is_generic_slop=is_slop,
            specificity_score=spec_score,
            authenticity_score=auth_score,
            is_canonical=False,
            provenance=Provenance(
                source_refs=hyp_refs,
                generated_by="cae-interview-intelligence:semantic-acquisition:v1",
            ),
        )

        self.assert_evidence_not_conflated_with_inference(obs)
        return obs

    @staticmethod
    def assert_evidence_not_conflated_with_inference(observation: SemanticAcquisitionObservation) -> None:
        """
        Validates that system inferences are never listed as guest-stated evidence,
        and that authenticated evidence cannot have kind SYSTEM_INFERENCE.
        """
        guest_ref_ids = {r.object_id for r in observation.guest_stated_evidence_refs}
        sys_ref_ids = {r.object_id for r in observation.system_inference_refs}

        overlap = guest_ref_ids.intersection(sys_ref_ids)
        if overlap:
            raise ValidationError(
                f"Lineage violation: System inference conflated with guest-stated evidence: {overlap}"
            )

        for rec in observation.evidence_records:
            if rec.kind == EvidenceLineageKind.SYSTEM_INFERENCE and rec.is_authenticated:
                raise ValidationError(
                    f"Lineage violation: System inference record {rec.record_id} cannot be authenticated."
                )
            if rec.kind == EvidenceLineageKind.GUEST_STATED_EVIDENCE and rec.record_id in sys_ref_ids:
                raise ValidationError(
                    f"Lineage violation: Guest-stated evidence record {rec.record_id} serialized as system inference."
                )

    @staticmethod
    def assert_receipt_alone_not_authenticated(record: AcquisitionEvidenceRecord) -> None:
        """
        Asserts that a record with authentication method 'unauthenticated_receipt'
        is not marked as authenticated.
        """
        if record.authentication_method == "unauthenticated_receipt" and record.is_authenticated:
            raise ValidationError(
                "Receipt presence alone does not authenticate evidence (FR-IP-007 violation)."
            )
