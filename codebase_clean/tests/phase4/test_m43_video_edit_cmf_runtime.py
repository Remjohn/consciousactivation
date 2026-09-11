"""
Phase 4 Mandate M43 Acceptance Test Suite:
Video Edit + CompositionIR + CMF Runtime.

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M43_video_edit_compositionir_cmf_runtime.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
- 00_CONTROL/37_PHASE4_PRODUCTION_FIXTURE_PACK.md
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
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
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
        "end_time_ms": 2200,
        "speaker_id": "jean-pierre-001",
    },
    {
        "segment_id": "seg-jp-002",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "text_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode("utf-8")).hexdigest(),
        "start_time_ms": 2200,
        "end_time_ms": 4200,
        "speaker_id": "jean-pierre-001",
    },
]

WRONG_READING_LOCKS = [
    "Do not portray operators as negligent or lazy.",
    "Do not depict the factory as dark or dystopian.",
    "Do not suggest AI completely replaces human operators.",
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
def authentic_source_video(tmp_path: Path) -> Path:
    """Generate a real 5-second video source fixture using ffmpeg testsrc2 and sine wave."""
    video_path = tmp_path / "jean_pierre_interview.mp4"
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=30",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
        "-t", "5",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        str(video_path),
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    assert p.returncode == 0, f"FFmpeg error: {p.stderr}"
    return video_path


# ----------------------------------------------------------------------------
# Test 1: Full End-to-End Real Video Realization (Jean Pierre 03_50-12)
# ----------------------------------------------------------------------------

def test_full_m43_video_edit_production_e2e(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    authentic_source_video: Path,
    tmp_path: Path,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-m43-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {
            "program_id": "sem-jp-m43-001",
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
            source_path=authentic_source_video,
            logical_uri="workspace://03_50-12/interview_raw.mp4",
            evidence_segments=JEAN_PIERRE_SEGMENTS,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )
        assert agg.current_state == "SOURCE_REGISTERED"
        assert len(agg.state_data["source_spans"]) == 2

        # 3. Compile Word Boundary EDL (COMPOSER)
        words = [
            {"word_id": "w1", "text": "We", "start_ms": 0, "end_ms": 300, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w2", "text": "were", "start_ms": 300, "end_ms": 600, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w3", "text": "running", "start_ms": 600, "end_ms": 1200, "speaker_id": "jean-pierre-001", "protected_tail_ms": 20},
            {"word_id": "w4", "text": "Operators", "start_ms": 2200, "end_ms": 2800, "speaker_id": "jean-pierre-001", "protected_tail_ms": 30},
            {"word_id": "w5", "text": "were", "start_ms": 2800, "end_ms": 3200, "speaker_id": "jean-pierre-001", "protected_tail_ms": 30},
            {"word_id": "w6", "text": "fatigued", "start_ms": 3200, "end_ms": 4000, "speaker_id": "jean-pierre-001", "protected_tail_ms": 40},
        ]
        selections = [
            {"selection_id": "sel-1", "start_word_id": "w1", "end_word_id": "w3", "function": "hook"},
            {"selection_id": "sel-2", "start_word_id": "w4", "end_word_id": "w6", "function": "problem"},
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

        # 4. Compile VideoEditProgram (COMPOSER)
        canvas = {"width": 360, "height": 640}
        timebase = {"fps_numerator": 30, "fps_denominator": 1}
        tracks = [
            {
                "track_id": "track_a_roll",
                "role": "PRIMARY_A_ROLL_SPINE",
                "elements": [
                    {
                        "element_id": "el_1",
                        "kind": "SOURCE_SEGMENT",
                        "edl_entry_id": edl["entries"][0]["entry_id"],
                        "source_span": {"start_ms": 0, "end_ms": 1220},
                        "timeline_start_ms": 0,
                        "timeline_end_ms": 1220,
                    },
                    {
                        "element_id": "el_2",
                        "kind": "SOURCE_SEGMENT",
                        "edl_entry_id": edl["entries"][1]["entry_id"],
                        "source_span": {"start_ms": 2200, "end_ms": 4040},
                        "timeline_start_ms": 1220,
                        "timeline_end_ms": 3060,
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

        # 6. Realize Real FFmpeg Render Pass (COMPOSER)
        render_out_dir = tmp_path / "m43_rendered_out"
        captions = ["We were running", "Operators were fatigued"]
        agg = coordinator.realize_ffmpeg_render(
            aggregate_id=effective_agg_id,
            output_dir=render_out_dir,
            logical_output_uri="artifact://rendered/03_50-12_final.mp4",
            workspace_id=ws_id,
            actor_id="composer-001",
            captions=captions,
        )
        assert agg.current_state == "VIDEO_RENDERED"
        render_art = agg.state_data["render_artifact"]
        mp4_path = Path(render_art["output_path"])
        assert mp4_path.is_file()
        assert len(render_art["probe"]["streams"]) >= 1
        assert "format" in render_art["probe"]

        # 7. Dual-Axis QA Evaluation (ANALYST)
        evidence_dir = tmp_path / "m43_evidence"
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
        # Verify cut evidence frames were extracted to evidence_dir
        cut_frames = list(evidence_dir.glob("*.png"))
        assert len(cut_frames) >= 2

        # 8. Authorize Video Release (COMMANDER)
        agg = coordinator.authorize_video_release(
            aggregate_id=effective_agg_id,
            operator_id=test_tenant_context.actor_id,
            rationale="Release approved: authentic Jean Pierre 03_50-12 source media rendered and verified with dual-axis QA",
            workspace_id=ws_id,
        )
        assert agg.current_state == "RELEASE_AUTHORIZED"
        rel_receipt = agg.state_data["video_release_receipt"]
        assert rel_receipt["receipt_id"].startswith("rcpt-release-")
        assert rel_receipt["operator_id"] == test_tenant_context.actor_id


# ----------------------------------------------------------------------------
# Test 2: Semantic QA Failure on Missing Primary A-Roll Spine
# ----------------------------------------------------------------------------

def test_semantic_qa_failure_on_missing_a_roll_spine(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    authentic_source_video: Path,
    tmp_path: Path,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-spine-fail-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-spine-001", "scenes": JEAN_PIERRE_SEGMENTS}
        agg = coordinator.admit_semantic_material(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
            aggregate_id=agg_id,
        )
        coordinator.register_source_media(
            aggregate_id=agg.aggregate_id,
            source_path=authentic_source_video,
            logical_uri="workspace://03_50-12/raw.mp4",
            evidence_segments=JEAN_PIERRE_SEGMENTS,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )

        words = [
            {"word_id": "w1", "text": "We", "start_ms": 0, "end_ms": 500, "speaker_id": "jean-pierre-001"},
            {"word_id": "w2", "text": "running", "start_ms": 500, "end_ms": 1000, "speaker_id": "jean-pierre-001"},
        ]
        selections = [
            {"selection_id": "sel-1", "start_word_id": "w1", "end_word_id": "w2", "function": "hook"},
        ]
        coordinator.compile_word_boundary_edl(
            aggregate_id=agg.aggregate_id,
            words=words,
            selections=selections,
            workspace_id=ws_id,
            actor_id="composer-001",
        )

        # VideoEditProgramService enforces PRIMARY_A_ROLL_SPINE at compilation time
        tracks_bad = [
            {
                "track_id": "track_b_roll",
                "role": "B_ROLL_OVERLAY",
                "elements": [
                    {
                        "element_id": "el_1",
                        "kind": "SOURCE_SEGMENT",
                        "edl_entry_id": "edl-001",
                        "source_span": {"start_ms": 0, "end_ms": 1000},
                        "timeline_start_ms": 0,
                        "timeline_end_ms": 1000,
                    }
                ],
            }
        ]

        with pytest.raises(Exception):
            coordinator.compile_video_edit_program(
                aggregate_id=agg.aggregate_id,
                canvas={"width": 360, "height": 640},
                timebase={"fps_numerator": 30, "fps_denominator": 1},
                tracks=tracks_bad,
                wrong_reading_locks=WRONG_READING_LOCKS,
                workspace_id=ws_id,
                actor_id="composer-001",
            )


# ----------------------------------------------------------------------------
# Test 3: Unapproved Release Blocked Before QA
# ----------------------------------------------------------------------------

def test_unapproved_release_blocked_before_qa(
    coordinator: VideoEditProductionCoordinator,
    test_tenant_context: TenantContext,
    authentic_source_video: Path,
    tmp_path: Path,
):
    ws_id = str(test_tenant_context.workspace_id)
    agg_id = f"agg-premature-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-pre-001", "scenes": JEAN_PIERRE_SEGMENTS}
        agg = coordinator.admit_semantic_material(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
            aggregate_id=agg_id,
        )

        # Attempting release before rendering/QA must fail
        with pytest.raises(Exception):
            coordinator.authorize_video_release(
                aggregate_id=agg.aggregate_id,
                operator_id=test_tenant_context.actor_id,
                rationale="Premature release",
                workspace_id=ws_id,
            )
