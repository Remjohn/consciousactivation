from __future__ import annotations

from ccp_studio.contracts.avatar_performance import (
    AudienceProxyPerformancePlan,
    AudienceProxyPersona,
    AudienceProxyPersonaSpec,
    AudienceProxyState,
    AvatarFormatUse,
    EdgeBand,
    MockingRisk,
)


class AudienceProxyService:
    def create_canonical_personas(self) -> list[AudienceProxyPersonaSpec]:
        return [
            AudienceProxyPersonaSpec(
                persona=AudienceProxyPersona.CONFUSED_SEEKER,
                visual_description="small paper figure with question mark and tilted posture",
                inner_line="Wait, what am I supposed to believe?",
                primitive_function="clarity_seeking",
                default_sfl_function="relevant_open_question",
                allowed_formats=[AvatarFormatUse.FORMAT_02, AvatarFormatUse.FORMAT_03, AvatarFormatUse.CAROUSEL, AvatarFormatUse.SUPERVISUAL],
            ),
            AudienceProxyPersonaSpec(
                persona=AudienceProxyPersona.OVERWHELMED_DOER,
                visual_description="small paper figure carrying too many cards with rain cloud",
                inner_line="I'm trying everything and still feel stuck.",
                primitive_function="relief",
                default_sfl_function="pressure_visibility",
                allowed_formats=[AvatarFormatUse.FORMAT_01, AvatarFormatUse.FORMAT_02, AvatarFormatUse.CAROUSEL],
            ),
            AudienceProxyPersonaSpec(
                persona=AudienceProxyPersona.SKEPTICAL_PROTECTOR,
                visual_description="small paper figure with magnifying glass and crossed arms",
                inner_line="Show me the evidence.",
                primitive_function="discernment",
                default_sfl_function="proof_demand",
                allowed_formats=[AvatarFormatUse.FORMAT_02, AvatarFormatUse.FORMAT_03, AvatarFormatUse.FORMAT_04, AvatarFormatUse.CAROUSEL],
            ),
            AudienceProxyPersonaSpec(
                persona=AudienceProxyPersona.GENTLE_BUILDER,
                visual_description="small paper figure watering seedling or holding checklist",
                inner_line="Okay, what do I do next?",
                primitive_function="progress",
                default_sfl_function="expected_future_value",
                allowed_formats=[AvatarFormatUse.FORMAT_02, AvatarFormatUse.CAROUSEL, AvatarFormatUse.SUPERVISUAL],
            ),
        ]

    def create_proxy_state(
        self,
        *,
        persona: AudienceProxyPersona,
        state_name: str,
        primitive_function: str,
        sfl_function: str,
        edge_band: EdgeBand = EdgeBand.GENTLE_RECOGNITION,
        mocking_risk: MockingRisk = MockingRisk.LOW,
    ) -> AudienceProxyState:
        return AudienceProxyState(
            persona=persona,
            state_name=state_name,
            primitive_function=primitive_function,
            sfl_function=sfl_function,
            edge_band=edge_band,
            mocking_risk=mocking_risk,
        )

    def compile_performance_plan(
        self,
        *,
        scene_id: str,
        persona: AudienceProxyPersona,
        state_name: str,
        primitive_function: str,
        sfl_function: str,
        start_ms: int = 0,
        end_ms: int = 900,
    ) -> AudienceProxyPerformancePlan:
        return AudienceProxyPerformancePlan(
            scene_id=scene_id,
            persona=persona,
            state_name=state_name,
            primitive_function=primitive_function,
            sfl_function=sfl_function,
            start_ms=start_ms,
            end_ms=end_ms,
        )
