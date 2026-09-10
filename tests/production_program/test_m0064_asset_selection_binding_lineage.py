import pydantic_core
"""
CAE-M0064 — Asset Selection, Production Binding and Lineage Handoff.

These tests cover exact selected identity, interval, rights and provenance preservation,
runtime projection, tamper detection, invalidation, and the mandatory false-proof cases.
"""

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "production-program" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "ca_runtime" / "src"))

from cae_production_program.composition_asset_pack import (  # noqa: E402
    AssetBindingInvalidatedError,
    AssetLineageValidationError,
    CompositionAssetPack,
    ExplicitSelectionReceipt,
    apply_composition_asset_pack,
    bind_selected_retrieval_candidates,
    invalidate_composition_asset_pack,
)
from cae_production_program.compiler import ProductionProgramCompiler  # noqa: E402
from cae_production_program.domain import SceneRole  # noqa: E402
import importlib.util
_runtime_spec = importlib.util.spec_from_file_location(
    "ca_runtime_composition_asset_handoff",
    ROOT / "packages" / "ca_runtime" / "src" / "ca_runtime" / "composition_asset_handoff.py",
)
_runtime_module = importlib.util.module_from_spec(_runtime_spec)
assert _runtime_spec.loader is not None
_runtime_spec.loader.exec_module(_runtime_module)
RuntimeAssetLineageError = _runtime_module.RuntimeAssetLineageError
resolve_runtime_asset_inputs = _runtime_module.resolve_runtime_asset_inputs
verify_runtime_asset_handoff = _runtime_module.verify_runtime_asset_handoff


TEXT = "The archive image turns the operational claim into visible evidence without changing the source meaning."
TEXT_SHA = hashlib.sha256(TEXT.encode("utf-8")).hexdigest()
ASSET_SHA = "a" * 64


def _program():
    program, _ = ProductionProgramCompiler.compile_program(
        candidate_id="CND-M064",
        workspace_id="WS-M064",
        title="M0064 lineage proof",
        semantic_intent="Bind an explicitly selected retrieval candidate without semantic mutation.",
        story_arc="THE_EVIDENCE",
        scenes_data=[
            {
                "scene_role": SceneRole.EVIDENCE_CLIMAX,
                "segment_id": "SEG-M064-01",
                "spoken_text": TEXT,
                "text_sha256": TEXT_SHA,
                "start_time": 0.0,
                "end_time": 6.0,
                "asset_inserts": [],
            }
        ],
        approved_asset_ids=[],
        wrong_reading_locks=["Never substitute a visually similar asset."],
    )
    return program


def _selection_receipt():
    core = {
        "receipt_id": "SEL-M064-001",
        "workspace_id": "WS-M064",
        "candidate_id": "CND-M064",
        "selected_asset_ids": ["AST-M064-001"],
        "selected_scene_ids": ["SCN-M064-001"],
        "actor": "operator-m064",
        "authority": "OPERATOR_SELECTION",
        "source_receipt_refs": ["RRET-M064-001"],
        "created_at": "2026-09-10T00:00:00+00:00",
    }
    encoded = hashlib.sha256(
        __import__("json").dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    return ExplicitSelectionReceipt(**core, receipt_sha256=encoded)


def _candidate(**overrides):
    value = {
        "scene_id": "SCN-M064-001",
        "asset_id": "AST-M064-001",
        "candidate_id": "CND-M064",
        "workspace_id": "WS-M064",
        "source_version": "v7",
        "source_sha256": ASSET_SHA,
        "start_time": 10.25,
        "end_time": 14.75,
        "duration": 4.5,
        "contextual_explanation": "Archival proof of an operational turning point.",
        "semantic_role": "HISTORICAL_TRIUMPH_METAPHOR",
        "insert_role": "SEMANTIC_SIMILE",
        "rights_status": "CLEARED",
        "rights": {
            "status": "CLEARED",
            "license_id": "LIC-M064-001",
            "allowed_territories": ["GLOBAL"],
        },
        "provenance": {
            "scene_id": "SCN-M064-001",
            "media_id": "MEDIA-M064-001",
            "source_version": "v7",
            "source_sha256": ASSET_SHA,
            "candidate_id": "CND-M064",
            "mandate_id": "CAE-M0063",
        },
        "lexical_score": 0.91,
        "semantic_score": 0.88,
        "hybrid_score": 0.90,
        "confidence": 0.90,
        "match_terms": ("archive", "turning"),
    }
    value.update(overrides)
    return value


def _pack(program=None):
    program = program or _program()
    program_ref = {
        "object_id": program.program_id,
        "version": program.program_version,
        "sha256": hashlib.sha256(
            __import__("json").dumps(
                program.model_dump(mode="python"), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
            ).encode()
        ).hexdigest(),
        "workspace_id": program.workspace_id,
        "candidate_id": program.candidate_id,
    }
    return bind_selected_retrieval_candidates(
        program_ref=program_ref,
        selection_receipt=_selection_receipt(),
        retrieval_candidates=[_candidate()],
        retrieval_receipt_id="RRET-M064-001",
        scene_index_by_scene_id={"SCN-M064-001": 1},
    )


def test_selected_candidate_becomes_typed_composition_asset_pack():
    pack = _pack()
    binding = pack.bindings[0]

    assert pack.state == "BOUND"
    assert binding.asset_id == "AST-M064-001"
    assert binding.source_version == "v7"
    assert binding.source_sha256 == ASSET_SHA
    assert (binding.start_time, binding.end_time, binding.duration) == (10.25, 14.75, 4.5)
    assert binding.rights["license_id"] == "LIC-M064-001"
    assert binding.provenance["media_id"] == "MEDIA-M064-001"
    assert binding.selection_receipt_id == "SEL-M064-001"
    assert len(pack.lineage_root_sha256) == 64


def test_pack_projects_into_existing_semantic_program_without_reselection():
    program = _program()
    packed = _pack(program)
    bound_program, receipt = apply_composition_asset_pack(program, packed)
    insert = bound_program.scenes[0].asset_inserts[0]

    assert insert["asset_id"] == "AST-M064-001"
    assert insert["asset_sha256"] == ASSET_SHA
    assert (insert["source_start_time"], insert["source_end_time"]) == (10.25, 14.75)
    assert insert["semantic_role"] == "HISTORICAL_TRIUMPH_METAPHOR"
    assert insert["insert_role"] == "SEMANTIC_SIMILE"
    assert insert["rights"]["license_id"] == "LIC-M064-001"
    assert insert["provenance"]["media_id"] == "MEDIA-M064-001"
    assert receipt.metadata["lineage_root_sha256"] == packed.lineage_root_sha256
    assert receipt.metadata["pack_sha256"] == packed.pack_sha256


def test_runtime_handoff_preserves_exact_binding_and_is_tamper_evident():
    pack = _pack()
    handoff = resolve_runtime_asset_inputs(pack)
    assert verify_runtime_asset_handoff(handoff)
    runtime = handoff.inputs[0]

    assert runtime.asset_id == "AST-M064-001"
    assert runtime.asset_sha256 == ASSET_SHA
    assert (runtime.source_start_time, runtime.source_end_time) == (10.25, 14.75)
    assert runtime.rights["license_id"] == "LIC-M064-001"
    assert runtime.provenance["media_id"] == "MEDIA-M064-001"
    assert runtime.lineage_root_sha256 == pack.lineage_root_sha256

    tampered = handoff.model_copy(update={"inputs": tuple([runtime.model_copy(update={"asset_sha256": "b" * 64})])})
    with pytest.raises(RuntimeAssetLineageError, match="digest mismatch"):
        verify_runtime_asset_handoff(tampered)


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("source_sha256", "b" * 64, "identity, timestamp, rights, role, or provenance"),
        ("start_time", 11.0, "identity, timestamp, rights, role, or provenance"),
        ("semantic_role", "GENERIC_ARCHIVE", "identity, timestamp, rights, role, or provenance"),
        ("rights", {"status": "RESTRICTED"}, "identity, timestamp, rights, role, or provenance"),
        ("provenance", {"media_id": "MEDIA-WRONG", "source_sha256": ASSET_SHA}, "identity, timestamp, rights, role, or provenance"),
    ],
)
def test_false_proof_modified_candidate_is_invalidated(field, value, error):
    pack = _pack()
    changed = _candidate()
    changed[field] = value
    if field == "start_time":
        changed["end_time"] = 15.5
        changed["duration"] = 4.5
    with pytest.raises(AssetBindingInvalidatedError, match=error):
        from cae_production_program.composition_asset_pack import validate_composition_asset_pack
        validate_composition_asset_pack(pack, current_retrieval_candidates=[changed])


def test_false_proof_wrong_candidate_or_scene_cannot_bind():
    program = _program()
    program_ref = {
        "object_id": program.program_id,
        "version": program.program_version,
        "sha256": hashlib.sha256(
            __import__("json").dumps(program.model_dump(mode="python"), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()
        ).hexdigest(),
        "workspace_id": program.workspace_id,
        "candidate_id": program.candidate_id,
    }
    receipt = _selection_receipt().model_copy(update={"selected_asset_ids": ("AST-M064-001",), "selected_scene_ids": ("SCN-OTHER",)})
    with pytest.raises(AssetLineageValidationError, match="present in the explicit selection receipt"):
        bind_selected_retrieval_candidates(
            program_ref=program_ref,
            selection_receipt=receipt,
            retrieval_candidates=[_candidate()],
            retrieval_receipt_id="RRET-M064-001",
            scene_index_by_scene_id={"SCN-M064-001": 1},
        )


def test_invalidation_creates_new_state_without_mutating_historical_bound_pack():
    bound = _pack()
    invalidated = invalidate_composition_asset_pack(bound)
    assert bound.state == "BOUND"
    assert invalidated.state == "INVALIDATED"
    assert invalidated.pack_sha256 != bound.pack_sha256
    with pytest.raises(AssetBindingInvalidatedError):
        from cae_production_program.composition_asset_pack import validate_composition_asset_pack
        validate_composition_asset_pack(invalidated)


def test_runtime_rejects_candidate_set_substitution():
    pack = _pack()
    with pytest.raises(RuntimeAssetLineageError, match="candidate set"):
        resolve_runtime_asset_inputs(
            pack,
            current_retrieval_candidates=[_candidate(asset_id="AST-M064-SUBSTITUTE", scene_id="SCN-M064-001")],
        )


def test_pack_identity_is_deterministic_for_same_inputs_except_creation_time():
    program = _program()
    first = _pack(program)
    second = _pack(program)
    assert first.lineage_root_sha256 == second.lineage_root_sha256
    assert first.pack_id == second.pack_id


def test_program_reference_change_invalidates_the_bound_pack():
    program = _program()
    pack = _pack(program)
    changed_ref = dict(pack.program_ref)
    changed_ref["sha256"] = "c" * 64
    from cae_production_program.composition_asset_pack import validate_composition_asset_pack
    with pytest.raises(AssetBindingInvalidatedError, match="program reference"):
        validate_composition_asset_pack(pack, current_program_ref=changed_ref)


def test_selection_receipt_cannot_name_unbound_scene():
    program = _program()
    program_ref = {
        "object_id": program.program_id,
        "version": program.program_version,
        "sha256": hashlib.sha256(
            __import__("json").dumps(
                program.model_dump(mode="python"), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
            ).encode()
        ).hexdigest(),
        "workspace_id": program.workspace_id,
        "candidate_id": program.candidate_id,
    }
    core = {
        "receipt_id": "SEL-M064-EXTRA",
        "workspace_id": "WS-M064",
        "candidate_id": "CND-M064",
        "selected_asset_ids": ["AST-M064-001"],
        "selected_scene_ids": ["SCN-M064-001", "SCN-EXTRA"],
        "actor": "operator-m064",
        "authority": "OPERATOR_SELECTION",
        "source_receipt_refs": ["RRET-M064-001"],
        "created_at": "2026-09-10T00:00:00+00:00",
    }
    receipt_sha = hashlib.sha256(
        __import__("json").dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    receipt = ExplicitSelectionReceipt(**core, receipt_sha256=receipt_sha)
    with pytest.raises((AssetLineageValidationError, pydantic_core.ValidationError), match="selection receipt scene set does not equal bound scene set"):
        bind_selected_retrieval_candidates(
            program_ref=program_ref,
            selection_receipt=receipt,
            retrieval_candidates=[_candidate()],
            retrieval_receipt_id="RRET-M064-001",
            scene_index_by_scene_id={"SCN-M064-001": 1},
        )
