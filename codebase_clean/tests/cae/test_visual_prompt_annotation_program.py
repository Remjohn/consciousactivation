"""
Phase 4 Mandate M41 Acceptance Test Suite:
Visual Prompt + Asset Annotation Program Runtime.

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M41_visual_prompt_asset_annotation_runtime.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
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
    get_canonical_visual_prompt_state_machine,
)
from ca_runtime.visual_prompt_annotation_program import (
    AssetAnnotationItem,
    AssetRightsUnverifiedError,
    EvidenceHashMismatchError,
    LaneAuthorityViolationError,
    SourceLineageMissingError,
    SyntheticProductionBlockedError,
    VisualAssetDemandContract,
    VisualPackageReceipt,
    VisualPackageSnapshot,
    VisualPromptAnnotationCoordinator,
    VisualPromptProgramError,
    VisualPromptSpec,
    VisualRequirement,
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
    },
    {
        "scene_index": 2,
        "scene_role": "TENSION_ESCALATION",
        "segment_id": "seg-jp-002",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "text_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode("utf-8")).hexdigest(),
        "start_time_ms": 4800,
        "end_time_ms": 10500,
    },
    {
        "scene_index": 3,
        "scene_role": "PIVOT_MECHANISM",
        "segment_id": "seg-jp-003",
        "spoken_text": "That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.",
        "text_sha256": hashlib.sha256("That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.".encode("utf-8")).hexdigest(),
        "start_time_ms": 10500,
        "end_time_ms": 16200,
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
def tenant_ctx(test_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(test_workspace_id),
        actor_id="usr_lead_commander",
        role="MEMBER",
    )


@pytest.fixture
def foreign_tenant_ctx(foreign_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(foreign_workspace_id),
        actor_id="usr_foreign_agent",
        role="MEMBER",
    )


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def coordinator(runtime: UniversalProgramStateRuntime) -> VisualPromptAnnotationCoordinator:
    return VisualPromptAnnotationCoordinator(runtime=runtime)


@pytest.fixture
def authentic_semantic_program(test_workspace_id: str) -> dict:
    return {
        "program_id": "PRG-JP-5012-001",
        "candidate_id": "CAN-JP-001",
        "workspace_id": test_workspace_id,
        "title": "Industrial Noise Filtering at Scale",
        "semantic_intent": "Demonstrate the shift from alarm fatigue to verified edge intelligence.",
        "story_arc": "The Witness",
        "scenes": JEAN_PIERRE_SCENES,
        "wrong_reading_locks": WRONG_READING_LOCKS,
        "is_synthetic": False,
    }


# ============================================================================
# Test Cases
# ============================================================================

def test_program_package_discovery_and_manifest():
    """1. Verify declarative program package discovery and preflight registration."""
    registry = ProgramRegistry(discovery_roots=[Path("programs")])
    discovered = registry.discover()
    discovered_ids = [p.program_id for p in discovered]
    assert "visual_prompt_annotation_program" in discovered_ids

    pkg = registry.get_program("visual_prompt_annotation_program")
    assert pkg is not None
    assert pkg.manifest.id == "visual_prompt_annotation_program"
    assert pkg.manifest.version == "1.0.0"
    assert pkg.manifest.lanes == ["COMMANDER", "HUNTER", "ANALYST", "COMPOSER"]
    assert len(pkg.manifest.skills) == 3


def test_state_machine_grammar_and_transitions():
    """2. Verify canonical state machine grammar and transitions."""
    sm = get_canonical_visual_prompt_state_machine()
    assert sm.program_id == "visual_prompt_annotation_program"
    assert sm.machine_id == "VISUAL_PROMPT_ANNOTATION_STATE_MACHINE_V1"
    assert sm.initial_state == "INITIAL"

    # Verify transitions exist
    assert "admit_semantic_program" in sm.transitions
    assert "extract_visual_requirements" in sm.transitions
    assert "annotate_asset_packages" in sm.transitions
    assert "compile_visual_demands" in sm.transitions
    assert "approve_visual_package" in sm.transitions
    assert "repair_visual_package" in sm.repair_transitions


def test_full_visual_prompt_annotation_lifecycle_e2e(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """3. End-to-end promotion and compilation: SemanticProgram -> Requirements -> Assets -> Demands -> Receipt."""
    with tenant_scope(tenant_ctx):
        # Step 1: Admit program (COMMANDER)
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )
        assert agg1.current_state == "PROGRAM_ADMITTED"
        assert agg1.metadata["scene_count"] == 3

        # Step 2: Extract visual requirements (HUNTER)
        agg2 = coordinator.extract_visual_requirements(
            aggregate=agg1,
            hunter_id="agent:visual_requirement_hunter",
            lane=AuthorityLane.HUNTER,
        )
        assert agg2.current_state == "REQUIREMENTS_EXTRACTED"
        reqs = agg2.metadata["requirements"]
        assert len(reqs) == 3
        assert reqs[0]["scene_role"] == "HOOK_PROBLEM"
        assert reqs[0]["somatic_effect"] == "tension_escalation"

        # Step 3: Annotate asset packages (ANALYST)
        agg3 = coordinator.annotate_asset_packages(
            aggregate=agg2,
            analyst_id="agent:asset_annotation_analyst",
            lane=AuthorityLane.ANALYST,
        )
        assert agg3.current_state == "ASSETS_ANNOTATED"
        annts = agg3.metadata["annotations"]
        assert len(annts) == 3
        assert annts[0]["rights_status"] == "CLEARED_COMMERCIAL"
        assert annts[0]["is_verified"] is True

        # Step 4: Compile visual demands (COMPOSER)
        agg4 = coordinator.compile_visual_demands(
            aggregate=agg3,
            composer_id="agent:visual_demand_composer",
            lane=AuthorityLane.COMPOSER,
        )
        assert agg4.current_state == "DEMANDS_COMPILED"
        prompts = agg4.metadata["prompts"]
        demands = agg4.metadata["demands"]
        assert len(prompts) == 3
        assert len(demands) == 3

        # Step 5: Approve visual package (COMMANDER)
        agg5, receipt = coordinator.approve_visual_package(
            aggregate=agg4,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )
        assert agg5.current_state == "PACKAGE_COMMITTED"
        assert receipt.production_authorized is True
        assert len(receipt.evidence_sha256_list) == 3
        assert len(receipt.demand_ids) == 3
        assert len(receipt.receipt_sha256) == 64


def test_unbroken_dag_lineage_and_quote_hash_verification(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """4. Lineage Integrity: Reject tampered spoken text checksums fail-closed."""
    with tenant_scope(tenant_ctx):
        tampered_program = dict(authentic_semantic_program)
        tampered_scenes = [dict(s) for s in authentic_semantic_program["scenes"]]
        tampered_scenes[0]["spoken_text"] = "Tampered transcript text that does not match original turn hash."
        tampered_program["scenes"] = tampered_scenes

        with pytest.raises(EvidenceHashMismatchError) as exc_info:
            coordinator.admit_semantic_program(
                workspace_id=test_workspace_id,
                program_id=tampered_program["program_id"],
                semantic_program_payload=tampered_program,
                operator_id="usr_lead_commander",
                lane=AuthorityLane.COMMANDER,
            )
        assert "Spoken text SHA256 mismatch" in str(exc_info.value)


def test_four_lane_authority_separation_strict_enforcement(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """5. Strict 4-lane authority separation checks."""
    with tenant_scope(tenant_ctx):
        # Hunter cannot admit programs
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.admit_semantic_program(
                workspace_id=test_workspace_id,
                program_id=authentic_semantic_program["program_id"],
                semantic_program_payload=authentic_semantic_program,
                operator_id="usr_lead_commander",
                lane=AuthorityLane.HUNTER,
            )

        # Successfully admit program
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )

        # Commander cannot extract requirements
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.extract_visual_requirements(
                aggregate=agg1,
                lane=AuthorityLane.COMMANDER,
            )

        # Hunter extracts requirements
        agg2 = coordinator.extract_visual_requirements(
            aggregate=agg1,
            lane=AuthorityLane.HUNTER,
        )

        # Composer cannot annotate assets
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.annotate_asset_packages(
                aggregate=agg2,
                lane=AuthorityLane.COMPOSER,
            )

        # Analyst annotates assets
        agg3 = coordinator.annotate_asset_packages(
            aggregate=agg2,
            lane=AuthorityLane.ANALYST,
        )

        # Analyst cannot compile demands
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.compile_visual_demands(
                aggregate=agg3,
                lane=AuthorityLane.ANALYST,
            )


def test_anti_synthetic_fail_closed_blocking(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """6. Anti-Synthetic Defense: Block synthetic or mock programs from production."""
    with tenant_scope(tenant_ctx):
        synthetic_program = dict(authentic_semantic_program)
        synthetic_program["is_synthetic"] = True

        with pytest.raises(SyntheticProductionBlockedError) as exc_info:
            coordinator.admit_semantic_program(
                workspace_id=test_workspace_id,
                program_id=synthetic_program["program_id"],
                semantic_program_payload=synthetic_program,
                operator_id="usr_lead_commander",
                lane=AuthorityLane.COMMANDER,
            )
        assert "Synthetic or mock semantic programs are blocked" in str(exc_info.value)


def test_wrong_reading_locks_negative_prompt_inheritance(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """7. Wrong-Reading Locks: Ensure locks are inherited in negative prompts and demand contracts."""
    with tenant_scope(tenant_ctx):
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )
        agg2 = coordinator.extract_visual_requirements(aggregate=agg1, lane=AuthorityLane.HUNTER)
        agg3 = coordinator.annotate_asset_packages(aggregate=agg2, lane=AuthorityLane.ANALYST)
        agg4 = coordinator.compile_visual_demands(aggregate=agg3, lane=AuthorityLane.COMPOSER)

        prompts = agg4.metadata["prompts"]
        demands = agg4.metadata["demands"]

        for p in prompts:
            for lock in WRONG_READING_LOCKS:
                assert f"DO NOT: {lock}" in p["negative_prompt"]

        for d in demands:
            assert d["wrong_reading_locks"] == WRONG_READING_LOCKS


def test_somatic_and_narrative_function_validation(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """8. Somatic & Narrative Function: Verify accurate extraction of viewer state and somatic effects."""
    with tenant_scope(tenant_ctx):
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )
        agg2 = coordinator.extract_visual_requirements(aggregate=agg1, lane=AuthorityLane.HUNTER)

        reqs = agg2.metadata["requirements"]
        # Scene 1: HOOK_PROBLEM -> tension_escalation
        assert reqs[0]["somatic_effect"] == "tension_escalation"
        assert reqs[0]["activative_function"] == "orient_attention"

        # Scene 3: PIVOT_MECHANISM -> cognitive_resolution
        assert reqs[2]["somatic_effect"] == "cognitive_resolution"
        assert reqs[2]["activative_function"] == "evidence_anchoring"


def test_asset_rights_clearance_and_hash_integrity(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
):
    """9. Asset Rights & Hash Integrity: Reject unverified rights or malformed SHA256 hashes."""
    with tenant_scope(tenant_ctx):
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )
        agg2 = coordinator.extract_visual_requirements(aggregate=agg1, lane=AuthorityLane.HUNTER)

        # Invalid rights status
        bad_rights_inserts = [
            {
                "asset_id": "AST-UNLICENSED-001",
                "scene_index": 1,
                "source_sha256": "a" * 64,
                "rights_status": "UNLICENSED_WEB_SCRAPE",
            }
        ]
        with pytest.raises(AssetRightsUnverifiedError):
            coordinator.annotate_asset_packages(
                aggregate=agg2,
                asset_inserts=bad_rights_inserts,
                lane=AuthorityLane.ANALYST,
            )

        # Malformed SHA256 checksum
        bad_hash_inserts = [
            {
                "asset_id": "AST-CORRUPT-001",
                "scene_index": 1,
                "source_sha256": "invalid_short_hash",
                "rights_status": "CLEARED_COMMERCIAL",
            }
        ]
        with pytest.raises(EvidenceHashMismatchError):
            coordinator.annotate_asset_packages(
                aggregate=agg2,
                asset_inserts=bad_hash_inserts,
                lane=AuthorityLane.ANALYST,
            )


def test_multi_tenant_workspace_isolation_denial(
    coordinator: VisualPromptAnnotationCoordinator,
    test_workspace_id: str,
    foreign_workspace_id: str,
    authentic_semantic_program: dict,
    tenant_ctx: TenantContext,
    foreign_tenant_ctx: TenantContext,
):
    """10. Workspace Tenancy: Deny cross-tenant operations."""
    with tenant_scope(tenant_ctx):
        agg1 = coordinator.admit_semantic_program(
            workspace_id=test_workspace_id,
            program_id=authentic_semantic_program["program_id"],
            semantic_program_payload=authentic_semantic_program,
            operator_id="usr_lead_commander",
            lane=AuthorityLane.COMMANDER,
        )

    # Attempt operation under foreign workspace tenant scope
    with tenant_scope(foreign_tenant_ctx):
        with pytest.raises(Exception):
            coordinator.extract_visual_requirements(
                aggregate=agg1,
                lane=AuthorityLane.HUNTER,
            )
