from __future__ import annotations
import importlib
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_implementation"))
base = importlib.import_module("activative_intelligence_v2.models")
v21 = importlib.import_module("activative_intelligence_v2.primitive_archetype_models")
class AllExampleTests(unittest.TestCase):
    def test_examples_validate_against_declared_models(self) -> None:
        mapping = json.loads((ROOT / "examples" / "EXAMPLE_MODEL_MAP.json").read_text(encoding="utf-8"))
        for filename, model_name in mapping.items():
            model = getattr(base, model_name, None) or getattr(v21, model_name)
            payload = json.loads((ROOT / "examples" / filename).read_text(encoding="utf-8"))
            model.model_validate(payload)
if __name__ == "__main__":
    unittest.main()
