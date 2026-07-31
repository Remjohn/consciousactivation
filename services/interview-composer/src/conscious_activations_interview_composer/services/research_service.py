from __future__ import annotations

from typing import Any, Mapping

from ..domain import make_guest_research_package
from ..repository import InterviewComposerRepository


class ResearchService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_package(self, command: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        payload = make_guest_research_package(**command)
        return self.repository.store_object(
            "guest_research_package", payload,
            object_id=payload["research_package_id"], idempotency_key=idempotency_key,
        )
