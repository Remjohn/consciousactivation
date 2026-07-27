from __future__ import annotations

from ccp_studio.contracts.capability_preflight import (
    CapabilityKind,
    CapabilityPreflightReport,
    CapabilityState,
    MissingCapabilityBlocker,
    PipelineCapabilityStatus,
    PipelineId,
    PreflightPassStatus,
)
from ccp_studio.repositories.capability_preflight import InMemoryCapabilityPreflightRepository
from ccp_studio.services.provider_menu_service import ProviderMenuService
from ccp_studio.services.runtime_availability_service import RuntimeAvailabilityService
from ccp_studio.services.tool_support_registry_service import ToolSupportRegistryService


class CapabilityPreflightService:
    def __init__(
        self,
        repository: InMemoryCapabilityPreflightRepository | None = None,
        provider_menu_service: ProviderMenuService | None = None,
        runtime_service: RuntimeAvailabilityService | None = None,
        tool_registry_service: ToolSupportRegistryService | None = None,
    ):
        self.repository = repository or InMemoryCapabilityPreflightRepository()
        self.provider_menu = provider_menu_service or ProviderMenuService()
        self.runtime = runtime_service or RuntimeAvailabilityService()
        self.tools = tool_registry_service or ToolSupportRegistryService()

    def run_preflight(
        self,
        *,
        pipeline_id: PipelineId,
        ideogram_configured: bool = False,
        ideogram_available: bool = False,
        flux_configured: bool = False,
        flux_available: bool = False,
        remotion_configured: bool = False,
        remotion_available: bool = False,
        ffmpeg_configured: bool = False,
        ffmpeg_available: bool = False,
        local_worker_configured: bool = False,
        local_worker_available: bool = False,
        artifact_store_configured: bool = True,
        artifact_store_available: bool = True,
        sample_approved: bool = False,
        batch_requested: bool = False,
    ) -> CapabilityPreflightReport:
        required = self.tools.required_capabilities_for_pipeline(pipeline_id)
        optional = self.tools.optional_capabilities_for_pipeline(pipeline_id)

        provider_menu = self.provider_menu.compile_default_provider_menu(
            ideogram_configured=ideogram_configured,
            ideogram_available=ideogram_available,
            flux_configured=flux_configured,
            flux_available=flux_available,
            sample_approved=sample_approved,
            batch_requested=batch_requested,
        )
        runtime_reports = self.runtime.compile_default_runtime_reports(
            remotion_configured=remotion_configured,
            remotion_available=remotion_available,
            ffmpeg_configured=ffmpeg_configured,
            ffmpeg_available=ffmpeg_available,
            local_worker_configured=local_worker_configured,
            local_worker_available=local_worker_available,
        )
        setup_offers = []
        blockers = []

        provider_by_cap = {report.capability_id: report for report in provider_menu.provider_reports}
        runtime_by_cap = {report.capability_id: report for report in runtime_reports}

        tool_support = []
        all_caps = list(dict.fromkeys(required + optional + ["tool:storage:artifact_store"]))
        for cap in all_caps:
            required_cap = cap in required
            if cap == "tool:storage:artifact_store":
                configured = artifact_store_configured
                available = artifact_store_available
                missing = [] if configured and available else ["artifact store not configured or unavailable"]
                kind = CapabilityKind.STORAGE
            elif cap in provider_by_cap:
                report = provider_by_cap[cap]
                configured = report.configured
                available = report.available
                missing = report.missing_secrets or ([] if report.available else [f"{cap} unavailable"])
                kind = CapabilityKind.PROVIDER
            elif cap in runtime_by_cap:
                report = runtime_by_cap[cap]
                configured = report.configured
                available = report.available
                missing = [] if report.available else [f"{cap} unavailable"]
                kind = CapabilityKind.RUNTIME
            else:
                configured = False
                available = False
                missing = [f"{cap} not registered"]
                kind = CapabilityKind.TOOL

            setup_offer_id = None
            if not configured or not available:
                offer = self.tools.default_setup_offer(cap, optional=not required_cap)
                setup_offers.append(offer)
                setup_offer_id = offer.setup_offer_id

            envelope = self.tools.make_tool_support(
                capability_id=cap,
                configured=configured,
                available=available,
                required=required_cap,
                kind=kind,
                missing_reasons=missing,
                setup_offer_id=setup_offer_id,
            )
            tool_support.append(envelope)

        available_required = [env.capability_id for env in tool_support if env.required and env.state == CapabilityState.AVAILABLE]
        missing_required = [env.capability_id for env in tool_support if env.required and env.state == CapabilityState.MISSING]
        degraded_required = [env.capability_id for env in tool_support if env.required and env.state == CapabilityState.DEGRADED]
        optional_missing = [env.capability_id for env in tool_support if (not env.required) and env.state in {CapabilityState.MISSING, CapabilityState.DEGRADED, CapabilityState.UNAVAILABLE}]

        batch_blocked = provider_menu.blocked_count > 0
        for cap in missing_required:
            offer = next((o for o in setup_offers if o.capability_id == cap), None)
            blockers.append(MissingCapabilityBlocker(
                capability_id=cap,
                reason=f"Required capability {cap} is missing",
                blocks_pipeline=True,
                setup_offer_id=offer.setup_offer_id if offer else None,
            ))
        if batch_blocked:
            blockers.append(MissingCapabilityBlocker(
                capability_id="sample_approval",
                reason="Batch requested before required sample approval",
                blocks_pipeline=True,
            ))

        if blockers:
            pass_status = PreflightPassStatus.BLOCKED
        elif degraded_required or optional_missing:
            pass_status = PreflightPassStatus.DEGRADED
        else:
            pass_status = PreflightPassStatus.PASS

        pipeline_status = PipelineCapabilityStatus(
            pipeline_id=pipeline_id,
            pass_status=pass_status,
            required_capability_ids=required,
            available_required_capability_ids=available_required,
            missing_required_capability_ids=missing_required,
            degraded_required_capability_ids=degraded_required,
            optional_missing_capability_ids=optional_missing,
            batch_blocked=batch_blocked,
            sample_required=provider_menu.sample_required,
            sample_approved=provider_menu.sample_approved,
        )
        report = CapabilityPreflightReport(
            pipeline_id=pipeline_id,
            pipeline_status=pipeline_status,
            provider_menu_summary=provider_menu,
            runtime_reports=runtime_reports,
            tool_support=tool_support,
            setup_offers=setup_offers,
            missing_blockers=blockers,
        )
        self.repository.upsert("reports", report.capability_preflight_report_id, report)
        self.repository.upsert("provider_menus", provider_menu.provider_menu_summary_id, provider_menu)
        for runtime_report in runtime_reports:
            self.repository.upsert("runtime_reports", runtime_report.runtime_availability_report_id, runtime_report)
        for offer in setup_offers:
            self.repository.upsert("setup_offers", offer.setup_offer_id, offer)
        return report
