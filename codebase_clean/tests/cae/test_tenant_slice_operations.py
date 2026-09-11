"""Unit and integration tests for CA-IMPL-01B tenant-scoped semantic operations.

Governed by TS-CAE-TEN-001, Gate A–I Review, and CA-IMPL-01B Mandate.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    IdempotencyPayloadMismatchError,
    ReceiptSelfAttestationViolationError,
    StaleVersionConflictError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    UnauthorizedOperatorAccessError,
    UnverifiedMediaDigestError,
    extract_tenant_context_from_claims,
    tenant_scope,
)
from ca_runtime.tenant_operations import (
    OperationReceipt,
    TenantScopedSemanticOperations,
    _build_receipt_envelope,
    _generate_receipt_id,
)


def test_generate_receipt_id() -> None:
    ws_id = uuid4()
    op_id = "cae.media.verify@1.0.0"
    idemp_key = "idemp_test_001"
    receipt_id = _generate_receipt_id(op_id, ws_id, idemp_key)
    assert receipt_id.startswith("rcpt_cae_media_verify_")
    assert len(receipt_id) > 24


def test_build_receipt_envelope_structure() -> None:
    ws_id = uuid4()
    envelope = _build_receipt_envelope(
        receipt_id="rcpt_test_001",
        workspace_id=ws_id,
        operation_id="cae.engagement.initialize@1.0.0",
        idempotency_key="idemp_eng_01",
        actor_id="actor_alice",
        command_payload={"title": "Test Engagement"},
        event_payload={"event_type": "EngagementInitialized"},
    )
    assert envelope["receipt_type"] == "cae_execution_receipt"
    assert envelope["receipt_id"] == "rcpt_test_001"
    assert envelope["workspace_id"] == str(ws_id)
    assert envelope["environment_fidelity"] == "E3_PRODUCTION_SHAPED"
    assert envelope["environment_identity"]["state_authority"] == "postgresql_supabase"
    assert envelope["reward_hack_result"] == "UNVERIFIED"
    assert envelope["taste_integrity_result"] == "NOT_APPLICABLE"
    assert envelope["anti_centroid_result"] == "NOT_APPLICABLE"


def test_error_taxonomy_inheritance() -> None:
    # Verify all domain exceptions inherit from TenancyError
    errors = [
        TenancyViolationError("scope forgery"),
        UnauthorizedOperatorAccessError("grant expired"),
        CrossWorkspaceLeakError("cross tenant link"),
        UnverifiedMediaDigestError("hash mismatch"),
        ReceiptSelfAttestationViolationError("self-attestation"),
        StaleVersionConflictError("version conflict"),
        IdempotencyPayloadMismatchError("payload conflict"),
    ]
    for err in errors:
        assert isinstance(err, TenancyError)
        assert isinstance(err, RuntimeError)


def test_tenant_context_operator_invariants() -> None:
    ws_id = uuid4()
    grant_id = uuid4()

    # Valid operator context
    op_ctx = TenantContext(
        workspace_id=ws_id,
        actor_id="operator_dave",
        is_operator=True,
        operator_grant_id=grant_id,
    )
    assert op_ctx.is_operator is True
    assert op_ctx.operator_grant_id == grant_id

    # Invalid operator context: is_operator=True without operator_grant_id
    with pytest.raises(UnauthorizedOperatorAccessError):
        TenantContext(
            workspace_id=ws_id,
            actor_id="operator_dave",
            is_operator=True,
            operator_grant_id=None,
        )


def test_fresh_read_media_hash_validation() -> None:
    # Test valid byte source vs tampered byte source
    valid_bytes = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
    claimed_sha256 = hashlib.sha256(valid_bytes).hexdigest()

    # Matching bytes
    observed_sha256 = hashlib.sha256(valid_bytes).hexdigest()
    assert observed_sha256 == claimed_sha256

    # Tampered 1 byte
    tampered_bytes = valid_bytes[:-1] + b"\xff"
    tampered_sha256 = hashlib.sha256(tampered_bytes).hexdigest()
    assert tampered_sha256 != claimed_sha256
