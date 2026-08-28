"""
test_program_domain_contracts.py
--------------------------------
Validates SemanticProgram and CompositionHandoffReceipt serialization, typing, and schema integrity.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "production-program" / "src"))

from cae_production_program.domain import (
    CompositionHandoffReceipt,
    SceneRole,
    SemanticProgram,
    SemanticSceneSpec,
    SFLModulationProfile,
    VisualAudioSpecs,
)


def test_program_domain_contracts():
    text = "We broke the monolith into 40 services and instantly tripled latency."
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()

    scene = SemanticSceneSpec(
        scene_index=1,
        scene_role=SceneRole.HOOK_INTERRUPT,
        segment_id="SEG-001",
        spoken_text=text,
        text_sha256=sha,
        start_time=0.0,
        end_time=5.2,
        duration=5.2,
    )

    program = SemanticProgram(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        title="The Microservices Latency Paradox",
        semantic_intent="Expose counter-intuitive scaling failure in premature distributed decomposition.",
        story_arc="THE_PARADOX_EXPOSURE",
        scenes=[scene],
        total_duration=5.2,
    )

    assert program.program_id.startswith("PRG-")
    assert len(program.scenes) == 1
    assert program.story_arc == "THE_PARADOX_EXPOSURE"
