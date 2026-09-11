"""
Phase 4 Mandate M44 Acceptance Test Suite:
VAE Delegation + Visual Asset Runtime.

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M44_vae_delegation_visual_asset_runtime.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
- CURRENT.md F15
"""

from __future__ import annotations

import copy
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
    get_canonical_vae_delegation_state_machine,
)
from ca_runtime.vae_delegation_program import (
    BoundedRepairExceededError,
    ConsumptionAuthorityViolationError,
    DelegatedDemandRecord,
    DelegationReceipt,
    DualAxisQAViolationError,
    EvidenceHashMismatchError,
    LaneAuthorityViolationError,
    SemanticQARecord,
    SourceLineageMissingError,
    SyntheticProductionBlockedError,
    VAEDelegationCoordinator,
    VAEDelegationProgramError,
    VAEExecutionArtifactRecord,
    VAEProductionPlanRecord,
    VAETechnicalEvaluationRecord,
    WorkspaceScopeViolationError,
    WrongReadingLockMissingError,
)
from ca_runtime.tenancy import TenantContext, tenant_scope
from cmf_pipeline.delegation import VisualDelegationService
from cmf_vae.application import VAEApplication


# ----------------------------------------------------------------------------
# Authentic Jean Pierre (03_50-12) Fixture Data & Delegation Demand Helpers
# ----------------------------------------------------------------------------

JEAN_PIERRE_EVIDENCE = [
    {
        "segment_id": "seg-jp-001",
        "spoken_text": "We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.",
        "text_sha256": hashlib.sha256("We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.".encode("utf-8")).hexdigest(),
    },
    {
        "segment_id": "seg-jp-002",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "text_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode("utf-8")).hexdigest(),
    },
]

WRONG_READING_LOCKS = [
    "Do not portray operators as negligent or lazy.",
    "Do not depict the factory as dark or dystopian.",
]


def ref(object_id: str, seed: str) -> dict[str, str]:
    return {"object_id": object_id, "version": "1.0.0", "sha256": canonical_sha256({"seed": seed})}


def get_delegation_root() -> Path:
    return Path(__file__).resolve().parents[2] / "services/delegation/delegation-contracts/1.1.0-rc.4"


def build_authentic_jean_pierre_demand(
    *,
    is_synthetic: bool = False,
    tampered_evidence: bool = False,
    omit_locks: bool = False,
    omit_lineage: bool = False,
) -> dict:
    svc = VisualDelegationService(get_delegation_root())
    package = svc.compile_demand(
        source_package_ref=ref("source-package:jp", "source"),
        reaction_receipt_refs=[ref("reaction-receipt:jp-01", "reaction")],
        expression_moment_refs=[ref("expression-moment:jp-01", "moment")],
        semantic_program_ref=ref("semantic-program:jp-03_50-12", "semantic"),
        final_script_ref=ref("final-script:jp", "script"),
        primitive_coalition_ref=ref("primitive:jp", "primitive"),
        archetype_coalition_ref=ref("archetype:jp", "archetype"),
        activation_transfer_contract_ref=ref("transfer:jp", "transfer"),
        content_harness_ref=ref("harness:jp", "harness"),
        category_profile_ref=ref("category:static", "category"),
        format_profile_ref=ref("format:supervisual", "format"),
        width_px=1080,
        height_px=1920,
        wrong_reading_locks=WRONG_READING_LOCKS,
    )
    demand = copy.deepcopy(package["demand"])
    if omit_locks:
        demand["wrong_reading_locks"] = []
    if omit_lineage:
        demand["activative_semantic_lineage"]["reaction_receipt_refs"] = []
        demand["activative_semantic_lineage"]["expression_moment_refs"] = []

    # Attach evidence segments metadata
    evidence_segments = copy.deepcopy(JEAN_PIERRE_EVIDENCE)
    if tampered_evidence:
        evidence_segments[0]["spoken_text"] = "Tampered quote text"

    demand["metadata"] = {
        "scene_index": 1,
        "is_synthetic": is_synthetic,
        "evidence_segments": evidence_segments,
    }
    return demand


@pytest.fixture
def test_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def foreign_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def vae_app(tmp_path: Path) -> VAEApplication:
    app = VAEApplication(
        database_path=tmp_path / "vae_test.db",
        storage_root=tmp_path / "vae_store",
        delegation_root=get_delegation_root(),
    )
    app.initialize()
    return app


# ----------------------------------------------------------------------------
# 1. Program Package Discovery & Manifest Validation
# ----------------------------------------------------------------------------

def test_01_program_package_discovery_and_manifest():
    """Verifies that vae_delegation_program is discoverable in the ProgramRegistry."""
    registry = ProgramRegistry(discovery_roots=[Path("programs")])
    registry.discover()
    package = registry.get_program("vae_delegation_program")

    assert package is not None
    assert package.program_id == "vae_delegation_program"
    assert package.version == "1.0.0"
    assert package.manifest.status.value == "ACTIVE"
    assert package.manifest.state_machine == "VAE_DELEGATION_STATE_MACHINE_V1"
    assert package.manifest.harness == "VAE_DELEGATION_HARNESS_V1"

    lanes = set(package.manifest.lanes)
    assert lanes == {"COMMANDER", "HUNTER", "ANALYST", "COMPOSER"}

    skill_names = {s.name for s in package.manifest.skills}
    assert "demand_admission_verifier" in skill_names
    assert "visual_render_composer" in skill_names
    assert "visual_production_analyst" in skill_names

    operations = set(package.manifest.operations)
    assert "cae.vae_delegation.admit_demand@1.0.0" in operations
    assert "cae.vae_delegation.compile_plan@1.0.0" in operations
    assert "cae.vae_delegation.generate_asset@1.0.0" in operations
    assert "cae.vae_delegation.evaluate_asset@1.0.0" in operations
    assert "cae.vae_delegation.acknowledge_result@1.0.0" in operations
    assert "cae.vae_delegation.repair@1.0.0" in operations


# ----------------------------------------------------------------------------
# 2. Canonical State Machine Grammar & Registration
# ----------------------------------------------------------------------------

def test_02_state_machine_grammar_and_transitions():
    """Verifies state machine transitions and lane constraints."""
    sm = get_canonical_vae_delegation_state_machine()
    assert sm.machine_id == "VAE_DELEGATION_STATE_MACHINE_V1"
    assert sm.program_id == "vae_delegation_program"
    assert sm.initial_state == "INITIAL"

    runtime = UniversalProgramStateRuntime()
    registered_sm = runtime.get_state_machine("vae_delegation_program")
    assert registered_sm.machine_id == sm.machine_id

    # Verify transition contracts
    assert sm.transitions["admit_visual_demand"].required_lane == AuthorityLane.COMMANDER
    assert sm.transitions["compile_production_plan"].required_lane == AuthorityLane.HUNTER
    assert sm.transitions["generate_visual_asset"].required_lane == AuthorityLane.COMPOSER
    assert sm.transitions["evaluate_technical_quality"].required_lane == AuthorityLane.ANALYST
    assert sm.transitions["acknowledge_result"].required_lane == AuthorityLane.COMMANDER


# ----------------------------------------------------------------------------
# 3. Full End-to-End Receipt-Driven Lifecycle
# ----------------------------------------------------------------------------

def test_03_full_receipt_driven_delegation_lifecycle_e2e(test_workspace_id: str, vae_app: VAEApplication):
    """Executes full 5-phase lifecycle on authentic Jean Pierre demand and verifies signed receipt."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    # Step 1: Admit Demand (COMMANDER)
    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator:jp-commander",
        lane=AuthorityLane.COMMANDER,
    )
    assert agg.current_state == "DEMAND_ADMITTED"
    assert agg.state_data["demand"]["scene_index"] == 1
    assert agg.state_data["demand"]["demand_hash"] is not None

    # Step 2: Compile Production Plan (HUNTER)
    agg = coordinator.compile_production_plan(
        aggregate_id=agg.aggregate_id,
        producer_actor_id="agent:vae-hunter",
        evaluator_actor_id="agent:vae-analyst",
        lane=AuthorityLane.HUNTER,
    )
    assert agg.current_state == "PRODUCTION_PLAN_COMPILED"
    assert len(agg.state_data["production_plan"]["stage_bindings"]) == 4

    # Step 3: Generate Visual Asset (COMPOSER)
    agg = coordinator.generate_visual_asset(
        aggregate_id=agg.aggregate_id,
        worker_id="agent:vae-composer",
        lane=AuthorityLane.COMPOSER,
    )
    assert agg.current_state == "VISUAL_ASSET_GENERATED"
    assert agg.state_data["artifact"]["candidate_uri"].startswith("vae/")
    assert agg.state_data["artifact"]["width_px"] == 1080
    assert agg.state_data["artifact"]["height_px"] == 1920

    # Step 4: Evaluate Technical Quality & Dual-Axis QA (ANALYST)
    agg = coordinator.evaluate_technical_quality(
        aggregate_id=agg.aggregate_id,
        evaluator_actor_id="agent:vae-analyst",
        lane=AuthorityLane.ANALYST,
    )
    assert agg.current_state == "TECHNICAL_EVALUATED"
    assert agg.state_data["technical_evaluation"]["hard_gate_result"] == "PASS"
    assert "consumption_authorized" not in agg.state_data["asset_result"]

    # Step 5: Acknowledge Result & Emit Receipt (COMMANDER)
    agg, receipt = coordinator.acknowledge_result(
        aggregate_id=agg.aggregate_id,
        operator_id="operator:jp-commander",
        decision="ACCEPTED",
        consumption_authorized=True,
        lane=AuthorityLane.COMMANDER,
    )
    assert agg.current_state == "RESULT_ACKNOWLEDGED"
    assert receipt.consumption_authorized is True
    assert receipt.decision == "ACCEPTED"
    assert receipt.receipt_sha256 is not None
    assert agg.state_data["acknowledgement"]["consumption_authorized"] is True


# ----------------------------------------------------------------------------
# 4. Strict Four-Lane Authority Separation
# ----------------------------------------------------------------------------

def test_04_four_lane_authority_separation_strict_enforcement(test_workspace_id: str, vae_app: VAEApplication):
    """Verifies that operations invoked under incorrect authority lanes fail closed."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    # COMMANDER gate: admit_demand called by COMPOSER -> rejected
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.admit_demand(
            workspace_id=test_workspace_id,
            program_id="vae_delegation_program",
            demand_payload=demand,
            operator_id="actor",
            lane=AuthorityLane.COMPOSER,
        )

    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator",
        lane=AuthorityLane.COMMANDER,
    )

    # HUNTER gate: compile_production_plan called by ANALYST -> rejected
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.compile_production_plan(
            aggregate_id=agg.aggregate_id,
            producer_actor_id="producer",
            evaluator_actor_id="evaluator",
            lane=AuthorityLane.ANALYST,
        )

    agg = coordinator.compile_production_plan(
        aggregate_id=agg.aggregate_id,
        producer_actor_id="producer",
        evaluator_actor_id="evaluator",
        lane=AuthorityLane.HUNTER,
    )

    # COMPOSER gate: generate_visual_asset called by HUNTER -> rejected
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.generate_visual_asset(
            aggregate_id=agg.aggregate_id,
            worker_id="worker",
            lane=AuthorityLane.HUNTER,
        )

    agg = coordinator.generate_visual_asset(
        aggregate_id=agg.aggregate_id,
        worker_id="worker",
        lane=AuthorityLane.COMPOSER,
    )

    # ANALYST gate: evaluate_technical_quality called by COMMANDER -> rejected
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.evaluate_technical_quality(
            aggregate_id=agg.aggregate_id,
            evaluator_actor_id="evaluator",
            lane=AuthorityLane.COMMANDER,
        )

    agg = coordinator.evaluate_technical_quality(
        aggregate_id=agg.aggregate_id,
        evaluator_actor_id="evaluator",
        lane=AuthorityLane.ANALYST,
    )

    # COMMANDER gate: acknowledge_result called by COMPOSER -> rejected
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.acknowledge_result(
            aggregate_id=agg.aggregate_id,
            operator_id="operator",
            lane=AuthorityLane.COMPOSER,
        )


# ----------------------------------------------------------------------------
# 5. Consumption Authority Ownership Boundary
# ----------------------------------------------------------------------------

def test_05_consumption_authority_ownership_boundary(test_workspace_id: str, vae_app: VAEApplication):
    """Proves that VAE cannot grant consumption authority, and Pipeline acknowledgement owns it."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator",
        lane=AuthorityLane.COMMANDER,
    )
    agg = coordinator.compile_production_plan(
        aggregate_id=agg.aggregate_id,
        producer_actor_id="producer",
        evaluator_actor_id="evaluator",
        lane=AuthorityLane.HUNTER,
    )
    agg = coordinator.generate_visual_asset(
        aggregate_id=agg.aggregate_id,
        worker_id="worker",
        lane=AuthorityLane.COMPOSER,
    )
    agg = coordinator.evaluate_technical_quality(
        aggregate_id=agg.aggregate_id,
        evaluator_actor_id="evaluator",
        lane=AuthorityLane.ANALYST,
    )

    # Invariant: VAE result cannot contain consumption_authorized
    asset_result = agg.state_data["asset_result"]
    assert "consumption_authorized" not in asset_result

    # Boundary violation simulation: If VAE result were tampered to assert consumption authority, acknowledgement fails
    agg.state_data["asset_result"]["consumption_authorized"] = True
    with pytest.raises(ConsumptionAuthorityViolationError):
        coordinator.acknowledge_result(
            aggregate_id=agg.aggregate_id,
            operator_id="operator",
            lane=AuthorityLane.COMMANDER,
        )


# ----------------------------------------------------------------------------
# 6. Anti-Synthetic Fail-Closed Blocking
# ----------------------------------------------------------------------------

def test_06_anti_synthetic_fail_closed_blocking(test_workspace_id: str):
    """Verifies that synthetic or mock demands are rejected from production delegation."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime)

    synthetic_demand = build_authentic_jean_pierre_demand(is_synthetic=True)
    with pytest.raises(SyntheticProductionBlockedError):
        coordinator.admit_demand(
            workspace_id=test_workspace_id,
            program_id="vae_delegation_program",
            demand_payload=synthetic_demand,
            operator_id="operator",
            lane=AuthorityLane.COMMANDER,
        )


# ----------------------------------------------------------------------------
# 7. Evidence Quote Hash Integrity Verification
# ----------------------------------------------------------------------------

def test_07_evidence_hash_integrity_verification(test_workspace_id: str):
    """Verifies that tampered spoken quotes in evidence segments fail closed immediately."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime)

    tampered_demand = build_authentic_jean_pierre_demand(tampered_evidence=True)
    with pytest.raises(EvidenceHashMismatchError):
        coordinator.admit_demand(
            workspace_id=test_workspace_id,
            program_id="vae_delegation_program",
            demand_payload=tampered_demand,
            operator_id="operator",
            lane=AuthorityLane.COMMANDER,
        )


# ----------------------------------------------------------------------------
# 8. Wrong-Reading Locks & Lineage Mandatory Enforcement
# ----------------------------------------------------------------------------

def test_08_wrong_reading_locks_and_lineage_enforcement(test_workspace_id: str):
    """Verifies that demands without locks or upstream lineage are rejected."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime)

    # Missing wrong reading locks
    no_locks_demand = build_authentic_jean_pierre_demand(omit_locks=True)
    with pytest.raises(WrongReadingLockMissingError):
        coordinator.admit_demand(
            workspace_id=test_workspace_id,
            program_id="vae_delegation_program",
            demand_payload=no_locks_demand,
            operator_id="operator",
            lane=AuthorityLane.COMMANDER,
        )

    # Missing upstream reaction / expression lineage
    no_lineage_demand = build_authentic_jean_pierre_demand(omit_lineage=True)
    with pytest.raises(SourceLineageMissingError):
        coordinator.admit_demand(
            workspace_id=test_workspace_id,
            program_id="vae_delegation_program",
            demand_payload=no_lineage_demand,
            operator_id="operator",
            lane=AuthorityLane.COMMANDER,
        )


# ----------------------------------------------------------------------------
# 9. Dual-Axis QA: Semantic QA vs Render QA Separation
# ----------------------------------------------------------------------------

def test_09_dual_axis_qa_separation(test_workspace_id: str, vae_app: VAEApplication):
    """Proves that a technical/render pass cannot override a failed independent semantic evaluation."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator",
        lane=AuthorityLane.COMMANDER,
    )
    agg = coordinator.compile_production_plan(
        aggregate_id=agg.aggregate_id,
        producer_actor_id="producer",
        evaluator_actor_id="evaluator",
        lane=AuthorityLane.HUNTER,
    )
    agg = coordinator.generate_visual_asset(
        aggregate_id=agg.aggregate_id,
        worker_id="worker",
        lane=AuthorityLane.COMPOSER,
    )

    # Evaluate with Render PASS but Semantic QA FAIL (narrative mismatch)
    failed_semantic_qa = {
        "narrative_fit": "FAIL",
        "somatic_effect_preserved": False,
        "anti_centroid_respected": True,
        "findings": [{"code": "NARRATIVE_MISMATCH", "verdict": "FAIL", "note": "Asset diverges from somatic tone."}],
    }
    agg = coordinator.evaluate_technical_quality(
        aggregate_id=agg.aggregate_id,
        evaluator_actor_id="evaluator",
        force_render_fail=False,
        semantic_qa_result=failed_semantic_qa,
        lane=AuthorityLane.ANALYST,
    )

    # Acknowledging with consumption authorization fails closed because of Semantic QA failure
    with pytest.raises(DualAxisQAViolationError):
        coordinator.acknowledge_result(
            aggregate_id=agg.aggregate_id,
            operator_id="operator",
            decision="ACCEPTED",
            consumption_authorized=True,
            lane=AuthorityLane.COMMANDER,
        )


# ----------------------------------------------------------------------------
# 10. Multi-Tenant Workspace Isolation
# ----------------------------------------------------------------------------

def test_10_multi_tenant_workspace_isolation(test_workspace_id: str, foreign_workspace_id: str, vae_app: VAEApplication):
    """Ensures cross-workspace operations are denied with WorkspaceScopeViolationError."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    # Admit under test_workspace_id
    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator",
        lane=AuthorityLane.COMMANDER,
    )

    # In tenant scope of foreign workspace, attempting to access aggregate fails
    with tenant_scope(TenantContext(workspace_id=UUID(foreign_workspace_id), actor_id="operator:analyst")):
        with pytest.raises(WorkspaceScopeViolationError):
            coordinator.compile_production_plan(
                aggregate_id=agg.aggregate_id,
                producer_actor_id="producer",
                evaluator_actor_id="evaluator",
                lane=AuthorityLane.HUNTER,
            )


# ----------------------------------------------------------------------------
# 11. Governed Fault Recovery and Bounded Repair Loop
# ----------------------------------------------------------------------------

def test_11_governed_fault_recovery_and_bounded_repair(test_workspace_id: str, vae_app: VAEApplication):
    """Tests bounded repair transitions and enforcement of max repair limits."""
    runtime = UniversalProgramStateRuntime()
    coordinator = VAEDelegationCoordinator(runtime=runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    agg = coordinator.admit_demand(
        workspace_id=test_workspace_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator",
        lane=AuthorityLane.COMMANDER,
    )

    # Repair cycle 1
    agg = coordinator.repair_delegation(
        aggregate_id=agg.aggregate_id,
        operator_id="operator",
        repair_reason="Alpha matte edge roughness",
        lane=AuthorityLane.COMMANDER,
    )
    assert agg.current_state == "PRODUCTION_PLAN_COMPILED"
    assert agg.state_data["repair_attempts"] == 1

    # Repair cycle 2
    agg = coordinator.repair_delegation(
        aggregate_id=agg.aggregate_id,
        operator_id="operator",
        repair_reason="Lighting grade calibration",
        lane=AuthorityLane.COMMANDER,
    )
    assert agg.state_data["repair_attempts"] == 2

    # Repair cycle 3 (reaches max=3)
    agg = coordinator.repair_delegation(
        aggregate_id=agg.aggregate_id,
        operator_id="operator",
        repair_reason="Pose angle correction",
        lane=AuthorityLane.COMMANDER,
    )
    assert agg.state_data["repair_attempts"] == 3

    # Repair cycle 4: Exceeds budget -> BoundedRepairExceededError
    with pytest.raises(BoundedRepairExceededError):
        coordinator.repair_delegation(
            aggregate_id=agg.aggregate_id,
            operator_id="operator",
            repair_reason="Excessive iteration attempt",
            lane=AuthorityLane.COMMANDER,
        )
