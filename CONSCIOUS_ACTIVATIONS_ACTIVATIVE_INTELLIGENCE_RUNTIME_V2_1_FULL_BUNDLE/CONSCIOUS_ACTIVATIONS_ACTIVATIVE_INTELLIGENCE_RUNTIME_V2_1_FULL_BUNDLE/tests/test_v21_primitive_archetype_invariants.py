from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import unittest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_implementation"))
from activative_intelligence_v2.models import *
from activative_intelligence_v2.primitive_archetype_models import *


def ref(name: str) -> ImmutableRef:
    return ImmutableRef(object_id=name, version="1.0.0", sha256=hashlib.sha256(name.encode()).hexdigest())


class V21InvariantTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_primitive_coalition_example(self):
        PrimitiveCoalitionContract.model_validate(self.load("24_primitive_coalition_contract.json"))

    def test_archetype_requires_role_tension_and_primitive_coalition(self):
        ArchetypeCoalitionProgram.model_validate(self.load("26_archetype_coalition_program.json"))

    def test_final_script_requires_five_distillation_receipts(self):
        data = self.load("30_final_script_package.json")
        data["rscs_receipt_refs"] = data["rscs_receipt_refs"][:4]
        with self.assertRaises(ValidationError):
            FinalScriptPackage.model_validate(data)

    def test_animation_package_cannot_activate_format02(self):
        data = self.load("31_animation_scene_package.json")
        data["format02_activated"] = True
        with self.assertRaises(ValidationError):
            AnimationScenePackage.model_validate(data)

    def test_failed_primitive_gate_cannot_pass(self):
        with self.assertRaises(ValidationError):
            PrimitiveEvaluationReceipt(
                receipt_id="r", coalition_ref=ref("c"), binding_results={"b1": "fail"},
                conflict_gate_passed=True, misuse_gate_passed=True,
                coalition_signature_preserved=True, edge_product_preserved=True,
                evidence_refs=(ref("e"),), verdict="pass"
            )

    def test_product_handoff_example(self):
        ProductHandoffReceipt.model_validate(self.load("33_product_handoff_receipt.json"))


if __name__ == "__main__":
    unittest.main()
