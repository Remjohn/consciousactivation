from __future__ import annotations
from pathlib import Path
from .application import InterviewExpressionApplication

def status(database_path: str|Path|None=None) -> dict[str,object]:
    return InterviewExpressionApplication(database_path).repository.health()
