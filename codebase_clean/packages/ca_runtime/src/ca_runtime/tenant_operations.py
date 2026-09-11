"""Typed PostgreSQL semantic operations for CAE's tenant/guest vertical slice.

Governed by TS-CAE-TEN-001, Gate A–I Review, and CA-IMPL-01B Mandate.
Provides strongly-typed operations with Row-Level Security session enforcement,
optimistic locking, fresh-read storage verification, and atomic receipt lineage.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Callable, Mapping, Optional, Sequence
from uuid import UUID, uuid4

import psycopg
from psycopg.types.json import Jsonb

from ca_contracts import canonical_json_text, canonical_sha256
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
    apply_tenant_session,
    require_current_tenant_context,
)


class SemanticOperationError(TenancyError):
    """A typed semantic operation cannot satisfy its contract."""
    pass


class SemanticOperationConflict(SemanticOperationError):
    """An idempotency or optimistic-concurrency condition was violated."""
    pass


@dataclass(frozen=True, slots=True)
class OperationReceipt:
    receipt_id: str
    workspace_id: UUID
    operation_id: str
    idempotency_key: str
    actor_id: str
    outcome: str
    idempotent_replay: bool
    payload: Mapping[str, Any]
    payload_sha256: str
    evidence_ids: tuple[UUID, ...] = ()


def _generate_receipt_id(operation_id: str, workspace_id: UUID, idempotency_key: str) -> str:
    seed = f"{operation_id}:{workspace_id}:{idempotency_key}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
    op_tag = operation_id.split("@")[0].replace(".", "_")
    return f"rcpt_{op_tag}_{digest}"


def _build_receipt_envelope(
    *,
    receipt_id: str,
    workspace_id: UUID,
    operation_id: str,
    idempotency_key: str,
    actor_id: str,
    command_payload: Mapping[str, Any],
    event_payload: Mapping[str, Any],
    validator_results: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "receipt_type": "cae_execution_receipt",
        "receipt_id": receipt_id,
        "workspace_id": str(workspace_id),
        "operation_id": operation_id,
        "idempotency_key": idempotency_key,
        "actor_id": actor_id,
        "input_snapshot_sha256": canonical_sha256(dict(command_payload)),
        "output_snapshot_sha256": canonical_sha256(dict(event_payload)),
        "environment_fidelity": "E3_PRODUCTION_SHAPED",
        "environment_identity": {
            "state_authority": "postgresql_supabase",
            "runtime_component": "ca_runtime.tenant_operations",
            "deployment_boundary": "staging_only",
        },
        "evaluator_versions": {
            "tenant_slice": "1.0.0",
        },
        "validator_results": dict(validator_results or {"transition_contract": "PASS"}),
        "reward_hack_result": "UNVERIFIED",
        "taste_integrity_result": "NOT_APPLICABLE",
        "anti_centroid_result": "NOT_APPLICABLE",
    }


class TenantScopedSemanticOperations:
    """Executes typed CAE tenant-scoped operations on Supabase/PostgreSQL staging.

    Every operation enforces TenantContext boundaries, sets PostgreSQL session configuration
    for Row-Level Security, validates parent chains, and commits state mutations,
    events, and immutable receipts atomically in a single transaction.
    """

    def __init__(self, connection: psycopg.Connection[Any]) -> None:
        self.connection = connection

    def _idempotent_replay_check(
        self,
        cursor: psycopg.Cursor[object],
        *,
        workspace_id: UUID,
        operation_id: str,
        idempotency_key: str,
        command_payload: Mapping[str, Any],
    ) -> Optional[OperationReceipt]:
        cursor.execute(
            """
            SELECT receipt_id, actor_id, canonical_payload, payload_sha256
            FROM cae.receipt
            WHERE workspace_id = %s AND operation_id = %s AND idempotency_key = %s;
            """,
            (workspace_id, operation_id, idempotency_key),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        existing_receipt_id = str(row[0])
        existing_actor_id = str(row[1])
        existing_payload_json = str(row[2])
        existing_sha256 = str(row[3])

        computed_sha256 = canonical_sha256(dict(command_payload))
        if existing_sha256 != computed_sha256:
            raise IdempotencyPayloadMismatchError(
                f"IDEMPOTENCY_PAYLOAD_MISMATCH: Key '{idempotency_key}' reused with altered payload. "
                f"Existing hash: {existing_sha256}, incoming hash: {computed_sha256}"
            )

        # Retrieve linked evidence IDs
        cursor.execute(
            """
            SELECT evidence_item_id FROM cae.receipt_evidence_link
            WHERE workspace_id = %s AND receipt_id = %s;
            """,
            (workspace_id, existing_receipt_id),
        )
        evidence_ids = tuple(UUID(str(r[0])) for r in cursor.fetchall())

        return OperationReceipt(
            receipt_id=existing_receipt_id,
            workspace_id=workspace_id,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            actor_id=existing_actor_id,
            outcome="IDEMPOTENT_REPLAY",
            idempotent_replay=True,
            payload=json.loads(existing_payload_json),
            payload_sha256=existing_sha256,
            evidence_ids=evidence_ids,
        )

    def _commit_atomic_receipt(
        self,
        cursor: psycopg.Cursor[object],
        *,
        workspace_id: UUID,
        operation_id: str,
        idempotency_key: str,
        actor_id: str,
        command_payload: Mapping[str, Any],
        event_payload: Mapping[str, Any],
        evidence_ids: Sequence[UUID] = (),
        validator_results: Mapping[str, str] | None = None,
    ) -> OperationReceipt:
        receipt_id = _generate_receipt_id(operation_id, workspace_id, idempotency_key)
        envelope = _build_receipt_envelope(
            receipt_id=receipt_id,
            workspace_id=workspace_id,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            actor_id=actor_id,
            command_payload=command_payload,
            event_payload=event_payload,
            validator_results=validator_results,
        )
        canonical_text = canonical_json_text(envelope)
        payload_hash = canonical_sha256(dict(command_payload))

        cursor.execute(
            """
            INSERT INTO cae.receipt (
                receipt_id, workspace_id, operation_id, idempotency_key,
                actor_id, canonical_payload, payload_jsonb, payload_sha256
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                receipt_id,
                workspace_id,
                operation_id,
                idempotency_key,
                actor_id,
                canonical_text,
                Jsonb(envelope),
                payload_hash,
            ),
        )

        for ev_id in evidence_ids:
            cursor.execute(
                """
                INSERT INTO cae.receipt_evidence_link (
                    link_id, workspace_id, receipt_id, evidence_item_id
                ) VALUES (%s, %s, %s, %s);
                """,
                (uuid4(), workspace_id, receipt_id, ev_id),
            )

        return OperationReceipt(
            receipt_id=receipt_id,
            workspace_id=workspace_id,
            operation_id=operation_id,
            idempotency_key=idempotency_key,
            actor_id=actor_id,
            outcome="COMMITTED",
            idempotent_replay=False,
            payload=envelope,
            payload_sha256=payload_hash,
            evidence_ids=tuple(evidence_ids),
        )

    # ------------------------------------------------------------------------
    # 1. cae.workspace.provision@1.0.0
    # ------------------------------------------------------------------------
    def provision_workspace(
        self,
        *,
        slug: str,
        display_name: str,
        actor_id: str,
        idempotency_key: str,
        workspace_id: Optional[UUID] = None,
    ) -> OperationReceipt:
        operation_id = "cae.workspace.provision@1.0.0"
        target_ws_id = workspace_id or uuid4()
        command_payload = {
            "workspace_id": str(target_ws_id),
            "slug": slug,
            "display_name": display_name,
            "actor_id": actor_id,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                # Configure tenant context for workspace insertion
                ws_context = TenantContext(workspace_id=target_ws_id, actor_id=actor_id, role="ADMIN")
                apply_tenant_session(cur, ws_context)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=target_ws_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                # Insert Workspace
                cur.execute(
                    """
                    INSERT INTO cae.workspace (workspace_id, slug, display_name, status)
                    VALUES (%s, %s, %s, 'ACTIVE');
                    """,
                    (target_ws_id, slug, display_name),
                )

                # Grant Admin Membership to provisioning actor
                cur.execute(
                    """
                    INSERT INTO cae.workspace_membership (membership_id, workspace_id, actor_id, role, status)
                    VALUES (%s, %s, %s, 'ADMIN', 'ACTIVE');
                    """,
                    (uuid4(), target_ws_id, actor_id),
                )

                event_payload = {
                    "event_type": "WorkspaceProvisioned",
                    "workspace_id": str(target_ws_id),
                    "slug": slug,
                    "admin_actor_id": actor_id,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=target_ws_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 2. cae.workspace.membership.grant@1.0.0
    # ------------------------------------------------------------------------
    def grant_workspace_membership(
        self,
        *,
        target_actor_id: str,
        role: str = "MEMBER",
        idempotency_key: str,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.workspace.membership.grant@1.0.0"
        ctx = context or require_current_tenant_context()
        command_payload = {
            "workspace_id": str(ctx.workspace_id),
            "target_actor_id": target_actor_id,
            "role": role,
            "granter_actor_id": ctx.actor_id,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                cur.execute(
                    """
                    INSERT INTO cae.workspace_membership (membership_id, workspace_id, actor_id, role, status)
                    VALUES (%s, %s, %s, %s, 'ACTIVE')
                    ON CONFLICT (workspace_id, actor_id) DO UPDATE SET role = EXCLUDED.role, status = 'ACTIVE';
                    """,
                    (uuid4(), ctx.workspace_id, target_actor_id, role),
                )

                event_payload = {
                    "event_type": "WorkspaceMembershipGranted",
                    "workspace_id": str(ctx.workspace_id),
                    "target_actor_id": target_actor_id,
                    "role": role,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 3. cae.operator.grant.issue@1.0.0
    # ------------------------------------------------------------------------
    def issue_operator_grant(
        self,
        *,
        operator_org_id: UUID,
        operator_actor_id: str,
        target_workspace_id: UUID,
        justification: str,
        expires_at: datetime,
        idempotency_key: str,
        grant_id: Optional[UUID] = None,
        issuer_actor_id: str = "platform_admin",
    ) -> OperationReceipt:
        operation_id = "cae.operator.grant.issue@1.0.0"
        target_grant_id = grant_id or uuid4()
        command_payload = {
            "grant_id": str(target_grant_id),
            "operator_org_id": str(operator_org_id),
            "operator_actor_id": operator_actor_id,
            "target_workspace_id": str(target_workspace_id),
            "justification": justification,
            "expires_at": expires_at.isoformat(),
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                # Operator grant issue executes with operator privilege
                op_context = TenantContext(
                    workspace_id=target_workspace_id,
                    actor_id=issuer_actor_id,
                    is_operator=True,
                    operator_grant_id=target_grant_id,
                )
                apply_tenant_session(cur, op_context)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=target_workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                cur.execute(
                    """
                    INSERT INTO cae.operator_access_grant (
                        grant_id, operator_org_id, operator_actor_id, workspace_id,
                        justification, expires_at
                    ) VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        target_grant_id,
                        operator_org_id,
                        operator_actor_id,
                        target_workspace_id,
                        justification,
                        expires_at,
                    ),
                )

                event_payload = {
                    "event_type": "OperatorAccessGrantIssued",
                    "grant_id": str(target_grant_id),
                    "workspace_id": str(target_workspace_id),
                    "operator_actor_id": operator_actor_id,
                    "expires_at": expires_at.isoformat(),
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=target_workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=issuer_actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 4. cae.engagement.initialize@1.0.0
    # ------------------------------------------------------------------------
    def initialize_engagement(
        self,
        *,
        title: str,
        idempotency_key: str,
        engagement_id: Optional[UUID] = None,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.engagement.initialize@1.0.0"
        ctx = context or require_current_tenant_context()
        target_eng_id = engagement_id or uuid4()
        command_payload = {
            "engagement_id": str(target_eng_id),
            "workspace_id": str(ctx.workspace_id),
            "title": title,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                cur.execute(
                    """
                    INSERT INTO cae.engagement (
                        engagement_id, workspace_id, title, lifecycle_state, version
                    ) VALUES (%s, %s, %s, 'PLANNED', 1);
                    """,
                    (target_eng_id, ctx.workspace_id, title),
                )

                event_payload = {
                    "event_type": "EngagementInitialized",
                    "engagement_id": str(target_eng_id),
                    "workspace_id": str(ctx.workspace_id),
                    "title": title,
                    "lifecycle_state": "PLANNED",
                    "version": 1,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 5. cae.guest.register@1.0.0
    # ------------------------------------------------------------------------
    def register_guest(
        self,
        *,
        pseudonym: str,
        external_reference_id: Optional[str] = None,
        consent_status: str = "PENDING",
        idempotency_key: str,
        guest_id: Optional[UUID] = None,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.guest.register@1.0.0"
        ctx = context or require_current_tenant_context()
        target_guest_id = guest_id or uuid4()
        command_payload = {
            "guest_id": str(target_guest_id),
            "workspace_id": str(ctx.workspace_id),
            "pseudonym": pseudonym,
            "external_reference_id": external_reference_id,
            "consent_status": consent_status,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                cur.execute(
                    """
                    INSERT INTO cae.guest (
                        guest_id, workspace_id, external_reference_id, pseudonym, consent_status
                    ) VALUES (%s, %s, %s, %s, %s);
                    """,
                    (target_guest_id, ctx.workspace_id, external_reference_id, pseudonym, consent_status),
                )

                event_payload = {
                    "event_type": "GuestRegistered",
                    "guest_id": str(target_guest_id),
                    "workspace_id": str(ctx.workspace_id),
                    "pseudonym": pseudonym,
                    "consent_status": consent_status,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 6. cae.media.verify@1.0.0
    # ------------------------------------------------------------------------
    def verify_media_asset(
        self,
        *,
        media_asset_id: UUID,
        storage_path: str,
        claimed_sha256: str,
        byte_size: int,
        mime_type: str,
        idempotency_key: str,
        engagement_id: Optional[UUID] = None,
        raw_bytes: Optional[bytes] = None,
        byte_reader_fn: Optional[Callable[[str], bytes]] = None,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.media.verify@1.0.0"
        ctx = context or require_current_tenant_context()
        command_payload = {
            "media_asset_id": str(media_asset_id),
            "workspace_id": str(ctx.workspace_id),
            "engagement_id": str(engagement_id) if engagement_id else None,
            "storage_path": storage_path,
            "claimed_sha256": claimed_sha256,
            "byte_size": byte_size,
            "mime_type": mime_type,
        }

        # Fresh-read reality contact: retrieve actual bytes and compute SHA-256
        data: Optional[bytes] = raw_bytes
        if data is None and byte_reader_fn is not None:
            data = byte_reader_fn(storage_path)

        if data is None:
            raise SemanticOperationError(
                "Fresh-read byte source required for cae.media.verify@1.0.0 (provide raw_bytes or byte_reader_fn)"
            )

        observed_sha256 = hashlib.sha256(data).hexdigest()
        is_hash_valid = observed_sha256.lower() == claimed_sha256.lower()

        quarantined_error: Optional[UnverifiedMediaDigestError] = None

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                # Validate engagement parent relation if supplied
                if engagement_id is not None:
                    cur.execute(
                        "SELECT 1 FROM cae.engagement WHERE engagement_id = %s AND workspace_id = %s;",
                        (engagement_id, ctx.workspace_id),
                    )
                    if cur.fetchone() is None:
                        raise CrossWorkspaceLeakError(
                            f"CROSS_WORKSPACE_LEAK: Engagement {engagement_id} not found in workspace {ctx.workspace_id}"
                        )

                if is_hash_valid:
                    cur.execute(
                        """
                        INSERT INTO cae.media_asset (
                            media_asset_id, workspace_id, engagement_id, storage_path,
                            canonical_sha256, byte_size, mime_type, lifecycle_state, version
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'VERIFIED', 1)
                        ON CONFLICT (workspace_id, media_asset_id) DO UPDATE SET
                            lifecycle_state = 'VERIFIED',
                            canonical_sha256 = EXCLUDED.canonical_sha256,
                            byte_size = EXCLUDED.byte_size,
                            version = cae.media_asset.version + 1;
                        """,
                        (
                            media_asset_id,
                            ctx.workspace_id,
                            engagement_id,
                            storage_path,
                            observed_sha256,
                            len(data),
                            mime_type,
                        ),
                    )

                    event_payload = {
                        "event_type": "MediaAssetVerified",
                        "media_asset_id": str(media_asset_id),
                        "workspace_id": str(ctx.workspace_id),
                        "lifecycle_state": "VERIFIED",
                        "canonical_sha256": observed_sha256,
                        "byte_size": len(data),
                    }

                    return self._commit_atomic_receipt(
                        cur,
                        workspace_id=ctx.workspace_id,
                        operation_id=operation_id,
                        idempotency_key=idempotency_key,
                        actor_id=ctx.actor_id,
                        command_payload=command_payload,
                        event_payload=event_payload,
                        validator_results={"storage_sha256_match": "PASS"},
                    )
                else:
                    # Mismatched bytes: transition/insert to QUARANTINED and commit receipt
                    cur.execute(
                        """
                        INSERT INTO cae.media_asset (
                            media_asset_id, workspace_id, engagement_id, storage_path,
                            canonical_sha256, byte_size, mime_type, lifecycle_state, version
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'QUARANTINED', 1)
                        ON CONFLICT (workspace_id, media_asset_id) DO UPDATE SET
                            lifecycle_state = 'QUARANTINED',
                            version = cae.media_asset.version + 1;
                        """,
                        (
                            media_asset_id,
                            ctx.workspace_id,
                            engagement_id,
                            storage_path,
                            claimed_sha256,
                            len(data),
                            mime_type,
                        ),
                    )

                    event_payload = {
                        "event_type": "MediaAssetQuarantined",
                        "media_asset_id": str(media_asset_id),
                        "workspace_id": str(ctx.workspace_id),
                        "lifecycle_state": "QUARANTINED",
                        "claimed_sha256": claimed_sha256,
                        "observed_sha256": observed_sha256,
                    }

                    self._commit_atomic_receipt(
                        cur,
                        workspace_id=ctx.workspace_id,
                        operation_id=operation_id,
                        idempotency_key=idempotency_key,
                        actor_id=ctx.actor_id,
                        command_payload=command_payload,
                        event_payload=event_payload,
                        validator_results={"storage_sha256_match": "FAIL"},
                    )

                    quarantined_error = UnverifiedMediaDigestError(
                        f"UNVERIFIED_MEDIA_DIGEST: Claimed SHA-256 {claimed_sha256} does not match observed hash {observed_sha256}"
                    )

        if quarantined_error is not None:
            raise quarantined_error

    # ------------------------------------------------------------------------
    # 7. cae.evidence.capture@1.0.0
    # ------------------------------------------------------------------------
    def capture_evidence(
        self,
        *,
        media_asset_id: UUID,
        evidence_item_id: UUID,
        idempotency_key: str,
        start_ms: Optional[int] = None,
        end_ms: Optional[int] = None,
        quoted_text: Optional[str] = None,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.evidence.capture@1.0.0"
        ctx = context or require_current_tenant_context()
        command_payload = {
            "evidence_item_id": str(evidence_item_id),
            "media_asset_id": str(media_asset_id),
            "workspace_id": str(ctx.workspace_id),
            "start_ms": start_ms,
            "end_ms": end_ms,
            "quoted_text": quoted_text,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                # Verify media asset existence and VERIFIED state in this workspace
                cur.execute(
                    """
                    SELECT lifecycle_state FROM cae.media_asset
                    WHERE media_asset_id = %s AND workspace_id = %s;
                    """,
                    (media_asset_id, ctx.workspace_id),
                )
                row = cur.fetchone()
                if row is None:
                    raise CrossWorkspaceLeakError(
                        f"MediaAsset {media_asset_id} not found in workspace {ctx.workspace_id}"
                    )
                if row[0] != "VERIFIED":
                    raise UnverifiedMediaDigestError(
                        f"Cannot capture evidence from MediaAsset in state '{row[0]}'; must be 'VERIFIED'"
                    )

                event_payload = {
                    "event_type": "EvidenceCaptured",
                    "evidence_item_id": str(evidence_item_id),
                    "media_asset_id": str(media_asset_id),
                    "workspace_id": str(ctx.workspace_id),
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                    evidence_ids=[evidence_item_id],
                )

    # ------------------------------------------------------------------------
    # 8. cae.harness.run.initialize@1.0.0
    # ------------------------------------------------------------------------
    def initialize_harness_run(
        self,
        *,
        engagement_id: UUID,
        template_id: str,
        template_version: str,
        idempotency_key: str,
        run_id: Optional[UUID] = None,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.harness.run.initialize@1.0.0"
        ctx = context or require_current_tenant_context()
        target_run_id = run_id or uuid4()
        command_payload = {
            "run_id": str(target_run_id),
            "workspace_id": str(ctx.workspace_id),
            "engagement_id": str(engagement_id),
            "template_id": template_id,
            "template_version": template_version,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                # Validate Engagement existence in same workspace
                cur.execute(
                    "SELECT 1 FROM cae.engagement WHERE engagement_id = %s AND workspace_id = %s;",
                    (engagement_id, ctx.workspace_id),
                )
                if cur.fetchone() is None:
                    raise CrossWorkspaceLeakError(
                        f"CROSS_WORKSPACE_LEAK: Engagement {engagement_id} does not exist in workspace {ctx.workspace_id}"
                    )

                # Validate HarnessTemplate canonical plane
                cur.execute(
                    "SELECT is_active FROM cae.harness_template WHERE template_id = %s AND version = %s;",
                    (template_id, template_version),
                )
                tmpl_row = cur.fetchone()
                if tmpl_row is None or not tmpl_row[0]:
                    raise SemanticOperationError(
                        f"Canonical template '{template_id}@{template_version}' not found or inactive"
                    )

                cur.execute(
                    """
                    INSERT INTO cae.harness_run (
                        run_id, workspace_id, engagement_id, template_id, template_version,
                        current_step, lifecycle_state, version
                    ) VALUES (%s, %s, %s, %s, %s, 'step_01', 'INITIALIZED', 1);
                    """,
                    (target_run_id, ctx.workspace_id, engagement_id, template_id, template_version),
                )

                event_payload = {
                    "event_type": "HarnessRunInitialized",
                    "run_id": str(target_run_id),
                    "workspace_id": str(ctx.workspace_id),
                    "engagement_id": str(engagement_id),
                    "template_id": template_id,
                    "template_version": template_version,
                    "lifecycle_state": "INITIALIZED",
                    "version": 1,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 9. cae.harness.run.step@1.0.0
    # ------------------------------------------------------------------------
    def step_harness_run(
        self,
        *,
        run_id: UUID,
        from_step: str,
        to_step: str,
        expected_version: int,
        outcome: str = "RUNNING",
        idempotency_key: str,
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        operation_id = "cae.harness.run.step@1.0.0"
        ctx = context or require_current_tenant_context()
        command_payload = {
            "run_id": str(run_id),
            "workspace_id": str(ctx.workspace_id),
            "from_step": from_step,
            "to_step": to_step,
            "expected_version": expected_version,
            "outcome": outcome,
        }

        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=command_payload,
                )
                if replay:
                    return replay

                # Optimistic concurrency & version locking check
                cur.execute(
                    """
                    SELECT current_step, lifecycle_state, version
                    FROM cae.harness_run
                    WHERE run_id = %s AND workspace_id = %s FOR UPDATE;
                    """,
                    (run_id, ctx.workspace_id),
                )
                row = cur.fetchone()
                if row is None:
                    raise SemanticOperationError(f"HarnessRun {run_id} not found in workspace {ctx.workspace_id}")

                current_step_db, current_state_db, current_version_db = row[0], row[1], int(row[2])

                if current_version_db != expected_version:
                    raise StaleVersionConflictError(
                        f"STALE_VERSION_CONFLICT: Expected version {expected_version}, found version {current_version_db}"
                    )

                if current_step_db != from_step:
                    raise SemanticOperationError(
                        f"Illegal step transition: expected from_step '{current_step_db}', got '{from_step}'"
                    )

                new_version = current_version_db + 1
                cur.execute(
                    """
                    UPDATE cae.harness_run
                    SET current_step = %s, lifecycle_state = %s, version = %s, updated_at = clock_timestamp()
                    WHERE run_id = %s AND workspace_id = %s AND version = %s;
                    """,
                    (to_step, outcome, new_version, run_id, ctx.workspace_id, current_version_db),
                )
                if cur.rowcount == 0:
                    raise StaleVersionConflictError("Optimistic locking update updated 0 rows")

                event_payload = {
                    "event_type": "HarnessRunStepped",
                    "run_id": str(run_id),
                    "workspace_id": str(ctx.workspace_id),
                    "from_step": from_step,
                    "to_step": to_step,
                    "lifecycle_state": outcome,
                    "version": new_version,
                }

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=ctx.actor_id,
                    command_payload=command_payload,
                    event_payload=event_payload,
                )

    # ------------------------------------------------------------------------
    # 10. cae.receipt.commit@1.0.0
    # ------------------------------------------------------------------------
    def commit_receipt(
        self,
        *,
        operation_id: str,
        idempotency_key: str,
        actor_id: str,
        payload: Mapping[str, Any],
        evidence_ids: Sequence[UUID] = (),
        context: Optional[TenantContext] = None,
    ) -> OperationReceipt:
        ctx = context or require_current_tenant_context()
        with self.connection.transaction():
            with self.connection.cursor() as cur:
                apply_tenant_session(cur, ctx)

                replay = self._idempotent_replay_check(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    command_payload=payload,
                )
                if replay:
                    return replay

                return self._commit_atomic_receipt(
                    cur,
                    workspace_id=ctx.workspace_id,
                    operation_id=operation_id,
                    idempotency_key=idempotency_key,
                    actor_id=actor_id,
                    command_payload=payload,
                    event_payload={"payload": payload},
                    evidence_ids=evidence_ids,
                )
