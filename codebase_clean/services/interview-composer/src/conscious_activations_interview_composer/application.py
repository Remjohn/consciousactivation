from __future__ import annotations

from pathlib import Path

from .repository import InterviewComposerRepository
from .services.research_service import ResearchService
from .services.brief_service import BriefService
from .services.session_service import SessionService


class InterviewComposerApplication:
    def __init__(self, database_path: str | Path | None = None):
        self.repository = InterviewComposerRepository(database_path)
        self.research = ResearchService(self.repository)
        self.briefs = BriefService(self.repository)
        self.sessions = SessionService(self.repository)

    def initialize(self):
        return self.repository.initialize()
