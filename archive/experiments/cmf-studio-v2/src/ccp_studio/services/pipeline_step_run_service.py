from datetime import datetime, timezone
from ccp_studio.contracts.studio_pipeline_recipe_harness import PassStatus, PipelineApprovalStatus, PipelineRunBlocker, PipelineStepReceipt, PipelineStepStatus
class PipelineStepRunService:
    def complete_step(self, run, step_id: str, output_artifact_ids=None, message=None):
        step=next((s for s in run.step_runs if s.step_id==step_id), None)
        if not step: raise KeyError(step_id)
        succeeded={s.step_id for s in run.step_runs if s.status==PipelineStepStatus.SUCCEEDED}
        blockers=[]; missing=sorted(set(step.depends_on_step_ids)-succeeded)
        if missing: blockers.append(PipelineRunBlocker(code='dependencies_not_satisfied', message=f'Missing dependencies: {missing}', step_id=step_id))
        if step.approval_gate_id:
            gate=next((g for g in run.approval_gates if g.gate_id==step.approval_gate_id), None)
            if gate and gate.required and gate.status != PipelineApprovalStatus.APPROVED: blockers.append(PipelineRunBlocker(code='approval_gate_not_approved', message=f'Gate {step.approval_gate_id} is not approved', step_id=step_id))
        if blockers:
            step.status=PipelineStepStatus.BLOCKED
            return PipelineStepReceipt(pipeline_step_run_id=step.pipeline_step_run_id, step_id=step.step_id, status=PipelineStepStatus.BLOCKED, pass_status=PassStatus.FAIL, blockers=blockers, message=message)
        step.status=PipelineStepStatus.SUCCEEDED; step.output_artifact_ids=output_artifact_ids or []; step.completed_at=datetime.now(timezone.utc).isoformat()
        return PipelineStepReceipt(pipeline_step_run_id=step.pipeline_step_run_id, step_id=step.step_id, status=PipelineStepStatus.SUCCEEDED, pass_status=PassStatus.PASS, output_artifact_ids=step.output_artifact_ids, message=message)
