"""Organization and brand scope contracts."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class BrandScope(BaseModel):
    organization_id: UUID
    brand_id: UUID

