from __future__ import annotations

from typing import Any, Mapping

from ..domain import make_activative_interview_brief
from ..errors import NotFoundError
from ..repository import InterviewComposerRepository


class BriefService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_brief(self, command: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        research_ref = command["research_package_ref"]
        try:
            self.repository.get_object(research_ref["object_id"])
        except NotFoundError:
            raise NotFoundError(f"no guest_research_package with id '{research_ref['object_id']}'") from None
        payload = make_activative_interview_brief(**command)
        result = self.repository.store_object(
            "activative_interview_brief", payload,
            object_id=payload["brief_id"], idempotency_key=idempotency_key,
        )
        self.repository.add_edge(payload["brief_id"], research_ref["object_id"], "researched_from")
        return result
