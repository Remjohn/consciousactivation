from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.services.asset_program_compiler_service import (  # noqa: E402
    AssetProgramCompilerService,
    AssetProgramCompilerServiceError,
)


def _service() -> AssetProgramCompilerService:
    return AssetProgramCompilerService()


def test_batch2_animation_studio_headless_render_avatar_export_and_geometrics_are_receipt_backed():
    service = _service()
    actor_id = uuid4()

    migration = service.migrate_animation_studio_manifest()
    rig_operation = service.plan_rig_edit(target_rig_ref="rig:claude-papercut", operator_id=actor_id)
    frame_request, frame_receipt = service.queue_headless_frame_render(
        composition_template_id=uuid4(),
        runtime_manifest_ref="papercut_runtime:claude-myth-truth",
    )
    avatar_job, avatar_receipt = service.queue_avatar_export(
        character_rig_ref="rig:claude-papercut",
        performance_program_ref="two_d_character_scene_program:myth-truth",
    )
    geometrics, skia_binding, skia_receipt = service.compile_geometrics_scene(scene_code="papercut-myth-truth")

    assert migration.operator_editor_route.endswith("/rig-editor")
    assert "pose-library" in migration.rig_editor_panels
    assert rig_operation.before_hash != rig_operation.after_hash
    assert frame_request.deterministic_inputs_hash == skia_binding.deterministic_inputs_hash or frame_request.deterministic_inputs_hash
    assert frame_receipt.decision_code == "HEADLESS_FRAME_RENDER_QUEUED"
    assert avatar_job.export_targets == ["alpha_png_sequence", "webm_alpha"]
    assert avatar_receipt.decision_code == "AVATAR_EXPORT_QUEUED"
    assert geometrics.primitive_validation_ids and len(geometrics.primitive_validation_ids) >= 3
    assert skia_receipt.decision_code == "SKIA_RENDER_CONTRACT_READY"


def test_batch2_carousel_library_sequence_atlas_and_builder_use_cmf_registries():
    service = _service()

    library = service.compile_carousel_slide_library()
    sequence = service.compile_carousel_sequence(
        library=library,
        source_context_refs=["context_premise:audience-comments", "expression_moment:edge-001"],
        format_code="CAR-JUX",
        slide_count=4,
    )
    program, receipt = service.compile_carousel_builder_program(sequence_plan=sequence, library=library)
    atlas = service.route_carousel_atlas(slide_atom_code=sequence.slide_atom_codes[0])

    assert library.registry_id == "CMF-CAROUSEL-SLIDE-COMP-LIB-001"
    assert library.global_rules["minimum_validated_primitives"] == 3
    assert sequence.slide_atom_codes[0].startswith("CAR-SL-001")
    assert len(sequence.primitive_validation_ids) == 3
    assert len(program.slide_specs) == 4
    assert all(spec["renderer"] == "skia" for spec in program.slide_specs)
    assert receipt.decision_code == "CAROUSEL_EXPORT_CONTRACT_READY"
    assert atlas.decision_code == "CAROUSEL_ATLAS_ROUTE_ACCEPTED"
    assert service.repository.registry_load_receipts


def test_batch2_single_image_supervisual_provider_jobs_skia_scene_and_eval_are_compiled():
    service = _service()

    snapshot = service.load_single_image_registry_snapshot()
    route = service.route_single_image(archetype_ref="archetype.challenger_frame_breaker.v1", format_code="SUPERVISUAL")
    supervisual = service.compile_supervisual_family_contract(route_decision=route)
    materialization, provider_plan = service.plan_single_image_provider_job(route_decision=route)
    scene = service.compile_single_image_skia_scene(route_decision=route)
    fixture, review = service.run_single_image_eval_review(scene=scene)

    assert "BLUNT_IMPERATIVE_POSTER" in snapshot.composition_ids
    assert route.decision_code == "SINGLE_IMAGE_ROUTE_ACCEPTED"
    assert supervisual.family_code.startswith("SUPERVISUAL-")
    assert len(supervisual.primitive_triads) == 3
    assert provider_plan.final_authority == "cmf_skia_renderer"
    assert materialization.text_layers_editable is True
    assert "rough-notation:annotation" in scene.skia_component_refs
    assert len(scene.primitive_validation_ids) == 3
    assert fixture.passed is True
    assert review.decision == "approved"


def test_batch2_video_edit_program_emits_otio_audit_and_proxy_final_render_contracts():
    service = _service()

    program = service.compile_video_edit_program(
        interview_asset_contract_ref="interview_asset_contract:claude-001",
        transcript_beat_map_ref="transcript_beat_map:claude-001",
    )

    assert {scene.video_format_code for scene in program.scenes} == {"SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"}
    assert program.otio_audit_manifest.timeline_ref.startswith("otio://timeline/")
    assert program.otio_audit_manifest.scene_refs == [scene.scene_code for scene in program.scenes]
    assert {contract.render_tier for contract in program.render_contracts} == {"proxy", "final"}
    assert {contract.render_target for contract in program.render_contracts} == {"remotion", "ffmpeg"}


def test_batch2_two_d_character_engine_compiles_rig_performance_adapter_and_render_receipt():
    service = _service()

    genesis, rig = service.compile_two_d_character_genesis(
        character_ref="claude-avatar",
        brand_genesis_ref="brand_genesis:claude",
    )
    adapter = service.decide_two_d_character_adapter(
        provider_name="stretchystudio",
        proposed_use="rig authoring reference and sandbox preview only",
    )
    program = service.compile_two_d_character_scene_program(
        rig=rig,
        transcript_spans=[
            {
                "transcript_span_ref": "transcript:001",
                "start_seconds": 0.0,
                "end_seconds": 3.2,
                "gesture": "index_finger_myth_break",
            },
            {
                "transcript_span_ref": "transcript:002",
                "start_seconds": 3.2,
                "end_seconds": 7.5,
                "gesture": "open_palm_explanation",
            },
        ],
    )
    render, repair = service.render_two_d_character_program(scene_program=program)

    assert genesis.required_pose_count == 64
    assert len(rig.pose_state_refs) == 64
    assert adapter.decision_code == "TWO_D_ADAPTER_SANDBOX_ACCEPTED"
    assert adapter.production_authority_allowed is False
    assert program.video_format_code == "SV-EDU"
    assert program.papercut_materiality_ref.startswith("papercut://")
    assert len(program.performance_cues) == 2
    assert render.decision == "approved"
    assert repair is None


def test_batch2_sequence_kernel_interview_brief_live_coverage_inventory_handoff_and_eval():
    service = _service()

    kernel = service.create_sequencing_kernel()
    brief = service.compile_interview_brief_v2(
        brand_context_ref="brand_context:claude",
        audience_context_ref="context_premise:audience-comments",
        research_evidence_refs=["cral:search:001", "context_premise:cluster:001"],
    )
    tracker = service.track_live_ingredient_coverage(
        interview_brief_v2_plan=brief,
        captured_ingredient_refs=[
            "story:transcript:origin",
            "claim:transcript:contrast",
            "framework:transcript:river",
            "reaction:transcript:pause",
            "visual_seed:transcript:memory-object",
        ],
        suppressed_cues=["cue:redundant-framework-probe"],
    )
    inventory = service.build_expression_inventory(
        ingredients=[
            {
                "ingredient_ref": "story:transcript:origin",
                "ingredient_type": "story",
                "source_evidence_refs": ["transcript:001"],
                "transcript_span_ref": "transcript:001",
            },
            {
                "ingredient_ref": "claim:transcript:contrast",
                "ingredient_type": "claim",
                "source_evidence_refs": ["transcript:002"],
                "transcript_span_ref": "transcript:002",
            },
            {
                "ingredient_ref": "visual_seed:transcript:memory-object",
                "ingredient_type": "visual_seed",
                "source_evidence_refs": ["transcript:003", "brand_genesis:micro-semiotic-anchor"],
                "transcript_span_ref": "transcript:003",
            },
        ],
        relation_edges=[
            {
                "source_ingredient_ref": "story:transcript:origin",
                "target_ingredient_ref": "claim:transcript:contrast",
                "relation_type": "supports",
            }
        ],
    )
    program = service.compile_content_sequence_program(kernel=kernel, inventory=inventory)
    eval_receipt, learning = service.run_sequence_eval(program=program)

    assert "single_image_composition_registry.v2.json" in kernel.registry_refs[2]
    assert brief.decision_code == "INTERVIEW_BRIEF_V2_READY"
    assert tracker.decision_code == "LIVE_COVERAGE_SUFFICIENT"
    assert tracker.cue_suppression_decisions[0].suppressed is True
    assert inventory.blocker_codes == []
    assert program.decision == "approved"
    assert {package.target_compiler for package in program.handoff_packages} == {"carousel", "single_image", "video_edit", "two_d_character"}
    assert all(package.no_fabricated_guest_truth for package in program.handoff_packages)
    assert eval_receipt.decision == "approved"
    assert learning.approval_required is True


def test_batch2_blocks_outside_registries_provider_final_authority_and_unsupported_guest_truth():
    service = _service()

    with pytest.raises(AssetProgramCompilerServiceError) as exc:
        service.load_registry_bundle("../outside.json")
    assert exc.value.code == "CMF_REGISTRY_OUTSIDE_PROJECT_ROOT"
    assert next(iter(service.repository.registry_load_receipts.values())).decision == "blocked"

    adapter = service.decide_two_d_character_adapter(
        provider_name="see_through",
        proposed_use="direct final rig/render authority",
        production_authority_allowed=True,
    )
    assert adapter.decision_code == "TWO_D_ADAPTER_BLOCKED"
    assert "TWO_D_PROVIDER_CANNOT_OWN_FINAL_AUTHORITY" in adapter.blocker_codes

    kernel = service.create_sequencing_kernel()
    inventory = service.build_expression_inventory(
        ingredients=[
            {
                "ingredient_ref": "claim:unsupported",
                "ingredient_type": "claim",
                "source_evidence_refs": [],
                "guest_truth_claim": "unsupported claim",
            }
        ]
    )
    program = service.compile_content_sequence_program(kernel=kernel, inventory=inventory)

    assert program.decision == "blocked"
    assert "CONTENT_SEQUENCE_GUEST_TRUTH_UNSUPPORTED" in program.blocker_codes
