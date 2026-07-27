from ccp_studio.contracts.provider_runtime import ProviderJobKind, ProviderName, ProviderRole
from ccp_studio.services.provider_capability_profile_service import ProviderCapabilityProfileService
from ccp_studio.services.provider_cost_estimate_service import ProviderCostEstimateService
from ccp_studio.services.provider_decision_log_service import ProviderDecisionLogService
from ccp_studio.services.provider_job_service import ProviderJobService
from ccp_studio.services.provider_retry_policy_service import ProviderRetryPolicyService

class IdeogramProviderRuntimeService:
    def __init__(self):
        self.capabilities = ProviderCapabilityProfileService()
        self.costs = ProviderCostEstimateService()
        self.decisions = ProviderDecisionLogService()
        self.jobs = ProviderJobService()
        self.retries = ProviderRetryPolicyService()

    def compile_scene_sample_job(self, input_payload: dict, source_refs: list[str], operator_approved=True):
        profile = self.capabilities.compile_ideogram_profile(configured=True, tested=True, available=True)
        provider_input = self.jobs.compile_input(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.SCENE_SAMPLE, input_payload, source_refs)
        cost = self.costs.estimate(ProviderName.IDEOGRAM, ProviderJobKind.SCENE_SAMPLE)
        decision = self.decisions.compile_decision(ProviderName.IDEOGRAM, ProviderRole.COMPOSITION_PLATE_GENERATOR, ProviderJobKind.SCENE_SAMPLE, "Generate composition plate sample for operator approval.", cost, "sample", ["local_svg_preview"], operator_approved)
        job = self.jobs.compile_job(provider_input, profile.provider_capability_profile_id, decision, self.retries.strict_sample_policy())
        return profile, job
