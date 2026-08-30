"""
question_resolver.py
--------------------
Derived question objective, mechanism coalition, and Question IR resolver (CAE-M03).

Implements the resolution chain:
  selected hypothesis -> question objective -> evidence requirement
    -> candidate mechanism coalition -> derived Question IR -> natural-language candidates

This module operates strictly on derived/in-memory structures and provisional mechanism
registries without promoting unaudited primitives to canonical ontology or writing to external stores.
"""

from __future__ import annotations

import copy
import hashlib
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, field_validator

from .hypothesis_adapter import (
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)


class AnswerResolution(str, Enum):
    ABSTRACT = "abstract"
    GENERAL = "general"
    SPECIFIC = "specific"
    EPISODIC = "episodic"
    MECHANISTIC = "mechanistic"
    EVIDENTIAL = "evidential"


class InformationCompleteness(str, Enum):
    UNKNOWN = "unknown"
    PARTIAL = "partial"
    SUFFICIENT = "sufficient"
    VERIFIED = "verified"
    EXHAUSTED = "exhausted"


class InquiryStateTransition(str, Enum):
    STABILIZE = "stabilize"
    SWITCH = "switch"
    EXPAND = "expand"
    CLARIFY = "clarify"
    REDISTRIBUTE_AGENCY = "redistribute_agency"
    CLOSE = "close"


class EvidenceMode(str, Enum):
    FACT = "fact"
    STORY = "story"
    FEELING = "feeling"
    INTERPRETATION = "interpretation"
    FORECAST = "forecast"
    ALTERNATIVE = "alternative"
    COUNTERFACTUAL = "counterfactual"


class TemporalOrientation(str, Enum):
    PAST_RECONSTRUCTION = "past_reconstruction"
    PRESENT_OBSERVATION = "present_observation"
    FUTURE_PROJECTION = "future_projection"
    COUNTERFACTUAL = "counterfactual"
    PREMORTEM = "premortem"
    HISTORICAL_UNCERTAINTY = "historical_uncertainty"


class SocialReferenceFrame(str, Enum):
    SELF = "self"
    PEER = "peer"
    AUTHORITY = "authority"
    GROUP = "group"
    INSTITUTION = "institution"
    AUDIENCE = "audience"


class MechanismDisposition(str, Enum):
    PROMOTION_CANDIDATE = "PROMOTION_CANDIDATE"
    MERGE_CANDIDATE = "MERGE_CANDIDATE"
    RESEARCH_MORE = "RESEARCH_MORE"


class ProvisionalMechanism(BaseModel):
    """
    Provisional, non-canonical mechanism definition admitted by Question Intelligence Synthesis.
    Cannot be marked canonical until an independent audit and promotion decision occurs.
    """
    mechanism_id: str = Field(..., description="Stable mechanism cluster ID, e.g. QI-C01")
    name: str = Field(...)
    family: str = Field(...)
    primary_transformation: str = Field(...)
    runtime_trigger: str = Field(...)
    disposition: MechanismDisposition = Field(...)
    is_canonical: bool = Field(False, description="Strictly False for all provisional mechanisms")
    source_lineage: List[str] = Field(default_factory=list)
    forbidden_failure_patterns: List[str] = Field(default_factory=list)

    @field_validator("is_canonical")
    @classmethod
    def enforce_non_canonical(cls, v: bool) -> bool:
        if v:
            raise ValueError(
                "Provisional mechanisms cannot be marked canonical without independent promotion authority (M03 Boundary Violation)."
            )
        return False


# In-Memory Catalog of Admitted Provisional Mechanisms from Synthesis §2
APPROVED_PROVISIONAL_MECHANISMS: Dict[str, ProvisionalMechanism] = {
    "QI-C01": ProvisionalMechanism(
        mechanism_id="QI-C01",
        name="Answer Resolution Escalation",
        family="Resolution Control",
        primary_transformation="abstract/general -> specific/episodic/mechanistic/evidential",
        runtime_trigger="low_resolution_answer",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:telling_true_stories", "book:the_art_of_inquiry"],
        forbidden_failure_patterns=["accepting_generic_platitude", "unanchored_abstraction"],
    ),
    "QI-C02": ProvisionalMechanism(
        mechanism_id="QI-C02",
        name="Second-Question State Routing",
        family="State Routing",
        primary_transformation="answer -> information gap -> next move",
        runtime_trigger="every_answer",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:the_mom_test", "book:good_questions"],
        forbidden_failure_patterns=["ignoring_guest_observation", "rigid_script_progression"],
    ),
    "QI-C03": ProvisionalMechanism(
        mechanism_id="QI-C03",
        name="Prepared Spine / Adaptive Branch",
        family="Execution Architecture",
        primary_transformation="fixed coverage + bounded adaptation",
        runtime_trigger="live_state",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:creative_interviews", "book:power_of_inquiry"],
        forbidden_failure_patterns=["unbounded_drift", "abandoning_core_hypothesis"],
    ),
    "QI-C04": ProvisionalMechanism(
        mechanism_id="QI-C04",
        name="Descriptive-Before-Explanatory",
        family="Chronology & Detail",
        primary_transformation="explanation-first -> lived event/detail first",
        runtime_trigger="abstract_account",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:creative_nonfiction", "book:crucial_conversations"],
        forbidden_failure_patterns=["premature_theory_theorizing", "leading_the_witness"],
    ),
    "QI-C05": ProvisionalMechanism(
        mechanism_id="QI-C05",
        name="Interpret-and-Return",
        family="Corrigible Inquiry",
        primary_transformation="system inference -> Guest confirmation/correction",
        runtime_trigger="interpretation_formed",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:active_listening", "book:expert_interrogation"],
        forbidden_failure_patterns=["asserting_inference_as_fact", "unconfirmed_conclusion"],
    ),
    "QI-C06": ProvisionalMechanism(
        mechanism_id="QI-C06",
        name="Contradiction Repair",
        family="Discrepancy Resolution",
        primary_transformation="discrepancy -> reconciliation/chronology",
        runtime_trigger="conflicting_evidence",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:forensic_interviewing", "book:difficult_conversations"],
        forbidden_failure_patterns=["hostile_accusation", "ignoring_contradiction"],
    ),
    "QI-C07": ProvisionalMechanism(
        mechanism_id="QI-C07",
        name="Breadth / What-Else Expansion",
        family="Completeness Expansion",
        primary_transformation="visible answer -> missing dimensions",
        runtime_trigger="completeness_deficit",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:strategic_questioning"],
        forbidden_failure_patterns=["stopping_at_first_surface_answer"],
    ),
    "QI-C08": ProvisionalMechanism(
        mechanism_id="QI-C08",
        name="Requirement-Led Lead Tracking",
        family="Coverage Tracking",
        primary_transformation="question sequence -> unresolved requirement set",
        runtime_trigger="missing_coverage",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:investigative_journalism"],
        forbidden_failure_patterns=["dropping_crucial_evidence_gaps"],
    ),
    "QI-C09": ProvisionalMechanism(
        mechanism_id="QI-C09",
        name="Research-to-Discrepancy",
        family="Expected State Modeling",
        primary_transformation="external evidence -> expected state -> compare",
        runtime_trigger="prepared_discrepancy",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:research_methods", "book:deep_interviews"],
        forbidden_failure_patterns=["unresearched_guessing", "false_presumption"],
    ),
    "QI-C10": ProvisionalMechanism(
        mechanism_id="QI-C10",
        name="Social / Contextual Reconstruction",
        family="Ecosystem Reconstruction",
        primary_transformation="individual account -> social/system context",
        runtime_trigger="contextual_gap",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:systems_thinking"],
        forbidden_failure_patterns=["isolated_individual_bias"],
    ),
    "QI-C11": ProvisionalMechanism(
        mechanism_id="QI-C11",
        name="Premortem / Future-Failure",
        family="Risk & Edge Analysis",
        primary_transformation="current belief -> failure conditions",
        runtime_trigger="forward_risk_gap",
        disposition=MechanismDisposition.RESEARCH_MORE,
        source_lineage=["book:thinking_in_bets"],
        forbidden_failure_patterns=["fatalistic_projection"],
    ),
    "QI-C12": ProvisionalMechanism(
        mechanism_id="QI-C12",
        name="Past-Self Contrast",
        family="Transformation Verification",
        primary_transformation="present stance -> historical transformation",
        runtime_trigger="transformation_hypothesis",
        disposition=MechanismDisposition.PROMOTION_CANDIDATE,
        source_lineage=["book:narrative_identity"],
        forbidden_failure_patterns=["ahistorical_flattening"],
    ),
    "QI-C13": ProvisionalMechanism(
        mechanism_id="QI-C13",
        name="Strategic Silence",
        family="Interactional Dynamics",
        primary_transformation="verbal prompt -> space for retrieval",
        runtime_trigger="reflective_opportunity",
        disposition=MechanismDisposition.RESEARCH_MORE,
        source_lineage=["book:art_of_interviewing"],
        forbidden_failure_patterns=["awkward_deadlock"],
    ),
    "QI-C14": ProvisionalMechanism(
        mechanism_id="QI-C14",
        name="Self-Generated Standard",
        family="Normative Clarification",
        primary_transformation="answer -> Guest's own evaluation criteria",
        runtime_trigger="normative_ambiguity",
        disposition=MechanismDisposition.RESEARCH_MORE,
        source_lineage=["book:evaluative_inquiry"],
        forbidden_failure_patterns=["imposing_system_norm"],
    ),
    "QI-C15": ProvisionalMechanism(
        mechanism_id="QI-C15",
        name="Social Reference Reconstruction",
        family="Authority Field",
        primary_transformation="stance -> surrounding actors/authority",
        runtime_trigger="social_field_gap",
        disposition=MechanismDisposition.RESEARCH_MORE,
        source_lineage=["book:social_psychology"],
        forbidden_failure_patterns=["gossip_diversion"],
    ),
}


class CompositionCompatibility(BaseModel):
    """
    Evaluates archetype, format, and narrative role compatibility.
    Constrains question elicitation to ensure answers naturally fit downstream targets
    without allowing format/archetype containers to manufacture evidence.
    """
    archetype_refs: List[SemanticRef] = Field(default_factory=list)
    format_refs: List[SemanticRef] = Field(default_factory=list)
    narrative_role_refs: List[SemanticRef] = Field(default_factory=list)
    expected_response_structure: List[str] = Field(
        default_factory=lambda: ["chronological_event", "internal_friction", "cost_paid"]
    )
    compatibility_score: float = Field(0.85, ge=0.0, le=1.0)
    compatible_reasons: List[str] = Field(default_factory=list)
    incompatible_reasons: List[str] = Field(default_factory=list)

    def is_compatible(self, min_threshold: float = 0.50) -> bool:
        return self.compatibility_score >= min_threshold and len(self.incompatible_reasons) == 0


class QuestionCandidate(BaseModel):
    """
    Derived natural-language question realization with explicit psychological/semantic targets.
    Maintains locked dimensions to prevent prompt drift during regeneration.
    """
    question_id: str = Field(default_factory=lambda: f"qc:{uuid.uuid4().hex[:12]}")
    version: str = Field("1.0.0")
    text: str = Field(..., min_length=15, description="The open-ended natural-language prompt")
    objective: str = Field(..., min_length=10, description="The psychological/semantic target")
    
    # Derived Dimensions
    target_resolution: AnswerResolution = Field(default=AnswerResolution.EPISODIC)
    evidence_mode: EvidenceMode = Field(default=EvidenceMode.STORY)
    temporal_orientation: TemporalOrientation = Field(default=TemporalOrientation.PAST_RECONSTRUCTION)
    social_reference_frame: SocialReferenceFrame = Field(default=SocialReferenceFrame.SELF)
    interactional_fit: Optional[str] = Field("high_rapport_direct", description="Interaction style/fit")
    epistemic_posture: str = Field("curious_inquiry", description="Interviewer epistemic stance")
    
    # Mechanism & Requirements
    mechanism_refs: List[SemanticRef] = Field(default_factory=list, description="Admitted provisional mechanism refs")
    expected_response_shape: List[str] = Field(default_factory=lambda: ["chronological_event", "internal_friction", "cost_paid"])
    expected_evidence: List[str] = Field(default_factory=list)
    trigger_state: Optional[str] = None
    forbidden_failure_patterns: List[str] = Field(default_factory=list)
    
    # Downstream Compatibility & Provenance
    composition_compatibility: CompositionCompatibility = Field(default_factory=CompositionCompatibility)
    parent_candidate_ref: Optional[SemanticRef] = None
    locked_dimensions: List[str] = Field(
        default_factory=lambda: ["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
        description="Immutable dimensions that cannot change during regeneration",
    )
    operator_feedback_refs: List[SemanticRef] = Field(default_factory=list)
    provenance: Provenance = Field(default_factory=Provenance)
    is_canonical: bool = Field(False)


class AnswerRoutingProfile(BaseModel):
    """
    State routing profile defining how observed answers transition the inquiry frontier.
    """
    bounded_frontier_size: int = Field(3, ge=1, le=5)
    allowed_actions: List[str] = Field(
        default_factory=lambda: ["deepen", "broaden", "reconcile", "verify", "reframe", "advance", "close"]
    )
    tie_break_order: List[str] = Field(
        default_factory=lambda: [
            "requirement_coverage",
            "hypothesis_evidence_fit",
            "interactional_fit",
            "composition_compatibility",
            "semantic_novelty",
            "operator_preferences",
            "deterministic_candidate_order",
        ]
    )


class QuestionProgram(BaseModel):
    """
    Derived Question IR combining selected hypothesis, objective, evidence requirements,
    candidate mechanism coalition, and multiple syntactic question candidates.
    """
    program_id: str = Field(default_factory=lambda: f"qp:{uuid.uuid4().hex[:10]}")
    hypothesis_ref: SemanticRef = Field(...)
    objective: str = Field(..., min_length=10)
    target_resolution: AnswerResolution = Field(default=AnswerResolution.EPISODIC)
    expected_evidence: List[str] = Field(default_factory=list)
    response_shape: List[str] = Field(default_factory=list)
    composition_compatibility: CompositionCompatibility = Field(default_factory=CompositionCompatibility)
    primitive_coalition_refs: List[SemanticRef] = Field(default_factory=list)
    candidate_questions: List[QuestionCandidate] = Field(default_factory=list)
    routing_policy: AnswerRoutingProfile = Field(default_factory=AnswerRoutingProfile)
    provenance: Provenance = Field(default_factory=Provenance)
    is_canonical: bool = Field(False)


# Backward compatibility alias
QuestionProgramDerived = QuestionProgram


PROVISIONAL_MECHANISM_SYNTHESIS_CATALOG = APPROVED_PROVISIONAL_MECHANISMS


class QuestionIntelligenceResolver:
    """
    Resolves a QuestionProgram from an approved HypothesisCandidate.
    Maintains the invariant that question mechanisms remain provisional unless independently promoted.
    """

    def __init__(self, mechanism_catalog: Optional[Dict[str, ProvisionalMechanism]] = None):
        self.catalog = mechanism_catalog or APPROVED_PROVISIONAL_MECHANISMS

    def verify_mechanism_admissibility(self, mechanism_id: str) -> ProvisionalMechanism:
        """
        Verifies that a mechanism is admitted by the approved synthesis catalog.
        Raises ValueError if the mechanism is unknown or unaudited.
        """
        mid = mechanism_id.strip().upper()
        if mid not in self.catalog:
            raise ValueError(
                f"Mechanism {mechanism_id!r} is not an admitted provisional mechanism in Question Intelligence Synthesis."
            )
        return self.catalog[mid]

    def resolve_question_program(
        self,
        candidate: HypothesisCandidate,
        target_archetype: Optional[str] = None,
        target_format: Optional[str] = None,
        target_narrative_role: Optional[str] = None,
    ) -> QuestionProgram:
        """
        Executes the resolution chain:
          hypothesis -> objective -> evidence requirements -> mechanism coalition -> Question IR -> NL realizations.
        """
        # 1. Derive Question Objective
        objective = (
            f"Elicit direct empirical lived testimony regarding collision: '{candidate.collision_statement}' "
            f"focusing on {candidate.coordinates.d05_guest_contradiction or 'operational friction'}."
        )

        # 2. Derive Evidence Requirements and Target Resolution
        expected_evidence = candidate.desired_evidence or [
            "Specific decision event with verifiable date or milestone",
            "Observed internal tension before action was taken",
            "Concrete operational consequence or personal cost",
        ]

        # 3. Form Candidate Mechanism Coalition
        # Combine default primary mechanisms based on coordinate features
        coalition_ids = ["QI-C01", "QI-C04", "QI-C09"]
        if candidate.coordinates.d05_guest_contradiction:
            coalition_ids.append("QI-C06")
        if candidate.coordinates.d06_guest_transformation:
            coalition_ids.append("QI-C12")

        primitive_coalition_refs = [
            SemanticRef(
                object_id=mid,
                object_type="provisional_question_mechanism",
                version="v3_synthesis",
            )
            for mid in coalition_ids
        ]

        # 4. Evaluate Composition Compatibility
        from .composition_compatibility import CompositionCompatibilityEvaluator
        evaluator = CompositionCompatibilityEvaluator()
        comp_compat = evaluator.evaluate_compatibility(
            candidate=candidate,
            target_archetype=target_archetype,
            target_format=target_format,
            target_narrative_role=target_narrative_role,
            question_objective=objective,
            target_resolution=AnswerResolution.EPISODIC,
            evidence_mode=EvidenceMode.STORY,
        )

        hyp_ref = (
            candidate.upstream_hypothesis_refs[0]
            if candidate.upstream_hypothesis_refs
            else SemanticRef(object_id=candidate.candidate_id, object_type="hypothesis_candidate")
        )

        # 5. Generate Distinct Syntactic Realizations
        # Syntactic Style 1: Direct Crucible Inquiry (QI-C04 + QI-C01)
        q1_text = (
            f"Take me back to the exact moment when you realized {candidate.collision_statement.lower().rstrip('.')} — "
            f"what was happening in the room, and what specific cost did you have to pay?"
        )
        q1_id = f"qc:{hashlib.sha256(f'{candidate.candidate_id}:crucible'.encode('utf-8')).hexdigest()[:8]}_crucible"
        q1 = QuestionCandidate(
            question_id=q1_id,
            text=q1_text,
            objective=objective,
            target_resolution=AnswerResolution.EPISODIC,
            evidence_mode=EvidenceMode.STORY,
            temporal_orientation=TemporalOrientation.PAST_RECONSTRUCTION,
            social_reference_frame=SocialReferenceFrame.SELF,
            interactional_fit="direct_experiential",
            epistemic_posture="grounded_inquiry",
            mechanism_refs=[primitive_coalition_refs[0], primitive_coalition_refs[1]],
            expected_evidence=expected_evidence,
            forbidden_failure_patterns=["abstract_intellectualization", "scripted_talking_points"],
            composition_compatibility=comp_compat,
            parent_candidate_ref=SemanticRef(object_id=candidate.candidate_id),
            locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
            provenance=Provenance(
                source_refs=[hyp_ref],
                generated_by="cae-interview-intelligence:question-resolver:v3",
            ),
        )

        # Syntactic Style 2: Chronological / Transformation Inquiry (QI-C12 + QI-C01)
        q2_text = (
            f"Earlier in your career you held a very different stance on this. Walk me through the chronology: "
            f"what specific event broke your previous model and forced you into this current position?"
        )
        q2_id = f"qc:{hashlib.sha256(f'{candidate.candidate_id}:chronology'.encode('utf-8')).hexdigest()[:8]}_chronology"
        q2 = QuestionCandidate(
            question_id=q2_id,
            text=q2_text,
            objective=objective,
            target_resolution=AnswerResolution.MECHANISTIC,
            evidence_mode=EvidenceMode.FACT,
            temporal_orientation=TemporalOrientation.PAST_RECONSTRUCTION,
            social_reference_frame=SocialReferenceFrame.SELF,
            interactional_fit="reflective_historical",
            epistemic_posture="exploratory_curiosity",
            mechanism_refs=[primitive_coalition_refs[0]],
            expected_evidence=expected_evidence,
            forbidden_failure_patterns=["vague_generalization", "unverifiable_claim"],
            composition_compatibility=comp_compat,
            parent_candidate_ref=SemanticRef(object_id=candidate.candidate_id),
            locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
            provenance=Provenance(
                source_refs=[hyp_ref],
                generated_by="cae-interview-intelligence:question-resolver:v3",
            ),
        )

        # Syntactic Style 3: Oblique / External Discrepancy Inquiry (QI-C09 + QI-C06)
        q3_text = (
            f"If someone looks at the external metrics, everything appeared successful. But what was the internal breakdown "
            f"or discrepancy that nobody outside that room could see?"
        )
        q3_id = f"qc:{hashlib.sha256(f'{candidate.candidate_id}:discrepancy'.encode('utf-8')).hexdigest()[:8]}_discrepancy"
        q3 = QuestionCandidate(
            question_id=q3_id,
            text=q3_text,
            objective=objective,
            target_resolution=AnswerResolution.EVIDENTIAL,
            evidence_mode=EvidenceMode.INTERPRETATION,
            temporal_orientation=TemporalOrientation.PRESENT_OBSERVATION,
            social_reference_frame=SocialReferenceFrame.AUDIENCE,
            interactional_fit="confidential_probe",
            epistemic_posture="respectful_challenge",
            mechanism_refs=[primitive_coalition_refs[2]],
            expected_evidence=expected_evidence,
            forbidden_failure_patterns=["defensive_retreat", "pat_answers"],
            composition_compatibility=comp_compat,
            parent_candidate_ref=SemanticRef(object_id=candidate.candidate_id),
            locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
            provenance=Provenance(
                source_refs=[hyp_ref],
                generated_by="cae-interview-intelligence:question-resolver:v3",
            ),
        )

        candidate_questions = [q1, q2, q3]

        return QuestionProgramDerived(
            hypothesis_ref=hyp_ref,
            objective=objective,
            target_resolution=AnswerResolution.EPISODIC,
            expected_evidence=expected_evidence,
            response_shape=["concrete_scene", "vulnerable_friction", "receipt"],
            composition_compatibility=comp_compat,
            primitive_coalition_refs=primitive_coalition_refs,
            candidate_questions=candidate_questions,
            routing_policy=AnswerRoutingProfile(),
            provenance=Provenance(
                source_refs=[hyp_ref],
                generated_by="cae-interview-intelligence:question-resolver:v3",
            ),
        )

    def regenerate_question_candidate(
        self,
        existing_candidate: QuestionCandidate,
        syntax_style: str,
        variation_prompt_prefix: Optional[str] = None,
    ) -> QuestionCandidate:
        """
        Regenerates a question candidate with an alternative syntactic phrasing while strictly
        enforcing immutability of all locked dimensions (hypothesis, evidence requirements, resolution).
        """
        # Create a deep copy to ensure no shared mutable state
        parts = existing_candidate.version.split(".")
        if len(parts) == 3 and parts[1].isdigit():
            new_version_num = f"{parts[0]}.{int(parts[1]) + 1}.{parts[2]}"
        else:
            new_version_num = f"{existing_candidate.version}.1"
        
        # Verify locked dimensions
        for dim in existing_candidate.locked_dimensions:
            if dim == "target_resolution" and not existing_candidate.target_resolution:
                raise ValueError(f"Locked dimension {dim} missing in original candidate.")
            if dim == "expected_evidence" and not existing_candidate.expected_evidence:
                raise ValueError(f"Locked dimension {dim} missing in original candidate.")

        prefix = variation_prompt_prefix or "Let's approach this from a different angle: "
        new_text = f"{prefix}When it comes to {existing_candidate.objective.lower().rstrip('.')}, what is the single most unvarnished truth you learned?"

        parent_key = (
            existing_candidate.parent_candidate_ref.object_id
            if existing_candidate.parent_candidate_ref
            else existing_candidate.question_id
        )
        regen_hash = hashlib.sha256(
            f"{parent_key}:{syntax_style}:{variation_prompt_prefix}:{new_version_num}".encode("utf-8")
        ).hexdigest()[:8]

        regenerated = QuestionCandidate(
            question_id=f"qc:{regen_hash}_v{new_version_num.replace('.', '_')}",
            version=new_version_num,
            text=new_text,
            objective=existing_candidate.objective,  # Preserved
            target_resolution=existing_candidate.target_resolution,  # Locked
            evidence_mode=existing_candidate.evidence_mode,  # Locked
            temporal_orientation=existing_candidate.temporal_orientation,
            social_reference_frame=existing_candidate.social_reference_frame,
            interactional_fit=f"style_{syntax_style}",
            epistemic_posture=existing_candidate.epistemic_posture,
            mechanism_refs=list(existing_candidate.mechanism_refs),
            expected_response_shape=list(existing_candidate.expected_response_shape),
            expected_evidence=list(existing_candidate.expected_evidence),  # Locked
            forbidden_failure_patterns=list(existing_candidate.forbidden_failure_patterns),
            composition_compatibility=existing_candidate.composition_compatibility,
            parent_candidate_ref=SemanticRef(object_id=existing_candidate.question_id),
            locked_dimensions=list(existing_candidate.locked_dimensions),
            operator_feedback_refs=list(existing_candidate.operator_feedback_refs),
            provenance=Provenance(
                source_refs=[SemanticRef(object_id=existing_candidate.question_id)],
                audit_refs=list(existing_candidate.provenance.audit_refs),
                generated_by="cae-interview-intelligence:question-resolver:regenerate:v3",
            ),
        )
        return regenerated
