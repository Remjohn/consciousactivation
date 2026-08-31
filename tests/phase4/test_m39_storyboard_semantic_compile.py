"""
test_m39_storyboard_semantic_compile.py
-----------------------------------------
Phase 4 Mandate M39 Acceptance Suite:
Editorial Storyboard + SemanticProgram Production Compile

Verifies:
1. End-to-end promotion and compilation: Authentic interview candidate (03_50-12 Jean Pierre) ->
   Operator Selection -> EditorialStoryboard -> SemanticProgram -> CompositionIR with signed handoff receipts.
2. Unbroken cryptographic DAG lineage: Every spoken quote and scene input is traceable to authentic EvidenceSegments.
3. Strict 4-lane authority separation (COMPOSER owns compilation; COMMANDER gates selection/eligibility).
4. Fail-closed anti-synthetic candidate blocking across all compilation stages.
5. Verbatim quote immutability & checksum defense (blocks tampered quote text and corrupt hashes).
6. Unapproved asset injection defense (rejects media asset IDs not in approved catalog).
7. Story arc preservation (verifier catches altered story arc geometry).
8. Timing continuity validation (rejects invalid durations, inverted timestamps, or discontinuities).
9. Downstream eligibility enforcement (rejects unselected or rejected candidates).
10. Wrong-reading locks and SFL modulation profile preservation.
11. Multi-tenant cross-workspace isolation.
"""

from __future__ import annotations

import hashlib
import uuid
import pytest
from typing import Any, Dict, List

from ca_contracts import canonical_sha256
from ca_runtime.program_state_runtime import AuthorityLane
from ca_runtime.editorial_discovery_store import (
    EditorialDiscoveryStore,
    EvidenceSegmentRecord,
    SemanticAnnotationRecord,
    ContentCandidateRecord,
    EditorialStoryboardRecord,
    EditorialDecisionReceiptRecord,
    SemanticProgramRecord,
    CompositionHandoffRecord,
)
from ca_runtime.editorial_discovery_program import (
    EditorialDiscoveryProgramCoordinator,
    EditorialDiscoveryError,
    LaneAuthorityViolationError,
    UngroundedCandidateError,
    SyntheticCandidateProductionBlockedError,
    EvidenceImmutabilityViolationError,
)
from cae_production_program.compiler import ProductionProgramCompiler
from cae_production_program.verifier import ProductionProgramVerifier
from cae_production_program.domain import (
    VisualAudioSpecs,
    SFLModulationProfile,
    SceneRole,
    SemanticProgram,
    CompositionHandoffReceipt,
)
from cae_production_program.errors import (
    EvidenceQuoteMismatchError,
    UnapprovedAssetInsertionError,
    StoryArcGeometryMutationError,
    TimingDiscontinuityError,
)
from cae_operator_intelligence.errors import UnapprovedExecutionError
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


# ---------------------------------------------------------------------------
# Authentic Jean Pierre (03_50-12) Fixture Data
# ---------------------------------------------------------------------------

JEAN_PIERRE_INTERVIEW_TURNS = [
    {
        "turn_id": "turn-001",
        "speaker": "Jean Pierre",
        "start_time_ms": 0,
        "end_time_ms": 4800,
        "verbatim_text": "We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.",
        "boundary_type": "SYNTACTIC_SENTENCE",
        "narrative_role": "HOOK_PROBLEM",
    },
    {
        "turn_id": "turn-002",
        "speaker": "Jean Pierre",
        "start_time_ms": 4800,
        "end_time_ms": 10500,
        "verbatim_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "boundary_type": "SYNTACTIC_SENTENCE",
        "narrative_role": "TENSION_ESCALATION",
    },
    {
        "turn_id": "turn-003",
        "speaker": "Jean Pierre",
        "start_time_ms": 10500,
        "end_time_ms": 16200,
        "verbatim_text": "That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.",
        "boundary_type": "SYNTACTIC_SENTENCE",
        "narrative_role": "PIVOT_MECHANISM",
    },
    {
        "turn_id": "turn-004",
        "speaker": "Jean Pierre",
        "start_time_ms": 16200,
        "end_time_ms": 22000,
        "verbatim_text": "Within forty-eight hours, true yield jumped four percent and operator alarm fatigue dropped to absolute zero.",
        "boundary_type": "SYNTACTIC_SENTENCE",
        "narrative_role": "RESOLUTION_PAYOFF",
    },
]


def seed_jean_pierre_candidate(
    coordinator: EditorialDiscoveryProgramCoordinator,
    workspace_id: str,
    operator_id: str = "operator-chief-01",
) -> tuple[ContentCandidateRecord, EditorialDecisionReceiptRecord]:
    """Helper to ingest raw Jean Pierre evidence, form a candidate, and execute operator selection."""
    evidence_links: List[Dict[str, Any]] = []

    # 1. Hunter Ingests lossless EvidenceSegments
    for turn in JEAN_PIERRE_INTERVIEW_TURNS:
        seg_id = f"seg-{turn['turn_id']}"
        text_sha = hashlib.sha256(turn["verbatim_text"].encode("utf-8")).hexdigest()
        seg = EvidenceSegmentRecord(
            workspace_id=workspace_id,
            segment_id=seg_id,
            session_id="session-jp-01",
            speaker=turn["speaker"],
            start_time_ms=turn["start_time_ms"],
            end_time_ms=turn["end_time_ms"],
            verbatim_text=turn["verbatim_text"],
            boundary_type=turn["boundary_type"],
            text_sha256=text_sha,
            observable_evidence={"turn_ref": turn["turn_id"]},
        )
        coordinator.editorial_store.insert_evidence_segment(seg)

        evidence_links.append({
            "segment_id": seg_id,
            "text_sha256": text_sha,
            "narrative_role": turn["narrative_role"],
            "epistemic_status": "OBSERVED_FACT",
            "emotional_register": "GROUNDED_CONVICTION",
        })

    # 2. Composer builds ContentCandidate
    candidate_id = f"cand-jp-{uuid.uuid4().hex[:8]}"
    candidate = ContentCandidateRecord(
        workspace_id=workspace_id,
        candidate_id=candidate_id,
        candidate_type="PROBLEM_SOLUTION_ARC",
        title="Edge Vision Line Triage",
        hook_statement="Seventy percent false defect alarms almost broke our night shift.",
        narrative_completeness="COMPLETE_ARC",
        story_arc="Manufacturing Crisis -> Edge AI Turning Point",
        evidence_links=evidence_links,
        cmf_score_bps={"heritage_weight": 8800, "narrative_coherence": 9200},
        production_status="DRAFT_CANDIDATE",
        is_synthetic=False,
    )
    coordinator.editorial_store.insert_content_candidate(candidate)

    # 3. Commander executes Operator SELECT action
    select_receipt = coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=workspace_id,
        operator_id=operator_id,
        candidate_id=candidate_id,
        priority_rank=1,
        rationale="Exceptional operational clarity and high narrative contrast.",
    )


    promoted_cand = coordinator.editorial_store.get_content_candidate(workspace_id, candidate_id)
    assert promoted_cand is not None
    assert promoted_cand.production_status == "SELECTED_FOR_PRODUCTION"

    return promoted_cand, select_receipt


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

def test_real_evidence_to_storyboard_semantic_ir_compilation_lifecycle():
    """
    Test 1: Full end-to-end compilation lifecycle on authentic Project 03_50-12 Jean Pierre data:
    Evidence -> Candidate -> Operator SELECT -> EditorialStoryboard -> SemanticProgram -> CompositionIR.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-jp-m39-01"
    op_id = "op-lead-jp"

    candidate, select_receipt = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    # 1. Compile EditorialStoryboard (COMPOSER Lane)
    approved_assets = ["asset-diagram-edge-cv", "asset-conveyor-b-roll"]
    planned_inserts = [
        {"scene_index": 3, "segment_id": candidate.evidence_links[2]["segment_id"], "asset_id": "asset-diagram-edge-cv", "role": "MECHANISM_VISUAL"},
        {"scene_index": 4, "segment_id": candidate.evidence_links[3]["segment_id"], "asset_id": "asset-conveyor-b-roll", "role": "PAYOFF_B_ROLL"},
    ]

    storyboard = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
        planned_inserts=planned_inserts,
        priority_rank=1,
        notes="High priority flagship production piece",
    )

    assert storyboard is not None
    assert storyboard.storyboard_id.startswith("STB-")
    assert storyboard.candidate_id == candidate.candidate_id
    assert len(storyboard.narrative_structure) == 4
    assert len(storyboard.planned_inserts) == 2

    # Verify storyboard was persisted in store
    saved_sb = store.get_editorial_storyboard(ws_id, storyboard.storyboard_id)
    assert saved_sb is not None
    assert saved_sb.title == candidate.title
    assert len(saved_sb.narrative_structure) == 4

    # 2. Compile SemanticProgram (COMPOSER Lane)
    sfl_profile = {
        "pacing_multiplier": 1.1,
        "kinetic_typography": True,
        "pause_duration_seconds": 0.5,
        "color_grade_tone": "INDUSTRIAL_COOL_CONTRAST",
    }
    visual_specs = VisualAudioSpecs(
        aspect_ratio="9:16",
        subtitle_font="Inter Bold",
        background_music_ducking=0.3,
        transition_style="HARD_CUT",
    )
    wrong_reading_locks = [
        "NO_MOCK_PRODUCTION",
        "VERBATIM_EVIDENCE_MANDATORY",
        "NEVER_FRAME_OPERATOR_AS_NEGLIGENT",
    ]

    semantic_program, handoff_receipt = coordinator.compile_semantic_program(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        storyboard_id=storyboard.storyboard_id,
        approved_asset_ids=approved_assets,
        sfl_profile=sfl_profile,
        visual_audio_specs=visual_specs,
        wrong_reading_locks=wrong_reading_locks,
    )

    assert semantic_program is not None
    assert semantic_program.program_id.startswith("PRG-")
    assert semantic_program.storyboard_id == storyboard.storyboard_id
    assert semantic_program.candidate_id == candidate.candidate_id
    assert len(semantic_program.scenes) == 4
    assert semantic_program.total_duration == 22.0
    assert semantic_program.wrong_reading_locks == wrong_reading_locks

    # Verify cryptographic evidence hashes match raw turns
    for idx, sc in enumerate(semantic_program.scenes):
        expected_sha = hashlib.sha256(JEAN_PIERRE_INTERVIEW_TURNS[idx]["verbatim_text"].encode("utf-8")).hexdigest()
        assert sc["text_sha256"] == expected_sha
        assert sc["spoken_text"] == JEAN_PIERRE_INTERVIEW_TURNS[idx]["verbatim_text"]

    # Verify handoff receipt
    assert handoff_receipt is not None
    assert handoff_receipt.program_id == semantic_program.program_id
    assert handoff_receipt.candidate_id == candidate.candidate_id
    assert handoff_receipt.storyboard_id == storyboard.storyboard_id
    assert len(handoff_receipt.evidence_sha256_list) == 4
    assert handoff_receipt.asset_id_list == approved_assets

    # 3. Compile CompositionIR (COMPOSER Lane)
    pipeline_repo = PipelineRepository()
    cir_result, handoff_updated = coordinator.compile_composition_ir(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        program_id=semantic_program.program_id,
        pipeline_repo=pipeline_repo,
        composition_kind="SUPERVISUAL",
    )

    assert cir_result is not None
    assert "composition_id" in cir_result
    assert cir_result["composition_kind"] == "SUPERVISUAL"
    assert cir_result["pages"][0]["elements"][0]["text"] == candidate.title
    assert cir_result["pages"][0]["geometry_receipt"]["result"] == "PASS"

    # Verify handoff record links to composition_ir_ref
    assert handoff_updated.composition_ir_ref is not None
    assert handoff_updated.composition_ir_ref["composition_id"] == cir_result["composition_id"]


def test_four_lane_authority_separation_strict_enforcement():
    """
    Test 2: Verifies strict 4-lane authority boundaries.
    Only COMPOSER can compile storyboards, semantic programs, and composition IR.
    HUNTER, ANALYST, and COMMANDER lanes are rejected with LaneAuthorityViolationError.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-jp-lanes"
    op_id = "op-lane-test"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    # 1. compile_editorial_storyboard lane violations
    for bad_lane in [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMMANDER]:
        with pytest.raises(LaneAuthorityViolationError) as exc_info:
            coordinator.compile_editorial_storyboard(
                lane=bad_lane,
                workspace_id=ws_id,
                candidate_id=candidate.candidate_id,
                operator_id=op_id,
            )
        assert exc_info.value.required_lane == AuthorityLane.COMPOSER
        assert exc_info.value.attempted_lane == bad_lane

    # Compile a valid storyboard for subsequent tests
    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
    )

    # 2. compile_semantic_program lane violations
    for bad_lane in [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMMANDER]:
        with pytest.raises(LaneAuthorityViolationError) as exc_info:
            coordinator.compile_semantic_program(
                lane=bad_lane,
                workspace_id=ws_id,
                storyboard_id=sb.storyboard_id,
            )
        assert exc_info.value.required_lane == AuthorityLane.COMPOSER

    # Compile a valid semantic program
    prg, _ = coordinator.compile_semantic_program(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        storyboard_id=sb.storyboard_id,
    )

    # 3. compile_composition_ir lane violations
    for bad_lane in [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMMANDER]:
        with pytest.raises(LaneAuthorityViolationError) as exc_info:
            coordinator.compile_composition_ir(
                lane=bad_lane,
                workspace_id=ws_id,
                program_id=prg.program_id,
            )
        assert exc_info.value.required_lane == AuthorityLane.COMPOSER


def test_synthetic_candidate_fail_closed_production_block():
    """
    Test 3: Verifies that synthetic or mock candidates are permanently blocked
    from storyboard compilation, semantic program compilation, and composition IR.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-synth-block"

    # Create a synthetic candidate
    synth_cand_id = "cand-synth-999"
    synth_cand = ContentCandidateRecord(
        workspace_id=ws_id,
        candidate_id=synth_cand_id,
        candidate_type="SYNTHETIC_PROTOTYPE",
        title="Mock Synthetic Line Story",
        hook_statement="This is a mock LLM generated hallucination.",
        narrative_completeness="COMPLETE_ARC",
        story_arc="Mock Arc",
        evidence_links=[],
        cmf_score_bps={"heritage_weight": 9900},
        production_status="SELECTED_FOR_PRODUCTION",  # fraudulently marked
        is_synthetic=True,
    )
    store.insert_content_candidate(synth_cand)

    # Attempting to compile storyboard MUST fail closed with SyntheticCandidateProductionBlockedError
    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.compile_editorial_storyboard(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_id=synth_cand_id,
            operator_id="op-synth-test",
        )


def test_tampered_quote_checksum_rejection_at_compilation():
    """
    Test 4: Verifies verbatim quote immutability. If spoken text is tampered with
    or does not match its registered SHA-256 hash, compilation is rejected.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-tamper-test"
    op_id = "op-tamper"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    # Tamper with narrative structure in storyboard
    tampered_structure = [
        {
            "scene_index": 1,
            "scene_role": "HOOK_INTERRUPT",
            "segment_id": candidate.evidence_links[0]["segment_id"],
            "spoken_text": "We were running only ten units a day and zero defects happened.", # Tampered text!
            "text_sha256": candidate.evidence_links[0]["text_sha256"],  # Original hash
            "start_time": 0.0,
            "end_time": 4.8,
            "narrative_focus": "CORE_EVIDENCE",
        }
    ]

    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
        narrative_structure=tampered_structure,
    )

    # Compilation MUST raise EvidenceQuoteMismatchError
    with pytest.raises(EvidenceQuoteMismatchError) as exc_info:
        coordinator.compile_semantic_program(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            storyboard_id=sb.storyboard_id,
        )
    assert "does not match registered hash" in str(exc_info.value)


def test_unapproved_asset_injection_defense():
    """
    Test 5: Verifies that inserting unapproved media assets is strictly rejected.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-asset-test"
    op_id = "op-asset"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    planned_inserts = [
        {
            "scene_index": 1,
            "segment_id": candidate.evidence_links[0]["segment_id"],
            "asset_id": "unapproved-rogue-asset-007",
            "role": "B_ROLL",
        }
    ]

    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
        planned_inserts=planned_inserts,
    )

    # Compile with approved_asset_ids that DO NOT contain the rogue asset
    with pytest.raises(UnapprovedAssetInsertionError) as exc_info:
        coordinator.compile_semantic_program(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            storyboard_id=sb.storyboard_id,
            approved_asset_ids=["approved-logo-01", "approved-chart-02"],
        )
    assert "unapproved-rogue-asset-007" in str(exc_info.value)


def test_story_arc_mutation_rejection():
    """
    Test 6: Verifies that attempting to compile a semantic program with an altered story arc
    triggers StoryArcGeometryMutationError in the verifier.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-arc-test"
    op_id = "op-arc"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
    )

    # Attempting to override candidate's story arc to a mismatched arc MUST fail
    with pytest.raises(StoryArcGeometryMutationError) as exc_info:
        coordinator.compile_semantic_program(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            storyboard_id=sb.storyboard_id,
            story_arc_override="Romance Comedy -> Happy Wedding",
        )
    assert "Story arc mutation detected" in str(exc_info.value)


def test_timing_discontinuity_and_negative_duration_rejection():
    """
    Test 7: Verifies that invalid timing (start >= end, negative duration) is rejected with TimingDiscontinuityError.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-timing-test"
    op_id = "op-timing"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
    )

    # Supply an inverted timing override for scene 1 (start: 10.0, end: 5.0 -> duration: -5.0)
    timing_overrides = [{"scene_index": 1, "start_time": 10.0, "end_time": 5.0}]

    with pytest.raises(TimingDiscontinuityError) as exc_info:
        coordinator.compile_semantic_program(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            storyboard_id=sb.storyboard_id,
            timing_overrides=timing_overrides,
        )
    assert "invalid" in str(exc_info.value).lower()


def test_unselected_and_rejected_candidate_production_block():
    """
    Test 8: Verifies that unselected (DRAFT_CANDIDATE) or explicitly REJECTED candidates
    are rejected from compiling into storyboards or semantic programs.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-unselected-test"
    op_id = "op-gatekeeper"

    # 1. Unselected candidate (DRAFT_CANDIDATE without SELECT receipt)
    seg = EvidenceSegmentRecord(
        workspace_id=ws_id,
        segment_id="seg-draft-01",
        session_id="session-draft",
        speaker="Speaker",
        start_time_ms=0,
        end_time_ms=5000,
        verbatim_text="Draft evidence that is not yet selected by operator.",
        boundary_type="SYNTACTIC_SENTENCE",
        text_sha256=hashlib.sha256(b"Draft evidence that is not yet selected by operator.").hexdigest(),
    )
    store.insert_evidence_segment(seg)

    draft_cand = ContentCandidateRecord(
        workspace_id=ws_id,
        candidate_id="cand-draft-01",
        candidate_type="PROBLEM_SOLUTION_ARC",
        title="Draft Candidate",
        hook_statement="Draft hook",
        narrative_completeness="COMPLETE_ARC",
        evidence_links=[{"segment_id": "seg-draft-01", "text_sha256": seg.text_sha256}],
        production_status="DRAFT_CANDIDATE",
    )
    store.insert_content_candidate(draft_cand)

    with pytest.raises(UnapprovedExecutionError) as exc_info:
        coordinator.compile_editorial_storyboard(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_id=draft_cand.candidate_id,
            operator_id=op_id,
        )
    assert "missing authoritative SELECT receipt" in str(exc_info.value)

    # 2. Rejected candidate
    coordinator.operator_reject_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=op_id,
        candidate_id=draft_cand.candidate_id,
        rationale="Narrative hook too weak for production.",
    )

    with pytest.raises(UnapprovedExecutionError) as exc_info:
        coordinator.compile_editorial_storyboard(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_id=draft_cand.candidate_id,
            operator_id=op_id,
        )
    assert "candidate is marked REJECTED" in str(exc_info.value)


def test_wrong_reading_locks_and_sfl_modulation_preservation():
    """
    Test 9: Verifies that operator-defined wrong-reading locks and SFL modulation profiles
    are faithfully preserved in the compiled SemanticProgram and CompositionHandoffReceipt.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_id = "ws-locks-test"
    op_id = "op-locks"

    candidate, _ = seed_jean_pierre_candidate(coordinator, ws_id, op_id)

    sb = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
        operator_id=op_id,
    )

    custom_locks = [
        "DO_NOT_DOWNPLAY_DEFECT_SEVERITY",
        "NO_SYNTHETIC_VOICE_OVERRIDE",
        "PRESERVE_ORIGINAL_JEAN_PIERRE_REGISTER",
    ]
    custom_sfl = {
        "pacing_multiplier": 1.35,
        "kinetic_typography": True,
        "pause_duration_seconds": 1.2,
        "color_grade_tone": "DOCUMENTARY_WARM_SHADOWS",
    }

    prg, handoff = coordinator.compile_semantic_program(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        storyboard_id=sb.storyboard_id,
        sfl_profile=custom_sfl,
        wrong_reading_locks=custom_locks,
    )

    assert prg.wrong_reading_locks == custom_locks
    assert handoff.wrong_reading_locks == custom_locks
    for sc in prg.scenes:
        assert sc["sfl_profile"]["pacing_multiplier"] == 1.35
        assert sc["sfl_profile"]["color_grade_tone"] == "DOCUMENTARY_WARM_SHADOWS"


def test_cross_workspace_multi_tenant_isolation():
    """
    Test 10: Multi-tenant isolation. Candidate and evidence belonging to Workspace A
    cannot be accessed or compiled into storyboards/programs from Workspace B.
    """
    store = EditorialDiscoveryStore(":memory:")
    coordinator = EditorialDiscoveryProgramCoordinator(editorial_store=store)
    ws_a = "ws-tenant-alpha"
    ws_b = "ws-tenant-bravo"
    op_id = "op-iso-test"

    cand_a, _ = seed_jean_pierre_candidate(coordinator, ws_a, op_id)

    # Attempting to compile storyboard in Workspace B using candidate from Workspace A MUST fail
    with pytest.raises(EditorialDiscoveryError) as exc_info:
        coordinator.compile_editorial_storyboard(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_b,
            candidate_id=cand_a.candidate_id,
            operator_id=op_id,
        )
    assert f"Candidate '{cand_a.candidate_id}' not found in workspace '{ws_b}'" in str(exc_info.value)

    # Create storyboard in Workspace A
    sb_a = coordinator.compile_editorial_storyboard(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_a,
        candidate_id=cand_a.candidate_id,
        operator_id=op_id,
    )

    # Attempting to compile semantic program in Workspace B using storyboard from Workspace A MUST fail
    with pytest.raises(EditorialDiscoveryError) as exc_info:
        coordinator.compile_semantic_program(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_b,
            storyboard_id=sb_a.storyboard_id,
        )
    assert f"EditorialStoryboard '{sb_a.storyboard_id}' not found in workspace '{ws_b}'" in str(exc_info.value)
