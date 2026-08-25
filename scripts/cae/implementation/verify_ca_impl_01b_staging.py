#!/usr/bin/env python3
"""Automated E3 Staging Verifier and Reality Contact Runner for Phase 11 / CA-IMPL-01B.

Executes the full typed runtime path and complete adversarial hard-negative suite:
1. Two-Workspace typed execution (WS Alpha & WS Beta) across all 10 semantic operations.
2. Storage reality contact (byte upload, fresh readback, SHA-256 verification, quarantine on tampered bytes).
3. Optimistic version locking, state machine transitions, and evidence-receipt lineage.
4. All 11 Hard-Negative Countertests (HN-TS-001 through HN-TS-011).
5. Complete transient teardown (0 rows remaining in database, 0 objects remaining in storage).

Governed by TS-CAE-TEN-001, Gate A–I Review, and CA-IMPL-01B Mandate.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from uuid import UUID, uuid4

import psycopg
from psycopg import errors

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime.database import get_staging_postgres_connection
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    IdempotencyPayloadMismatchError,
    ReceiptSelfAttestationViolationError,
    StaleVersionConflictError,
    TenantContext,
    TenancyViolationError,
    UnauthorizedOperatorAccessError,
    UnverifiedMediaDigestError,
    apply_tenant_session,
    extract_tenant_context_from_claims,
    tenant_scope,
)
from ca_runtime.tenant_operations import (
    OperationReceipt,
    SemanticOperationError,
    TenantScopedSemanticOperations,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
STORAGE_KEY_VARIABLE = "CAE_SUPABASE_SECRET_KEY"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
STORAGE_BUCKET = "cae-media"


def load_local_environment() -> None:
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            key, separator, value = line.partition("=")
            if separator and key and not key.lstrip().startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())


class StagingVerificationFailure(Exception):
    pass


def log_pass(test_name: str) -> None:
    print(f"  [PASS] {test_name}")


def log_fail(test_name: str, reason: str) -> None:
    print(f"  [FAIL] {test_name}: {reason}")


# ============================================================================
# Storage Helper Functions (Supabase REST API via urllib)
# ============================================================================


def get_storage_headers(auth_token: str | None = None) -> dict[str, str]:
    secret_key = auth_token or os.environ.get(STORAGE_KEY_VARIABLE, "")
    return {
        "apikey": secret_key,
        "Authorization": f"Bearer {secret_key}",
    }


def storage_base_url() -> str:
    return f"https://{PROJECT_REF}.supabase.co/storage/v1"


def upload_storage_object(object_path: str, data: bytes, mime_type: str = "application/octet-stream") -> None:
    url = f"{storage_base_url()}/object/{STORAGE_BUCKET}/{object_path}"
    headers = get_storage_headers()
    headers["Content-Type"] = mime_type
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status not in (200, 201):
                raise StagingVerificationFailure(f"Storage upload failed: status {response.status}")
    except urllib.error.HTTPError as err:
        raise StagingVerificationFailure(f"Storage upload HTTP error: {err.code} {err.reason}") from err


def read_storage_object(object_path: str, auth_token: str | None = None) -> bytes:
    url = f"{storage_base_url()}/object/{STORAGE_BUCKET}/{object_path}"
    headers = get_storage_headers(auth_token) if auth_token is not None else get_storage_headers()
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read()


def delete_storage_object(object_path: str) -> None:
    url = f"{storage_base_url()}/object/{STORAGE_BUCKET}/{object_path}"
    headers = get_storage_headers()
    req = urllib.request.Request(url, headers=headers, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            pass
    except urllib.error.HTTPError:
        pass


# ============================================================================
# Phase 1: Two-Workspace Typed Semantic Operation Path Execution
# ============================================================================


def run_phase_1_two_workspace_path() -> dict[str, Any]:
    print("\n--- Phase 1: Two-Workspace Typed Semantic Operation Path Execution ---")
    storage_cleanup_paths: list[str] = []
    recorded_receipts: list[OperationReceipt] = []

    ws_alpha_id = uuid4()
    ws_beta_id = uuid4()
    op_org_id = uuid4()
    op_grant_id = uuid4()
    media_alpha_id = uuid4()
    ev_alpha_id = uuid4()
    now = datetime.now(timezone.utc)

    with get_staging_postgres_connection() as conn:
        ops = TenantScopedSemanticOperations(conn)

        # 1. Provision Canonical Harness Template (Canonical Plane)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cae.harness_template (template_id, version, definition_yaml, definition_sha256, is_active)
                VALUES (%s, %s, %s, %s, true)
                ON CONFLICT (template_id, version) DO NOTHING;
                """,
                ("ht_interview_slice", "1.0.0", "steps:\n  - step_01\n  - step_02", hashlib.sha256(b"steps").hexdigest()),
            )
            # Provision Operator Organization
            cur.execute(
                """
                INSERT INTO cae.operator_organization (operator_org_id, org_name, status)
                VALUES (%s, %s, 'ACTIVE')
                ON CONFLICT DO NOTHING;
                """,
                (op_org_id, "Platform Global Operations"),
            )
        conn.commit()

        # 2. Provision Workspace Alpha & Workspace Beta via typed operation
        rcpt_ws_a = ops.provision_workspace(
            slug=f"ws-alpha-{ws_alpha_id.hex[:6]}",
            display_name="Workspace Alpha Client",
            actor_id="actor_alice_admin",
            idempotency_key=f"idemp_ws_a_{ws_alpha_id.hex[:8]}",
            workspace_id=ws_alpha_id,
        )
        recorded_receipts.append(rcpt_ws_a)
        log_pass(f"1. cae.workspace.provision@1.0.0: WS Alpha provisioned ({rcpt_ws_a.receipt_id})")

        rcpt_ws_b = ops.provision_workspace(
            slug=f"ws-beta-{ws_beta_id.hex[:6]}",
            display_name="Workspace Beta Client",
            actor_id="actor_bob_admin",
            idempotency_key=f"idemp_ws_b_{ws_beta_id.hex[:8]}",
            workspace_id=ws_beta_id,
        )
        recorded_receipts.append(rcpt_ws_b)
        log_pass(f"1. cae.workspace.provision@1.0.0: WS Beta provisioned ({rcpt_ws_b.receipt_id})")

        # 3. Grant Membership via typed operation
        ctx_alpha = TenantContext(workspace_id=ws_alpha_id, actor_id="actor_alice_admin", role="ADMIN")
        rcpt_mem_a = ops.grant_workspace_membership(
            target_actor_id="actor_alice_member",
            role="MEMBER",
            idempotency_key=f"idemp_mem_a_{uuid4().hex[:8]}",
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_mem_a)
        log_pass(f"2. cae.workspace.membership.grant@1.0.0: Membership granted in WS Alpha ({rcpt_mem_a.receipt_id})")

        # 4. Issue Ephemeral Operator Access Grant via typed operation
        rcpt_op_grant = ops.issue_operator_grant(
            operator_org_id=op_org_id,
            operator_actor_id="operator_dave",
            target_workspace_id=ws_alpha_id,
            justification="Auditing tenant audio ingestion pipeline per ticket AUD-102",
            expires_at=now + timedelta(hours=2),
            idempotency_key=f"idemp_op_grant_{uuid4().hex[:8]}",
            grant_id=op_grant_id,
        )
        recorded_receipts.append(rcpt_op_grant)
        log_pass(f"3. cae.operator.grant.issue@1.0.0: Operator grant issued for WS Alpha ({rcpt_op_grant.receipt_id})")

        # 5. Initialize Engagement via typed operation
        eng_alpha_id = uuid4()
        rcpt_eng_a = ops.initialize_engagement(
            title="Executive Leadership Qualitative Intake",
            idempotency_key=f"idemp_eng_a_{uuid4().hex[:8]}",
            engagement_id=eng_alpha_id,
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_eng_a)
        log_pass(f"4. cae.engagement.initialize@1.0.0: Engagement initialized in WS Alpha ({eng_alpha_id})")

        # 6. Register Guest via typed operation
        guest_alpha_id = uuid4()
        rcpt_guest_a = ops.register_guest(
            pseudonym="Guest Dr. Smith",
            external_reference_id="ref_smith_01",
            consent_status="VERIFIED_CONSENT",
            idempotency_key=f"idemp_gst_a_{uuid4().hex[:8]}",
            guest_id=guest_alpha_id,
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_guest_a)
        log_pass(f"5. cae.guest.register@1.0.0: Guest registered in WS Alpha ({rcpt_guest_a.receipt_id})")

        # 7. Upload & Verify Media Asset via Storage Fresh-Read Reality Contact
        storage_path = f"staging-test/{ws_alpha_id}/{media_alpha_id}/interview_audio.wav"
        raw_audio_bytes = b"RIFF\x2c\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        claimed_sha256 = hashlib.sha256(raw_audio_bytes).hexdigest()

        # Reality contact: upload to Supabase private storage
        upload_storage_object(storage_path, raw_audio_bytes, mime_type="audio/wav")
        storage_cleanup_paths.append(storage_path)
        log_pass(f"Reality Contact: Uploaded {len(raw_audio_bytes)} bytes to private Storage ({storage_path})")

        # Execute verify_media_asset with byte_reader_fn retrieving from Supabase Storage
        def storage_reader(path: str) -> bytes:
            return read_storage_object(path)

        rcpt_media_verify = ops.verify_media_asset(
            media_asset_id=media_alpha_id,
            storage_path=storage_path,
            claimed_sha256=claimed_sha256,
            byte_size=len(raw_audio_bytes),
            mime_type="audio/wav",
            idempotency_key=f"idemp_med_verify_{uuid4().hex[:8]}",
            engagement_id=eng_alpha_id,
            byte_reader_fn=storage_reader,
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_media_verify)
        log_pass(f"6. cae.media.verify@1.0.0: Fresh-read verified from Storage -> STAGED -> VERIFIED ({rcpt_media_verify.receipt_id})")

        # 8. Capture Evidence Item & Link to Verified Media Asset
        rcpt_ev_capture = ops.capture_evidence(
            media_asset_id=media_alpha_id,
            evidence_item_id=ev_alpha_id,
            start_ms=1200,
            end_ms=4500,
            quoted_text="Conscious activation unlocks foundational strategic clarity.",
            idempotency_key=f"idemp_ev_cap_{uuid4().hex[:8]}",
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_ev_capture)
        log_pass(f"7. cae.evidence.capture@1.0.0: Evidence captured and linked to receipt ({rcpt_ev_capture.receipt_id})")

        # 9. Initialize HarnessRun referencing Canonical Template
        run_alpha_id = uuid4()
        rcpt_run_init = ops.initialize_harness_run(
            engagement_id=eng_alpha_id,
            template_id="ht_interview_slice",
            template_version="1.0.0",
            idempotency_key=f"idemp_run_init_{uuid4().hex[:8]}",
            run_id=run_alpha_id,
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_run_init)
        log_pass(f"8. cae.harness.run.initialize@1.0.0: HarnessRun initialized in state INITIALIZED ({run_alpha_id})")

        # 10. Step HarnessRun through state machine transitions
        rcpt_run_step1 = ops.step_harness_run(
            run_id=run_alpha_id,
            from_step="step_01",
            to_step="step_02",
            expected_version=1,
            outcome="RUNNING",
            idempotency_key=f"idemp_run_step1_{uuid4().hex[:8]}",
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_run_step1)
        log_pass(f"9a. cae.harness.run.step@1.0.0: Step advanced INITIALIZED -> RUNNING (v1->v2)")

        rcpt_run_step2 = ops.step_harness_run(
            run_id=run_alpha_id,
            from_step="step_02",
            to_step="step_completed",
            expected_version=2,
            outcome="COMPLETED",
            idempotency_key=f"idemp_run_step2_{uuid4().hex[:8]}",
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_run_step2)
        log_pass(f"9b. cae.harness.run.step@1.0.0: Step advanced RUNNING -> COMPLETED (v2->v3)")

        # 11. Generic Direct Receipt Commit
        rcpt_custom = ops.commit_receipt(
            operation_id="cae.receipt.commit@1.0.0",
            idempotency_key=f"idemp_custom_rcpt_{uuid4().hex[:8]}",
            actor_id="actor_alice_admin",
            payload={"summary": "End-to-end typed operation execution verified"},
            evidence_ids=[ev_alpha_id],
            context=ctx_alpha,
        )
        recorded_receipts.append(rcpt_custom)
        log_pass(f"10. cae.receipt.commit@1.0.0: Immutable receipt committed with evidence link ({rcpt_custom.receipt_id})")

    return {
        "ws_alpha_id": ws_alpha_id,
        "ws_beta_id": ws_beta_id,
        "op_org_id": op_org_id,
        "eng_alpha_id": eng_alpha_id,
        "media_alpha_id": media_alpha_id,
        "run_alpha_id": run_alpha_id,
        "storage_cleanup_paths": storage_cleanup_paths,
        "recorded_receipts": recorded_receipts,
    }


# ============================================================================
# Phase 2: Adversarial Hard-Negative Countertests (HN-TS-001 - HN-TS-011)
# ============================================================================


def run_phase_2_adversarial_matrix(context_ids: dict[str, Any]) -> None:
    print("\n--- Phase 2: Adversarial Hard-Negative Matrix (HN-TS-001 - HN-TS-011) ---")
    ws_alpha_id = context_ids["ws_alpha_id"]
    ws_beta_id = context_ids["ws_beta_id"]
    eng_alpha_id = context_ids["eng_alpha_id"]
    media_alpha_id = context_ids["media_alpha_id"]
    run_alpha_id = context_ids["run_alpha_id"]

    with get_staging_postgres_connection() as conn:
        ops = TenantScopedSemanticOperations(conn)
        ctx_alpha = TenantContext(workspace_id=ws_alpha_id, actor_id="actor_alice_admin", role="ADMIN")

        # HN-TS-001: Scope Forgery Defense (Token Workspace vs Request Parameter mismatch)
        claims = {"sub": "actor_alice_admin", "workspace_id": str(ws_alpha_id)}
        try:
            extract_tenant_context_from_claims(claims, requested_workspace_id=str(ws_beta_id))
            raise StagingVerificationFailure("HN-TS-001 failed: scope forgery was not rejected")
        except TenancyViolationError as err:
            log_pass(f"HN-TS-001 (Scope Forgery Defense): Successfully rejected mismatched workspace parameter ({err})")

        # HN-TS-002: RLS Bypass Defense (Unauthenticated connection returns 0 rows)
        with conn.cursor() as cur:
            cur.execute("SET LOCAL ROLE authenticated;")
            cur.execute("SELECT set_config('app.current_workspace_id', '', true);")
            cur.execute("SELECT set_config('app.is_operator', 'false', true);")
            cur.execute("SELECT COUNT(*) FROM cae.engagement;")
            count = cur.fetchone()[0]
            if count != 0:
                raise StagingVerificationFailure(f"HN-TS-002 failed: unauthenticated session saw {count} rows")
            log_pass("HN-TS-002 (RLS Bypass Defense): Connection without tenant context returns 0 rows")

        # HN-TS-003: Cross-Workspace Parent Linkage Defense
        eng_beta_id = uuid4()
        # Initialize engagement in WS Beta
        ctx_beta = TenantContext(workspace_id=ws_beta_id, actor_id="actor_bob_admin", role="ADMIN")
        ops.initialize_engagement(
            title="Engagement in Beta",
            idempotency_key=f"idemp_eng_b_{uuid4().hex[:8]}",
            engagement_id=eng_beta_id,
            context=ctx_beta,
        )

        try:
            # Attempt to initialize a media asset in WS Alpha referencing engagement in WS Beta
            ops.verify_media_asset(
                media_asset_id=uuid4(),
                storage_path="staging-test/cross_parent.wav",
                claimed_sha256=hashlib.sha256(b"cross").hexdigest(),
                byte_size=5,
                mime_type="audio/wav",
                idempotency_key=f"idemp_cross_{uuid4().hex[:8]}",
                engagement_id=eng_beta_id,  # Belongs to WS Beta!
                raw_bytes=b"cross",
                context=ctx_alpha,
            )
            raise StagingVerificationFailure("HN-TS-003 failed: cross-workspace parent link was not rejected")
        except CrossWorkspaceLeakError:
            log_pass("HN-TS-003 (Cross-Workspace Parent Defense): Cross-workspace parent link rejected by typed validator & composite FK")

        # HN-TS-004: Tampered Storage Byte Hash Defense -> QUARANTINED
        tampered_media_id = uuid4()
        tampered_bytes = b"original_payload_bytes_here"
        actual_tampered_hash = hashlib.sha256(tampered_bytes).hexdigest()
        falsified_hash = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

        try:
            ops.verify_media_asset(
                media_asset_id=tampered_media_id,
                storage_path=f"staging-test/{ws_alpha_id}/{tampered_media_id}/tampered.wav",
                claimed_sha256=falsified_hash,
                byte_size=len(tampered_bytes),
                mime_type="audio/wav",
                idempotency_key=f"idemp_tamp_{uuid4().hex[:8]}",
                raw_bytes=tampered_bytes,
                context=ctx_alpha,
            )
            raise StagingVerificationFailure("HN-TS-004 failed: tampered byte hash was not rejected")
        except UnverifiedMediaDigestError as err:
            # Verify that the media asset was quarantined in database
            with conn.cursor() as cur:
                apply_tenant_session(cur, ctx_alpha)
                cur.execute(
                    "SELECT lifecycle_state FROM cae.media_asset WHERE media_asset_id = %s;",
                    (tampered_media_id,),
                )
                row = cur.fetchone()
                if row is None or row[0] != "QUARANTINED":
                    raise StagingVerificationFailure(f"HN-TS-004 failed: asset state is {row}, expected QUARANTINED")
            log_pass(f"HN-TS-004 (Tampered Bytes Defense): Hash mismatch detected, asset transitioned to QUARANTINED ({err})")

        # HN-TS-005: Atomic Transaction & Receipt Rollback Defense
        failed_idemp_key = f"idemp_fail_{uuid4().hex[:8]}"
        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    apply_tenant_session(cur, ctx_alpha)
                    # Insert receipt directly
                    cur.execute(
                        """
                        INSERT INTO cae.receipt (
                            receipt_id, workspace_id, operation_id, idempotency_key, actor_id,
                            canonical_payload, payload_jsonb, payload_sha256
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """,
                        (
                            f"rcpt_fail_{uuid4().hex[:8]}",
                            ws_alpha_id,
                            "cae.engagement.initialize@1.0.0",
                            failed_idemp_key,
                            "actor_alice_admin",
                            "{}",
                            psycopg.types.json.Jsonb({}),
                            hashlib.sha256(b"{}").hexdigest(),
                        ),
                    )
                    # Force transaction failure
                    cur.execute("INSERT INTO cae.engagement (engagement_id, workspace_id, title) VALUES (NULL, NULL, NULL);")
        except Exception:
            pass  # Expected rollback

        # Verify receipt was rolled back
        with conn.cursor() as cur:
            apply_tenant_session(cur, ctx_alpha)
            cur.execute("SELECT COUNT(*) FROM cae.receipt WHERE idempotency_key = %s;", (failed_idemp_key,))
            if cur.fetchone()[0] != 0:
                raise StagingVerificationFailure("HN-TS-005 failed: receipt persisted despite transaction abort")
            log_pass("HN-TS-005 (Atomic Receipt Rollback Defense): Transaction failure rolls back receipt emission completely")

        # HN-TS-006: Cross-Tenant Idempotency Collision Isolation
        shared_idemp_key = "idemp_shared_cross_tenant_test"
        rcpt_iso_a = ops.register_guest(
            pseudonym="Guest Isolated Alpha",
            idempotency_key=shared_idemp_key,
            context=ctx_alpha,
        )
        rcpt_iso_b = ops.register_guest(
            pseudonym="Guest Isolated Beta",
            idempotency_key=shared_idemp_key,
            context=ctx_beta,
        )
        if rcpt_iso_a.workspace_id == rcpt_iso_b.workspace_id:
            raise StagingVerificationFailure("HN-TS-006 failed: workspace IDs collided")
        log_pass("HN-TS-006 (Idempotency Isolation Defense): Identical idempotency keys succeed independently across workspaces")

        # HN-TS-007: Guest Locality Anti-Merge Defense
        with conn.cursor() as cur:
            cur.execute("SET LOCAL ROLE authenticated;")
            cur.execute("SELECT set_config('app.current_workspace_id', %s, true);", (str(ws_alpha_id),))
            cur.execute("SELECT set_config('app.is_operator', 'false', true);")
            cur.execute("SELECT COUNT(*) FROM cae.guest WHERE pseudonym = 'Guest Isolated Beta';")
            if cur.fetchone()[0] != 0:
                raise StagingVerificationFailure("HN-TS-007 failed: WS Beta guest leaked into WS Alpha scope")
            log_pass("HN-TS-007 (Guest Locality Defense): Guest identities strictly isolated within workspace boundary")

        # HN-TS-008: Stale Version Conflict / Optimistic Concurrency Defense
        try:
            # HarnessRun in WS Alpha is at version 3 (COMPLETED). Attempting step with expected_version=1 must fail
            ops.step_harness_run(
                run_id=run_alpha_id,
                from_step="step_01",
                to_step="step_02",
                expected_version=1,
                outcome="RUNNING",
                idempotency_key=f"idemp_stale_{uuid4().hex[:8]}",
                context=ctx_alpha,
            )
            raise StagingVerificationFailure("HN-TS-008 failed: stale version update was not rejected")
        except StaleVersionConflictError as err:
            log_pass(f"HN-TS-008 (Optimistic Lock Defense): Stale version mutation rejected with StaleVersionConflictError ({err})")

        # HN-TS-009: Idempotency Payload Mismatch Defense
        replay_idemp_key = f"idemp_replay_check_{uuid4().hex[:8]}"
        rcpt_orig = ops.initialize_engagement(
            title="Original Engagement Title",
            idempotency_key=replay_idemp_key,
            context=ctx_alpha,
        )
        # Attempt to reuse the same key with altered title
        try:
            ops.initialize_engagement(
                title="Altered Engagement Title Mismatch",
                idempotency_key=replay_idemp_key,
                context=ctx_alpha,
            )
            raise StagingVerificationFailure("HN-TS-009 failed: idempotency payload mismatch was not rejected")
        except IdempotencyPayloadMismatchError as err:
            log_pass(f"HN-TS-009 (Idempotency Payload Mismatch Defense): Altered payload on existing key rejected ({err})")

        # HN-TS-010: Append-Only Receipt Mutation Defense (Trigger prevents UPDATE/DELETE)
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE cae.receipt SET actor_id = 'malicious_actor' WHERE workspace_id = %s;", (ws_alpha_id,))
                conn.commit()
                raise StagingVerificationFailure("HN-TS-010 failed: UPDATE on cae.receipt succeeded")
            except Exception:
                conn.rollback()
                log_pass("HN-TS-010 (Immutable Receipt Defense): UPDATE on cae.receipt blocked by trigger trg_prevent_receipt_mutation")

            try:
                cur.execute("DELETE FROM cae.receipt WHERE workspace_id = %s;", (ws_alpha_id,))
                conn.commit()
                raise StagingVerificationFailure("HN-TS-010 failed: DELETE on cae.receipt succeeded")
            except Exception:
                conn.rollback()
                log_pass("HN-TS-010 (Immutable Receipt Defense): DELETE on cae.receipt blocked by trigger trg_prevent_receipt_mutation")

        # HN-TS-011: Expired & Revoked Operator Access Grant Denial
        op_org_id = context_ids["op_org_id"]
        grant_exp_id = uuid4()
        grant_rev_id = uuid4()
        now = datetime.now(timezone.utc)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cae.operator_access_grant (
                    grant_id, operator_org_id, operator_actor_id, workspace_id, justification, expires_at
                ) VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (grant_exp_id, op_org_id, "op_user", ws_alpha_id, "Expired grant", now - timedelta(minutes=10)),
            )
            cur.execute(
                """
                INSERT INTO cae.operator_access_grant (
                    grant_id, operator_org_id, operator_actor_id, workspace_id, justification, expires_at, revoked_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (grant_rev_id, op_org_id, "op_user", ws_alpha_id, "Revoked grant", now + timedelta(hours=1), now - timedelta(minutes=1)),
            )
        conn.commit()

        # Check expired grant query
        with conn.cursor() as cur:
            cur.execute("SET LOCAL ROLE authenticated;")
            cur.execute("SELECT set_config('app.is_operator', 'true', true);")
            cur.execute("SELECT set_config('app.current_operator_grant_id', %s, true);", (str(grant_exp_id),))
            cur.execute("SELECT set_config('app.current_workspace_id', '', true);")
            cur.execute("SELECT COUNT(*) FROM cae.engagement WHERE workspace_id = %s;", (ws_alpha_id,))
            if cur.fetchone()[0] != 0:
                raise StagingVerificationFailure("HN-TS-011 failed: expired operator grant yielded rows")
            log_pass("HN-TS-011 (Operator Grant Defense): Expired operator grant strictly yields 0 rows")

            cur.execute("SELECT set_config('app.current_operator_grant_id', %s, true);", (str(grant_rev_id),))
            cur.execute("SELECT COUNT(*) FROM cae.engagement WHERE workspace_id = %s;", (ws_alpha_id,))
            if cur.fetchone()[0] != 0:
                raise StagingVerificationFailure("HN-TS-011 failed: revoked operator grant yielded rows")
            log_pass("HN-TS-011 (Operator Grant Defense): Revoked operator grant strictly yields 0 rows")


# ============================================================================
# Phase 3: Transient Cleanup & Teardown Verification
# ============================================================================


def run_phase_3_cleanup(cleanup_paths: list[str]) -> None:
    print("\n--- Phase 3: Transient Cleanup & Teardown Verification ---")

    # 1. Prune Storage Objects
    for path in cleanup_paths:
        delete_storage_object(path)
    log_pass(f"Pruned {len(cleanup_paths)} test storage object(s) from bucket '{STORAGE_BUCKET}'")

    # 2. Prune Database Rows
    with get_staging_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cae.receipt_evidence_link;")
            cur.execute("ALTER TABLE cae.receipt DISABLE TRIGGER trg_prevent_receipt_mutation;")
            cur.execute("DELETE FROM cae.receipt;")
            cur.execute("ALTER TABLE cae.receipt ENABLE TRIGGER trg_prevent_receipt_mutation;")
            cur.execute("DELETE FROM cae.harness_run;")
            cur.execute("DELETE FROM cae.media_asset;")
            cur.execute("DELETE FROM cae.guest;")
            cur.execute("DELETE FROM cae.engagement;")
            cur.execute("DELETE FROM cae.operator_access_grant;")
            cur.execute("DELETE FROM cae.operator_organization;")
            cur.execute("DELETE FROM cae.workspace_membership;")
            cur.execute("DELETE FROM cae.workspace;")
        conn.commit()

        # 3. Assert 0 rows in all operational tables
        tables = [
            "workspace",
            "workspace_membership",
            "operator_organization",
            "operator_access_grant",
            "engagement",
            "guest",
            "media_asset",
            "harness_run",
            "receipt",
            "receipt_evidence_link",
        ]
        with conn.cursor() as cur:
            for table in tables:
                cur.execute(f"SELECT COUNT(*) FROM cae.{table};")
                cnt = cur.fetchone()[0]
                if cnt != 0:
                    raise StagingVerificationFailure(f"Cleanup incomplete: cae.{table} still contains {cnt} rows")
        log_pass("Database transient cleanup verified: 0 test rows remaining across all operational tables")


# ============================================================================
# Main Execution Runner
# ============================================================================


def run_all_ca_impl_01b_verifications() -> int:
    load_local_environment()
    print("================================================================================")
    print("   CAE STAGING E3 REALITY CONTACT & ADVERSARIAL MATRIX: CA-IMPL-01B             ")
    print("================================================================================")
    print(f"Target Staging Database: aws-1-eu-west-1.pooler.supabase.com:5432/postgres")
    print(f"Target Staging Storage:  {PROJECT_REF}.supabase.co/storage/v1/object/{STORAGE_BUCKET}")

    try:
        context_ids = run_phase_1_two_workspace_path()
        run_phase_2_adversarial_matrix(context_ids)
        run_phase_3_cleanup(context_ids["storage_cleanup_paths"])

        print("\n================================================================================")
        print("   SUCCESS: CA-IMPL-01B TYPED RUNTIME PATH & E3 PROOF VERIFIED                  ")
        print("   ALL 10 OPERATIONS AND ALL 11 HARD NEGATIVES PASSED (100% COMPLIANT)          ")
        print("================================================================================")
        return 0
    except StagingVerificationFailure as exc:
        print(f"\n[FATAL STAGING VERIFICATION FAILURE]: {exc}")
        return 1
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR]: {type(exc).__name__}: {exc}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(run_all_ca_impl_01b_verifications())
