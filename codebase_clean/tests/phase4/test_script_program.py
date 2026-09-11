"""
test_script_program.py
-----------------------
Phase 4 Mandate M40 Acceptance Suite:
Script Program Runtime — Governed JIT Authoring, Semantic QA, Backend-Authoritative Operator Approval, and Activation Transfer Contracts.

Governing Standards:
- CAE Phase 4 Mandate M40
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
- FR-APP-032 Script Approval and Transfer Contract Invariants
"""

from __future__ import annotations

import hashlib
import uuid
import pytest
from typing import Any, Dict, List

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import (
    ProgramPackage,
    get_program_registry,
)
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateRuntimeError,
    UniversalProgramStateRuntime,
    get_canonical_script_state_machine,
)
from ca_runtime.state_lifecycle import CausalTraceLedger
from ca_runtime.hook_runtime import (
    OperatorGateRuntimeEngine,
    SelfApprovalProhibitedError,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    tenant_scope,
)
from ca_runtime.script_program import (
    ActivationTransferContract,
    EvidenceQuoteMismatchError,
    FinalScriptApprovalReceipt,
    FinalScriptPackage,
    JITAuthoringRequest,
    JITAuthoringRequestNotFoundError,
    ScriptAlreadyApprovedError,
    ScriptIntegrityError,
    ScriptNotApprovedError,
    ScriptNotFoundError,
    ScriptProgramCoordinator,
    ScriptProgramError,
    ScriptProposal,
    ScriptProposalNotFoundError,
    ScriptSegment,
    SemanticQAFailureError,
    SemanticQAReceipt,
)


# ---------------------------------------------------------------------------
# Authentic Jean Pierre (03_50-12) Fixture Data
# ---------------------------------------------------------------------------

JEAN_PIERRE_SEGMENTS = [
    {
        "segment_id": "seg-001",
        "scene_number": 1,
        "speaker": "Jean Pierre",
        "spoken_text": "We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.",
        "start_time_ms": 0,
        "end_time_ms": 4800,
        "source_evidence_ref": {"object_id": "turn-001", "version": "1.0.0", "sha256": hashlib.sha256("We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.".encode()).hexdigest()},
        "quote_sha256": hashlib.sha256("We were running thirty thousand units a day through the line, and seventy percent of our defect alerts were completely false.".encode()).hexdigest(),
    },
    {
        "segment_id": "seg-002",
        "scene_number": 2,
        "speaker": "Jean Pierre",
        "spoken_text": "Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.",
        "start_time_ms": 4800,
        "end_time_ms": 10500,
        "source_evidence_ref": {"object_id": "turn-002", "version": "1.0.0", "sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode()).hexdigest()},
        "quote_sha256": hashlib.sha256("Operators were fatigued. They started muting the audio alarms just to keep their sanity during the twelve-hour night shift.".encode()).hexdigest(),
    },
    {
        "segment_id": "seg-003",
        "scene_number": 3,
        "speaker": "Jean Pierre",
        "spoken_text": "That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.",
        "start_time_ms": 10500,
        "end_time_ms": 16200,
        "source_evidence_ref": {"object_id": "turn-003", "version": "1.0.0", "sha256": hashlib.sha256("That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.".encode()).hexdigest()},
        "quote_sha256": hashlib.sha256("That's when we deployed the edge computer vision model directly on the conveyor cameras to filter noise before it reached human ears.".encode()).hexdigest(),
    },
]

WORKSPACE_ID = "00000000-0000-0000-0000-000000000003"
WORKSPACE_ID_A = "00000000-0000-0000-0000-00000000000a"
WORKSPACE_ID_B = "00000000-0000-0000-0000-00000000000b"
SCRIPT_ID = "script-03-50-12-v1"


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

class TestScriptProgramRuntime:

    def setup_method(self) -> None:
        self.store = InMemoryProgramStateStore()
        self.runtime = UniversalProgramStateRuntime(store=self.store)
        self.ledger = CausalTraceLedger()
        self.operator_gate = OperatorGateRuntimeEngine()
        self.coordinator = ScriptProgramCoordinator(
            runtime=self.runtime,
            ledger=self.ledger,
            operator_gate=self.operator_gate,
            store=self.store,
        )

    def test_script_program_manifest_registration(self) -> None:
        """Verify program manifest discovery, schema compliance, and skill registration."""
        registry = get_program_registry()
        pkg = registry.get_program("script_program")
        assert pkg is not None
        assert pkg.manifest.id == "script_program"
        assert pkg.manifest.version == "1.0.0"
        assert pkg.manifest.harness == "SCRIPT_HARNESS_V1"
        assert "HUNTER" in pkg.manifest.lanes
        assert "COMPOSER" in pkg.manifest.lanes
        assert "ANALYST" in pkg.manifest.lanes
        assert "COMMANDER" in pkg.manifest.lanes
        assert len(pkg.manifest.skills) >= 1
        assert pkg.manifest.skills[0].name == "script_generation"

    def test_script_program_canonical_state_machine(self) -> None:
        """Verify canonical state machine transitions and triggers."""
        sm = get_canonical_script_state_machine()
        assert sm.program_id == "script_program"
        assert sm.initial_state == "INITIAL"
        assert "request_jit_authoring" in sm.transitions
        assert "propose_script" in sm.transitions
        assert "evaluate_semantic_qa" in sm.transitions
        assert "compile_final_script" in sm.transitions
        assert "approve_script" in sm.transitions
        assert "create_transfer_contract" in sm.transitions
        assert "revise_script" in sm.transitions
        assert "repair_script" in sm.repair_transitions

    def test_script_program_e2e_authentic_lifecycle(self) -> None:
        """Complete end-to-end governed lifecycle from JIT admission to approved transfer contract."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            # 1. Initialize session
            agg = self.coordinator.initialize_script_session(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
            )
            assert agg.current_state == "INITIAL"

            # 2. HUNTER Lane: Admit context via JIT Authoring Request
            req = self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-001",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
                actor_id="hunter-001",
            )
            assert req.request_id == "jit-req-001"
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "JIT_REQUESTED"

            # 3. COMPOSER Lane: Propose Script Candidate
            proposal = self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-001",
                request_id="jit-req-001",
                title="Jean Pierre — Conveyor Edge Filtering",
                scenes=[
                    {"scene_id": "sc-1", "heading": "Factory Floor Noise Problem"},
                    {"scene_id": "sc-2", "heading": "Alarm Fatigue Breakdown"},
                    {"scene_id": "sc-3", "heading": "Edge Camera Filtration Deployment"},
                ],
                lane=AuthorityLane.COMPOSER,
                actor_id="composer-001",
            )
            assert proposal.proposal_id == "prop-001"
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SCRIPT_PROPOSED"

            # 4. ANALYST Lane: Semantic QA Evaluation (PASS)
            receipt_qa = self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-001",
                proposal_id="prop-001",
                evaluator_id="eval-analyst-01",
                voice_dna_adherence=True,
                forbidden_centroids_avoided=True,
                wrong_reading_locks_preserved=True,
                quote_integrity_verified=True,
                lane=AuthorityLane.ANALYST,
                actor_id="analyst-001",
            )
            assert receipt_qa.verdict == "PASS"
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SEMANTIC_QA_EVALUATED"

            # 5. COMPOSER Lane: Compile Final Script Package
            script = self.coordinator.compile_final_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-001",
                qa_receipt_id="qa-rcpt-001",
                version="1.0.0",
                revision=1,
                segments=JEAN_PIERRE_SEGMENTS,
                lane=AuthorityLane.COMPOSER,
                actor_id="composer-001",
            )
            assert script.script_id == SCRIPT_ID
            assert script.operator_approved is False
            assert script.composition_eligible is False
            assert script.script_sha256 == canonical_sha256(JEAN_PIERRE_SEGMENTS)
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SCRIPT_COMPILED"

            # 6. COMMANDER Lane: Authoritative Operator Gate Approval
            approval_receipt, approved_script = self.coordinator.approve_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="appr-rcpt-001",
                operator_id="operator-director-marie",
                operator_decision_ref={"object_id": "dec-001", "version": "1.0.0", "sha256": "d001"},
                rationale="Authentic narrative structure approved for production transfer.",
                lane=AuthorityLane.COMMANDER,
                requester_id="composer-001",  # Different from operator_id
            )
            assert approval_receipt.decision == "APPROVE"
            assert approved_script.operator_approved is True
            assert approved_script.composition_eligible is True
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SCRIPT_APPROVED"

            # 7. COMMANDER Lane: Activation Transfer Contract
            contract = self.coordinator.create_transfer_contract(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                contract_id="contract-xfer-001",
                selected_hypothesis_ref={"object_id": "hyp-001", "version": "1.0.0", "sha256": "h001"},
                must_survive_properties=["speaker_authenticity", "verbatim_quotes"],
                transformation_rules=["preserve_sfl_register"],
                lane=AuthorityLane.COMMANDER,
                actor_id="commander-operator",
            )
            assert contract.contract_id == "contract-xfer-001"
            assert contract.lifecycle_state == "approved"
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "TRANSFER_CONTRACT_CREATED"

            # 8. Verify Causal Trace records with SHA-256 chain integrity
            events = self.ledger.get_traces_for_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert len(events) >= 6
            for idx in range(1, len(events)):
                assert events[idx].previous_trace_sha256 == events[idx - 1].trace_sha256

    def test_transfer_contract_blocked_without_operator_approval(self) -> None:
        """NON-NEGOTIABLE: Transfer contract creation fails closed if script is unapproved."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-002",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )
            self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-002",
                request_id="jit-req-002",
                title="Unapproved Candidate",
                scenes=[{"scene_id": "sc-1", "heading": "Test Scene"}],
                lane=AuthorityLane.COMPOSER,
            )
            self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-002",
                proposal_id="prop-002",
                evaluator_id="eval-01",
                lane=AuthorityLane.ANALYST,
            )
            self.coordinator.compile_final_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-002",
                qa_receipt_id="qa-rcpt-002",
                segments=JEAN_PIERRE_SEGMENTS,
                lane=AuthorityLane.COMPOSER,
            )

            # Attempt transfer WITHOUT approval -> MUST FAIL CLOSED
            with pytest.raises(ScriptNotApprovedError) as exc_info:
                self.coordinator.create_transfer_contract(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    contract_id="contract-xfer-unapproved",
                    selected_hypothesis_ref={"object_id": "hyp-001", "version": "1.0.0", "sha256": "h001"},
                    lane=AuthorityLane.COMMANDER,
                )
            assert "is not approved by an operator" in str(exc_info.value)
            assert exc_info.value.reason_code == "SCRIPT_NOT_APPROVED"

    def test_script_revision_versioning_and_approval_reset(self) -> None:
        """Governed revision creates v2 proposal with explicit parent hash, resetting approval status."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            # Setup approved v1
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-003",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )
            self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-003",
                request_id="jit-req-003",
                title="v1 Proposal",
                scenes=[{"scene_id": "sc-1", "heading": "v1 Scene"}],
                lane=AuthorityLane.COMPOSER,
            )
            self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-003",
                proposal_id="prop-003",
                evaluator_id="eval-01",
                lane=AuthorityLane.ANALYST,
            )
            v1_script = self.coordinator.compile_final_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-003",
                qa_receipt_id="qa-rcpt-003",
                version="1.0.0",
                revision=1,
                segments=JEAN_PIERRE_SEGMENTS,
                lane=AuthorityLane.COMPOSER,
            )
            self.coordinator.approve_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="appr-rcpt-003",
                operator_id="operator-marie",
                operator_decision_ref={"object_id": "dec-003", "version": "1.0.0", "sha256": "d003"},
                lane=AuthorityLane.COMMANDER,
                requester_id="composer-001",
            )

            # REVISE script to v2 (Composer)
            v2_proposal = self.coordinator.revise_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                new_proposal_id="prop-003-v2",
                new_title="v2 Proposal with Revised Ending",
                new_scenes=[{"scene_id": "sc-1", "heading": "v2 Scene"}],
                rationale="Editorial feedback requires tighter scene 3 focus.",
                lane=AuthorityLane.COMPOSER,
            )
            assert v2_proposal.proposal_id == "prop-003-v2"
            assert v2_proposal.rejected_alternative_refs[0]["sha256"] == v1_script.script_sha256

            # State aggregate is reset to SCRIPT_PROPOSED
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SCRIPT_PROPOSED"

            # Pass new QA for v2
            self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-003-v2",
                proposal_id="prop-003-v2",
                evaluator_id="eval-01",
                lane=AuthorityLane.ANALYST,
            )

            # Compile v2 script
            v2_script = self.coordinator.compile_final_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-003-v2",
                qa_receipt_id="qa-rcpt-003-v2",
                version="2.0.0",
                revision=2,
                segments=JEAN_PIERRE_SEGMENTS,
                supersedes_ref=v1_script.immutable_ref(),
                lane=AuthorityLane.COMPOSER,
            )
            assert v2_script.version == "2.0.0"
            assert v2_script.revision == 2
            assert v2_script.operator_approved is False
            assert v2_script.supersedes_ref == v1_script.immutable_ref()

            # Transfer contract attempt before approving v2 must fail
            with pytest.raises(ScriptNotApprovedError):
                self.coordinator.create_transfer_contract(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    contract_id="contract-xfer-v2-premature",
                    selected_hypothesis_ref={"object_id": "hyp-001", "version": "1.0.0", "sha256": "h001"},
                    lane=AuthorityLane.COMMANDER,
                )

            # Authoritative approval for v2
            self.coordinator.approve_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="appr-rcpt-003-v2",
                operator_id="operator-marie",
                operator_decision_ref={"object_id": "dec-003-v2", "version": "1.0.0", "sha256": "d003-v2"},
                lane=AuthorityLane.COMMANDER,
                requester_id="composer-001",
            )

            # Transfer contract creation on v2 now succeeds
            contract_v2 = self.coordinator.create_transfer_contract(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                contract_id="contract-xfer-v2",
                selected_hypothesis_ref={"object_id": "hyp-001", "version": "1.0.0", "sha256": "h001"},
                lane=AuthorityLane.COMMANDER,
            )
            assert contract_v2.final_script_ref["version"] == "2.0.0"

    def test_semantic_qa_rejection_blocks_compilation(self) -> None:
        """Semantic QA violations (forbidden centroids, voice DNA drift) fail closed."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-004",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )
            self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-004",
                request_id="jit-req-004",
                title="Bad Candidate",
                scenes=[{"scene_id": "sc-1", "heading": "Violating Scene"}],
                lane=AuthorityLane.COMPOSER,
            )

            # Semantic QA fails with Voice DNA drift and forbidden centroid collision
            with pytest.raises(SemanticQAFailureError) as exc_info:
                self.coordinator.evaluate_semantic_qa(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    receipt_id="qa-rcpt-004-fail",
                    proposal_id="prop-004",
                    evaluator_id="eval-01",
                    voice_dna_adherence=False,
                    forbidden_centroids_avoided=False,
                    lane=AuthorityLane.ANALYST,
                )
            assert "VOICE_DNA_DRIFT_DETECTED" in exc_info.value.violations
            assert "FORBIDDEN_CENTROID_COLLISION" in exc_info.value.violations

            # Aggregate remains in SCRIPT_PROPOSED state
            agg = self.store.get_aggregate(f"prog:script_program:{WORKSPACE_ID}:{SCRIPT_ID}")
            assert agg.current_state == "SCRIPT_PROPOSED"

    def test_spoken_quote_tamper_detection(self) -> None:
        """Tampered spoken text or corrupt quote checksum triggers EvidenceQuoteMismatchError."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-005",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )
            self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-005",
                request_id="jit-req-005",
                title="Tampered Candidate",
                scenes=[{"scene_id": "sc-1", "heading": "Scene 1"}],
                lane=AuthorityLane.COMPOSER,
            )
            self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-005",
                proposal_id="prop-005",
                evaluator_id="eval-01",
                lane=AuthorityLane.ANALYST,
            )

            tampered_segments = [
                {
                    "segment_id": "seg-tampered",
                    "scene_number": 1,
                    "speaker": "Jean Pierre",
                    "spoken_text": "We completely fabricated this fake quote.",
                    "start_time_ms": 0,
                    "end_time_ms": 4000,
                    "quote_sha256": "invalid_corrupted_hash_value_12345",
                }
            ]

            with pytest.raises(EvidenceQuoteMismatchError) as exc_info:
                self.coordinator.compile_final_script(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    proposal_id="prop-005",
                    qa_receipt_id="qa-rcpt-005",
                    segments=tampered_segments,
                    lane=AuthorityLane.COMPOSER,
                )
            assert exc_info.value.reason_code == "EVIDENCE_QUOTE_MISMATCH"

    def test_anti_self_approval_gate(self) -> None:
        """Requester cannot self-approve their own script package."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-006",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )
            self.coordinator.propose_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-006",
                request_id="jit-req-006",
                title="Self Approval Candidate",
                scenes=[{"scene_id": "sc-1", "heading": "Scene 1"}],
                lane=AuthorityLane.COMPOSER,
            )
            self.coordinator.evaluate_semantic_qa(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                receipt_id="qa-rcpt-006",
                proposal_id="prop-006",
                evaluator_id="eval-01",
                lane=AuthorityLane.ANALYST,
            )
            self.coordinator.compile_final_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                proposal_id="prop-006",
                qa_receipt_id="qa-rcpt-006",
                segments=JEAN_PIERRE_SEGMENTS,
                lane=AuthorityLane.COMPOSER,
            )

            # Same user as requester and operator
            with pytest.raises(SelfApprovalProhibitedError) as exc_info:
                self.coordinator.approve_script(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    receipt_id="appr-rcpt-006",
                    operator_id="operator-alex",
                    operator_decision_ref={"object_id": "dec-006", "version": "1.0.0", "sha256": "d006"},
                    lane=AuthorityLane.COMMANDER,
                    requester_id="operator-alex",  # SELF-APPROVAL ATTEMPT
                )
            assert "SELF_APPROVAL_PROHIBITED" in str(exc_info.value)

    def test_authority_lane_enforcement(self) -> None:
        """Operations executed in wrong authority lanes are rejected immediately."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            # Hunter trying to propose script -> fails
            with pytest.raises(ProgramAuthorityLaneViolationError):
                self.coordinator.propose_script(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    proposal_id="prop-lane-fail",
                    request_id="req-1",
                    title="Title",
                    scenes=[],
                    lane=AuthorityLane.HUNTER,  # Wrong lane!
                )

            # Composer trying to evaluate QA -> fails
            with pytest.raises(ProgramAuthorityLaneViolationError):
                self.coordinator.evaluate_semantic_qa(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    receipt_id="rcpt-lane-fail",
                    proposal_id="prop-1",
                    evaluator_id="eval-1",
                    lane=AuthorityLane.COMPOSER,  # Wrong lane!
                )

            # Analyst trying to approve script -> fails
            with pytest.raises(ProgramAuthorityLaneViolationError):
                self.coordinator.approve_script(
                    workspace_id=WORKSPACE_ID,
                    script_id=SCRIPT_ID,
                    receipt_id="appr-lane-fail",
                    operator_id="op-1",
                    operator_decision_ref={"object_id": "d1", "version": "1.0.0", "sha256": "h1"},
                    lane=AuthorityLane.ANALYST,  # Wrong lane!
                )

    def test_cross_workspace_isolation(self) -> None:
        """Operations targeting different workspaces than active tenant context fail closed."""
        tenant_a = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID_A), actor_id="op-a")
        with tenant_scope(tenant_a):
            with pytest.raises(CrossWorkspaceLeakError):
                self.coordinator.initialize_script_session(
                    workspace_id=WORKSPACE_ID_B,  # LEAK ATTEMPT
                    script_id=SCRIPT_ID,
                )

    def test_state_recovery_and_repair(self) -> None:
        """Repair transitions route through REPAIRING state back to JIT_REQUESTED."""
        tenant = TenantContext(workspace_id=uuid.UUID(WORKSPACE_ID), actor_id="op-admin")
        with tenant_scope(tenant):
            self.coordinator.request_jit_authoring(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                request_id="jit-req-007",
                program_ref={"object_id": "prog-sem-03", "version": "1.0.0", "sha256": "hash001"},
                voice_dna_ref={"object_id": "vdna-jp", "version": "1.0.0", "sha256": "vdna001"},
                role_tension_ref={"object_id": "tension-jp", "version": "1.0.0", "sha256": "t001"},
                primitive_coalition_ref={"object_id": "prim-jp", "version": "1.0.0", "sha256": "p001"},
                archetype_coalition_ref={"object_id": "arch-jp", "version": "1.0.0", "sha256": "a001"},
                lane=AuthorityLane.HUNTER,
            )

            # Recover to REPAIRING
            recovered = self.coordinator.recover_to_repairing(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                reason="Corrupt upstream context detected during generation",
                lane=AuthorityLane.COMMANDER,
            )
            assert recovered.current_state == "REPAIRING"

            # Execute repair back to JIT_REQUESTED
            repaired = self.coordinator.repair_script(
                workspace_id=WORKSPACE_ID,
                script_id=SCRIPT_ID,
                repair_action="Re-fetch authentic interview evidence",
                lane=AuthorityLane.COMMANDER,
            )
            assert repaired.current_state == "JIT_REQUESTED"
