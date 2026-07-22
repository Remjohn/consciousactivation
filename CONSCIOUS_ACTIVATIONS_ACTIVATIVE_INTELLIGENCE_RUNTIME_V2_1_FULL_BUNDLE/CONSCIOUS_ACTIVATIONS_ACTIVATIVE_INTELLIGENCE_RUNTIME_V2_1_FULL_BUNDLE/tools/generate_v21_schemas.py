from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference_implementation"))
from activative_intelligence_v2.primitive_archetype_models import *
MODELS = [
    PrimitiveBinding, PrimitiveMisuseRisk, CoalitionSignature, EdgeProduct,
    PrimitiveCoalitionContract, PrimitiveEvaluationReceipt,
    PsychologicalRoleTensionContract, ArchetypeBinding, ArchetypeCoalitionProgram,
    BrandContextVersion, VoiceDNA, VisualDNA, DistillationLayerReceipt,
    FinalScriptSegment, FinalScriptPackage, AnimationSceneSpec, AnimationScenePackage,
    ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, ProductHandoffReceipt,
]
out = ROOT / "contracts" / "schemas"
out.mkdir(parents=True, exist_ok=True)
for model in MODELS:
    name = ''.join(['_' + c.lower() if c.isupper() else c for c in model.__name__]).lstrip('_')
    (out / f"{name}.schema.json").write_text(json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
