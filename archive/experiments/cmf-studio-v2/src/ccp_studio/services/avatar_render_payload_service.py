from __future__ import annotations

from ccp_studio.contracts.avatar_performance import AvatarPerformancePlan, AvatarRenderPayload, RuntimeTarget


class AvatarRenderPayloadService:
    def compile_render_payload(
        self,
        *,
        plan: AvatarPerformancePlan,
        runtime_target: RuntimeTarget = RuntimeTarget.REMOTION_LAYER,
        layer_refs: list[str] | None = None,
    ) -> AvatarRenderPayload:
        return AvatarRenderPayload(
            avatar_performance_plan_id=plan.avatar_performance_plan_id,
            runtime_target=runtime_target,
            layer_refs=layer_refs or ["avatar_body_layer", "avatar_face_plate_layer"],
            performance_state_refs=[state.avatar_performance_state_id for state in plan.performance_states],
        )
