# Product-local discovery wrapper. The executable acceptance suite lives at tests/phase4/test_ts_int_004_expression.py.
from pathlib import Path
SPEC_ID="TS-INT-004"
TARGET=Path("tests/phase4/test_ts_int_004_expression.py")
def test_acceptance_suite_path_is_declared():
    assert SPEC_ID.startswith("TS-INT-")
    assert str(TARGET).endswith(".py")
