from ccp_studio.contracts.provider_runtime import (
    PassStatus, ProviderExecutionMode, ProviderJob, ProviderJobInput, ProviderJobOutput, ProviderJobReceipt,
    ProviderJobStatus, ProviderName, ProviderRole, ProviderJobKind, stable_hash
)
from ccp_studio.repositories.provider_runtime import InMemoryProviderRuntimeRepository

class ProviderJobService:
    def __init__(self, repository=None):
        self.repository = repository or InMemoryProviderRuntimeRepository()

    def compile_input(self, provider_name, provider_role, job_kind, input_payload, source_refs, reference_asset_refs=None, template_preview_refs=None, composition_scene_refs=None, avatar_asset_refs=None):
        obj = ProviderJobInput(provider_name=provider_name, provider_role=provider_role, job_kind=job_kind, input_payload=input_payload, source_refs=source_refs, reference_asset_refs=reference_asset_refs or [], template_preview_refs=template_preview_refs or [], composition_scene_refs=composition_scene_refs or [], avatar_asset_refs=avatar_asset_refs or [])
        self.repository.upsert("inputs", obj.provider_job_input_id, obj)
        return obj

    def compile_job(self, provider_input, capability_profile_id, decision_log, retry_policy, sample_approval_gate=None, batch_requested=False):
        job = ProviderJob(provider_name=provider_input.provider_name, provider_role=provider_input.provider_role, job_kind=provider_input.job_kind, job_input=provider_input, capability_profile_id=capability_profile_id, decision_log=decision_log, retry_policy=retry_policy, sample_approval_gate=sample_approval_gate, batch_requested=batch_requested, execution_mode=ProviderExecutionMode.FAKE, provider_calls_allowed=False)
        self.repository.upsert("jobs", job.provider_job_id, job)
        return job

    def fake_execute(self, job: ProviderJob):
        digest = stable_hash(f"{job.provider_job_id}:{job.provider_name.value}:{job.job_kind.value}")
        output = ProviderJobOutput(provider_job_id=job.provider_job_id, provider_name=job.provider_name, job_kind=job.job_kind, output_uri=f"fake://provider-runtime/{job.provider_name.value}/{job.job_kind.value}/{digest}.json", output_sha256=digest, output_payload={"fake": True}, fake_output=True, provider_calls_executed=False)
        job.status = ProviderJobStatus.SUCCEEDED
        receipt = ProviderJobReceipt(provider_job_id=job.provider_job_id, provider_job_output_id=output.provider_job_output_id, provider_name=job.provider_name, job_kind=job.job_kind, status=ProviderJobStatus.SUCCEEDED, pass_status=PassStatus.PASS, cost_estimate=job.decision_log.cost_estimate, decision_log_id=job.decision_log.provider_decision_log_id, fake_execution=True, provider_calls_executed=False)
        self.repository.upsert("outputs", output.provider_job_output_id, output)
        self.repository.upsert("receipts", receipt.provider_job_receipt_id, receipt)
        return output, receipt
