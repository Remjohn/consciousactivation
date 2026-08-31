"""
manager.py
----------
Operator Selection Manager executing typed editorial actions and emitting decision receipts.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

from .domain import (
    CandidateComparisonItem,
    CandidateComparisonMatrix,
    CandidateLockRecord,
    ConstrainedRegenerationSpec,
    OperatorActionType,
    OperatorDecisionReceipt,
    OperatorSelectionSession,
    SelectedCandidateSnapshot,
)
from .errors import (
    CandidateLockedError,
    EvidenceMutationViolationError,
    InvalidRegenerationSpecError,
    MissingRationaleError,
)


class OperatorSelectionManager:
    """Manages human operator editorial decisions with full auditability and learning receipt emission."""

    @classmethod
    def create_session(cls, *, workspace_id: str, operator_id: str) -> OperatorSelectionSession:
        return OperatorSelectionSession(workspace_id=workspace_id, operator_id=operator_id)

    @classmethod
    def select_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        title: str,
        hook_statement: str,
        priority_rank: int,
        evidence_links: List[Dict[str, Any]],
        rationale: str,
        taste_delta: Optional[str] = None,
        notes: Optional[str] = None,
        version: int = 1,
        predecessor_candidate_id: Optional[str] = None,
    ) -> SelectedCandidateSnapshot:
        """Selects a candidate for production, emitting an audit receipt and creating an immutable snapshot."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator selection requires an explanatory rationale of at least 5 characters.")

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.SELECT,
            rationale=rationale,
            taste_delta=taste_delta,
            predecessor_candidate_id=predecessor_candidate_id,
            version=version,
        )
        session.receipts.append(receipt)

        snapshot = SelectedCandidateSnapshot(
            candidate_id=candidate_id,
            workspace_id=session.workspace_id,
            title=title,
            hook_statement=hook_statement,
            priority_rank=priority_rank,
            version=version,
            predecessor_candidate_id=predecessor_candidate_id,
            status="SELECTED_FOR_PRODUCTION",
            evidence_links=evidence_links,
            approved_by=session.operator_id,
            notes=notes,
        )
        session.approved_snapshots.append(snapshot)
        return snapshot

    @classmethod
    def reject_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        rationale: str,
        taste_delta: Optional[str] = None,
    ) -> OperatorDecisionReceipt:
        """Rejects a candidate, recording the rejection as a permanent learning event."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator rejection requires an explanatory rationale.")

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.REJECT,
            rationale=rationale,
            taste_delta=taste_delta,
        )
        session.receipts.append(receipt)
        return receipt

    @classmethod
    def lock_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        rationale: str,
    ) -> CandidateLockRecord:
        """Locks a candidate against automated mutations or downstream pruning, emitting a LOCK receipt."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator locking requires an explanatory rationale.")

        lock_record = CandidateLockRecord(
            candidate_id=candidate_id,
            workspace_id=session.workspace_id,
            locked_by=session.operator_id,
            rationale=rationale,
        )
        session.locked_candidates.append(lock_record)

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.LOCK,
            rationale=rationale,
        )
        session.receipts.append(receipt)
        return lock_record

    @classmethod
    def compare_candidates(
        cls,
        session: OperatorSelectionSession,
        *,
        candidates: List[Dict[str, Any]],
        rationale: str,
        trade_off_notes: Optional[str] = None,
    ) -> CandidateComparisonMatrix:
        """Generates a side-by-side comparative matrix across multiple candidates with score and evidence deltas."""
        if len(candidates) < 2:
            raise MissingRationaleError("Candidate comparison requires at least 2 candidates.")
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Candidate comparison requires an explanatory rationale.")

        items: List[CandidateComparisonItem] = []
        scores: Dict[str, float] = {}
        segment_map: Dict[str, List[str]] = {}

        for c in candidates:
            cid = c.get("candidate_id", "UNKNOWN")
            composite_score = float(c.get("cmf_composite_score", 0.0))
            score_bps = int(c.get("cmf_score_bps", int(composite_score * 10000)))
            ev_ids = [
                str(link.get("segment_id"))
                for link in c.get("evidence_links", [])
                if link.get("segment_id")
            ]
            
            is_locked = any(l.candidate_id == cid for l in session.locked_candidates)
            is_selected = any(s.candidate_id == cid for s in session.approved_snapshots)

            item = CandidateComparisonItem(
                candidate_id=cid,
                title=str(c.get("title", "")),
                hook_statement=str(c.get("hook_statement", "")),
                candidate_type=str(c.get("candidate_type", "CINEMATIC_STORY")),
                cmf_composite_score=composite_score,
                cmf_score_bps=score_bps,
                dimension_scores={k: float(v) for k, v in c.get("dimension_scores", {}).items()},
                evidence_segment_ids=ev_ids,
                is_selected=is_selected,
                is_locked=is_locked,
            )
            items.append(item)
            scores[cid] = composite_score
            segment_map[cid] = ev_ids

        # Compute score deltas relative to top candidate
        top_cid = max(scores, key=lambda k: scores[k])
        top_score = scores[top_cid]
        score_deltas = {cid: round(scores[cid] - top_score, 4) for cid in scores}

        # Compute pairwise evidence overlaps
        overlap: Dict[str, List[str]] = {}
        for i, c1 in enumerate(items):
            for c2 in items[i + 1 :]:
                common = list(set(c1.evidence_segment_ids) & set(c2.evidence_segment_ids))
                overlap[f"{c1.candidate_id}:{c2.candidate_id}"] = sorted(common)

        matrix = CandidateComparisonMatrix(
            workspace_id=session.workspace_id,
            operator_id=session.operator_id,
            candidates=items,
            score_deltas=score_deltas,
            evidence_overlap=overlap,
            trade_off_notes=trade_off_notes,
        )

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=top_cid,
            action_type=OperatorActionType.COMPARE,
            rationale=rationale,
            metadata={"candidate_ids": [c.candidate_id for c in items], "matrix_id": matrix.matrix_id},
        )
        session.receipts.append(receipt)
        return matrix

    @classmethod
    def request_regeneration(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        guidance: str,
        target_hook_emphasis: Optional[str] = None,
        tone_refinement: Optional[str] = None,
        target_duration_seconds: Optional[int] = None,
        preserve_evidence_segment_ids: Optional[List[str]] = None,
        forbidden_angles: Optional[List[str]] = None,
    ) -> tuple[OperatorDecisionReceipt, ConstrainedRegenerationSpec]:
        """Creates a constrained candidate regeneration specification and logs a REGENERATE receipt."""
        if not guidance or len(guidance.strip()) < 5:
            raise InvalidRegenerationSpecError("Regeneration guidance must be at least 5 characters long.")

        spec = ConstrainedRegenerationSpec(
            predecessor_candidate_id=candidate_id,
            workspace_id=session.workspace_id,
            operator_id=session.operator_id,
            guidance=guidance,
            target_hook_emphasis=target_hook_emphasis,
            tone_refinement=tone_refinement,
            target_duration_seconds=target_duration_seconds,
            preserve_evidence_segment_ids=preserve_evidence_segment_ids or [],
            forbidden_angles=forbidden_angles or [],
        )

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.REGENERATE,
            rationale=guidance,
            predecessor_candidate_id=candidate_id,
            constraints=spec.model_dump(),
        )
        session.receipts.append(receipt)
        return receipt, spec

    @classmethod
    def prioritize_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        priority_rank: int,
        rationale: str,
    ) -> OperatorDecisionReceipt:
        """Updates candidate priority rank with an audit receipt."""
        if priority_rank < 1 or priority_rank > 10:
            raise MissingRationaleError("Priority rank must be between 1 and 10.")
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Prioritization requires an explanatory rationale.")

        for snapshot in session.approved_snapshots:
            if snapshot.candidate_id == candidate_id:
                snapshot.priority_rank = priority_rank

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.PRIORITIZE,
            rationale=rationale,
            metadata={"new_priority_rank": priority_rank},
        )
        session.receipts.append(receipt)
        return receipt

    @classmethod
    def modify_framing(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        new_title: str,
        new_hook: str,
        original_evidence_links: List[Dict[str, Any]],
        modified_evidence_links: List[Dict[str, Any]],
        rationale: str,
    ) -> OperatorDecisionReceipt:
        """Modifies title/hook framing while strictly verifying that evidence text and hashes are unchanged."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator modification requires an explanatory rationale.")

        # Check evidence immutability
        if len(original_evidence_links) != len(modified_evidence_links):
            raise EvidenceMutationViolationError("Cannot add or remove evidence segments during framing modification.")

        for orig, mod in zip(original_evidence_links, modified_evidence_links):
            if orig.get("text_sha256") != mod.get("text_sha256") or orig.get("verbatim_text") != mod.get("verbatim_text"):
                raise EvidenceMutationViolationError(
                    f"Evidence mutation detected: verbatim text or hash was altered for segment '{orig.get('segment_id')}'."
                )

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.MODIFY,
            rationale=rationale,
            metadata={"new_title": new_title, "new_hook": new_hook},
        )
        session.receipts.append(receipt)
        return receipt

