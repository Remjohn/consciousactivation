"""Typed PostgreSQL semantic operations for CAE's first evidence-to-AIR slice.

This module intentionally owns only the bounded WP-03 slice. It does not
replace existing SQLite services or perform legacy-data migration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import psycopg
from psycopg.types.json import Jsonb

from ca_contracts import canonical_json_text, canonical_sha256


class SemanticOperationError(RuntimeError):
    """A typed operation cannot satisfy its contract."""


class SemanticOperationConflict(SemanticOperationError):
    """An idempotency or optimistic-concurrency condition was violated."""


@dataclass(frozen=True, slots=True)
class OperationReceipt:
    receipt_id: str
    outcome: str
    idempotent_replay: bool
    payload: Mapping[str, Any]


def _required(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SemanticOperationError(f"{name} is required")
    return value.strip()


def _stable_id(prefix: str, payload: Mapping[str, Any]) -> str:
    return f"{prefix}:{canonical_sha256(payload)[:32]}"


def _execution_receipt_context(
    *,
    operation_id: str,
    command_payload: Mapping[str, Any],
    event_payload: Mapping[str, Any],
    receipt_id: str,
    receipt_payload: Mapping[str, Any],
) -> Mapping[str, Any]:
    """Build context for one immutable execution receipt.

    The context reports what this transition actually exercised. It does not
    convert a receipt into independent evidence or manufacture semantic/taste
    proof that this bounded transition does not evaluate.
    """
    claim_ids = {
        "cae.evidence.capture": "CAE-EVID-001.capture-traceability",
        "cae.evidence.authenticate": "CAE-EVID-001.authentication-lineage",
        "cae.air.propose-assessment": "CAE-EVID-001.assessment-evidence-linkage",
        "cae.air.validate-assessment": "CAE-EVID-001.assessment-validation-lineage",
        "cae.air.confirm-assessment": "CAE-EVID-001.operator-confirmation-lineage",
        "cae.bridge.register-interview-source": "CAE-BRIDGE-001.verified-interview-source-registration",
    }
    return {
        "receipt_type": "cae_execution_receipt",
        "receipt_id": receipt_id,
        "claim_id": claim_ids[operation_id],
        "component_id": "ca_runtime.first_slice_semantic_operations",
        "input_snapshot_sha256": canonical_sha256(dict(command_payload)),
        "output_snapshot_sha256": canonical_sha256(dict(event_payload)),
        "registry_scope": "NOT_READ",
        "registry_snapshot_sha256": None,
        "environment_fidelity": "E3_PRODUCTION_SHAPED",
        "environment_identity": {
            "state_authority": "postgresql_supabase",
            "runtime_component": "ca_runtime.FirstSliceSemanticOperations",
            "deployment_boundary": "staging_only",
        },
        "evaluator_versions": {"semantic_operation": f"{operation_id}@1.0.0"},
        "validator_results": {
            "transition_contract": "PASS",
            "independent_evidence_precondition": "PASS",
            "operator_decision_precondition": (
                "PASS" if receipt_payload.get("operator_decision") else "NOT_APPLICABLE"
            ),
        },
        "reward_hack_result": "UNVERIFIED",
        "taste_integrity_result": "NOT_APPLICABLE",
        "anti_centroid_result": "NOT_APPLICABLE",
        "evidence_status": (
            "NOT_APPLICABLE"
            if operation_id == "cae.bridge.register-interview-source"
            else "TRACEABLE"
        ),
        "receipt_payload_sha256": canonical_sha256(dict(receipt_payload)),
    }


def _receipt_lineage_role(operation_id: str) -> str:
    return {
        "cae.evidence.capture": "CREATED",
        "cae.evidence.authenticate": "AUTHENTICATES",
        "cae.air.propose-assessment": "SUPPORTS",
        "cae.air.validate-assessment": "VALIDATES",
        "cae.air.confirm-assessment": "CONFIRMS",
    }[operation_id]


class FirstSliceSemanticOperations:
    """Executes only registered first-slice CAE semantic operations.

    The caller supplies an open psycopg connection. Every public method opens
    one database transaction and creates a typed command, transition, event,
    and immutable receipt atomically.
    """

    def __init__(self, connection: psycopg.Connection[Any]):
        self.connection = connection

    def capture_evidence(
        self,
        *,
        workspace_id: str,
        evidence_id: str,
        source_package_id: str,
        capture_actor_id: str,
        media_asset_id: str,
        start_ms: int,
        end_ms: int,
        quoted_text: str,
        idempotency_key: str,
    ) -> OperationReceipt:
        operation_id = "cae.evidence.capture"
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "evidence_id": _required(evidence_id, "evidence_id"),
            "source_package_id": _required(source_package_id, "source_package_id"),
            "capture_actor_id": _required(capture_actor_id, "capture_actor_id"),
            "media_asset_id": _required(media_asset_id, "media_asset_id"),
            "start_ms": int(start_ms),
            "end_ms": int(end_ms),
            "quoted_text": _required(quoted_text, "quoted_text"),
        }
        if command_payload["start_ms"] < 0 or command_payload["end_ms"] < command_payload["start_ms"]:
            raise SemanticOperationError("evidence span timing is invalid")
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                cursor.execute(
                    """
                    SELECT package.workspace_id, asset.lifecycle_state
                    FROM cae.source_package package
                    JOIN cae.media_asset asset ON asset.asset_id = package.media_asset_id
                    WHERE package.source_package_id = %s AND package.media_asset_id = %s
                    """,
                    (source_package_id, media_asset_id),
                )
                source = cursor.fetchone()
                if source is None or source[0] != workspace_id or source[1] != "VERIFIED":
                    raise SemanticOperationError("source package does not identify a verified workspace media asset")
                self._require_actor(cursor, workspace_id, capture_actor_id)
                evidence_core = {
                    "source_package_id": source_package_id,
                    "capture_actor_id": capture_actor_id,
                    "media_asset_id": media_asset_id,
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "quoted_text": quoted_text,
                }
                cursor.execute(
                    """
                    INSERT INTO cae.evidence_item(
                      evidence_id, workspace_id, source_package_id, evidence_kind,
                      capture_actor_id, state, canonical_sha256
                    ) VALUES (%s, %s, %s, 'INTERVIEW_SOURCE_SPAN', %s, 'CAPTURED', %s)
                    """,
                    (evidence_id, workspace_id, source_package_id, capture_actor_id, canonical_sha256(evidence_core)),
                )
                cursor.execute(
                    """
                    INSERT INTO cae.evidence_span(
                      evidence_span_id, evidence_id, media_asset_id, start_ms, end_ms, quoted_text
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (_stable_id("cae:evidence-span", evidence_core), evidence_id, media_asset_id, start_ms, end_ms, quoted_text),
                )
                cursor.execute(
                    """
                    INSERT INTO cae.state_aggregate(aggregate_id, workspace_id, aggregate_type, current_state, version)
                    VALUES (%s, %s, 'evidence_item', 'CREATED', 0)
                    """,
                    (evidence_id, workspace_id),
                )
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-EVID-000",
                    workspace_id=workspace_id,
                    aggregate_id=evidence_id,
                    actor_id=capture_actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=0,
                    command_payload=command_payload,
                    event_type="EvidenceCaptured",
                    independent_evidence_refs=[{"source_package_id": source_package_id, "media_asset_id": media_asset_id}],
                )

    def authenticate_evidence(
        self,
        *,
        workspace_id: str,
        evidence_id: str,
        evaluator_actor_id: str,
        rationale: str,
        idempotency_key: str,
        expected_version: int = 1,
    ) -> OperationReceipt:
        operation_id = "cae.evidence.authenticate"
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "evidence_id": _required(evidence_id, "evidence_id"),
            "evaluator_actor_id": _required(evaluator_actor_id, "evaluator_actor_id"),
            "rationale": _required(rationale, "rationale"),
        }
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                cursor.execute(
                    """
                    SELECT capture_actor_id, source_package_id, state
                    FROM cae.evidence_item WHERE evidence_id = %s AND workspace_id = %s FOR UPDATE
                    """,
                    (evidence_id, workspace_id),
                )
                evidence = cursor.fetchone()
                if evidence is None or evidence[2] != "CAPTURED":
                    raise SemanticOperationError("evidence is not captured")
                if evidence[0] == evaluator_actor_id:
                    raise SemanticOperationError("evidence authentication requires an evaluator distinct from the capture actor")
                self._require_actor(cursor, workspace_id, evaluator_actor_id)
                cursor.execute("SELECT count(*) FROM cae.evidence_span WHERE evidence_id = %s", (evidence_id,))
                if int(cursor.fetchone()[0]) < 1:
                    raise SemanticOperationError("evidence authentication requires at least one anchored span")
                evidence_refs = [{"evidence_id": evidence_id, "source_package_id": evidence[1]}]
                authentication_core = {
                    "evidence_id": evidence_id,
                    "evaluator_actor_id": evaluator_actor_id,
                    "rationale": rationale,
                    "evidence_refs": evidence_refs,
                }
                cursor.execute(
                    """
                    INSERT INTO cae.evidence_authentication(
                      authentication_id, evidence_id, decision, evaluator_actor_id, rationale, evidence_set_sha256
                    ) VALUES (%s, %s, 'AUTHENTICATED', %s, %s, %s)
                    """,
                    (_stable_id("cae:evidence-authentication", authentication_core), evidence_id, evaluator_actor_id, rationale, canonical_sha256(evidence_refs)),
                )
                cursor.execute("UPDATE cae.evidence_item SET state = 'AUTHENTICATED' WHERE evidence_id = %s", (evidence_id,))
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-EVID-001",
                    workspace_id=workspace_id,
                    aggregate_id=evidence_id,
                    actor_id=evaluator_actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=expected_version,
                    command_payload=command_payload,
                    event_type="EvidenceAuthenticated",
                    independent_evidence_refs=evidence_refs,
                )

    def propose_assessment(
        self,
        *,
        workspace_id: str,
        assessment_id: str,
        evidence_id: str,
        actor_id: str,
        assessment_kind: str,
        validator_id: str,
        validator_version: str,
        assessment_payload: Mapping[str, Any],
        idempotency_key: str,
    ) -> OperationReceipt:
        operation_id = "cae.air.propose-assessment"
        if not assessment_payload:
            raise SemanticOperationError("assessment_payload is required")
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "assessment_id": _required(assessment_id, "assessment_id"),
            "evidence_id": _required(evidence_id, "evidence_id"),
            "assessment_kind": _required(assessment_kind, "assessment_kind"),
            "validator_id": _required(validator_id, "validator_id"),
            "validator_version": _required(validator_version, "validator_version"),
            "assessment_payload": dict(assessment_payload),
        }
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                self._require_actor(cursor, workspace_id, actor_id)
                self._require_authenticated_evidence(cursor, workspace_id, evidence_id)
                assessment_core = {**command_payload, "actor_id": actor_id, "revision": 1}
                cursor.execute(
                    """
                    INSERT INTO cae.semantic_assessment(
                      assessment_id, workspace_id, assessment_kind, revision, epistemic_state,
                      lifecycle_state, validator_id, validator_version, payload, canonical_sha256
                    ) VALUES (%s, %s, %s, 1, 'INFERRED', 'PROPOSED', %s, %s, %s, %s)
                    """,
                    (assessment_id, workspace_id, assessment_kind, validator_id, validator_version, Jsonb(dict(assessment_payload)), canonical_sha256(assessment_core)),
                )
                cursor.execute(
                    "INSERT INTO cae.assessment_evidence_link(assessment_id, assessment_revision, evidence_id, relation_type) VALUES (%s, 1, %s, 'SUPPORTS')",
                    (assessment_id, evidence_id),
                )
                cursor.execute(
                    "INSERT INTO cae.state_aggregate(aggregate_id, workspace_id, aggregate_type, current_state, version) VALUES (%s, %s, 'semantic_assessment', 'CREATED', 0)",
                    (assessment_id, workspace_id),
                )
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-AIR-000",
                    workspace_id=workspace_id,
                    aggregate_id=assessment_id,
                    actor_id=actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=0,
                    command_payload=command_payload,
                    event_type="SemanticAssessmentProposed",
                    independent_evidence_refs=[{"evidence_id": evidence_id}],
                )

    def validate_assessment(
        self,
        *,
        workspace_id: str,
        assessment_id: str,
        validator_actor_id: str,
        idempotency_key: str,
        expected_version: int = 1,
    ) -> OperationReceipt:
        operation_id = "cae.air.validate-assessment"
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "assessment_id": _required(assessment_id, "assessment_id"),
            "validator_actor_id": _required(validator_actor_id, "validator_actor_id"),
        }
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                self._require_actor(cursor, workspace_id, validator_actor_id)
                cursor.execute(
                    """
                    SELECT lifecycle_state, validator_id, validator_version
                    FROM cae.semantic_assessment
                    WHERE assessment_id = %s AND revision = 1 AND workspace_id = %s FOR UPDATE
                    """,
                    (assessment_id, workspace_id),
                )
                assessment = cursor.fetchone()
                if assessment is None or assessment[0] != "PROPOSED":
                    raise SemanticOperationError("assessment is not proposed")
                cursor.execute(
                    """
                    SELECT evidence_id FROM cae.assessment_evidence_link
                    WHERE assessment_id = %s AND assessment_revision = 1 ORDER BY evidence_id
                    """,
                    (assessment_id,),
                )
                evidence_refs = [{"evidence_id": row[0]} for row in cursor.fetchall()]
                if not evidence_refs:
                    raise SemanticOperationError("assessment validation requires evidence")
                for ref in evidence_refs:
                    self._require_authenticated_evidence(cursor, workspace_id, str(ref["evidence_id"]))
                cursor.execute("UPDATE cae.semantic_assessment SET lifecycle_state = 'VALIDATED' WHERE assessment_id = %s AND revision = 1", (assessment_id,))
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-AIR-001",
                    workspace_id=workspace_id,
                    aggregate_id=assessment_id,
                    actor_id=validator_actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=expected_version,
                    command_payload=command_payload,
                    event_type="SemanticAssessmentValidated",
                    independent_evidence_refs=evidence_refs,
                )

    def confirm_assessment(
        self,
        *,
        workspace_id: str,
        assessment_id: str,
        operator_actor_id: str,
        operator_decision: str,
        idempotency_key: str,
        expected_version: int = 2,
    ) -> OperationReceipt:
        operation_id = "cae.air.confirm-assessment"
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "assessment_id": _required(assessment_id, "assessment_id"),
            "operator_actor_id": _required(operator_actor_id, "operator_actor_id"),
            "operator_decision": _required(operator_decision, "operator_decision"),
        }
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                self._require_actor(cursor, workspace_id, operator_actor_id)
                cursor.execute(
                    "SELECT lifecycle_state FROM cae.semantic_assessment WHERE assessment_id = %s AND revision = 1 AND workspace_id = %s FOR UPDATE",
                    (assessment_id, workspace_id),
                )
                assessment = cursor.fetchone()
                if assessment is None or assessment[0] != "VALIDATED":
                    raise SemanticOperationError("assessment is not validated")
                cursor.execute(
                    "SELECT evidence_id FROM cae.assessment_evidence_link WHERE assessment_id = %s AND assessment_revision = 1 ORDER BY evidence_id",
                    (assessment_id,),
                )
                evidence_refs = [{"evidence_id": row[0]} for row in cursor.fetchall()]
                cursor.execute(
                    "UPDATE cae.semantic_assessment SET lifecycle_state = 'APPROVED', epistemic_state = 'OPERATOR_CONFIRMED' WHERE assessment_id = %s AND revision = 1",
                    (assessment_id,),
                )
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-AIR-002",
                    workspace_id=workspace_id,
                    aggregate_id=assessment_id,
                    actor_id=operator_actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=expected_version,
                    command_payload=command_payload,
                    event_type="SemanticAssessmentOperatorConfirmed",
                    independent_evidence_refs=evidence_refs,
                    operator_decision=operator_decision,
                )

    def register_verified_interview_source(
        self,
        *,
        workspace_id: str,
        project_id: str,
        bridge_actor_id: str,
        source_package_id: str,
        upstream_source_ref: Mapping[str, Any],
        media_asset_id: str,
        storage_bucket: str,
        storage_object_key: str,
        content_sha256: str,
        byte_size: int,
        media_type: str,
        idempotency_key: str,
    ) -> OperationReceipt:
        """Register bytes verified by the read-only Interview Expression bridge.

        The bridge validates the legacy package and media bytes before it calls
        this typed operation. This method persists only the CAE copy and its
        immutable upstream reference; it does not mutate the legacy service.
        """
        operation_id = "cae.bridge.register-interview-source"
        if set(upstream_source_ref) != {"object_id", "revision", "sha256"}:
            raise SemanticOperationError("upstream_source_ref has invalid shape")
        upstream_ref = {key: _required(str(upstream_source_ref[key]), f"upstream_source_ref.{key}") for key in sorted(upstream_source_ref)}
        digest = _required(content_sha256, "content_sha256")
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise SemanticOperationError("content_sha256 must be a lowercase SHA-256")
        if isinstance(byte_size, bool) or int(byte_size) < 1:
            raise SemanticOperationError("byte_size must be positive")
        command_payload = {
            "workspace_id": _required(workspace_id, "workspace_id"),
            "project_id": _required(project_id, "project_id"),
            "bridge_actor_id": _required(bridge_actor_id, "bridge_actor_id"),
            "source_package_id": _required(source_package_id, "source_package_id"),
            "upstream_source_ref": upstream_ref,
            "media_asset_id": _required(media_asset_id, "media_asset_id"),
            "storage_bucket": _required(storage_bucket, "storage_bucket"),
            "storage_object_key": _required(storage_object_key, "storage_object_key"),
            "content_sha256": digest,
            "byte_size": int(byte_size),
            "media_type": _required(media_type, "media_type"),
        }
        with self.connection.transaction():
            with self.connection.cursor() as cursor:
                replay = self._idempotent_replay(cursor, operation_id, workspace_id, idempotency_key, command_payload)
                if replay:
                    return replay
                cursor.execute(
                    "SELECT 1 FROM cae.project WHERE workspace_id = %s AND project_id = %s",
                    (workspace_id, project_id),
                )
                if cursor.fetchone() is None:
                    raise SemanticOperationError("project is not a member of the workspace")
                self._require_actor(cursor, workspace_id, bridge_actor_id)
                media_core = {
                    "storage_provider": "SUPABASE_STORAGE",
                    "storage_bucket": command_payload["storage_bucket"],
                    "storage_object_key": command_payload["storage_object_key"],
                    "content_sha256": digest,
                    "byte_size": command_payload["byte_size"],
                    "media_type": command_payload["media_type"],
                    "upstream_source_ref": upstream_ref,
                }
                cursor.execute(
                    """
                    INSERT INTO cae.media_asset(
                      asset_id, workspace_id, project_id, storage_provider, storage_bucket,
                      storage_object_key, canonical_uri, content_sha256, byte_size, media_type,
                      lifecycle_state, created_by_actor_id, verified_at
                    ) VALUES (%s, %s, %s, 'SUPABASE_STORAGE', %s, %s, %s, %s, %s, %s, 'VERIFIED', %s, now())
                    """,
                    (
                        media_asset_id, workspace_id, project_id, command_payload["storage_bucket"],
                        command_payload["storage_object_key"],
                        f"storage://SUPABASE_STORAGE/{command_payload['storage_bucket']}/{command_payload['storage_object_key']}",
                        digest, command_payload["byte_size"], command_payload["media_type"], bridge_actor_id,
                    ),
                )
                source_core = {
                    "source_kind": "INTERVIEW_EXPRESSION",
                    "media_asset_id": media_asset_id,
                    "upstream_source_ref": upstream_ref,
                    "media_verification": media_core,
                }
                cursor.execute(
                    """
                    INSERT INTO cae.source_package(
                      source_package_id, workspace_id, media_asset_id, source_kind, canonical_sha256
                    ) VALUES (%s, %s, %s, 'INTERVIEW_EXPRESSION', %s)
                    """,
                    (source_package_id, workspace_id, media_asset_id, canonical_sha256(source_core)),
                )
                cursor.execute(
                    """
                    INSERT INTO cae.state_aggregate(
                      aggregate_id, workspace_id, aggregate_type, current_state, version
                    ) VALUES (%s, %s, 'source_package', 'CREATED', 0)
                    """,
                    (source_package_id, workspace_id),
                )
                return self._transition(
                    cursor,
                    operation_id=operation_id,
                    contract_id="STC-BRIDGE-000",
                    workspace_id=workspace_id,
                    aggregate_id=source_package_id,
                    actor_id=bridge_actor_id,
                    idempotency_key=idempotency_key,
                    expected_version=0,
                    command_payload=command_payload,
                    event_type="InterviewExpressionSourceVerified",
                    independent_evidence_refs=[
                        {"upstream_source_ref": upstream_ref},
                        {"media_asset_id": media_asset_id, "content_sha256": digest},
                    ],
                )

    def _transition(
        self,
        cursor: psycopg.Cursor[Any],
        *,
        operation_id: str,
        contract_id: str,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        idempotency_key: str,
        expected_version: int,
        command_payload: Mapping[str, Any],
        event_type: str,
        independent_evidence_refs: Sequence[Mapping[str, Any]],
        operator_decision: str | None = None,
    ) -> OperationReceipt:
        cursor.execute(
            """
            SELECT contract_version, aggregate_type, from_state, to_state,
                   semantic_operation_id, semantic_operation_version,
                   requires_operator_decision, requires_independent_evidence
            FROM cae.state_transition_contract
            WHERE contract_id = %s AND active = true
            """,
            (contract_id,),
        )
        contract = cursor.fetchone()
        if contract is None:
            raise SemanticOperationError(f"active transition contract is missing: {contract_id}")
        (
            contract_version,
            aggregate_type,
            from_state,
            to_state,
            registered_operation_id,
            registered_operation_version,
            needs_operator,
            needs_evidence,
        ) = contract
        if registered_operation_id != operation_id or registered_operation_version != "1.0.0":
            raise SemanticOperationError("transition contract is not bound to the requested semantic operation")
        if bool(needs_operator) and not operator_decision:
            raise SemanticOperationError("transition requires an operator decision")
        if bool(needs_evidence) and not independent_evidence_refs:
            raise SemanticOperationError("transition requires independent evidence")
        cursor.execute(
            "SELECT current_state, version, aggregate_type FROM cae.state_aggregate WHERE aggregate_id = %s AND workspace_id = %s FOR UPDATE",
            (aggregate_id, workspace_id),
        )
        aggregate = cursor.fetchone()
        if aggregate is None or aggregate[2] != aggregate_type:
            raise SemanticOperationError("aggregate does not match transition contract")
        if aggregate[0] != from_state or int(aggregate[1]) != expected_version:
            raise SemanticOperationConflict(
                f"stale or invalid transition: expected {from_state}@{expected_version}, observed {aggregate[0]}@{aggregate[1]}"
            )
        command_sha = canonical_sha256(dict(command_payload))
        command_id = _stable_id(
            "cae:command",
            {"operation_id": operation_id, "workspace_id": workspace_id, "idempotency_key": idempotency_key},
        )
        resulting_version = expected_version + 1
        event_payload = {
            "event_type": event_type,
            "contract_id": contract_id,
            "contract_version": contract_version,
            "aggregate_id": aggregate_id,
            "from_state": from_state,
            "to_state": to_state,
            "resulting_version": resulting_version,
            "independent_evidence_refs": [dict(item) for item in independent_evidence_refs],
            "operator_decision": operator_decision,
        }
        event_sha = canonical_sha256(event_payload)
        event_id = _stable_id("cae:event", {"command_id": command_id, "event_payload": event_payload})
        receipt_payload = {
            "receipt_type": "semantic_operation_receipt",
            "operation_id": operation_id,
            "operation_version": "1.0.0",
            "command_id": command_id,
            "event_id": event_id,
            "aggregate_id": aggregate_id,
            "transition": {"from_state": from_state, "to_state": to_state, "version": resulting_version},
            "independent_evidence_refs": [dict(item) for item in independent_evidence_refs],
            "operator_decision": operator_decision,
            "outcome": "ACCEPTED",
        }
        receipt_sha = canonical_sha256(receipt_payload)
        receipt_id = _stable_id("cae:receipt", {"command_id": command_id, "receipt_sha256": receipt_sha})
        transition_id = _stable_id("cae:transition", {"command_id": command_id, "contract_id": contract_id})
        cursor.execute(
            """
            INSERT INTO cae.command(
              command_id, workspace_id, operation_id, operation_version, actor_id,
              idempotency_key, payload_sha256, payload_canonical_json, payload
            ) VALUES (%s, %s, %s, '1.0.0', %s, %s, %s, %s, %s)
            """,
            (command_id, workspace_id, operation_id, actor_id, idempotency_key, command_sha, canonical_json_text(command_payload), Jsonb(dict(command_payload))),
        )
        cursor.execute(
            "UPDATE cae.state_aggregate SET current_state = %s, version = %s, updated_at = now() WHERE aggregate_id = %s",
            (to_state, resulting_version, aggregate_id),
        )
        cursor.execute(
            """
            INSERT INTO cae.state_transition(
              transition_id, aggregate_id, contract_id, contract_version, command_id,
              actor_id, from_state, to_state, expected_version, resulting_version
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (transition_id, aggregate_id, contract_id, contract_version, command_id, actor_id, from_state, to_state, expected_version, resulting_version),
        )
        cursor.execute(
            """
            INSERT INTO cae.event(
              event_id, workspace_id, aggregate_id, aggregate_version, event_type,
              command_id, correlation_id, causation_id, payload_sha256, payload_canonical_json, payload
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (event_id, workspace_id, aggregate_id, resulting_version, event_type, command_id, command_id, command_id, event_sha, canonical_json_text(event_payload), Jsonb(event_payload)),
        )
        cursor.execute(
            """
            INSERT INTO cae.receipt(
              receipt_id, command_id, transition_id, outcome, evidence_summary_sha256,
              payload_sha256, payload_canonical_json, payload
            ) VALUES (%s, %s, %s, 'ACCEPTED', %s, %s, %s, %s)
            """,
            (receipt_id, command_id, transition_id, canonical_sha256([dict(item) for item in independent_evidence_refs]), receipt_sha, canonical_json_text(receipt_payload), Jsonb(receipt_payload)),
        )
        execution_payload = _execution_receipt_context(
            operation_id=operation_id,
            command_payload=command_payload,
            event_payload=event_payload,
            receipt_id=receipt_id,
            receipt_payload=receipt_payload,
        )
        execution_payload_sha = canonical_sha256(execution_payload)
        cursor.execute(
            """
            INSERT INTO cae.execution_receipt(
              receipt_id, claim_id, component_id, input_snapshot_sha256,
              output_snapshot_sha256, registry_scope, registry_snapshot_sha256,
              environment_fidelity, environment_identity, evaluator_versions,
              validator_results, reward_hack_result, taste_integrity_result,
              anti_centroid_result, evidence_status, payload_sha256,
              payload_canonical_json, payload
            ) VALUES (
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s
            )
            """,
            (
                receipt_id,
                execution_payload["claim_id"],
                execution_payload["component_id"],
                execution_payload["input_snapshot_sha256"],
                execution_payload["output_snapshot_sha256"],
                execution_payload["registry_scope"],
                execution_payload["registry_snapshot_sha256"],
                execution_payload["environment_fidelity"],
                Jsonb(execution_payload["environment_identity"]),
                Jsonb(execution_payload["evaluator_versions"]),
                Jsonb(execution_payload["validator_results"]),
                execution_payload["reward_hack_result"],
                execution_payload["taste_integrity_result"],
                execution_payload["anti_centroid_result"],
                execution_payload["evidence_status"],
                execution_payload_sha,
                canonical_json_text(execution_payload),
                Jsonb(execution_payload),
            ),
        )
        evidence_ids = {
            str(reference["evidence_id"])
            for reference in independent_evidence_refs
            if reference.get("evidence_id")
        }
        if operation_id == "cae.evidence.capture":
            evidence_ids.add(str(command_payload["evidence_id"]))
        for evidence_id in sorted(evidence_ids):
            cursor.execute(
                """
                INSERT INTO cae.receipt_evidence_link(receipt_id, evidence_id, lineage_role)
                VALUES (%s, %s, %s)
                """,
                (receipt_id, evidence_id, _receipt_lineage_role(operation_id)),
            )
        return OperationReceipt(receipt_id=receipt_id, outcome="ACCEPTED", idempotent_replay=False, payload=receipt_payload)

    @staticmethod
    def _require_actor(cursor: psycopg.Cursor[Any], workspace_id: str, actor_id: str) -> None:
        cursor.execute("SELECT 1 FROM cae.actor WHERE workspace_id = %s AND actor_id = %s", (workspace_id, actor_id))
        if cursor.fetchone() is None:
            raise SemanticOperationError("actor is not a member of the workspace")

    @staticmethod
    def _require_authenticated_evidence(cursor: psycopg.Cursor[Any], workspace_id: str, evidence_id: str) -> None:
        cursor.execute("SELECT state FROM cae.evidence_item WHERE workspace_id = %s AND evidence_id = %s", (workspace_id, evidence_id))
        row = cursor.fetchone()
        if row is None or row[0] != "AUTHENTICATED":
            raise SemanticOperationError("assessment requires authenticated evidence")

    @staticmethod
    def _idempotent_replay(
        cursor: psycopg.Cursor[Any], operation_id: str, workspace_id: str, idempotency_key: str, command_payload: Mapping[str, Any]
    ) -> OperationReceipt | None:
        cursor.execute(
            """
            SELECT command.command_id, command.payload_sha256, receipt.receipt_id, receipt.outcome, receipt.payload
            FROM cae.command command
            JOIN cae.receipt receipt ON receipt.command_id = command.command_id
            WHERE command.workspace_id = %s AND command.operation_id = %s AND command.idempotency_key = %s
            """,
            (workspace_id, operation_id, idempotency_key),
        )
        existing = cursor.fetchone()
        if existing is None:
            return None
        if existing[1] != canonical_sha256(dict(command_payload)):
            raise SemanticOperationConflict("idempotency key was reused with different canonical command payload")
        return OperationReceipt(receipt_id=str(existing[2]), outcome=str(existing[3]), idempotent_replay=True, payload=dict(existing[4]))
