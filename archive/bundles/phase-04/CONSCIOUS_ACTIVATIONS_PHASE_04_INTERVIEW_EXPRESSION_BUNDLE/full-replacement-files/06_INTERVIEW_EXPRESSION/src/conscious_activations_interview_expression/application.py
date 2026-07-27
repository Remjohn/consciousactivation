from __future__ import annotations
from pathlib import Path
from .repository import InterviewRepository
from .source_package import SourcePackageService
from .transcript import TranscriptService
from .visual import VisualIndexService
from .reaction import ReactionEvidenceService
from .expression import ExpressionGovernanceService
from .inventory import AssetInventoryService
from .live_state import LiveSessionService
from .media import MediaInspector

class InterviewExpressionApplication:
    def __init__(self, database_path: str|Path|None=None):
        self.repository=InterviewRepository(database_path)
        self.source_packages=SourcePackageService(self.repository)
        self.transcripts=TranscriptService(self.repository)
        self.visual=VisualIndexService(self.repository)
        self.reactions=ReactionEvidenceService(self.repository)
        self.expression=ExpressionGovernanceService(self.repository)
        self.inventory=AssetInventoryService(self.repository)
        self.live=LiveSessionService(self.repository)
        self.media=MediaInspector()
    def initialize(self): return self.repository.initialize()
