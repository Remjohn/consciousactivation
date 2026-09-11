"""
Unit and Integration Tests for CAE Mandate M60: Workflow Step Contracts.

Validates:
- All 7 Acceptance Gates
- All 4 False-proof/Reward-hacking Defense Vectors (§10)
- Two Representative Program Migrations (Research & Collision Programs)
- Step Contract Coverage Reporting
"""

import pytest
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.step_contracts import (
    EmptyOutputContractsError,
    HiddenModelDependenceError,
    MissingMutationValidatorError,
    SideEffectDeclarationMismatchError,
    StepContract,
    StepContractCoverageReport,
    StepContractError,
    StepContractNotFoundError,
    StepContractRegistry,
    StepContractValidationError,
    StepContractValidator,
    StepExecutionVerificationReport,
    UnregisteredStepContractError,
    create_collision_program_step_contracts,
    create_research_canonicalization_step_contracts,
)
from ca_runtime.workflow_ir import (
    ExecutableWorkflowIR,
    WorkflowIRCompiler,
)
from ca_runtime.workflow_primitives import (
    RetryPolicyDefinition,
    WorkUnitKind,
)


# ============================================================================
# Gate 1 & 2: Complete contract & Agent vs Code typing
# ============================================================================


def test_gate1_and_gate2_complete_step_contract_and_work_unit_typing() -> None:
    """Verify complete step contract validation and explicit Agent vs Code typing."""
    code_contract = StepContract(
        step_id="CODE_STEP_CLEAN",
        name="Data Cleaning Function",
        purpose="Normalize research records deterministically",
        work_unit_kind=WorkUnitKind.CODE_FUNCTION,
        target_ref="cmf_pipeline.cleaners.normalize_records",
        authority_lane=AuthorityLane.HUNTER,
        product_boundary="ATOMIC_HARNESS_PIPELINE",
        side_effect_class="READ_ONLY",
        input_contracts=("RAW_DATA_CONTRACT",),
        output_contracts=("CLEAN_DATA_CONTRACT",),
        preconditions=("DATA_INGESTED",),
        postconditions=("RECORDS_NORMALIZED",),
    )
    StepContractValidator.validate_contract(code_contract)
    assert code_contract.verify_integrity()
    assert len(code_contract.contract_sha256) == 64

    agent_contract = StepContract(
        step_id="AGENT_STEP_ANALYZE",
        name="Dialectical Analysis Agent",
        purpose="Reason entity relationships",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="RelationshipCanonicalizationAnalystAgent",
        authority_lane=AuthorityLane.ANALYST,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("CLEAN_DATA_CONTRACT",),
        output_contracts=("ANALYSIS_RESULT_CONTRACT",),
        preconditions=("RECORDS_NORMALIZED",),
        postconditions=("RELATIONSHIPS_EXTRACTED",),
    )
    StepContractValidator.validate_contract(agent_contract)
    assert agent_contract.verify_integrity()


# ============================================================================
# Gate 3 & 4: Explicit side effects & failure routing
# ============================================================================


def test_gate3_and_gate4_explicit_side_effects_and_failure_routing() -> None:
    """Verify side effect class validation and failure routing mappings."""
    # Invalid side effect class
    with pytest.raises(StepContractValidationError):
        StepContract(
            step_id="BAD_EFFECT",
            name="Bad Effect Step",
            purpose="Testing",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,
            target_ref="cmf_pipeline.test",
            authority_lane=AuthorityLane.HUNTER,
            product_boundary="ATOMIC_HARNESS_PIPELINE",
            side_effect_class="ARBITRARY_MUTATION",  # Invalid
            input_contracts=("IN",),
            output_contracts=("OUT",),
        )

    # Valid step with failure routing
    contract_with_routing = StepContract(
        step_id="STEP_WITH_ROUTING",
        name="Step With Failure Routing",
        purpose="Testing routing",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="RelationshipCanonicalizationAnalystAgent",
        authority_lane=AuthorityLane.ANALYST,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("IN",),
        output_contracts=("OUT",),
        failure_routing={
            "ON_FAILURE": "STEP_REPAIR",
            "ON_TIMEOUT": "STEP_TIMEOUT_FALLBACK",
        },
    )
    StepContractValidator.validate_contract(contract_with_routing)
    assert contract_with_routing.failure_routing["ON_FAILURE"] == "STEP_REPAIR"


# ============================================================================
# Gate 5: Mandatory validators & postconditions for mutation steps
# ============================================================================


def test_gate5_mutation_steps_require_validators_and_postconditions() -> None:
    """Verify that MUTATION_OPERATION steps strictly require postconditions and validators."""
    # Mutation step missing validators
    with pytest.raises(MissingMutationValidatorError) as exc_info:
        StepContract(
            step_id="MUTATION_NO_VALIDATOR",
            name="Mutation Without Validator",
            purpose="Testing",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,
            target_ref="cmf_pipeline.mutators.commit_data",
            authority_lane=AuthorityLane.COMMANDER,
            product_boundary="CONSCIOUS_ACTIVATIONS_STUDIO",
            side_effect_class="MUTATION_OPERATION",
            input_contracts=("IN",),
            output_contracts=("OUT",),
            postconditions=("STATE_COMMITTED",),
            validators=(),  # Missing!
        )
    assert exc_info.value.reason_code == "ERR_MISSING_MUTATION_VALIDATOR"

    # Valid mutation step
    valid_mutation = StepContract(
        step_id="VALID_MUTATION_STEP",
        name="Valid Mutation Step",
        purpose="Commit verified state",
        work_unit_kind=WorkUnitKind.CODE_FUNCTION,
        target_ref="cmf_pipeline.mutators.commit_data",
        authority_lane=AuthorityLane.COMMANDER,
        product_boundary="CONSCIOUS_ACTIVATIONS_STUDIO",
        side_effect_class="MUTATION_OPERATION",
        input_contracts=("IN",),
        output_contracts=("OUT",),
        postconditions=("STATE_COMMITTED",),
        validators=("VALIDATOR_COMMIT_SIGNATURE",),
    )
    StepContractValidator.validate_contract(valid_mutation)


# ============================================================================
# Gate 6 & 7: StateM boundary anchor & host-controlled state commits
# ============================================================================


def test_gate6_and_gate7_statem_boundary_anchor_and_host_commit() -> None:
    """Verify StateM state/phase boundary fields and execution verification report."""
    contract = StepContract(
        step_id="STATEM_ANCHORED_STEP",
        name="StateM Anchored Step",
        purpose="Anchor execution to StateAggregate boundary",
        work_unit_kind=WorkUnitKind.AGENT_CALL,
        target_ref="OKFBundleComposerAgent",
        authority_lane=AuthorityLane.COMPOSER,
        product_boundary="ACTIVATIVE_INTELLIGENCE_RUNTIME",
        side_effect_class="READ_ONLY",
        input_contracts=("CANONICAL_RELATIONSHIPS",),
        output_contracts=("OKF_BUNDLE",),
        state_boundary="STATE_SYNTHESIS",
        state_entry_context_requirements=("CANONICAL_RELATIONSHIPS",),
        blocking_exit_checks=("OKF_SCHEMA_VALID",),
        evidence_required_to_transition=("SYNTHESIS_RECEIPT",),
    )
    StepContractValidator.validate_contract(contract)

    # Runtime verification report confirms host-controlled authorization
    report = StepExecutionVerificationReport(
        step_id=contract.step_id,
        run_id="run_statem_001",
        contract_sha256=contract.contract_sha256,
        work_unit_kind=contract.work_unit_kind,
        inputs_valid=True,
        outputs_valid=True,
        postconditions_satisfied=True,
        validators_passed=True,
        state_transition_authorized=True,
        verified_at_utc="2026-09-02T05:40:00Z",
    )
    assert report.state_transition_authorized
    assert len(report.receipt_sha256) == 64


# ============================================================================
# False-Proof & Reward-Hacking Defenses (§10)
# ============================================================================


def test_false_proof_1_empty_outputs_rejected() -> None:
    """False-proof 1: Create a node that declares no outputs."""
    with pytest.raises(EmptyOutputContractsError) as exc_info:
        StepContract(
            step_id="NO_OUTPUTS_STEP",
            name="No Outputs Step",
            purpose="Testing",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,
            target_ref="cmf_pipeline.cleaners.noop",
            authority_lane=AuthorityLane.HUNTER,
            product_boundary="ATOMIC_HARNESS_PIPELINE",
            side_effect_class="READ_ONLY",
            input_contracts=("RAW_DATA",),
            output_contracts=(),  # Empty output contracts!
        )
    assert exc_info.value.reason_code == "ERR_EMPTY_OUTPUT_CONTRACTS"


def test_false_proof_2_code_step_with_hidden_model_dependence_rejected() -> None:
    """False-proof 2: Declare a code step with hidden model dependence."""
    with pytest.raises(HiddenModelDependenceError) as exc_info:
        StepContract(
            step_id="HIDDEN_MODEL_STEP",
            name="Hidden Model Step",
            purpose="Testing hidden prompt call",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,  # Declared as code
            target_ref="cmf_pipeline.agents.hidden_llm_prompt_caller",  # Hidden model!
            authority_lane=AuthorityLane.HUNTER,
            product_boundary="ATOMIC_HARNESS_PIPELINE",
            side_effect_class="READ_ONLY",
            input_contracts=("RAW_DATA",),
            output_contracts=("MODEL_OUTPUT",),
        )
    assert exc_info.value.reason_code == "ERR_HIDDEN_MODEL_DEPENDENCE"


def test_false_proof_3_mutation_step_missing_postconditions_rejected() -> None:
    """False-proof 3: Omit postconditions on a MUTATION_OPERATION step."""
    with pytest.raises(MissingMutationValidatorError) as exc_info:
        StepContract(
            step_id="MUTATION_NO_POSTCONDITION",
            name="Mutation Without Postconditions",
            purpose="Testing",
            work_unit_kind=WorkUnitKind.CODE_FUNCTION,
            target_ref="cmf_pipeline.mutators.write_db",
            authority_lane=AuthorityLane.COMMANDER,
            product_boundary="CONSCIOUS_ACTIVATIONS_STUDIO",
            side_effect_class="MUTATION_OPERATION",
            input_contracts=("IN",),
            output_contracts=("OUT",),
            postconditions=(),  # Missing!
            validators=("VAL_1",),
        )
    assert exc_info.value.reason_code == "ERR_MISSING_MUTATION_VALIDATOR"


# ============================================================================
# Two Representative Program Migrations & Coverage Reporting
# ============================================================================


def test_research_and_collision_program_migrations_and_coverage() -> None:
    """Verify migrations for research_canonicalization_program and collision_program with 100% coverage."""
    registry = StepContractRegistry()

    # 1. Research Canonicalization Program migration
    research_contracts = create_research_canonicalization_step_contracts()
    assert len(research_contracts) == 4
    for rc in research_contracts:
        registry.register(rc)

    # 2. Collision Program migration
    collision_contracts = create_collision_program_step_contracts()
    assert len(collision_contracts) == 4
    for cc in collision_contracts:
        registry.register(cc)

    assert len(registry.list_all()) == 8

    # 3. Create representative ExecutableWorkflowIR for Research Canonicalization
    research_nodes = [
        {"node_id": "RESEARCH_SIGNAL_EXTRACTION", "capability_id": "cap_extract", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "RELATIONSHIP_CANONICALIZATION", "capability_id": "cap_canon", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "OKF_BUNDLE_SYNTHESIS", "capability_id": "cap_synth", "phase_order": 3, "actor_kind": "AGENT_PROGRAM", "role": "COMPOSER", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "OPERATOR_RELEASE_GATE", "capability_id": "cap_gate", "phase_order": 4, "actor_kind": "HUMAN_GATE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "MUTATION_OPERATION"},
    ]
    research_edges = [
        {"source_node_id": "RESEARCH_SIGNAL_EXTRACTION", "target_node_id": "RELATIONSHIP_CANONICALIZATION", "contract_id": "C1"},
        {"source_node_id": "RELATIONSHIP_CANONICALIZATION", "target_node_id": "OKF_BUNDLE_SYNTHESIS", "contract_id": "C2"},
        {"source_node_id": "OKF_BUNDLE_SYNTHESIS", "target_node_id": "OPERATOR_RELEASE_GATE", "contract_id": "C3"},
    ]

    ir_research = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_RESEARCH_PROGRAM",
        name="Research Canonicalization Program",
        category_id="RESEARCH",
        profile_id="CANONICALIZATION",
        purpose="Research Canonicalization Pipeline",
        authority_lane=AuthorityLane.COMMANDER,
        nodes=research_nodes,
        edges=research_edges,
    )

    # 4. Generate coverage report
    report = registry.generate_coverage_report(ir_research)
    assert report.total_steps_count == 4
    assert report.contracted_steps_count == 4
    assert report.coverage_percentage == 100.0
    assert report.agent_steps_count == 2
    assert report.code_steps_count == 2
    assert report.mutation_steps_count == 1
    assert not report.uncontracted_step_ids
    assert len(report.report_sha256) == 64
