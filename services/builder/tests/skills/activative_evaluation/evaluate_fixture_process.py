from __future__ import annotations

from pathlib import Path
import sys


evaluation_root = Path(sys.argv[1])
sys.path.insert(0, str(evaluation_root))

from evaluator import evaluate_case, load_case, read_json  # noqa: E402


case = load_case(
    evaluation_root / "fixtures" / "BASE_CASE.json",
    evaluation_root / "fixtures" / "strong_golden_truth_over_approval.json",
)
rubric = read_json(evaluation_root / "RUBRIC.yaml")
print(evaluate_case(case, rubric).receipt_hash)
