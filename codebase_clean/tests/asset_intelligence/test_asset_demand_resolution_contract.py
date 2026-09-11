
"""
CAE-M061 demand/resolution boundary tests.

These tests prove the declared contract carries physical-media constraints and
that catalog resolution validates those constraints without re-selecting meaning.
"""

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "asset-intelligence" / "src"))
sys.path.insert(0, str(ROOT / "services" / "production-program" / "src"))

from cae_asset_intelligence.demand_contract import (  # noqa: E402
    AssetDemandResolver,
    AssetDemandValidationError,
    AssetResolutionState,
    compile_production_asset_demand,
)
from cae_asset_intelligence.domain import (  # noqa: E402
    AssetAnnotation,
    AssetCatalog,
    EditorialInsertRole,
    MediaType,
    RightsMetadata,
    RightsStatus,
    SourceType,
)
from cae_production_program.compiler import ProductionProgramCompiler  # noqa: E402
from cae_production_program.domain import SceneRole  # noqa: E402


TEXT = "The archive clip makes the production claim visible without changing the spoken evidence."
TEXT_SHA = hashlib.sha256(TEXT.encode("utf-8")).hexdigest()


def build_program():
    program, receipt = ProductionProgramCompiler.compile_program(
        candidate_id="CND-M061",
        workspace_id="WS-M061",
        title="Asset demand proof",
        semantic_intent="Demonstrate an explicit physical-media requirement without semantic re-selection.",
        story_arc="THE_EVIDENCE",
        scenes_data=[
            {
                "scene_role": SceneRole.EVIDENCE_CLIMAX,
                "segment_id": "SEG-M061-01",
                "spoken_text": TEXT,
                "text_sha256": TEXT_SHA,
                "start_time": 0.0,
                "end_time": 5.0,
                "asset_demands": [
                    {
                        "demand_key": "archive-proof",
                        "media_type": "VIDEO_CLIP",
                        "source_type": "ARCHIVAL",
                        "insert_role": "SEMANTIC_SIMILE",
                        "semantic_role": "HISTORICAL_TRIUMPH_METAPHOR",
                        "semantic_obligation": "Provide archival footage that preserves the declared historical-triumph metaphor.",
                        "min_duration_seconds": 3.0,
                        "max_duration_seconds": 6.0,
                        "preferred_duration_seconds": 4.0,
                        "rights_statuses": ["CLEARED"],
                        "allowed_territories": ["GLOBAL"],
                        "license_required": True,
                        "evidence_ref": "SEG-M061-01",
                        "evidence_sha256": TEXT_SHA,
                    }
                ],
            }
        ],
        approved_asset_ids=[],
        wrong_reading_locks=["Do not replace the historical evidence with generic stock."],
    )
    return program, receipt


def cleared_annotation(**overrides):
    values = {
        "candidate_id": "CND-M061",
        "workspace_id": "WS-M061",
        "source_type": SourceType.ARCHIVAL,
        "media_type": MediaType.VIDEO_CLIP,
        "start_time": 10.0,
        "end_time": 14.0,
        "duration": 4.0,
        "contextual_caption": "Archival control-room footage that visually echoes a hard-won operational milestone.",
        "semantic_role": "HISTORICAL_TRIUMPH_METAPHOR",
        "insert_role": EditorialInsertRole.SEMANTIC_SIMILE,
        "source_sha256": "a" * 64,
        "rights": RightsMetadata(
            status=RightsStatus.CLEARED,
            license_id="LIC-M061-001",
            copyright_holder="Archive Holder",
            allowed_territories=["GLOBAL"],
        ),
    }
    values.update(overrides)
    return AssetAnnotation(**values)


def test_program_emits_provider_neutral_asset_demand_with_field_level_semantics():
    program, receipt = build_program()

    contract = compile_production_asset_demand(program)

    assert receipt.asset_id_list == []
    assert contract.state == AssetResolutionState.DEMAND_EMITTED
    assert contract.workspace_id == "WS-M061"
    assert contract.program_ref.object_id == program.program_id
    assert contract.program_ref.version == "1.0.0"

    demand = contract.demands[0]
    assert demand.segment_id == "SEG-M061-01"
    assert demand.media.media_type == MediaType.VIDEO_CLIP
    assert demand.media.duration.minimum_seconds == 3.0
    assert demand.media.duration.maximum_seconds == 6.0
    assert demand.semantic_obligation.scene_role == SceneRole.EVIDENCE_CLIMAX
    assert demand.semantic_obligation.semantic_role == "HISTORICAL_TRIUMPH_METAPHOR"
    assert demand.semantic_obligation.obligation.startswith("Provide archival footage")
    assert demand.rights.acceptable_statuses == ("CLEARED",)
    assert demand.rights.license_required is True
    assert demand.provenance_ref.object_id == "SEG-M061-01"
    assert demand.provenance_ref.sha256 == TEXT_SHA


def test_catalog_resolution_satisfies_every_declared_constraint_without_reselection():
    program, _ = build_program()
    contract = compile_production_asset_demand(program)
    asset = cleared_annotation()
    resolved = AssetDemandResolver.resolve_catalog(
        demand_contract=contract,
        catalog=AssetCatalog(
            candidate_id="CND-M061",
            workspace_id="WS-M061",
            assets=[asset],
        ),
    )

    assert resolved.state == AssetResolutionState.SATISFIED
    assert resolved.resolutions[0].state == AssetResolutionState.SATISFIED
    assert resolved.resolutions[0].asset_ref.object_id == asset.asset_id
    assert resolved.resolutions[0].matched_duration_seconds == 4.0
    assert resolved.resolutions[0].resolved_rights_status == "CLEARED"


def test_false_proof_wrong_semantic_role_is_blocked_even_when_physical_media_is_valid():
    program, _ = build_program()
    contract = compile_production_asset_demand(program)
    wrong_meaning_asset = cleared_annotation(semantic_role="GENERIC_ARCHIVE")

    outcome = AssetDemandResolver.resolve_candidate(
        demand_contract=contract,
        demand_id=contract.demands[0].demand_id,
        annotation=wrong_meaning_asset,
    )

    assert outcome.state == AssetResolutionState.BLOCKED
    assert outcome.reason_code == "SEMANTIC_OBLIGATION_MISMATCH"


def test_false_proof_wrong_provenance_hash_is_rejected_before_resolution():
    program, _ = build_program()
    program_data = program.model_dump(mode="python")
    program_data["scenes"][0]["asset_demands"][0]["evidence_sha256"] = "b" * 64

    with pytest.raises(AssetDemandValidationError, match="evidence_sha256"):
        compile_production_asset_demand(program_data)


def test_duration_and_rights_constraints_are_real_gates():
    program, _ = build_program()
    contract = compile_production_asset_demand(program)

    short_asset = cleared_annotation(end_time=12.5, duration=2.5)
    short_outcome = AssetDemandResolver.resolve_candidate(
        demand_contract=contract,
        demand_id=contract.demands[0].demand_id,
        annotation=short_asset,
    )
    assert short_outcome.reason_code == "DURATION_CONSTRAINT_VIOLATION"

    unlicensed_asset = cleared_annotation(
        rights=RightsMetadata(
            status=RightsStatus.CLEARED,
            copyright_holder="Archive Holder",
            allowed_territories=["GLOBAL"],
        )
    )
    rights_outcome = AssetDemandResolver.resolve_candidate(
        demand_contract=contract,
        demand_id=contract.demands[0].demand_id,
        annotation=unlicensed_asset,
    )
    assert rights_outcome.reason_code == "RIGHTS_CONSTRAINT_VIOLATION"


def test_cross_workspace_catalog_is_blocked():
    program, _ = build_program()
    contract = compile_production_asset_demand(program)

    with pytest.raises(Exception, match="scope"):
        AssetDemandResolver.resolve_catalog(
            demand_contract=contract,
            catalog=AssetCatalog(
                candidate_id="CND-M061",
                workspace_id="OTHER-WS",
                assets=[cleared_annotation(workspace_id="OTHER-WS")],
            ),
        )
