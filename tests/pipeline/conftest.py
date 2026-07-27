"""Shared sys.path setup for tests/pipeline/*.

Mirrors the per-phase conftest pattern so that imports of
``cmf_builder`` and ``cmf_pipeline`` resolve against the in-tree ``src/``
packages rather than any stale editable-install site-packages paths.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Repo root = tests/pipeline/../../ (= repository root after TS-APP-SETUP-001)
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
