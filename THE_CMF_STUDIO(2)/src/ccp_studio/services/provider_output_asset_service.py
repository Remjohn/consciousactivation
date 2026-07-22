from ccp_studio.contracts.provider_runtime import ProviderJobOutput, ProviderJobReceipt, ProviderOutputAssetRef, ProviderOutputAssetRole

class ProviderOutputAssetService:
    def compile_asset_ref(self, output: ProviderJobOutput, receipt: ProviderJobReceipt, asset_role: ProviderOutputAssetRole, source_refs: list[str], workspace_artifact_ref_id=None):
        if receipt.provider_job_id != output.provider_job_id:
            raise ValueError("Provider receipt/job output mismatch")
        if receipt.provider_job_output_id != output.provider_job_output_id:
            raise ValueError("Provider receipt output id mismatch")
        return ProviderOutputAssetRef(provider_job_id=output.provider_job_id, provider_job_receipt_id=receipt.provider_job_receipt_id, provider_job_output_id=output.provider_job_output_id, provider_name=output.provider_name, asset_role=asset_role, asset_uri=output.output_uri, sha256=output.output_sha256, source_refs=source_refs, workspace_artifact_ref_id=workspace_artifact_ref_id)
