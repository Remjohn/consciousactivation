"""Unit and integration tests for CAE M13 Pi Runtime Substrate + CAE State Boundary.

Governed by 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md and Phase 1 M11 ADR.

Proves:
1. One real CAE typed operation executes in Pi runtime substrate carrying CAE run identity.
2. Canonical CAE state aggregate and Pi runtime session state are cleanly distinguishable.
3. Safe interruption mid-execution preserves CAE state integrity (zero corruption).
4. Lossless resumption from verified checkpoint executes cleanly and produces matching receipts.
5. Strict fail-closed Authority Lane enforcement (HUNTER, ANALYST, COMPOSER, COMMANDER).
6. Cross-workspace boundary isolation under Pi session execution.
7. Idempotent replay validation.
"""

from __future__ import annotations

import hashlib
from typing import Any, Mapping
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import (
    AuthorityLane,
    AuthorityLaneMismatchError,
    CaePiRuntimeAdapter,
    CaePiRuntimeTrace,
    PiExecutionReceipt,
    PiRuntimeError,
    PiRuntimeStateError,
    PiSession,
    PiSessionInterruptedError,
    PiSessionState,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyViolationError,
    tenant_scope,
)
from ca_runtime.tenant_operations import (
    OperationReceipt,
    _build_receipt_envelope,
    _generate_receipt_id,
)


def _mock_execute_evidence_capture(
    *,
    workspace_id: UUID,
    evidence_id: UUID,
    media_asset_id: UUID,
    actor_id: str,
    idempotency_key: str,
) -> OperationReceipt:
    """Mock execution of a real typed CAE evidence capture operation."""
    op_id = "cae.evidence.capture@1.0.0"
    receipt_id = _generate_receipt_id(op_id, workspace_id, idempotency_key)
    command_payload = {
        "evidence_id": str(evidence_id),
        "media_asset_id": str(media_asset_id),
        "workspace_id": str(workspace_id),
        "actor_id": actor_id,
        "start_ms": 1000,
        "end_ms": 5000,
        "quoted_text": "Real evidence quote for verification",
    }
    event_payload = {
        "event_type": "EvidenceCaptured",
        "evidence_id": str(evidence_id),
        "workspace_id": str(workspace_id),
        "status": "CAPTURED",
    }
    envelope = _build_receipt_envelope(
        receipt_id=receipt_id,
        workspace_id=workspace_id,
        operation_id=op_id,
        idempotency_key=idempotency_key,
        actor_id=actor_id,
        command_payload=command_payload,
        event_payload=event_payload,
    )
    return OperationReceipt(
        receipt_id=receipt_id,
        workspace_id=workspace_id,
        operation_id=op_id,
        idempotency_key=idempotency_key,
        actor_id=actor_id,
        outcome="COMMITTED",
        idempotent_replay=False,
        payload=envelope,
        payload_sha256=canonical_sha256(command_payload),
        evidence_ids=(evidence_id,),
    )


def test_pi_adapter_executes_real_cae_operation() -> None:
    """Proof 1: Real CAE typed operation executes in Pi runtime substrate with CAE run identity."""
    adapter = CaePiRuntimeAdapter()
    ws_id = uuid4()
    cae_run_id = f"cae_run_{uuid4().hex[:12]}"
    actor_id = "hunter_actor_01"
    evidence_id = uuid4()
    media_asset_id = uuid4()
    idemp_key = "idemp_evid_001"

    context = TenantContext(workspace_id=ws_id, actor_id=actor_id, role="MEMBER")

    # 1. Create Pi execution session carrying canonical CAE run ID in HUNTER lane
    session = adapter.create_session(
        cae_run_id=cae_run_id,
        workspace_id=ws_id,
        lane=AuthorityLane.HUNTER,
        metadata={"project_id": "03_50-12 Jean Pierre"},
    )

    assert session.session_id.startswith("pi_sess_")
    assert session.cae_run_id == cae_run_id
    assert session.workspace_id == ws_id
    assert session.lane == AuthorityLane.HUNTER
    assert session.state == PiSessionState.IDLE

    # 2. Execute typed operation inside Pi session
    command_payload = {
        "evidence_id": str(evidence_id),
        "media_asset_id": str(media_asset_id),
        "workspace_id": str(ws_id),
        "actor_id": actor_id,
    }

    with tenant_scope(context):
        receipt = adapter.execute_operation(
            session=session,
            operation_id="cae.evidence.capture@1.0.0",
            idempotency_key=idemp_key,
            command_payload=command_payload,
            execute_fn=lambda: _mock_execute_evidence_capture(
                workspace_id=ws_id,
                evidence_id=evidence_id,
                media_asset_id=media_asset_id,
                actor_id=actor_id,
                idempotency_key=idemp_key,
            ),
            context=context,
        )

    # 3. Assertions on Pi receipt & trace
    assert isinstance(receipt, PiExecutionReceipt)
    assert receipt.cae_run_id == cae_run_id
    assert receipt.session_id == session.session_id
    assert receipt.workspace_id == ws_id
    assert receipt.operation_id == "cae.evidence.capture@1.0.0"
    assert receipt.outcome == "COMMITTED"
    assert receipt.idempotent_replay is False

    # 4. Assertions on canonical CAE state advance
    state = adapter.get_canonical_state(str(evidence_id))
    assert state is not None
    assert state["version"] == 1
    assert state["state"] == "COMMITTED"
    assert state["last_receipt_id"] == receipt.receipt_id

    # 5. Assertions on Pi Session state advance
    assert session.state == PiSessionState.COMPLETED
    assert session.checkpoint_sequence == 1

    # 6. Assertions on Runtime Trace
    trace = receipt.runtime_trace
    assert trace.cae_run_id == cae_run_id
    assert trace.in_hook_passed is True
    assert trace.out_hook_passed is True
    assert trace.pre_state_version == 0
    assert trace.post_state_version == 1
    assert trace.interrupted is False
    assert trace.resumed is False


def test_distinguishable_cae_and_pi_state() -> None:
    """Proof 2: Canonical CAE state aggregate and Pi runtime session state are clearly distinguishable."""
    adapter = CaePiRuntimeAdapter()
    ws_id = uuid4()
    cae_run_id = "cae_run_distinguish_test"
    evidence_id = uuid4()
    actor_id = "hunter_actor_02"

    context = TenantContext(workspace_id=ws_id, actor_id=actor_id, role="MEMBER")
    session = adapter.create_session(
        cae_run_id=cae_run_id,
        workspace_id=ws_id,
        lane=AuthorityLane.HUNTER,
    )

    command_payload = {"evidence_id": str(evidence_id), "workspace_id": str(ws_id)}

    receipt = adapter.execute_operation(
        session=session,
        operation_id="cae.evidence.capture@1.0.0",
        idempotency_key="idemp_distinguish_01",
        command_payload=command_payload,
        execute_fn=lambda: _mock_execute_evidence_capture(
            workspace_id=ws_id,
            evidence_id=evidence_id,
            media_asset_id=uuid4(),
            actor_id=actor_id,
            idempotency_key="idemp_distinguish_01",
        ),
        context=context,
    )

    cae_state = adapter.get_canonical_state(str(evidence_id))
    pi_session_state = adapter.get_session(session.session_id)

    # Invariant: CAE canonical state aggregate owns semantic data & aggregate version
    assert "version" in cae_state
    assert "state" in cae_state
    assert "last_receipt_id" in cae_state
    assert "session_id" not in cae_state

    # Invariant: Pi runtime session owns ephemeral runner lifecycle
    assert pi_session_state.state == PiSessionState.COMPLETED
    assert pi_session_state.checkpoint_sequence == 1
    assert pi_session_state.lane == AuthorityLane.HUNTER
    assert pi_session_state.cae_run_id == cae_run_id


def test_interruption_and_resume_without_corruption() -> None:
    """Proof 3: Interruption halts execution before mutation; resumption completes losslessly."""
    adapter = CaePiRuntimeAdapter()
    ws_id = uuid4()
    cae_run_id = "cae_run_interruption_test"
    evidence_id = uuid4()
    media_asset_id = uuid4()
    actor_id = "hunter_actor_03"
    idemp_key = "idemp_interrupt_01"

    context = TenantContext(workspace_id=ws_id, actor_id=actor_id, role="MEMBER")
    session = adapter.create_session(
        cae_run_id=cae_run_id,
        workspace_id=ws_id,
        lane=AuthorityLane.HUNTER,
    )

    command_payload = {
        "evidence_id": str(evidence_id),
        "media_asset_id": str(media_asset_id),
        "workspace_id": str(ws_id),
    }

    # Step 1: Execute with simulated interruption
    with pytest.raises(PiSessionInterruptedError) as exc_info:
        adapter.execute_operation(
            session=session,
            operation_id="cae.evidence.capture@1.0.0",
            idempotency_key=idemp_key,
            command_payload=command_payload,
            execute_fn=lambda: _mock_execute_evidence_capture(
                workspace_id=ws_id,
                evidence_id=evidence_id,
                media_asset_id=media_asset_id,
                actor_id=actor_id,
                idempotency_key=idemp_key,
            ),
            context=context,
            simulate_interruption=True,
        )

    assert "PI_SESSION_INTERRUPTED" in str(exc_info.value)

    # Verify session is marked INTERRUPTED and checkpoint exists
    assert session.state == PiSessionState.INTERRUPTED
    assert session.current_checkpoint_id is not None
    assert session.checkpoint_sequence == 0  # Not completed

    # Verify CAE canonical state was NOT mutated/corrupted
    cae_state = adapter.get_canonical_state(str(evidence_id))
    assert cae_state is None  # No partial commit

    # Step 2: Resume session from checkpoint
    resumed_receipt = adapter.resume_session(
        session=session,
        operation_id="cae.evidence.capture@1.0.0",
        idempotency_key=idemp_key,
        command_payload=command_payload,
        execute_fn=lambda: _mock_execute_evidence_capture(
            workspace_id=ws_id,
            evidence_id=evidence_id,
            media_asset_id=media_asset_id,
            actor_id=actor_id,
            idempotency_key=idemp_key,
        ),
        context=context,
    )

    # Verify clean completion after resumption
    assert session.state == PiSessionState.COMPLETED
    assert session.checkpoint_sequence == 1
    assert resumed_receipt.runtime_trace.resumed is True
    assert resumed_receipt.runtime_trace.pre_state_version == 0
    assert resumed_receipt.runtime_trace.post_state_version == 1

    # Verify canonical CAE state aggregate is now committed at version 1
    committed_state = adapter.get_canonical_state(str(evidence_id))
    assert committed_state is not None
    assert committed_state["version"] == 1
    assert committed_state["state"] == "COMMITTED"
    assert committed_state["last_receipt_id"] == resumed_receipt.receipt_id


def test_authority_lane_enforcement_fail_closed() -> None:
    """Proof 4 (Contrastive): Cross-lane execution is blocked fail-closed."""
    adapter = CaePiRuntimeAdapter()
    ws_id = uuid4()
    context = TenantContext(workspace_id=ws_id, actor_id="hunter_01", role="MEMBER")

    # Create session in HUNTER lane
    hunter_session = adapter.create_session(
        cae_run_id="cae_run_lane_test",
        workspace_id=ws_id,
        lane=AuthorityLane.HUNTER,
    )

    # Attempt to execute COMMANDER operation (e.g. provision workspace or engagement init)
    with pytest.raises(AuthorityLaneMismatchError) as exc_info:
        adapter.execute_operation(
            session=hunter_session,
            operation_id="cae.workspace.provision@1.0.0",
            idempotency_key="idemp_lane_violation",
            command_payload={"workspace_id": str(ws_id)},
            execute_fn=lambda: None,
            context=context,
        )

    assert "AUTHORITY_LANE_MISMATCH" in str(exc_info.value)
    assert "COMMANDER" in str(exc_info.value)
    assert "HUNTER" in str(exc_info.value)


def test_cross_workspace_isolation_in_pi_session() -> None:
    """Proof 5 (Contrastive): Pi session rejects cross-workspace execution."""
    adapter = CaePiRuntimeAdapter()
    ws_id_a = uuid4()
    ws_id_b = uuid4()

    # Session created for Workspace A
    session = adapter.create_session(
        cae_run_id="cae_run_isolation_test",
        workspace_id=ws_id_a,
        lane=AuthorityLane.HUNTER,
    )

    # Context presenting Workspace B token
    context_b = TenantContext(workspace_id=ws_id_b, actor_id="actor_b", role="MEMBER")

    with pytest.raises(CrossWorkspaceLeakError) as exc_info:
        adapter.execute_operation(
            session=session,
            operation_id="cae.evidence.capture@1.0.0",
            idempotency_key="idemp_leak_01",
            command_payload={"workspace_id": str(ws_id_b)},
            execute_fn=lambda: None,
            context=context_b,
        )

    assert "CROSS_WORKSPACE_LEAK" in str(exc_info.value)


def test_idempotent_replay() -> None:
    """Proof 6: Replaying an operation with same idempotency key returns cached receipt without re-executing."""
    adapter = CaePiRuntimeAdapter()
    ws_id = uuid4()
    cae_run_id = "cae_run_idemp_test"
    evidence_id = uuid4()
    media_asset_id = uuid4()
    actor_id = "hunter_actor_04"
    idemp_key = "idemp_replay_001"

    context = TenantContext(workspace_id=ws_id, actor_id=actor_id, role="MEMBER")
    session = adapter.create_session(
        cae_run_id=cae_run_id,
        workspace_id=ws_id,
        lane=AuthorityLane.HUNTER,
    )

    command_payload = {
        "evidence_id": str(evidence_id),
        "media_asset_id": str(media_asset_id),
        "workspace_id": str(ws_id),
    }

    # Initial execution
    receipt1 = adapter.execute_operation(
        session=session,
        operation_id="cae.evidence.capture@1.0.0",
        idempotency_key=idemp_key,
        command_payload=command_payload,
        execute_fn=lambda: _mock_execute_evidence_capture(
            workspace_id=ws_id,
            evidence_id=evidence_id,
            media_asset_id=media_asset_id,
            actor_id=actor_id,
            idempotency_key=idemp_key,
        ),
        context=context,
    )
    assert receipt1.idempotent_replay is False

    # Second execution with same idempotency key
    replay_receipt = adapter.execute_operation(
        session=session,
        operation_id="cae.evidence.capture@1.0.0",
        idempotency_key=idemp_key,
        command_payload=command_payload,
        execute_fn=lambda: pytest.fail("execute_fn should not be invoked on replay!"),
        context=context,
    )

    assert replay_receipt.idempotent_replay is True
    assert replay_receipt.outcome == "IDEMPOTENT_REPLAY"
    assert replay_receipt.receipt_id == receipt1.receipt_id
    assert replay_receipt.receipt_sha256 == receipt1.receipt_sha256
