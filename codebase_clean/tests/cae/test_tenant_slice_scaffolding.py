"""Unit and integration test suite for CA-IMPL-01A Tenant Foundation & Scaffolding.

Governed by TS-CAE-TEN-001, CA-CAN-01A/B/C object constitutions, and FR-CAE-TEN-001 through FR-CAE-TEN-015.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from uuid import UUID, uuid4
import pytest
from pydantic import ValidationError

from ca_runtime.database import ProductDatabaseError, get_staging_postgres_connection
from ca_runtime.models.tenant_slice import (
    ConsentStatus,
    EngagementLifecycleState,
    EngagementModel,
    GuestModel,
    HarnessRunLifecycleState,
    HarnessRunModel,
    HarnessTemplateModel,
    MediaAssetLifecycleState,
    MediaAssetModel,
    MembershipRole,
    MembershipStatus,
    OperatorAccessGrantModel,
    OperatorOrganizationModel,
    OperatorOrgStatus,
    ReceiptEvidenceLinkModel,
    ReceiptModel,
    WorkspaceMembershipModel,
    WorkspaceModel,
    WorkspaceStatus,
)
from ca_runtime.tenancy import (
    TenantContext,
    TenancyViolationError,
    UnauthorizedOperatorAccessError,
    extract_tenant_context_from_claims,
    get_current_tenant_context,
    require_current_tenant_context,
    tenant_scope,
)


def test_workspace_model_valid() -> None:
    ws = WorkspaceModel(slug="acme-corp", display_name="Acme Corporation")
    assert isinstance(ws.workspace_id, UUID)
    assert ws.slug == "acme-corp"
    assert ws.display_name == "Acme Corporation"
    assert ws.status == WorkspaceStatus.ACTIVE


def test_workspace_model_invalid_slug() -> None:
    with pytest.raises(ValidationError):
        WorkspaceModel(slug="INVALID_SLUG_WITH_CAPS", display_name="Invalid Slug")
    with pytest.raises(ValidationError):
        WorkspaceModel(slug="a", display_name="Too short")


def test_workspace_membership_model() -> None:
    ws_id = uuid4()
    mem = WorkspaceMembershipModel(
        workspace_id=ws_id,
        actor_id="usr_12345",
        role=MembershipRole.ADMIN,
    )
    assert mem.workspace_id == ws_id
    assert mem.actor_id == "usr_12345"
    assert mem.role == MembershipRole.ADMIN
    assert mem.status == MembershipStatus.ACTIVE


def test_operator_access_grant_lifecycle() -> None:
    ws_id = uuid4()
    org_id = uuid4()
    now = datetime.now(timezone.utc)

    # Active grant
    grant_active = OperatorAccessGrantModel(
        operator_org_id=org_id,
        operator_actor_id="op_dave",
        workspace_id=ws_id,
        justification="Support ticket verification #12345",
        expires_at=now + timedelta(hours=1),
    )
    assert grant_active.is_active is True

    # Expired grant
    grant_expired = OperatorAccessGrantModel(
        operator_org_id=org_id,
        operator_actor_id="op_dave",
        workspace_id=ws_id,
        justification="Support ticket verification #12345",
        expires_at=now - timedelta(minutes=10),
    )
    assert grant_expired.is_active is False

    # Revoked grant
    grant_revoked = OperatorAccessGrantModel(
        operator_org_id=org_id,
        operator_actor_id="op_dave",
        workspace_id=ws_id,
        justification="Support ticket verification #12345",
        expires_at=now + timedelta(hours=1),
        revoked_at=now - timedelta(minutes=1),
    )
    assert grant_revoked.is_active is False


def test_engagement_model() -> None:
    ws_id = uuid4()
    eng = EngagementModel(
        workspace_id=ws_id,
        title="Q3 Brand Positioning Assessment",
    )
    assert eng.workspace_id == ws_id
    assert eng.title == "Q3 Brand Positioning Assessment"
    assert eng.lifecycle_state == EngagementLifecycleState.PLANNED
    assert eng.version == 1


def test_guest_model_workspace_locality() -> None:
    ws_id = uuid4()
    guest = GuestModel(
        workspace_id=ws_id,
        pseudonym="Guest Echo",
        consent_status=ConsentStatus.GRANTED,
    )
    assert guest.workspace_id == ws_id
    assert guest.pseudonym == "Guest Echo"
    assert guest.consent_status == ConsentStatus.GRANTED


def test_media_asset_model_and_hash_validation() -> None:
    ws_id = uuid4()
    valid_sha = hashlib.sha256(b"raw audio samples").hexdigest()

    asset = MediaAssetModel(
        workspace_id=ws_id,
        storage_path="cae-media/tenant-1/audio.wav",
        canonical_sha256=valid_sha,
        byte_size=17,
        mime_type="audio/wav",
    )
    assert asset.canonical_sha256 == valid_sha
    assert asset.lifecycle_state == MediaAssetLifecycleState.REGISTERED

    # Invalid SHA-256 pattern
    with pytest.raises(ValidationError):
        MediaAssetModel(
            workspace_id=ws_id,
            storage_path="cae-media/tenant-1/audio.wav",
            canonical_sha256="not_a_valid_sha256_hash",
            byte_size=17,
            mime_type="audio/wav",
        )


def test_harness_template_and_run_models() -> None:
    tpl_yaml = "steps:\n  - id: step_01\n    name: Welcome\n"
    tpl_sha = hashlib.sha256(tpl_yaml.encode("utf-8")).hexdigest()

    template = HarnessTemplateModel(
        template_id="tpl_interview_v1",
        version="1.0.0",
        definition_yaml=tpl_yaml,
        definition_sha256=tpl_sha,
    )
    assert template.template_id == "tpl_interview_v1"
    assert template.version == "1.0.0"

    ws_id = uuid4()
    eng_id = uuid4()
    run = HarnessRunModel(
        workspace_id=ws_id,
        engagement_id=eng_id,
        template_id="tpl_interview_v1",
        template_version="1.0.0",
        current_step="step_01",
    )
    assert run.lifecycle_state == HarnessRunLifecycleState.INITIALIZED
    assert run.version == 1


def test_receipt_model() -> None:
    ws_id = uuid4()
    payload = {"status": "SUCCESS", "records_created": 1}
    payload_str = json.dumps(payload, sort_keys=True)
    payload_sha = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

    receipt = ReceiptModel(
        receipt_id="rcpt_test_001",
        workspace_id=ws_id,
        operation_id="cae.engagement.initialize@1.0.0",
        idempotency_key="idemp_eng_init_001",
        actor_id="usr_admin_1",
        canonical_payload=payload_str,
        payload_jsonb=payload,
        payload_sha256=payload_sha,
    )
    assert receipt.receipt_id == "rcpt_test_001"
    assert receipt.payload_sha256 == payload_sha


def test_tenant_context_and_scope_manager() -> None:
    ws_id = uuid4()
    ctx = TenantContext(workspace_id=ws_id, actor_id="usr_alice")

    assert get_current_tenant_context() is None
    with pytest.raises(TenancyViolationError):
        require_current_tenant_context()

    with tenant_scope(ctx):
        current = require_current_tenant_context()
        assert current.workspace_id == ws_id
        assert current.actor_id == "usr_alice"

    assert get_current_tenant_context() is None


def test_extract_tenant_context_from_claims_valid() -> None:
    ws_id = uuid4()
    claims = {
        "sub": "actor_alice",
        "workspace_id": str(ws_id),
        "role": "ADMIN",
    }
    ctx = extract_tenant_context_from_claims(claims, requested_workspace_id=str(ws_id))
    assert ctx.workspace_id == ws_id
    assert ctx.actor_id == "actor_alice"
    assert ctx.role == "ADMIN"
    assert ctx.is_operator is False


def test_extract_tenant_context_scope_forgery_rejection_hn_ts_001() -> None:
    ws_a_id = uuid4()
    ws_b_id = uuid4()
    claims = {
        "sub": "actor_alice",
        "workspace_id": str(ws_a_id),
    }
    # Caller attempts to access Workspace B using Workspace A token
    with pytest.raises(TenancyViolationError, match="TENANCY_VIOLATION"):
        extract_tenant_context_from_claims(claims, requested_workspace_id=str(ws_b_id))


def test_staging_database_connection_guard() -> None:
    # Non-pooler or malicious database URL should be rejected
    with pytest.raises(ProductDatabaseError, match="not the approved CAE staging session pooler"):
        get_staging_postgres_connection("postgresql://postgres:fake@malicious-host.com:5432/postgres")
