from __future__ import annotations
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[1]
class SchemaTests(unittest.TestCase):
    def test_all_schemas_are_valid(self) -> None:
        schemas = list((ROOT / "contracts" / "schemas").glob("*.schema.json"))
        self.assertGreaterEqual(len(schemas), 40)
        for path in schemas:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
if __name__ == "__main__":
    unittest.main()
