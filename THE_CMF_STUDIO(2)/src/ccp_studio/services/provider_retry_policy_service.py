from ccp_studio.contracts.provider_runtime import ProviderRetryPolicy

class ProviderRetryPolicyService:
    def default_policy(self) -> ProviderRetryPolicy:
        return ProviderRetryPolicy(max_attempts=2, retry_backoff_seconds=30)
    def strict_sample_policy(self) -> ProviderRetryPolicy:
        return ProviderRetryPolicy(max_attempts=1, retry_on_sample_rejection=False)
