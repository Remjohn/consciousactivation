"""Source artifact repositories for TS-CMF-009."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.source import (
    RecordingConfiguration,
    SourceArtifact,
    SourceArtifactManifest,
    SourceIntakeReceipt,
    SourceQualityReport,
)


@dataclass
class InMemorySourceArtifactRepository:
    configurations: dict[UUID, RecordingConfiguration] = field(default_factory=dict)
    artifacts: dict[UUID, SourceArtifact] = field(default_factory=dict)
    reports: dict[UUID, SourceQualityReport] = field(default_factory=dict)
    manifests: dict[UUID, SourceArtifactManifest] = field(default_factory=dict)
    receipts: dict[UUID, SourceIntakeReceipt] = field(default_factory=dict)
    approved_exceptions: set[UUID] = field(default_factory=set)

    def put_configuration(self, configuration: RecordingConfiguration) -> RecordingConfiguration:
        self.configurations[configuration.session_id] = configuration
        return configuration

    def get_configuration(self, session_id: UUID) -> RecordingConfiguration | None:
        return self.configurations.get(session_id)

    def put_artifact(self, artifact: SourceArtifact) -> SourceArtifact:
        existing = self.artifacts.get(artifact.source_artifact_id)
        if existing and existing.accepted_at is not None and existing != artifact:
            raise ValueError("accepted source artifact is immutable")
        self.artifacts[artifact.source_artifact_id] = artifact
        return artifact

    def accepted_for_session(self, session_id: UUID) -> list[SourceArtifact]:
        return [
            artifact
            for artifact in self.artifacts.values()
            if artifact.session_id == session_id and artifact.accepted_at is not None
        ]

    def artifacts_for_session(self, session_id: UUID) -> list[SourceArtifact]:
        return [artifact for artifact in self.artifacts.values() if artifact.session_id == session_id]

    def put_report(self, report: SourceQualityReport) -> SourceQualityReport:
        self.reports[report.source_quality_report_id] = report
        return report

    def put_manifest(self, manifest: SourceArtifactManifest) -> SourceArtifactManifest:
        self.manifests[manifest.source_artifact_manifest_id] = manifest
        return manifest

    def put_receipt(self, receipt: SourceIntakeReceipt) -> SourceIntakeReceipt:
        self.receipts[receipt.source_intake_receipt_id] = receipt
        return receipt
