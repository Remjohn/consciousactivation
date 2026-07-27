"""Expression Moment review repositories for TS-CMF-032."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.expression_review import (
    ExpressionMoment,
    ExpressionMomentReviewDecision,
    ExpressionMomentStatus,
    ExpressionReviewReceipt,
    SensitivityHold,
)


class ImmutableApprovedMomentError(ValueError):
    pass


@dataclass
class InMemoryExpressionReviewRepository:
    moments: dict[UUID, ExpressionMoment] = field(default_factory=dict)
    decisions: dict[UUID, ExpressionMomentReviewDecision] = field(default_factory=dict)
    sensitivity_holds: dict[UUID, SensitivityHold] = field(default_factory=dict)
    receipts: dict[UUID, ExpressionReviewReceipt] = field(default_factory=dict)

    def put_moment(self, moment: ExpressionMoment) -> ExpressionMoment:
        existing = self.moments.get(moment.expression_moment_id)
        if existing is not None and existing.status == ExpressionMomentStatus.approved:
            allowed_supersession = (
                moment.status == ExpressionMomentStatus.superseded
                and moment.source_quote == existing.source_quote
                and moment.boundary == existing.boundary
                and moment.superseded_by_expression_moment_id is not None
            )
            if not allowed_supersession and moment != existing:
                raise ImmutableApprovedMomentError("approved Expression Moments are immutable except supersession")
        self.moments[moment.expression_moment_id] = moment
        return moment

    def put_decision(self, decision: ExpressionMomentReviewDecision) -> ExpressionMomentReviewDecision:
        self.decisions[decision.review_decision_id] = decision
        return decision

    def put_hold(self, hold: SensitivityHold) -> SensitivityHold:
        self.sensitivity_holds[hold.sensitivity_hold_id] = hold
        return hold

    def put_receipt(self, receipt: ExpressionReviewReceipt) -> ExpressionReviewReceipt:
        self.receipts[receipt.expression_review_receipt_id] = receipt
        return receipt

    def active_hold_for_moment(self, expression_moment_id: UUID) -> SensitivityHold | None:
        return next(
            (
                hold
                for hold in self.sensitivity_holds.values()
                if hold.expression_moment_id == expression_moment_id and hold.active
            ),
            None,
        )
