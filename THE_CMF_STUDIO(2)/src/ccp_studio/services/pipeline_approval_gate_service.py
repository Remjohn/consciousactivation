from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineApprovalGate, PipelineApprovalStatus
class PipelineApprovalGateService:
    def approve(self, gate: PipelineApprovalGate, approved_by: str, approved_sample_types=None):
        return PipelineApprovalGate(gate_id=gate.gate_id, gate_type=gate.gate_type, required=gate.required, status=PipelineApprovalStatus.APPROVED, approved_by=approved_by, blockers=[], required_sample_types=list(gate.required_sample_types), approved_sample_types=approved_sample_types if approved_sample_types is not None else list(gate.required_sample_types))
    def reject(self, gate: PipelineApprovalGate, blocker):
        return PipelineApprovalGate(gate_id=gate.gate_id, gate_type=gate.gate_type, required=gate.required, status=PipelineApprovalStatus.REJECTED, blockers=[blocker], required_sample_types=list(gate.required_sample_types), approved_sample_types=list(gate.approved_sample_types))
