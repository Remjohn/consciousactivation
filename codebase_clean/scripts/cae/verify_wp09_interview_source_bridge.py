"""Repository-integrated staging proof for the bounded WP-09 source bridge."""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import uuid
from pathlib import Path

import psycopg
import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [
    str(ROOT / "packages" / "ca_contracts" / "src"),
    str(ROOT / "packages" / "ca_runtime" / "src"),
    str(ROOT / "services" / "interview" / "src"),
]

from ca_contracts import canonical_sha256  # noqa: E402
from ca_runtime.interview_source_bridge import (  # noqa: E402
    InterviewExpressionSourceBridge,
    InterviewSourceBridgeError,
)
from ca_runtime.semantic_operations import (  # noqa: E402
    FirstSliceSemanticOperations,
    SemanticOperationError,
)
from conscious_activations_interview_expression.application import InterviewExpressionApplication  # noqa: E402
from conscious_activations_interview_expression.domain import make_media_asset  # noqa: E402
from verify_wp03_first_slice import BUCKET, PROJECT_URL, connection_url, load_local_environment  # noqa: E402


SECRET_VARIABLE = "CAE_SUPABASE_SECRET_KEY"
MANIFEST = ROOT / "docs" / "cae" / "evaluations" / "INTERVIEW_SOURCE_BRIDGE_WP09_EVALUATION_SUITE.yaml"


def assert_raises(callback: object, error_type: type[Exception]) -> bool:
    try:
        callback()  # type: ignore[operator]
    except error_type:
        return True
    return False


def main() -> int:
    load_local_environment()
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    expected_test_ids = {"WP09-INT-001", "WP09-RH-001", "WP09-RH-002", "WP09-STATE-001", "WP09-INT-002"}
    required_test_fields = {
        "test_id", "claim_id", "class", "subject", "preconditions", "fixture_source",
        "required_environment_fidelity", "actual_environment_fidelity", "execution_path",
        "assertions", "expected_failure_mode", "reward_hacking_scenario", "taste_risk",
        "anticentroid_risk", "evidence_status", "receipt_required",
    }
    manifest_is_governed = (
        manifest.get("suite_id") == "cae.interview_source_bridge.wp09"
        and {test.get("test_id") for test in manifest.get("tests", [])} == expected_test_ids
        and all(required_test_fields <= set(test) for test in manifest.get("tests", []))
    )
    secret = os.environ.get(SECRET_VARIABLE, "")
    if not secret or secret == "***":
        print("wp09_proof=NOT_CONFIGURED")
        return 2
    proof_id = uuid.uuid4().hex
    workspace_id = f"proof-wp09-{proof_id}"
    project_id = f"proof-project-{proof_id}"
    bridge_actor = f"proof:bridge:{proof_id}"
    capture_actor = f"proof:capturer:{proof_id}"
    storage_key: str | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="cae-wp09-") as temporary:
            root = Path(temporary)
            media_root = root / "media"
            source_bytes = b"A source sentence preserved through the Interview Expression bridge.\n"
            source_sha = hashlib.sha256(source_bytes).hexdigest()
            local_media = media_root / "interviews" / workspace_id / project_id / "source.txt"
            local_media.parent.mkdir(parents=True)
            local_media.write_bytes(source_bytes)
            interview = InterviewExpressionApplication(root / "interview.sqlite3")
            interview.initialize()
            legacy_media = make_media_asset(
                logical_uri=f"workspace://{workspace_id}/{project_id}/source.txt",
                sha256=source_sha,
                bytes_count=len(source_bytes),
                media_type="text/plain",
                technical={"probe_status": "PROBED", "duration_ms": len(source_bytes)},
            )
            admitted = interview.source_packages.admit(
                {
                    "workspace_id": workspace_id,
                    "project_id": project_id,
                    "admission_mode": "IMPORTED",
                    "source_kind": "INTERVIEW_EXPRESSION",
                    "media_assets": [legacy_media],
                    "source_authority": {
                        "operator_id": "wp09-operator",
                        "authority_scope": "DEVELOPMENT_EVIDENCE_ONLY",
                        "assertion_id": "wp09-source-authority",
                    },
                    "planning_lineage": {"state": "ABSENT_NOT_CREATED"},
                },
                idempotency_key=f"admit:{proof_id}",
            )
            legacy_source = admitted["object"]
            legacy_hash_before = legacy_source["sha256"]
            legacy_revision_before = legacy_source["revision"]

            with psycopg.connect(connection_url(), connect_timeout=10) as connection:
                with connection.transaction(force_rollback=True):
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO cae.workspace(workspace_id, display_name) VALUES (%s, 'WP-09 proof')", (workspace_id,))
                        cursor.execute("INSERT INTO cae.project(project_id, workspace_id, display_name) VALUES (%s, %s, 'WP-09 proof project')", (project_id, workspace_id))
                        for actor_id, subject in ((bridge_actor, f"bridge-{proof_id}"), (capture_actor, f"capture-{proof_id}")):
                            cursor.execute(
                                "INSERT INTO cae.actor(actor_id, workspace_id, actor_kind, external_subject) VALUES (%s, %s, 'SERVICE', %s)",
                                (actor_id, workspace_id, subject),
                            )
                    bridge = InterviewExpressionSourceBridge(
                        connection,
                        media_root=media_root,
                        supabase_url=PROJECT_URL,
                        secret_key=secret,
                        bucket=BUCKET,
                    )
                    receipt, storage_key = bridge.bridge_source_package(
                        legacy_source=legacy_source,
                        bridge_actor_id=bridge_actor,
                        idempotency_key=f"bridge:{proof_id}",
                    )
                    bridged_source_id = receipt.payload["aggregate_id"]
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            SELECT media.content_sha256, media.byte_size, media.lifecycle_state,
                              source.source_kind, aggregate.current_state, aggregate.version,
                              execution.claim_id, execution.evidence_status,
                              execution.registry_scope, receipt.payload -> 'independent_evidence_refs'
                            FROM cae.media_asset media
                            JOIN cae.source_package source ON source.media_asset_id = media.asset_id
                            JOIN cae.state_aggregate aggregate ON aggregate.aggregate_id = source.source_package_id
                            JOIN cae.receipt receipt ON receipt.receipt_id = %s
                            JOIN cae.execution_receipt execution ON execution.receipt_id = receipt.receipt_id
                            WHERE source.source_package_id = %s
                            """,
                            (receipt.receipt_id, bridged_source_id),
                        )
                        registered = cursor.fetchone()
                    verified_registration = bool(registered) and (
                        registered[0] == source_sha and int(registered[1]) == len(source_bytes)
                        and registered[2] == "VERIFIED" and registered[3] == "INTERVIEW_EXPRESSION"
                        and registered[4] == "VERIFIED" and int(registered[5]) == 1
                        and registered[6] == "CAE-BRIDGE-001.verified-interview-source-registration"
                        and registered[7] == "NOT_APPLICABLE" and registered[8] == "NOT_READ"
                        and legacy_source["object_id"] in str(registered[9])
                    )
                    replay, replay_key = bridge.bridge_source_package(
                        legacy_source=legacy_source,
                        bridge_actor_id=bridge_actor,
                        idempotency_key=f"bridge:{proof_id}",
                    )
                    idempotent_bridge = replay.idempotent_replay and replay.receipt_id == receipt.receipt_id and replay_key == storage_key
                    tampered_source = {**legacy_source, "payload": {**legacy_source["payload"], "project_id": "tampered-project"}}
                    tampered_legacy_rejected = assert_raises(
                        lambda: bridge.bridge_source_package(
                            legacy_source=tampered_source, bridge_actor_id=bridge_actor,
                            idempotency_key=f"tampered:{proof_id}",
                        ),
                        InterviewSourceBridgeError,
                    )
                    local_media.write_bytes(b"tampered local bytes")
                    local_media_tamper_rejected = assert_raises(
                        lambda: bridge.bridge_source_package(
                            legacy_source=legacy_source, bridge_actor_id=bridge_actor,
                            idempotency_key=f"tampered-media:{proof_id}",
                        ),
                        InterviewSourceBridgeError,
                    )
                    local_media.write_bytes(source_bytes)
                    capture = FirstSliceSemanticOperations(connection).capture_evidence(
                        workspace_id=workspace_id,
                        evidence_id=f"proof:wp09:evidence:{proof_id}",
                        source_package_id=bridged_source_id,
                        capture_actor_id=capture_actor,
                        media_asset_id=f"cae:media:ie:{canonical_sha256({'upstream_source_ref': {'object_id': legacy_source['object_id'], 'revision': str(legacy_source['revision']), 'sha256': legacy_source['sha256']}, 'content_sha256': source_sha})[:32]}",
                        start_ms=0,
                        end_ms=len(source_bytes),
                        quoted_text="source sentence preserved through bridge",
                        idempotency_key=f"capture:{proof_id}",
                    )
                    bridged_capture_accepted = capture.outcome == "ACCEPTED"
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT count(*) FROM cae.command WHERE workspace_id = %s", (workspace_id,))
                        command_count = int(cursor.fetchone()[0])
                        cursor.execute("SELECT count(*) FROM cae.receipt receipt JOIN cae.command command ON command.command_id = receipt.command_id WHERE command.workspace_id = %s", (workspace_id,))
                        receipt_count = int(cursor.fetchone()[0])
                    bridge_receipt_cardinality = command_count == receipt_count == 2

            legacy_after = interview.repository.get_object(legacy_source["object_id"])
            legacy_unchanged = legacy_after["sha256"] == legacy_hash_before and legacy_after["revision"] == legacy_revision_before
        checks = {
            "test_governance_manifest": manifest_is_governed,
            "legacy_source_created_via_real_repository": legacy_unchanged,
            "verified_source_registered": verified_registration,
            "idempotent_bridge": idempotent_bridge,
            "tampered_legacy_payload_rejected": tampered_legacy_rejected,
            "tampered_local_media_rejected": local_media_tamper_rejected,
            "bridged_source_accepts_typed_capture": bridged_capture_accepted,
            "bridge_and_capture_receipts_atomic": bridge_receipt_cardinality,
        }
        for name, passed in checks.items():
            print(f"{name}={'PASS' if passed else 'FAIL'}")
        return 0 if all(checks.values()) else 1
    except Exception as error:
        print("wp09_proof=FAILED")
        print(f"failure_type={type(error).__name__}")
        print(f"failure_message={error}")
        return 1
    finally:
        if storage_key:
            try:
                with psycopg.connect(connection_url(), connect_timeout=10) as connection:
                    InterviewExpressionSourceBridge(
                        connection, media_root=Path.cwd(), supabase_url=PROJECT_URL,
                        secret_key=secret, bucket=BUCKET,
                    ).delete_object(storage_key)
                print("temporary_bridge_object_deleted=PASS")
            except Exception:
                print("temporary_bridge_object_deleted=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
