from pathlib import Path
import json, importlib.util, sys
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sequence_engine_models", ROOT / "models" / "sequence_engine_models.py")
mod = importlib.util.module_from_spec(spec); sys.modules["sequence_engine_models"] = mod; spec.loader.exec_module(mod)
CASES = {
 "example_interview_brief_v2.json": mod.InterviewBriefV2,
 "example_live_coverage_state.json": mod.LiveIngredientCoverageState,
 "example_expression_ingredient_inventory.json": mod.ExpressionIngredientInventory,
 "example_content_sequence_program.json": mod.ContentSequenceProgram,
 "example_package_sequence_program.json": mod.PackageSequenceProgram,
 "example_sequence_evaluation_receipt.json": mod.SequenceEvaluationReceipt,
}
def test_examples_validate():
    for filename, cls in CASES.items():
        data = json.loads((ROOT / "examples" / filename).read_text())
        cls.model_validate(data)
