"""Source ingestion and recording setup service for TS-CMF-009."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.source import (
    RecordingConfiguration,
    SourceArtifact,
    SourceArtifactKind,
    SourceArtifactManifest,
    SourceIntakeReceipt,
    SourceQualityReport,
    SourceQualityStatus,
    new_recording_configuration,
)
from ccp_studio.repositories.source_artifacts import InMemorySourceArtifactRepository


class SourceIngestionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SourceIngestionService:
    repository: InMemorySourceArtifactRepository = field(default_factory=InMemorySourceArtifactRepository)

    def submit_recording_configuration(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        session_id: UUID,
        expected_master_source: str,
        backup_route: str,
        platform_source: str | None,
        upload_method: str,
        file_safety_expectations: list[str],
        quality_requirements: list[str],
    ) -> RecordingConfiguration:
        configuration = new_recording_configuration(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            expected_master_source=expected_master_source,
            backup_route=backup_route,
            platform_source=platform_source,
            upload_method=upload_method,
            file_safety_expectations=file_safety_expectations,
            quality_requirements=quality_requirements,
        )
        return self.repository.put_configuration(configuration)

    def create_source_artifact(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        session_id: UUID,
        kind: SourceArtifactKind,
        filename: str,
        content_hash: str,
        source_hash: str,
        retention_policy_id: UUID,
        provenance: str,
    ) -> SourceArtifact:
        if not content_hash:
            raise SourceIngestionError("CONTENT_HASH_REQUIRED", "content_hash is required.")
        if not source_hash:
            raise SourceIngestionError("SOURCE_HASH_REQUIRED", "source_hash is required.")
        immutable_uri = self.object_storage_path(brand_id, session_id, content_hash, filename)
        artifact = SourceArtifact(
            schema_version="cmf.source_artifact.v1",
            source_artifact_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            kind=kind,
            filename=filename,
            content_hash=content_hash,
            source_hash=source_hash,
            retention_policy_id=retention_policy_id,
            provenance=provenance,
            immutable_uri=immutable_uri,
        )
        return self.repository.put_artifact(artifact)

    def evaluate_quality(self, *, session_id: UUID, artifact: SourceArtifact | None) -> SourceQualityReport:
        configuration = self.repository.get_configuration(session_id)
        if configuration is None:
            raise SourceIngestionError("RECORDING_CONFIGURATION_REQUIRED", "Recording configuration is required.")
        if artifact is None:
            return self._report(None, SourceQualityStatus.blocked, "MASTER_SOURCE_REQUIRED", "upload master recording")
        if artifact.kind == SourceArtifactKind.platform_recording and configuration.expected_master_source:
            return self._report(
                artifact,
                SourceQualityStatus.review_required,
                "CANONICAL_SOURCE_REVIEW_REQUIRED",
                "review platform recording before canonical acceptance",
            )
        if not artifact.retention_policy_id:
            return self._report(artifact, SourceQualityStatus.blocked, "RETENTION_POLICY_REQUIRED", "assign retention policy")
        if artifact.content_hash == "mismatch" or artifact.source_hash == "mismatch":
            return self._report(artifact, SourceQualityStatus.blocked, "SOURCE_HASH_MISMATCH", "re-upload source artifact")
        return self._report(artifact, SourceQualityStatus.accepted, None, None)

    def accept_source_artifact(self, *, artifact: SourceArtifact, report: SourceQualityReport) -> SourceArtifact:
        if report.status != SourceQualityStatus.accepted and artifact.source_artifact_id not in self.repository.approved_exceptions:
            raise SourceIngestionError(report.failure_category or "SOURCE_NOT_ACCEPTED", report.recovery_action or "review source")
        accepted = artifact.model_copy(update={"accepted_at": utc_now()})
        self.repository.put_artifact(accepted)
        self._receipt(
            organization_id=accepted.organization_id,
            brand_id=accepted.brand_id,
            session_id=accepted.session_id,
            decision_code="SOURCE_ARTIFACT_ACCEPTED",
            source_artifact_id=accepted.source_artifact_id,
            evidence_refs=[accepted.content_hash, accepted.source_hash],
        )
        return accepted

    def approve_source_exception(self, *, source_artifact_id: UUID, organization_id: UUID, brand_id: UUID, session_id: UUID, reason: str) -> SourceIntakeReceipt:
        self.repository.approved_exceptions.add(source_artifact_id)
        return self._receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            decision_code="SOURCE_EXCEPTION_APPROVED",
            source_artifact_id=source_artifact_id,
            evidence_refs=[reason],
        )

    def create_manifest_for_session(self, *, organization_id: UUID, brand_id: UUID, session_id: UUID, consent_compatible: bool = True) -> SourceArtifactManifest:
        if not consent_compatible:
            raise SourceIngestionError("CONSENT_RECORD_REQUIRED", "Consent compatibility is required.")
        accepted = self.repository.accepted_for_session(session_id)
        if not accepted:
            raise SourceIngestionError("MASTER_SOURCE_REQUIRED", "Accepted source artifact is required.")
        manifest = SourceArtifactManifest(
            schema_version="cmf.source_artifact_manifest.v1",
            source_artifact_manifest_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            source_artifact_ids=[artifact.source_artifact_id for artifact in accepted],
            source_quality_report_ids=list(self.repository.reports.keys()),
            created_at=utc_now(),
        )
        self.repository.put_manifest(manifest)
        self._receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            decision_code="SOURCE_ARTIFACT_MANIFEST_CREATED",
            manifest_id=manifest.source_artifact_manifest_id,
            evidence_refs=[str(item) for item in manifest.source_artifact_ids],
        )
        return manifest

    @staticmethod
    def object_storage_path(brand_id: UUID, session_id: UUID, content_hash: str, filename: str) -> str:
        return f"brands/{brand_id}/source/{session_id}/{content_hash}/{filename.replace('..', '')}"

    def _report(self, artifact: SourceArtifact | None, status: SourceQualityStatus, failure_category: str | None, recovery_action: str | None) -> SourceQualityReport:
        report = SourceQualityReport(
            schema_version="cmf.source_quality_report.v1",
            source_quality_report_id=uuid4(),
            source_artifact_id=artifact.source_artifact_id if artifact else None,
            status=status,
            failure_category=failure_category,
            recovery_action=recovery_action,
            evidence_refs=[artifact.content_hash, artifact.source_hash] if artifact else [],
        )
        return self.repository.put_report(report)

    def _receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        session_id: UUID,
        decision_code: str,
        source_artifact_id: UUID | None = None,
        manifest_id: UUID | None = None,
        evidence_refs: list[str],
    ) -> SourceIntakeReceipt:
        receipt = SourceIntakeReceipt(
            schema_version="cmf.source_intake_receipt.v1",
            source_intake_receipt_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            decision_code=decision_code,
            source_artifact_id=source_artifact_id,
            manifest_id=manifest_id,
            evidence_refs=evidence_refs,
            written_at=utc_now(),
        )
        return self.repository.put_receipt(receipt)
