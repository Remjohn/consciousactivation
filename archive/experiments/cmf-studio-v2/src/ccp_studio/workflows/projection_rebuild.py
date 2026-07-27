"""Projection rebuild workflow for TS-CMF-058."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ccp_studio.contracts.projection import ProjectionReceipt
from ccp_studio.services.projection_service import ProjectionService


@dataclass
class ProjectionRebuildWorkflow:
    projection_service: ProjectionService

    def stage14_rebuild_graph_projection(self, **kwargs: Any) -> ProjectionReceipt:
        return self.projection_service.stage14_rebuild_graph_projection(**kwargs)
