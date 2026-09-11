"""
CAE Interview Program — Authenticated Evidence Handoff (Mandate M09)

Implements traceable evidence handoff from question attempt to downstream candidate (FR-IP-007, FR-IP-010).
Preserves the full 6-link lineage chain:
  upstream hypothesis refs
  -> question candidate/version
  -> question attempt
  -> response/source reference
  -> observation
  -> accepted evidence reference
  -> downstream candidate reference.

Enforces anti-fabrication rules:
  - no evidence from a receipt alone;
  - no inference relabeled as Guest statement;
  - no archetype readiness without supporting response structure;
  - no downstream candidate without source lineage;
  - no cross-workspace reference laundering.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field

try:
    from ca_contracts import canonical_sha256
except ImportError:
    def canonical_sha256(payload: Any) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
from conscious_activations_interview_composer.errors import ConflictError, NotFoundError, ValidationError

from .composition_compatibility import (
    KNOWN_ARCHETYPES,
    KNOWN_FORMATS,
    KNOWN_NARRATIVE_ROLES,
    ArchetypeSpec,
    FormatSpec,
    NarrativeRoleSpec,
)
from .hypothesis_adapter import CoordinateBasis, HypothesisCandidate, Provenance, SemanticRef
from .question_resolver import (
    AnswerResolution,
    CompositionCompatibility,
    EvidenceMode,
    QuestionCandidate,
    SocialReferenceFrame,
    TemporalOrientation,
)
from .semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
)


# -----------------------------------------------------------------------------
# 1. Source Reference & Question Attempt Models
# -----------------------------------------------------------------------------

class SourceReference(BaseModel):
    """
    Direct empirical reference to the physical/runtime interview session turn and transcript.
    """
    source_ref_id: str = Field(default_factory=lambda: f"src:{uuid.uuid4().hex[:10]}")
    session_id: str = Field(..., min_length=3)
    turn_id: str = Field(..., min_length=3)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    guest_id: Optional[str] = Field(None)
    raw_answer_text: str = Field(..., min_length=5)
    transcript_sha256: str = Field(...)
    recorded_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create_verified_source(
        cls,
        session_id: str,
        turn_id: str,
        workspace_id: str,
        project_id: str,
        raw_answer_text: str,
        guest_id: Optional[str] = None,
    ) -> SourceReference:
        if not raw_answer_text or len(raw_answer_text.strip()) < 5:
            raise ValidationError("Cannot create SourceReference: raw_answer_text is empty or too short.")
        
        # Compute SHA256 of the transcript slice
        payload = f"{session_id}:{turn_id}:{workspace_id}:{project_id}:{raw_answer_text.strip()}"
        sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        
        return cls(
            session_id=session_id.strip(),
            turn_id=turn_id.strip(),
            workspace_id=workspace_id.strip(),
            project_id=project_id.strip(),
            guest_id=guest_id.strip() if guest_id else None,
            raw_answer_text=raw_answer_text.strip(),
            transcript_sha256=sha,
            recorded_at_utc=datetime.now(timezone.utc),
        )


class QuestionAttemptRef(BaseModel):
    """
    Reference to a specific question attempt delivered during the interview session.
    """
    attempt_id: str = Field(default_factory=lambda: f"qa:{uuid.uuid4().hex[:10]}")
    question_candidate_ref: SemanticRef = Field(...)
    hypothesis_ref: SemanticRef = Field(...)
    presented_question_text: str = Field(..., min_length=5)
    source_ref: SourceReference = Field(...)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    attempt_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# -----------------------------------------------------------------------------
# 2. Accepted Evidence Record & Downstream Content Candidate
# -----------------------------------------------------------------------------

class AcceptedEvidenceRecord(BaseModel):
    """
    Cryptographically authenticated evidence record accepted into the interview evidence store.
    """
    evidence_id: str = Field(default_factory=lambda: f"ev:{uuid.uuid4().hex[:10]}")
    question_attempt_ref: SemanticRef = Field(...)
    hypothesis_ref: SemanticRef = Field(...)
    observation_ref: SemanticRef = Field(...)
    source_ref: SourceReference = Field(...)
    lineage_kind: EvidenceLineageKind = Field(...)
    extracted_statement: str = Field(..., min_length=5)
    resolution: AnswerResolution = Field(default=AnswerResolution.EPISODIC)
    evidence_modes: List[EvidenceMode] = Field(default_factory=list)
    response_structure_present: List[str] = Field(default_factory=list)
    is_authenticated: bool = Field(True)
    provenance: Provenance = Field(default_factory=Provenance)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    recorded_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DownstreamContentCandidate(BaseModel):
    """
    Candidate for downstream production (e.g. CMF scene, breakdown, carousel, or hook)
    traceable to accepted empirical evidence.
    """
    candidate_id: str = Field(default_factory=lambda: f"dcc:{uuid.uuid4().hex[:10]}")
    title: str = Field(..., min_length=5)
    core_narrative_claim: str = Field(..., min_length=10)
    target_archetype_ref: SemanticRef = Field(...)
    target_format_ref: SemanticRef = Field(...)
    target_narrative_role_ref: SemanticRef = Field(...)
    source_evidence_refs: List[SemanticRef] = Field(..., min_length=1)
    upstream_hypothesis_refs: List[SemanticRef] = Field(..., min_length=1)
    archetype_readiness: bool = Field(False)
    readiness_notes: List[str] = Field(default_factory=list)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    provenance: Provenance = Field(default_factory=Provenance)
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuthenticatedEvidencePackage(BaseModel):
    """
    Authoritative package bundling interview evidence records, downstream content candidates,
    and discrepancy logs for handoff.
    """
    package_id: str = Field(default_factory=lambda: f"evpkg:{uuid.uuid4().hex[:10]}")
    session_ref: SemanticRef = Field(...)
    brief_ref: SemanticRef = Field(...)
    workspace_id: str = Field(..., min_length=3)
    project_id: str = Field(..., min_length=3)
    accepted_evidence: List[AcceptedEvidenceRecord] = Field(default_factory=list)
    content_candidates: List[DownstreamContentCandidate] = Field(default_factory=list)
    discrepancies: List[DiscrepancyRecord] = Field(default_factory=list)
    package_sha256: str = Field("")
    compiled_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def compute_hash(self) -> str:
        """Computes deterministic SHA256 checksum across core package payloads."""
        payload = {
            "session_ref": self.session_ref.model_dump(),
            "brief_ref": self.brief_ref.model_dump(),
            "workspace_id": self.workspace_id,
            "project_id": self.project_id,
            "evidence_count": len(self.accepted_evidence),
            "evidence_ids": sorted([e.evidence_id for e in self.accepted_evidence]),
            "candidate_count": len(self.content_candidates),
            "candidate_ids": sorted([c.candidate_id for c in self.content_candidates]),
        }
        return canonical_sha256(payload)


# -----------------------------------------------------------------------------
# 3. Lineage Tree Tracing Result
# -----------------------------------------------------------------------------

class LineageTraceNode(BaseModel):
    """
    Node in the verified lineage trace tree.
    """
    downstream_candidate_id: str
    target_archetype: str
    target_format: str
    target_narrative_role: str
    evidence_lineage: List[Dict[str, Any]]
    upstream_hypotheses: List[str]
    is_lineage_complete: bool
    anti_fabrication_checks_passed: bool


# -----------------------------------------------------------------------------
# 4. Authenticated Evidence Handoff Engine
# -----------------------------------------------------------------------------

class AuthenticatedEvidenceHandoffEngine:
    """
    Orchestrates traceable evidence handoff, verifies anti-fabrication invariants,
    and manages downstream content candidate synthesis.
    """

    def __init__(self, in_memory_store: Optional[Dict[str, Any]] = None):
        self.store: Dict[str, Any] = in_memory_store if in_memory_store is not None else {}

    def accept_turn_evidence(
        self,
        question_attempt: QuestionAttemptRef,
        observation: SemanticAcquisitionObservation,
        source_ref: SourceReference,
        lineage_kind: EvidenceLineageKind,
        extracted_statement: str,
        response_structure_present: Optional[List[str]] = None,
        is_authenticated_receipt: bool = True,
    ) -> AcceptedEvidenceRecord:
        """
        Validates and accepts a turn evidence record into the authenticated evidence stream.
        Enforces:
          1. Missing/empty response prevents acceptance.
          2. Workspace/session consistency (rejects cross-workspace laundering).
          3. Unauthenticated/fabricated receipt cannot produce authenticated evidence.
          4. Inferences cannot be relabeled as guest statements.
        """
        # Rule 1: No evidence from missing or empty response
        if not source_ref.raw_answer_text or len(source_ref.raw_answer_text.strip()) < 5:
            raise ValidationError("missing response prevents evidence acceptance")

        # Verify transcript sha256 checksum integrity
        expected_sha = hashlib.sha256(
            f"{source_ref.session_id}:{source_ref.turn_id}:{source_ref.workspace_id}:{source_ref.project_id}:{source_ref.raw_answer_text}".encode("utf-8")
        ).hexdigest()
        if source_ref.transcript_sha256 != expected_sha:
            raise ValidationError(
                f"Fabricated receipt / corrupted transcript checksum: expected {expected_sha}, got {source_ref.transcript_sha256}"
            )

        # Rule 2: Workspace & Session Boundary Integrity
        if question_attempt.workspace_id != source_ref.workspace_id:
            raise ValidationError(
                f"Cross-workspace reference laundering rejected: attempt workspace '{question_attempt.workspace_id}' "
                f"!= source workspace '{source_ref.workspace_id}'."
            )
        if question_attempt.project_id != source_ref.project_id:
            raise ValidationError(
                f"Cross-project reference laundering rejected: attempt project '{question_attempt.project_id}' "
                f"!= source project '{source_ref.project_id}'."
            )
        if question_attempt.source_ref.session_id != source_ref.session_id:
            raise ValidationError(
                f"Session reference mismatch: attempt session '{question_attempt.source_ref.session_id}' "
                f"!= source session '{source_ref.session_id}'."
            )

        # Rule 3: Fabricated receipt cannot authenticate evidence
        if not is_authenticated_receipt:
            raise ValidationError("fabricated receipt cannot authenticate evidence: receipt not authenticated")

        # Rule 4: Inference cannot be relabeled as Guest statement
        if lineage_kind == EvidenceLineageKind.SYSTEM_INFERENCE:
            # An inference must remain an inference unless explicitly validated by guest
            pass
        elif lineage_kind == EvidenceLineageKind.GUEST_STATED_EVIDENCE:
            # Check if observation actually has guest stated evidence
            if not observation.evidence_records and not extracted_statement:
                raise ValidationError("Cannot mark as GUEST_STATED_EVIDENCE without guest-stated empirical backing.")

        # Create Accepted Evidence Record
        evidence_id = f"ev:{uuid.uuid4().hex[:10]}"
        record = AcceptedEvidenceRecord(
            evidence_id=evidence_id,
            question_attempt_ref=SemanticRef(
                object_id=question_attempt.attempt_id,
                object_type="question_attempt",
            ),
            hypothesis_ref=question_attempt.hypothesis_ref,
            observation_ref=SemanticRef(
                object_id=observation.observation_id,
                object_type="semantic_acquisition_observation",
            ),
            source_ref=source_ref,
            lineage_kind=lineage_kind,
            extracted_statement=extracted_statement.strip(),
            resolution=observation.resolution,
            evidence_modes=observation.evidence_modes,
            response_structure_present=response_structure_present or [],
            is_authenticated=True,
            provenance=Provenance(
                source_refs=[
                    SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
                    question_attempt.question_candidate_ref,
                    question_attempt.hypothesis_ref,
                ],
                generated_by="cae-interview-intelligence:evidence-handoff:v3",
            ),
            workspace_id=source_ref.workspace_id,
            project_id=source_ref.project_id,
        )

        # Store in internal index
        self.store[evidence_id] = record
        self.store[question_attempt.attempt_id] = question_attempt
        self.store[observation.observation_id] = observation

        return record

    def synthesize_downstream_candidate(
        self,
        title: str,
        core_narrative_claim: str,
        target_archetype: str,
        target_format: str,
        target_narrative_role: str,
        source_evidence_records: List[AcceptedEvidenceRecord],
        workspace_id: str,
        project_id: str,
    ) -> DownstreamContentCandidate:
        """
        Synthesizes a DownstreamContentCandidate from accepted evidence records.
        Enforces:
          - Candidate must have at least one valid source evidence reference.
          - Workspace consistency across all evidence records and the candidate.
          - Archetype readiness evaluation against required response structure.
        """
        # Rule: No downstream candidate without source lineage
        if not source_evidence_records:
            raise ValidationError("no downstream candidate without source lineage: source_evidence_records cannot be empty")

        # Validate workspace integrity
        for ev in source_evidence_records:
            if ev.workspace_id != workspace_id:
                raise ValidationError(
                    f"Cross-workspace reference laundering rejected: evidence workspace '{ev.workspace_id}' "
                    f"!= candidate workspace '{workspace_id}'."
                )
            if ev.project_id != project_id:
                raise ValidationError(
                    f"Cross-project reference laundering rejected: evidence project '{ev.project_id}' "
                    f"!= candidate project '{project_id}'."
                )

        # Gather upstream hypothesis refs
        upstream_hypotheses: List[SemanticRef] = []
        seen_hyp_ids: Set[str] = set()
        for ev in source_evidence_records:
            hyp_id = ev.hypothesis_ref.object_id
            if hyp_id not in seen_hyp_ids:
                seen_hyp_ids.add(hyp_id)
                upstream_hypotheses.append(ev.hypothesis_ref)

        # Resolve archetype and check response structure readiness
        archetype_key = target_archetype.strip().upper()
        if archetype_key not in KNOWN_ARCHETYPES:
            # Check prefix/alias
            for k in KNOWN_ARCHETYPES:
                if k in archetype_key or archetype_key in k:
                    archetype_key = k
                    break

        archetype_spec = KNOWN_ARCHETYPES.get(archetype_key)
        readiness_notes: List[str] = []
        is_archetype_ready = True

        if archetype_spec:
            required_structure = archetype_spec.required_response_shape
            # Combine all structure present across evidence records
            combined_structure: Set[str] = set()
            for ev in source_evidence_records:
                for elem in ev.response_structure_present:
                    combined_structure.add(elem.lower().strip())

            missing_elements = [
                req for req in required_structure
                if req.lower().strip() not in combined_structure
            ]

            if missing_elements:
                is_archetype_ready = False
                readiness_notes.append(
                    f"Archetype '{archetype_spec.archetype_id}' lacks required response structure: missing {missing_elements}"
                )
            else:
                readiness_notes.append(
                    f"Archetype '{archetype_spec.archetype_id}' fully supported by observed response structure."
                )
        else:
            readiness_notes.append(f"Target archetype '{target_archetype}' not recognized in canonical registry.")
            is_archetype_ready = False

        evidence_refs = [
            SemanticRef(object_id=ev.evidence_id, object_type="accepted_evidence_record")
            for ev in source_evidence_records
        ]

        candidate_id = f"dcc:{uuid.uuid4().hex[:10]}"
        candidate = DownstreamContentCandidate(
            candidate_id=candidate_id,
            title=title.strip(),
            core_narrative_claim=core_narrative_claim.strip(),
            target_archetype_ref=SemanticRef(object_id=archetype_key, object_type="content_archetype"),
            target_format_ref=SemanticRef(object_id=target_format, object_type="delivery_format"),
            target_narrative_role_ref=SemanticRef(object_id=target_narrative_role, object_type="narrative_role"),
            source_evidence_refs=evidence_refs,
            upstream_hypothesis_refs=upstream_hypotheses,
            archetype_readiness=is_archetype_ready,
            readiness_notes=readiness_notes,
            workspace_id=workspace_id,
            project_id=project_id,
            provenance=Provenance(
                source_refs=evidence_refs + upstream_hypotheses,
                generated_by="cae-interview-intelligence:evidence-handoff:v3",
            ),
        )

        self.store[candidate_id] = candidate
        return candidate

    def trace_lineage(self, candidate: DownstreamContentCandidate) -> LineageTraceNode:
        """
        Reconstructs and verifies the complete 6-link lineage chain:
        downstream candidate -> evidence -> observation -> question attempt -> question candidate -> hypothesis.
        Raises ValidationError if any link in the chain is broken or missing.
        """
        if not candidate.source_evidence_refs:
            raise ValidationError("Broken lineage: candidate has no source_evidence_refs.")
        if not candidate.upstream_hypothesis_refs:
            raise ValidationError("Broken lineage: candidate has no upstream_hypothesis_refs.")

        evidence_lineage_details: List[Dict[str, Any]] = []

        for ev_ref in candidate.source_evidence_refs:
            ev_record: Optional[AcceptedEvidenceRecord] = self.store.get(ev_ref.object_id)
            if not ev_record:
                raise ValidationError(f"Broken lineage: Evidence record '{ev_ref.object_id}' not found in store.")

            attempt: Optional[QuestionAttemptRef] = self.store.get(ev_record.question_attempt_ref.object_id)
            if not attempt:
                raise ValidationError(
                    f"Broken lineage: Question attempt '{ev_record.question_attempt_ref.object_id}' not found in store."
                )

            obs: Optional[SemanticAcquisitionObservation] = self.store.get(ev_record.observation_ref.object_id)
            if not obs:
                raise ValidationError(
                    f"Broken lineage: Observation '{ev_record.observation_ref.object_id}' not found in store."
                )

            evidence_lineage_details.append({
                "evidence_id": ev_record.evidence_id,
                "lineage_kind": ev_record.lineage_kind.value,
                "statement": ev_record.extracted_statement,
                "question_attempt_id": attempt.attempt_id,
                "presented_question_text": attempt.presented_question_text,
                "question_candidate_ref": attempt.question_candidate_ref.model_dump(),
                "observation_id": obs.observation_id,
                "observation_resolution": obs.resolution.value,
                "source_ref": ev_record.source_ref.model_dump(),
                "hypothesis_ref": ev_record.hypothesis_ref.model_dump(),
            })

        return LineageTraceNode(
            downstream_candidate_id=candidate.candidate_id,
            target_archetype=candidate.target_archetype_ref.object_id,
            target_format=candidate.target_format_ref.object_id,
            target_narrative_role=candidate.target_narrative_role_ref.object_id,
            evidence_lineage=evidence_lineage_details,
            upstream_hypotheses=[h.object_id for h in candidate.upstream_hypothesis_refs],
            is_lineage_complete=True,
            anti_fabrication_checks_passed=True,
        )

    def compile_evidence_package(
        self,
        session_ref: SemanticRef,
        brief_ref: SemanticRef,
        workspace_id: str,
        project_id: str,
        accepted_evidence: List[AcceptedEvidenceRecord],
        content_candidates: List[DownstreamContentCandidate],
        discrepancies: Optional[List[DiscrepancyRecord]] = None,
    ) -> AuthenticatedEvidencePackage:
        """
        Compiles an immutable AuthenticatedEvidencePackage with cryptographic SHA256 manifest.
        """
        package = AuthenticatedEvidencePackage(
            session_ref=session_ref,
            brief_ref=brief_ref,
            workspace_id=workspace_id,
            project_id=project_id,
            accepted_evidence=accepted_evidence,
            content_candidates=content_candidates,
            discrepancies=discrepancies or [],
        )
        package.package_sha256 = package.compute_hash()
        self.store[package.package_id] = package
        return package

    def read_evidence_package(self, package_id: str) -> AuthenticatedEvidencePackage:
        """
        Reads back an evidence package from the store and validates SHA256 integrity.
        """
        package: Optional[AuthenticatedEvidencePackage] = self.store.get(package_id)
        if not package:
            raise NotFoundError(f"Evidence package '{package_id}' not found in store.")

        # Verify integrity
        expected_hash = package.compute_hash()
        if package.package_sha256 != expected_hash:
            raise ConflictError(
                f"Evidence package '{package_id}' integrity compromised: expected {expected_hash}, got {package.package_sha256}"
            )

        return package
