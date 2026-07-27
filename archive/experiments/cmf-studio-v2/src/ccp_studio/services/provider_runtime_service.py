from ccp_studio.contracts.provider_runtime import ProviderCostEstimate, ProviderJobKind, ProviderRuntimePlan
from ccp_studio.services.provider_sample_approval_service import ProviderSampleApprovalService

class ProviderRuntimeService:
    def __init__(self):
        self.samples = ProviderSampleApprovalService()

    def compile_runtime_plan(self, provider_jobs: list, sample_gate, unit_count: int = 1) -> ProviderRuntimePlan:
        batch_requested = any(job.job_kind in {ProviderJobKind.COMPOSITION_PLATE_BATCH, ProviderJobKind.REFERENCE_EDIT_BATCH} or job.batch_requested for job in provider_jobs)
        batch_policy = self.samples.compile_batch_policy_receipt(gate=sample_gate, batch_requested=batch_requested)
        total_min = sum(job.decision_log.cost_estimate.min_usd for job in provider_jobs)
        total_max = sum(job.decision_log.cost_estimate.max_usd for job in provider_jobs)
        estimate = ProviderCostEstimate(provider_name=provider_jobs[0].provider_name, job_kind=provider_jobs[0].job_kind, unit_count=unit_count, min_usd=total_min, max_usd=total_max, notes="Aggregate provider runtime plan estimate.")
        return ProviderRuntimePlan(provider_jobs=provider_jobs, sample_approval_gate=sample_gate, batch_policy_receipt=batch_policy, estimated_total_cost=estimate)
