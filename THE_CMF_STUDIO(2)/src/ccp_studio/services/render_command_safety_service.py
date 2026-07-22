from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import RenderCommandPlan


class RenderCommandSafetyService:
    def compile_command_plan(self, *, executable: str, args: list[str], cwd: str | None = None, safe_for_execution: bool = False) -> RenderCommandPlan:
        forbidden_tokens = {";", "&&", "||", "|", "`"}
        if any(token in executable for token in forbidden_tokens):
            raise ValueError("Executable contains forbidden shell token")
        for arg in args:
            if any(token in arg for token in ["\n", "\r", "\x00"]):
                raise ValueError("Command arg contains forbidden character")
        return RenderCommandPlan(executable=executable, args=args, cwd=cwd, safe_for_execution=safe_for_execution)
