"""
test_program_compiler_scene_progression.py
------------------------------------------
Tests multi-scene compilation from candidate evidence with E/D-roll asset synchronization.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "production-program" / "src"))

from cae_production_program.compiler import ProductionProgramCompiler
from cae_production_program.domain import SceneRole


def test_multi_scene_compilation():
    t1 = "Everyone told us microservices were the gold standard."
    t2 = "Six months later, a single user checkout touched 42 separate network calls."
    t3 = "The lesson: network boundaries are not domain boundaries."

    h1 = hashlib.sha256(t1.encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(t2.encode("utf-8")).hexdigest()
    h3 = hashlib.sha256(t3.encode("utf-8")).hexdigest()

    scenes_data = [
        {
            "scene_role": SceneRole.HOOK_INTERRUPT,
            "segment_id": "SEG-01",
            "spoken_text": t1,
            "text_sha256": h1,
            "start_time": 0.0,
            "end_time": 4.0,
            "asset_inserts": [{"asset_id": "AST-01"}],
        },
        {
            "scene_role": SceneRole.EVIDENCE_CLIMAX,
            "segment_id": "SEG-02",
            "spoken_text": t2,
            "text_sha256": h2,
            "start_time": 4.0,
            "end_time": 10.5,
            "asset_inserts": [{"asset_id": "AST-02"}],
        },
        {
            "scene_role": SceneRole.INSIGHT_RESOLUTION,
            "segment_id": "SEG-03",
            "spoken_text": t3,
            "text_sha256": h3,
            "start_time": 10.5,
            "end_time": 15.0,
            "asset_inserts": [],
        },
    ]

    program, receipt = ProductionProgramCompiler.compile_program(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        title="Microservices Failure",
        semantic_intent="Deconstruct architectural overengineering.",
        story_arc="THE_INVERSION",
        scenes_data=scenes_data,
        approved_asset_ids=["AST-01", "AST-02"],
    )

    assert len(program.scenes) == 3
    assert program.total_duration == 15.0
    assert len(receipt.evidence_sha256_list) == 3
    assert len(receipt.asset_id_list) == 2
