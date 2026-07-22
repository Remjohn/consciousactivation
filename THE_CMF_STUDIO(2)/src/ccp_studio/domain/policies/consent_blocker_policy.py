"""Registry-backed cross-workflow consent blocker policy for TS-CMF-010."""

from __future__ import annotations

from dataclasses import dataclass, field

from ccp_studio.contracts.consent import ConsentRecordVersion, ConsentVersionStatus
from ccp_studio.contracts.consent_blockers import (
    ConsentGuardDecision,
    ConsentRepairAction,
    ConsentSensitiveCommand,
    new_consent_sensitive_command,
)


def default_consent_sensitive_registry() -> dict[str, ConsentSensitiveCommand]:
    commands = [
        new_consent_sensitive_command(
            command_type="SubmitProviderJobCommand",
            required_scopes=["provider_processing_allowed"],
            applies_to_stages=["provider_processing"],
            external_side_effect=True,
        ),
        new_consent_sensitive_command(
            command_type="QueueRenderCommand",
            required_scopes=["likeness_use_allowed", "derivative_generation_allowed"],
            applies_to_stages=["rendering"],
            external_side_effect=True,
        ),
        new_consent_sensitive_command(
            command_type="RerenderSceneCommand",
            required_scopes=["likeness_use_allowed", "derivative_generation_allowed", "reuse_allowed"],
            applies_to_stages=["rendering", "future_reuse"],
            external_side_effect=True,
        ),
        new_consent_sensitive_command(
            command_type="MemoryAdmissionCommand",
            required_scopes=["reuse_allowed", "retention_allowed"],
            applies_to_stages=["memory_admission"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="ApproveMemoryAdmissionCommand",
            required_scopes=["reuse_allowed", "retention_allowed"],
            applies_to_stages=["memory_admission", "review"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="ApproveReviewCommand",
            required_scopes=["reuse_allowed"],
            applies_to_stages=["review"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="PublishIntentCommand",
            required_scopes=["publication_allowed"],
            applies_to_stages=["publishing"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="DraftPublishingIntentCommand",
            required_scopes=["publication_allowed"],
            applies_to_stages=["publishing"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="SchedulePublerPostCommand",
            required_scopes=["publication_allowed"],
            applies_to_stages=["publishing", "publer_scheduling"],
            external_side_effect=True,
        ),
        new_consent_sensitive_command(
            command_type="GenerateAssetPackageSpecCommand",
            required_scopes=["derivative_generation_allowed", "reuse_allowed"],
            applies_to_stages=["asset_package", "future_reuse"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="RequestFutureReuseCommand",
            required_scopes=["reuse_allowed", "likeness_use_allowed"],
            applies_to_stages=["future_reuse"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="RequestVoiceBoostEligibilityCommand",
            required_scopes=["synthetic_voice_eligible", "provider_processing_allowed"],
            applies_to_stages=["voice_repair", "evaluation_review"],
            external_side_effect=False,
        ),
        new_consent_sensitive_command(
            command_type="CreateVoiceBridgeManifestCommand",
            required_scopes=["synthetic_voice_eligible", "provider_processing_allowed"],
            applies_to_stages=["voice_repair", "rendering"],
            external_side_effect=True,
        ),
        new_consent_sensitive_command(
            command_type="RequestVoiceRepairCommand",
            required_scopes=["synthetic_voice_eligible", "provider_processing_allowed"],
            applies_to_stages=["voice_repair"],
            external_side_effect=True,
        ),
    ]
    return {command.command_type: command for command in commands}


@dataclass
class ConsentBlockerPolicy:
    registry: dict[str, ConsentSensitiveCommand] = field(default_factory=default_consent_sensitive_registry)

    def register(self, command: ConsentSensitiveCommand) -> ConsentSensitiveCommand:
        self.registry[command.command_type] = command
        return command

    def get(self, command_type: str) -> ConsentSensitiveCommand | None:
        return self.registry.get(command_type)

    def evaluate(
        self,
        *,
        command_type: str,
        version: ConsentRecordVersion | None,
        require_mapping: bool = False,
    ) -> ConsentGuardDecision:
        command = self.get(command_type)
        if command is None:
            if require_mapping:
                return self._blocked(
                    command_type=command_type,
                    decision_code="CONSENT_SCOPE_MAPPING_REQUIRED",
                    blocked_scope="scope_mapping",
                    repair_actions=[ConsentRepairAction.human_review],
                )
            return ConsentGuardDecision(
                schema_version="cmf.consent_guard_decision.v1",
                command_type=command_type,
                allowed=True,
                decision_code="CONSENT_NOT_APPLICABLE",
            )
        if version is None:
            return self._blocked(
                command_type=command_type,
                decision_code="CONSENT_RECORD_REQUIRED",
                blocked_scope="active_consent",
                repair_actions=[
                    ConsentRepairAction.request_updated_consent,
                    ConsentRepairAction.human_review,
                ],
            )
        if version.status == ConsentVersionStatus.expired:
            return self._blocked(
                command_type=command_type,
                decision_code="CONSENT_EXPIRED",
                blocked_scope="active_consent",
                consent_record_version_id=version.consent_record_version_id,
                repair_actions=[
                    ConsentRepairAction.request_updated_consent,
                    ConsentRepairAction.quarantine,
                ],
                evidence_refs=version.evidence_refs,
            )
        if version.status == ConsentVersionStatus.revoked:
            return self._blocked(
                command_type=command_type,
                decision_code="CONSENT_REVOKED",
                blocked_scope="active_consent",
                consent_record_version_id=version.consent_record_version_id,
                repair_actions=[
                    ConsentRepairAction.request_updated_consent,
                    ConsentRepairAction.quarantine,
                    ConsentRepairAction.human_review,
                ],
                evidence_refs=version.evidence_refs,
            )
        for scope_name in command.required_scopes:
            if not getattr(version.scope, scope_name):
                return self._blocked(
                    command_type=command_type,
                    decision_code=self._decision_code_for_scope(scope_name, command_type),
                    blocked_scope=scope_name,
                    consent_record_version_id=version.consent_record_version_id,
                    repair_actions=self._repair_actions_for_scope(scope_name),
                    evidence_refs=version.evidence_refs,
                )
        return ConsentGuardDecision(
            schema_version="cmf.consent_guard_decision.v1",
            command_type=command_type,
            allowed=True,
            decision_code="CONSENT_ALLOWED",
            consent_record_version_id=version.consent_record_version_id,
            evidence_refs=version.evidence_refs,
        )

    @staticmethod
    def _blocked(
        *,
        command_type: str,
        decision_code: str,
        blocked_scope: str,
        repair_actions: list[ConsentRepairAction],
        consent_record_version_id=None,
        evidence_refs: list[str] | None = None,
    ) -> ConsentGuardDecision:
        return ConsentGuardDecision(
            schema_version="cmf.consent_guard_decision.v1",
            command_type=command_type,
            allowed=False,
            decision_code=decision_code,
            consent_record_version_id=consent_record_version_id,
            blocked_scope=blocked_scope,
            repair_actions=repair_actions,
            evidence_refs=evidence_refs or [],
        )

    @staticmethod
    def _decision_code_for_scope(scope_name: str, command_type: str) -> str:
        if scope_name == "likeness_use_allowed":
            return "LIKENESS_REUSE_BLOCKED"
        if scope_name == "publication_allowed":
            return "PUBLICATION_CONSENT_REQUIRED"
        if scope_name == "synthetic_voice_eligible":
            return "SYNTHETIC_VOICE_CONSENT_REQUIRED"
        if command_type in {"MemoryAdmissionCommand", "ApproveMemoryAdmissionCommand"}:
            return "MEMORY_ADMISSION_CONSENT_BLOCKED"
        return "CONSENT_SCOPE_BLOCKED"

    @staticmethod
    def _repair_actions_for_scope(scope_name: str) -> list[ConsentRepairAction]:
        if scope_name == "likeness_use_allowed":
            return [
                ConsentRepairAction.remove_likeness,
                ConsentRepairAction.request_updated_consent,
                ConsentRepairAction.quarantine,
            ]
        if scope_name == "publication_allowed":
            return [
                ConsentRepairAction.request_updated_consent,
                ConsentRepairAction.human_review,
            ]
        if scope_name in {"reuse_allowed", "retention_allowed"}:
            return [
                ConsentRepairAction.quarantine,
                ConsentRepairAction.remove_claim,
                ConsentRepairAction.human_review,
            ]
        if scope_name == "synthetic_voice_eligible":
            return [
                ConsentRepairAction.human_review,
                ConsentRepairAction.request_updated_consent,
            ]
        return [
            ConsentRepairAction.request_updated_consent,
            ConsentRepairAction.quarantine,
        ]
