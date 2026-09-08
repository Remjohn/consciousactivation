"""
composition_compatibility.py
----------------------------
Downstream Format and Content Archetype Compatibility Engine for CAE.

Implements FR-IP-004:
"Downstream composition, format, and narrative constraints shall guide question elicitation
objectives without manufacturing evidence."

Provides:
- Authoritative metadata containers for Known Content Archetypes, Formats, and Narrative Roles.
- CompositionCompatibility model capturing derived evaluation scores and explanations.
- CompositionCompatibilityEvaluator enforcing semantic vs syntax alignment and anti-evidence-manufacturing invariants.
"""

import hashlib
import json
import uuid
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from conscious_activations_interview_composer.errors import ValidationError

from .hypothesis_adapter import CoordinateBasis, HypothesisCandidate, SemanticRef
from .question_resolver import (
    AnswerResolution,
    EvidenceMode,
    SocialReferenceFrame,
    TemporalOrientation,
    CompositionCompatibility,
)
from .semantic_acquisition import (
    AcquisitionEvidenceRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
)


class ArchetypeSpec(BaseModel):
    """
    Specification for a downstream content archetype container in the Conscious Movie Factory (CMF).
    """
    archetype_id: str = Field(..., description="Canonical identifier e.g. ARCH-CRUCIBLE")
    canonical_name: str
    preferred_resolution: AnswerResolution
    preferred_evidence_modes: List[EvidenceMode]
    required_response_shape: List[str]
    cognitive_job: str
    anti_failure_warning: str


class FormatSpec(BaseModel):
    """
    Specification for a downstream delivery/layout/pacing harness.
    """
    format_id: str = Field(..., description="Canonical format identifier e.g. FMT-01-STORY")
    canonical_name: str
    harness_description: str
    supported_archetype_ids: List[str]
    pacing_and_roll_structure: List[str]
    supported_aspect_ratios: List[str] = Field(default_factory=list)
    required_capabilities: List[str] = Field(default_factory=list)
    registry_version: str = "1.0.0"


class NarrativeRoleSpec(BaseModel):
    """
    Specification for a guest or narrator psychological role posture.
    """
    role_id: str = Field(..., description="Canonical role identifier e.g. ROLE-PROTAGONIST-CRUCIBLE")
    canonical_name: str
    posture_description: str
    preferred_social_frame: SocialReferenceFrame


# -----------------------------------------------------------------------------
# Authoritative Known Inventories (Reusing Existing Identifiers)
# -----------------------------------------------------------------------------

KNOWN_ARCHETYPES: Dict[str, ArchetypeSpec] = {
    "ARCH-CRUCIBLE": ArchetypeSpec(
        archetype_id="ARCH-CRUCIBLE",
        canonical_name="Crucible Testimony",
        preferred_resolution=AnswerResolution.EPISODIC,
        preferred_evidence_modes=[EvidenceMode.STORY],
        required_response_shape=["chronological_event", "internal_friction", "cost_paid"],
        cognitive_job="Expose high-friction reckoning and empirical sacrifice under pressure.",
        anti_failure_warning="Do not accept general philosophy or retrospective rationalization.",
    ),
    "ARCH-WITNESS": ArchetypeSpec(
        archetype_id="ARCH-WITNESS",
        canonical_name="The Witness Arc",
        preferred_resolution=AnswerResolution.EPISODIC,
        preferred_evidence_modes=[EvidenceMode.STORY, EvidenceMode.FACT],
        required_response_shape=["observed_scene", "sensory_detail", "verifiable_action"],
        cognitive_job="Provide first-hand empirical observation of institutional/systemic realities.",
        anti_failure_warning="Do not accept secondary rumors without direct sensory observation.",
    ),
    "ARCH-ACHIEVEMENT": ArchetypeSpec(
        archetype_id="ARCH-ACHIEVEMENT",
        canonical_name="Achievement Transformation Story",
        preferred_resolution=AnswerResolution.EPISODIC,
        preferred_evidence_modes=[EvidenceMode.STORY],
        required_response_shape=["starting_barrier", "inflection_decision", "transformation_outcome"],
        cognitive_job="Demonstrate sovereign victory over a structural or cognitive barrier.",
        anti_failure_warning="Do not substitute unearned boastful summary for the inflection struggle.",
    ),
    "ARCH-INVESTIGATIVE": ArchetypeSpec(
        archetype_id="ARCH-INVESTIGATIVE",
        canonical_name="Investigative Breakdown",
        preferred_resolution=AnswerResolution.MECHANISTIC,
        preferred_evidence_modes=[EvidenceMode.FACT, EvidenceMode.INTERPRETATION],
        required_response_shape=["causal_mechanism", "structural_anomaly", "empirical_metric"],
        cognitive_job="Deconstruct hidden operational debt and causal root drivers.",
        anti_failure_warning="Do not accept vague hand-wavy blame without concrete mechanism trace.",
    ),
    "ARCH-DEBUNK": ArchetypeSpec(
        archetype_id="ARCH-DEBUNK",
        canonical_name="Myth Debunk",
        preferred_resolution=AnswerResolution.MECHANISTIC,
        preferred_evidence_modes=[EvidenceMode.COUNTERFACTUAL, EvidenceMode.FACT],
        required_response_shape=["stated_orthodoxy", "contradictory_evidence", "underlying_reality"],
        cognitive_job="Expose widely accepted consensus illusion against empirical contradiction.",
        anti_failure_warning="Do not attack strawmen without citing the real dogma.",
    ),
    "ARCH-OBSERVATIONAL": ArchetypeSpec(
        archetype_id="ARCH-OBSERVATIONAL",
        canonical_name="Observational Systemic Critique",
        preferred_resolution=AnswerResolution.SPECIFIC,
        preferred_evidence_modes=[EvidenceMode.INTERPRETATION, EvidenceMode.FACT],
        required_response_shape=["absurd_norm", "unspoken_incentive", "cultural_contradiction"],
        cognitive_job="Highlight systemic irony or behavioral contradiction with sharp wit.",
        anti_failure_warning="Avoid mean-spirited cynicism devoid of structural insight.",
    ),
}

# Aliases for historical / lower-case keys
ARCHETYPE_ALIASES: Dict[str, str] = {
    "archetype_crucible": "ARCH-CRUCIBLE",
    "crucible_testimony": "ARCH-CRUCIBLE",
    "archetype:crucible_testimony": "ARCH-CRUCIBLE",
    "archetype_witness": "ARCH-WITNESS",
    "the_witness": "ARCH-WITNESS",
    "archetype:witness": "ARCH-WITNESS",
    "witness": "ARCH-WITNESS",
    "archetype_achievement": "ARCH-ACHIEVEMENT",
    "achievement_story": "ARCH-ACHIEVEMENT",
    "archetype:achievement_story": "ARCH-ACHIEVEMENT",
    "archetype_investigative": "ARCH-INVESTIGATIVE",
    "investigative_breakdown": "ARCH-INVESTIGATIVE",
    "archetype:investigative_breakdown": "ARCH-INVESTIGATIVE",
    "archetype_debunk": "ARCH-DEBUNK",
    "myth_debunk": "ARCH-DEBUNK",
    "archetype:myth_debunk": "ARCH-DEBUNK",
    "archetype_observational": "ARCH-OBSERVATIONAL",
    "observational_humor": "ARCH-OBSERVATIONAL",
    "archetype:observational_humor": "ARCH-OBSERVATIONAL",
}


KNOWN_FORMATS: Dict[str, FormatSpec] = {
    "FMT-01-STORY": FormatSpec(
        format_id="FMT-01-STORY",
        canonical_name="Cinematic Multi-Roll Story",
        harness_description="Rich narrative editing combining A-roll, B-roll, C-roll, and E-roll sonic integration.",
        supported_archetype_ids=["ARCH-CRUCIBLE", "ARCH-WITNESS", "ARCH-ACHIEVEMENT"],
        pacing_and_roll_structure=["A_ROLL_NARRATIVE", "B_ROLL_CONTEXT", "C_ROLL_EVIDENCE", "E_ROLL_SONIC"],
        required_capabilities=["A_ROLL_NARRATIVE", "B_ROLL_CONTEXT", "C_ROLL_EVIDENCE", "E_ROLL_SONIC"],
    ),
    "FMT-02-REACTION": FormatSpec(
        format_id="FMT-02-REACTION",
        canonical_name="Conscious Reaction Harness",
        harness_description="Dynamic perspective juxtaposition and emotional commentary.",
        supported_archetype_ids=["ARCH-DEBUNK", "ARCH-OBSERVATIONAL", "ARCH-WITNESS"],
        pacing_and_roll_structure=["HOOK_STIMULUS", "GUEST_REACTION", "SEMANTIC_SYNTHESIS"],
        supported_aspect_ratios=["9:16"],
        required_capabilities=["HOOK_STIMULUS", "GUEST_REACTION", "SEMANTIC_SYNTHESIS"],
    ),
    "FMT-03-BREAKDOWN": FormatSpec(
        format_id="FMT-03-BREAKDOWN",
        canonical_name="Analytical Explainer Breakdown",
        harness_description="High-density step-by-step causal flow with diagrams and evidence callouts.",
        supported_archetype_ids=["ARCH-INVESTIGATIVE", "ARCH-DEBUNK"],
        pacing_and_roll_structure=["ANOMALY_HOOK", "CAUSAL_TRACE", "EMPIRICAL_PROOF", "SYSTEM_CONCLUSION"],
        required_capabilities=["ANOMALY_HOOK", "CAUSAL_TRACE", "EMPIRICAL_PROOF", "SYSTEM_CONCLUSION"],
    ),
    "FMT-04-CAROUSEL": FormatSpec(
        format_id="FMT-04-CAROUSEL",
        canonical_name="Structured Sequential Narrative Carousel",
        harness_description="Swipeable visual card progression requiring concise self-contained beats.",
        supported_archetype_ids=["ARCH-ACHIEVEMENT", "ARCH-INVESTIGATIVE", "ARCH-DEBUNK"],
        pacing_and_roll_structure=["SLIDE_HOOK", "SLIDE_CONFLICT", "SLIDE_INSIGHT", "SLIDE_PAYOFF"],
        required_capabilities=["SLIDE_HOOK", "SLIDE_CONFLICT", "SLIDE_INSIGHT", "SLIDE_PAYOFF"],
    ),
}

FORMAT_ALIASES: Dict[str, str] = {
    "format:01_story": "FMT-01-STORY",
    "format_01_story": "FMT-01-STORY",
    "01_story": "FMT-01-STORY",
    "format:02_reaction": "FMT-02-REACTION",
    "format_reaction": "FMT-02-REACTION",
    "format:03_breakdown": "FMT-03-BREAKDOWN",
    "format_breakdown": "FMT-03-BREAKDOWN",
    "format:04_carousel": "FMT-04-CAROUSEL",
    "format_carousel": "FMT-04-CAROUSEL",
}


KNOWN_NARRATIVE_ROLES: Dict[str, NarrativeRoleSpec] = {
    "ROLE-PROTAGONIST-CRUCIBLE": NarrativeRoleSpec(
        role_id="ROLE-PROTAGONIST-CRUCIBLE",
        canonical_name="Crucible Protagonist",
        posture_description="Direct participant who faced high-stakes consequence.",
        preferred_social_frame=SocialReferenceFrame.SELF,
    ),
    "ROLE-OBSERVER-WITNESS": NarrativeRoleSpec(
        role_id="ROLE-OBSERVER-WITNESS",
        canonical_name="Empirical Witness",
        posture_description="Objective observer who witnessed actions and conditions first-hand.",
        preferred_social_frame=SocialReferenceFrame.GROUP,
    ),
    "ROLE-TECHNICAL-ANALYST": NarrativeRoleSpec(
        role_id="ROLE-TECHNICAL-ANALYST",
        canonical_name="Technical Analyst",
        posture_description="Specialist deconstructing systemic mechanics and data traces.",
        preferred_social_frame=SocialReferenceFrame.INSTITUTION,
    ),
    "ROLE-CONTRARIAN-DEBUNKER": NarrativeRoleSpec(
        role_id="ROLE-CONTRARIAN-DEBUNKER",
        canonical_name="Contrarian Debunker",
        posture_description="Challenger confronting consensus falsehood with conflicting facts.",
        preferred_social_frame=SocialReferenceFrame.AUDIENCE,
    ),
    "ROLE-SYSTEMIC-CRITIC": NarrativeRoleSpec(
        role_id="ROLE-SYSTEMIC-CRITIC",
        canonical_name="Systemic Critic",
        posture_description="Observant narrator revealing structural absurdities.",
        preferred_social_frame=SocialReferenceFrame.PEER,
    ),
}

ROLE_ALIASES: Dict[str, str] = {
    "role:protagonist_crucible": "ROLE-PROTAGONIST-CRUCIBLE",
    "protagonist_crucible": "ROLE-PROTAGONIST-CRUCIBLE",
    "role:observer_witness": "ROLE-OBSERVER-WITNESS",
    "observer_witness": "ROLE-OBSERVER-WITNESS",
    "role:technical_analyst": "ROLE-TECHNICAL-ANALYST",
    "technical_analyst": "ROLE-TECHNICAL-ANALYST",
    "role:contrarian_debunker": "ROLE-CONTRARIAN-DEBUNKER",
    "contrarian_debunker": "ROLE-CONTRARIAN-DEBUNKER",
    "role:systemic_critic": "ROLE-SYSTEMIC-CRITIC",
    "systemic_critic": "ROLE-SYSTEMIC-CRITIC",
}


# -----------------------------------------------------------------------------
# Composition Compatibility Evaluator
# -----------------------------------------------------------------------------

class CompositionCompatibilityEvaluator:
    """
    Evaluator engine for downstream format, archetype, and narrative role constraints.
    Enforces FR-IP-004 rules and anti-reward hacking invariants.
    """

    def resolve_archetype_key(self, raw_id: Optional[str]) -> Optional[str]:
        if not raw_id:
            return None
        cleaned = raw_id.strip()
        if cleaned in KNOWN_ARCHETYPES:
            return cleaned
        return ARCHETYPE_ALIASES.get(cleaned.lower(), cleaned)

    def resolve_format_key(self, raw_id: Optional[str]) -> Optional[str]:
        if not raw_id:
            return None
        cleaned = raw_id.strip()
        if cleaned in KNOWN_FORMATS:
            return cleaned
        return FORMAT_ALIASES.get(cleaned.lower(), cleaned)

    def resolve_role_key(self, raw_id: Optional[str]) -> Optional[str]:
        if not raw_id:
            return None
        cleaned = raw_id.strip()
        if cleaned in KNOWN_NARRATIVE_ROLES:
            return cleaned
        return ROLE_ALIASES.get(cleaned.lower(), cleaned)

    def evaluate_compatibility(
        self,
        candidate: Optional[HypothesisCandidate] = None,
        target_archetype: Optional[str] = None,
        target_format: Optional[str] = None,
        target_narrative_role: Optional[str] = None,
        question_objective: Optional[str] = None,
        target_resolution: AnswerResolution = AnswerResolution.EPISODIC,
        evidence_mode: EvidenceMode = EvidenceMode.STORY,
        expected_evidence: Optional[List[str]] = None,
    ) -> CompositionCompatibility:
        """
        Evaluates compatibility between question targets and downstream format/archetype constraints.
        Returns a typed CompositionCompatibility object with detailed explanation reasons.
        """
        # Resolve keys
        raw_arch = target_archetype or (
            candidate.archetype_refs[0].object_id if candidate and candidate.archetype_refs else (
                candidate.coordinates.d10_archetype_opportunity if candidate else "ARCH-CRUCIBLE"
            )
        )
        arch_key = self.resolve_archetype_key(raw_arch)
        arch_spec = KNOWN_ARCHETYPES.get(arch_key) if arch_key else None

        raw_fmt = target_format or (
            candidate.format_refs[0].object_id if candidate and candidate.format_refs else "FMT-01-STORY"
        )
        fmt_key = self.resolve_format_key(raw_fmt)
        fmt_spec = KNOWN_FORMATS.get(fmt_key) if fmt_key else None

        raw_role = target_narrative_role or (
            candidate.narrative_role_refs[0].object_id if candidate and candidate.narrative_role_refs else "ROLE-PROTAGONIST-CRUCIBLE"
        )
        role_key = self.resolve_role_key(raw_role)
        role_spec = KNOWN_NARRATIVE_ROLES.get(role_key) if role_key else None

        # Base scoring and collections
        score = 1.0
        compatible_reasons: List[str] = []
        incompatible_reasons: List[str] = []
        expected_response_shape: List[str] = []

        # 1. Hard check: Explicitly incompatible / unsupported broadcast promo formats
        if arch_key == "incompatible_archetype_broadcast_promo" or raw_arch == "incompatible_archetype_broadcast_promo":
            score = 0.20
            incompatible_reasons.append("Interview elicitation format incompatible with promotional soundbite broadcast syntax.")
            return CompositionCompatibility(
                archetype_refs=[SemanticRef(object_id=raw_arch or "incompatible_archetype_broadcast_promo", object_type="content_archetype")],
                format_refs=[SemanticRef(object_id=raw_fmt or "FMT-01-STORY", object_type="delivery_format")],
                narrative_role_refs=[SemanticRef(object_id=raw_role or "ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role")],
                expected_response_structure=["unsupported_soundbite"],
                compatibility_score=score,
                compatible_reasons=[],
                incompatible_reasons=incompatible_reasons,
            )

        # 2. Archetype Evaluation
        if arch_spec:
            expected_response_shape.extend(arch_spec.required_response_shape)
            
            # Resolution alignment
            if target_resolution == arch_spec.preferred_resolution:
                score += 0.0
                compatible_reasons.append(
                    f"Target resolution '{target_resolution.value}' matches archetype '{arch_spec.canonical_name}' requirement."
                )
            else:
                # E.g. story archetype requested but question yields abstract / mechanistic
                if arch_spec.preferred_resolution == AnswerResolution.EPISODIC and target_resolution in (AnswerResolution.ABSTRACT, AnswerResolution.GENERAL):
                    score -= 0.45
                    incompatible_reasons.append(
                        f"Archetype '{arch_spec.canonical_name}' requires EPISODIC lived testimony, but question targets {target_resolution.value}."
                    )
                elif arch_spec.preferred_resolution == AnswerResolution.MECHANISTIC and target_resolution in (AnswerResolution.ABSTRACT, AnswerResolution.GENERAL):
                    score -= 0.40
                    incompatible_reasons.append(
                        f"Archetype '{arch_spec.canonical_name}' requires MECHANISTIC causal trace, but question targets {target_resolution.value}."
                    )
                else:
                    score -= 0.15
                    compatible_reasons.append(
                        f"Target resolution '{target_resolution.value}' provides usable context for archetype '{arch_spec.canonical_name}'."
                    )

            # Evidence Mode alignment
            if evidence_mode in arch_spec.preferred_evidence_modes:
                compatible_reasons.append(
                    f"Evidence mode '{evidence_mode.value}' aligns with archetype '{arch_spec.canonical_name}'."
                )
            else:
                score -= 0.20
                incompatible_reasons.append(
                    f"Evidence mode '{evidence_mode.value}' is less optimal for archetype '{arch_spec.canonical_name}' (prefers {[m.value for m in arch_spec.preferred_evidence_modes]})."
                )
        else:
            expected_response_shape.extend(["chronological_event", "internal_friction", "cost_paid"])
            compatible_reasons.append(f"Using default response shape for uncataloged archetype '{raw_arch}'.")

        # 3. Format Evaluation
        if fmt_spec:
            if arch_spec and arch_spec.archetype_id not in fmt_spec.supported_archetype_ids:
                score -= 0.35
                incompatible_reasons.append(
                    f"Delivery format '{fmt_spec.canonical_name}' is not optimized for archetype '{arch_spec.canonical_name}'."
                )
            else:
                compatible_reasons.append(
                    f"Delivery format '{fmt_spec.canonical_name}' fully supports archetype '{arch_spec.canonical_name if arch_spec else raw_arch}'."
                )

        # 4. Narrative Role Evaluation
        if role_spec:
            compatible_reasons.append(
                f"Narrative role '{role_spec.canonical_name}' is compatible with interviewer inquiry posture."
            )

        # Normalize score bounds
        final_score = max(0.0, min(1.0, round(score, 2)))

        return CompositionCompatibility(
            archetype_refs=[
                SemanticRef(object_id=arch_spec.archetype_id if arch_spec else (raw_arch or "ARCH-CRUCIBLE"), object_type="content_archetype")
            ],
            format_refs=[
                SemanticRef(object_id=fmt_spec.format_id if fmt_spec else (raw_fmt or "FMT-01-STORY"), object_type="delivery_format")
            ],
            narrative_role_refs=[
                SemanticRef(object_id=role_spec.role_id if role_spec else (raw_role or "ROLE-PROTAGONIST-CRUCIBLE"), object_type="narrative_role")
            ],
            expected_response_structure=list(dict.fromkeys(expected_response_shape)),
            compatibility_score=final_score,
            compatible_reasons=compatible_reasons,
            incompatible_reasons=incompatible_reasons,
        )

    @staticmethod
    def _profile_ref(object_id: str, object_type: str, payload: Any, version: str) -> SemanticRef:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return SemanticRef(
            object_id=object_id,
            object_type=object_type,
            version=version,
            sha256=hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        )

    @staticmethod
    def _binding_ref(ref: Optional[SemanticRef]) -> Optional[SemanticRef]:
        if ref is None:
            return None
        return SemanticRef(**ref.model_dump())

    @classmethod
    def evaluate_preproduction_admission(
        cls,
        *,
        target_archetype: str,
        target_format: str,
        target_narrative_role: Optional[str] = None,
        target_aspect_ratio: Optional[str] = None,
        provided_format_capabilities: Optional[List[str]] = None,
        narrative_ref: Optional[SemanticRef] = None,
        hypothesis_ref: Optional[SemanticRef] = None,
        target_resolution: AnswerResolution = AnswerResolution.EPISODIC,
        evidence_mode: EvidenceMode = EvidenceMode.STORY,
    ) -> CompositionCompatibility:
        """
        CA-M005 authoritative admission check for Stage 05 PreProduction.

        The calculation is deterministic and fail-closed: unknown profiles, unsupported
        archetype/format pairs, declared aspect-ratio conflicts, and missing declared
        format capabilities all block admission. Narrative/hypothesis refs are carried
        into the result so the operator/runtime can persist the exact binding when one
        is available.
        """
        evaluator = cls()
        arch_key = evaluator.resolve_archetype_key(target_archetype)
        fmt_key = evaluator.resolve_format_key(target_format)
        role_key = evaluator.resolve_role_key(target_narrative_role) if target_narrative_role else None
        arch_spec = KNOWN_ARCHETYPES.get(arch_key) if arch_key else None
        fmt_spec = KNOWN_FORMATS.get(fmt_key) if fmt_key else None

        base = evaluator.evaluate_compatibility(
            target_archetype=target_archetype,
            target_format=target_format,
            target_narrative_role=target_narrative_role,
            target_resolution=target_resolution,
            evidence_mode=evidence_mode,
        )

        incompatible = list(base.incompatible_reasons)
        compatible = list(base.compatible_reasons)
        required = list(fmt_spec.required_capabilities) if fmt_spec else []
        provided = sorted(set(required if provided_format_capabilities is None and fmt_spec else (provided_format_capabilities or [])))
        missing = sorted(set(required) - set(provided))

        if fmt_spec is None:
            incompatible.append(f"Unknown delivery format profile '{target_format}' is not admitted by the current format registry.")
        if arch_spec is None:
            incompatible.append(f"Unknown archetype profile '{target_archetype}' is not admitted by the current archetype registry.")
        if role_key is not None and role_key not in KNOWN_NARRATIVE_ROLES:
            incompatible.append(f"Unknown narrative role profile '{target_narrative_role}' is not admitted by the current narrative-role registry.")
        if arch_spec and fmt_spec and arch_spec.archetype_id not in fmt_spec.supported_archetype_ids:
            incompatible.append(
                f"Archetype '{arch_spec.canonical_name}' is not supported by delivery format '{fmt_spec.canonical_name}'."
            )
        if target_aspect_ratio and fmt_spec and fmt_spec.supported_aspect_ratios:
            if target_aspect_ratio not in fmt_spec.supported_aspect_ratios:
                incompatible.append(
                    f"Aspect ratio '{target_aspect_ratio}' is not supported by delivery format '{fmt_spec.canonical_name}'; "
                    f"supported ratios are {fmt_spec.supported_aspect_ratios}."
                )
            else:
                compatible.append(
                    f"Aspect ratio '{target_aspect_ratio}' is supported by delivery format '{fmt_spec.canonical_name}'."
                )
        if missing:
            incompatible.append(
                "Required format capabilities are missing: " + ", ".join(missing) + "."
            )

        status = "PASS" if not incompatible and base.is_compatible() else "BLOCK"
        format_ref = evaluator._profile_ref(fmt_spec.format_id, "delivery_format_profile", fmt_spec.model_dump(), fmt_spec.registry_version) if fmt_spec else None
        archetype_ref = evaluator._profile_ref(arch_spec.archetype_id, "content_archetype_profile", arch_spec.model_dump(), "1.0.0") if arch_spec else None
        result = CompositionCompatibility(
            **base.model_dump(exclude={
                "gate_status", "target_aspect_ratio", "required_format_capabilities",
                "provided_format_capabilities", "missing_format_capabilities",
                "narrative_ref", "hypothesis_ref", "format_profile_ref",
                "archetype_profile_ref", "gate_version", "decision_sha256",
            }),
            gate_status=status,
            target_aspect_ratio=target_aspect_ratio,
            required_format_capabilities=required,
            provided_format_capabilities=provided,
            missing_format_capabilities=missing,
            narrative_ref=cls._binding_ref(narrative_ref),
            hypothesis_ref=cls._binding_ref(hypothesis_ref),
            format_profile_ref=format_ref,
            archetype_profile_ref=archetype_ref,
            gate_version="CA-M005-v1",
            compatible_reasons=compatible,
            incompatible_reasons=sorted(set(incompatible)),
        )
        core = result.model_dump(exclude={"decision_sha256"}, mode="json")
        result.decision_sha256 = hashlib.sha256(
            json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        ).hexdigest()
        return result

    @staticmethod
    def verify_admission_result(result: CompositionCompatibility) -> bool:
        if not result.decision_sha256:
            return False
        core = result.model_dump(exclude={"decision_sha256"}, mode="json")
        expected = hashlib.sha256(
            json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        ).hexdigest()
        return expected == result.decision_sha256

    def assert_archetype_does_not_manufacture_evidence(
        self,
        observation: SemanticAcquisitionObservation,
        target_archetype: str,
    ) -> None:
        """
        Enforces invariant: An archetype container label cannot turn generic, vague, or absent
        responses into authenticated story evidence.
        """
        if observation.is_generic_slop or observation.specificity_score < 0.40:
            # Check if any evidence record was claimed as authenticated story evidence
            for rec in observation.evidence_records:
                if rec.is_authenticated and rec.kind == EvidenceLineageKind.GUEST_STATED_EVIDENCE:
                    raise ValidationError(
                        f"Archetype '{target_archetype}' cannot manufacture authenticated evidence from generic response."
                    )
