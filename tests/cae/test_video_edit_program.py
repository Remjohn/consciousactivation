"""
CAE Program Test Suite: Video Edit Production Program (Phase 4 Mandate M43).

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M43_video_edit_compositionir_cmf_runtime.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from uuid import UUID, uuid4
import pytest

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    UniversalProgramStateRuntime,
    get_canonical_video_edit_state_machine,
)
from ca_runtime.video_edit_program import (
    DualAxisVideoQAReceipt,
    EvidenceQuoteMismatchError,
    LaneAuthorityViolationError,
    RenderQAFailureError,
    SemanticQAFailureError,
    SourceLineageMissingError,
    SyntheticVideoBlockedError,
    UnapprovedVideoReleaseError,
    VideoEditError,
    VideoEditProductionCoordinator,
    VideoEditRenderArtifact,
    VideoEditSourceSpan,
    VideoReleaseReceipt,
    WorkspaceScopeViolationError,
    WrongReadingLockMissingError,
)
from ca_runtime.tenancy import TenantContext, tenant_scope


# ----------------------------------------------------------------------------
# Authentic Jean Pierre (03_50-12) Fixture Data
# ----------------------------------------------------------------------------

JEAN_PIERRE_SEGMENTS = [
    {
        "segment_id": "seg-jp-001",
        "spoken_text": "We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.",
        "text_sha256": hashlib.sha256("We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.".encode("utf-8")).hexdigest(),
        "start_time_ms": 0,
        "end_time_ms": 2000,
        "speaker_id": "jean-pierre-001",
    },
    {
        "segment_id": "seg-jp-002",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "text_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode("utf-8")).hexdigest(),
        "start_time_ms": 2000,
        "end_time_ms": 4000,
        "speaker_id": "jean-pierre-001",
    },
]

WRONG_READING_LOCKS = [
    "Do not portray operators as negligent or lazy.",
    "Do not depict the factory as dark or dystopian.",
]


@pytest.fixture
def test_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def foreign_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def test_tenant_context(test_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(test_workspace_id),
        actor_id="op-jp-lead-001",
        role="MEMBER",
    )


@pytest.fixture
def program_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def coordinator(program_runtime: UniversalProgramStateRuntime) -> VideoEditProductionCoordinator:
    return VideoEditProductionCoordinator(runtime=program_runtime)


@pytest.fixture
def source_video_file(tmp_path: Path) -> Path:
    """Generate a real 4-second video file using ffmpeg."""
    video_path = tmp_path / "source_interview.mp4"
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
        "-t", "4",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        str(video_path),
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    assert p.returncode == 0, f"FFmpeg error: {p.stderr}"
    return video_path


# ----------------------------------------------------------------------------
# Test 1: Program Package Discovery & Manifest Integrity
# ----------------------------------------------------------------------------

def test_video_edit_program_discovery_and_manifest(test_workspace_id: str):
    programs_dir = Path(__file__).resolve().parents[2] / "programs"
    registry = ProgramRegistry(discovery_roots=[programs_dir])
    discovered = registry.discover()
    discovered_ids = [p.program_id for p in discovered]
    assert "video_edit_program" in discovered_ids

    pkg = registry.get_program("video_edit_program", "1.0.0")
    assert pkg is not None
    assert pkg.manifest.id == "video_edit_program"
    assert pkg.manifest.version == "1.0.0"
    assert set(pkg.manifest.lanes) == {"COMMANDER", "HUNTER", "ANALYST", "COMPOSER"}
    assert len(pkg.manifest.skills) == 3

    skill_names = {s.name for s in pkg.manifest.skills}
    assert "video_source_extractor" in skill_names
    assert "video_edl_compiler" in skill_names
    assert "video_qa_evaluator" in skill_names

    preflight = registry.preflight(
        "video_edit_program",
        test_workspace_id,
        context_refs=["workspace_active", "material_admitted", "source_media_registered", "evidence_verified"],
    )
    assert preflight.eligible is True


# ----------------------------------------------------------------------------
# Test 2: Canonical State Machine Grammar & Transitions
# ----------------------------------------------------------------------------

def test_video_edit_state_machine_grammar_and_transitions():
    sm = get_canonical_video_edit_state_machine()
    assert sm.machine_id == "VIDEO_EDIT_STATE_MACHINE_V1"
    assert sm.program_id == "video_edit_program"
    assert sm.initial_state == "INITIAL"

    expected_transitions = {
        "admit_semantic_material": ("INITIAL", "MATERIAL_ADMITTED", AuthorityLane.COMMANDER),
        "register_source_media": ("MATERIAL_ADMITTED", "SOURCE_REGISTERED", AuthorityLane.HUNTER),
        "compile_word_boundary_edl": ("SOURCE_REGISTERED", "EDL_COMPILED", AuthorityLane.COMPOSER),
        "compile_video_edit_program": ("EDL_COMPILED", "PROGRAM_COMPILED", AuthorityLane.COMPOSER),
        "compile_export_bindings": ("PROGRAM_COMPILED", "BINDINGS_COMPILED", AuthorityLane.COMPOSER),
        "realize_ffmpeg_render": ("BINDINGS_COMPILED", "VIDEO_RENDERED", AuthorityLane.COMPOSER),
        "evaluate_dual_axis_qa": ("VIDEO_RENDERED", "QA_EVALUATED", AuthorityLane.ANALYST),
        "authorize_video_release": ("QA_EVALUATED", "RELEASE_AUTHORIZED", AuthorityLane.COMMANDER),
    }

    for t_name, (from_s, to_s, lane) in expected_transitions.items():
        assert t_name in sm.transitions
        contract = sm.transitions[t_name]
        assert contract.from_state == from_s
        assert contract.to_state == to_s
        assert contract.required_lane == lane


# ----------------------------------------------------------------------------
# Test 3: Full End-to-End Video Edit Production Lifecycle
# ----------------------------------------------------------------------------

def test_full_video_edit_production_lifecycle_e2e(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    source_video_file: Path,
    tmp_path: Path,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-video-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {
            "program_id": "sem-jp-video-001",
            "narrative_arc": "The Witness",
            "scenes": JEAN_PIERRE_SEGMENTS,
        }

        # 1. Admit Semantic Material (COMMANDER)
        agg = coordinator.admit_semantic_material(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
            aggregate_id=agg_id,
        )
        assert agg.current_state == "MATERIAL_ADMITTED"
        effective_agg_id = agg.aggregate_id

        # 2. Register Source Media & Extract Spans (HUNTER)
        agg = coordinator.register_source_media(
            aggregate_id=effective_agg_id,
            source_path=source_video_file,
            logical_uri="workspace://interview/jp_raw.mp4",
            evidence_segments=JEAN_PIERRE_SEGMENTS,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )
        assert agg.current_state == "SOURCE_REGISTERED"
        assert len(agg.state_data["source_spans"]) == 2

        # 3. Compile Word Boundary EDL (COMPOSER)
        words = [
            {"word_id": "w1", "text": "We", "start_ms": 0, "end_ms": 400, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w2", "text": "were", "start_ms": 400, "end_ms": 800, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w3", "text": "running", "start_ms": 800, "end_ms": 1400, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w4", "text": "thirty", "start_ms": 1400, "end_ms": 2000, "speaker_id": "jean-pierre-001", "protected_tail_ms": 30},
            {"word_id": "w5", "text": "thousand", "start_ms": 2000, "end_ms": 2800, "speaker_id": "jean-pierre-001", "protected_tail_ms": 30},
            {"word_id": "w6", "text": "units", "start_ms": 2800, "end_ms": 3500, "speaker_id": "jean-pierre-001", "protected_tail_ms": 40},
        ]
        selections = [
            {"selection_id": "sel1", "start_word_id": "w1", "end_word_id": "w3", "function": "hook"},
            {"selection_id": "sel2", "start_word_id": "w4", "end_word_id": "w6", "function": "problem"},
        ]

        agg = coordinator.compile_word_boundary_edl(
            aggregate_id=effective_agg_id,
            words=words,
            selections=selections,
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "EDL_COMPILED"
        edl = agg.state_data["edl"]
        assert len(edl["entries"]) == 2
        assert edl["output_duration_ms"] > 0

        # 4. Compile VideoEditProgram (COMPOSER)
        canvas = {"width": 360, "height": 640}
        timebase = {"fps_numerator": 30, "fps_denominator": 1}
        tracks = [
            {
                "track_id": "track_a_roll",
                "role": "PRIMARY_A_ROLL_SPINE",
                "elements": [
                    {
                        "element_id": "elem_1",
                        "kind": "SOURCE_SEGMENT",
                        "edl_entry_id": edl["entries"][0]["entry_id"],
                        "source_span": {"start_ms": 0, "end_ms": 1420},
                        "timeline_start_ms": 0,
                        "timeline_end_ms": 1420,
                    },
                    {
                        "element_id": "elem_2",
                        "kind": "SOURCE_SEGMENT",
                        "edl_entry_id": edl["entries"][1]["entry_id"],
                        "source_span": {"start_ms": 1400, "end_ms": 3540},
                        "timeline_start_ms": 1420,
                        "timeline_end_ms": 3560,
                    },
                ],
            }
        ]

        agg = coordinator.compile_video_edit_program(
            aggregate_id=effective_agg_id,
            canvas=canvas,
            timebase=timebase,
            tracks=tracks,
            wrong_reading_locks=WRONG_READING_LOCKS,
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "PROGRAM_COMPILED"

        # 5. Compile Export Bindings (COMPOSER)
        agg = coordinator.compile_export_bindings(
            aggregate_id=effective_agg_id,
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "BINDINGS_COMPILED"
        assert "remotion_binding" in agg.state_data
        assert "hyperframes_binding" in agg.state_data

        # 6. Realize Real FFmpeg Render Pass (COMPOSER)
        render_out_dir = tmp_path / "video_render_out"
        captions = ["We were running", "thirty thousand units"]
        agg = coordinator.realize_ffmpeg_render(
            aggregate_id=effective_agg_id,
            output_dir=render_out_dir,
            logical_output_uri="artifact://rendered/jp_final.mp4",
            workspace_id=ws_id,
            actor_id="composer-001",
            captions=captions,
        )
        assert agg.current_state == "VIDEO_RENDERED"
        render_artifact = agg.state_data["render_artifact"]
        output_mp4 = Path(render_artifact["output_path"])
        assert output_mp4.is_file()
        assert output_mp4.stat().st_size > 0
        assert render_artifact["srt_path"] is not None
        assert Path(render_artifact["srt_path"]).is_file()

        # 7. Dual-Axis QA Evaluation (ANALYST)
        evidence_dir = tmp_path / "qa_evidence"
        agg = coordinator.evaluate_dual_axis_qa(
            aggregate_id=effective_agg_id,
            workspace_id=ws_id,
            actor_id="analyst-001",
            evidence_dir=evidence_dir,
        )
        assert agg.current_state == "QA_EVALUATED"
        qa_receipt = agg.state_data["dual_axis_qa_receipt"]
        assert qa_receipt["overall_result"] == "PASS"
        assert qa_receipt["semantic_qa_passed"] is True
        assert qa_receipt["render_qa_passed"] is True
        assert len(list(evidence_dir.glob("*.png"))) >= 2

        # 8. Authorize Video Release (COMMANDER)
        agg = coordinator.authorize_video_release(
            aggregate_id=effective_agg_id,
            operator_id=test_tenant_context.actor_id,
            rationale="Authentic 03_50-12 Jean Pierre source render passed dual-axis QA with complete cut frame evidence",
            workspace_id=ws_id,
        )
        assert agg.current_state == "RELEASE_AUTHORIZED"
        release_rcpt = agg.state_data["video_release_receipt"]
        assert release_rcpt["program_id"] == "video_edit_program"
        assert release_rcpt["operator_id"] == test_tenant_context.actor_id
        assert release_rcpt["receipt_sha256"] is not None


# ----------------------------------------------------------------------------
# Test 4: Strict 4-Lane Authority Separation
# ----------------------------------------------------------------------------

def test_four_lane_authority_separation_strict_enforcement(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-lane-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-lane-001", "scenes": JEAN_PIERRE_SEGMENTS}

        # 1. Admit requires COMMANDER (HUNTER must fail)
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.admit_semantic_material(
                semantic_program=sem_prog,
                workspace_id=ws_id,
                operator_id=test_tenant_context.actor_id,
                aggregate_id=agg_id,
                lane=AuthorityLane.HUNTER,
            )


# ----------------------------------------------------------------------------
# Test 5: Fail-Closed Anti-Synthetic Derivative Blocking
# ----------------------------------------------------------------------------

def test_anti_synthetic_fail_closed_blocking(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-synth-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        synthetic_prog = {
            "program_id": "sem-synth-001",
            "is_synthetic": True,
            "scenes": [],
        }

        with pytest.raises(SyntheticVideoBlockedError):
            coordinator.admit_semantic_material(
                semantic_program=synthetic_prog,
                workspace_id=ws_id,
                operator_id=test_tenant_context.actor_id,
                aggregate_id=agg_id,
            )


# ----------------------------------------------------------------------------
# Test 6: Evidence Quote Tamper Detection
# ----------------------------------------------------------------------------

def test_evidence_quote_tamper_detection(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    source_video_file: Path,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-tamper-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-tamper-001", "scenes": JEAN_PIERRE_SEGMENTS}
        agg = coordinator.admit_semantic_material(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
            aggregate_id=agg_id,
        )

        tampered_segments = [
            {
                "segment_id": "seg-jp-001",
                "spoken_text": "We were running thirty thousand units a day...",
                "text_sha256": "bad_hash_00000000000000000000000000000000000000000000000000000000",
                "start_time_ms": 0,
                "end_time_ms": 2000,
            }
        ]

        with pytest.raises(EvidenceQuoteMismatchError):
            coordinator.register_source_media(
                aggregate_id=agg.aggregate_id,
                source_path=source_video_file,
                logical_uri="workspace://interview/jp_raw.mp4",
                evidence_segments=tampered_segments,
                workspace_id=ws_id,
                actor_id="hunter-001",
            )


# ----------------------------------------------------------------------------
# Test 7: Multi-Tenant Workspace Isolation Denial
# ----------------------------------------------------------------------------

def test_multi_tenant_workspace_isolation_denial(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    foreign_workspace_id: str,
):
    agg_id = f"agg-cross-tenant-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-007", "scenes": JEAN_PIERRE_SEGMENTS}

        with pytest.raises(WorkspaceScopeViolationError):
            coordinator.admit_semantic_material(
                semantic_program=sem_prog,
                workspace_id=foreign_workspace_id,
                operator_id=test_tenant_context.actor_id,
                aggregate_id=agg_id,
            )
