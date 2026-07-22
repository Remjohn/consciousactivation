"""Consent compatibility policy for TS-CMF-008."""

from __future__ import annotations

from ccp_studio.contracts.consent import ConsentCompatibilityResult, ConsentRecordVersion, ConsentVersionStatus


COMMAND_REQUIRED_SCOPES = {
    "StartCompleteExpressionSessionCommand": ["recording_allowed", "source_storage_allowed"],
    "QueueRenderCommand": ["likeness_use_allowed", "derivative_generation_allowed"],
    "SubmitProviderJobCommand": ["provider_processing_allowed"],
    "MemoryAdmissionCommand": ["reuse_allowed", "retention_allowed"],
    "PublishIntentCommand": ["publication_allowed"],
    "GenerateAssetPackageSpecCommand": ["derivative_generation_allowed", "reuse_allowed"],
    "StartBrandGenesisWorkflowCommand": [
        "source_storage_allowed",
        "likeness_use_allowed",
        "derivative_generation_allowed",
        "provider_processing_allowed",
        "reuse_allowed",
        "retention_allowed",
    ],
    "GenerateActingReferenceGridCommand": [
        "source_storage_allowed",
        "likeness_use_allowed",
        "derivative_generation_allowed",
        "provider_processing_allowed",
        "reuse_allowed",
        "retention_allowed",
    ],
}


class ConsentPolicy:
    def evaluate(self, *, command_type: str, version: ConsentRecordVersion | None) -> ConsentCompatibilityResult:
        if version is None:
            return ConsentCompatibilityResult(
                schema_version="cmf.consent_compatibility_result.v1",
                command_type=command_type,
                allowed=False,
                decision_code="CONSENT_RECORD_REQUIRED",
            )
        if version.status == ConsentVersionStatus.expired:
            return ConsentCompatibilityResult(
                schema_version="cmf.consent_compatibility_result.v1",
                consent_record_version_id=version.consent_record_version_id,
                command_type=command_type,
                allowed=False,
                blocked_scope="active_consent",
                decision_code="CONSENT_EXPIRED",
                evidence_refs=version.evidence_refs,
            )
        if version.status == ConsentVersionStatus.revoked:
            return ConsentCompatibilityResult(
                schema_version="cmf.consent_compatibility_result.v1",
                consent_record_version_id=version.consent_record_version_id,
                command_type=command_type,
                allowed=False,
                blocked_scope="active_consent",
                decision_code="CONSENT_REVOKED",
                evidence_refs=version.evidence_refs,
            )
        for scope_name in COMMAND_REQUIRED_SCOPES.get(command_type, []):
            if not getattr(version.scope, scope_name):
                return ConsentCompatibilityResult(
                    schema_version="cmf.consent_compatibility_result.v1",
                    consent_record_version_id=version.consent_record_version_id,
                    command_type=command_type,
                    allowed=False,
                    blocked_scope=scope_name,
                    decision_code="CONSENT_SCOPE_BLOCKED",
                    evidence_refs=version.evidence_refs,
                )
        return ConsentCompatibilityResult(
            schema_version="cmf.consent_compatibility_result.v1",
            consent_record_version_id=version.consent_record_version_id,
            command_type=command_type,
            allowed=True,
            decision_code="CONSENT_ALLOWED",
            evidence_refs=version.evidence_refs,
        )
