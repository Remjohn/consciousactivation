"""Organization repository for TS-CMF-004."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.workspace_lifecycle import Organization


@dataclass
class InMemoryOrganizationRepository:
    organizations: dict[UUID, Organization] = field(default_factory=dict)

    def put(self, organization: Organization) -> Organization:
        self.organizations[organization.organization_id] = organization
        return organization

    def get(self, organization_id: UUID) -> Organization | None:
        return self.organizations.get(organization_id)
