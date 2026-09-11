"""Real staging proof of the bounded CAE evidence-to-AIR semantic-operation slice.

The script temporarily uploads a private source object, creates all relational
fixtures and executes the five typed operations in a force-rolled-back database
transaction, then deletes the temporary storage object. It persists no proof
fixture or legacy data.
"""

from __future__ import annotations

import hashlib
import os
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

import psycopg
from psycopg.errors import ForeignKeyViolation, RaiseException
from psycopg.types.json import Jsonb


ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "packages" / "ca_contracts" / "src"), str(ROOT / "packages" / "ca_runtime" / "src")]

from ca_contracts import canonical_json_text, canonical_sha256  # noqa: E402
from ca_runtime.semantic_operations import (  # noqa: E402
    FirstSliceSemanticOperations,
    SemanticOperationConflict,
    SemanticOperationError,
)


ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
SECRET_VARIABLE = "CAE_SUPABASE_SECRET_KEY"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
PROJECT_URL = f"https://{PROJECT_REF}.supabase.co"
BUCKET = "cae-media"


def load_local_environment() -> None:
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    parsed = urlsplit(url)
    if not (
        parsed.hostname
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    ):
        raise RuntimeError("connection is not the approved CAE staging session pooler")
    return url


def storage_request(url: str, *, method: str, headers: dict[str, str], body: bytes | None = None) -> None:
    with urlopen(Request(url, method=method, headers=headers, data=body), timeout=20):
        return None


def expect_raises_in_savepoint(
    connection: psycopg.Connection[object], callback: object, error_type: type[Exception]
) -> bool:
    try:
        with connection.transaction():
            callback()  # type: ignore[operator]
    except error_type:
        return True
    return False


def main() -> int:
    load_local_environment()
    secret = os.environ.get(SECRET_VARIABLE, "")
    if not secret or secret == "***":
        print("wp03_proof=NOT_CONFIGURED")
        return 2
    object_key = f"proof/wp03/{uuid.uuid4()}.txt"
    payload = b"CAE WP-03 first-slice source proof\n"
    object_url = f"{PROJECT_URL}/storage/v1/object/{BUCKET}/{object_key}"
    headers = {
        "apikey": secret,
        "Authorization": f"Bearer {secret}",
        "Content-Type": "text/plain",
        "x-upsert": "false",
    }
    uploaded = False
    try:
        storage_request(object_url, method="POST", headers=headers, body=payload)
        uploaded = True
        proof_id = uuid.uuid4().hex
        workspace_id = f"proof:wp03:{proof_id}"
        capture_actor = f"proof:capturer:{proof_id}"
        evaluator_actor = f"proof:evaluator:{proof_id}"
        validator_actor = f"proof:validator:{proof_id}"
        operator_actor = f"proof:operator:{proof_id}"
        asset_id = f"proof:media:{proof_id}"
        source_id = f"proof:source:{proof_id}"
        evidence_id = f"proof:evidence:{proof_id}"
        assessment_id = f"proof:assessment:{proof_id}"
        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            with connection.transaction(force_rollback=True):
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO cae.workspace(workspace_id, display_name) VALUES (%s, 'WP-03 proof')", (workspace_id,))
                    for actor_id, subject in (
                        (capture_actor, f"proof-capturer-{proof_id}"),
                        (evaluator_actor, f"proof-evaluator-{proof_id}"),
                        (validator_actor, f"proof-validator-{proof_id}"),
                        (operator_actor, f"proof-operator-{proof_id}"),
                    ):
                        cursor.execute(
                            "INSERT INTO cae.actor(actor_id, workspace_id, actor_kind, external_subject) VALUES (%s, %s, 'HUMAN', %s)",
                            (actor_id, workspace_id, subject),
                        )
                    asset_sha = hashlib.sha256(payload).hexdigest()
                    cursor.execute(
                        """
                        INSERT INTO cae.media_asset(
                          asset_id, workspace_id, storage_provider, storage_bucket, storage_object_key,
                          canonical_uri, content_sha256, byte_size, media_type, lifecycle_state, created_by_actor_id,
                          verified_at
                        ) VALUES (%s, %s, 'SUPABASE_STORAGE', %s, %s, %s, %s, %s, 'text/plain', 'VERIFIED', %s, now())
                        """,
                        (asset_id, workspace_id, BUCKET, object_key, f"storage://SUPABASE_STORAGE/{BUCKET}/{object_key}", asset_sha, len(payload), capture_actor),
                    )
                    source_core = {"asset_id": asset_id, "kind": "WP03_PROOF"}
                    cursor.execute(
                        "INSERT INTO cae.source_package(source_package_id, workspace_id, media_asset_id, source_kind, canonical_sha256) VALUES (%s, %s, %s, 'INTERVIEW', %s)",
                        (source_id, workspace_id, asset_id, canonical_sha256(source_core)),
                    )
                service = FirstSliceSemanticOperations(connection)
                captured = service.capture_evidence(
                    workspace_id=workspace_id, evidence_id=evidence_id, source_package_id=source_id,
                    capture_actor_id=capture_actor, media_asset_id=asset_id, start_ms=0, end_ms=31,
                    quoted_text="CAE proof source", idempotency_key=f"capture:{proof_id}",
                )
                replay = service.capture_evidence(
                    workspace_id=workspace_id, evidence_id=evidence_id, source_package_id=source_id,
                    capture_actor_id=capture_actor, media_asset_id=asset_id, start_ms=0, end_ms=31,
                    quoted_text="CAE proof source", idempotency_key=f"capture:{proof_id}",
                )
                self_auth_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.authenticate_evidence(
                        workspace_id=workspace_id, evidence_id=evidence_id, evaluator_actor_id=capture_actor,
                        rationale="self authentication must fail", idempotency_key=f"self-auth:{proof_id}",
                    ),
                    SemanticOperationError,
                )
                authenticated = service.authenticate_evidence(
                    workspace_id=workspace_id, evidence_id=evidence_id, evaluator_actor_id=evaluator_actor,
                    rationale="independent evaluator checked source span", idempotency_key=f"auth:{proof_id}",
                )
                proposed = service.propose_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id, evidence_id=evidence_id,
                    actor_id=validator_actor, assessment_kind="SEMANTIC_ELIGIBILITY",
                    validator_id="cae.air.eligibility", validator_version="1.0.0",
                    assessment_payload={"eligibility": "candidate", "rationale": "specific evidenced semantic direction"},
                    idempotency_key=f"propose:{proof_id}",
                )
                stale_validation_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.validate_assessment(
                        workspace_id=workspace_id, assessment_id=assessment_id, validator_actor_id=validator_actor,
                        idempotency_key=f"stale:{proof_id}", expected_version=99,
                    ),
                    SemanticOperationConflict,
                )
                validated = service.validate_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id, validator_actor_id=validator_actor,
                    idempotency_key=f"validate:{proof_id}",
                )
                confirmed = service.confirm_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id, operator_actor_id=operator_actor,
                    operator_decision="approved after evidence review", idempotency_key=f"confirm:{proof_id}",
                )
                with connection.cursor() as cursor:
                    cursor.execute("SELECT count(*) FROM cae.event WHERE aggregate_id IN (%s, %s)", (evidence_id, assessment_id))
                    event_count = int(cursor.fetchone()[0])
                    cursor.execute("SELECT count(*) FROM cae.receipt WHERE payload ->> 'outcome' = 'ACCEPTED'")
                    receipt_count = int(cursor.fetchone()[0])
                    cursor.execute(
                        """
                        SELECT
                          count(*),
                          count(DISTINCT execution.receipt_id),
                          count(DISTINCT lineage.receipt_id),
                          bool_and(execution.registry_scope = 'NOT_READ'
                            AND execution.registry_snapshot_sha256 IS NULL),
                          bool_and(execution.environment_fidelity = 'E3_PRODUCTION_SHAPED'
                            AND execution.environment_identity ->> 'deployment_boundary' = 'staging_only'),
                          bool_and(execution.reward_hack_result = 'UNVERIFIED'
                            AND execution.taste_integrity_result = 'NOT_APPLICABLE'
                            AND execution.anti_centroid_result = 'NOT_APPLICABLE')
                        FROM cae.execution_receipt execution
                        LEFT JOIN cae.receipt_evidence_link lineage ON lineage.receipt_id = execution.receipt_id
                        WHERE execution.receipt_id IN (
                          SELECT receipt_id FROM cae.receipt
                          WHERE payload ->> 'command_id' IN (%s, %s, %s, %s, %s)
                        )
                        """,
                        (
                            captured.payload["command_id"], authenticated.payload["command_id"],
                            proposed.payload["command_id"], validated.payload["command_id"],
                            confirmed.payload["command_id"],
                        ),
                    )
                    (
                        execution_receipt_count,
                        lineage_receipt_count,
                        lineage_link_receipt_count,
                        registry_not_read,
                        staging_identity_present,
                        no_semantic_overclaim,
                    ) = cursor.fetchone()
                    cursor.execute(
                        "SELECT count(*) FROM cae.v_receipt_evidence_lineage WHERE receipt_id = %s",
                        (confirmed.receipt_id,),
                    )
                    confirmation_lineage_visible = int(cursor.fetchone()[0]) == 1
                    immutable_update_rejected = expect_raises_in_savepoint(
                        connection,
                        lambda: cursor.execute("UPDATE cae.command SET payload = %s WHERE command_id = %s", (Jsonb({"tampered": True}), captured.payload["command_id"])),
                        RaiseException,
                    )
                    hash_mismatch_rejected = expect_raises_in_savepoint(
                        connection,
                        lambda: cursor.execute(
                            """
                            INSERT INTO cae.command(
                              command_id, workspace_id, operation_id, operation_version, actor_id, idempotency_key,
                              payload_sha256, payload_canonical_json, payload
                            ) VALUES (%s, %s, 'cae.evidence.capture', '1.0.0', %s, %s, %s, %s, %s)
                            """,
                            (
                                f"proof:bad-hash:{proof_id}", workspace_id, capture_actor, f"bad-hash:{proof_id}",
                                "0" * 64, canonical_json_text({"valid": "bytes"}), Jsonb({"valid": "bytes"}),
                            ),
                        ),
                        RaiseException,
                    )
                    execution_receipt_update_rejected = expect_raises_in_savepoint(
                        connection,
                        lambda: cursor.execute(
                            "UPDATE cae.execution_receipt SET payload = %s WHERE receipt_id = %s",
                            (Jsonb({"tampered": True}), captured.receipt_id),
                        ),
                        RaiseException,
                    )
                    false_evidence_reference_rejected = expect_raises_in_savepoint(
                        connection,
                        lambda: cursor.execute(
                            "INSERT INTO cae.receipt_evidence_link(receipt_id, evidence_id, lineage_role) VALUES (%s, %s, 'SUPPORTS')",
                            (captured.receipt_id, f"proof:nonexistent-evidence:{proof_id}"),
                        ),
                        ForeignKeyViolation,
                    )
        print(f"capture_transition={'PASS' if captured.outcome == 'ACCEPTED' else 'FAIL'}")
        print(f"idempotent_replay={'PASS' if replay.idempotent_replay else 'FAIL'}")
        print(f"self_authentication_rejected={'PASS' if self_auth_rejected else 'FAIL'}")
        print(f"authentication_transition={'PASS' if authenticated.outcome == 'ACCEPTED' else 'FAIL'}")
        print(f"assessment_proposal_transition={'PASS' if proposed.outcome == 'ACCEPTED' else 'FAIL'}")
        print(f"stale_transition_rejected={'PASS' if stale_validation_rejected else 'FAIL'}")
        print(f"assessment_validation_transition={'PASS' if validated.outcome == 'ACCEPTED' else 'FAIL'}")
        print(f"operator_confirmation_transition={'PASS' if confirmed.outcome == 'ACCEPTED' else 'FAIL'}")
        print(f"event_count={'PASS' if event_count == 5 else 'FAIL'}")
        print(f"receipt_count={'PASS' if receipt_count == 5 else 'FAIL'}")
        print(f"immutable_command_update_rejected={'PASS' if immutable_update_rejected else 'FAIL'}")
        print(f"hash_payload_mismatch_rejected={'PASS' if hash_mismatch_rejected else 'FAIL'}")
        print(f"execution_receipt_count={'PASS' if execution_receipt_count == 5 else 'FAIL'}")
        print(f"receipt_evidence_lineage_count={'PASS' if lineage_receipt_count == 5 and lineage_link_receipt_count == 5 else 'FAIL'}")
        print(f"receipt_lineage_view={'PASS' if confirmation_lineage_visible else 'FAIL'}")
        print(f"registry_scope_not_read={'PASS' if registry_not_read else 'FAIL'}")
        print(f"staging_environment_identity={'PASS' if staging_identity_present else 'FAIL'}")
        print(f"semantic_outcome_not_overclaimed={'PASS' if no_semantic_overclaim else 'FAIL'}")
        print(f"immutable_execution_receipt_rejected={'PASS' if execution_receipt_update_rejected else 'FAIL'}")
        print(f"false_evidence_reference_rejected={'PASS' if false_evidence_reference_rejected else 'FAIL'}")
        return 0 if all((
            captured.outcome == 'ACCEPTED', replay.idempotent_replay, self_auth_rejected,
            authenticated.outcome == 'ACCEPTED', proposed.outcome == 'ACCEPTED', stale_validation_rejected,
            validated.outcome == 'ACCEPTED', confirmed.outcome == 'ACCEPTED', event_count == 5,
            receipt_count == 5, immutable_update_rejected, hash_mismatch_rejected,
            execution_receipt_count == 5, lineage_receipt_count == 5, lineage_link_receipt_count == 5,
            confirmation_lineage_visible, registry_not_read, staging_identity_present,
            no_semantic_overclaim, execution_receipt_update_rejected, false_evidence_reference_rejected,
        )) else 1
    except (HTTPError, OSError, psycopg.Error, SemanticOperationError) as error:
        print("wp03_proof=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1
    finally:
        if uploaded:
            try:
                storage_request(object_url, method="DELETE", headers=headers)
                print("temporary_source_object_deleted=PASS")
            except (HTTPError, OSError):
                print("temporary_source_object_deleted=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
