"""E3 reality-contact and reward-hack proof for the CAE first transition slice.

This is deliberately a transition/evidence test, not a semantic-quality
evaluator. It proves only the operational claims named in the WP-08 manifest.
All database fixtures are force-rolled back and the temporary private object is
deleted after its bytes are read back and hashed.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from pathlib import Path
from urllib.request import Request, urlopen

import psycopg
import yaml

from verify_wp03_first_slice import (
    BUCKET,
    PROJECT_URL,
    connection_url,
    expect_raises_in_savepoint,
    load_local_environment,
    storage_request,
)
from ca_contracts import canonical_sha256
from ca_runtime.semantic_operations import (
    FirstSliceSemanticOperations,
    SemanticOperationConflict,
    SemanticOperationError,
)


SECRET_VARIABLE = "CAE_SUPABASE_SECRET_KEY"
ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "cae" / "evaluations" / "EVIDENCE_TO_AIR_FIRST_SLICE_WP08_EVALUATION_SUITE.yaml"


def read_private_object(url: str, headers: dict[str, str]) -> bytes:
    with urlopen(Request(url, method="GET", headers=headers), timeout=20) as response:
        return response.read()


def main() -> int:
    load_local_environment()
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    required_test_fields = {
        "test_id", "claim_id", "class", "subject", "preconditions", "fixture_source",
        "required_environment_fidelity", "actual_environment_fidelity", "execution_path",
        "assertions", "expected_failure_mode", "reward_hacking_scenario", "taste_risk",
        "anticentroid_risk", "evidence_status", "receipt_required",
    }
    expected_test_ids = {
        "WP08-ENV-001", "WP08-RH-001", "WP08-RH-002", "WP08-RH-003",
        "WP08-STATE-001", "WP08-CLAIM-001",
    }
    manifest_is_governed = (
        manifest.get("suite_id") == "cae.evidence_to_air_first_slice.wp08"
        and manifest.get("environment", {}).get("required") == "E3_PRODUCTION_SHAPED"
        and {test.get("test_id") for test in manifest.get("tests", [])} == expected_test_ids
        and all(required_test_fields <= set(test) for test in manifest.get("tests", []))
    )
    secret = os.environ.get(SECRET_VARIABLE, "")
    if not secret or secret == "***":
        print("wp08_proof=NOT_CONFIGURED")
        return 2
    proof_id = uuid.uuid4().hex
    object_key = f"proof/wp08/{proof_id}.txt"
    source_bytes = b"A specific, authenticated source span for CAE WP-08 proof.\n"
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    object_url = f"{PROJECT_URL}/storage/v1/object/{BUCKET}/{object_key}"
    headers = {
        "apikey": secret,
        "Authorization": f"Bearer {secret}",
        "Content-Type": "text/plain",
        "x-upsert": "false",
    }
    uploaded = False
    try:
        storage_request(object_url, method="POST", headers=headers, body=source_bytes)
        uploaded = True
        remote_bytes = read_private_object(object_url, headers)
        remote_hash_matches = hashlib.sha256(remote_bytes).hexdigest() == source_sha

        workspace_id = f"proof:wp08:{proof_id}"
        capture_actor = f"proof:capturer:{proof_id}"
        evaluator_actor = f"proof:evaluator:{proof_id}"
        validator_actor = f"proof:validator:{proof_id}"
        operator_actor = f"proof:operator:{proof_id}"
        asset_id = f"proof:media:{proof_id}"
        source_id = f"proof:source:{proof_id}"
        staged_asset_id = f"proof:staged-media:{proof_id}"
        staged_source_id = f"proof:staged-source:{proof_id}"
        evidence_id = f"proof:evidence:{proof_id}"
        rejected_evidence_id = f"proof:rejected-evidence:{proof_id}"
        assessment_id = f"proof:assessment:{proof_id}"
        rejected_assessment_id = f"proof:rejected-assessment:{proof_id}"

        with psycopg.connect(connection_url(), connect_timeout=10) as connection:
            with connection.transaction(force_rollback=True):
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO cae.workspace(workspace_id, display_name) VALUES (%s, 'WP-08 proof')", (workspace_id,))
                    for actor_id, subject in (
                        (capture_actor, f"wp08-capturer-{proof_id}"),
                        (evaluator_actor, f"wp08-evaluator-{proof_id}"),
                        (validator_actor, f"wp08-validator-{proof_id}"),
                        (operator_actor, f"wp08-operator-{proof_id}"),
                    ):
                        cursor.execute(
                            "INSERT INTO cae.actor(actor_id, workspace_id, actor_kind, external_subject) VALUES (%s, %s, 'HUMAN', %s)",
                            (actor_id, workspace_id, subject),
                        )
                    cursor.execute(
                        """
                        INSERT INTO cae.media_asset(
                          asset_id, workspace_id, storage_provider, storage_bucket, storage_object_key,
                          canonical_uri, content_sha256, byte_size, media_type, lifecycle_state,
                          created_by_actor_id, verified_at
                        ) VALUES (%s, %s, 'SUPABASE_STORAGE', %s, %s, %s, %s, %s, 'text/plain', 'VERIFIED', %s, now())
                        """,
                        (asset_id, workspace_id, BUCKET, object_key, f"storage://SUPABASE_STORAGE/{BUCKET}/{object_key}", source_sha, len(source_bytes), capture_actor),
                    )
                    cursor.execute(
                        "INSERT INTO cae.source_package(source_package_id, workspace_id, media_asset_id, source_kind, canonical_sha256) VALUES (%s, %s, %s, 'INTERVIEW', %s)",
                        (source_id, workspace_id, asset_id, canonical_sha256({"asset_id": asset_id, "kind": "WP08_PROOF"})),
                    )
                    staged_bytes = b"deliberately unverified WP-08 source\n"
                    cursor.execute(
                        """
                        INSERT INTO cae.media_asset(
                          asset_id, workspace_id, storage_provider, storage_bucket, storage_object_key,
                          canonical_uri, content_sha256, byte_size, media_type, lifecycle_state, created_by_actor_id
                        ) VALUES (%s, %s, 'SUPABASE_STORAGE', %s, %s, %s, %s, %s, 'text/plain', 'STAGED', %s)
                        """,
                        (staged_asset_id, workspace_id, BUCKET, f"proof/wp08/staged/{proof_id}.txt", f"storage://SUPABASE_STORAGE/{BUCKET}/proof/wp08/staged/{proof_id}.txt", hashlib.sha256(staged_bytes).hexdigest(), len(staged_bytes), capture_actor),
                    )
                    cursor.execute(
                        "INSERT INTO cae.source_package(source_package_id, workspace_id, media_asset_id, source_kind, canonical_sha256) VALUES (%s, %s, %s, 'INTERVIEW', %s)",
                        (staged_source_id, workspace_id, staged_asset_id, canonical_sha256({"asset_id": staged_asset_id, "kind": "WP08_UNVERIFIED"})),
                    )

                service = FirstSliceSemanticOperations(connection)
                unverified_asset_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.capture_evidence(
                        workspace_id=workspace_id, evidence_id=rejected_evidence_id,
                        source_package_id=staged_source_id, capture_actor_id=capture_actor,
                        media_asset_id=staged_asset_id, start_ms=0, end_ms=1,
                        quoted_text="unverified source must not capture", idempotency_key=f"unverified:{proof_id}",
                    ),
                    SemanticOperationError,
                )
                captured = service.capture_evidence(
                    workspace_id=workspace_id, evidence_id=evidence_id, source_package_id=source_id,
                    capture_actor_id=capture_actor, media_asset_id=asset_id, start_ms=0,
                    end_ms=len(source_bytes), quoted_text="specific authenticated source span",
                    idempotency_key=f"capture:{proof_id}",
                )
                changed_idempotency_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.capture_evidence(
                        workspace_id=workspace_id, evidence_id=evidence_id, source_package_id=source_id,
                        capture_actor_id=capture_actor, media_asset_id=asset_id, start_ms=0,
                        end_ms=len(source_bytes), quoted_text="changed payload must conflict",
                        idempotency_key=f"capture:{proof_id}",
                    ),
                    SemanticOperationConflict,
                )
                unauthenticated_assessment_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.propose_assessment(
                        workspace_id=workspace_id, assessment_id=rejected_assessment_id,
                        evidence_id=evidence_id, actor_id=validator_actor,
                        assessment_kind="SEMANTIC_ELIGIBILITY", validator_id="cae.air.eligibility",
                        validator_version="1.0.0", assessment_payload={"eligibility": "candidate"},
                        idempotency_key=f"unauth-propose:{proof_id}",
                    ),
                    SemanticOperationError,
                )
                self_authentication_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.authenticate_evidence(
                        workspace_id=workspace_id, evidence_id=evidence_id,
                        evaluator_actor_id=capture_actor, rationale="self-auth must fail",
                        idempotency_key=f"self-auth:{proof_id}",
                    ),
                    SemanticOperationError,
                )
                authenticated = service.authenticate_evidence(
                    workspace_id=workspace_id, evidence_id=evidence_id, evaluator_actor_id=evaluator_actor,
                    rationale="independent evaluator checked the anchored source span",
                    idempotency_key=f"authenticate:{proof_id}",
                )
                proposed = service.propose_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id, evidence_id=evidence_id,
                    actor_id=validator_actor, assessment_kind="SEMANTIC_ELIGIBILITY",
                    validator_id="cae.air.eligibility", validator_version="1.0.0",
                    assessment_payload={"eligibility": "candidate", "rationale": "bounded lifecycle proof only"},
                    idempotency_key=f"propose:{proof_id}",
                )
                stale_validation_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.validate_assessment(
                        workspace_id=workspace_id, assessment_id=assessment_id,
                        validator_actor_id=validator_actor, expected_version=99,
                        idempotency_key=f"stale:{proof_id}",
                    ),
                    SemanticOperationConflict,
                )
                validated = service.validate_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id,
                    validator_actor_id=validator_actor, idempotency_key=f"validate:{proof_id}",
                )
                empty_operator_decision_rejected = expect_raises_in_savepoint(
                    connection,
                    lambda: service.confirm_assessment(
                        workspace_id=workspace_id, assessment_id=assessment_id,
                        operator_actor_id=operator_actor, operator_decision="   ",
                        idempotency_key=f"empty-decision:{proof_id}",
                    ),
                    SemanticOperationError,
                )
                confirmed = service.confirm_assessment(
                    workspace_id=workspace_id, assessment_id=assessment_id,
                    operator_actor_id=operator_actor, operator_decision="approved after evidence review",
                    idempotency_key=f"confirm:{proof_id}",
                )
                with connection.cursor() as cursor:
                    cursor.execute("SELECT count(*) FROM cae.command WHERE workspace_id = %s", (workspace_id,))
                    command_count = int(cursor.fetchone()[0])
                    cursor.execute("SELECT count(*) FROM cae.receipt receipt JOIN cae.command command ON command.command_id = receipt.command_id WHERE command.workspace_id = %s", (workspace_id,))
                    receipt_count = int(cursor.fetchone()[0])
                    cursor.execute("SELECT count(*) FROM cae.execution_receipt execution JOIN cae.receipt receipt ON receipt.receipt_id = execution.receipt_id JOIN cae.command command ON command.command_id = receipt.command_id WHERE command.workspace_id = %s", (workspace_id,))
                    execution_receipt_count = int(cursor.fetchone()[0])
                    cursor.execute("SELECT count(*) FROM cae.receipt_evidence_link link JOIN cae.receipt receipt ON receipt.receipt_id = link.receipt_id JOIN cae.command command ON command.command_id = receipt.command_id WHERE command.workspace_id = %s", (workspace_id,))
                    evidence_link_count = int(cursor.fetchone()[0])
                    cursor.execute("SELECT count(*) FROM cae.evidence_item WHERE evidence_id = %s", (rejected_evidence_id,))
                    rejected_evidence_absent = int(cursor.fetchone()[0]) == 0
                    cursor.execute("SELECT count(*) FROM cae.semantic_assessment WHERE assessment_id = %s", (rejected_assessment_id,))
                    rejected_assessment_absent = int(cursor.fetchone()[0]) == 0
                    cursor.execute(
                        """
                        SELECT bool_and(reward_hack_result = 'UNVERIFIED'
                          AND taste_integrity_result = 'NOT_APPLICABLE'
                          AND anti_centroid_result = 'NOT_APPLICABLE')
                        FROM cae.execution_receipt execution
                        JOIN cae.receipt receipt ON receipt.receipt_id = execution.receipt_id
                        JOIN cae.command command ON command.command_id = receipt.command_id
                        WHERE command.workspace_id = %s
                        """,
                        (workspace_id,),
                    )
                    no_semantic_overclaim = bool(cursor.fetchone()[0])

        checks = {
            "test_governance_manifest": manifest_is_governed,
            "private_source_bytes_read_and_hashed": remote_hash_matches,
            "unverified_asset_rejected": unverified_asset_rejected,
            "changed_idempotency_rejected": changed_idempotency_rejected,
            "unauthenticated_assessment_rejected": unauthenticated_assessment_rejected,
            "self_authentication_rejected": self_authentication_rejected,
            "stale_transition_rejected": stale_validation_rejected,
            "empty_operator_decision_rejected": empty_operator_decision_rejected,
            "valid_five_step_transition": all(receipt.outcome == "ACCEPTED" for receipt in (captured, authenticated, proposed, validated, confirmed)),
            "negative_cases_left_no_domain_side_effect": rejected_evidence_absent and rejected_assessment_absent,
            "receipt_and_lineage_cardinality": command_count == receipt_count == execution_receipt_count == evidence_link_count == 5,
            "semantic_quality_not_overclaimed": no_semantic_overclaim,
        }
        for name, passed in checks.items():
            print(f"{name}={'PASS' if passed else 'FAIL'}")
        return 0 if all(checks.values()) else 1
    except Exception as error:
        print("wp08_proof=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1
    finally:
        if uploaded:
            try:
                storage_request(object_url, method="DELETE", headers=headers)
                print("temporary_source_object_deleted=PASS")
            except Exception:
                print("temporary_source_object_deleted=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
