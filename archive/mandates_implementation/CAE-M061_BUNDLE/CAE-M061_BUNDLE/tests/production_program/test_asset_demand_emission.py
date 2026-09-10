
"""
CAE-M061 production-program emission tests.
"""

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "production-program" / "src"))

from cae_production_program.compiler import ProductionProgramCompiler  # noqa: E402
from cae_production_program.domain import AssetDemandSpec, SceneRole  # noqa: E402
from cae_production_program.errors import EvidenceQuoteMismatchError, TimingDiscontinuityError  # noqa: E402


TEXT = "The production needs the exact archival moment described by the approved scene."
SHA = hashlib.sha256(TEXT.encode("utf-8")).hexdigest()


def test_asset_demand_spec_is_typed_and_attached_to_the_scene():
    demand = AssetDemandSpec(
        demand_key="archive-moment",
        media_type="VIDEO_CLIP",
        source_type="ARCHIVAL",
        insert_role="SEMANTIC_SIMILE",
        semantic_role="HISTORICAL_TRIUMPH_METAPHOR",
        semantic_obligation="Provide archival footage preserving the approved historical metaphor.",
        min_duration_seconds=3.0,
        max_duration_seconds=6.0,
        preferred_duration_seconds=4.0,
        rights_statuses=["CLEARED"],
        allowed_territories=["GLOBAL"],
        license_required=True,
        evidence_ref="SEG-M061",
        evidence_sha256=SHA,
    )
    assert demand.duration_is_valid is True


def test_compiler_rejects_demand_when_it_detaches_from_evidence():
    with pytest.raises(EvidenceQuoteMismatchError, match="evidence ref"):
        ProductionProgramCompiler.compile_program(
            candidate_id="CND",
            workspace_id="WS",
            title="Demand proof",
            semantic_intent="Preserve evidence.",
            story_arc="ARC",
            scenes_data=[
                {
                    "scene_role": SceneRole.EVIDENCE_CLIMAX,
                    "segment_id": "SEG-M061",
                    "spoken_text": TEXT,
                    "text_sha256": SHA,
                    "end_time": 4.0,
                    "asset_demands": [
                        {
                            "demand_key": "bad-ref",
                            "media_type": "VIDEO_CLIP",
                            "source_type": "ARCHIVAL",
                            "insert_role": "SEMANTIC_SIMILE",
                            "semantic_role": "HISTORICAL_TRIUMPH_METAPHOR",
                            "semantic_obligation": "Provide archival footage preserving the approved historical metaphor.",
                            "min_duration_seconds": 3.0,
                            "max_duration_seconds": 6.0,
                            "rights_statuses": ["CLEARED"],
                            "evidence_ref": "OTHER-SEGMENT",
                            "evidence_sha256": SHA,
                        }
                    ],
                }
            ],
            approved_asset_ids=[],
        )


def test_compiler_rejects_invalid_duration_constraints():
    with pytest.raises(TimingDiscontinuityError, match="duration constraints"):
        ProductionProgramCompiler.compile_program(
            candidate_id="CND",
            workspace_id="WS",
            title="Demand proof",
            semantic_intent="Preserve evidence.",
            story_arc="ARC",
            scenes_data=[
                {
                    "scene_role": SceneRole.EVIDENCE_CLIMAX,
                    "segment_id": "SEG-M061",
                    "spoken_text": TEXT,
                    "text_sha256": SHA,
                    "end_time": 4.0,
                    "asset_demands": [
                        {
                            "demand_key": "bad-duration",
                            "media_type": "VIDEO_CLIP",
                            "source_type": "ARCHIVAL",
                            "insert_role": "SEMANTIC_SIMILE",
                            "semantic_role": "HISTORICAL_TRIUMPH_METAPHOR",
                            "semantic_obligation": "Provide archival footage preserving the approved historical metaphor.",
                            "min_duration_seconds": 6.0,
                            "max_duration_seconds": 3.0,
                            "rights_statuses": ["CLEARED"],
                            "evidence_ref": "SEG-M061",
                            "evidence_sha256": SHA,
                        }
                    ],
                }
            ],
            approved_asset_ids=[],
        )
