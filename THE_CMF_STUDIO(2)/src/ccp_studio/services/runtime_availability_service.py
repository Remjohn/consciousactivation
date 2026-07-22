from __future__ import annotations

from ccp_studio.contracts.capability_preflight import RuntimeAvailabilityReport, RuntimeName


class RuntimeAvailabilityService:
    def compile_runtime_report(
        self,
        *,
        runtime_name: RuntimeName,
        capability_id: str,
        configured: bool,
        available: bool,
        version: str | None = None,
        executable_path: str | None = None,
        supports: list[str] | None = None,
        degraded_reasons: list[str] | None = None,
        setup_offer_id: str | None = None,
    ) -> RuntimeAvailabilityReport:
        return RuntimeAvailabilityReport(
            runtime_name=runtime_name,
            capability_id=capability_id,
            configured=configured,
            available=available,
            version=version,
            executable_path=executable_path,
            supports=supports or [],
            degraded_reasons=degraded_reasons or [],
            setup_offer_id=setup_offer_id,
        )

    def compile_default_runtime_reports(
        self,
        *,
        remotion_configured: bool = False,
        remotion_available: bool = False,
        ffmpeg_configured: bool = False,
        ffmpeg_available: bool = False,
        local_worker_configured: bool = False,
        local_worker_available: bool = False,
        python_configured: bool = True,
        python_available: bool = True,
    ) -> list[RuntimeAvailabilityReport]:
        return [
            self.compile_runtime_report(
                runtime_name=RuntimeName.PYTHON,
                capability_id="runtime:python",
                configured=python_configured,
                available=python_available,
                supports=["fake_render", "contract_validation"],
            ),
            self.compile_runtime_report(
                runtime_name=RuntimeName.REMOTION,
                capability_id="runtime:render:remotion",
                configured=remotion_configured,
                available=remotion_available,
                supports=["video_render", "template_preview"],
            ),
            self.compile_runtime_report(
                runtime_name=RuntimeName.FFMPEG,
                capability_id="runtime:finish:ffmpeg",
                configured=ffmpeg_configured,
                available=ffmpeg_available,
                supports=["finish", "loudness", "scale"],
            ),
            self.compile_runtime_report(
                runtime_name=RuntimeName.LOCAL_RENDER_WORKER,
                capability_id="runtime:worker:local_render_worker",
                configured=local_worker_configured,
                available=local_worker_available,
                supports=["proxy_render", "final_render"],
            ),
        ]
