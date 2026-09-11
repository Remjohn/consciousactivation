"""
test_composition_handoff_receipt.py
-----------------------------------
Tests cryptographic composition handoff receipt generation.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "production-program" / "src"))

from cae_production_program.compiler import ProductionProgramCompiler
from cae_production_program.domain import SceneRole


def test_handoff_receipt_generation():
    t = "Clear architectural thesis."
    h = hashlib.sha256(t.encode("utf-8")).hexdigest()

    scenes_data = [
        {
            "scene_role": SceneRole.HOOK_INTERRUPT,
            "segment_id": "SEG-01",
            "spoken_text": t,
            "text_sha256": h,
            "start_time": 0.0,
            "end_time": 5.0,
            "asset_inserts": [],
        }
    ]

    program, receipt = ProductionProgramCompiler.compile_program(
        candidate_id="CND-100",
        workspace_id="ws-client-99",
        title="Title",
        semantic_intent="Intent thesis",
        story_arc="THE_WITNESS",
        scenes_data=scenes_data,
        approved_asset_ids=[],
    )

    assert receipt.receipt_id.startswith("PRG-RCP-")
    assert receipt.candidate_id == "CND-100"
    assert receipt.compiler_version == "1.0.0"
    assert h in receipt.evidence_sha256_list
