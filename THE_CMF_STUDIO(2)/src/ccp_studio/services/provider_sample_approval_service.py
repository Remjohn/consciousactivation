from ccp_studio.contracts.provider_runtime import ProviderBatchPolicyReceipt, ProviderSampleApprovalGate

class ProviderSampleApprovalService:
    def compile_gate(self, scene_sample_approved=False, face_plate_sample_approved=False, template_preview_sample_approved=False, approved_by=None, blockers=None):
        return ProviderSampleApprovalGate(scene_sample_approved=scene_sample_approved, face_plate_sample_approved=face_plate_sample_approved, template_preview_sample_approved=template_preview_sample_approved, approved_by=approved_by, blockers=blockers or [])
    def compile_batch_policy_receipt(self, gate: ProviderSampleApprovalGate, batch_requested: bool) -> ProviderBatchPolicyReceipt:
        return ProviderBatchPolicyReceipt(sample_gate=gate, batch_requested=batch_requested)
