from ccp_studio.contracts.provider_runtime import ProviderCostEstimate, ProviderJobKind, ProviderName

class ProviderCostEstimateService:
    def estimate(self, provider_name: ProviderName, job_kind: ProviderJobKind, unit_count: int = 1) -> ProviderCostEstimate:
        low, high = {ProviderName.IDEOGRAM: (0.05, 0.25), ProviderName.FLUX: (0.05, 0.30)}[provider_name]
        return ProviderCostEstimate(provider_name=provider_name, job_kind=job_kind, unit_count=unit_count, min_usd=low*unit_count, max_usd=high*unit_count, notes="Deterministic estimate only.")
