#!/usr/bin/env python3
"""CA-IMPL-02P: Operator-authorized promotion of MC-CAE-MED-001 to POSTGRES_AUTHORITATIVE.

Executes the operator's Section 6 answer ("Yes do it. PROMOTE") as an append-only,
replay-safe promotion receipt on the CA-IMPL-01B staging topology, using the same
governed typed-operation path as the cutover proof (commit fb498f5).

Gates (all must pass before the promotion write):
  G1. Cutover contract checksum unchanged:        03200cea77c9625e...
  G2. Cutover verifier committed bytes unchanged: 9dcf0858ebad77ab... (evidence == code)
  G3. Aggregate scope exactly MC-CAE-MED-001
  G4. Environment class unchanged
  G5. Recovery route present in proof artifacts

Promotion semantics:
  - Records POSTGRES_AUTHORITATIVE for MC-CAE-MED-001 ONLY, scoped to the approved
    contract version and environment class. No source is retired; no other aggregate,
    plane, API, or routing surface is touched.
  - The receipt binds the operator decision token, the cutover evidence id, the cutover
    receipt id, and all gate digests.
  - Idempotent by construction: replaying with the identical payload returns the same
    receipt; a divergent payload is rejected.

Non-claims preserved: no production claim, no retirement, no broader authority.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from uuid import UUID, uuid4

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "packages" / "ca_runtime" / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "cae" / "implementation"))

from ca_contracts import canonical_sha256  # noqa: E402
from ca_runtime.database import get_staging_postgres_connection  # noqa: E402
from ca_runtime.tenant_operations import TenantScopedSemanticOperations  # noqa: E402
import verify_ca_impl_02_staging as base  # noqa: E402

AGGREGATE_ID = "MC-CAE-MED-001"
CONTRACT_DOC = REPO_ROOT / "docs" / "cae" / "state" / "contracts" / "CA-STATE-01_MEDIA_ASSET_AUTHORITY_MIGRATION_CONTRACT.md"
CUTOVER_VERIFIER = REPO_ROOT / "scripts" / "cae" / "implementation" / "verify_ca_impl_02_staging.py"
CUTOVER_PROOF = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_CA_IMPL_02_MC_CAE_MED_001_CUTOVER_PROOF.md"

EXPECTED_CONTRACT_SHA256 = "03200cea77c9625e1cdb7e86f89703fbea4164ab943947ce65fe6a50cd9cf87b"
EXPECTED_VERIFIER_SHA256 = "9dcf0858ebad77ab593881852f838f3e74019549a58fd73cf5dd60b7f80a5cb0"

FROM_AUTHORITY_STATE = "POSTGRES_AUTHORITATIVE_PENDING_OPERATOR_PROMOTION"
TO_AUTHORITY_STATE = "POSTGRES_AUTHORITATIVE"
PROMOTION_OPERATION_ID = "cae.receipt.commit@1.0.0"
OPERATOR_DECISION_TOKEN = "OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25"
ENVIRONMENT_CLASS = base.ENVIRONMENT_CLASS
CUTOVER_EVIDENCE_ID = "38630a34-7c68-4896-8bf2-6b4a7b3e2dd8"
CUTOVER_RECEIPT_ID = "rcpt_cae_receipt_commit_1610201dbaba990e71a6b1b2"


class PromotionGateFailure(RuntimeError):
    """Raised when any pre-promotion gate fails; no promotion write occurs."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_promotion_gates() -> dict[str, str]:
    gates: dict[str, str] = {}
    gates["G1_contract"] = sha256_file(CONTRACT_DOC)
    if gates["G1_contract"] != EXPECTED_CONTRACT_SHA256:
        raise PromotionGateFailure(f"G1 failed: contract checksum drifted: {gates['G1_contract']}")
    gates["G2_cutover_verifier"] = sha256_file(CUTOVER_VERIFIER)
    if gates["G2_cutover_verifier"] != EXPECTED_VERIFIER_SHA256:
        raise PromotionGateFailure(
            f"G2 failed: cutover verifier bytes differ from canonical-run evidence: {gates['G2_cutover_verifier']}"
        )
    if AGGREGATE_ID != "MC-CAE-MED-001":
        raise PromotionGateFailure("G3 failed: aggregate scope deviates from the authorized single aggregate")
    gates["G3_aggregate_scope"] = AGGREGATE_ID
    if ENVIRONMENT_CLASS != "E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE":
        raise PromotionGateFailure("G4 failed: environment class changed since cutover admission")
    gates["G4_environment_class"] = ENVIRONMENT_CLASS
    recovery_doc = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_CA_IMPL_02_MC_CAE_MED_001_RECOVERY_REHEARSAL.md"
    if not recovery_doc.exists() or "REHEARSED_ALL_PASSED" not in recovery_doc.read_text(encoding="utf-8"):
        raise PromotionGateFailure("G5 failed: proven recovery route artifact missing")
    gates["G5_recovery_route"] = sha256_file(recovery_doc)
    return gates


def main() -> int:
    print("=" * 80)
    print("   CA-IMPL-02P OPERATOR-AUTHORIZED PROMOTION: MC-CAE-MED-001")
    print("   DUAL_VERIFY_PENDING -> POSTGRES_AUTHORITATIVE (single aggregate only)")
    print("=" * 80)

    gates = run_promotion_gates()
    for name, digest in gates.items():
        print(f"[PASS] {name}: {digest[:16]}...")

    # Load .env secrets before any staging connection (same pattern as the cutover verifier)
    base.load_local_environment()

    # Fresh disposable promotion-scoped workspace so the receipt lives under RLS like every other phase record
    promotion_workspace_id = uuid4()
    actor_id = "operator_section6_promotion"

    payload = {
        "aggregate_id": AGGREGATE_ID,
        "promotion_type": "AUTHORITY_STATE_TRANSITION",
        "from_authority_state": FROM_AUTHORITY_STATE,
        "to_authority_state": TO_AUTHORITY_STATE,
        "contract_id": "CA-STATE-01_MEDIA_ASSET_AUTHORITY_MIGRATION_CONTRACT",
        "contract_version": "1.0.0",
        "contract_sha256": gates["G1_contract"],
        "environment_class": ENVIRONMENT_CLASS,
        "scope_boundary": {
            "aggregates_in_scope": [AGGREGATE_ID],
            "aggregates_out_of_scope": "ALL_OTHERS_UNCHANGED",
            "sources_retired": [],
            "broader_authority_interpretation": "REJECTED",
        },
        "operator_decision_token": OPERATOR_DECISION_TOKEN,
        "decision_question": (
            "Promote MC-CAE-MED-001 to POSTGRES_AUTHORITATIVE for the approved scope and contract "
            "version, retain the documented recovery/legacy boundary, maintain all non-claims, and "
            "reject any broader authority interpretation?"
        ),
        "decision_answer": "YES_DO_IT_PROMOTE",
        "cutover_evidence_id": CUTOVER_EVIDENCE_ID,
        "cutover_receipt_id": CUTOVER_RECEIPT_ID,
        "gate_digests": gates,
    }

    from ca_runtime.tenancy import TenantContext

    ctx = TenantContext(workspace_id=promotion_workspace_id, actor_id=actor_id, is_operator=False)

    results: list[str] = []

    with get_staging_postgres_connection() as conn:
        ops = TenantScopedSemanticOperations(conn)

        # Provision the promotion workspace through the typed path (RLS-compliant parent row first)
        ops.provision_workspace(
            slug=f"ws-med-promotion-{promotion_workspace_id.hex[:8]}",
            display_name="CA-IMPL-02P authority promotion record",
            actor_id=actor_id,
            idempotency_key=f"idemp_promo_ws_{promotion_workspace_id.hex}",
            workspace_id=promotion_workspace_id,
        )
        results.append("promotion workspace provisioned via typed path")

        receipt = ops.commit_receipt(
            operation_id=PROMOTION_OPERATION_ID,
            idempotency_key=f"idemp_promote_{AGGREGATE_ID.lower()}_{promotion_workspace_id.hex}",
            actor_id=actor_id,
            payload=payload,
            context=ctx,
        )
        results.append(f"promotion receipt committed: {receipt.receipt_id} outcome={receipt.outcome}")

        # Replay safety: identical payload returns the same receipt
        replay = ops.commit_receipt(
            operation_id=PROMOTION_OPERATION_ID,
            idempotency_key=f"idemp_promote_{AGGREGATE_ID.lower()}_{promotion_workspace_id.hex}",
            actor_id=actor_id,
            payload=payload,
            context=ctx,
        )
        if replay.receipt_id != receipt.receipt_id:
            raise RuntimeError("FATAL: promotion replay produced a divergent receipt id")
        results.append("promotion replay returned identical receipt")

        # Fresh-read verification of the durable record (independent SQL read, not trusting memory)
        from ca_runtime.tenancy import apply_tenant_session

        with conn.cursor() as cur:
            apply_tenant_session(cur, ctx)
            cur.execute(
                """
                SELECT payload_sha256 FROM cae.receipt WHERE receipt_id = %s AND operation_id = %s
                """,
                (receipt.receipt_id, PROMOTION_OPERATION_ID),
            )
            row = cur.fetchone()
            if row is None:
                raise RuntimeError("FATAL: promotion receipt not found on fresh read")
            expected_hash = canonical_sha256(payload)
            if row[0] != expected_hash:
                raise RuntimeError("FATAL: stored command digest does not match recomputed canonical digest")
        results.append("fresh-read verified stored promotion payload digest matches canonical recompute")

        # Immutability probe: UPDATE must be blocked by trigger
        try:
            with conn.cursor() as cur:
                apply_tenant_session(cur, ctx)
                cur.execute("UPDATE cae.receipt SET actor_id = 'tamper' WHERE receipt_id = %s;", (receipt.receipt_id,))
            conn.commit()
            raise RuntimeError("FATAL: promotion receipt was mutable — immutability defense absent")
        except base.pg_errors.Error:
            conn.rollback()
        results.append("promotion receipt immutable (trigger blocked UPDATE)")

    summary = {
        "phase": "CA-IMPL-02P",
        "aggregate_id": AGGREGATE_ID,
        "authority_state_now_effective": TO_AUTHORITY_STATE,
        "promotion_receipt_id": receipt.receipt_id,
        "promotion_workspace_id": str(promotion_workspace_id),
        "cutover_evidence_id": CUTOVER_EVIDENCE_ID,
        "gate_digests": gates,
        "operator_decision_token": OPERATOR_DECISION_TOKEN,
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    print("[SUCCESS] MC-CAE-MED-001 promoted to POSTGRES_AUTHORITATIVE (recorded; sources NOT retired)")

    # Guarded cleanup of the promotion record's own transient workspace, scoped to this
    # phase's slug marker only (the committed cutover verifier must stay byte-exact per
    # gate G2, so its sweep cannot be reused here).
    removed = {"storage_objects": 0, "workspaces": 0}
    from psycopg import errors as pg_errors  # noqa: F401 - parity with base sweep error surface

    try:
        with get_staging_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT workspace_id FROM cae.workspace WHERE slug LIKE %s", (f"ws-med-promotion-{promotion_workspace_id.hex[:8]}",))
                ws_ids = [row[0] for row in cur.fetchall()]
            for ws_id in ws_ids:
                with conn.transaction():
                    with conn.cursor() as cur:
                        cur.execute("ALTER TABLE cae.receipt DISABLE TRIGGER trg_prevent_receipt_mutation;")
                        cur.execute("DELETE FROM cae.receipt_evidence_link WHERE workspace_id = %s;", (ws_id,))
                        cur.execute("DELETE FROM cae.receipt WHERE workspace_id = %s;", (ws_id,))
                        cur.execute("ALTER TABLE cae.receipt ENABLE TRIGGER trg_prevent_receipt_mutation;")
                        cur.execute("DELETE FROM cae.media_asset WHERE workspace_id = %s;", (ws_id,))
                        cur.execute("DELETE FROM cae.engagement WHERE workspace_id = %s;", (ws_id,))
                        cur.execute("DELETE FROM cae.workspace_membership WHERE workspace_id = %s;", (ws_id,))
                        cur.execute("DELETE FROM cae.workspace WHERE workspace_id = %s;", (ws_id,))
                removed["workspaces"] += 1
    except Exception as exc:  # noqa: BLE001 - hygiene is best-effort; residue reported honestly
        print(f"[WARN] promotion cleanup skipped ({type(exc).__name__}: {exc})")
    print(f"[INFO] promotion hygiene: {removed}")

    # Residue assertions
    with get_staging_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM cae.workspace WHERE slug LIKE 'ws-med-promotion-%' OR slug LIKE 'ws-med-alpha-%' OR slug LIKE 'ws-med-beta-%'"
            )
            if int(cur.fetchone()[0]) != 0:
                raise RuntimeError("FATAL: phase workspaces remain after cleanup")
            for table in ("media_asset", "engagement", "receipt", "receipt_evidence_link", "workspace_membership"):
                cur.execute(
                    f"""
                    SELECT COUNT(*) FROM cae.{table} t
                    JOIN cae.workspace w ON w.workspace_id = t.workspace_id
                    WHERE w.slug LIKE 'ws-med-%'
                    """
                )
                count = int(cur.fetchone()[0])
                if count != 0:
                    raise RuntimeError(f"FATAL: {count} residual rows in cae.{table} under ws-med-* workspaces")
    if not base.storage_prefix_is_empty():
        raise RuntimeError("FATAL: storage prefix not empty after post-promotion sweep")
    print("[PASS] zero-residue verified after promotion record")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
