from ccp_studio.contracts.provider_runtime import ProviderCostEstimate, ProviderDecisionLog, ProviderJobKind, ProviderName, ProviderRole

class ProviderDecisionLogService:
    def compile_decision(self, provider_name: ProviderName, provider_role: ProviderRole, job_kind: ProviderJobKind, decision_reason: str, cost_estimate: ProviderCostEstimate, sample_or_batch: str, alternatives_considered=None, operator_approved=False):
        return ProviderDecisionLog(provider_name=provider_name, provider_role=provider_role, job_kind=job_kind, decision_reason=decision_reason, alternatives_considered=alternatives_considered or [], sample_or_batch=sample_or_batch, operator_approved=operator_approved, cost_estimate=cost_estimate)
