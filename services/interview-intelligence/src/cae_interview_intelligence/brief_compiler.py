"""
brief_compiler.py
-----------------
Compiles Operator-approved hypothesis and question intelligence material into the
existing canonical Activative Interview Brief contract (CAE-M04).

Conforms strictly to TS-APP-COMPOSER-001 and conscious_activations_interview_composer.domain.
Zero parallel brief structures or duplicate schemas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from conscious_activations_interview_composer.domain import (
    MATRIX_SEED_FIELDS,
    make_activative_interview_brief,
)
from conscious_activations_interview_composer.errors import ValidationError

from .composer import InterviewBriefComposer
from .hypothesis_adapter import (
    CandidateState,
    HypothesisCandidate,
    SemanticRef,
)
from .question_resolver import (
    QuestionCandidate,
    QuestionProgramDerived,
)


class ActivativeInterviewBriefCompiler:
    """
    Compiles Operator-approved HypothesisCandidate and QuestionProgramDerived into
    the authoritative canonical activative_interview_brief payload.
    """

    @classmethod
    def compile_brief_payload(
        cls,
        *,
        candidate: HypothesisCandidate,
        question_program: QuestionProgramDerived,
        guest_name: str,
        research_package_ref: Mapping[str, Any],
        composer_authority: Mapping[str, str],
        brand_context_ref: Optional[Mapping[str, Any]] = None,
        voice_dna_ref: Optional[Mapping[str, Any]] = None,
        custom_expression_targets: Optional[List[str]] = None,
        matrix_seed_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Compiles an approved hypothesis and question program into the canonical Brief command payload.
        
        Enforces:
        1. Candidate must be in SELECTED or APPROVED state.
        2. Questions must be non-scripted open-ended prompts.
        3. Operator authority must be provided.
        4. Validates payload via conscious_activations_interview_composer.domain.make_activative_interview_brief.
        """
        # 1. State check
        if candidate.state in (CandidateState.REJECTED, CandidateState.DEFERRED):
            raise ValueError(
                f"Cannot compile brief from candidate in state {candidate.state.value!r}. "
                "Only SELECTED or APPROVED candidates may be compiled into an Activative Interview Brief."
            )

        # 2. Operator Authority check
        for required_auth in ("operator_id", "authority_scope", "assertion_id"):
            if required_auth not in composer_authority or not composer_authority[required_auth]:
                raise ValueError(
                    f"Missing required composer authority field {required_auth!r}. "
                    "Operator authorization is required before compiling Brief."
                )

        # 3. Research Package Ref check
        if not research_package_ref or "object_id" not in research_package_ref or not research_package_ref["object_id"]:
            raise ValueError("Valid research_package_ref with non-blank object_id is required.")

        # 4. Form Planned Questions Sequence
        if not question_program.candidate_questions:
            raise ValueError("question_program must contain at least one QuestionCandidate.")

        planned_questions = []
        for i, q in enumerate(question_program.candidate_questions):
            # Assert non-scripted
            InterviewBriefComposer.assert_non_scripted_prompt(q.text)
            
            act_dir = f"elicit_{q.target_resolution.value}" if hasattr(q, "target_resolution") else "elicit_episodic"
            psych_role = (
                q.social_reference_frame.value
                if hasattr(q, "social_reference_frame")
                else "reluctant_witness"
            )
            planned_questions.append({
                "question_text": q.text,
                "activation_direction": act_dir,
                "psychological_role": psych_role,
            })

        # 5. Build Matrix of Edging Seed from coordinates
        coords = candidate.coordinates
        default_seed: Dict[str, Any] = {
            "psychological_role": coords.d04_guest_lived_authority or "unvarnished_operator",
            "tension": coords.d01_audience_tension or candidate.collision_statement,
            "activation_direction_set": [
                "provoke_unvarnished_truth",
                "expose_systemic_friction",
            ],
            "pressure_path": "progressive_escalation_to_crucible",
            "stance": "curious_and_uncompromising",
            "counteractivation_strategy": "redirect_platitude_to_episodic_receipt",
            "smallest_commitment": "acknowledge_initial_frictional_compromise",
        }
        if matrix_seed_overrides:
            default_seed.update(matrix_seed_overrides)

        # 6. Expression Targets
        expression_targets = custom_expression_targets or [
            "self-recognizing witness",
            "unvarnished crucible evidence",
        ]

        # 7. Format canonical Brief command dictionary
        raw_command: Dict[str, Any] = {
            "research_package_ref": dict(research_package_ref),
            "brand_context_ref": dict(brand_context_ref) if brand_context_ref else None,
            "voice_dna_ref": dict(voice_dna_ref) if voice_dna_ref else None,
            "guest_name": guest_name,
            "tension_hypothesis": candidate.collision_statement,
            "matrix_of_edging_seed": default_seed,
            "planned_questions": planned_questions,
            "expression_targets": expression_targets,
            "composer_authority": dict(composer_authority),
        }

        # 8. Validate against canonical composer domain schema
        return make_activative_interview_brief(**raw_command)

    @classmethod
    def compile_and_store(
        cls,
        *,
        brief_service: Any,
        idempotency_key: str,
        candidate: HypothesisCandidate,
        question_program: QuestionProgramDerived,
        guest_name: str,
        research_package_ref: Mapping[str, Any],
        composer_authority: Mapping[str, str],
        brand_context_ref: Optional[Mapping[str, Any]] = None,
        voice_dna_ref: Optional[Mapping[str, Any]] = None,
        custom_expression_targets: Optional[List[str]] = None,
        matrix_seed_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Compiles the brief payload and stores it via the provided BriefService instance.
        """
        # Format the raw command dictionary expected by BriefService.create_brief
        coords = candidate.coordinates
        default_seed: Dict[str, Any] = {
            "psychological_role": coords.d04_guest_lived_authority or "unvarnished_operator",
            "tension": coords.d01_audience_tension or candidate.collision_statement,
            "activation_direction_set": [
                "provoke_unvarnished_truth",
                "expose_systemic_friction",
            ],
            "pressure_path": "progressive_escalation_to_crucible",
            "stance": "curious_and_uncompromising",
            "counteractivation_strategy": "redirect_platitude_to_episodic_receipt",
            "smallest_commitment": "acknowledge_initial_frictional_compromise",
        }
        if matrix_seed_overrides:
            default_seed.update(matrix_seed_overrides)

        planned_questions = []
        for q in question_program.candidate_questions:
            InterviewBriefComposer.assert_non_scripted_prompt(q.text)
            act_dir = f"elicit_{q.target_resolution.value}" if hasattr(q, "target_resolution") else "elicit_episodic"
            psych_role = (
                q.social_reference_frame.value
                if hasattr(q, "social_reference_frame")
                else "reluctant_witness"
            )
            planned_questions.append({
                "question_text": q.text,
                "activation_direction": act_dir,
                "psychological_role": psych_role,
            })

        command = {
            "research_package_ref": dict(research_package_ref),
            "brand_context_ref": dict(brand_context_ref) if brand_context_ref else None,
            "voice_dna_ref": dict(voice_dna_ref) if voice_dna_ref else None,
            "guest_name": guest_name,
            "tension_hypothesis": candidate.collision_statement,
            "matrix_of_edging_seed": default_seed,
            "planned_questions": planned_questions,
            "expression_targets": custom_expression_targets or ["self-recognizing witness"],
            "composer_authority": dict(composer_authority),
        }

        # Check candidate state
        if candidate.state in (CandidateState.REJECTED, CandidateState.DEFERRED):
            raise ValueError(
                f"Cannot compile brief from candidate in state {candidate.state.value!r}."
            )

        return brief_service.create_brief(command, idempotency_key=idempotency_key)
