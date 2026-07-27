from __future__ import annotations

from ccp_studio.contracts.capability_preflight import (
    CostEstimate,
    ProviderAvailabilityReport,
    ProviderMenuSummary,
    ProviderName,
    ProviderRole,
)


class ProviderMenuService:
    def compile_provider_report(
        self,
        *,
        provider_name: ProviderName,
        provider_role: ProviderRole,
        capability_id: str,
        configured: bool,
        available: bool,
        missing_secrets: list[str] | None = None,
        degraded_reasons: list[str] | None = None,
        sample_required: bool = True,
        sample_approved: bool = False,
        batch_requested: bool = False,
        min_cost_usd: float = 0.0,
        max_cost_usd: float = 0.0,
        setup_offer_id: str | None = None,
    ) -> ProviderAvailabilityReport:
        return ProviderAvailabilityReport(
            provider_name=provider_name,
            provider_role=provider_role,
            capability_id=capability_id,
            configured=configured,
            available=available,
            missing_secrets=missing_secrets or [],
            degraded_reasons=degraded_reasons or [],
            sample_required=sample_required,
            sample_approved=sample_approved,
            batch_requested=batch_requested,
            estimated_cost=CostEstimate(min_usd=min_cost_usd, max_usd=max_cost_usd, unit="provider_job"),
            setup_offer_id=setup_offer_id,
        )

    def compile_default_provider_menu(
        self,
        *,
        ideogram_configured: bool = False,
        ideogram_available: bool = False,
        flux_configured: bool = False,
        flux_available: bool = False,
        sample_approved: bool = False,
        batch_requested: bool = False,
    ) -> ProviderMenuSummary:
        reports = [
            self.compile_provider_report(
                provider_name=ProviderName.IDEOGRAM,
                provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR,
                capability_id="provider:image:ideogram",
                configured=ideogram_configured,
                available=ideogram_available,
                missing_secrets=[] if ideogram_configured else ["IDEOGRAM_API_KEY"],
                sample_required=True,
                sample_approved=sample_approved,
                batch_requested=batch_requested,
                min_cost_usd=0.05,
                max_cost_usd=0.25,
            ),
            self.compile_provider_report(
                provider_name=ProviderName.FLUX,
                provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
                capability_id="provider:image:flux",
                configured=flux_configured,
                available=flux_available,
                missing_secrets=[] if flux_configured else ["BFL_API_KEY"],
                sample_required=True,
                sample_approved=sample_approved,
                batch_requested=batch_requested,
                min_cost_usd=0.05,
                max_cost_usd=0.30,
            ),
        ]
        return ProviderMenuSummary(provider_reports=reports)

    def compile_menu(self, reports: list[ProviderAvailabilityReport]) -> ProviderMenuSummary:
        return ProviderMenuSummary(provider_reports=reports)
