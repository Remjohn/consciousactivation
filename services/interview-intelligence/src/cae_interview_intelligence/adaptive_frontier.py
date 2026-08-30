"""
adaptive_frontier.py
--------------------
Adaptive Question Frontier and Bounded Next-Question Selection Engine (CAE-M06).

Implements bounded adaptive planning for live elicitation:
  `coverage spine + unresolved requirements + latest answer observation + locks`
  `→ eligible candidates (preferred 3, max 5)`
  `→ deterministic selection`
  `→ next QuestionAttempt`.

Allowed next actions:
  `deepen | broaden | reconcile | verify | reframe | advance | close`

Deterministic tie-breaking order:
  1. requirement_coverage
  2. hypothesis_evidence_fit
  3. interactional_fit
  4. composition_compatibility
  5. semantic_novelty
  6. operator_preferences
  7. deterministic_candidate_order
"""

from __future__ import annotations

import copy
import hashlib
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from conscious_activations_interview_composer.errors import ValidationError

from .composer import InterviewBriefComposer
from .domain import (
    DesiredEvidenceClass,
    InterviewBrief,
    InterviewQuestion,
    QuestionStage,
)
from .hypothesis_adapter import (
    CandidateState,
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)
from .question_resolver import (
    AnswerResolution,
    AnswerRoutingProfile,
    CompositionCompatibility,
    EvidenceMode,
    InformationCompleteness,
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
    SocialReferenceFrame,
    TemporalOrientation,
)


class AdaptiveAction(str, Enum):
    """The bounded set of allowed next moves in the interview frontier."""
    DEEPEN = "deepen"        # Escalates specificity when answer is vague, generic, or abstract
    BROADEN = "broaden"      # Explores missing requirement dimensions
    RECONCILE = "reconcile"  # Probes contradiction or discrepancy with known reality
    VERIFY = "verify"        # Validates factual assertions or claims
    REFRAME = "reframe"      # Resets perspective if inquiry is defensive or deadlocked
    ADVANCE = "advance"      # Moves forward to next milestone in coverage spine
    CLOSE = "close"          # Terminates session when requirements are saturated


class RequirementStatus(str, Enum):
    UNRESOLVED = "UNRESOLVED"
    PARTIAL = "PARTIAL"
    SATISFIED = "SATISFIED"
    INVALIDATED = "INVALIDATED"


class EvidenceRequirement(BaseModel):
    """A granular semantic or evidentiary requirement needed by a hypothesis."""
    requirement_id: str = Field(default_factory=lambda: f"req:{uuid.uuid4().hex[:8]}")
    description: str = Field(..., min_length=5)
    target_resolution: AnswerResolution = Field(default=AnswerResolution.EPISODIC)
    status: RequirementStatus = Field(default=RequirementStatus.UNRESOLVED)
    covered_by_turn_ids: List[str] = Field(default_factory=list)


class CoverageSpineItem(BaseModel):
    """A planned milestone in the deterministic interview coverage progression."""
    spine_item_id: str = Field(default_factory=lambda: f"spn:{uuid.uuid4().hex[:8]}")
    stage: QuestionStage = Field(...)
    hypothesis_ref: SemanticRef = Field(...)
    primary_question: QuestionCandidate = Field(...)
    requirements: List[EvidenceRequirement] = Field(default_factory=list)
    is_completed: bool = Field(False)
    is_locked: bool = Field(False)


from .semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)

# Alias for backward-compatibility with adaptive frontier contracts
AnswerObservation = SemanticAcquisitionObservation


class QuestionAttempt(BaseModel):
    """
    A concrete next-question attempt chosen deterministically by the frontier.
    Carries the bounded candidate pool evaluated and the scoring rationale.
    """
    attempt_id: str = Field(default_factory=lambda: f"qa:{uuid.uuid4().hex[:10]}")
    session_id: str = Field(...)
    sequence_number: int = Field(..., ge=1)
    action: AdaptiveAction = Field(...)
    selected_candidate: QuestionCandidate = Field(...)
    candidate_pool: List[QuestionCandidate] = Field(..., min_length=1, max_length=5)
    scoring_breakdown: Dict[str, float] = Field(default_factory=dict)
    rationale: str = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FrontierState(BaseModel):
    """Active in-memory state tracking the coverage spine and question progression."""
    session_id: str = Field(...)
    coverage_spine: List[CoverageSpineItem] = Field(default_factory=list)
    spine_index: int = Field(0, ge=0)
    unresolved_requirements: List[EvidenceRequirement] = Field(default_factory=list)
    history_attempts: List[QuestionAttempt] = Field(default_factory=list)
    history_observations: List[AnswerObservation] = Field(default_factory=list)
    locked_question_ids: Set[str] = Field(default_factory=set)
    is_terminal: bool = Field(False)
    terminal_reason: Optional[str] = None


class AdaptiveQuestionFrontierEngine:
    """
    Deterministic coverage spine + bounded adaptive next-question selection engine.
    Never improvises unconstrained prompts; selects among verified QuestionCandidates.
    """

    def __init__(self, resolver: Optional[QuestionIntelligenceResolver] = None):
        self.resolver = resolver or QuestionIntelligenceResolver()

    def initialize_frontier(
        self,
        *,
        session_id: str,
        candidates: List[HypothesisCandidate],
        locked_candidate_ids: Optional[Set[str]] = None,
    ) -> FrontierState:
        """
        Initializes the deterministic coverage spine from approved hypothesis candidates.
        """
        locked_ids = locked_candidate_ids or set()
        spine_items: List[CoverageSpineItem] = []
        all_requirements: List[EvidenceRequirement] = []

        stages = [
            QuestionStage.ORIENTATION,
            QuestionStage.TENSION_PROBE,
            QuestionStage.CRUCIBLE_EXPOSURE,
            QuestionStage.RESOLUTION_SYNTHESIS,
        ]

        for i, cand in enumerate(candidates):
            stage = stages[i % len(stages)]
            q_prog = self.resolver.resolve_question_program(cand)
            primary_qc = q_prog.candidate_questions[0] if q_prog.candidate_questions else None
            if not primary_qc:
                continue

            reqs = [
                EvidenceRequirement(
                    description=ev,
                    target_resolution=AnswerResolution.EPISODIC if "audit" in ev or "moment" in ev else AnswerResolution.SPECIFIC,
                    status=RequirementStatus.UNRESOLVED,
                )
                for ev in cand.desired_evidence
            ]
            if not reqs:
                reqs = [
                    EvidenceRequirement(
                        description=f"Authentic lived evidence for {cand.collision_statement[:40]}",
                        target_resolution=AnswerResolution.SPECIFIC,
                    )
                ]

            is_locked = (cand.candidate_id in locked_ids) or (cand.state == CandidateState.LOCKED)
            spine_item = CoverageSpineItem(
                stage=stage,
                hypothesis_ref=SemanticRef(object_id=cand.candidate_id),
                primary_question=primary_qc,
                requirements=reqs,
                is_completed=False,
                is_locked=is_locked,
            )
            spine_items.append(spine_item)
            all_requirements.extend(reqs)

        return FrontierState(
            session_id=session_id,
            coverage_spine=spine_items,
            spine_index=0,
            unresolved_requirements=all_requirements,
            history_attempts=[],
            history_observations=[],
            locked_question_ids=locked_ids,
            is_terminal=False,
        )

    def observe_answer(
        self,
        frontier: FrontierState,
        *,
        question_attempt_id: str,
        turn_id: str,
        transcript_text: str,
        resolution: AnswerResolution = AnswerResolution.GENERAL,
        completeness: InformationCompleteness = InformationCompleteness.PARTIAL,
        has_contradiction: bool = False,
        discrepancy_refs: Optional[List[SemanticRef]] = None,
        specificity_score: float = 0.70,
        authenticity_score: float = 0.80,
    ) -> AnswerObservation:
        """
        Ingests a live turn response and produces a structured AnswerObservation.
        Updates requirement resolution state on the active coverage spine.
        """
        # Generic slop detection
        is_slop = (
            specificity_score < 0.40
            or resolution == AnswerResolution.ABSTRACT
            or "as an ai" in transcript_text.lower()
            or len(transcript_text.strip().split()) < 4
        )

        obs = AnswerObservation(
            question_attempt_id=question_attempt_id,
            turn_id=turn_id,
            transcript_text=transcript_text.strip(),
            resolution=resolution,
            completeness=completeness,
            has_contradiction=has_contradiction,
            discrepancy_refs=discrepancy_refs or [],
            is_generic_slop=is_slop,
            specificity_score=specificity_score,
            authenticity_score=authenticity_score,
            provenance=Provenance(
                source_refs=[SemanticRef(object_id=f"turn:{turn_id}")],
                generated_by="cae-interview-intelligence:adaptive-frontier:v1",
            ),
        )

        frontier.history_observations.append(obs)

        # Update requirements for current spine item if evidence was sufficient
        if frontier.spine_index < len(frontier.coverage_spine):
            current_spine = frontier.coverage_spine[frontier.spine_index]
            if completeness in (InformationCompleteness.SUFFICIENT, InformationCompleteness.VERIFIED) and not is_slop:
                for req in current_spine.requirements:
                    req.status = RequirementStatus.SATISFIED
                    req.covered_by_turn_ids.append(turn_id)
            elif completeness == InformationCompleteness.PARTIAL:
                for req in current_spine.requirements:
                    if req.status == RequirementStatus.UNRESOLVED:
                        req.status = RequirementStatus.PARTIAL
                        req.covered_by_turn_ids.append(turn_id)

        return obs

    def evaluate_next_action(self, frontier: FrontierState) -> Tuple[AdaptiveAction, str]:
        """
        Evaluates current state against runtime decision rules to determine the next AdaptiveAction.
        """
        if frontier.is_terminal:
            return AdaptiveAction.CLOSE, "Session is marked terminal."

        if not frontier.history_observations:
            # First question in session
            return AdaptiveAction.ADVANCE, "Initial session kickoff on coverage spine."

        latest_obs = frontier.history_observations[-1]

        # 1. Generic / Abstract Answer -> DEEPEN (Specificity escalation)
        if latest_obs.is_generic_slop or latest_obs.resolution in (AnswerResolution.ABSTRACT, AnswerResolution.GENERAL):
            return (
                AdaptiveAction.DEEPEN,
                f"Observed low resolution ({latest_obs.resolution.value}) or generic slop; escalating specificity.",
            )

        # 2. Contradiction Detected -> RECONCILE
        if latest_obs.has_contradiction or bool(latest_obs.discrepancy_refs):
            return (
                AdaptiveAction.RECONCILE,
                "Observed factual contradiction or prepared discrepancy; reconciling.",
            )

        # 3. Current Milestone Incomplete -> BROADEN or VERIFY
        if frontier.spine_index < len(frontier.coverage_spine):
            current_spine = frontier.coverage_spine[frontier.spine_index]
            unresolved_in_spine = [
                r for r in current_spine.requirements if r.status in (RequirementStatus.UNRESOLVED, RequirementStatus.PARTIAL)
            ]

            if latest_obs.completeness == InformationCompleteness.PARTIAL and unresolved_in_spine:
                return (
                    AdaptiveAction.BROADEN,
                    f"Current milestone requirements partially resolved ({len(unresolved_in_spine)} remaining); expanding breadth.",
                )

            if latest_obs.completeness == InformationCompleteness.SUFFICIENT and unresolved_in_spine:
                return (
                    AdaptiveAction.VERIFY,
                    "Evidence stated but unverified; confirming factual bounds before advancement.",
                )

        # 4. Sufficient / Verified Evidence -> ADVANCE or CLOSE
        if frontier.spine_index + 1 >= len(frontier.coverage_spine):
            frontier.is_terminal = True
            frontier.terminal_reason = "All coverage spine milestones completed and verified."
            return AdaptiveAction.CLOSE, "All milestones in coverage spine satisfied; closing inquiry."

        return (
            AdaptiveAction.ADVANCE,
            f"Current milestone satisfied; advancing to spine index {frontier.spine_index + 1}.",
        )

    def assemble_candidate_pool(
        self,
        frontier: FrontierState,
        action: AdaptiveAction,
    ) -> List[QuestionCandidate]:
        """
        Assembles a bounded pool of 3–5 eligible QuestionCandidates for the determined action.
        Prunes invalid/scripted questions and enforces operator lock priority.
        """
        if frontier.spine_index >= len(frontier.coverage_spine):
            # Fallback closing candidate
            return [
                QuestionCandidate(
                    text="Looking back across everything we discussed today, what is the single biggest lesson you take away?",
                    objective="Synthesize overall reflection and close interview session.",
                )
            ]

        current_spine = frontier.coverage_spine[frontier.spine_index]
        base_qc = current_spine.primary_question

        # If current spine item is locked by operator, prioritize the locked question
        if current_spine.is_locked:
            pool = [base_qc]
            # Add syntactic variations for pool completeness
            for style in ["crucible", "chronology"]:
                alt = self.resolver.regenerate_question_candidate(
                    existing_candidate=base_qc,
                    syntax_style=style,
                )
                pool.append(alt)
            return pool[:3]

        pool: List[QuestionCandidate] = []

        if action == AdaptiveAction.DEEPEN:
            # Generate specificity-escalating probes
            styles = ["crucible", "chronology", "discrepancy"]
            for s in styles:
                qc = self.resolver.regenerate_question_candidate(
                    existing_candidate=base_qc,
                    syntax_style=s,
                    variation_prompt_prefix="Focus on exact physical scene, timestamp, and sensory details.",
                )
                qc.target_resolution = AnswerResolution.EPISODIC
                pool.append(qc)

        elif action == AdaptiveAction.RECONCILE:
            # Generate contradiction/reconciliation probes
            for s in ["discrepancy", "crucible"]:
                qc = self.resolver.regenerate_question_candidate(
                    existing_candidate=base_qc,
                    syntax_style=s,
                    variation_prompt_prefix="Reconcile the stated contradiction between official policy and lived action.",
                )
                qc.target_resolution = AnswerResolution.SPECIFIC
                pool.append(qc)
            # Add third candidate
            qc_alt = self.resolver.regenerate_question_candidate(
                existing_candidate=base_qc,
                syntax_style="chronology",
                variation_prompt_prefix="Compare what was expected against what actually occurred.",
            )
            pool.append(qc_alt)

        elif action == AdaptiveAction.BROADEN:
            # Generate breadth expansion probes
            for s in ["chronology", "crucible"]:
                qc = self.resolver.regenerate_question_candidate(
                    existing_candidate=base_qc,
                    syntax_style=s,
                    variation_prompt_prefix="Expand to the wider organizational context and unaddressed requirements.",
                )
                pool.append(qc)
            pool.append(base_qc)

        elif action == AdaptiveAction.VERIFY:
            # Generate verification probes
            for s in ["discrepancy", "chronology"]:
                qc = self.resolver.regenerate_question_candidate(
                    existing_candidate=base_qc,
                    syntax_style=s,
                    variation_prompt_prefix="Verify exact paper trail, documentation, and specific names.",
                )
                qc.target_resolution = AnswerResolution.EVIDENTIAL
                pool.append(qc)
            pool.append(base_qc)

        elif action == AdaptiveAction.ADVANCE:
            # Target next spine item
            target_spine = current_spine
            if frontier.history_observations and frontier.history_observations[-1].completeness in (
                InformationCompleteness.SUFFICIENT, InformationCompleteness.VERIFIED
            ):
                if frontier.spine_index + 1 < len(frontier.coverage_spine):
                    target_spine = frontier.coverage_spine[frontier.spine_index + 1]

            pool.append(target_spine.primary_question)
            for s in ["crucible", "chronology"]:
                alt = self.resolver.regenerate_question_candidate(
                    existing_candidate=target_spine.primary_question,
                    syntax_style=s,
                )
                pool.append(alt)

        elif action == AdaptiveAction.CLOSE:
            pool = [
                QuestionCandidate(
                    text="Reflecting on this entire journey, what is the ultimate truth you wish the industry understood?",
                    objective="Final synthesis and closing statement.",
                ),
                QuestionCandidate(
                    text="Before we conclude, is there any crucial piece of evidence or nuance we have not yet touched on?",
                    objective="Exhaustion check and closing reflection.",
                ),
                QuestionCandidate(
                    text="What is the one takeaway from your crucible moment that should guide future leaders?",
                    objective="Closing normative synthesis.",
                ),
            ]

        # Filter out any candidates that violate non-scripted rules
        valid_pool: List[QuestionCandidate] = []
        for qc in pool:
            try:
                InterviewBriefComposer.assert_non_scripted_prompt(qc.text)
                valid_pool.append(qc)
            except Exception:
                # Prune invalid/scripted candidate
                continue

        # Ensure bounded between 3 and 5 items
        pad_idx = 0
        while len(valid_pool) < 3:
            pad_idx += 1
            safe_text = (
                f"Reflecting on this from another perspective, walk me through what occurred during "
                f"{current_spine.stage.value.lower().replace('_', ' ')}."
            )
            valid_pool.append(
                QuestionCandidate(
                    question_id=f"qc:pad_{pad_idx}_{current_spine.spine_item_id}",
                    text=safe_text,
                    objective=f"Probe stage {current_spine.stage.value}",
                    target_resolution=AnswerResolution.SPECIFIC,
                )
            )

        return valid_pool[:5]

    def score_and_rank_candidates(
        self,
        frontier: FrontierState,
        candidate_pool: List[QuestionCandidate],
        action: AdaptiveAction,
    ) -> List[Tuple[QuestionCandidate, float, Dict[str, float]]]:
        """
        Scores and deterministically ranks candidates using the 7-tier tie-breaking order:
          1. requirement_coverage (100.0)
          2. hypothesis_evidence_fit (50.0)
          3. interactional_fit (25.0)
          4. composition_compatibility (15.0)
          5. semantic_novelty (10.0)
          6. operator_preferences (5.0)
          7. deterministic_candidate_order (final tie-breaker)
        """
        scored: List[Tuple[QuestionCandidate, float, Dict[str, float]]] = []

        unresolved_req_texts = [
            r.description.lower() for r in frontier.unresolved_requirements if r.status != RequirementStatus.SATISFIED
        ]
        attempted_texts = {a.selected_candidate.text for a in frontier.history_attempts}

        for qc in candidate_pool:
            breakdown: Dict[str, float] = {}

            # 1. Requirement coverage (100.0 max)
            qc_text_lower = qc.text.lower()
            overlap_count = sum(1 for req in unresolved_req_texts if any(w in qc_text_lower for w in req.split()[:3]))
            req_score = min(1.0, (overlap_count + 1) / max(1, len(unresolved_req_texts) + 1))
            breakdown["requirement_coverage"] = req_score * 100.0

            # 2. Hypothesis / Evidence fit (50.0 max)
            fit_score = 0.8
            if action == AdaptiveAction.DEEPEN and qc.target_resolution == AnswerResolution.EPISODIC:
                fit_score = 1.0
            elif action == AdaptiveAction.VERIFY and qc.target_resolution == AnswerResolution.EVIDENTIAL:
                fit_score = 1.0
            elif action == AdaptiveAction.RECONCILE and "contradiction" in qc.objective.lower():
                fit_score = 1.0
            breakdown["hypothesis_evidence_fit"] = fit_score * 50.0

            # 3. Interactional fit (25.0 max)
            inter_score = 1.0 if qc.interactional_fit in ("high_rapport_direct", "confidential_probe") else 0.7
            breakdown["interactional_fit"] = inter_score * 25.0

            # 4. Composition compatibility (15.0 max)
            comp_score = qc.composition_compatibility.compatibility_score
            breakdown["composition_compatibility"] = comp_score * 15.0

            # 5. Semantic novelty (10.0 max)
            novelty_score = 0.2 if qc.text in attempted_texts else 1.0
            breakdown["semantic_novelty"] = novelty_score * 10.0

            # 6. Operator preferences (5.0 max)
            op_score = 1.0 if bool(qc.operator_feedback_refs) or qc.question_id in frontier.locked_question_ids else 0.5
            breakdown["operator_preferences"] = op_score * 5.0

            total_score = sum(breakdown.values())
            scored.append((qc, total_score, breakdown))

        # 7. Deterministic tie-breaking sort: descending score, then ascending question_id / hash
        scored.sort(
            key=lambda x: (
                -round(x[1], 4),
                hashlib.sha256(x[0].question_id.encode("utf-8")).hexdigest(),
            )
        )
        return scored

    def select_next_question(self, frontier: FrontierState) -> QuestionAttempt:
        """
        Executes end-to-end bounded adaptive next-question selection.
        Advances coverage spine when appropriate.
        """
        action, action_rationale = self.evaluate_next_action(frontier)

        # Advance spine index if action is ADVANCE and prior observation was complete
        if action == AdaptiveAction.ADVANCE and frontier.history_observations:
            latest_obs = frontier.history_observations[-1]
            if latest_obs.completeness in (InformationCompleteness.SUFFICIENT, InformationCompleteness.VERIFIED):
                if frontier.spine_index + 1 < len(frontier.coverage_spine):
                    frontier.coverage_spine[frontier.spine_index].is_completed = True
                    frontier.spine_index += 1

        pool = self.assemble_candidate_pool(frontier, action)
        scored = self.score_and_rank_candidates(frontier, pool, action)

        best_qc, best_score, best_breakdown = scored[0]

        attempt = QuestionAttempt(
            session_id=frontier.session_id,
            sequence_number=len(frontier.history_attempts) + 1,
            action=action,
            selected_candidate=best_qc,
            candidate_pool=[s[0] for s in scored],
            scoring_breakdown=best_breakdown,
            rationale=f"Selected via action '{action.value}' (Score: {best_score:.2f}). {action_rationale}",
        )

        frontier.history_attempts.append(attempt)
        return attempt
