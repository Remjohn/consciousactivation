from __future__ import annotations

from typing import Any, Mapping

from ..domain import make_composer_session
from ..errors import NotFoundError
from ..repository import InterviewComposerRepository


class SessionService:
    def __init__(self, repository: InterviewComposerRepository):
        self.repository = repository

    def create_session(self, *, brief_ref: Mapping[str, str],
                       relationship_state_ref: Mapping[str, str],
                       progression_ref: Mapping[str, str],
                       recording_date: str | None,
                       composer_authority: Mapping[str, str],
                       idempotency_key: str) -> dict[str, Any]:
        try:
            self.repository.get_object(brief_ref["object_id"])
        except NotFoundError:
            raise NotFoundError(f"no activative_interview_brief with id '{brief_ref['object_id']}'") from None
        payload = make_composer_session(
            brief_ref=brief_ref, relationship_state_ref=relationship_state_ref,
            progression_ref=progression_ref, recording_date=recording_date,
            composer_authority=composer_authority,
        )
        result = self.repository.store_object(
            "composer_session", payload,
            object_id=payload["session_id"], idempotency_key=idempotency_key,
        )
        self.repository.add_edge(payload["session_id"], brief_ref["object_id"], "schedules")
        return result
