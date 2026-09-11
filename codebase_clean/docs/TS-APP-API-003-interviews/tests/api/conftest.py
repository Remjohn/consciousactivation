from __future__ import annotations
import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def api_app(tmp_path, monkeypatch):
    """Point the gateway at an isolated CA_DATA_ROOT for this test only.

    Mirrors tests/api/test_startup.py's own local api_app fixture: env vars
    must be set before api.config.load_config() runs at lifespan startup, so
    api.main is imported lazily, inside the fixture, not at module top.
    Centralized here so test_interviews_import.py, test_interviews_brief_led.py,
    and test_interviews_status.py all share one definition.
    """
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app

    return app
