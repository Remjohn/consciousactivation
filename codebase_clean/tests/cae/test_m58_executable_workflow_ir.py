"""
Unit and Integration Tests for CAE Mandate M58: Executable Workflow IR.

Validates:
- All 5 Acceptance Gates
- All 4 False-proof/Reward-hacking Defense Vectors (§10)
- Structural Diffing Engine (WorkflowIRDiff)
- Compilation to Runtime Workflow Definition (validate_runtime_workflow compatibility)
"""

import pytest
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.workflow_ir import (
    ExecutableWorkflowIR,
    IREdgeType,
    WorkflowIRBranchTargetMissingError,
    WorkflowIRCompilationError,
    WorkflowIRCompiler,
    WorkflowIRCyclicGraphError,
    WorkflowIRDiff,
    WorkflowIRDiffResult,
    WorkflowIRDuplicateNodeError,
    WorkflowIREdge,
    WorkflowIRError,
    WorkflowIRNode,
    WorkflowIRNodeNotFoundError,
    WorkflowIRValidationError,
    WorkflowIRValidator,
)
from ca_runtime.workflow_primitives import (
    AgentMutatedLoopBoundError,
    ConditionBranchDefinition,
    HumanGateRequirement,
    LoopBoundPolicy,
    ParallelBranchDefinition,
    ParallelSideEffectConflictError,
    SwitchCaseDefinition,
    UnboundedLoopError,
    UnevaluableConditionError,
    WorkflowPrimitiveDefinition,
    WorkflowPrimitiveKind,
    WorkflowStepContract,
    WorkUnitKind,
)
from cmf_pipeline.workflow.domain.models import validate_runtime_workflow


# ============================================================================
# Gate 1: IR validates before runtime compilation
# ============================================================================


def test_gate1_ir_validates_before_runtime_compilation() -> None:
    """Verify ExecutableWorkflowIR structural and semantic validation."""
    node_1 = WorkflowIRNode(
        node_id="NODE_EXTRACT",
        capability_id="research_signal_extraction",
        phase_order=1,
        purpose="Extract signal from research sources",
        actor_kind="DETERMINISTIC_MODULE",
        role="HUNTER",
        product_boundary="AHP",
        side_effect_class="READ_ONLY",
        input_contracts=("RAW_EVIDENCE_CONTRACT",),
        output_contracts=("SIGNAL_CONTRACT",),
    )
    node_2 = WorkflowIRNode(
        node_id="NODE_ANALYZE",
        capability_id="relationship_canonicalization",
        phase_order=2,
        purpose="Analyze entity relationships",
        actor_kind="AGENT_PROGRAM",
        role="ANALYST",
        product_boundary="AIR",
        side_effect_class="READ_ONLY",
        input_contracts=("SIGNAL_CONTRACT",),
        output_contracts=("CANONICAL_KNOWLEDGE_CONTRACT",),
    )
    edge_1 = WorkflowIREdge(
        source_node_id="NODE_EXTRACT",
        target_node_id="NODE_ANALYZE",
        contract_id="SIGNAL_CONTRACT",
    )

    ir = ExecutableWorkflowIR(
        workflow_ir_id="WIR_RESEARCH_CANONICALIZATION",
        name="Research Canonicalization Workflow",
        version="1.0.0",
        category_id="RESEARCH",
        profile_id="CANONICALIZATION",
        purpose="Transform research signals into canonical knowledge",
        authority_lane=AuthorityLane.ANALYST,
        nodes=(node_1, node_2),
        edges=(edge_1,),
        topological_order=("NODE_EXTRACT", "NODE_ANALYZE"),
    )

    WorkflowIRValidator.validate_ir(ir)
    assert ir.verify_integrity()
    assert len(ir.ir_digest_sha256) == 64


# ============================================================================
# Gate 2: Equivalent source graphs produce canonicalized identity
# ============================================================================


def test_gate2_equivalent_source_graphs_produce_canonicalized_identity() -> None:
    """Verify that scrambled node/edge insertion orders produce identical SHA-256 digests."""
    nodes_source_a = [
        {"node_id": "STEP_A", "capability_id": "cap_a", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "STEP_B", "capability_id": "cap_b", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "STEP_C", "capability_id": "cap_c", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
    ]
    edges_source_a = [
        {"source_node_id": "STEP_A", "target_node_id": "STEP_B", "contract_id": "C1"},
        {"source_node_id": "STEP_B", "target_node_id": "STEP_C", "contract_id": "C2"},
    ]

    # Scrambled order for B
    nodes_source_b = [
        {"node_id": "STEP_C", "capability_id": "cap_c", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "STEP_A", "capability_id": "cap_a", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "STEP_B", "capability_id": "cap_b", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges_source_b = [
        {"source_node_id": "STEP_B", "target_node_id": "STEP_C", "contract_id": "C2"},
        {"source_node_id": "STEP_A", "target_node_id": "STEP_B", "contract_id": "C1"},
    ]

    ir_a = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_CANONICAL_TEST",
        name="Canonical Equivalence Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Equivalence Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes_source_a,
        edges=edges_source_a,
    )

    ir_b = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_CANONICAL_TEST",
        name="Canonical Equivalence Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Equivalence Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes_source_b,
        edges=edges_source_b,
    )

    assert ir_a.ir_digest_sha256 == ir_b.ir_digest_sha256
    assert ir_a.topological_order == ir_b.topological_order == ("STEP_A", "STEP_B", "STEP_C")

    # Diff engine should confirm they are identical
    diff = WorkflowIRDiff.diff(ir_a, ir_b)
    assert diff.identical
    assert not diff.added_nodes
    assert not diff.removed_nodes
    assert not diff.modified_nodes


# ============================================================================
# Gate 3: Illegal cycles are rejected unless an explicit LOOP primitive declares termination
# ============================================================================


def test_gate3_illegal_cycles_rejected_and_bounded_loops_permitted() -> None:
    """Verify that unbounded cycles raise error, but bounded loops are accepted."""
    # Case A: Illegal unbounded cycle A -> B -> C -> A
    nodes_cyclic = [
        {"node_id": "A", "capability_id": "cap_a", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "B", "capability_id": "cap_b", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "C", "capability_id": "cap_c", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
    ]
    edges_cyclic = [
        {"source_node_id": "A", "target_node_id": "B", "contract_id": "C1"},
        {"source_node_id": "B", "target_node_id": "C", "contract_id": "C2"},
        {"source_node_id": "C", "target_node_id": "A", "contract_id": "C3"},  # Unbounded back-edge!
    ]

    with pytest.raises(WorkflowIRCyclicGraphError) as exc_info:
        WorkflowIRCompiler.compile_from_source(
            workflow_ir_id="WIR_BAD_CYCLE",
            name="Illegal Cycle Test",
            category_id="TEST",
            profile_id="DEFAULT",
            purpose="Cycle Detection",
            authority_lane=AuthorityLane.ANALYST,
            nodes=nodes_cyclic,
            edges=edges_cyclic,
        )
    assert exc_info.value.reason_code == "ERR_WORKFLOW_IR_ILLEGAL_CYCLE"

    # Case B: Authorized bounded loop A -> B (with LOOP_BACK to A governed by LoopBoundPolicy)
    node_loop = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_LOOP_A",
        primitive_kind=WorkflowPrimitiveKind.LOOP,
        loop_policy=LoopBoundPolicy(max_iterations=3, timeout_seconds=120),
    )
    nodes_loop = [
        {"node_id": "A", "capability_id": "cap_a", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": node_loop},
        {"node_id": "B", "capability_id": "cap_b", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges_loop = [
        {"source_node_id": "A", "target_node_id": "B", "contract_id": "C1"},
        {"source_node_id": "B", "target_node_id": "A", "contract_id": "C2", "edge_type": IREdgeType.LOOP_BACK.value},
    ]

    ir_loop = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_BOUNDED_LOOP",
        name="Bounded Loop Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Bounded Loop Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes_loop,
        edges=edges_loop,
    )
    assert ir_loop.topological_order == ("A", "B")
    assert ir_loop.verify_integrity()


# ============================================================================
# Gate 4: Branch conditions reference declared values and valid targets
# ============================================================================


def test_gate4_branch_conditions_and_targets_validated() -> None:
    """Verify that condition and switch branch targets must exist in graph."""
    # Case A: Missing then_step_id
    cond_missing = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_COND_BAD",
        primitive_kind=WorkflowPrimitiveKind.CONDITION,
        condition_config=ConditionBranchDefinition(
            condition_expression="eval_score >= 80",
            then_step_id="NON_EXISTENT_STEP",
            else_step_id="STEP_B",
        ),
    )
    nodes_bad_cond = [
        {"node_id": "STEP_A", "capability_id": "cap_a", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": cond_missing},
        {"node_id": "STEP_B", "capability_id": "cap_b", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges_bad_cond = [
        {"source_node_id": "STEP_A", "target_node_id": "STEP_B", "contract_id": "C1"},
    ]

    with pytest.raises(WorkflowIRBranchTargetMissingError) as exc_info:
        WorkflowIRCompiler.compile_from_source(
            workflow_ir_id="WIR_BAD_BRANCH",
            name="Missing Branch Target Test",
            category_id="TEST",
            profile_id="DEFAULT",
            purpose="Branch Verification",
            authority_lane=AuthorityLane.ANALYST,
            nodes=nodes_bad_cond,
            edges=edges_bad_cond,
        )
    assert exc_info.value.reason_code == "ERR_WORKFLOW_IR_BRANCH_TARGET_MISSING"


# ============================================================================
# Gate 5: Runtime compiler remains the execution authority
# ============================================================================


def test_gate5_compiles_to_runtime_workflow_definition() -> None:
    """Verify ExecutableWorkflowIR compiles into dictionary accepted by validate_runtime_workflow()."""
    nodes_src = [
        {
            "node_id": "SIGNAL_EXTRACTION",
            "capability_id": "research_signal_extraction",
            "phase_order": 1,
            "purpose": "Extract research signals",
            "actor_kind": "DETERMINISTIC_MODULE",
            "role": "HUNTER",
            "product_boundary": "AHP",
            "side_effect_class": "READ_ONLY",
            "input_contracts": ["RAW_EVIDENCE"],
            "output_contracts": ["RESEARCH_SIGNALS"],
        },
        {
            "node_id": "CANONICAL_SYNTHESIS",
            "capability_id": "relationship_canonicalization",
            "phase_order": 2,
            "purpose": "Synthesize relationships",
            "actor_kind": "AGENT_PROGRAM",
            "role": "ANALYST",
            "product_boundary": "AIR",
            "side_effect_class": "READ_ONLY",
            "input_contracts": ["RESEARCH_SIGNALS"],
            "output_contracts": ["CANONICAL_KNOWLEDGE"],
        },
    ]
    edges_src = [
        {
            "source_node_id": "SIGNAL_EXTRACTION",
            "target_node_id": "CANONICAL_SYNTHESIS",
            "contract_id": "RESEARCH_SIGNALS",
        }
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_PIPELINE_SYNTHESIS",
        name="Pipeline Synthesis",
        category_id="RESEARCH",
        profile_id="CANONICALIZATION",
        purpose="Synthesize research",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes_src,
        edges=edges_src,
        wrong_reading_locks=["LOCK_NO_SYNTHETIC_CANDIDATES"],
        evaluation_requirements=["REQUIRE_GROUNDED_SIGNALS"],
        repair_laws=["BOUNDED_REPAIR_LAW"],
    )

    binding_manifest = {
        "manifest_id": "bm_synthesis_v1",
        "bindings": [
            {
                "capability_id": "research_signal_extraction",
                "implementation_id": "cmf_pipeline.signal_extractor",
                "implementation_version": "1.0.0",
                "implementation_sha256": "a" * 64,
                "owner_product": "AHP",
                "implementation_kind": "DETERMINISTIC_MODULE",
                "side_effect_class": "READ_ONLY",
                "authority_boundary": "HUNTER",
            },
            {
                "capability_id": "relationship_canonicalization",
                "implementation_id": "cmf_pipeline.relationship_analyst",
                "implementation_version": "1.0.0",
                "implementation_sha256": "b" * 64,
                "owner_product": "AIR",
                "implementation_kind": "AGENT_PROGRAM",
                "side_effect_class": "READ_ONLY",
                "authority_boundary": "ANALYST",
            },
        ],
    }

    runtime_projection = WorkflowIRCompiler.compile_to_runtime_projection(ir, binding_manifest)

    # Validate against pipeline validate_runtime_workflow
    validated = validate_runtime_workflow(runtime_projection)
    assert validated["source_projection_id"] == "proj_WIR_PIPELINE_SYNTHESIS"
    assert len(validated["nodes"]) == 2
    assert len(validated["edges"]) == 1
    assert validated["topological_order"] == ["SIGNAL_EXTRACTION", "CANONICAL_SYNTHESIS"]


# ============================================================================
# Structural Diffing Engine Tests
# ============================================================================


def test_workflow_ir_diff_engine() -> None:
    """Verify WorkflowIRDiff identifies added, removed, and modified elements."""
    base_nodes = [
        {"node_id": "N1", "capability_id": "cap_1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "N2", "capability_id": "cap_2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    base_edges = [
        {"source_node_id": "N1", "target_node_id": "N2", "contract_id": "C1"},
    ]

    ir_v1 = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_DIFF_TEST",
        name="Diff Test",
        version="1.0.0",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Diff Engine",
        authority_lane=AuthorityLane.ANALYST,
        nodes=base_nodes,
        edges=base_edges,
    )

    # Version 2: Modified N2 (role changed to COMPOSER), Added N3
    v2_nodes = [
        {"node_id": "N1", "capability_id": "cap_1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "N2", "capability_id": "cap_2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "COMPOSER", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "N3", "capability_id": "cap_3", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "READ_ONLY"},
    ]
    v2_edges = [
        {"source_node_id": "N1", "target_node_id": "N2", "contract_id": "C1"},
        {"source_node_id": "N2", "target_node_id": "N3", "contract_id": "C2"},
    ]

    ir_v2 = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_DIFF_TEST",
        name="Diff Test",
        version="2.0.0",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Diff Engine",
        authority_lane=AuthorityLane.ANALYST,
        nodes=v2_nodes,
        edges=v2_edges,
    )

    diff = WorkflowIRDiff.diff(ir_v1, ir_v2)
    assert not diff.identical
    assert diff.added_nodes == ("N3",)
    assert not diff.removed_nodes
    assert diff.modified_nodes == ("N2",)
    assert diff.added_edges == (("N2", "N3", "C2"),)
    assert not diff.removed_edges


# ============================================================================
# False-Proof & Reward-Hacking Defenses (§10)
# ============================================================================


def test_false_proof_1_hidden_cycle_rejected() -> None:
    """False-proof 1: Encode a hidden cycle among 4 nodes."""
    nodes = [
        {"node_id": "N1", "capability_id": "c1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "N2", "capability_id": "c2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "N3", "capability_id": "c3", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "N4", "capability_id": "c4", "phase_order": 4, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "READ_ONLY"},
    ]
    edges = [
        {"source_node_id": "N1", "target_node_id": "N2", "contract_id": "C1"},
        {"source_node_id": "N2", "target_node_id": "N3", "contract_id": "C2"},
        {"source_node_id": "N3", "target_node_id": "N4", "contract_id": "C3"},
        {"source_node_id": "N4", "target_node_id": "N2", "contract_id": "C4"},  # Hidden cycle N2 -> N3 -> N4 -> N2
    ]

    with pytest.raises(WorkflowIRCyclicGraphError) as exc_info:
        WorkflowIRCompiler.compile_from_source(
            workflow_ir_id="WIR_HIDDEN_CYCLE",
            name="Hidden Cycle",
            category_id="TEST",
            profile_id="DEFAULT",
            purpose="Cycle Defense",
            authority_lane=AuthorityLane.ANALYST,
            nodes=nodes,
            edges=edges,
        )
    assert exc_info.value.reason_code == "ERR_WORKFLOW_IR_ILLEGAL_CYCLE"


def test_false_proof_2_loop_without_bound_rejected() -> None:
    """False-proof 2: Create a loop without bound or termination condition."""
    with pytest.raises(UnboundedLoopError):
        LoopBoundPolicy(max_iterations=0)


def test_false_proof_3_missing_branch_target_rejected() -> None:
    """False-proof 3: Omit a branch target in switch cases."""
    switch_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_SWITCH",
        primitive_kind=WorkflowPrimitiveKind.SWITCH,
        switch_cases=(
            SwitchCaseDefinition(match_value="CASE_A", target_step_id="TARGET_EXISTS"),
            SwitchCaseDefinition(match_value="CASE_B", target_step_id="TARGET_MISSING"),
        ),
    )
    nodes = [
        {"node_id": "SWITCH_NODE", "capability_id": "c1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": switch_prim},
        {"node_id": "TARGET_EXISTS", "capability_id": "c2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges = [
        {"source_node_id": "SWITCH_NODE", "target_node_id": "TARGET_EXISTS", "contract_id": "C1"},
    ]

    with pytest.raises(WorkflowIRBranchTargetMissingError) as exc_info:
        WorkflowIRCompiler.compile_from_source(
            workflow_ir_id="WIR_MISSING_SWITCH_TARGET",
            name="Missing Target",
            category_id="TEST",
            profile_id="DEFAULT",
            purpose="Branch Defense",
            authority_lane=AuthorityLane.ANALYST,
            nodes=nodes,
            edges=edges,
        )
    assert exc_info.value.reason_code == "ERR_WORKFLOW_IR_BRANCH_TARGET_MISSING"


def test_false_proof_4_parallel_conflicting_mutations_rejected() -> None:
    """False-proof 4: Two nodes both mutate the same external side effect concurrently."""
    nodes = [
        {"node_id": "PARENT", "capability_id": "c0", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "MUTATOR_1", "capability_id": "c1", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "MUTATION_OPERATION"},
        {"node_id": "MUTATOR_2", "capability_id": "c2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "MUTATION_OPERATION"},
    ]
    edges = [
        {"source_node_id": "PARENT", "target_node_id": "MUTATOR_1", "contract_id": "C1"},
        {"source_node_id": "PARENT", "target_node_id": "MUTATOR_2", "contract_id": "C2"},
    ]

    with pytest.raises(ParallelSideEffectConflictError) as exc_info:
        WorkflowIRCompiler.compile_from_source(
            workflow_ir_id="WIR_PARALLEL_CONFLICT",
            name="Parallel Conflict",
            category_id="TEST",
            profile_id="DEFAULT",
            purpose="Side-Effect Defense",
            authority_lane=AuthorityLane.ANALYST,
            nodes=nodes,
            edges=edges,
        )
    assert exc_info.value.reason_code == "ERR_PARALLEL_SIDE_EFFECT_CONFLICT"


# ============================================================================
# Concrete End-to-End IR Compilation Trace
# ============================================================================


def test_concrete_ir_compilation_and_runtime_validation_trace() -> None:
    """Demonstrate end-to-end compilation: Source Dict -> ExecutableWorkflowIR -> Runtime Projection -> Pipeline Validation."""
    # 1. Source definition
    source_nodes = [
        {
            "node_id": "HUNTER_EXTRACTION",
            "capability_id": "research_signal_extraction",
            "phase_order": 1,
            "purpose": "Extract candidate signals from verified sources",
            "actor_kind": "DETERMINISTIC_MODULE",
            "role": "HUNTER",
            "product_boundary": "AHP",
            "side_effect_class": "READ_ONLY",
            "input_contracts": ["RAW_MEDIA_STREAM"],
            "output_contracts": ["RESEARCH_SIGNALS"],
        },
        {
            "node_id": "ANALYST_CANONICALIZATION",
            "capability_id": "relationship_canonicalization",
            "phase_order": 2,
            "purpose": "Synthesize entity relationships and ontology",
            "actor_kind": "AGENT_PROGRAM",
            "role": "ANALYST",
            "product_boundary": "AIR",
            "side_effect_class": "READ_ONLY",
            "input_contracts": ["RESEARCH_SIGNALS"],
            "output_contracts": ["OKF_KNOWLEDGE_BUNDLE"],
        },
        {
            "node_id": "COMMANDER_RELEASE_GATE",
            "capability_id": "operator_release_approval",
            "phase_order": 3,
            "purpose": "Human operator release approval gate",
            "actor_kind": "HUMAN_GATE",
            "role": "COMMANDER",
            "product_boundary": "STUDIO",
            "side_effect_class": "READ_ONLY",
            "input_contracts": ["OKF_KNOWLEDGE_BUNDLE"],
            "output_contracts": ["RATIFIED_RELEASE_RECEIPT"],
        },
    ]

    source_edges = [
        {"source_node_id": "HUNTER_EXTRACTION", "target_node_id": "ANALYST_CANONICALIZATION", "contract_id": "RESEARCH_SIGNALS"},
        {"source_node_id": "ANALYST_CANONICALIZATION", "target_node_id": "COMMANDER_RELEASE_GATE", "contract_id": "OKF_KNOWLEDGE_BUNDLE"},
    ]

    # 2. Compile to ExecutableWorkflowIR
    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_E2E_CANONICAL_CHAIN",
        name="End-to-End Canonical Chain",
        version="1.0.0",
        category_id="RESEARCH",
        profile_id="PRODUCTION",
        purpose="Full verified research-to-operator pipeline",
        authority_lane=AuthorityLane.COMMANDER,
        nodes=source_nodes,
        edges=source_edges,
        wrong_reading_locks=["LOCK_NO_SYNTHETIC_DATA"],
        evaluation_requirements=["VERIFIED_OKF_SCHEMA"],
        repair_laws=["BOUNDED_SAME_SESSION_REPAIR"],
    )

    assert ir.topological_order == ("HUNTER_EXTRACTION", "ANALYST_CANONICALIZATION", "COMMANDER_RELEASE_GATE")
    assert ir.verify_integrity()

    # 3. Compile to Runtime Projection
    bindings = {
        "manifest_id": "bm_e2e_001",
        "bindings": [
            {
                "capability_id": "research_signal_extraction",
                "implementation_id": "cmf_pipeline.extractor_impl",
                "implementation_version": "1.0.0",
                "implementation_sha256": "1" * 64,
                "owner_product": "AHP",
                "implementation_kind": "DETERMINISTIC_MODULE",
                "side_effect_class": "READ_ONLY",
                "authority_boundary": "HUNTER",
            },
            {
                "capability_id": "relationship_canonicalization",
                "implementation_id": "cmf_pipeline.analyst_impl",
                "implementation_version": "1.0.0",
                "implementation_sha256": "2" * 64,
                "owner_product": "AIR",
                "implementation_kind": "AGENT_PROGRAM",
                "side_effect_class": "READ_ONLY",
                "authority_boundary": "ANALYST",
            },
            {
                "capability_id": "operator_release_approval",
                "implementation_id": "cmf_pipeline.gate_impl",
                "implementation_version": "1.0.0",
                "implementation_sha256": "3" * 64,
                "owner_product": "STUDIO",
                "implementation_kind": "HUMAN_GATE",
                "side_effect_class": "READ_ONLY",
                "authority_boundary": "COMMANDER",
            },
        ],
    }

    runtime_dict = WorkflowIRCompiler.compile_to_runtime_projection(ir, bindings)

    # 4. Pipeline validation
    validated = validate_runtime_workflow(runtime_dict)
    assert validated["source_projection_id"] == "proj_WIR_E2E_CANONICAL_CHAIN"
    assert len(validated["nodes"]) == 3
    assert len(validated["edges"]) == 2
    assert validated["topological_order"] == ["HUNTER_EXTRACTION", "ANALYST_CANONICALIZATION", "COMMANDER_RELEASE_GATE"]
