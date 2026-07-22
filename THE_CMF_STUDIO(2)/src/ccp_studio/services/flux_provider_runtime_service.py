from ccp_studio.contracts.provider_runtime import ProviderJobKind, ProviderName, ProviderRole
from ccp_studio.services.provider_capability_profile_service import ProviderCapabilityProfileService
from ccp_studio.services.provider_cost_estimate_service import ProviderCostEstimateService
from ccp_studio.services.provider_decision_log_service import ProviderDecisionLogService
from ccp_studio.services.provider_job_service import ProviderJobService
from ccp_studio.services.provider_retry_policy_service import ProviderRetryPolicyService

class FluxProviderRuntimeService:
    def __init__(self):
        self.capabilities = ProviderCapabilityProfileService()
        self.costs = ProviderCostEstimateService()
        self.decisions = ProviderDecisionLogService()
        self.jobs = ProviderJobService()
        self.retries = ProviderRetryPolicyService()

    def compile_face_plate_sample_job(self, input_payload: dict, source_refs: list[str], reference_asset_refs: list[str], operator_approved=True):
        profile = self.capabilities.compile_flux_profile(configured=True, tested=True, available=True)
        provider_input = self.jobs.compile_input(ProviderName.FLUX, ProviderRole.REFERENCE_BASED_OBJECT_EDITOR, ProviderJobKind.FACE_PLATE_SAMPLE, input_payload, source_refs, reference_asset_refs=reference_asset_refs)
        cost = self.costs.estimate(ProviderName.FLUX, ProviderJobKind.FACE_PLATE_SAMPLE)
        decision = self.decisions.compile_decision(ProviderName.FLUX, ProviderRole.REFERENCE_BASED_OBJECT_EDITOR, ProviderJobKind.FACE_PLATE_SAMPLE, "Generate reference-based face plate sample for approval.", cost, "sample", ["manual_expression_plate"], operator_approved)
        job = self.jobs.compile_job(provider_input, profile.provider_capability_profile_id, decision, self.retries.strict_sample_policy())
        return profile, job
