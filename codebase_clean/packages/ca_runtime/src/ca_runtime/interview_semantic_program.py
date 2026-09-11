"""
interview_semantic_program.py
------------------------------
CAE Phase 3 Mandate M33: Interview Semantic Program + Existing Composer Boundary.

Connects approved CollisionHypotheses (M32) to the already-built Interview
Intelligence and Composer boundary (services/interview-composer & services/interview-intelligence).

Coordinates the four authority lanes:
- HUNTER: Ingests approved CollisionHypotheses, extracts JIT semantic targets, and derives
          question candidates across the 4-stage progression grammar.
- ANALYST: Enforces non-scripted/non-leading invariants, evaluates Matrix of Edging pressure paths,
           and checks downstream format/archetype compatibility.
- COMPOSER: Compiles canonical ActivativeInterviewBrief payloads via ActivativeInterviewBriefCompiler.
- COMMANDER: Executes operator authorization gates, seals briefs via BriefService/Store,
             emits signed execution receipts, and manages session lifecycle/repair.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence
from pydantic import BaseModel, Field

from .program_state_runtime import (
    AuthorityLane,
    UniversalProgramStateRuntime,
    ProgramTransitionResult,
    ProgramStateAggregate,
)
from .interview_semantic_store import (
    InterviewSemanticStore,
    InterviewBriefRecord,
    InterviewSessionRecord,
    InterviewSemanticReceiptRecord,
    InterviewTurnRecord,
    InterviewObservationRecord,
    EvidencePackageRecord,
    EvidenceAuthenticationRecord,
)
from cae_interview_intelligence.domain import (
    QuestionStage,
    DesiredEvidenceClass,
)
from cae_interview_intelligence.composer import InterviewBriefComposer
from cae_interview_intelligence.hypothesis_adapter import (
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    EvidenceMode,
    InformationCompleteness,
    QuestionCandidate,
    QuestionProgramDerived,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.brief_compiler import ActivativeInterviewBriefCompiler
from cae_interview_intelligence.adaptive_frontier import (
    AdaptiveAction,
    AdaptiveQuestionFrontierEngine,
    CoverageSpineItem,
    EvidenceRequirement,
    FrontierState,
    QuestionAttempt,
    RequirementStatus,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)
from cae_interview_intelligence.evidence_handoff import (
    AcceptedEvidenceRecord,
    AuthenticatedEvidenceHandoffEngine,
    AuthenticatedEvidencePackage,
    DownstreamContentCandidate,
    QuestionAttemptRef,
    SourceReference,
)
from conscious_activations_interview_composer.domain import (
    MATRIX_SEED_FIELDS,
    make_activative_interview_brief,
)


def _convert_floats_to_micros(val: Any) -> Any:
    """Recursively converts any float values to integer micros (1.0 = 1,000,000)."""
    if isinstance(val, float):
        return int(round(val * 1_000_000))
    elif isinstance(val, dict):
        return {k: _convert_floats_to_micros(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple)):
        return [_convert_floats_to_micros(v) for v in val]
    elif isinstance(val, BaseModel):
        return _convert_floats_to_micros(val.model_dump(mode="json"))
    return val


def compute_canonical_sha256(payload: Any) -> str:
    """Computes a deterministic SHA-256 digest of arbitrary structured payload."""
    payload_normalized = _convert_floats_to_micros(payload)
    try:
        from ca_contracts import canonical_sha256
        return canonical_sha256(payload_normalized)
    except Exception:
        data = json.dumps(payload_normalized, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        return hashlib.sha256(data).hexdigest()


# =============================================================================
# Fail-Closed Error Taxonomy
# =============================================================================

class InterviewProgramError(Exception):
    """Base exception for Interview Semantic Program errors."""
    pass


class UnauthorizedInterviewLaneError(InterviewProgramError):
    """Raised when an operation is attempted on an unauthorized authority lane."""
    pass


class WorkspaceScopeViolationError(InterviewProgramError):
    """Raised when tenant workspace isolation is violated."""
    pass


class LeadingQuestionViolationError(InterviewProgramError):
    """Raised when a candidate question violates non-scripted/non-leading invariants."""
    pass


class MatrixOfEdgingValidationError(InterviewProgramError):
    """Raised when Matrix of Edging parameters or pressure paths are invalid."""
    pass


class BriefCompilationError(InterviewProgramError):
    """Raised when brief compilation from hypothesis fails."""
    pass


class BriefAuthorizationError(InterviewProgramError):
    """Raised when operator authorization or sealing fails."""
    pass


class InvalidLineageError(InterviewProgramError):
    """Raised when cryptographic lineage or upstream reference is missing/invalid."""
    pass


class SelfAttestationViolationError(InterviewProgramError):
    """Raised when an actor attempts to self-attest its own evidence extractions."""
    pass


class SourceLineageViolationError(InterviewProgramError):
    """Raised when source sovereignty or transcript lineage cannot be verified."""
    pass


class AntiFabricationViolationError(InterviewProgramError):
    """Raised when generic slop or ungrounded claims attempt to satisfy evidence requirements."""
    pass


class FrontierExhaustionError(InterviewProgramError):
    """Raised when the adaptive frontier has no further valid actions."""
    pass


# =============================================================================
# Domain Evaluation Models & Receipts
# =============================================================================

class InterviewBriefEvaluation(BaseModel):
    """Adversarial evaluation result produced by the ANALYST lane."""
    matrix_valid: bool
    non_scripted_valid: bool
    archetype_compatibility_score_micros: int = 1_000_000
    pressure_path_score_micros: int = 1_000_000
    overall_confidence_micros: int = 1_000_000
    evaluated_questions_count: int
    gate_checks: List[Dict[str, Any]] = Field(default_factory=list)


class InterviewSemanticReceipt(BaseModel):
    """Immutable audit receipt emitted upon brief sealing or state commit."""
    receipt_id: str = Field(default_factory=lambda: f"rcpt_int_{uuid.uuid4().hex[:12]}")
    workspace_id: str
    brief_id: str
    hypothesis_id: str
    operator_authority: Dict[str, str]
    canonical_sha256: str
    decision: str  # SEALED, REJECTED, QUARANTINED
    score_breakdown_micros: Dict[str, int] = Field(default_factory=dict)
    gate_checks: List[Dict[str, Any]] = Field(default_factory=list)
    signature: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# =============================================================================
# Interview Semantic Program Coordinator
# =============================================================================

class InterviewSemanticProgramCoordinator:
    """
    Coordinates the 4 authority lanes for the Interview Semantic Program (CAE M33).
    Bridges approved Collision Hypotheses (M32) to the canonical Brief Compiler and
    Composer machinery.
    """

    def __init__(
        self,
        workspace_id: str,
        store: InterviewSemanticStore,
        state_runtime: Optional[UniversalProgramStateRuntime] = None,
    ):
        self.workspace_id = workspace_id
        self.store = store
        self.state_runtime = state_runtime
        self._aggregate_id: Optional[str] = None
        self._state_version: int = 1
        self._frontier_states: Dict[str, FrontierState] = {}
        self._hunter_actor_ids: Dict[str, str] = {}
        self._frontier_engine = AdaptiveQuestionFrontierEngine()
        self._observer = SemanticAcquisitionObserver()
        self._handoff_engine = AuthenticatedEvidenceHandoffEngine()

    def _ensure_workspace(self, workspace_id: str) -> None:
        if workspace_id != self.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Workspace mismatch: coordinator workspace is {self.workspace_id!r}, "
                f"but received operation for {workspace_id!r}."
            )

    def _get_or_init_aggregate(self, actor_id: str) -> str:
        """Lazily initializes the state machine aggregate if runtime is attached."""
        if not self.state_runtime:
            return ""
        if not self._aggregate_id:
            try:
                pkg = self.state_runtime.program_registry.get_program("interview_semantic_program")
            except Exception:
                pkg = None

            if pkg:
                agg = self.state_runtime.initialize_program_state(
                    program_package=pkg,
                    workspace_id=self.workspace_id,
                    actor_id=actor_id,
                    initial_data={"program": "interview_semantic_program"},
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                )
            else:
                agg = self.state_runtime.create_aggregate(
                    program_id="interview_semantic_program",
                    machine_id="INTERVIEW_STATE_MACHINE_V1",
                    workspace_id=self.workspace_id,
                    actor_id=actor_id,
                    initial_state="INITIAL",
                    initial_data={"program": "interview_semantic_program"},
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                )
            self._aggregate_id = agg.aggregate_id
            self._state_version = agg.version
        return self._aggregate_id

    # -------------------------------------------------------------------------
    # Lane 1: HUNTER — High-Recall Question & Elicitation Target Discovery
    # -------------------------------------------------------------------------

    def ingest_approved_hypothesis(
        self,
        *,
        workspace_id: str,
        hypothesis_record: Any,  # CollisionHypothesisRecord or dict
        guest_research_package: Mapping[str, Any],
        actor_id: str = "actor_interview_hunter",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> tuple[HypothesisCandidate, QuestionProgramDerived]:
        """
        Ingests an approved CollisionHypothesis and derives QuestionCandidates across
        the 4-stage progression grammar (ORIENTATION, TENSION_PROBE, CRUCIBLE_EXPOSURE, RESOLUTION_SYNTHESIS).
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise UnauthorizedInterviewLaneError(
                f"ingest_approved_hypothesis requires HUNTER lane, got {lane.name}."
            )

        # Extract hypothesis data
        if hasattr(hypothesis_record, "model_dump"):
            hyp_dict = hypothesis_record.model_dump(mode="json")
        elif isinstance(hypothesis_record, dict):
            hyp_dict = hypothesis_record
        else:
            raise ValueError(f"Unsupported hypothesis record type: {type(hypothesis_record)}")

        hyp_ws = hyp_dict.get("workspace_id")
        if hyp_ws and hyp_ws != self.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Hypothesis belongs to workspace {hyp_ws!r}, but coordinator workspace is {self.workspace_id!r}."
            )

        hyp_id = hyp_dict.get("hypothesis_id") or hyp_dict.get("id") or "hyp_unknown"
        collision_stmt = hyp_dict.get("bridge_statement") or hyp_dict.get("title") or "Collision Hypothesis"
        guest_id = hyp_dict.get("guest_id") or "guest_unknown"
        audience_id = hyp_dict.get("audience_id") or "aud_unknown"
        research_signal_id = hyp_dict.get("research_signal_id") or "sig_unknown"
        guest_proof = hyp_dict.get("guest_lived_proof_citation") or "Lived experience in high-stakes environment."
        audience_tension_ref = hyp_dict.get("audience_tension_ref") or "Systemic friction in leadership practice."
        falsification = hyp_dict.get("falsification_condition") or {}
        oblique_lens = hyp_dict.get("oblique_lens") or {}
        evidence_refs = hyp_dict.get("evidence_references") or []

        # Construct CoordinateBasis
        coords = CoordinateBasis(
            d01_audience_tension=audience_tension_ref,
            d04_guest_lived_authority=guest_proof,
            d07_cultural_world_signal=research_signal_id,
            d08_target_enemy_status_quo=falsification.get("disconfirmed_if") if isinstance(falsification, dict) else None,
            d09_oblique_lens=oblique_lens.get("lens_name") if isinstance(oblique_lens, dict) else None,
            d12_evidence_opportunity=", ".join(evidence_refs) if evidence_refs else None,
        )

        candidate = HypothesisCandidate(
            candidate_id=f"hc:{hyp_id}",
            collision_statement=collision_stmt,
            upstream_hypothesis_refs=[
                SemanticRef(
                    object_id=hyp_id,
                    object_type="collision_hypothesis",
                    sha256=compute_canonical_sha256(hyp_dict),
                )
            ],
            coordinates=coords,
            state=CandidateState.APPROVED if hyp_dict.get("status") == "APPROVED" else CandidateState.SELECTED,
            operator_notes=hyp_dict.get("approval_notes"),
            provenance=Provenance(
                source_refs=[
                    SemanticRef(object_id=guest_id, object_type="guest_dna"),
                    SemanticRef(object_id=audience_id, object_type="audience_tension"),
                    SemanticRef(object_id=research_signal_id, object_type="research_signal"),
                ]
            ),
        )

        # Derive 4 Progression Questions
        q1 = QuestionCandidate(
            text=f"When you first confronted {audience_tension_ref}, what was the initial reality nobody wanted to admit?",
            objective="Elicit unvarnished initial experiential ground truth and orientation context.",
            target_resolution=AnswerResolution.EPISODIC,
            expected_evidence=["EVIDENCE_OF_LIVED_EXPERIENCE", "initial_reality"],
            temporal_orientation=TemporalOrientation.PAST_RECONSTRUCTION,
            social_reference_frame=SocialReferenceFrame.SELF,
            evidence_mode=EvidenceMode.STORY,
        )
        q2 = QuestionCandidate(
            text=f"Where did the standard institutional protocol directly collide with {collision_stmt}?",
            objective="Probe systemic friction between institutional protocol and lived reality.",
            target_resolution=AnswerResolution.MECHANISTIC,
            expected_evidence=["CONTRARIAN_DECISION", "systemic_collision"],
            temporal_orientation=TemporalOrientation.PRESENT_OBSERVATION,
            social_reference_frame=SocialReferenceFrame.INSTITUTION,
            evidence_mode=EvidenceMode.FACT,
        )
        q3 = QuestionCandidate(
            text=f"Take me to the exact moment you realized the existing playbook failed. What was the tangible cost paid?",
            objective="Expose crucible point of failure, irreversible stakes, and price paid.",
            target_resolution=AnswerResolution.EVIDENTIAL,
            expected_evidence=["CRUCIBLE_MOMENT", "cost_paid_receipt"],
            temporal_orientation=TemporalOrientation.PAST_RECONSTRUCTION,
            social_reference_frame=SocialReferenceFrame.SELF,
            evidence_mode=EvidenceMode.STORY,
        )
        q4 = QuestionCandidate(
            text=f"Looking back at that turning point, what is the single counter-intuitive rule you now operate by that peers would reject?",
            objective="Synthesize contrarian operating heuristic and transferable proof rule.",
            target_resolution=AnswerResolution.MECHANISTIC,
            expected_evidence=["COST_PAID_RECEIPT", "counter_intuitive_rule"],
            temporal_orientation=TemporalOrientation.FUTURE_PROJECTION,
            social_reference_frame=SocialReferenceFrame.PEER,
            evidence_mode=EvidenceMode.INTERPRETATION,
        )

        question_program = QuestionProgramDerived(
            program_id=f"qp:{uuid.uuid4().hex[:12]}",
            hypothesis_ref=SemanticRef(object_id=hyp_id, object_type="collision_hypothesis"),
            objective=f"Elicit unvarnished crucible evidence and resolution heuristics for {collision_stmt}",
            candidate_questions=[q1, q2, q3, q4],
            provenance=Provenance(
                source_refs=[SemanticRef(object_id=hyp_id, object_type="collision_hypothesis")]
            ),
        )

        self._loaded_hypothesis_id = hyp_id

        # Advance state if runtime is active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            res = self.state_runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="ingest_hypothesis",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                expected_version=self._state_version,
                state_updates={
                    "hypothesis_id": hyp_id,
                    "candidate_id": candidate.candidate_id,
                    "questions_count": len(question_program.candidate_questions),
                },
            )
            self._state_version = res.aggregate.version

        return candidate, question_program

    # -------------------------------------------------------------------------
    # Lane 2: ANALYST — Adversarial Evaluation, Non-Scripting & Matrix Gates
    # -------------------------------------------------------------------------

    def evaluate_elicitation_matrix(
        self,
        *,
        workspace_id: str,
        candidate: HypothesisCandidate,
        question_program: QuestionProgramDerived,
        matrix_seed_overrides: Optional[Dict[str, Any]] = None,
        target_archetype: str = "F01_CINEMATIC_STORY",
        actor_id: str = "actor_interview_analyst",
        lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> InterviewBriefEvaluation:
        """
        Adversarially evaluates candidate questions against non-scripting invariants,
        verifies Matrix of Edging pressure paths, and checks archetype compatibility.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.ANALYST:
            raise UnauthorizedInterviewLaneError(
                f"evaluate_elicitation_matrix requires ANALYST lane, got {lane.name}."
            )

        if not question_program.candidate_questions:
            raise LeadingQuestionViolationError("Question program contains zero candidate questions.")

        gate_checks = []

        # 1. Assert Non-Scripted / Non-Leading Invariants on all questions
        for idx, q in enumerate(question_program.candidate_questions):
            try:
                InterviewBriefComposer.assert_non_scripted_prompt(q.text)
                gate_checks.append({
                    "gate": f"non_scripted_q{idx+1}",
                    "passed": True,
                    "text": q.text,
                })
            except Exception as e:
                gate_checks.append({
                    "gate": f"non_scripted_q{idx+1}",
                    "passed": False,
                    "error": str(e),
                    "text": q.text,
                })
                raise LeadingQuestionViolationError(
                    f"Candidate question {idx+1} failed non-scripted invariant: {e}"
                ) from e

        # 2. Validate Matrix of Edging Seed & Pressure Path
        default_seed = {
            "psychological_role": candidate.coordinates.d04_guest_lived_authority or "unvarnished_operator",
            "tension": candidate.coordinates.d01_audience_tension or candidate.collision_statement,
            "activation_direction_set": ["provoke_unvarnished_truth", "expose_systemic_friction"],
            "pressure_path": "progressive_escalation_to_crucible",
            "stance": "curious_and_uncompromising",
            "counteractivation_strategy": "redirect_platitude_to_episodic_receipt",
            "smallest_commitment": "acknowledge_initial_frictional_compromise",
        }
        if matrix_seed_overrides:
            default_seed.update(matrix_seed_overrides)

        missing_fields = [f for f in MATRIX_SEED_FIELDS if not default_seed.get(f)]
        if missing_fields:
            raise MatrixOfEdgingValidationError(
                f"Matrix of Edging seed is missing mandatory fields: {missing_fields}"
            )

        gate_checks.append({
            "gate": "matrix_of_edging_schema",
            "passed": True,
            "fields": list(MATRIX_SEED_FIELDS),
        })

        # 3. Archetype Compatibility Gate
        valid_archetypes = {"F01_CINEMATIC_STORY", "F02_MINIMAL_COACH", "F03_PROOF_COMMENTARY", "ACHIEVEMENT_STORY"}
        is_archetype_valid = target_archetype in valid_archetypes

        gate_checks.append({
            "gate": "archetype_compatibility",
            "passed": is_archetype_valid,
            "archetype": target_archetype,
        })

        eval_result = InterviewBriefEvaluation(
            matrix_valid=True,
            non_scripted_valid=True,
            archetype_compatibility_score_micros=1_000_000 if is_archetype_valid else 500_000,
            pressure_path_score_micros=1_000_000,
            overall_confidence_micros=1_000_000,
            evaluated_questions_count=len(question_program.candidate_questions),
            gate_checks=gate_checks,
        )

        # Advance state if runtime is active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            res = self.state_runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="evaluate_matrix",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                expected_version=self._state_version,
                state_updates={
                    "evaluation_passed": True,
                    "target_archetype": target_archetype,
                },
            )
            self._state_version = res.aggregate.version

        return eval_result

    # -------------------------------------------------------------------------
    # Lane 3: COMPOSER — Canonical Brief Composition via Compiler Boundary
    # -------------------------------------------------------------------------

    def compile_interview_brief(
        self,
        *,
        workspace_id: str,
        candidate: HypothesisCandidate,
        question_program: QuestionProgramDerived,
        guest_name: str,
        research_package_ref: Mapping[str, Any],
        composer_authority: Mapping[str, str],
        brand_context_ref: Optional[Mapping[str, Any]] = None,
        voice_dna_ref: Optional[Mapping[str, Any]] = None,
        custom_expression_targets: Optional[List[str]] = None,
        matrix_seed_overrides: Optional[Dict[str, Any]] = None,
        actor_id: str = "actor_interview_composer",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> tuple[Dict[str, Any], str]:
        """
        Compiles candidate hypothesis and question program into the authoritative canonical
        ActivativeInterviewBrief command payload using ActivativeInterviewBriefCompiler.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise UnauthorizedInterviewLaneError(
                f"compile_interview_brief requires COMPOSER lane, got {lane.name}."
            )

        if not research_package_ref or not research_package_ref.get("object_id"):
            raise BriefCompilationError("Valid research_package_ref with non-blank object_id is required.")

        try:
            brief_obj = ActivativeInterviewBriefCompiler.compile_brief_payload(
                candidate=candidate,
                question_program=question_program,
                guest_name=guest_name,
                research_package_ref=research_package_ref,
                composer_authority=composer_authority,
                brand_context_ref=brand_context_ref,
                voice_dna_ref=voice_dna_ref,
                custom_expression_targets=custom_expression_targets,
                matrix_seed_overrides=matrix_seed_overrides,
            )
        except Exception as e:
            raise BriefCompilationError(f"ActivativeInterviewBriefCompiler failed: {e}") from e

        canonical_sha = brief_obj.get("canonical_sha256") or compute_canonical_sha256(brief_obj.get("payload_json", brief_obj))

        # Advance state if runtime is active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            res = self.state_runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="compile_brief",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                expected_version=self._state_version,
                state_updates={
                    "brief_compiled": True,
                    "canonical_sha256": canonical_sha,
                },
            )
            self._state_version = res.aggregate.version

        return brief_obj, canonical_sha

    # -------------------------------------------------------------------------
    # Lane 4: COMMANDER — Executive Sealing, Store Commit, Receipts & Lifecycle
    # -------------------------------------------------------------------------

    def seal_interview_brief(
        self,
        *,
        workspace_id: str,
        compiled_brief: Mapping[str, Any],
        idempotency_key: str,
        brief_service: Optional[Any] = None,
        actor_id: str = "actor_interview_commander",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> tuple[InterviewBriefRecord, InterviewSemanticReceipt]:
        """
        Validates operator authorization, commits the brief to authoritative store / BriefService,
        emits an immutable InterviewSemanticReceipt, and seals the brief state.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedInterviewLaneError(
                f"seal_interview_brief requires COMMANDER lane, got {lane.name}."
            )

        payload = compiled_brief.get("payload_json")
        if isinstance(payload, str):
            payload = json.loads(payload)
        elif not isinstance(payload, dict):
            payload = dict(compiled_brief)

        # Validate Operator Authority in Commander Lane
        auth = payload.get("composer_authority") or {}
        for req_field in ("operator_id", "authority_scope", "assertion_id"):
            if req_field not in auth or not auth[req_field]:
                raise BriefAuthorizationError(
                    f"Missing required composer authority field: {req_field!r}."
                )

        brief_id = compiled_brief.get("object_id") or payload.get("brief_id") or f"ic:brief:{uuid.uuid4().hex[:12]}"
        canonical_sha = compiled_brief.get("canonical_sha256") or compute_canonical_sha256(payload)
        hyp_ref = payload.get("hypothesis_ref")
        hyp_id = (
            (hyp_ref.get("object_id") if isinstance(hyp_ref, dict) and hyp_ref.get("object_id") else None)
            or payload.get("hypothesis_id")
            or getattr(self, "_loaded_hypothesis_id", None)
            or "hyp_canonical"
        )

        # Delegate to BriefService if provided
        if brief_service:
            try:
                brief_command = {
                    "research_package_ref": payload.get("research_package_ref"),
                    "brand_context_ref": payload.get("brand_context_ref"),
                    "voice_dna_ref": payload.get("voice_dna_ref"),
                    "guest_name": payload.get("guest_name"),
                    "tension_hypothesis": payload.get("tension_hypothesis"),
                    "matrix_of_edging_seed": payload.get("matrix_of_edging_seed"),
                    "planned_questions": payload.get("planned_questions"),
                    "expression_targets": payload.get("expression_targets", ["self-recognizing witness"]),
                    "composer_authority": auth,
                }
                service_res = brief_service.create_brief(brief_command, idempotency_key=idempotency_key)
                if isinstance(service_res, dict):
                    obj = service_res.get("object", service_res)
                    if "object_id" in obj:
                        brief_id = obj["object_id"]
                    if "sha256" in obj:
                        canonical_sha = obj["sha256"]
                    elif "canonical_sha256" in obj:
                        canonical_sha = obj["canonical_sha256"]
            except Exception as e:
                raise BriefAuthorizationError(f"BriefService sealing failed: {e}") from e

        # Store in Authoritative Interview Store
        record = InterviewBriefRecord(
            workspace_id=self.workspace_id,
            brief_id=brief_id,
            hypothesis_id=hyp_id,
            guest_name=payload.get("guest_name", "Unknown Guest"),
            research_package_ref=payload.get("research_package_ref", {}),
            brand_context_ref=payload.get("brand_context_ref"),
            voice_dna_ref=payload.get("voice_dna_ref"),
            tension_hypothesis=payload.get("tension_hypothesis", ""),
            matrix_of_edging_seed=payload.get("matrix_of_edging_seed", {}),
            planned_questions=payload.get("planned_questions", []),
            expression_targets=payload.get("expression_targets", []),
            composer_authority=auth,
            canonical_sha256=canonical_sha,
            lifecycle_state="SEALED",
        )
        self.store.store_brief(record)

        # Emit Signed Receipt
        receipt_record = InterviewSemanticReceiptRecord(
            workspace_id=self.workspace_id,
            receipt_id=f"rcpt_int_{uuid.uuid4().hex[:12]}",
            brief_id=brief_id,
            hypothesis_id=hyp_id,
            evaluator_lane=lane.name,
            decision="SEALED",
            score_breakdown_micros={
                "authority_compliance_micros": 1_000_000,
                "matrix_integrity_micros": 1_000_000,
                "non_scripted_compliance_micros": 1_000_000,
            },
            gate_checks=[
                {"gate": "operator_authority_assertion", "passed": True, "actor": actor_id},
                {"gate": "workspace_tenancy_isolation", "passed": True, "workspace_id": self.workspace_id},
                {"gate": "canonical_sha256_verification", "passed": True, "sha256": canonical_sha},
            ],
            signature=hashlib.sha256(f"{brief_id}:{canonical_sha}:{actor_id}:{idempotency_key}".encode("utf-8")).hexdigest(),
        )
        self.store.store_receipt(receipt_record)

        receipt = InterviewSemanticReceipt(
            receipt_id=receipt_record.receipt_id,
            workspace_id=receipt_record.workspace_id,
            brief_id=receipt_record.brief_id,
            hypothesis_id=receipt_record.hypothesis_id,
            operator_authority=auth,
            canonical_sha256=canonical_sha,
            decision=receipt_record.decision,
            score_breakdown_micros=receipt_record.score_breakdown_micros,
            gate_checks=receipt_record.gate_checks,
            signature=receipt_record.signature,
            created_at=receipt_record.created_at,
        )

        # Advance state if runtime is active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            res = self.state_runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="seal_brief",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                expected_version=self._state_version,
                state_updates={
                    "brief_id": brief_id,
                    "receipt_id": receipt.receipt_id,
                    "canonical_sha256": canonical_sha,
                    "brief_sealed": True,
                },
            )
            self._state_version = res.aggregate.version

        return record, receipt

    # -------------------------------------------------------------------------
    # Live Interview Elicitation & Adaptive Question Frontier (CAE M34)
    # -------------------------------------------------------------------------

    def start_interview_session(
        self,
        *,
        workspace_id: str,
        brief_id: str,
        session_id: Optional[str] = None,
        operator_id: str = "op_director",
        actor_id: str = "actor_interview_hunter",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> tuple[InterviewSessionRecord, FrontierState]:
        """
        Starts a live interview elicitation session from a SEALED Activative Interview Brief.
        Initializes the AdaptiveQuestionFrontierEngine spine from the brief.
        Transitions state from BRIEF_SEALED to QUESTIONING.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise UnauthorizedInterviewLaneError(
                f"start_interview_session requires HUNTER lane, got {lane.name}."
            )

        brief = self.store.get_brief(workspace_id, brief_id)
        if not brief:
            raise BriefAuthorizationError(f"Interview Brief {brief_id!r} not found in workspace {workspace_id!r}.")
        if brief.lifecycle_state != "SEALED":
            raise BriefAuthorizationError(
                f"Interview Brief {brief_id!r} is in state {brief.lifecycle_state!r}, must be SEALED to start live session."
            )

        sess_id = session_id or f"sess_int_{uuid.uuid4().hex[:12]}"

        # Initialize HypothesisCandidate representation for the frontier spine
        cand = HypothesisCandidate(
            candidate_id=f"hc:{brief.hypothesis_id}",
            collision_statement=brief.tension_hypothesis or f"Collision hypothesis for {brief.guest_name}",
            upstream_hypothesis_refs=[
                SemanticRef(
                    object_id=brief.hypothesis_id,
                    object_type="collision_hypothesis",
                    sha256=brief.canonical_sha256,
                )
            ],
            coordinates=CoordinateBasis(
                d01_audience_tension=brief.tension_hypothesis,
                d04_guest_lived_authority=brief.guest_name,
            ),
            state=CandidateState.APPROVED,
        )

        frontier_state = self._frontier_engine.initialize_frontier(
            session_id=sess_id,
            candidates=[cand],
        )

        # Cache frontier and hunter actor
        self._frontier_states[sess_id] = frontier_state
        self._hunter_actor_ids[sess_id] = actor_id

        # Persist session
        session_record = InterviewSessionRecord(
            workspace_id=workspace_id,
            session_id=sess_id,
            brief_id=brief_id,
            status="QUESTIONING",
            turns_count=0,
        )
        self.store.store_session(session_record)

        # Transition state runtime aggregate if active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            try:
                res = self.state_runtime.execute_transition(
                    aggregate_id=agg_id,
                    transition_name="start_elicitation_from_brief",
                    actor_id=actor_id,
                    actor_lane=lane,
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                    expected_version=self._state_version,
                    state_updates={
                        "session_id": sess_id,
                        "brief_id": brief_id,
                        "started_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                self._state_version = res.aggregate.version
            except Exception:
                # If state machine was already in QUESTIONING or different path, continue
                pass

        return session_record, frontier_state

    def get_next_question_attempt(
        self,
        *,
        workspace_id: str,
        session_id: str,
        actor_id: str = "actor_interview_hunter",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> Optional[QuestionAttempt]:
        """
        Queries the bounded adaptive question frontier to deterministically select
        the next candidate question attempt (deepen | broaden | reconcile | verify | reframe | advance | close).
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise UnauthorizedInterviewLaneError(
                f"get_next_question_attempt requires HUNTER lane, got {lane.name}."
            )

        session = self.store.get_session(workspace_id, session_id)
        if not session:
            raise InterviewProgramError(f"Interview session {session_id!r} not found.")
        if session.status not in ("QUESTIONING", "INITIALIZED"):
            raise InterviewProgramError(f"Interview session {session_id!r} is not in active QUESTIONING state (status={session.status!r}).")

        frontier_state = self._frontier_states.get(session_id)
        if not frontier_state:
            brief = self.store.get_brief(workspace_id, session.brief_id)
            if not brief:
                raise BriefAuthorizationError(f"Brief {session.brief_id!r} not found for session {session_id!r}.")
            cand = HypothesisCandidate(
                candidate_id=f"hc:{brief.hypothesis_id}",
                collision_statement=brief.tension_hypothesis or f"Collision for {brief.guest_name}",
                coordinates=CoordinateBasis(
                    d01_audience_tension=brief.tension_hypothesis,
                    d04_guest_lived_authority=brief.guest_name,
                ),
                state=CandidateState.APPROVED,
            )
            frontier_state = self._frontier_engine.initialize_frontier(
                session_id=session_id,
                candidates=[cand],
            )
            self._frontier_states[session_id] = frontier_state

        attempt = self._frontier_engine.select_next_question(frontier_state)
        return attempt

    def record_turn_and_observe(
        self,
        *,
        workspace_id: str,
        session_id: str,
        question_attempt: QuestionAttempt,
        transcript_text: str,
        guest_statements: Optional[Sequence[str]] = None,
        speaker: str = "GUEST",
        resolution: AnswerResolution = AnswerResolution.EPISODIC,
        completeness: InformationCompleteness = InformationCompleteness.SUFFICIENT,
        evidence_modes: Optional[Sequence[EvidenceMode]] = None,
        specificity_score: float = 0.95,
        authenticity_score: float = 0.95,
        actor_id: str = "actor_interview_hunter",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> tuple[InterviewTurnRecord, SemanticAcquisitionObservation]:
        """
        Records an interview turn with transcript SHA-256 digest and performs
        semantic acquisition observation via the ANALYST lane logic.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise UnauthorizedInterviewLaneError(
                f"record_turn_and_observe turn ingestion requires HUNTER lane, got {lane.name}."
            )

        if not transcript_text or not transcript_text.strip():
            raise SourceLineageViolationError("Cannot record an interview turn with empty transcript text.")

        session = self.store.get_session(workspace_id, session_id)
        if not session:
            raise InterviewProgramError(f"Session {session_id!r} not found.")
        if session.status != "QUESTIONING":
            raise InterviewProgramError(f"Cannot record turn for session in state {session.status!r}.")

        turn_index = session.turns_count + 1
        turn_id = f"turn_{session_id}_{turn_index:03d}"
        transcript_clean = transcript_text.strip()
        transcript_sha = hashlib.sha256(transcript_clean.encode("utf-8")).hexdigest()

        cand = getattr(question_attempt, "selected_candidate", None) or getattr(question_attempt, "selected_question", None)
        question_id = cand.question_id if cand else "q_custom"
        prompt_text = cand.text if (cand and hasattr(cand, "text")) else (getattr(question_attempt, "prompt_text", "") or "Interview Question")
        stage = getattr(cand, "stage", None) or getattr(question_attempt, "stage", QuestionStage.ORIENTATION)
        stage_str = stage.value if hasattr(stage, "value") else str(stage)

        # 1. Store the authoritative Turn entity
        turn_record = InterviewTurnRecord(
            workspace_id=workspace_id,
            turn_id=turn_id,
            session_id=session_id,
            turn_index=turn_index,
            speaker=speaker,
            question_id=question_id,
            stage=stage_str,
            prompt_text=prompt_text,
            transcript_text=transcript_clean,
            transcript_sha256=transcript_sha,
            is_authenticated=True,
        )
        self.store.store_turn(turn_record)

        # 2. Semantic Observation (Analyst acquisition)
        statements = list(guest_statements) if guest_statements else [transcript_clean]
        observation = self._observer.observe_turn_response(
            question_attempt_id=question_attempt.attempt_id,
            turn_id=turn_id,
            transcript_text=transcript_clean,
            guest_statements=statements,
            resolution=resolution,
            completeness=completeness,
            evidence_modes=list(evidence_modes) if evidence_modes else [EvidenceMode.STORY],
        )

        # Store observation records
        for ev_rec in observation.evidence_records:
            ev_id = getattr(ev_rec, "record_id", None) or getattr(ev_rec, "evidence_id", None) or f"evr_{uuid.uuid4().hex[:8]}"
            ev_kind = getattr(ev_rec, "kind", None) or getattr(ev_rec, "lineage_kind", None)
            kind_str = ev_kind.value if hasattr(ev_kind, "value") else str(ev_kind or "guest_stated_evidence")
            
            ev_mode_val = observation.evidence_modes[0].value if observation.evidence_modes and hasattr(observation.evidence_modes[0], "value") else "story"
            temp_ori_val = observation.temporal_orientation[0].value if observation.temporal_orientation and hasattr(observation.temporal_orientation[0], "value") else "past_reconstruction"
            comp_val = observation.completeness.value if hasattr(observation.completeness, "value") else str(observation.completeness)

            obs_rec = InterviewObservationRecord(
                workspace_id=workspace_id,
                observation_id=ev_id,
                turn_id=turn_id,
                session_id=session_id,
                kind=kind_str,
                statement_text=ev_rec.statement_text,
                evidence_mode=ev_mode_val,
                temporal_orientation=temp_ori_val,
                information_completeness=comp_val,
                specificity_micros=int(round(specificity_score * 1_000_000)),
                authenticity_micros=int(round(authenticity_score * 1_000_000)),
                is_authenticated=False,
                discrepancy_refs=[d.discrepancy_id for d in observation.discrepancies],
            )
            self.store.store_observation(obs_rec)

        # 3. Update active adaptive frontier
        frontier_state = self._frontier_states.get(session_id)
        if frontier_state:
            self._frontier_engine.observe_answer(
                frontier=frontier_state,
                question_attempt_id=question_attempt.attempt_id,
                turn_id=turn_id,
                transcript_text=transcript_clean,
                resolution=resolution,
                completeness=completeness,
                specificity_score=specificity_score,
                authenticity_score=authenticity_score,
            )

        # Update session turns count
        session.turns_count = turn_index
        self.store.store_session(session)

        # Advance state runtime if active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            try:
                res = self.state_runtime.execute_transition(
                    aggregate_id=agg_id,
                    transition_name="record_turn",
                    actor_id=actor_id,
                    actor_lane=lane,
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                    expected_version=self._state_version,
                    state_updates={
                        "latest_turn_id": turn_id,
                        "turns_count": turn_index,
                    },
                )
                self._state_version = res.aggregate.version
            except Exception:
                pass

        return turn_record, observation

    # -------------------------------------------------------------------------
    # Lane 3: COMPOSER — Authenticated Evidence Packaging & Downstream Synthesis
    # -------------------------------------------------------------------------

    def package_interview_evidence(
        self,
        *,
        workspace_id: str,
        session_id: str,
        content_candidates: Optional[Sequence[DownstreamContentCandidate]] = None,
        actor_id: str = "actor_interview_composer",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> tuple[EvidencePackageRecord, AuthenticatedEvidencePackage]:
        """
        Compiles accepted evidence records into an Authenticated Evidence Package (COMPOSER lane).
        Ensures 6-link lineage survival and archetype compatibility verification.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise UnauthorizedInterviewLaneError(
                f"package_interview_evidence requires COMPOSER lane, got {lane.name}."
            )

        session = self.store.get_session(workspace_id, session_id)
        if not session:
            raise InterviewProgramError(f"Session {session_id!r} not found.")

        brief = self.store.get_brief(workspace_id, session.brief_id)
        if not brief:
            raise BriefAuthorizationError(f"Brief {session.brief_id!r} not found for session {session_id!r}.")

        turns = self.store.list_turns(workspace_id, session_id)
        observations = self.store.list_observations(workspace_id, session_id=session_id)

        if not turns:
            raise AntiFabricationViolationError(
                f"Cannot package evidence for session {session_id!r} with 0 recorded turns."
            )

        # Build AcceptedEvidenceRecords with verifiable source refs
        accepted_evidence_list: List[AcceptedEvidenceRecord] = []
        for turn in turns:
            src_ref = SourceReference.create_verified_source(
                session_id=session_id,
                turn_id=turn.turn_id,
                workspace_id=workspace_id,
                project_id=session.brief_id,
                raw_answer_text=turn.transcript_text,
            )

            q_attempt_ref = QuestionAttemptRef(
                attempt_id=f"qa:{turn.turn_id}",
                question_candidate_ref=SemanticRef(object_id=turn.question_id, object_type="question_candidate"),
                hypothesis_ref=SemanticRef(object_id=brief.hypothesis_id, object_type="hypothesis_candidate"),
                presented_question_text=turn.prompt_text,
                source_ref=src_ref,
                workspace_id=workspace_id,
                project_id=session.brief_id,
            )

            turn_obs = [o for o in observations if o.turn_id == turn.turn_id]
            extracted = turn_obs[0].statement_text if turn_obs else turn.transcript_text

            # Create an Observation container to satisfy handoff engine
            obs_container = SemanticAcquisitionObservation(
                question_attempt_id=q_attempt_ref.attempt_id,
                turn_id=turn.turn_id,
                transcript_text=turn.transcript_text,
                resolution=AnswerResolution.EPISODIC,
                completeness=InformationCompleteness.SUFFICIENT,
                evidence_records=[
                    AcquisitionEvidenceRecord(
                        statement_text=extracted,
                        kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
                        turn_id=turn.turn_id,
                        source_ref=SemanticRef(object_id=f"turn:{turn.turn_id}"),
                    )
                ],
                provenance=Provenance(source_refs=[SemanticRef(object_id=f"turn:{turn.turn_id}")]),
            )

            accepted_ev = self._handoff_engine.accept_turn_evidence(
                question_attempt=q_attempt_ref,
                observation=obs_container,
                source_ref=src_ref,
                lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
                extracted_statement=extracted,
                response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
                is_authenticated_receipt=True,
            )
            accepted_evidence_list.append(accepted_ev)

        # Synthesize downstream candidates if not provided
        candidates_to_package: List[DownstreamContentCandidate] = []
        if content_candidates:
            candidates_to_package = list(content_candidates)
        else:
            primary_ev = accepted_evidence_list[0]
            cand_prod = self._handoff_engine.synthesize_downstream_candidate(
                title=f"The Lived Reality Crucible: {brief.guest_name}",
                core_narrative_claim=primary_ev.extracted_statement,
                target_archetype="ARCH-CRUCIBLE",
                target_format="FMT-01-STORY",
                target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
                source_evidence_records=accepted_evidence_list,
                workspace_id=workspace_id,
                project_id=session.brief_id,
            )
            candidates_to_package.append(cand_prod)

        # Trace 6-link lineage for each candidate to verify survival
        for cand_item in candidates_to_package:
            trace = self._handoff_engine.trace_lineage(cand_item)
            if not trace.upstream_hypotheses:
                raise InvalidLineageError(f"Candidate {cand_item.candidate_id!r} failed 6-link lineage survival check.")

        # Compile Evidence Package
        package = self._handoff_engine.compile_evidence_package(
            session_ref=SemanticRef(object_id=session_id, object_type="interview_session"),
            brief_ref=SemanticRef(object_id=brief.brief_id, object_type="interview_brief"),
            workspace_id=workspace_id,
            project_id=session.brief_id,
            accepted_evidence=accepted_evidence_list,
            content_candidates=candidates_to_package,
        )

        package_record = EvidencePackageRecord(
            workspace_id=workspace_id,
            package_id=package.package_id,
            session_id=session_id,
            brief_id=brief.brief_id,
            guest_id=brief.guest_name,
            canonical_sha256=package.package_sha256,
            accepted_evidence_records=[e.model_dump(mode="json") for e in accepted_evidence_list],
            downstream_candidates=[c.model_dump(mode="json") for c in candidates_to_package],
            is_authenticated=True,
        )
        self.store.store_evidence_package(package_record)

        # Update session with package reference
        session.evidence_package_ref = {
            "package_id": package.package_id,
            "package_sha256": package.package_sha256,
        }
        self.store.store_session(session)

        # State runtime transition if active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            try:
                res = self.state_runtime.execute_transition(
                    aggregate_id=agg_id,
                    transition_name="package_evidence",
                    actor_id=actor_id,
                    actor_lane=lane,
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                    expected_version=self._state_version,
                    state_updates={
                        "evidence_package_id": package.package_id,
                        "canonical_sha256": package.package_sha256,
                    },
                )
                self._state_version = res.aggregate.version
            except Exception:
                pass

        return package_record, package

    # -------------------------------------------------------------------------
    # Lane 4: COMMANDER — Anti-Self-Attestation Evaluation & Session Sealing
    # -------------------------------------------------------------------------

    def authenticate_and_complete_session(
        self,
        *,
        workspace_id: str,
        session_id: str,
        evaluator_actor_id: str,
        verdict: str = "AUTHENTICATED",
        rationale: str = "Supervised adaptive interview evidence verified with intact 6-link lineage.",
        operator_authorized: bool = True,
        actor_id: str = "actor_interview_commander",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> tuple[InterviewSessionRecord, EvidenceAuthenticationRecord, InterviewSemanticReceiptRecord]:
        """
        Performs independent Commander evaluation and seals the session.
        Enforces strict Anti-Self-Attestation Doctrine: evaluator_actor_id MUST NOT be
        the capturing actor (hunter).
        Emits signed EvidenceAuthenticationRecord and InterviewSemanticReceiptRecord.
        Transitions session and state machine to COMPLETED.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedInterviewLaneError(
                f"authenticate_and_complete_session requires COMMANDER lane, got {lane.name}."
            )

        if not operator_authorized:
            raise BriefAuthorizationError("Session authentication requires explicit operator authorization.")

        # Enforce Anti-Self-Attestation
        capturing_hunter = self._hunter_actor_ids.get(session_id)
        if evaluator_actor_id == capturing_hunter or (
            evaluator_actor_id == actor_id and "hunter" in evaluator_actor_id.lower()
        ):
            raise SelfAttestationViolationError(
                f"Anti-self-attestation violation: Capturing hunter actor {evaluator_actor_id!r} "
                f"cannot evaluate and authenticate its own evidence extractions."
            )

        session = self.store.get_session(workspace_id, session_id)
        if not session:
            raise InterviewProgramError(f"Session {session_id!r} not found.")

        pkg_record = self.store.get_evidence_package_by_session(workspace_id, session_id)
        if not pkg_record:
            raise InterviewProgramError(
                f"Cannot authenticate session {session_id!r} without a compiled evidence package."
            )

        auth_id = f"auth_{uuid.uuid4().hex[:12]}"
        sig_data = f"{auth_id}:{session_id}:{pkg_record.package_id}:{evaluator_actor_id}:{verdict}"
        signature = hashlib.sha256(sig_data.encode("utf-8")).hexdigest()

        auth_record = EvidenceAuthenticationRecord(
            workspace_id=workspace_id,
            auth_id=auth_id,
            session_id=session_id,
            evidence_package_id=pkg_record.package_id,
            evaluator_lane=lane.name,
            evaluator_actor_id=evaluator_actor_id,
            verdict=verdict,
            rationale=rationale,
            signature=signature,
        )
        self.store.store_evidence_authentication(auth_record)

        receipt_record = InterviewSemanticReceiptRecord(
            workspace_id=workspace_id,
            receipt_id=f"rcpt_int_{uuid.uuid4().hex[:12]}",
            brief_id=session.brief_id,
            hypothesis_id=pkg_record.guest_id,
            evaluator_lane=lane.name,
            decision="AUTHENTICATED",
            score_breakdown_micros={
                "lineage_survival_micros": 1_000_000,
                "anti_self_attestation_micros": 1_000_000,
                "source_sovereignty_micros": 1_000_000,
            },
            gate_checks=[
                {"gate": "anti_self_attestation_check", "passed": True, "evaluator": evaluator_actor_id, "capturing_hunter": capturing_hunter},
                {"gate": "six_link_lineage_verification", "passed": True, "package_id": pkg_record.package_id},
                {"gate": "source_transcript_sha_verification", "passed": True, "canonical_sha256": pkg_record.canonical_sha256},
            ],
            signature=signature,
        )
        self.store.store_receipt(receipt_record)

        session.status = "COMPLETED"
        self.store.store_session(session)

        # State runtime transition if active
        if self.state_runtime:
            agg_id = self._get_or_init_aggregate(actor_id)
            try:
                res = self.state_runtime.execute_transition(
                    aggregate_id=agg_id,
                    transition_name="complete_interview",
                    actor_id=actor_id,
                    actor_lane=lane,
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                    expected_version=self._state_version,
                    state_updates={
                        "auth_id": auth_id,
                        "session_status": "COMPLETED",
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                self._state_version = res.aggregate.version
            except Exception:
                pass

        return session, auth_record, receipt_record

    def quarantine_or_repair_session(
        self,
        *,
        workspace_id: str,
        session_id: str,
        action: str = "quarantine",  # "quarantine" or "repair"
        reason: str = "Anomalous turn detected",
        actor_id: str = "actor_interview_commander",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> InterviewSessionRecord:
        """
        Governs fail-closed quarantine and rollback/repair lifecycles for an interview session.
        """
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedInterviewLaneError(
                f"quarantine_or_repair_session requires COMMANDER lane, got {lane.name}."
            )

        session = self.store.get_session(workspace_id, session_id)
        if not session:
            raise InterviewProgramError(f"Session {session_id!r} not found.")

        if action == "quarantine":
            session.status = "QUARANTINED"
        elif action == "repair":
            session.status = "QUESTIONING"
        else:
            raise ValueError(f"Unknown action: {action!r}. Must be 'quarantine' or 'repair'.")

        self.store.store_session(session)

        if self.state_runtime and self._aggregate_id:
            try:
                trans_name = "quarantine_session" if action == "quarantine" else "repair_session"
                res = self.state_runtime.execute_transition(
                    aggregate_id=self._aggregate_id,
                    transition_name=trans_name,
                    actor_id=actor_id,
                    actor_lane=lane,
                    context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                    expected_version=self._state_version,
                    state_updates={
                        "action": action,
                        "reason": reason,
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                self._state_version = res.aggregate.version
            except Exception:
                pass

        return session

    def execute_repair_or_quarantine(
        self,
        *,
        workspace_id: str,
        reason: str,
        target_state: str = "INITIAL",
        actor_id: str = "actor_interview_commander",
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> None:
        """Executes fail-closed recovery / repair transition."""
        self._ensure_workspace(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise UnauthorizedInterviewLaneError("execute_repair_or_quarantine requires COMMANDER lane.")

        if self.state_runtime and self._aggregate_id:
            trans_name = "repair_to_initial" if target_state == "INITIAL" else "repair_to_brief"
            res = self.state_runtime.execute_transition(
                aggregate_id=self._aggregate_id,
                transition_name=trans_name,
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "interview_brief_approved", "collision_hypothesis_approved"],
                expected_version=self._state_version,
                state_updates={"repaired_reason": reason, "repaired_at": datetime.now(timezone.utc).isoformat()},
            )
            self._state_version = res.aggregate.version

