"""
operator_studio.py
------------------
Operator Hypothesis & Question Studio implementation for CAE-M05.

Provides the Operator control surface for reviewing, evaluating, editing,
regenerating with locked dimensions, locking, and server-side authorizing candidate
hypotheses and Question Programs before Brief compilation and launch.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional

from pydantic import BaseModel, Field

from conscious_activations_interview_composer.errors import (
    ConflictError,
    NotFoundError,
    ValidationError,
)

from .brief_compiler import ActivativeInterviewBriefCompiler
from .composer import InterviewBriefComposer
from .hypothesis_adapter import (
    CandidateState,
    HypothesisCandidate,
    SemanticRef,
)
from .question_resolver import (
    CompositionCompatibility,
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
)


class OperatorActionType(str, Enum):
    KEEP = "KEEP"
    REJECT = "REJECT"
    EDIT = "EDIT"
    REGENERATE = "REGENERATE"
    DEFER = "DEFER"
    LOCK = "LOCK"
    APPROVE = "APPROVE"


class OperatorFeedback(BaseModel):
    """Structured operator feedback capturing action, rationale, locked dimensions, and authority."""
    action: OperatorActionType
    operator_id: str = Field(..., min_length=1, description="Authoritative operator identifier")
    authority_scope: str = Field(..., min_length=1, description="Scope of authority (e.g., DEV, PRODUCTION)")
    assertion_id: str = Field(..., min_length=1, description="Unique assertion or intent identifier")
    notes: Optional[str] = Field(None, description="Editorial rationale or feedback notes")
    locked_dimensions: List[str] = Field(
        default_factory=lambda: ["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
        description="Dimensions to lock against mutation during regeneration",
    )
    edited_text: Optional[str] = Field(None, description="Custom edited question text when action is EDIT")
    target_version: Optional[int] = Field(None, description="Expected candidate revision for concurrency control")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="RFC3339 timestamp of feedback assertion",
    )


class CandidateReviewItem(BaseModel):
    """Complete presentation entity wrapping candidate, derived Question IR, compatibility, and audit history."""
    candidate: HypothesisCandidate
    question_program: QuestionProgramDerived
    compatibility_view: Optional[CompositionCompatibility] = None
    current_version: int = Field(default=1, description="Revision integer for optimistic concurrency control")
    review_state: CandidateState = Field(default=CandidateState.EVALUATED)
    feedback_history: List[OperatorFeedback] = Field(default_factory=list)
    alternatives: List[QuestionCandidate] = Field(default_factory=list)


class StudioSession(BaseModel):
    """Persistent Studio Review Session tracking review state across a candidate portfolio."""
    session_id: str = Field(..., description="Unique studio session identifier")
    workspace_id: str = Field(..., description="Workspace ID")
    project_id: str = Field(..., description="Project ID")
    guest_name: str = Field(..., description="Target guest name")
    research_package_ref: SemanticRef = Field(..., description="Upstream GuestResearchPackage reference")
    candidates: Dict[str, CandidateReviewItem] = Field(
        default_factory=dict,
        description="Candidate review items keyed by candidate_id",
    )
    created_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    compiled_brief_id: Optional[str] = Field(None, description="Object ID of compiled ActivativeInterviewBrief")
    launch_authorized: bool = Field(default=False, description="Server-side launch authorization flag")


class OperatorStudioService:
    """
    Operator Hypothesis & Question Studio service managing candidate review,
    optimistic concurrency, constrained regeneration, and authorized brief compilation.
    """

    def __init__(self, resolver: Optional[QuestionIntelligenceResolver] = None):
        self.resolver = resolver or QuestionIntelligenceResolver()
        self._sessions: Dict[str, StudioSession] = {}

    def create_session(
        self,
        *,
        workspace_id: str,
        project_id: str,
        guest_name: str,
        research_package_ref: Mapping[str, Any],
        candidates: List[HypothesisCandidate],
        session_id: Optional[str] = None,
    ) -> StudioSession:
        """Initialize a new Operator Studio review session from a working candidate portfolio."""
        sid = session_id or f"studio:sess:{uuid.uuid4().hex[:12]}"
        ref_model = (
            research_package_ref
            if isinstance(research_package_ref, SemanticRef)
            else SemanticRef(
                object_id=research_package_ref["object_id"],
                version=research_package_ref.get("version", "1.0.0"),
                sha256=research_package_ref.get("sha256"),
                object_type="guest_research_package",
            )
        )

        review_items: Dict[str, CandidateReviewItem] = {}
        for cand in candidates:
            q_prog = self.resolver.resolve_question_program(cand)
            item = CandidateReviewItem(
                candidate=cand,
                question_program=q_prog,
                compatibility_view=q_prog.composition_compatibility,
                current_version=1,
                review_state=cand.state,
                feedback_history=[],
                alternatives=[],
            )
            review_items[cand.candidate_id] = item

        session = StudioSession(
            session_id=sid,
            workspace_id=workspace_id,
            project_id=project_id,
            guest_name=guest_name,
            research_package_ref=ref_model,
            candidates=review_items,
        )
        self._sessions[sid] = session
        return session

    def get_session(self, session_id: str) -> StudioSession:
        """Retrieve an existing studio session."""
        if session_id not in self._sessions:
            raise NotFoundError(f"Studio session '{session_id}' not found.")
        return self._sessions[session_id]

    def get_candidate_view(self, session_id: str, candidate_id: str) -> CandidateReviewItem:
        """Retrieve rich candidate presentation metadata for studio inspection."""
        session = self.get_session(session_id)
        if candidate_id not in session.candidates:
            raise NotFoundError(f"Candidate '{candidate_id}' not found in session '{session_id}'.")
        return session.candidates[candidate_id]

    def apply_action(
        self,
        *,
        session_id: str,
        candidate_id: str,
        feedback: OperatorFeedback,
        expected_version: int,
    ) -> CandidateReviewItem:
        """
        Apply structured Operator feedback with optimistic concurrency control.
        """
        item = self.get_candidate_view(session_id, candidate_id)

        # 1. Idempotency check: if action with this assertion_id was already applied, return immediately
        for existing in item.feedback_history:
            if existing.assertion_id == feedback.assertion_id:
                return item

        # 2. Concurrency check: verify revision version
        if item.current_version != expected_version:
            raise ConflictError(
                f"Stale edit conflict: Candidate '{candidate_id}' is at revision {item.current_version}, "
                f"but action targeted revision {expected_version}."
            )

        # 3. Apply state machine transition
        action = feedback.action
        if action == OperatorActionType.KEEP:
            item.review_state = CandidateState.SELECTED
            item.candidate.state = CandidateState.SELECTED

        elif action == OperatorActionType.REJECT:
            item.review_state = CandidateState.REJECTED
            item.candidate.state = CandidateState.REJECTED

        elif action == OperatorActionType.DEFER:
            item.review_state = CandidateState.DEFERRED
            item.candidate.state = CandidateState.DEFERRED

        elif action == OperatorActionType.LOCK:
            item.review_state = CandidateState.LOCKED
            item.candidate.state = CandidateState.LOCKED

        elif action == OperatorActionType.EDIT:
            if not feedback.edited_text or not feedback.edited_text.strip():
                raise ValidationError("edited_text is required when applying EDIT action.")
            
            # Assert non-scripted
            InterviewBriefComposer.assert_non_scripted_prompt(feedback.edited_text.strip())
            
            if item.question_program.candidate_questions:
                item.question_program.candidate_questions[0].text = feedback.edited_text.strip()
            item.review_state = CandidateState.SELECTED
            item.candidate.state = CandidateState.SELECTED
            item.current_version += 1

        elif action == OperatorActionType.REGENERATE:
            # Generate 3-5 bounded alternatives preserving locked dimensions
            locked = feedback.locked_dimensions or [
                "hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence",
            ]
            
            alternatives = []
            syntactic_styles = ["crucible", "chronology", "discrepancy"]
            for style in syntactic_styles:
                alt = self.resolver.regenerate_question_candidate(
                    existing_candidate=item.question_program.candidate_questions[0],
                    syntax_style=style,
                    variation_prompt_prefix=feedback.notes,
                )
                alt.locked_dimensions = list(set(alt.locked_dimensions + locked))
                alternatives.append(alt)
            
            item.alternatives = alternatives
            item.review_state = CandidateState.EVALUATED
            item.current_version += 1


        elif action == OperatorActionType.APPROVE:
            # Verify server-side operator authority
            if not feedback.operator_id or not feedback.authority_scope or not feedback.assertion_id:
                raise ValidationError("Valid operator authority (operator_id, authority_scope, assertion_id) is required to APPROVE.")
            
            if feedback.authority_scope.upper() not in ("DEV", "PRODUCTION"):
                raise ValidationError(f"Invalid authority scope '{feedback.authority_scope}'. Must be 'DEV' or 'PRODUCTION'.")
            
            item.review_state = CandidateState.APPROVED
            item.candidate.state = CandidateState.APPROVED

        # 4. Audit trail and timestamp
        item.feedback_history.append(feedback)
        session = self.get_session(session_id)
        session.updated_at_utc = datetime.now(timezone.utc).isoformat()
        return item

    def assemble_working_portfolio(self, session_id: str) -> List[CandidateReviewItem]:
        """
        Assemble the working portfolio from the session.
        Strictly includes SELECTED, APPROVED, or LOCKED candidates; excludes REJECTED and DEFERRED.
        """
        session = self.get_session(session_id)
        valid_states = (CandidateState.SELECTED, CandidateState.APPROVED, CandidateState.LOCKED)
        return [item for item in session.candidates.values() if item.review_state in valid_states]

    def compile_and_authorize_brief(
        self,
        *,
        session_id: str,
        brief_service: Any,
        idempotency_key: str,
        composer_authority: Mapping[str, str],
        primary_candidate_id: Optional[str] = None,
        brand_context_ref: Optional[Mapping[str, Any]] = None,
        voice_dna_ref: Optional[Mapping[str, Any]] = None,
        custom_expression_targets: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Server-side authorized brief compilation from studio review session.
        """
        session = self.get_session(session_id)

        # 1. Authority validation
        for required in ("operator_id", "authority_scope", "assertion_id"):
            if required not in composer_authority or not composer_authority[required]:
                raise ValidationError(f"Missing required composer authority field '{required}'.")

        # 2. Get working portfolio
        working_items = self.assemble_working_portfolio(session_id)
        if not working_items:
            raise ValidationError("Cannot compile brief: zero approved or selected candidates in studio session.")

        # 3. Resolve primary candidate item
        target_item: Optional[CandidateReviewItem] = None
        if primary_candidate_id:
            if primary_candidate_id not in session.candidates:
                raise NotFoundError(f"Candidate '{primary_candidate_id}' not found in studio session.")
            target_item = session.candidates[primary_candidate_id]
            if target_item.review_state in (CandidateState.REJECTED, CandidateState.DEFERRED):
                raise ValidationError(f"Cannot compile brief: candidate '{primary_candidate_id}' is {target_item.review_state.value}.")
        else:
            # Pick first APPROVED or SELECTED item
            approved_items = [it for it in working_items if it.review_state == CandidateState.APPROVED]
            target_item = approved_items[0] if approved_items else working_items[0]

        # Ensure candidate is approved before compilation
        target_item.candidate.state = CandidateState.APPROVED
        target_item.review_state = CandidateState.APPROVED

        # 4. Compile and store via ActivativeInterviewBriefCompiler
        result = ActivativeInterviewBriefCompiler.compile_and_store(
            brief_service=brief_service,
            idempotency_key=idempotency_key,
            candidate=target_item.candidate,
            question_program=target_item.question_program,
            guest_name=session.guest_name,
            research_package_ref={
                "object_id": session.research_package_ref.object_id,
                "version": session.research_package_ref.version or "1.0.0",
                "sha256": session.research_package_ref.sha256,
            },
            composer_authority=composer_authority,
            brand_context_ref=brand_context_ref,
            voice_dna_ref=voice_dna_ref,
            custom_expression_targets=custom_expression_targets,
        )

        # 5. Authorize session launch
        session.compiled_brief_id = result["object"]["object_id"]
        session.launch_authorized = True
        session.updated_at_utc = datetime.now(timezone.utc).isoformat()
        return result
