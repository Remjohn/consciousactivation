from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AvatarContinuityReceipt,
    AvatarFormatFitReceipt,
    AvatarFormatUse,
    AvatarPerformancePlan,
    AvatarPerformanceReceipt,
    AvatarUncannyRiskReceipt,
    PassStatus,
)


class AvatarPerformanceEvalService:
    def evaluate_performance_plan(self, plan: AvatarPerformancePlan) -> AvatarPerformanceReceipt:
        blockers = []
        if plan.lip_sync_enabled:
            blockers.append("lip_sync_enabled")
        if not plan.performance_states:
            blockers.append("missing_performance_states")
        return AvatarPerformanceReceipt(
            avatar_performance_plan_id=plan.avatar_performance_plan_id,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )

    def evaluate_continuity(
        self,
        *,
        avatar_id: str,
        identity_anchors_preserved: bool = True,
        expression_plate_set_consistent: bool = True,
        body_rig_consistent: bool = True,
    ) -> AvatarContinuityReceipt:
        passing = identity_anchors_preserved and expression_plate_set_consistent and body_rig_consistent
        return AvatarContinuityReceipt(
            avatar_id=avatar_id,
            identity_anchors_preserved=identity_anchors_preserved,
            expression_plate_set_consistent=expression_plate_set_consistent,
            body_rig_consistent=body_rig_consistent,
            pass_status=PassStatus.PASS if passing else PassStatus.FAIL,
        )

    def evaluate_uncanny_risk(
        self,
        *,
        avatar_id: str,
        face_morphing_detected: bool = False,
        lip_sync_detected: bool = False,
        mouth_flap_detected: bool = False,
        mismatched_lighting_detected: bool = False,
    ) -> AvatarUncannyRiskReceipt:
        return AvatarUncannyRiskReceipt(
            avatar_id=avatar_id,
            face_morphing_detected=face_morphing_detected,
            lip_sync_detected=lip_sync_detected,
            mouth_flap_detected=mouth_flap_detected,
            mismatched_lighting_detected=mismatched_lighting_detected,
        )

    def evaluate_format_fit(
        self,
        *,
        format_use: AvatarFormatUse,
        avatar_usage_role: str,
        rationale: str,
        allowed: bool = True,
    ) -> AvatarFormatFitReceipt:
        return AvatarFormatFitReceipt(
            format_use=format_use,
            avatar_usage_role=avatar_usage_role,
            pass_status=PassStatus.PASS if allowed else PassStatus.FAIL,
            rationale=rationale,
        )
