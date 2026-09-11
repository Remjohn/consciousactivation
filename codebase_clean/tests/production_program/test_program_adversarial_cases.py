"""
test_program_adversarial_cases.py
---------------------------------
Adversarial tests for quote tampering rejection, unapproved asset injections, and story arc mutations.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "production-program" / "src"))

import pytest

from cae_production_program.compiler import ProductionProgramCompiler
from cae_production_program.domain import SceneRole
from cae_production_program.errors import (
    EvidenceQuoteMismatchError,
    StoryArcGeometryMutationError,
    TimingDiscontinuityError,
    UnapprovedAssetInsertionError,
)
from cae_production_program.verifier import ProductionProgramVerifier


def test_quote_checksum_mismatch_during_compilation():
    t_orig = "Authentic quote from interview."
    h_orig = hashlib.sha256(t_orig.encode("utf-8")).hexdigest()

    # Tampered quote text with original hash
    scenes_data = [
        {
            "scene_role": SceneRole.HOOK_INTERRUPT,
            "segment_id": "SEG-01",
            "spoken_text": "Tampered quote text.",  # VIOLATION
            "text_sha256": h_orig,
            "start_time": 0.0,
            "end_time": 4.0,
            "asset_inserts": [],
        }
    ]

    with pytest.raises(EvidenceQuoteMismatchError, match="does not match registered hash"):
        ProductionProgramCompiler.compile_program(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            title="Title",
            semantic_intent="Authentic intent statement",
            story_arc="THE_WITNESS",
            scenes_data=scenes_data,
            approved_asset_ids=[],
        )


def test_unapproved_asset_injection_rejected():
    t = "Authentic quote."
    h = hashlib.sha256(t.encode("utf-8")).hexdigest()

    scenes_data = [
        {
            "scene_role": SceneRole.HOOK_INTERRUPT,
            "segment_id": "SEG-01",
            "spoken_text": t,
            "text_sha256": h,
            "start_time": 0.0,
            "end_time": 4.0,
            "asset_inserts": [{"asset_id": "AST-UNAPPROVED-ROGUE"}],  # VIOLATION
        }
    ]

    with pytest.raises(UnapprovedAssetInsertionError, match="unapproved asset"):
        ProductionProgramCompiler.compile_program(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            title="Title",
            semantic_intent="Authentic intent statement",
            story_arc="THE_WITNESS",
            scenes_data=scenes_data,
            approved_asset_ids=["AST-APPROVED-01"],
        )


def test_story_arc_mutation_caught_by_verifier():
    t = "Authentic quote."
    h = hashlib.sha256(t.encode("utf-8")).hexdigest()

    scenes_data = [
        {
            "scene_role": SceneRole.HOOK_INTERRUPT,
            "segment_id": "SEG-01",
            "spoken_text": t,
            "text_sha256": h,
            "start_time": 0.0,
            "end_time": 4.0,
            "asset_inserts": [],
        }
    ]

    program, _ = ProductionProgramCompiler.compile_program(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        title="Title",
        semantic_intent="Authentic intent statement",
        story_arc="THE_WITNESS",
        scenes_data=scenes_data,
        approved_asset_ids=[],
    )

    # Downstream render spec attempts to switch arc to THE_PARADOX_EXPOSURE
    tampered_render = {
        "story_arc": "THE_PARADOX_EXPOSURE",  # VIOLATION
        "scenes": [
            {
                "scene_role": SceneRole.HOOK_INTERRUPT,
                "spoken_text": t,
                "asset_inserts": [],
            }
        ],
    }

    with pytest.raises(StoryArcGeometryMutationError, match="mutated story arc geometry"):
        ProductionProgramVerifier.verify_render_conformance(program, tampered_render)
