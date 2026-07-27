from __future__ import annotations

import subprocess

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    FFmpegFinishJob,
    FFmpegFinishResult,
    RenderExecutionMode,
    RenderJobStatus,
    stable_hash,
)
from ccp_studio.services.render_command_safety_service import RenderCommandSafetyService


class FFmpegFinishAdapterService:
    def __init__(self, command_safety: RenderCommandSafetyService | None = None):
        self.command_safety = command_safety or RenderCommandSafetyService()

    def compile_command_plan(self, job: FFmpegFinishJob):
        args = ["-y", "-i", job.input_path]
        for filter_expr in job.filters:
            args.extend(["-vf" if filter_expr.startswith("scale") else "-af", filter_expr])
        args.extend(["-c:v", job.codec.value, job.output_path])
        return self.command_safety.compile_command_plan(
            executable="ffmpeg",
            args=args,
            safe_for_execution=(job.execution_mode == RenderExecutionMode.REAL_LOCAL and job.allow_subprocess_execution),
        )

    def execute_dry_run(self, job: FFmpegFinishJob) -> FFmpegFinishResult:
        plan = self.compile_command_plan(job)
        digest = stable_hash(f"ffmpeg:{job.ffmpeg_finish_job_id}:{plan.command_preview}")
        return FFmpegFinishResult(
            ffmpeg_finish_job_id=job.ffmpeg_finish_job_id,
            status=RenderJobStatus.SUCCEEDED,
            output_uri=f"dry-run://ffmpeg/{digest}.mp4",
            output_sha256=digest,
            command_plan=plan,
            dry_run=True,
            external_runtime_calls_executed=False,
            logs=["Dry run only. FFmpeg was not called."],
        )

    def execute_real_local(self, job: FFmpegFinishJob) -> FFmpegFinishResult:
        if job.execution_mode != RenderExecutionMode.REAL_LOCAL or not job.allow_subprocess_execution:
            raise ValueError("Real FFmpeg execution requires execution_mode=real_local and allow_subprocess_execution=True")
        plan = self.compile_command_plan(job)
        if not plan.safe_for_execution:
            raise ValueError("Command plan not marked safe for execution")
        completed = subprocess.run([plan.executable] + plan.args, cwd=plan.cwd, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            return FFmpegFinishResult(
                ffmpeg_finish_job_id=job.ffmpeg_finish_job_id,
                status=RenderJobStatus.FAILED,
                command_plan=plan,
                dry_run=False,
                external_runtime_calls_executed=True,
                error_message=completed.stderr or completed.stdout,
                logs=[completed.stdout, completed.stderr],
            )
        digest = stable_hash(f"ffmpeg-real:{job.ffmpeg_finish_job_id}:{job.output_path}")
        return FFmpegFinishResult(
            ffmpeg_finish_job_id=job.ffmpeg_finish_job_id,
            status=RenderJobStatus.SUCCEEDED,
            output_uri=f"file://{job.output_path}",
            output_sha256=digest,
            command_plan=plan,
            dry_run=False,
            external_runtime_calls_executed=True,
            logs=[completed.stdout],
        )
