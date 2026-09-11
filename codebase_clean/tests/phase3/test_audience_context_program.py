"""Audience Context + Cognitive Island State Program Verification Suite.

Governed by Phase 3 Mandate M26.
Validates:
- End-to-end 5-phase lifecycle (INITIAL -> AUDIENCE_INITIALIZED -> TENSIONS_HUNTED -> ISLANDS_MAPPED -> CONTEXT_PROJECTED -> AUDIENCE_ACTIVE).
- Invariant Protection of Cognitive Islands (Prohibits silent in-place rewriting).
- Explicit versioned supersession (version increment + parent hash link).
- Dynamic recompilation of derived expressions (projections retain lineage).
- Workspace isolation and anti-tenant-leak fail-closed gates.
- Strict Four-Lane Authority separation (HUNTER, ANALYST, COMPOSER, COMMANDER).
- Operator gate anti-self-approval enforcement.
- Recovery routing to REPAIRING state.
- Append-only CausalTraceLedger cryptographic chaining.
"""

from __future__ import annotations

import hashlib
import json
import pytest
from uuid import uuid4

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.audience_context_program import (
    AudienceContextProgramCoordinator,
    AudienceContextSnapshot,
    AudienceIntegrityError,
    AudienceLineageMissingError,
    AudienceProfile,
    AudienceProfileNotInitializedError,
    AudienceProgramError,
    AudienceStateProjection,
    AudienceWorkspaceScopeViolationError,
    CognitiveIsland,
    CognitiveIslandNotFoundError,
    ProtectedCognitiveIslandMutationError,
)
from ca_runtime.hook_runtime import (
    HookExtensionManager,
    OperatorGateReceipt,
    OperatorGateRuntimeEngine,
    SelfApprovalProhibitedError,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramTransitionBlockedError,
    ProgramTransitionResult,
    UniversalProgramStateRuntime,
    get_canonical_audience_context_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceEventType,
    CausalTraceLedger,
    StateLifecycleCoordinator,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
)


# ============================================================================
from pathlib import Path
from uuid import UUID, uuid4

# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def workspace_id() -> UUID:
    return uuid4()


@pytest.fixture
def audience_id() -> str:
    return f"aud_{uuid4().hex[:8]}"


@pytest.fixture
def tenant_ctx(workspace_id: UUID) -> TenantContext:
    return TenantContext(
        workspace_id=workspace_id,
        actor_id="usr_planner_001",
        role="MEMBER",
        is_operator=False,
    )


@pytest.fixture
def operator_ctx(workspace_id: UUID) -> TenantContext:
    return TenantContext(
        workspace_id=workspace_id,
        actor_id="usr_operator_001",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id=uuid4(),
    )


@pytest.fixture
def runtime_stack():
    store = InMemoryProgramStateStore()
    registry = ProgramRegistry(discovery_roots=[Path("programs")])
    registry.discover()
    runtime = UniversalProgramStateRuntime(store=store, program_registry=registry)
    trace_ledger = CausalTraceLedger()
    coordinator = StateLifecycleCoordinator(
        state_runtime=runtime,
        trace_ledger=trace_ledger,
    )
    operator_gate_engine = OperatorGateRuntimeEngine(trace_ledger=trace_ledger)
    audience_coordinator = AudienceContextProgramCoordinator(
        runtime=runtime,
        coordinator=coordinator,
        trace_ledger=trace_ledger,
        operator_gate_engine=operator_gate_engine,
    )
    return {
        "store": store,
        "registry": registry,
        "runtime": runtime,
        "trace_ledger": trace_ledger,
        "coordinator": coordinator,
        "operator_gate_engine": operator_gate_engine,
        "audience_coordinator": audience_coordinator,
    }


# ============================================================================
# 1. Program Package Discovery Test
# ============================================================================

def test_audience_context_program_discovery(runtime_stack):
    registry: ProgramRegistry = runtime_stack["registry"]
    package = registry.get_program("audience_context_program")
    assert package is not None
    assert package.program_id == "audience_context_program"
    assert package.manifest.id == "audience_context_program"
    assert package.manifest.version == "1.0.0"
    assert "COMMANDER" in package.manifest.lanes
    assert "HUNTER" in package.manifest.lanes
    assert "ANALYST" in package.manifest.lanes
    assert "COMPOSER" in package.manifest.lanes
    assert len(package.manifest.skills) == 3
    assert len(package.skills_inventory) == 3


# ============================================================================
# 2. End-to-End Lifecycle & Phase Execution
# ============================================================================

def test_audience_context_lifecycle_end_to_end(runtime_stack, workspace_id, audience_id, tenant_ctx, operator_ctx):
    coordinator: AudienceContextProgramCoordinator = runtime_stack["audience_coordinator"]
    trace_ledger: CausalTraceLedger = runtime_stack["trace_ledger"]

    # Phase 1: Initialize Audience Profile (COMMANDER)
    init_res = coordinator.initialize_audience(
        workspace_id=workspace_id,
        audience_id=audience_id,
        target_segment="Enterprise AI Executives & Risk Officers",
        core_demographics={"industry": "FinTech / Enterprise", "seniority": "C-Level / VP"},
        psychographic_baseline={"skepticism_level": "high", "primary_desire": "verifiable_safety"},
        context=tenant_ctx,
        actor_id="aud_commander_01",
    )
    assert init_res.aggregate.current_state == "AUDIENCE_INITIALIZED"
    agg_id = init_res.aggregate.aggregate_id

    # Phase 2: Hunt Tensions (HUNTER)
    tensions = [
        {
            "tension_id": "ten_001",
            "tension_type": "AUTONOMY_VS_CONTROL",
            "severity_bps": 8500,
            "description": "Desire for autonomous agent speed colliding with audit compliance fears.",
        },
        {
            "tension_id": "ten_002",
            "tension_type": "SPEED_VS_ACCURACY",
            "severity_bps": 7200,
            "description": "Frustration with slow manual reviews vs fear of generative hallucination.",
        },
    ]
    hunt_res = coordinator.hunt_tensions(
        aggregate_id=agg_id,
        tension_observations=tensions,
        context=tenant_ctx,
        actor_id="aud_tension_hunter_01",
    )
    assert hunt_res.aggregate.current_state == "TENSIONS_HUNTED"

    # Phase 3: Map Protected Cognitive Islands (ANALYST)
    evidence_hash_1 = hashlib.sha256(b"source_interview_transcript_001").hexdigest()
    evidence_hash_2 = hashlib.sha256(b"market_survey_report_2026").hexdigest()

    islands_data = [
        {
            "island_id": "isl_skepticism",
            "name": "Deterministic Automation Skepticism",
            "mental_model": "LLM systems are fundamentally stochastic and cannot be trusted for financial operations.",
            "resistance_patterns": ["Demands deterministic receipts", "Rejects black-box prompts"],
            "friction_points": ["Audit committee pushback", "Regulatory compliance ambiguity"],
            "source_evidence_hashes": [evidence_hash_1, evidence_hash_2],
            "version": 1,
        },
        {
            "island_id": "isl_ownership",
            "name": "Sovereign Infrastructure Protectionism",
            "mental_model": "Data and cognitive memory must remain in-tenant without third-party vendor lock-in.",
            "resistance_patterns": ["Refuses multi-tenant SaaS without strict RLS", "Demands self-custody of cryptographic keys"],
            "friction_points": ["Vendor security questionnaires", "GDPR article 28 concerns"],
            "source_evidence_hashes": [evidence_hash_1],
            "version": 1,
        },
    ]

    map_res = coordinator.map_cognitive_islands(
        aggregate_id=agg_id,
        islands_data=islands_data,
        context=tenant_ctx,
        actor_id="aud_island_mapper_01",
    )
    assert map_res.aggregate.current_state == "ISLANDS_MAPPED"

    # Phase 4: Project Current State (COMPOSER)
    coordinates = {
        "readiness_bps": 6500,
        "skepticism_bps": 8800,
        "resonance_bps": 7200,
    }
    progression = ("RESISTANT", "PROVOKED", "ENGAGED", "CONVINCED")
    proj_res = coordinator.project_current_state(
        aggregate_id=agg_id,
        activation_coordinates_bps=coordinates,
        viewer_state_sequence=progression,
        tension_summary="Audience presents acute deterministic audit demands with high willingness to adopt once cryptographic receipts are demonstrated.",
        context=tenant_ctx,
        actor_id="aud_state_composer_01",
    )
    assert proj_res.aggregate.current_state == "CONTEXT_PROJECTED"

    # Phase 5: Approve Audience Context via Operator Gate (COMMANDER & Operator)
    app_res = coordinator.approve_audience_context(
        aggregate_id=agg_id,
        operator_context=operator_ctx,
        approver_id="usr_operator_001",
        approval_decision="APPROVED",
        reason="Audience cognitive islands and projection verified against enterprise interview data.",
        requester_id="aud_commander_01",
    )
    assert app_res.aggregate.current_state == "AUDIENCE_ACTIVE"

    # Verify Snapshot
    snapshot: AudienceContextSnapshot = coordinator.get_snapshot(agg_id, tenant_ctx)
    assert snapshot.current_state == "AUDIENCE_ACTIVE"
    assert snapshot.audience_profile is not None
    assert snapshot.audience_profile.target_segment == "Enterprise AI Executives & Risk Officers"
    assert len(snapshot.cognitive_islands) == 2
    assert snapshot.current_projection is not None
    assert snapshot.current_projection.activation_coordinates_bps["skepticism_bps"] == 8800
    assert snapshot.last_receipt_id is not None

    # Verify Causal Trace Hash Chain Integrity
    traces = trace_ledger.get_traces_for_aggregate(agg_id)
    assert len(traces) >= 4
    prev_hash = None
    for tr in traces:
        if prev_hash is not None:
            assert tr.previous_trace_sha256 == prev_hash
        assert len(tr.trace_sha256) == 64
        assert len(tr.payload_hash) == 64
        prev_hash = tr.trace_sha256


# ============================================================================
# 3. Protected Cognitive Island Invariant Tests (Contrastive / False-Proof)
# ============================================================================

def test_protected_cognitive_island_mutation_prohibited(workspace_id, audience_id):
    evidence_hash = hashlib.sha256(b"evidence_01").hexdigest()
    computed_sha = CognitiveIsland.compute_content_hash(
        island_id="isl_test",
        workspace_id=workspace_id,
        audience_id=audience_id,
        name="Test Island",
        mental_model="Initial Model",
        resistance_patterns=["pattern 1"],
        friction_points=["friction 1"],
        source_evidence_hashes=[evidence_hash],
        version=1,
    )

    # Valid creation
    island = CognitiveIsland(
        island_id="isl_test",
        workspace_id=workspace_id,
        audience_id=audience_id,
        name="Test Island",
        mental_model="Initial Model",
        resistance_patterns=("pattern 1",),
        friction_points=("friction 1",),
        source_evidence_hashes=(evidence_hash,),
        content_sha256=computed_sha,
        version=1,
    )
    assert island.content_sha256 == computed_sha

    # Tampered content without updating content_sha256 raises ProtectedCognitiveIslandMutationError
    with pytest.raises(ProtectedCognitiveIslandMutationError) as exc_info:
        CognitiveIsland(
            island_id="isl_test",
            workspace_id=workspace_id,
            audience_id=audience_id,
            name="Tampered Island Name",
            mental_model="Silently rewritten model",
            resistance_patterns=("pattern 1",),
            friction_points=("friction 1",),
            source_evidence_hashes=(evidence_hash,),
            content_sha256=computed_sha,  # stale hash
            version=1,
        )
    assert exc_info.value.reason_code == "PROTECTED_COGNITIVE_ISLAND_MUTATION_PROHIBITED"


# ============================================================================
# 4. Explicit Versioned Supersession & Recompilation
# ============================================================================

def test_explicit_versioned_supersession_and_recompilation(runtime_stack, workspace_id, audience_id, tenant_ctx, operator_ctx):
    coordinator: AudienceContextProgramCoordinator = runtime_stack["audience_coordinator"]
    trace_ledger: CausalTraceLedger = runtime_stack["trace_ledger"]

    # 1. Initialize, hunt, and map
    init_res = coordinator.initialize_audience(
        workspace_id=workspace_id,
        audience_id=audience_id,
        target_segment="Enterprise AI Executives",
        context=tenant_ctx,
    )
    agg_id = init_res.aggregate.aggregate_id

    coordinator.hunt_tensions(
        aggregate_id=agg_id,
        tension_observations=[{"tension_id": "t1", "severity_bps": 5000}],
        context=tenant_ctx,
    )

    ev_hash = hashlib.sha256(b"source_evidence").hexdigest()
    coordinator.map_cognitive_islands(
        aggregate_id=agg_id,
        islands_data=[
            {
                "island_id": "isl_v1",
                "name": "Initial Skepticism",
                "mental_model": "Original mental model",
                "resistance_patterns": ["p1"],
                "friction_points": ["f1"],
                "source_evidence_hashes": [ev_hash],
                "version": 1,
            }
        ],
        context=tenant_ctx,
    )

    proj_res = coordinator.project_current_state(
        aggregate_id=agg_id,
        activation_coordinates_bps={"skepticism_bps": 8000},
        viewer_state_sequence=["RESISTANT", "OPEN"],
        tension_summary="Initial summary",
        context=tenant_ctx,
    )
    assert proj_res.aggregate.current_state == "CONTEXT_PROJECTED"

    # 2. Supersede island explicitly (version 1 -> version 2)
    ev_hash_2 = hashlib.sha256(b"second_source_evidence").hexdigest()
    superseded_island = coordinator.supersede_cognitive_island(
        aggregate_id=agg_id,
        island_id="isl_v1",
        updated_name="Evolved Skepticism & Audit Readiness",
        updated_mental_model="Refined model: willing to adopt under cryptographic trace guarantees",
        updated_resistance_patterns=["p1", "p2_audit_required"],
        updated_friction_points=["f1"],
        updated_source_evidence_hashes=[ev_hash, ev_hash_2],
        context=tenant_ctx,
    )

    assert superseded_island.version == 2
    assert superseded_island.parent_island_sha256 is not None
    assert len(superseded_island.parent_island_sha256) == 64

    # 3. Recompile derived projections against updated island
    new_proj = coordinator.recompile_projections(
        aggregate_id=agg_id,
        activation_coordinates_bps={"skepticism_bps": 5500, "readiness_bps": 7500},
        viewer_state_sequence=["CURIOUS", "ENGAGED"],
        tension_summary="Audience readiness increased following receipt proof demonstration.",
        context=tenant_ctx,
    )

    assert new_proj.source_island_hashes[0] == superseded_island.content_sha256
    assert new_proj.activation_coordinates_bps["readiness_bps"] == 7500

    snapshot = coordinator.get_snapshot(agg_id, tenant_ctx)
    assert snapshot.cognitive_islands[0].version == 2
    assert snapshot.current_projection.projection_sha256 == new_proj.projection_sha256


# ============================================================================
# 5. Multi-Tenant Workspace Boundary & Isolation Tests
# ============================================================================

def test_cross_workspace_isolation_rejection(runtime_stack, workspace_id, audience_id, tenant_ctx):
    coordinator: AudienceContextProgramCoordinator = runtime_stack["audience_coordinator"]

    # Initialize in workspace A
    init_res = coordinator.initialize_audience(
        workspace_id=workspace_id,
        audience_id=audience_id,
        target_segment="Segment A",
        context=tenant_ctx,
    )
    agg_id = init_res.aggregate.aggregate_id

    # Foreign tenant context for workspace B
    foreign_ctx = TenantContext(
        workspace_id=uuid4(),
        actor_id="usr_foreign_001",
        role="MEMBER",
        is_operator=False,
    )

    # Attempting to access or mutate from foreign workspace raises CrossWorkspaceLeakError
    with pytest.raises(CrossWorkspaceLeakError):
        coordinator.hunt_tensions(
            aggregate_id=agg_id,
            tension_observations=[],
            context=foreign_ctx,
        )

    with pytest.raises(CrossWorkspaceLeakError):
        coordinator.get_snapshot(agg_id, foreign_ctx)


# ============================================================================
# 6. Anti-Self-Approval Operator Gate Enforcement
# ============================================================================

def test_operator_gate_anti_self_approval_enforcement(runtime_stack, workspace_id, audience_id, tenant_ctx):
    coordinator: AudienceContextProgramCoordinator = runtime_stack["audience_coordinator"]

    init_res = coordinator.initialize_audience(
        workspace_id=workspace_id,
        audience_id=audience_id,
        target_segment="Enterprise",
        context=tenant_ctx,
        actor_id="requester_agent_01",
    )
    agg_id = init_res.aggregate.aggregate_id

    coordinator.hunt_tensions(
        aggregate_id=agg_id,
        tension_observations=[{"tension_id": "t1", "severity_bps": 5000}],
        context=tenant_ctx,
    )

    ev_hash = hashlib.sha256(b"source").hexdigest()
    coordinator.map_cognitive_islands(
        aggregate_id=agg_id,
        islands_data=[
            {
                "island_id": "isl_1",
                "name": "Island 1",
                "mental_model": "MM1",
                "resistance_patterns": [],
                "friction_points": [],
                "source_evidence_hashes": [ev_hash],
                "version": 1,
            }
        ],
        context=tenant_ctx,
    )

    coordinator.project_current_state(
        aggregate_id=agg_id,
        activation_coordinates_bps={"readiness_bps": 6000},
        viewer_state_sequence=["RESISTANT", "ACTIVE"],
        tension_summary="Summary",
        context=tenant_ctx,
    )

    # Context of requester attempting to self-approve as operator
    requester_as_operator_ctx = TenantContext(
        workspace_id=workspace_id,
        actor_id="requester_agent_01",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id=uuid4(),
    )

    with pytest.raises(SelfApprovalProhibitedError):
        coordinator.approve_audience_context(
            aggregate_id=agg_id,
            operator_context=requester_as_operator_ctx,
            approver_id="requester_agent_01",
            approval_decision="APPROVED",
            requester_id="requester_agent_01",
        )


# ============================================================================
# 7. Recovery & Repair Lifecycle Routing
# ============================================================================

def test_recovery_routing_to_repairing_and_resume(runtime_stack, workspace_id, audience_id, tenant_ctx):
    coordinator: AudienceContextProgramCoordinator = runtime_stack["audience_coordinator"]

    init_res = coordinator.initialize_audience(
        workspace_id=workspace_id,
        audience_id=audience_id,
        target_segment="Enterprise",
        context=tenant_ctx,
    )
    agg_id = init_res.aggregate.aggregate_id

    # Route to REPAIRING on simulated fault
    repaired_agg = coordinator.recover_to_repairing(
        aggregate_id=agg_id,
        failure_reason="Corrupted external market feed during tension hunting",
        context=tenant_ctx,
    )
    assert repaired_agg.current_state == "REPAIRING"
    assert repaired_agg.lifecycle == ProgramStateLifecycle.REPAIRING

    # Transition back from REPAIRING to AUDIENCE_INITIALIZED via repair_audience_context
    def repair_work(agg: ProgramStateAggregate) -> dict:
        data = dict(agg.state_data)
        data["repair_resolved"] = True
        return data

    repair_res = runtime_stack["coordinator"].execute_state_phase(
        aggregate_id=agg_id,
        transition_name="repair_audience_context",
        actor_id="aud_commander_01",
        actor_lane=AuthorityLane.COMMANDER,
        work_fn=repair_work,
        context=tenant_ctx,
        context_claims=["workspace_active", "operator_authorized"],
    )
    assert repair_res.aggregate.current_state == "AUDIENCE_INITIALIZED"
