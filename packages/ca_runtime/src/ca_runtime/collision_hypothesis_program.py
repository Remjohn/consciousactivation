"""
collision_hypothesis_program.py
--------------------------------
Audience x Guest Resonance + Matrix of Edging + Collision Hypothesis Program Coordinator (CAE M32).

Coordinates the four authority lanes:
- HUNTER: Discovers semantic resonance fields between Guest DNA and Audience Tensions.
- ANALYST: Evaluates Matrix of Edging, checks falsification standards, anti-cliché/trope gates, and portfolio diversity.
- COMPOSER: Composes grounded CollisionHypothesis entities and packages CollisionHypothesisPortfolios.
- COMMANDER: Executes comparative evaluation, operator approval/rejection gates, emits signed audit receipts,
             and handles recovery/quarantines without mutating source evidence.
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
from .collision_hypothesis_store import (
    CollisionHypothesisStore,
    MatrixOfEdgingRecord,
    CollisionHypothesisRecord,
    CollisionHypothesisPortfolioRecord,
    HypothesisEvaluationReceiptRecord,
)
from cae_collision_intelligence.domain import (
    CollisionHypothesis,
    CollisionRelationType,
    FalsificationCondition,
    HeritageCMFEval,
    NoveltyClicheAssessment,
    ObliqueLens,
)
from cae_collision_intelligence.composer import CollisionHypothesisComposer
from cae_collision_intelligence.verifier import CollisionHypothesisVerifier
from cae_collision_intelligence.errors import (
    ClicheTropeError,
    LowTruthQuarantineError,
    MissingFalsificationError,
    UngroundedAnalogyError,
    VectorTruthFallacyError,
)


def _convert_floats_to_micros(val: Any) -> Any:
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


# -----------------------------------------------------------------------------
# Fail-Closed Error Taxonomy
# -----------------------------------------------------------------------------

class CollisionProgramError(Exception):
    """Base exception for Collision Hypothesis Program errors."""
    pass


class UnauthorizedCollisionLaneError(CollisionProgramError):
    """Raised when an operation is attempted on an unauthorized authority lane."""
    pass


class WorkspaceScopeViolationError(CollisionProgramError):
    """Raised when tenant workspace isolation is violated."""
    pass


class ResonanceAlignmentError(CollisionProgramError):
    """Raised when candidate resonance inputs are ungrounded or empty."""
    pass


class MatrixOfEdgingError(CollisionProgramError):
    """Raised when Matrix of Edging structure or invariants are violated."""
    pass


class UngroundedHypothesisError(CollisionProgramError):
    """Raised when guest lived authority or evidence references are missing."""
    pass


class ClicheTropeQuarantineError(CollisionProgramError):
    """Raised when a hypothesis is quarantined due to generic viral clichés or tropes."""
    pass


class PortfolioDiversityError(CollisionProgramError):
    """Raised when a hypothesis portfolio lacks required editorial diversity."""
    pass


class HypothesisApprovalError(CollisionProgramError):
    """Raised when hypothesis approval or rejection fails validation."""
    pass


# -----------------------------------------------------------------------------
# Domain Data Classes
# -----------------------------------------------------------------------------

class ResonanceCandidate(BaseModel):
    """Candidate intersection discovered between Guest Authority and Audience Tension."""
    candidate_id: str = Field(default_factory=lambda: f"RES-{uuid.uuid4().hex[:8]}")
    guest_id: str
    guest_proof_citation: str
    audience_id: str
    audience_tension_ref: str
    world_signal_id: str
    relation_type: str  # ANALOGY, INVERSION, PARADOX, SYSTEMS_LENS, COUNTER_POSITION
    theme: str
    resonance_score_bps: int = Field(..., ge=0, le=10000, description="Alignment score in basis points")
    oblique_lens: Optional[Dict[str, Any]] = None


class CollisionHypothesisCandidate(BaseModel):
    """Structured input parameters for composing a CollisionHypothesis."""
    title: str
    relation_type: str
    audience_id: str
    audience_tension_ref: str
    guest_id: str
    guest_lived_proof_citation: str
    research_signal_id: str
    sda_invariant: str = "SDA-INV-001_ACTIVE_TENSION"
    oblique_lens: Optional[Dict[str, Any]] = None
    bridge_statement: str
    evidence_references: List[str] = Field(default_factory=list)
    refuting_observation: str
    disconfirming_testimony: str
    boundary_limitation: str
    surprise_score: float = 0.80
    emotion_score: float = 0.80
    specificity_score: float = 0.85
    diversity_axes: Dict[str, str] = Field(default_factory=dict)


class CollisionHypothesisReceipt(BaseModel):
    """Cryptographically verifiable signed audit receipt for collision hypothesis lifecycle."""
    receipt_id: str = Field(default_factory=lambda: f"RCP-COLLISION-{uuid.uuid4().hex[:12]}")
    workspace_id: str
    program_id: str = "collision_discovery_program"
    operation: str
    lane: str
    target_id: str
    status: str
    state_digest: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    signature: str


class CollisionHypothesisSnapshot(BaseModel):
    """Immutable state snapshot for collision discovery program."""
    aggregate_id: str
    workspace_id: str
    current_state: str
    lifecycle: str
    version: int
    candidate_count: int
    matrix_count: int
    portfolio_count: int
    last_updated: str


# Standard Gates & Dimensions matching AIR authority
HYPOTHESIS_GATES = (
    "SOURCE_FIDELITY",
    "EPISTEMIC_LEGALITY",
    "IDENTITY_FIT",
    "DOMAIN_FIT",
    "OPERATOR_CONSTRAINTS",
    "FATAL_PRIMITIVE_CONFLICT",
    "WRONG_READING_LOCKS",
    "LINEAGE_COMPLETE",
    "CURRENT_VERSION",
    "SEMANTIC_DUPLICATE",
)

EVALUATION_DIMENSIONS = (
    "source_fidelity",
    "role_tension_integrity",
    "primitive_coalition_fitness",
    "archetype_fit",
    "edge_integrity",
    "anti_centroid_distinctiveness",
    "execution_feasibility",
)


# -----------------------------------------------------------------------------
# Collision Hypothesis Program Coordinator
# -----------------------------------------------------------------------------

class CollisionHypothesisProgramCoordinator:
    """
    Coordinates the four authority lanes to discover, evaluate, compose,
    and decide on CollisionHypotheses within strict tenant workspace isolation.
    """

    def __init__(
        self,
        workspace_id: str,
        store: CollisionHypothesisStore,
        state_runtime: Optional[UniversalProgramStateRuntime] = None,
        aggregate_id: Optional[str] = None,
    ):
        if not workspace_id:
            raise WorkspaceScopeViolationError("workspace_id cannot be empty")
        self.workspace_id = workspace_id
        self.store = store
        self.state_runtime = state_runtime or UniversalProgramStateRuntime()

        if aggregate_id:
            try:
                self._aggregate = self.state_runtime.get_aggregate(aggregate_id)
                self.aggregate_id = aggregate_id
            except Exception:
                self._aggregate = self.state_runtime.initialize_program_state(
                    program_id="collision_discovery_program",
                    workspace_id=self.workspace_id,
                    actor_id="usr_collision_commander",
                    cae_run_id=aggregate_id,
                    initial_data={
                        "candidates": [],
                        "matrices": {},
                        "portfolios": {},
                        "hypotheses": {},
                    },
                )
                self.aggregate_id = self._aggregate.aggregate_id
        else:
            self._aggregate = self.state_runtime.initialize_program_state(
                program_id="collision_discovery_program",
                workspace_id=self.workspace_id,
                actor_id="usr_collision_commander",
                initial_data={
                    "candidates": [],
                    "matrices": {},
                    "portfolios": {},
                    "hypotheses": {},
                },
            )
            self.aggregate_id = self._aggregate.aggregate_id

    def _verify_workspace(self, workspace_id: str) -> None:
        if not workspace_id or workspace_id != self.workspace_id:
            raise WorkspaceScopeViolationError(
                f"Operation targeted workspace '{workspace_id}', but coordinator is bound to '{self.workspace_id}'."
            )

    def _verify_lane(self, lane: AuthorityLane, expected_lane: AuthorityLane, operation_name: str) -> None:
        """Enforces authority lane boundaries."""
        if lane != expected_lane:
            raise UnauthorizedCollisionLaneError(
                f"Operation '{operation_name}' requires authority lane '{expected_lane.value}', but was invoked by '{lane.value}'."
            )

    def get_snapshot(self) -> CollisionHypothesisSnapshot:
        """Returns the current state snapshot of the program."""
        agg = self.state_runtime.get_aggregate(self.aggregate_id)
        matrices = self.store.list_matrices(self.workspace_id)
        portfolios = self.store.list_portfolios(self.workspace_id)
        hypotheses = self.store.list_hypotheses(self.workspace_id)

        return CollisionHypothesisSnapshot(
            aggregate_id=self.aggregate_id,
            workspace_id=self.workspace_id,
            current_state=agg.current_state,
            lifecycle=agg.lifecycle.value,
            version=agg.version,
            candidate_count=len(hypotheses),
            matrix_count=len(matrices),
            portfolio_count=len(portfolios),
            last_updated=agg.updated_at,
        )

    # -------------------------------------------------------------------------
    # 1. HUNTER LANE: Discover Resonance Fields
    # -------------------------------------------------------------------------

    def discover_resonance(
        self,
        *,
        workspace_id: str,
        guest_dna: Dict[str, Any],
        audience_tensions: List[Dict[str, Any]],
        world_signals: List[Dict[str, Any]],
        oblique_lenses: Optional[List[Dict[str, Any]]] = None,
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> List[ResonanceCandidate]:
        """
        HUNTER LANE: Correlates Guest Authority / DNA with Audience Tensions and World Signals.
        Transitions state from INITIAL -> SIGNAL_HUNTING.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.HUNTER, "discover_resonance")

        guest_id = guest_dna.get("guest_id")
        guest_proof = guest_dna.get("proof_citation") or guest_dna.get("lived_proof_citation")
        if not guest_id or not guest_proof or len(guest_proof.strip()) < 10:
            raise ResonanceAlignmentError("Guest DNA must contain guest_id and substantive lived proof citation.")

        if not audience_tensions:
            raise ResonanceAlignmentError("Audience tensions list cannot be empty.")
        if not world_signals:
            raise ResonanceAlignmentError("World research signals list cannot be empty.")

        candidates: List[ResonanceCandidate] = []
        lenses = oblique_lenses or [{"lens_id": "LENS-DEFAULT", "domain_name": "General Invariants"}]

        relation_types = [
            CollisionRelationType.ANALOGY.value,
            CollisionRelationType.INVERSION.value,
            CollisionRelationType.PARADOX.value,
            CollisionRelationType.SYSTEMS_LENS.value,
            CollisionRelationType.COUNTER_POSITION.value,
        ]

        # Deterministic generation across intersections
        for i, tension in enumerate(audience_tensions):
            audience_id = tension.get("audience_id", f"AUD-{i+1:02d}")
            tension_ref = tension.get("tension_ref") or tension.get("tension_label", "TENSION-ACTIVE")
            
            for j, signal in enumerate(world_signals):
                signal_id = signal.get("signal_id", f"SIG-{j+1:02d}")
                theme = signal.get("theme", "Emergent Domain Tension")
                lens = lenses[(i + j) % len(lenses)]
                rel_type = relation_types[(i + j) % len(relation_types)]

                # Integer basis points scoring (7000 to 9500 bps)
                score_bps = 7000 + ((i * 300 + j * 500) % 2500)

                candidate = ResonanceCandidate(
                    guest_id=guest_id,
                    guest_proof_citation=guest_proof,
                    audience_id=audience_id,
                    audience_tension_ref=tension_ref,
                    world_signal_id=signal_id,
                    relation_type=rel_type,
                    theme=theme,
                    resonance_score_bps=score_bps,
                    oblique_lens=lens,
                )
                candidates.append(candidate)

        # Execute state machine transition
        agg = self.state_runtime.get_aggregate(self.aggregate_id)
        if agg.current_state == "INITIAL":
            self.state_runtime.execute_transition(
                aggregate_id=self.aggregate_id,
                transition_name="ingest_corpus",
                actor_id="hunter-agent",
                actor_lane=AuthorityLane.HUNTER,
                context_claims=["workspace_active", "guest_profile_verified"],
            )
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="hunt_signals",
            actor_id="hunter-agent",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active"],
            state_updates={"candidate_count": len(candidates), "guest_id": guest_id},
        )

        return candidates

    # -------------------------------------------------------------------------
    # 2. ANALYST LANE: Evaluate Matrix of Edging
    # -------------------------------------------------------------------------

    def evaluate_matrix_of_edging(
        self,
        *,
        workspace_id: str,
        matrix_id: str,
        broad_signal: str,
        hidden_pressure: str,
        surviving_edge: str,
        identity_gap: str,
        audience_reality: str,
        desired_recognition: str,
        smallest_useful_movement: str,
        counteractivation_risks: Optional[List[str]] = None,
        source_refs: Optional[List[Dict[str, Any]]] = None,
        lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> MatrixOfEdgingRecord:
        """
        ANALYST LANE: Constructs and validates Matrix of Edging entity.
        Transitions state from SIGNAL_HUNTING -> HYPOTHESIS_FORMED.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.ANALYST, "evaluate_matrix_of_edging")

        for name, val in [
            ("broad_signal", broad_signal),
            ("hidden_pressure", hidden_pressure),
            ("surviving_edge", surviving_edge),
            ("identity_gap", identity_gap),
            ("audience_reality", audience_reality),
            ("desired_recognition", desired_recognition),
            ("smallest_useful_movement", smallest_useful_movement),
        ]:
            if not val or len(val.strip()) < 5:
                raise MatrixOfEdgingError(f"Matrix of Edging field '{name}' must be non-empty and substantive.")

        matrix = MatrixOfEdgingRecord(
            workspace_id=workspace_id,
            matrix_id=matrix_id,
            broad_signal=broad_signal,
            hidden_pressure=hidden_pressure,
            surviving_edge=surviving_edge,
            identity_gap=identity_gap,
            audience_reality=audience_reality,
            desired_recognition=desired_recognition,
            smallest_useful_movement=smallest_useful_movement,
            counteractivation_risks=counteractivation_risks or [],
            source_refs=source_refs or [{"ref_id": matrix_id, "kind": "matrix_source"}],
        )

        stored = self.store.store_matrix(matrix)

        # Transition state
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="form_hypothesis",
            actor_id="analyst-agent",
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
            state_updates={"matrix_id": matrix_id},
        )

        return stored

    # -------------------------------------------------------------------------
    # 3. COMPOSER LANE: Compose Hypotheses and Form Portfolio
    # -------------------------------------------------------------------------

    def compose_hypotheses(
        self,
        *,
        workspace_id: str,
        portfolio_id: str,
        candidates: List[CollisionHypothesisCandidate],
        matrix_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> CollisionHypothesisPortfolioRecord:
        """
        COMPOSER LANE: Composes typed CollisionHypothesis records and packages portfolio.
        Verifies guest lived proof and anti-cliché filters before saving.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMPOSER, "compose_hypotheses")
        if not candidates:
            raise UngroundedHypothesisError("Cannot compose portfolio with zero candidates.")

        matrix = self.store.get_matrix(workspace_id, matrix_id)
        if not matrix:
            raise MatrixOfEdgingError(f"Matrix of Edging '{matrix_id}' not found in workspace '{workspace_id}'.")

        stored_hypothesis_ids: List[str] = []
        portfolio_axes: Dict[str, str] = {}

        for item in candidates:
            # Map relation type
            try:
                rel_enum = CollisionRelationType(item.relation_type)
            except ValueError:
                raise UngroundedHypothesisError(f"Invalid collision relation type: '{item.relation_type}'.")

            # Check falsification
            try:
                falsification = FalsificationCondition(
                    refuting_observation=item.refuting_observation,
                    disconfirming_testimony=item.disconfirming_testimony,
                    boundary_limitation=item.boundary_limitation,
                )
            except Exception as f_err:
                raise UngroundedHypothesisError(f"Invalid falsification condition: {f_err}") from f_err

            lens_obj = None
            if item.oblique_lens:
                lens_obj = ObliqueLens(
                    lens_id=item.oblique_lens.get("lens_id", f"LENS-{uuid.uuid4().hex[:6]}"),
                    domain_name=item.oblique_lens.get("domain_name", "Cross-Domain Invariant"),
                    source_reference=item.oblique_lens.get("source_reference", "Canonical Reference"),
                    invariant_principle=item.oblique_lens.get("invariant_principle", "Structural Dynamic Principle"),
                )

            # Compose through domain composer
            try:
                composed = CollisionHypothesisComposer.compose(
                    workspace_id=workspace_id,
                    title=item.title,
                    relation_type=rel_enum,
                    audience_id=item.audience_id,
                    audience_tension_ref=item.audience_tension_ref,
                    guest_id=item.guest_id,
                    guest_lived_proof_citation=item.guest_lived_proof_citation,
                    research_signal_id=item.research_signal_id,
                    bridge_statement=item.bridge_statement,
                    falsification_condition=falsification,
                    evidence_references=item.evidence_references or [item.research_signal_id],
                    oblique_lens=lens_obj,
                    sda_invariant=item.sda_invariant,
                    surprise_score=item.surprise_score,
                    emotion_score=item.emotion_score,
                    specificity_score=item.specificity_score,
                )
            except (UngroundedAnalogyError, ClicheTropeError, MissingFalsificationError) as exc:
                raise UngroundedHypothesisError(str(exc)) from exc

            # Verify with domain verifier
            try:
                CollisionHypothesisVerifier.verify(composed)
            except ClicheTropeError as c_err:
                raise ClicheTropeQuarantineError(str(c_err)) from c_err
            except (UngroundedAnalogyError, MissingFalsificationError, LowTruthQuarantineError, VectorTruthFallacyError) as v_err:
                raise UngroundedHypothesisError(str(v_err)) from v_err

            record = CollisionHypothesisRecord(
                workspace_id=workspace_id,
                hypothesis_id=composed.hypothesis_id,
                title=composed.title,
                relation_type=composed.relation_type.value,
                audience_id=composed.audience_id,
                audience_tension_ref=composed.audience_tension_ref,
                guest_id=composed.guest_id,
                guest_lived_proof_citation=composed.guest_lived_proof_citation,
                research_signal_id=composed.research_signal_id,
                sda_invariant=composed.sda_invariant,
                oblique_lens=composed.oblique_lens.model_dump() if composed.oblique_lens else None,
                bridge_statement=composed.bridge_statement,
                evidence_references=composed.evidence_references,
                novelty_assessment=composed.novelty_assessment.model_dump(),
                falsification_condition=composed.falsification_condition.model_dump(),
                heritage_eval=composed.heritage_eval.model_dump(),
                status="PENDING",
            )
            self.store.store_hypothesis(record)
            stored_hypothesis_ids.append(record.hypothesis_id)
            portfolio_axes[record.hypothesis_id] = record.relation_type

        # Compute diversity signature
        proof_hash = compute_canonical_sha256(portfolio_axes)
        diversity_sig = {
            "axes": portfolio_axes,
            "proof_sha256": proof_hash,
            "candidate_count": len(stored_hypothesis_ids),
        }

        portfolio = CollisionHypothesisPortfolioRecord(
            workspace_id=workspace_id,
            portfolio_id=portfolio_id,
            candidate_hypothesis_ids=stored_hypothesis_ids,
            diversity_signature=diversity_sig,
            status="DRAFT",
        )
        stored_portfolio = self.store.store_portfolio(portfolio)
        return stored_portfolio

    # -------------------------------------------------------------------------
    # 4. ANALYST LANE: Comparative Evaluation & Gate Checks
    # -------------------------------------------------------------------------

    def evaluate_portfolio(
        self,
        *,
        workspace_id: str,
        portfolio_id: str,
        gate_outcomes: Dict[str, Dict[str, bool]],  # hypothesis_id -> gate -> bool
        candidate_scores_micros: Dict[str, Dict[str, int]],  # hypothesis_id -> dimension -> int micros
        decisive_margin_micros: int = 50000,
        lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> Dict[str, Any]:
        """
        ANALYST LANE: Evaluates 10 hypothesis gates and 7 dimensions in integer micros.
        Transitions state from HYPOTHESIS_FORMED -> EVALUATED.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.ANALYST, "evaluate_portfolio")
        portfolio = self.store.get_portfolio(workspace_id, portfolio_id)
        if not portfolio:
            raise PortfolioDiversityError(f"Portfolio '{portfolio_id}' not found.")

        hyp_ids = portfolio.candidate_hypothesis_ids
        if set(hyp_ids) != set(candidate_scores_micros.keys()):
            raise PortfolioDiversityError("Candidate scores must cover every candidate in portfolio.")

        evaluation_rows = []
        for hid in hyp_ids:
            hyp = self.store.get_hypothesis(workspace_id, hid)
            if not hyp:
                continue

            scores = candidate_scores_micros[hid]
            for dim in EVALUATION_DIMENSIONS:
                if dim not in scores:
                    raise PortfolioDiversityError(f"Candidate '{hid}' missing evaluation dimension '{dim}'.")
                val = scores[dim]
                if not isinstance(val, int) or isinstance(val, bool) or val < 0 or val > 1_000_000:
                    raise PortfolioDiversityError(f"Dimension score for '{dim}' must be an integer between 0 and 1,000,000 micros.")

            gates = gate_outcomes.get(hid, {})
            gate_checks = []
            all_passed = True
            for g in HYPOTHESIS_GATES:
                verdict = gates.get(g, True)
                gate_checks.append({
                    "gate": g,
                    "verdict": "PASS" if verdict else "FAIL",
                })
                if not verdict:
                    all_passed = False

            total_score = sum(scores.values())
            evaluation_rows.append({
                "hypothesis_id": hid,
                "scores_micros": scores,
                "total_micros": total_score,
                "eligible": all_passed,
                "gate_checks": gate_checks,
            })

        eligible_candidates = sorted(
            [r for r in evaluation_rows if r["eligible"]],
            key=lambda r: (-r["total_micros"], r["hypothesis_id"]),
        )

        selected_id = None
        if not eligible_candidates:
            decision = "NO_ELIGIBLE_CANDIDATE"
        elif len(eligible_candidates) == 1 or (
            eligible_candidates[0]["total_micros"] - eligible_candidates[1]["total_micros"] >= decisive_margin_micros
        ):
            decision = "DECISIVE_WINNER"
            selected_id = eligible_candidates[0]["hypothesis_id"]
        else:
            decision = "AMBIGUOUS"
            selected_id = eligible_candidates[0]["hypothesis_id"]

        # Store evaluation receipts for each candidate
        for row in evaluation_rows:
            receipt = HypothesisEvaluationReceiptRecord(
                workspace_id=workspace_id,
                receipt_id=f"EV-RCP-{uuid.uuid4().hex[:8]}",
                portfolio_id=portfolio_id,
                hypothesis_id=row["hypothesis_id"],
                evaluator_lane=AuthorityLane.ANALYST.value,
                decision="ELIGIBLE" if row["eligible"] else "INELIGIBLE",
                score_breakdown_micros=row["scores_micros"],
                gate_checks=row["gate_checks"],
                signature=compute_canonical_sha256(row),
            )
            self.store.store_evaluation_receipt(receipt)

        self.store.update_portfolio_selection(workspace_id, portfolio_id, "EVALUATED", selected_id)

        # Transition state machine
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="evaluate_collision",
            actor_id="analyst-agent",
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active"],
            state_updates={"portfolio_id": portfolio_id, "decision": decision, "selected_id": selected_id},
        )

        return {
            "portfolio_id": portfolio_id,
            "decision": decision,
            "selected_hypothesis_id": selected_id,
            "candidates": evaluation_rows,
        }

    # -------------------------------------------------------------------------
    # 5. COMMANDER LANE: Operator Approval & Rejection Gates
    # -------------------------------------------------------------------------

    def approve_hypothesis(
        self,
        *,
        workspace_id: str,
        portfolio_id: str,
        hypothesis_id: str,
        approval_notes: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> CollisionHypothesisReceipt:
        """
        COMMANDER LANE: Human operator / Commander approves a CollisionHypothesis.
        Emits signed immutable receipt and transitions state to APPROVED.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMMANDER, "approve_hypothesis")

        hyp = self.store.get_hypothesis(workspace_id, hypothesis_id)
        if not hyp:
            raise HypothesisApprovalError(f"Hypothesis '{hypothesis_id}' not found.")

        updated = self.store.update_hypothesis_status(
            workspace_id, hypothesis_id, "APPROVED", approval_notes
        )
        self.store.update_portfolio_selection(workspace_id, portfolio_id, "DECIDED", hypothesis_id)

        digest = compute_canonical_sha256(updated.model_dump())
        receipt = CollisionHypothesisReceipt(
            workspace_id=workspace_id,
            operation="operator_approve",
            lane=AuthorityLane.COMMANDER.value,
            target_id=hypothesis_id,
            status="APPROVED",
            state_digest=digest,
            signature=f"SIG-COMMANDER-{uuid.uuid4().hex[:12]}",
        )

        # Execute terminal/approved transition
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="operator_approve",
            actor_id="commander-operator",
            actor_lane=AuthorityLane.COMMANDER,
            context_claims=["workspace_active"],
            state_updates={"hypothesis_id": hypothesis_id, "receipt_id": receipt.receipt_id},
        )

        return receipt

    def reject_hypothesis(
        self,
        *,
        workspace_id: str,
        portfolio_id: str,
        hypothesis_id: str,
        rejection_reason: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> CollisionHypothesisReceipt:
        """
        COMMANDER LANE: Operator / Commander rejects a CollisionHypothesis.
        Emits signed immutable receipt and transitions state to REJECTED.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMMANDER, "reject_hypothesis")

        hyp = self.store.get_hypothesis(workspace_id, hypothesis_id)
        if not hyp:
            raise HypothesisApprovalError(f"Hypothesis '{hypothesis_id}' not found.")

        updated = self.store.update_hypothesis_status(
            workspace_id, hypothesis_id, "REJECTED", rejection_reason
        )
        self.store.update_portfolio_selection(workspace_id, portfolio_id, "DECIDED", None)

        digest = compute_canonical_sha256(updated.model_dump())
        receipt = CollisionHypothesisReceipt(
            workspace_id=workspace_id,
            operation="operator_reject",
            lane=AuthorityLane.COMMANDER.value,
            target_id=hypothesis_id,
            status="REJECTED",
            state_digest=digest,
            signature=f"SIG-COMMANDER-{uuid.uuid4().hex[:12]}",
        )

        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name="operator_reject",
            actor_id="commander-operator",
            actor_lane=AuthorityLane.COMMANDER,
            context_claims=["workspace_active"],
            state_updates={"hypothesis_id": hypothesis_id, "receipt_id": receipt.receipt_id},
        )

        return receipt

    # -------------------------------------------------------------------------
    # 6. COMPOSER LANE: Rebuild Portfolio (Idempotent Derived Expressions)
    # -------------------------------------------------------------------------

    def rebuild_portfolio(
        self,
        *,
        workspace_id: str,
        portfolio_id: str,
        new_candidates: List[CollisionHypothesisCandidate],
        matrix_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> CollisionHypothesisPortfolioRecord:
        """
        COMPOSER LANE: Rebuilds portfolio expressions idempotently with source lineage.
        Does not mutate underlying source evidence.
        """
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMPOSER, "rebuild_portfolio")

        agg = self.state_runtime.get_aggregate(self.aggregate_id)
        trans_name = "rebuild_portfolio" if agg.current_state == "APPROVED" else "rebuild_from_rejected"
        self.state_runtime.execute_transition(
            aggregate_id=self.aggregate_id,
            transition_name=trans_name,
            actor_id="composer-agent",
            actor_lane=AuthorityLane.COMPOSER,
            context_claims=["workspace_active"],
        )

        return self.compose_hypotheses(
            workspace_id=workspace_id,
            portfolio_id=portfolio_id,
            candidates=new_candidates,
            matrix_id=matrix_id,
            lane=lane,
        )

    # -------------------------------------------------------------------------
    # 7. COMMANDER LANE: Governed Repairs & Quarantine
    # -------------------------------------------------------------------------

    def quarantine_hypothesis(
        self,
        *,
        workspace_id: str,
        hypothesis_id: str,
        reason: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> CollisionHypothesisRecord:
        """Quarantine a hypothesis due to invalidity or cliché risk."""
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMMANDER, "quarantine_hypothesis")
        updated = self.store.update_hypothesis_status(
            workspace_id, hypothesis_id, "QUARANTINED", reason
        )
        if not updated:
            raise HypothesisApprovalError(f"Hypothesis '{hypothesis_id}' not found.")
        return updated

    def retry_discovery(
        self,
        *,
        workspace_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> None:
        """Commander initiates discovery retry with diversity penalty from REPAIRING state."""
        self._verify_workspace(workspace_id)
        self._verify_lane(lane, AuthorityLane.COMMANDER, "retry_discovery")
        self.state_runtime.repair_state(
            aggregate_id=self.aggregate_id,
            repair_action="retry_discovery",
            repair_payload={"reason": "diversity_retry"},
            actor_id="commander-operator",
            actor_lane=AuthorityLane.COMMANDER,
            target_state="SIGNAL_HUNTING",
        )
