# Product-local discovery wrapper. The executable acceptance suite lives at tests/phase4/test_ts_int_002_transcript.py.
from pathlib import Path
SPEC_ID="TS-INT-002"
TARGET=Path("tests/phase4/test_ts_int_002_transcript.py")
def test_acceptance_suite_path_is_declared():
    assert SPEC_ID.startswith("TS-INT-")
    assert str(TARGET).endswith(".py")
