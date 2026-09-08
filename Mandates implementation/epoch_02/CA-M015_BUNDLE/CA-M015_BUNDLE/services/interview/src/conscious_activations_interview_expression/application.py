from __future__ import annotations

from pathlib import Path

from .inventory import AssetInventoryService
from .media import MediaInspector
from .live_state import LiveSessionService
from .reaction import ReactionEvidenceService
from .repository import InterviewRepository
from .expression import ExpressionGovernanceService
from .source_package import SourcePackageService
from .transcript import TranscriptService
from .verbatim import VerbatimEvidenceService
from .visual import VisualIndexService


class InterviewExpressionApplication:
    def __init__(self, database_path: str | Path | None = None):
        self.repository = InterviewRepository(database_path)
        self.source_packages = SourcePackageService(self.repository)
        self.transcripts = TranscriptService(self.repository)
        self.verbatim = VerbatimEvidenceService(self.repository)
        self.visual = VisualIndexService(self.repository)
        self.reactions = ReactionEvidenceService(self.repository)
        self.expression = ExpressionGovernanceService(self.repository)
        self.inventory = AssetInventoryService(self.repository)
        self.live = LiveSessionService(self.repository)
        self.media = MediaInspector()

    def initialize(self):
        return self.repository.initialize()
