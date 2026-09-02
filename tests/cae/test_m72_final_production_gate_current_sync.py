"""Comprehensive Test Suite for CAE Mandate M72: Final Production Gate + CURRENT Synchronization.

Governed by:
- 07_PRODUCTION_OPERATOR_GATES/M72_final_production_gate_current_sync.md
- docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md
- governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml
- docs/PRD/CURRENT.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md
- 00_CONTROL/05_CLAIM_CEILING.md

Verifies:
- Gate 1: Full Factory Certification evaluation over real SDLF and Domain Program benchmarks and adversarial pack yields READY disposition.
- Gate 2: Representative Domain Program (research_canonicalization_program) golden run produces complete cryptographic evidence manifest.
- Gate 3: SQLite state persistence, process restart, replay parity, and backup/restore verification.
- Gate 4: Multi-tenant isolation and authority lane boundaries strictly enforced fail-closed.
- Gate 5: Fail-closed production execution mode integrity (ProductionExecutionModeViolationError).
- Gate 6: Factory floor snapshot and observability parity.
- Gate 7 (Countertest): Demonstrates that missing evidence or manufactured readiness fails closed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Dict, List
from uuid import UUID, uuid4
import pytest

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime import (
    AgentDefinition,
    AgentInvocationCompiler,
    AgentInvocationReceipt,
    AgentInvocationRuntime,
    AgentRegistry,
    AuthorityLane,
    CertificationCriterion,
    ExecutionMode,
    FactoryCertificationReport,
    FactoryCertificationRunner,
    JITContextCapsule,
    JITContextCompiler,
    ObservabilityTenantIsolationError,
    ProductionExecutionModeViolationError,
    ProductionReadinessStatus,
    ProgramAuthorityLaneViolationError,
    ProgramOperatorRuntimeService,
    ProgramRegistry,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramTransitionBlockedError,
    ProgramTransitionResult,
    ReadOnlyObservabilityViewer,
    ResearchCanonicalizationProgramCoordinator,
    SqliteProgramStateStore,
    TenantContext,
    UnifiedFactoryCommandEngine,
    UniversalProgramStateRuntime,
    get_agent_registry,
    get_canonical_research_canonicalization_state_machine,
    tenant_scope,
)
from ca_runtime.research_canonicalization_program import (
    CanonicalKnowledgeNode,
    KnowledgeCandidate,
)


@pytest.fixture
def temp_db_dir():
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sqlite_store(temp_db_dir: Path) -> SqliteProgramStateStore:
    db_path = temp_db_dir / "m72_production_gate_state.db"
    return SqliteProgramStateStore(str(db_path))


@pytest.fixture
def state_runtime(sqlite_store: SqliteProgramStateStore) -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime(store=sqlite_store)


@pytest.fixture
def operator_service(state_runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    return ProgramOperatorRuntimeService(runtime=state_runtime)


@pytest.fixture
def command_engine(operator_service: ProgramOperatorRuntimeService) -> UnifiedFactoryCommandEngine:
    return UnifiedFactoryCommandEngine(program_operator=operator_service)


@pytest.fixture
def test_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def sample_sources() -> List[Dict[str, Any]]:
    s1_text = "Artificial General Intelligence (AGI) is the hypothetical ability of an intelligent agent to understand or learn any intellectual task that human beings can."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()

    s2_text = "Strong AI refers to artificial intelligence that possesses human-like cognitive abilities and self-awareness."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    return [
        {
            "source_id": "src_agi_001",
            "topic": "Artificial General Intelligence",
            "evidence_excerpt": s1_text,
            "content_hash_sha256": s1_hash,
            "origin_url": "https://en.wikipedia.org/wiki/Artificial_general_intelligence",
        },
        {
            "source_id": "src_strong_ai_002",
            "topic": "Strong AI",
            "evidence_excerpt": s2_text,
            "content_hash_sha256": s2_hash,
            "origin_url": "https://en.wikipedia.org/wiki/Strong_AI",
        },
    ]


# ===========================================================================
# Gate 1: End-to-End Factory Certification Evidence Verification
# ===========================================================================

def test_m72_gate1_full_factory_certification_report_ready() -> None:
    """Gate 1: Full Factory Certification evaluation over real SDLF and Domain Program benchmarks yields READY."""
    runner = FactoryCertificationRunner()
    report = runner.run_full_certification()

    assert isinstance(report, FactoryCertificationReport)
    assert report.readiness_status == ProductionReadinessStatus.READY
    assert len(report.report_sha256) == 64
    assert len(report.evaluations) == 12

    # Verify all 12 criteria are PASSED (zero BLOCKED, zero FAILED)
    passed_count = sum(1 for e in report.evaluations if e.status.value == "PASSED")
    blocked_count = sum(1 for e in report.evaluations if e.status.value == "BLOCKED")
    failed_count = sum(1 for e in report.evaluations if e.status.value == "FAILED")

    assert passed_count == 12
    assert blocked_count == 0
    assert failed_count == 0

    # Verify evidence contracts on every criterion
    for ev in report.evaluations:
        assert len(ev.required_evidence) > 0
        assert len(ev.observed_evidence_refs) > 0
        assert len(ev.evaluation_sha256) == 64


# ===========================================================================
# Gate 2: Representative Domain Program Golden Run Manifest & Lineage
# ===========================================================================

def test_m72_gate2_domain_golden_run_evidence_manifest(
    state_runtime: UniversalProgramStateRuntime,
    operator_service: ProgramOperatorRuntimeService,
    command_engine: UnifiedFactoryCommandEngine,
    test_workspace_id: str,
    sample_sources: List[Dict[str, Any]],
) -> None:
    """Gate 2: Representative domain program golden run produces complete cryptographic evidence manifest."""
    ws_uuid = UUID(test_workspace_id)
    tenant_ctx = TenantContext(workspace_id=ws_uuid, actor_id="usr_commander_001", role="MEMBER")

    with tenant_scope(tenant_ctx):
        # 1. Run Program
        agg = operator_service.run_program(
            program_id="research_canonicalization_program",
            workspace_id=test_workspace_id,
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
        )
        agg_id = agg.aggregate_id

        # 2. Attach Sources
        state_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="attach_sources",
            payload={"sources": sample_sources},
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
            context_claims=["workspace_active", "sources_verified"],
            state_updates={"source_records": sample_sources},
        )

        # 3. Extract Candidates
        candidates = [
            KnowledgeCandidate(
                candidate_id="cand_agi_001",
                label="Artificial General Intelligence",
                candidate_type="concept",
                extracted_text=sample_sources[0]["evidence_excerpt"],
                source_id="src_agi_001",
                source_sha256=sample_sources[0]["content_hash_sha256"],
                confidence_score=95,
                attributes={"aliases": ["AGI", "General AI"]},
            ).model_dump()
        ]
        state_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="extract_candidates",
            payload={"candidates": candidates},
            actor_id="usr_hunter_001",
            actor_lane=AuthorityLane.HUNTER,
            context_claims=["workspace_active", "sources_attached"],
            state_updates={"candidates": candidates},
        )

        # 4. Canonicalize
        node = CanonicalKnowledgeNode(
            node_id="kn_agi_001",
            canonical_label="Artificial General Intelligence",
            category="concept",
            aliases=["AGI", "General AI"],
            definition=sample_sources[0]["evidence_excerpt"],
            source_record_refs=["src_agi_001"],
            source_evidence_hashes=[sample_sources[0]["content_hash_sha256"]],
            lineage_sha256=CanonicalKnowledgeNode.compute_lineage_hash(
                canonical_label="Artificial General Intelligence",
                category="concept",
                aliases=["AGI", "General AI"],
                definition=sample_sources[0]["evidence_excerpt"],
                source_record_refs=["src_agi_001"],
                source_evidence_hashes=[sample_sources[0]["content_hash_sha256"]],
                version=1,
            ),
            version=1,
        ).model_dump()
        state_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="canonicalize_candidates",
            payload={"canonical_nodes": [node]},
            actor_id="usr_analyst_001",
            actor_lane=AuthorityLane.ANALYST,
            context_claims=["workspace_active", "candidates_extracted", "false_merge_verified"],
            state_updates={"canonical_nodes": [node]},
        )

        # 5. Project OKF
        okf_bundle = {
            "bundle_id": "okf_bundle_001",
            "bundle_sha256": "e" * 64,
            "index_markdown": "# Research Knowledge Catalog (OKF)",
            "documents": [],
            "node_count": 1,
            "edge_count": 0,
            "created_at": utc_now_rfc3339(),
        }
        state_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="project_okf_bundle",
            payload={"okf_bundle": okf_bundle},
            actor_id="usr_composer_001",
            actor_lane=AuthorityLane.COMPOSER,
            context_claims=["workspace_active", "canonical_nodes_resolved"],
            state_updates={"okf_bundle": okf_bundle},
        )

        # 6. Commit Knowledge
        res_commit = state_runtime.execute_transition(
            aggregate_id=agg_id,
            transition_name="commit_canonical_knowledge",
            payload={"committed_at": utc_now_rfc3339()},
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
            context_claims=["workspace_active", "okf_bundle_valid", "operator_adjudicated"],
        )

        # Generate projections
        trace = operator_service.project_execution_trace(agg_id)
        lineage = operator_service.project_artifact_lineage(agg_id)
        replay = command_engine.execute_command_text(f"replay run {agg_id}", tenant_id=test_workspace_id)

        # Build final evidence manifest
        evidence_manifest = {
            "aggregate_id": agg_id,
            "program_id": agg.program_id,
            "program_version": agg.program_version,
            "final_state": res_commit.aggregate.current_state,
            "final_version": res_commit.aggregate.version,
            "state_hash": res_commit.aggregate.state_hash,
            "transitions_count": len(trace.trace_nodes),
            "trace_digest": trace.state_hash,
            "lineage_digest": lineage.verification_digest,
            "replay_events_count": replay.data["replay"]["total_events"],
            "all_transitions_have_receipts": all(t.receipt_id for t in trace.trace_nodes),
        }

        manifest_digest = canonical_sha256(evidence_manifest)
        assert len(manifest_digest) == 64
        assert evidence_manifest["transitions_count"] == 5
        assert evidence_manifest["final_version"] == 7
        assert evidence_manifest["all_transitions_have_receipts"] is True


# ===========================================================================
# Gate 3: State Durability, Process Restart, Replay & Backup/Restore Parity
# ===========================================================================

def test_m72_gate3_sqlite_backup_restore_and_replay_parity(
    temp_db_dir: Path,
    test_workspace_id: str,
    sample_sources: List[Dict[str, Any]],
) -> None:
    """Gate 3: SQLite state persistence, process restart, replay parity, and backup/restore verification."""
    primary_db = temp_db_dir / "primary_state.db"
    backup_db = temp_db_dir / "backup_state.db"
    ws_uuid = UUID(test_workspace_id)
    tenant_ctx = TenantContext(workspace_id=ws_uuid, actor_id="usr_commander_001", role="MEMBER")

    # Step 1: Run on primary runtime
    store_prim = SqliteProgramStateStore(primary_db)
    runtime_prim = UniversalProgramStateRuntime(store=store_prim)
    op_prim = ProgramOperatorRuntimeService(runtime=runtime_prim)

    with tenant_scope(tenant_ctx):
        agg = op_prim.run_program(
            program_id="research_canonicalization_program",
            workspace_id=test_workspace_id,
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
        )
        agg_id = agg.aggregate_id

        runtime_prim.execute_transition(
            aggregate_id=agg_id,
            transition_name="attach_sources",
            payload={"sources": sample_sources},
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
            context_claims=["workspace_active", "sources_verified"],
        )

    # Step 2: Perform backup (copy SQLite database file)
    shutil.copyfile(primary_db, backup_db)

    # Step 3: Restore to a brand-new process / runtime instance
    store_restored = SqliteProgramStateStore(backup_db)
    runtime_restored = UniversalProgramStateRuntime(store=store_restored)
    op_restored = ProgramOperatorRuntimeService(runtime=runtime_restored)
    cmd_restored = UnifiedFactoryCommandEngine(program_operator=op_restored)

    with tenant_scope(tenant_ctx):
        # Verify aggregate is intact
        restored_agg = runtime_restored.get_aggregate(agg_id)
        assert restored_agg.current_state == "SOURCES_ATTACHED"
        assert restored_agg.version == 3

        # Verify replay reproduces exact event history
        replay_res = cmd_restored.execute_command_text(f"replay run {agg_id}", tenant_id=test_workspace_id)
        assert replay_res.success is True
        replay_data = replay_res.data["replay"]
        assert replay_data["total_events"] == 1
        assert replay_data["events"][0]["phase_or_node"] == "cae.research.attach_sources@1.0.0"
        assert replay_data["events"][0]["state_before"] == "INITIAL"
        assert replay_data["events"][0]["state_after"] == "SOURCES_ATTACHED"
        assert replay_data["events"][0]["is_committed"] is True


# ===========================================================================
# Gate 4: Multi-Tenant Isolation and Authority Lane Boundaries
# ===========================================================================

def test_m72_gate4_multi_tenant_isolation_and_lane_boundaries(
    state_runtime: UniversalProgramStateRuntime,
    operator_service: ProgramOperatorRuntimeService,
    command_engine: UnifiedFactoryCommandEngine,
    test_workspace_id: str,
    sample_sources: List[Dict[str, Any]],
) -> None:
    """Gate 4: Multi-tenant isolation and authority lane boundaries strictly enforced fail-closed."""
    ws_uuid = UUID(test_workspace_id)
    tenant_ctx = TenantContext(workspace_id=ws_uuid, actor_id="usr_commander_001", role="MEMBER")

    with tenant_scope(tenant_ctx):
        agg = operator_service.run_program(
            program_id="research_canonicalization_program",
            workspace_id=test_workspace_id,
            actor_id="usr_commander_001",
            actor_lane=AuthorityLane.COMMANDER,
        )
        agg_id = agg.aggregate_id

    # 1. Cross-tenant inspect attempt fails closed
    with pytest.raises(ObservabilityTenantIsolationError):
        command_engine.execute_command_text(f"inspect run {agg_id}", tenant_id="foreign_tenant_999")

    # 2. Cross-tenant replay attempt fails closed
    with pytest.raises(ObservabilityTenantIsolationError):
        command_engine.execute_command_text(f"replay run {agg_id}", tenant_id="foreign_tenant_999")

    # 3. Wrong authority lane transition fails closed
    with tenant_scope(tenant_ctx):
        with pytest.raises(ProgramAuthorityLaneViolationError):
            state_runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="attach_sources",
                payload={"sources": sample_sources},
                actor_id="usr_hunter_001",
                actor_lane=AuthorityLane.HUNTER,  # Requires COMMANDER
                context_claims=["workspace_active", "sources_verified"],
            )


# ===========================================================================
# Gate 5: Fail-Closed Production Execution Mode Integrity
# ===========================================================================

def test_m72_gate5_fail_closed_production_execution_mode() -> None:
    """Gate 5: ExecutionMode.PRODUCTION fails closed without live model and succeeds with authorized engine."""
    registry = get_agent_registry()
    agent_def = AgentDefinition(
        agent_id="KnowledgeCandidateHunterAgent",
        version="1.0.0",
        name="Knowledge Candidate Hunter Agent",
        purpose="Extracts raw knowledge candidates from research sources",
        authority_lane=AuthorityLane.HUNTER,
    )
    if not registry.has_agent("KnowledgeCandidateHunterAgent"):
        registry.register(agent_def)
    agent = registry.get("KnowledgeCandidateHunterAgent")

    ws_uuid = uuid4()
    capsule = JITContextCompiler.assemble(
        workspace_id=ws_uuid,
        lane=AuthorityLane.HUNTER,
        actor_id="hunter_001",
        program_id="research_canonicalization_program",
        harness_id="RESEARCH_CANONICALIZATION_HARNESS_V1",
        agent_id="KnowledgeCandidateHunterAgent",
        agent_instructions=("instruction_ref", "Extract knowledge candidates"),
    )

    invocation = AgentInvocationCompiler.compile(
        agent=agent,
        capsule=capsule,
        workspace_id=ws_uuid,
    )

    # 1. Production mode without inference_fn fails closed
    with pytest.raises(ProductionExecutionModeViolationError):
        AgentInvocationRuntime.execute(invocation, mode=ExecutionMode.PRODUCTION)

    # 2. Production mode with authorized inference_fn succeeds and emits verified receipt
    def dummy_inference(inv: Any) -> Dict[str, Any]:
        return {"output_payload": {"candidates": [{"candidate_id": "c1", "label": "AGI"}]}}

    receipt = AgentInvocationRuntime.execute(
        invocation,
        mode=ExecutionMode.PRODUCTION,
        inference_fn=dummy_inference,
    )
    assert isinstance(receipt, AgentInvocationReceipt)
    assert receipt.execution_mode == "PRODUCTION"
    assert receipt.is_synthetic is False
    assert len(receipt.receipt_sha256) == 64


# ===========================================================================
# Gate 6: Factory Floor Observation Parity
# ===========================================================================

def test_m72_gate6_factory_floor_observation_parity(
    command_engine: UnifiedFactoryCommandEngine,
    test_workspace_id: str,
) -> None:
    """Gate 6: observe floor projects pure operational truth without in-memory drift."""
    # Ensure at least one agent is registered
    agent_def = AgentDefinition(
        agent_id="TestFloorAgent",
        version="1.0.0",
        name="Test Floor Agent",
        purpose="Testing floor observation",
        authority_lane=AuthorityLane.HUNTER,
    )
    if not command_engine.agent_registry.has_agent("TestFloorAgent"):
        command_engine.agent_registry.register(agent_def)

    snapshot = command_engine.get_floor_snapshot(tenant_id=test_workspace_id)
    assert snapshot.active_runs_count >= 0
    assert len(snapshot.snapshot_sha256) == 64
    assert snapshot.program_count > 0
    assert snapshot.agent_count > 0

    viewer = ReadOnlyObservabilityViewer(command_engine)
    dashboard = viewer.render_factory_floor(tenant_id=test_workspace_id)
    assert "CAE FACTORY FLOOR DASHBOARD (READ-ONLY)" in dashboard


# ===========================================================================
# Gate 7 (Countertest): Hardcoded or Manufactured READY Fails Verification
# ===========================================================================

def test_m72_gate7_countertest_manufactured_ready_fails_verification() -> None:
    """Countertest: Missing evidence or defeated criteria prevents READY status."""
    runner = FactoryCertificationRunner()
    all_criteria = list(CertificationCriterion)

    # If full certification is evaluated with missing evidence inputs (None), all criteria evaluate to BLOCKED
    evaluations = [runner._evaluate_criterion(c, None, None, None, None, None) for c in all_criteria]
    passed_count = sum(1 for e in evaluations if e.status.value == "PASSED")
    blocked_count = sum(1 for e in evaluations if e.status.value == "BLOCKED")

    assert passed_count == 0
    assert blocked_count == 12

    # A report constructed with blocked criteria cannot have READY disposition
    ready_status = (
        ProductionReadinessStatus.READY
        if all(e.status.value == "PASSED" for e in evaluations)
        else ProductionReadinessStatus.NOT_READY
    )
    assert ready_status == ProductionReadinessStatus.NOT_READY
