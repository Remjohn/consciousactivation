from __future__ import annotations

from ccp_studio.contracts.capability_preflight import (
    CapabilityKind,
    PipelineId,
    SetupOffer,
    ToolSupportEnvelope,
)


class ToolSupportRegistryService:
    def required_capabilities_for_pipeline(self, pipeline_id: PipelineId) -> list[str]:
        mapping = {
            PipelineId.FORMAT02_GOLDEN_PATH: [
                "runtime:python",
                "tool:storage:artifact_store",
            ],
            PipelineId.FORMAT02_PROVIDER_SCENE_BATCH: [
                "provider:image:ideogram",
                "provider:image:flux",
                "tool:storage:artifact_store",
            ],
            PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION: [
                "provider:image:ideogram",
                "provider:image:flux",
                "tool:storage:artifact_store",
            ],
            PipelineId.VIDEO_REAL_RENDER: [
                "runtime:render:remotion",
                "runtime:finish:ffmpeg",
                "runtime:worker:local_render_worker",
            ],
            PipelineId.TEMPLATE_PREVIEW: [
                "runtime:render:remotion",
                "tool:storage:artifact_store",
            ],
        }
        return mapping[pipeline_id]

    def optional_capabilities_for_pipeline(self, pipeline_id: PipelineId) -> list[str]:
        mapping = {
            PipelineId.FORMAT02_GOLDEN_PATH: ["runtime:render:remotion", "runtime:finish:ffmpeg"],
            # Optional workflow providers are intentionally not required for PASS.
            # They can be displayed later by provider menu expansion without degrading the core batch path.
            PipelineId.FORMAT02_PROVIDER_SCENE_BATCH: [],
            PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION: [],
            PipelineId.VIDEO_REAL_RENDER: [],
            PipelineId.TEMPLATE_PREVIEW: ["runtime:render:hyperframes"],
        }
        return mapping[pipeline_id]

    def default_setup_offer(self, capability_id: str, optional: bool = False) -> SetupOffer:
        return SetupOffer(
            capability_id=capability_id,
            title=f"Configure {capability_id}",
            steps=[
                f"Add configuration for {capability_id}.",
                "Run capability preflight again.",
                "Approve sample before batch if this capability executes a provider job.",
            ],
            optional=optional,
        )

    def make_tool_support(
        self,
        *,
        capability_id: str,
        configured: bool,
        available: bool,
        required: bool,
        display_name: str | None = None,
        kind: CapabilityKind = CapabilityKind.TOOL,
        supports: list[str] | None = None,
        degraded: bool = False,
        missing_reasons: list[str] | None = None,
        setup_offer_id: str | None = None,
    ) -> ToolSupportEnvelope:
        return ToolSupportEnvelope(
            capability_id=capability_id,
            kind=kind,
            display_name=display_name or capability_id,
            configured=configured,
            available=available,
            required=required,
            degraded=degraded,
            missing_reasons=missing_reasons or [],
            supports=supports or [],
            setup_offer_id=setup_offer_id,
        )
