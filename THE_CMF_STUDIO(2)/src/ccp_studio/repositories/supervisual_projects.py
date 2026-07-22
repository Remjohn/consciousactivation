"""In-memory repository for SuperVisual projects and variants."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.supervisual_projects import (
    SuperVisualApprovalReceipt,
    SuperVisualExportArtifact,
    SuperVisualProject,
    SuperVisualTimelineEvent,
    SuperVisualVariant,
)


@dataclass
class InMemorySuperVisualProjectRepository:
    projects: dict[UUID, SuperVisualProject] = field(default_factory=dict)
    variants: dict[UUID, SuperVisualVariant] = field(default_factory=dict)
    approval_receipts: dict[UUID, SuperVisualApprovalReceipt] = field(default_factory=dict)
    export_artifacts: dict[UUID, SuperVisualExportArtifact] = field(default_factory=dict)
    timeline_events: dict[UUID, list[SuperVisualTimelineEvent]] = field(default_factory=dict)

    def put_project(self, item: SuperVisualProject) -> SuperVisualProject:
        self.projects[item.supervisual_project_id] = item
        return item

    def put_variant(self, item: SuperVisualVariant) -> SuperVisualVariant:
        self.variants[item.supervisual_variant_id] = item
        return item

    def put_approval_receipt(self, item: SuperVisualApprovalReceipt) -> SuperVisualApprovalReceipt:
        self.approval_receipts[item.supervisual_approval_receipt_id] = item
        return item

    def put_export_artifact(self, item: SuperVisualExportArtifact) -> SuperVisualExportArtifact:
        self.export_artifacts[item.supervisual_export_artifact_id] = item
        return item

    def append_timeline_event(self, item: SuperVisualTimelineEvent) -> SuperVisualTimelineEvent:
        self.timeline_events.setdefault(item.project_id, []).append(item)
        return item
