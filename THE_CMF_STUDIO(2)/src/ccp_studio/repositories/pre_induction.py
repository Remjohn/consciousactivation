"""Pre-induction repositories for TS-CMF-026."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.pre_induction import (
    LiveInterviewModeBinding,
    OperatorEdit,
    PreInductionPlan,
    PreInductionReceipt,
)


@dataclass
class InMemoryPreInductionRepository:
    plans: dict[UUID, PreInductionPlan] = field(default_factory=dict)
    edits: dict[UUID, OperatorEdit] = field(default_factory=dict)
    receipts: dict[UUID, PreInductionReceipt] = field(default_factory=dict)
    bindings: dict[UUID, LiveInterviewModeBinding] = field(default_factory=dict)

    def put_plan(self, plan: PreInductionPlan) -> PreInductionPlan:
        self.plans[plan.pre_induction_plan_id] = plan
        return plan

    def put_edit(self, edit: OperatorEdit) -> OperatorEdit:
        self.edits[edit.operator_edit_id] = edit
        return edit

    def put_receipt(self, receipt: PreInductionReceipt) -> PreInductionReceipt:
        self.receipts[receipt.pre_induction_receipt_id] = receipt
        return receipt

    def put_binding(self, binding: LiveInterviewModeBinding) -> LiveInterviewModeBinding:
        self.bindings[binding.live_interview_mode_binding_id] = binding
        return binding
