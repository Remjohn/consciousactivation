"""Authoritative unit and integration tests for CAE M25: Workspace + Guest Operating Context Program.

Governed by:
- Phase 3 Mandate M25 (03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M25_workspace_guest_operating_context_program.md)
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- CA-CAN-01A_WORKSPACE.yaml & CA-CAN-01B_GUEST.yaml
- SPEC-TWC-UI-001 & SPEC-GST-UI-001
- Live PostgreSQL/RLS Tenancy Authority (TS-CAE-TEN-001)
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_registry import (
    ProgramPackage,
    ProgramRegistry,
    ProgramStatus,
)
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_workspace_guest_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceEventType,
    CausalTraceLedger,
    HookRejectionError,
    StateLifecycleCoordinator,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyViolationError,
)
from ca_runtime.workspace_guest_program import (
    DerivedBrandContext,
    GuestEvidenceIntegrityError,
    GuestEvidenceItem,
    GuestNotRegisteredError,
    LineageMissingError,
    SingleActiveGuestViolationError,
    WorkspaceGuestContextSnapshot,
    WorkspaceGuestProgramCoordinator,
    WorkspaceGuestProgramError,
    WorkspaceScopeViolationError,
    PROGRAM_ID,
)


# ============================================================================
# 1. Package Discovery & State Machine Grammar Tests
# ============================================================================

def test_workspace_guest_program_package_discovery_and_manifest() -> None:
    """Verifies that ProgramRegistry discovers and validates workspace_guest_program package."""
    registry = ProgramRegistry(discovery_roots=[Path("programs")])
    registry.discover()
    pkg: ProgramPackage = registry.get_program(PROGRAM_ID)
    
    assert pkg.program_id == PROGRAM_ID
    assert pkg.version == "1.0.0"
    assert pkg.manifest.status == ProgramStatus.ACTIVE
    assert pkg.manifest.state_machine == "WORKSPACE_GUEST_STATE_MACHINE_V1"
    
    # Verify lanes
    assert "COMMANDER" in pkg.manifest.lanes
    assert "HUNTER" in pkg.manifest.lanes
    assert "ANALYST" in pkg.manifest.lanes
    
    # Verify passive flat skills
    skill_names = [s.name for s in pkg.manifest.skills]
    assert "workspace_boundary_verifier" in skill_names
    assert "guest_evidence_indexer" in skill_names
    assert "brand_context_deriver" in skill_names
    
    # Verify composite SHA-256 package hash
    assert len(pkg.package_sha256) == 64
    assert len(pkg.manifest_sha256) == 64


def test_workspace_guest_state_machine_definition() -> None:
    """Verifies grammar and transition rules of WORKSPACE_GUEST_STATE_MACHINE_V1."""
    sm = get_canonical_workspace_guest_state_machine()
    assert sm.machine_id == "WORKSPACE_GUEST_STATE_MACHINE_V1"
    assert sm.program_id == PROGRAM_ID
    assert sm.initial_state == "INITIAL"
    assert sm.terminal_states == {"CONTEXT_ACTIVE"}
    
    expected_transitions = {
        "configure_workspace",
        "register_guest",
        "bind_guest_evidence",
        "activate_guest_context",
    }
    assert set(sm.transitions.keys()) == expected_transitions
    assert "repair_context" in sm.repair_transitions
    
    # Check transition lanes
    assert sm.transitions["configure_workspace"].required_lane == AuthorityLane.COMMANDER
    assert sm.transitions["register_guest"].required_lane == AuthorityLane.HUNTER
    assert sm.transitions["bind_guest_evidence"].required_lane == AuthorityLane.ANALYST
    assert sm.transitions["activate_guest_context"].required_lane == AuthorityLane.COMMANDER
    assert sm.repair_transitions["repair_context"].required_lane == AuthorityLane.COMMANDER


# ============================================================================
# 2. End-to-End Program Lifecycle Tests
# ============================================================================

def test_full_lifecycle_initial_to_active_context() -> None:
    """Tests the full progression: INITIAL -> WORKSPACE_CONFIGURED -> GUEST_REGISTERED -> EVIDENCE_BOUND -> CONTEXT_ACTIVE."""
    workspace_id = uuid4()
    operator_grant_id = uuid4()
    context_commander = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_commander_01",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id=operator_grant_id,
    )
    context_hunter = TenantContext(
        workspace_id=workspace_id,
        actor_id="hunter_scout_01",
        role="MEMBER",
    )
    context_analyst = TenantContext(
        workspace_id=workspace_id,
        actor_id="analyst_curator_01",
        role="MEMBER",
    )

    coordinator = WorkspaceGuestProgramCoordinator()

    # Step 1: Initialize Program State Aggregate
    aggregate = coordinator.initialize_program(
        workspace_id=workspace_id,
        actor_id="operator_commander_01",
    )
    assert aggregate.current_state == "INITIAL"
    assert aggregate.version == 1
    assert aggregate.lifecycle == ProgramStateLifecycle.INITIALIZED

    # Step 2: Configure Workspace (COMMANDER)
    res_conf = coordinator.configure_workspace(
        aggregate_id=aggregate.aggregate_id,
        display_name="Enterprise Alpha Activation",
        config={"isolation_level": "STRICT_RLS", "encryption": "AES_GCM_256"},
        context=context_commander,
        idempotency_key="idemp_conf_001",
    )
    assert res_conf.aggregate.current_state == "WORKSPACE_CONFIGURED"
    assert res_conf.aggregate.version == 2
    assert res_conf.receipt_id.startswith("rcpt_")

    # Step 3: Register Single Active Guest (HUNTER)
    res_guest = coordinator.register_guest(
        aggregate_id=aggregate.aggregate_id,
        pseudonym="Jean-Pierre Luminary",
        external_reference_id="crm_cust_8871",
        consent_status="EXPLICIT_CONSENT_GRANTED",
        context=context_hunter,
        idempotency_key="idemp_guest_001",
    )
    assert res_guest.aggregate.current_state == "GUEST_REGISTERED"
    assert res_guest.aggregate.version == 3
    guest_id = res_guest.aggregate.state_data["active_guest_id"]
    assert guest_id.startswith("gst_")

    # Step 4: Bind Guest Evidence (ANALYST)
    raw_audio_bytes = b"sample audio recording of Jean-Pierre keynote 2026"
    audio_sha256 = hashlib.sha256(raw_audio_bytes).hexdigest()
    raw_transcript_bytes = b"sample transcript text of Jean-Pierre keynote"
    transcript_sha256 = hashlib.sha256(raw_transcript_bytes).hexdigest()

    evidence_items = [
        GuestEvidenceItem(
            evidence_id="ev_audio_001",
            source_url="s3://conscious-vault/audio/jp_keynote.m4a",
            content_type="audio/mp4",
            sha256_digest=audio_sha256,
            metadata={"duration_seconds": 1840, "sample_rate": 48000},
        ),
        GuestEvidenceItem(
            evidence_id="ev_transcript_001",
            source_url="s3://conscious-vault/transcripts/jp_keynote.json",
            content_type="application/json",
            sha256_digest=transcript_sha256,
            metadata={"word_count": 4520, "language": "en-US"},
        ),
    ]

    res_evidence = coordinator.bind_guest_evidence(
        aggregate_id=aggregate.aggregate_id,
        guest_id=guest_id,
        evidence_items=evidence_items,
        context=context_analyst,
        idempotency_key="idemp_ev_001",
    )
    assert res_evidence.aggregate.current_state == "EVIDENCE_BOUND"
    assert res_evidence.aggregate.version == 4
    assert len(res_evidence.aggregate.state_data["evidence_items"]) == 2

    # Step 5: Derive Subordinate Persona/Brand Context with Lineage
    brand_context = coordinator.derive_brand_context(
        aggregate_id=aggregate.aggregate_id,
        guest_id=guest_id,
        tone_attributes=["Visionary", "Pragmatic", "Provocative"],
        voice_archetype="The Maverick Architect",
        visual_theme="Minimal Monochrome with Neon Amber Accents",
        source_evidence_hashes=[audio_sha256, transcript_sha256],
        context=context_analyst,
    )
    assert brand_context.brand_id.startswith("brand_")
    assert brand_context.guest_id == guest_id
    assert len(brand_context.lineage_sha256) == 64

    # Step 6: Activate Operating Context (COMMANDER)
    res_activate = coordinator.activate_guest_context(
        aggregate_id=aggregate.aggregate_id,
        guest_id=guest_id,
        context=context_commander,
        idempotency_key="idemp_act_001",
    )
    assert res_activate.aggregate.current_state == "CONTEXT_ACTIVE"
    assert res_activate.aggregate.version == 5
    assert res_activate.aggregate.lifecycle == ProgramStateLifecycle.COMPLETED

    # Step 7: Inspect Snapshot
    snapshot: WorkspaceGuestContextSnapshot = coordinator.get_context_snapshot(aggregate.aggregate_id)
    assert snapshot.workspace_id == str(workspace_id)
    assert snapshot.workspace_name == "Enterprise Alpha Activation"
    assert snapshot.current_state == "CONTEXT_ACTIVE"
    assert snapshot.active_guest_id == guest_id
    assert snapshot.active_guest_pseudonym == "Jean-Pierre Luminary"
    assert snapshot.active_guest_consent == "EXPLICIT_CONSENT_GRANTED"
    assert snapshot.evidence_count == 2
    assert snapshot.derived_brand_context is not None
    assert snapshot.derived_brand_context.voice_archetype == "The Maverick Architect"
    assert snapshot.version == 5


# ============================================================================
# 3. One-Workspace / One-Active-Guest Invariant Tests
# ============================================================================

def test_single_active_guest_enforcement_fail_closed() -> None:
    """Proves that attempting to register or activate a second concurrent guest fails closed."""
    workspace_id = uuid4()
    context = TenantContext(workspace_id=workspace_id, actor_id="lead_operator")
    coordinator = WorkspaceGuestProgramCoordinator()

    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="lead_operator")
    coordinator.configure_workspace(
        aggregate_id=agg.aggregate_id,
        display_name="Single Guest Isolation Workspace",
        context=context,
    )

    # Register first guest
    res_1 = coordinator.register_guest(
        aggregate_id=agg.aggregate_id,
        pseudonym="Guest Alpha",
        guest_id="gst_alpha_001",
        context=context,
    )
    assert res_1.aggregate.state_data["active_guest_id"] == "gst_alpha_001"

    # Attempting to register another guest on the same aggregate must raise SingleActiveGuestViolationError
    with pytest.raises(SingleActiveGuestViolationError) as exc_info:
        coordinator.register_guest(
            aggregate_id=agg.aggregate_id,
            pseudonym="Guest Beta",
            guest_id="gst_beta_002",
            context=context,
        )
    assert exc_info.value.active_guest_id == "gst_alpha_001"
    assert exc_info.value.candidate_guest_id == "gst_beta_002"

    # Attempting to bind evidence for a non-active guest must raise SingleActiveGuestViolationError
    raw_bytes = b"sample evidence"
    digest = hashlib.sha256(raw_bytes).hexdigest()
    ev = GuestEvidenceItem(evidence_id="ev_01", source_url="s3://url", content_type="audio/mp3", sha256_digest=digest)
    with pytest.raises(SingleActiveGuestViolationError):
        coordinator.bind_guest_evidence(
            aggregate_id=agg.aggregate_id,
            guest_id="gst_beta_002",
            evidence_items=[ev],
            context=context,
        )


# ============================================================================
# 4. Persona / Brand Context Cryptographic Lineage Tests
# ============================================================================

def test_subordinate_brand_context_lineage_preservation_and_validation() -> None:
    """Proves that Persona/Brand context derivation requires non-empty, verified source hashes."""
    workspace_id = uuid4()
    context = TenantContext(workspace_id=workspace_id, actor_id="curator_alice")
    coordinator = WorkspaceGuestProgramCoordinator()

    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="curator_alice")
    coordinator.configure_workspace(aggregate_id=agg.aggregate_id, display_name="Brand Lineage Workspace", context=context)
    coordinator.register_guest(aggregate_id=agg.aggregate_id, pseudonym="Audrey Stellar", guest_id="gst_audrey_01", context=context)

    audio_hash = hashlib.sha256(b"audrey audio recording").hexdigest()
    ev = GuestEvidenceItem(
        evidence_id="ev_audrey_01",
        source_url="s3://vault/audrey.mp3",
        content_type="audio/mp3",
        sha256_digest=audio_hash,
    )
    coordinator.bind_guest_evidence(
        aggregate_id=agg.aggregate_id,
        guest_id="gst_audrey_01",
        evidence_items=[ev],
        context=context,
    )

    # Negative Case 1: Empty source_evidence_hashes
    with pytest.raises(LineageMissingError) as exc_empty:
        coordinator.derive_brand_context(
            aggregate_id=agg.aggregate_id,
            guest_id="gst_audrey_01",
            tone_attributes=["Authentic", "Daring"],
            voice_archetype="The Witness",
            visual_theme="Deep Indigo & Brass",
            source_evidence_hashes=[],
            context=context,
        )
    assert exc_empty.value.guest_id == "gst_audrey_01"

    # Negative Case 2: Unknown unverified evidence hash
    unverified_hash = hashlib.sha256(b"fabricated evidence").hexdigest()
    with pytest.raises(LineageMissingError) as exc_missing:
        coordinator.derive_brand_context(
            aggregate_id=agg.aggregate_id,
            guest_id="gst_audrey_01",
            tone_attributes=["Authentic", "Daring"],
            voice_archetype="The Witness",
            visual_theme="Deep Indigo & Brass",
            source_evidence_hashes=[audio_hash, unverified_hash],
            context=context,
        )
    assert unverified_hash in exc_missing.value.missing_hashes

    # Positive Case: Verified evidence hashes derive subordinate brand context
    brand_ctx = coordinator.derive_brand_context(
        aggregate_id=agg.aggregate_id,
        guest_id="gst_audrey_01",
        tone_attributes=["Authentic", "Daring"],
        voice_archetype="The Witness",
        visual_theme="Deep Indigo & Brass",
        source_evidence_hashes=[audio_hash],
        context=context,
    )
    assert brand_ctx.guest_id == "gst_audrey_01"
    assert brand_ctx.source_evidence_hashes == (audio_hash,)


# ============================================================================
# 5. Cross-Tenant Isolation & Lane Violation Negative Tests
# ============================================================================

def test_cross_workspace_isolation_denial() -> None:
    """Proves that operations across different workspace boundaries fail closed."""
    ws_a = uuid4()
    ws_b = uuid4()
    ctx_a = TenantContext(workspace_id=ws_a, actor_id="operator_a")
    ctx_b = TenantContext(workspace_id=ws_b, actor_id="operator_b")

    coordinator = WorkspaceGuestProgramCoordinator()
    agg_a = coordinator.initialize_program(workspace_id=ws_a, actor_id="operator_a")

    # Attempting to mutate ws_a aggregate with ws_b tenant context raises CrossWorkspaceLeakError
    with pytest.raises(CrossWorkspaceLeakError):
        coordinator.configure_workspace(
            aggregate_id=agg_a.aggregate_id,
            display_name="Hacked Workspace",
            context=ctx_b,
        )


def test_authority_lane_enforcement() -> None:
    """Proves that executing transitions with unauthorized authority lanes is blocked."""
    workspace_id = uuid4()
    ctx = TenantContext(workspace_id=workspace_id, actor_id="agent_hunter")
    coordinator = WorkspaceGuestProgramCoordinator()

    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="agent_hunter")

    # configure_workspace requires COMMANDER lane. Calling coordinator.lifecycle_coordinator directly
    # with HUNTER lane must fail closed with ProgramAuthorityLaneViolationError or HookRejectionError.
    with pytest.raises((ProgramAuthorityLaneViolationError, HookRejectionError)):
        coordinator.lifecycle_coordinator.execute_state_phase(
            aggregate_id=agg.aggregate_id,
            transition_name="configure_workspace",
            actor_id="agent_hunter",
            actor_lane=AuthorityLane.HUNTER,  # Wrong lane!
            work_fn=lambda _a: {"workspace_configured": True},
            context=ctx,
        )


def test_evidence_integrity_and_guest_unregistered_errors() -> None:
    """Validates negative validation paths for evidence items and unregistered guests."""
    workspace_id = uuid4()
    ctx = TenantContext(workspace_id=workspace_id, actor_id="curator_bob")
    coordinator = WorkspaceGuestProgramCoordinator()

    # Invalid sha256 hash (< 64 chars)
    with pytest.raises(GuestEvidenceIntegrityError):
        GuestEvidenceItem(
            evidence_id="ev_bad",
            source_url="s3://bad",
            content_type="audio/mp3",
            sha256_digest="invalid_short_hash",
        )

    # Empty evidence ID
    with pytest.raises(GuestEvidenceIntegrityError):
        GuestEvidenceItem(
            evidence_id="",
            source_url="s3://bad",
            content_type="audio/mp3",
            sha256_digest=hashlib.sha256(b"test").hexdigest(),
        )

    # Attempting to bind evidence before guest registration
    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="curator_bob")
    coordinator.configure_workspace(aggregate_id=agg.aggregate_id, display_name="Test WS", context=ctx)
    valid_ev = GuestEvidenceItem(
        evidence_id="ev_valid",
        source_url="s3://valid",
        content_type="audio/mp3",
        sha256_digest=hashlib.sha256(b"valid").hexdigest(),
    )
    with pytest.raises(GuestNotRegisteredError):
        coordinator.bind_guest_evidence(
            aggregate_id=agg.aggregate_id,
            guest_id="gst_unregistered",
            evidence_items=[valid_ev],
            context=ctx,
        )


# ============================================================================
# 6. Governed Repair and Concurrency Conflict Tests
# ============================================================================

def test_governed_repair_and_resume_lifecycle() -> None:
    """Tests fault injection -> REPAIRING -> repair_context -> WORKSPACE_CONFIGURED recovery."""
    workspace_id = uuid4()
    ctx = TenantContext(workspace_id=workspace_id, actor_id="operator_repairman")
    coordinator = WorkspaceGuestProgramCoordinator()

    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="operator_repairman")
    coordinator.configure_workspace(aggregate_id=agg.aggregate_id, display_name="Repairable WS", context=ctx)

    # Inject repair state directly into aggregate
    current_agg = coordinator.state_runtime.get_aggregate(agg.aggregate_id)
    repaired_data = dict(current_agg.state_data)
    repaired_agg = ProgramStateAggregate(
        aggregate_id=current_agg.aggregate_id,
        workspace_id=current_agg.workspace_id,
        cae_run_id=current_agg.cae_run_id,
        program_id=current_agg.program_id,
        program_version=current_agg.program_version,
        current_state="REPAIRING",
        state_data=repaired_data,
        version=current_agg.version,
        state_hash=current_agg.state_hash,
        lifecycle=ProgramStateLifecycle.REPAIRING,
        last_receipt_id=current_agg.last_receipt_id,
        created_at=current_agg.created_at,
        updated_at=current_agg.updated_at,
    )
    coordinator.state_runtime.store.save_aggregate(repaired_agg, expected_version=current_agg.version)

    # Execute repair transition
    res_repair = coordinator.repair_context(
        aggregate_id=agg.aggregate_id,
        repair_reason="Recovered from network evidence indexer partition",
        context=ctx,
        idempotency_key="idemp_repair_001",
    )
    assert res_repair.aggregate.current_state == "WORKSPACE_CONFIGURED"
    assert res_repair.aggregate.state_data["last_repair_reason"] == "Recovered from network evidence indexer partition"


def test_optimistic_concurrency_version_conflict() -> None:
    """Tests optimistic concurrency control on concurrent aggregate mutations."""
    workspace_id = uuid4()
    ctx = TenantContext(workspace_id=workspace_id, actor_id="concurrent_operator")
    coordinator = WorkspaceGuestProgramCoordinator()

    agg = coordinator.initialize_program(workspace_id=workspace_id, actor_id="concurrent_operator")
    
    # Mutate to version 2
    coordinator.configure_workspace(aggregate_id=agg.aggregate_id, display_name="WS Ver 2", context=ctx)
    
    # Attempting to save aggregate with stale expected_version=1 raises ProgramStateVersionConflictError
    stale_agg = coordinator.state_runtime.get_aggregate(agg.aggregate_id)
    with pytest.raises(ProgramStateVersionConflictError):
        coordinator.state_runtime.store.save_aggregate(stale_agg, expected_version=1)
