from __future__ import annotations

from ccp_studio.contracts.composition_intelligence import (
    CompositionCommanderVerdict,
    CompositionDecisionReceipt,
    CompositionSceneProgram,
    PassStatus,
)


class CompositionCommanderService:
    def authorize(
        self,
        scene_program: CompositionSceneProgram,
        decision_receipt: CompositionDecisionReceipt,
    ) -> CompositionCommanderVerdict:
        blockers = []
        if decision_receipt.pass_status != PassStatus.PASS:
            blockers.extend(decision_receipt.blockers or ["composition_decision_failed"])
        if not decision_receipt.locked:
            blockers.append("composition_not_locked")
        return CompositionCommanderVerdict(
            authorized=not blockers,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
            repair_recommendations=["reduce cognitive load", "lock composition"] if blockers else [],
        )
