from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import OperatorVideoRevisionCommand, OperatorVideoRevisionReceipt


class VideoRevisionService:
    def compile_revision_command(self, *, command_type: str, target_ref: str, reason: str, payload: dict | None = None) -> OperatorVideoRevisionCommand:
        return OperatorVideoRevisionCommand(command_type=command_type, target_ref=target_ref, reason=reason, payload=payload or {})

    def apply_revision_fake(self, command: OperatorVideoRevisionCommand) -> OperatorVideoRevisionReceipt:
        return OperatorVideoRevisionReceipt(command_id=command.operator_video_revision_command_id, applied=True, notes="fake deterministic revision applied")
