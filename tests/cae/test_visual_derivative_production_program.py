"""
Phase 4 Mandate M42 Acceptance Test Suite:
Visual Derivative Production Program (Carousel, SuperVisual, Animation).

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M42_carousel_supervisual_animation_production_programs.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
"""

from __future__ import annotations

import hashlib
import json
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
    get_canonical_visual_derivative_state_machine,
)
from ca_runtime.visual_derivative_production_program import (
    DerivativeKind,
    DerivativeReleaseReceipt,
    DerivativeRenderArtifact,
    DerivativeSourceSpan,
    DualAxisQAReceipt,
    EvidenceQuoteMismatchError,
    LaneAuthorityViolationError,
    RenderQAFailureError,
    SemanticQAFailureError,
    SourceLineageMissingError,
    SyntheticDerivativeBlockedError,
    UnapprovedDerivativeReleaseError,
    VisualDerivativeError,
    VisualDerivativeProductionCoordinator,
    WorkspaceScopeViolationError,
    WrongReadingLockMissingError,
)
from ca_runtime.tenancy import TenantContext, tenant_scope


# ----------------------------------------------------------------------------
# Authentic Jean Pierre (03_50-12) Fixture Data
# ----------------------------------------------------------------------------

JEAN_PIERRE_SCENES = [
    {
        "scene_index": 1,
        "scene_role": "HOOK_PROBLEM",
        "segment_id": "seg-jp-001",
        "spoken_text": "We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.",
        "text_sha256": hashlib.sha256("We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.".encode("utf-8")).hexdigest(),
        "start_time_ms": 0,
        "end_time_ms": 4800,
        "speaker_id": "jean-pierre-001",
    },
    {
        "scene_index": 2,
        "scene_role": "TENSION_ESCALATION",
        "segment_id": "seg-jp-002",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "text_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode("utf-8")).hexdigest(),
        "start_time_ms": 4800,
        "end_time_ms": 10500,
        "speaker_id": "jean-pierre-001",
    },
    {
        "scene_index": 3,
        "scene_role": "PIVOT_MECHANISM",
        "segment_id": "seg-jp-003",
        "spoken_text": "That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.",
        "text_sha256": hashlib.sha256("That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.".encode("utf-8")).hexdigest(),
        "start_time_ms": 10500,
        "end_time_ms": 16200,
        "speaker_id": "jean-pierre-001",
    },
]

WRONG_READING_LOCKS = sorted([
    "Do not portray operators as negligent or lazy.",
    "Do not depict the factory as dark or dystopian.",
    "Do not suggest AI completely replaces human operators.",
])


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
def foreign_tenant_context(foreign_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(foreign_workspace_id),
        actor_id="op-foreign-002",
        role="MEMBER",
    )


@pytest.fixture
def program_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def coordinator(program_runtime: UniversalProgramStateRuntime) -> VisualDerivativeProductionCoordinator:
    return VisualDerivativeProductionCoordinator(runtime=program_runtime)


# ----------------------------------------------------------------------------
# Test 1: Program Package Discovery & Manifest Integrity
# ----------------------------------------------------------------------------

def test_program_package_discovery_and_manifest(test_workspace_id: str):
    programs_dir = Path(__file__).resolve().parents[2] / "programs"
    registry = ProgramRegistry(discovery_roots=[programs_dir])
    discovered = registry.discover()
    discovered_ids = [p.program_id for p in discovered]
    assert "visual_derivative_production_program" in discovered_ids

    pkg = registry.get_program("visual_derivative_production_program", "1.0.0")
    assert pkg is not None
    assert pkg.manifest.id == "visual_derivative_production_program"
    assert pkg.manifest.version == "1.0.0"
    assert set(pkg.manifest.lanes) == {"COMMANDER", "HUNTER", "ANALYST", "COMPOSER"}
    assert len(pkg.manifest.skills) == 3

    skill_names = {s.name for s in pkg.manifest.skills}
    assert "derivative_source_extractor" in skill_names
    assert "derivative_qa_evaluator" in skill_names
    assert "derivative_composition_compiler" in skill_names

    preflight = registry.preflight(
        "visual_derivative_production_program",
        test_workspace_id,
        context_refs=["workspace_active", "program_admitted", "evidence_verified"],
    )
    assert preflight.eligible is True


# ----------------------------------------------------------------------------
# Test 2: Canonical State Machine Grammar & Transitions
# ----------------------------------------------------------------------------

def test_state_machine_grammar_and_transitions():
    sm = get_canonical_visual_derivative_state_machine()
    assert sm.machine_id == "VISUAL_DERIVATIVE_PRODUCTION_STATE_MACHINE_V1"
    assert sm.program_id == "visual_derivative_production_program"
    assert sm.initial_state == "INITIAL"

    expected_transitions = {
        "admit_semantic_program": ("INITIAL", "DERIVATIVE_ADMITTED", AuthorityLane.COMMANDER),
        "extract_derivative_sources": ("DERIVATIVE_ADMITTED", "SOURCES_EXTRACTED", AuthorityLane.HUNTER),
        "compile_derivative_compositions": ("SOURCES_EXTRACTED", "COMPOSITIONS_COMPILED", AuthorityLane.COMPOSER),
        "realize_derivative_renders": ("COMPOSITIONS_COMPILED", "RENDERS_REALIZED", AuthorityLane.COMPOSER),
        "evaluate_dual_axis_qa": ("RENDERS_REALIZED", "QA_EVALUATED", AuthorityLane.ANALYST),
        "authorize_derivative_release": ("QA_EVALUATED", "RELEASE_AUTHORIZED", AuthorityLane.COMMANDER),
    }

    for t_name, (from_s, to_s, lane) in expected_transitions.items():
        assert t_name in sm.transitions
        contract = sm.transitions[t_name]
        assert contract.from_state == from_s
        assert contract.to_state == to_s
        assert contract.required_lane == lane


# ----------------------------------------------------------------------------
# Test 3: Full Carousel Derivative Lifecycle E2E
# ----------------------------------------------------------------------------

def test_full_carousel_derivative_lifecycle_e2e(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
    tmp_path: Path,
):
    ws_id = test_tenant_context.workspace_id
    agg_id = f"agg-carousel-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {
            "program_id": "sem-jp-001",
            "narrative_arc": "The Witness",
            "scenes": JEAN_PIERRE_SCENES,
        }

        # 1. Admit (COMMANDER)
        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
        )
        assert agg.current_state == "DERIVATIVE_ADMITTED"
        agg_id = agg.aggregate_id

        # 2. Extract Sources (HUNTER)
        agg = coordinator.extract_derivative_sources(
            aggregate_id=agg_id,
            evidence_segments=JEAN_PIERRE_SCENES,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )
        assert agg.current_state == "SOURCES_EXTRACTED"
        assert len(agg.state_data["source_spans"]) == 3

        # 3. Compile Compositions (COMPOSER)
        canvas = {"width_px": 800, "height_px": 1000, "background_rgb": [15, 25, 45]}
        pages = [
            {
                "page_id": "slide-1",
                "sequence_role": "HOOK",
                "viewer_state_goal": "RECOGNITION",
                "negative_space_regions": [{"x": 600000, "y": 50000, "width": 300000, "height": 200000}],
                "elements": [
                    {
                        "element_id": "t-1",
                        "element_type": "TEXT",
                        "semantic_role": "CLAIM",
                        "syntax_role": "PRIMARY_CLAIM",
                        "bbox": {"x": 50000, "y": 100000, "width": 800000, "height": 300000},
                        "why": "Hook the problem",
                        "z_index": 1,
                        "text": "30,000 Units Per Day",
                        "font_size_px": 40,
                        "foreground_rgb": [255, 255, 255],
                        "background_rgb": [30, 50, 90],
                        "overlap_allowed": False,
                        "source_refs": [{"object_id": "seg-jp-001", "version": "1.0.0", "sha256": "0" * 64}],
                        "protected_properties": ["source_fidelity"],
                    }
                ],
            },
            {
                "page_id": "slide-2",
                "sequence_role": "RESOLUTION",
                "viewer_state_goal": "RESOLUTION",
                "negative_space_regions": [{"x": 600000, "y": 50000, "width": 300000, "height": 200000}],
                "elements": [
                    {
                        "element_id": "t-2",
                        "element_type": "TEXT",
                        "semantic_role": "RESOLUTION",
                        "syntax_role": "PRIMARY_CLAIM",
                        "bbox": {"x": 50000, "y": 100000, "width": 800000, "height": 300000},
                        "why": "Provide pivot resolution",
                        "z_index": 1,
                        "text": "Edge Computer Vision",
                        "font_size_px": 40,
                        "foreground_rgb": [255, 255, 255],
                        "background_rgb": [30, 50, 90],
                        "overlap_allowed": False,
                        "source_refs": [{"object_id": "seg-jp-003", "version": "1.0.0", "sha256": "0" * 64}],
                        "protected_properties": ["source_fidelity"],
                    }
                ],
            },
        ]

        agg = coordinator.compile_derivative_compositions(
            aggregate_id=agg_id,
            derivative_kind=DerivativeKind.CAROUSEL,
            canvas=canvas,
            pages=pages,
            wrong_reading_locks=WRONG_READING_LOCKS,
            profile_id="carousel-profile-01",
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "COMPOSITIONS_COMPILED"

        # 4. Realize Renders (COMPOSER)
        render_out = tmp_path / "carousel_out"
        agg = coordinator.realize_derivative_renders(
            aggregate_id=agg_id,
            output_dir=render_out,
            logical_prefix="jp_carousel",
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "RENDERS_REALIZED"
        assert len(agg.state_data["render_artifacts"]) == 1
        pdf_path = Path(agg.state_data["render_artifacts"][0]["output_path"])
        assert pdf_path.is_file()
        assert pdf_path.stat().st_size > 0

        # 5. Dual-Axis QA Evaluation (ANALYST)
        agg = coordinator.evaluate_dual_axis_qa(
            aggregate_id=agg_id,
            workspace_id=ws_id,
            actor_id="analyst-001",
        )
        assert agg.current_state == "QA_EVALUATED"
        qa_rcpt = agg.state_data["dual_axis_qa_receipt"]
        assert qa_rcpt["overall_result"] == "PASS"
        assert qa_rcpt["semantic_qa_passed"] is True
        assert qa_rcpt["render_qa_passed"] is True

        # 6. Authorize Release (COMMANDER)
        agg = coordinator.authorize_derivative_release(
            aggregate_id=agg_id,
            operator_id=test_tenant_context.actor_id,
            rationale="Authentic Jean Pierre evidence validated with full dual-axis QA pass",
            workspace_id=ws_id,
        )
        assert agg.current_state == "RELEASE_AUTHORIZED"
        rel_rcpt = agg.state_data["derivative_release_receipt"]
        assert rel_rcpt["derivative_kind"] == "CAROUSEL"
        assert len(rel_rcpt["render_artifact_refs"]) == 1


# ----------------------------------------------------------------------------
# Test 4: Full SuperVisual Derivative Lifecycle E2E
# ----------------------------------------------------------------------------

def test_full_supervisual_derivative_lifecycle_e2e(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
    tmp_path: Path,
):
    ws_id = test_tenant_context.workspace_id
    agg_id = f"agg-supervis-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {
            "program_id": "sem-jp-002",
            "narrative_arc": "The Witness",
            "scenes": JEAN_PIERRE_SCENES,
        }

        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
        )
        agg_id = agg.aggregate_id
        coordinator.extract_derivative_sources(
            aggregate_id=agg_id,
            evidence_segments=JEAN_PIERRE_SCENES,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )

        canvas = {"width_px": 600, "height_px": 900, "background_rgb": [20, 20, 30]}
        pages = [
            {
                "page_id": "sv-main",
                "sequence_role": "HERO_STATEMENT",
                "viewer_state_goal": "AWARENESS",
                "negative_space_regions": [{"x": 500000, "y": 50000, "width": 400000, "height": 300000}],
                "elements": [
                    {
                        "element_id": "t-hero",
                        "element_type": "TEXT",
                        "semantic_role": "PRIMARY_AXIS",
                        "syntax_role": "PRIMARY_CLAIM",
                        "bbox": {"x": 50000, "y": 100000, "width": 800000, "height": 300000},
                        "why": "Hero visual anchor",
                        "z_index": 1,
                        "text": "OPERATOR SANITY FIRST",
                        "font_size_px": 36,
                        "foreground_rgb": [255, 255, 255],
                        "background_rgb": [10, 40, 80],
                        "overlap_allowed": False,
                        "source_refs": [{"object_id": "seg-jp-002", "version": "1.0.0", "sha256": "0" * 64}],
                        "protected_properties": ["source_fidelity"],
                    }
                ],
            }
        ]

        coordinator.compile_derivative_compositions(
            aggregate_id=agg_id,
            derivative_kind=DerivativeKind.SUPERVISUAL,
            canvas=canvas,
            pages=pages,
            wrong_reading_locks=WRONG_READING_LOCKS,
            profile_id="sv-profile-01",
            workspace_id=ws_id,
            actor_id="composer-001",
        )

        render_out = tmp_path / "supervis_out"
        agg = coordinator.realize_derivative_renders(
            aggregate_id=agg_id,
            output_dir=render_out,
            logical_prefix="jp_supervisual",
            workspace_id=ws_id,
            actor_id="composer-001",
        )
        assert agg.current_state == "RENDERS_REALIZED"
        png_path = Path(agg.state_data["render_artifacts"][0]["output_path"])
        assert png_path.is_file()
        assert png_path.stat().st_size > 0

        coordinator.evaluate_dual_axis_qa(
            aggregate_id=agg_id,
            workspace_id=ws_id,
            actor_id="analyst-001",
        )

        agg = coordinator.authorize_derivative_release(
            aggregate_id=agg_id,
            operator_id=test_tenant_context.actor_id,
            rationale="SuperVisual verified and operator ratified",
            workspace_id=ws_id,
        )
        assert agg.current_state == "RELEASE_AUTHORIZED"
        assert agg.state_data["derivative_release_receipt"]["derivative_kind"] == "SUPERVISUAL"


# ----------------------------------------------------------------------------
# Test 5: Full Animation Derivative Lifecycle E2E
# ----------------------------------------------------------------------------

def test_full_animation_derivative_lifecycle_e2e(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
    tmp_path: Path,
):
    ws_id = test_tenant_context.workspace_id
    agg_id = f"agg-animation-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {
            "program_id": "sem-jp-003",
            "narrative_arc": "The Witness",
            "scenes": JEAN_PIERRE_SCENES,
        }

        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
        )
        agg_id = agg.aggregate_id
        coordinator.extract_derivative_sources(
            aggregate_id=agg_id,
            evidence_segments=JEAN_PIERRE_SCENES,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )

        canvas = {"width_px": 400, "height_px": 400, "background_rgb": [10, 20, 30]}
        pages = [
            {
                "page_id": "ani-scene-1",
                "sequence_role": "MOTION_HOOK",
                "viewer_state_goal": "ENGAGEMENT",
                "negative_space_regions": [{"x": 600000, "y": 50000, "width": 300000, "height": 200000}],
                "elements": [
                    {
                        "element_id": "m-subject",
                        "element_type": "TEXT",
                        "semantic_role": "MOTION_SUBJECT",
                        "syntax_role": "MOTION_SUBJECT",
                        "bbox": {"x": 50000, "y": 100000, "width": 500000, "height": 200000},
                        "why": "Moving conveyor subject",
                        "z_index": 1,
                        "text": "DEFECT ALERT FILTERED",
                        "font_size_px": 24,
                        "foreground_rgb": [255, 255, 255],
                        "background_rgb": [40, 80, 160],
                        "overlap_allowed": False,
                        "source_refs": [{"object_id": "seg-jp-003", "version": "1.0.0", "sha256": "0" * 64}],
                        "protected_properties": ["source_fidelity"],
                    }
                ],
            }
        ]

        coordinator.compile_derivative_compositions(
            aggregate_id=agg_id,
            derivative_kind=DerivativeKind.ANIMATION_SCENE_PACKAGE,
            canvas=canvas,
            pages=pages,
            wrong_reading_locks=WRONG_READING_LOCKS,
            profile_id="ani-profile-01",
            workspace_id=ws_id,
            actor_id="composer-001",
        )

        render_out = tmp_path / "animation_out"
        agg = coordinator.realize_derivative_renders(
            aggregate_id=agg_id,
            output_dir=render_out,
            logical_prefix="jp_animation",
            workspace_id=ws_id,
            actor_id="composer-001",
            frame_count=6,
            fps=6,
        )
        assert agg.current_state == "RENDERS_REALIZED"
        mp4_path = Path(agg.state_data["render_artifacts"][0]["output_path"])
        assert mp4_path.is_file()
        assert mp4_path.stat().st_size > 0
        assert agg.state_data["render_artifacts"][0]["format02_activated"] is False

        coordinator.evaluate_dual_axis_qa(
            aggregate_id=agg_id,
            workspace_id=ws_id,
            actor_id="analyst-001",
        )

        agg = coordinator.authorize_derivative_release(
            aggregate_id=agg_id,
            operator_id=test_tenant_context.actor_id,
            rationale="Animation derivative verified and operator signed",
            workspace_id=ws_id,
        )
        assert agg.current_state == "RELEASE_AUTHORIZED"
        assert agg.state_data["derivative_release_receipt"]["derivative_kind"] == "ANIMATION_SCENE_PACKAGE"


# ----------------------------------------------------------------------------
# Test 6: Unbroken Cryptographic DAG Lineage & Verbatim Hash Verification
# ----------------------------------------------------------------------------

def test_unbroken_dag_lineage_and_quote_hash_verification(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
):
    ws_id = test_tenant_context.workspace_id

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-004", "scenes": JEAN_PIERRE_SCENES}
        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
        )
        agg_id = agg.aggregate_id

        # Tamper with the quote text hash
        tampered_scenes = [
            {
                "segment_id": "seg-jp-001",
                "spoken_text": "We were running thirty thousand units a day...",
                "text_sha256": "bad_hash_00000000000000000000000000000000000000000000000000000000",
                "start_time_ms": 0,
                "end_time_ms": 4800,
            }
        ]

        with pytest.raises(EvidenceQuoteMismatchError):
            coordinator.extract_derivative_sources(
                aggregate_id=agg_id,
                evidence_segments=tampered_scenes,
                workspace_id=ws_id,
                actor_id="hunter-001",
            )


# ----------------------------------------------------------------------------
# Test 7: Strict 4-Lane Authority Separation
# ----------------------------------------------------------------------------

def test_four_lane_authority_separation_strict_enforcement(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
):
    ws_id = test_tenant_context.workspace_id

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-005", "scenes": JEAN_PIERRE_SCENES}

        # 1. Admit requires COMMANDER (HUNTER must fail)
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.admit_semantic_program(
                semantic_program=sem_prog,
                workspace_id=ws_id,
                operator_id=test_tenant_context.actor_id,
                lane=AuthorityLane.HUNTER,
            )

        # Valid admit
        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
            lane=AuthorityLane.COMMANDER,
        )
        agg_id = agg.aggregate_id

        # 2. Extract sources requires HUNTER (COMPOSER must fail)
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.extract_derivative_sources(
                aggregate_id=agg_id,
                evidence_segments=JEAN_PIERRE_SCENES,
                workspace_id=ws_id,
                actor_id="composer-001",
                lane=AuthorityLane.COMPOSER,
            )


# ----------------------------------------------------------------------------
# Test 8: Fail-Closed Anti-Synthetic Derivative Blocking
# ----------------------------------------------------------------------------

def test_anti_synthetic_fail_closed_blocking(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
):
    ws_id = test_tenant_context.workspace_id

    with tenant_scope(test_tenant_context):
        synthetic_prog = {
            "program_id": "sem-synth-001",
            "is_synthetic": True,
            "scenes": [],
        }

        with pytest.raises(SyntheticDerivativeBlockedError):
            coordinator.admit_semantic_program(
                semantic_program=synthetic_prog,
                workspace_id=ws_id,
                operator_id=test_tenant_context.actor_id,
            )


# ----------------------------------------------------------------------------
# Test 9: Dual-Axis QA Independent Failure Modes
# ----------------------------------------------------------------------------

def test_dual_axis_qa_independent_failure_modes(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
    tmp_path: Path,
):
    ws_id = test_tenant_context.workspace_id

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-006", "scenes": JEAN_PIERRE_SCENES}
        agg = coordinator.admit_semantic_program(
            semantic_program=sem_prog,
            workspace_id=ws_id,
            operator_id=test_tenant_context.actor_id,
        )
        agg_id = agg.aggregate_id
        coordinator.extract_derivative_sources(
            aggregate_id=agg_id,
            evidence_segments=JEAN_PIERRE_SCENES,
            workspace_id=ws_id,
            actor_id="hunter-001",
        )

        canvas = {"width_px": 400, "height_px": 600, "background_rgb": [10, 20, 30]}
        # Missing source_refs on text element -> Semantic QA failure
        pages = [
            {
                "page_id": "p1",
                "sequence_role": "CLAIM",
                "viewer_state_goal": "RECOGNITION",
                "negative_space_regions": [{"x": 600000, "y": 50000, "width": 300000, "height": 200000}],
                "elements": [
                    {
                        "element_id": "t-ungrounded",
                        "element_type": "TEXT",
                        "semantic_role": "UNANCHORED",
                        "syntax_role": "PRIMARY_CLAIM",
                        "bbox": {"x": 50000, "y": 100000, "width": 800000, "height": 300000},
                        "why": "Ungrounded text",
                        "z_index": 1,
                        "text": "UNANCHORED TEXT",
                        "font_size_px": 30,
                        "foreground_rgb": [255, 255, 255],
                        "background_rgb": [30, 40, 50],
                        "overlap_allowed": False,
                        "source_refs": [],
                        "protected_properties": ["source_fidelity"],
                    }
                ],
            }
        ]

        coordinator.compile_derivative_compositions(
            aggregate_id=agg_id,
            derivative_kind=DerivativeKind.SUPERVISUAL,
            canvas=canvas,
            pages=pages,
            wrong_reading_locks=WRONG_READING_LOCKS,
            profile_id="sv-test",
            workspace_id=ws_id,
            actor_id="composer-001",
        )

        render_out = tmp_path / "qa_fail_out"
        coordinator.realize_derivative_renders(
            aggregate_id=agg_id,
            output_dir=render_out,
            logical_prefix="qa_fail_sv",
            workspace_id=ws_id,
            actor_id="composer-001",
        )

        # Semantic QA must fail because element is ungrounded in source_refs
        with pytest.raises(SemanticQAFailureError):
            coordinator.evaluate_dual_axis_qa(
                aggregate_id=agg_id,
                workspace_id=ws_id,
                actor_id="analyst-001",
            )


# ----------------------------------------------------------------------------
# Test 10: Multi-Tenant Workspace Isolation Denial
# ----------------------------------------------------------------------------

def test_multi_tenant_workspace_isolation_denial(
    coordinator: VisualDerivativeProductionCoordinator,
    test_tenant_context: TenantContext,
    foreign_workspace_id: str,
):
    agg_id = f"agg-cross-tenant-{uuid4().hex[:8]}"

    with tenant_scope(test_tenant_context):
        sem_prog = {"program_id": "sem-jp-007", "scenes": JEAN_PIERRE_SCENES}

        # Attempting operation with foreign workspace ID must raise WorkspaceScopeViolationError
        with pytest.raises(WorkspaceScopeViolationError):
            coordinator.admit_semantic_program(
                semantic_program=sem_prog,
                workspace_id=foreign_workspace_id,
                operator_id=test_tenant_context.actor_id,
            )
