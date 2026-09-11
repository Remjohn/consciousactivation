"""
Pytest suite for CA-CAN-02 Constitution Set Completion.
Executes automated reality probes verifying the 30 constitutions and near-miss fixture corpus.
"""

import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.cae.constitutions.verify_ca_can_02 import verify_all


def test_ca_can_02_reality_probes():
    """Verify all 8 CA-CAN-02 reality probes pass."""
    assert verify_all() is True
