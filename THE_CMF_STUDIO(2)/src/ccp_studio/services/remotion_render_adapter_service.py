from __future__ import annotations

import subprocess

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    RemotionRenderJob,
    RemotionRenderResult,
    RenderExecutionMode,
    RenderJobStatus,
    stable_hash,
)
from ccp_studio.services.render_command_safety_service import RenderCommandSafetyService


class RemotionRenderAdapterService:
    def __init__(self, command_safety: RenderCommandSafetyService | None = None):
        self.command_safety = command_safety or RenderCommandSafetyService()

    def compile_command_plan(self, job: RemotionRenderJob):
        args = [
            "remotion",
            "render",
            job.entry_point,
            job.composition_id,
            job.output_path,
            "--codec",
            job.codec.value,
            "--props",
            job.input_props_ref,
            "--fps",
            str(job.fps),
            "--width",
            str(job.width),
            "--height",
            str(job.height),
        ]
        return self.command_safety.compile_command_plan(
            executable="npx",
            args=args,
            safe_for_execution=(job.execution_mode == RenderExecutionMode.REAL_LOCAL and job.allow_subprocess_execution),
        )

    def execute_dry_run(self, job: RemotionRenderJob) -> RemotionRenderResult:
        plan = self.compile_command_plan(job)
        digest = stable_hash(f"remotion:{job.remotion_render_job_id}:{plan.command_preview}")
        return RemotionRenderResult(
            remotion_render_job_id=job.remotion_render_job_id,
            status=RenderJobStatus.SUCCEEDED,
            output_uri=f"dry-run://remotion/{digest}.mp4",
            output_sha256=digest,
            command_plan=plan,
            dry_run=True,
            external_runtime_calls_executed=False,
            logs=["Dry run only. Remotion was not called."],
        )

    def execute_real_local(self, job: RemotionRenderJob) -> RemotionRenderResult:
        if job.execution_mode != RenderExecutionMode.REAL_LOCAL or not job.allow_subprocess_execution:
            raise ValueError("Real Remotion execution requires execution_mode=real_local and allow_subprocess_execution=True")
        plan = self.compile_command_plan(job)
        if not plan.safe_for_execution:
            raise ValueError("Command plan not marked safe for execution")
        completed = subprocess.run([plan.executable] + plan.args, cwd=plan.cwd, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            return RemotionRenderResult(
                remotion_render_job_id=job.remotion_render_job_id,
                status=RenderJobStatus.FAILED,
                command_plan=plan,
                dry_run=False,
                external_runtime_calls_executed=True,
                error_message=completed.stderr or completed.stdout,
                logs=[completed.stdout, completed.stderr],
            )
        digest = stable_hash(f"remotion-real:{job.remotion_render_job_id}:{job.output_path}")
        return RemotionRenderResult(
            remotion_render_job_id=job.remotion_render_job_id,
            status=RenderJobStatus.SUCCEEDED,
            output_uri=f"file://{job.output_path}",
            output_sha256=digest,
            command_plan=plan,
            dry_run=False,
            external_runtime_calls_executed=True,
            logs=[completed.stdout],
        )
