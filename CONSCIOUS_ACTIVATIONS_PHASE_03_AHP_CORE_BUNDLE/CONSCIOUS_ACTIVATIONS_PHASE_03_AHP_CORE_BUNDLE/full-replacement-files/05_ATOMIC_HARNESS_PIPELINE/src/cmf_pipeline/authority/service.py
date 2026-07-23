from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.enums import AdmissionDecision, SourceClass, SourceDisposition
from ..domain.errors import PipelineAuthorityError, PipelineValidationError
from ..domain.validation import (
    reject_noncanonical,
    reject_unknown,
    require_authority,
    require_int,
    require_ref,
    require_ref_list,
    require_relative_path,
    require_semver,
    require_sha,
    require_string,
    require_string_list,
    semantic_identity,
)
from ..workflow.infrastructure.repository import PipelineRepository


class ProgramAuthorityService:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def reconcile_program_state(
        self,
        authority_snapshot: Mapping[str, Any],
        status_projections: list[Mapping[str, Any]],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        normalized_authority = self._authority_snapshot(authority_snapshot)
        normalized_statuses = [self._program_status(item, index) for index, item in enumerate(status_projections)]
        if not normalized_statuses:
            raise PipelineValidationError("at least one program status projection is required")
        canonical = [item for item in normalized_statuses if item["canonical"]]
        if len(canonical) != 1:
            raise PipelineValidationError("exactly one canonical Program Control status projection is required")
        result = {
            "authority_snapshot": normalized_authority,
            "canonical_program_status": canonical[0],
            "repository_status_projections": sorted(normalized_statuses, key=lambda item: item["product_id"]),
            "conflicts": self._status_conflicts(canonical[0], normalized_statuses),
            "claim_dimensions_separate": True,
        }
        stored = self.repository.store_object(
            "program_state_reconciliation",
            result,
            idempotency_key=idempotency_key,
            object_id=semantic_identity("program-state", result),
            lifecycle_state="VERIFIED",
        )
        return stored

    def register_source(
        self,
        source: Mapping[str, Any],
        decision: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        normalized_source = self._source_record(source)
        normalized_decision = self._source_decision(decision, normalized_source)
        source_result = self.repository.store_object(
            "brownfield_source_record",
            normalized_source,
            idempotency_key=f"{idempotency_key}:source",
            object_id=normalized_source["source_record_id"],
            lifecycle_state="ADMITTED" if normalized_decision["disposition"] != "ARCHIVE" else "ARCHIVED",
        )
        decision_result = self.repository.store_object(
            "source_disposition_decision",
            normalized_decision,
            idempotency_key=f"{idempotency_key}:decision",
            object_id=normalized_decision["decision_id"],
            lifecycle_state="ACTIVE",
        )
        self.repository.add_edge(
            normalized_source["source_record_id"],
            normalized_decision["decision_id"],
            "governed_by_disposition",
            evidence={"source_sha256": normalized_source["sha256"]},
        )
        return {"source": source_result["object"], "decision": decision_result["object"]}

    def evaluate_binding_admission(
        self,
        request: Mapping[str, Any],
        *,
        authority_snapshot: Mapping[str, Any],
        canonical_program_status: Mapping[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        normalized_request = self._admission_request(request)
        normalized_authority = self._authority_snapshot(authority_snapshot)
        normalized_status = self._program_status(canonical_program_status, 0)
        blockers: list[str] = []
        if normalized_request["authority_snapshot_id"] != normalized_authority["snapshot_id"]:
            blockers.append("AUTHORITY_SNAPSHOT_MISMATCH")
        if normalized_request["program_status_id"] != normalized_status["projection_id"]:
            blockers.append("PROGRAM_STATUS_MISMATCH")
        requested_claim = normalized_request["requested_claim"]
        if normalized_authority["candidate_authorities"] and requested_claim in {
            "ACCEPTED_FOR_BUILD",
            "PRODUCTION_READY",
            "CERTIFIED",
        }:
            blockers.append("CANDIDATE_AUTHORITY_NOT_RATIFIED")
        if normalized_request["category_id"] == "format02" or "format02" in normalized_request["profile_id"].lower():
            blockers.append("FORMAT02_DEFERRED")
        decision = AdmissionDecision.ACCEPTED.value if not blockers else AdmissionDecision.DENIED.value
        receipt_core = {
            "request_id": normalized_request["request_id"],
            "decision": decision,
            "authority_snapshot_id": normalized_authority["snapshot_id"],
            "program_status_id": normalized_status["projection_id"],
            "binding_sha256": normalized_request["binding_sha256"],
            "validated_source_record_ids": normalized_request["source_record_ids"],
            "validated_contract_refs": normalized_request["contract_refs"],
            "blockers": sorted(blockers),
            "maximum_claim": "DEVELOPMENT_EXECUTION_ELIGIBLE" if not blockers else "DENIED",
            "supersedes_receipt_id": "NOT_APPLICABLE",
            "actor_id": "atomic-harness-pipeline:authority-admission",
        }
        receipt = {
            **receipt_core,
            "decision_digest": canonical_sha256(receipt_core),
            "receipt_id": semantic_identity("binding-admission", receipt_core),
        }
        stored = self.repository.store_object(
            "execution_binding_admission_receipt",
            receipt,
            idempotency_key=idempotency_key,
            object_id=receipt["receipt_id"],
            lifecycle_state="ACCEPTED" if decision == "ACCEPTED" else "DENIED",
        )
        return stored

    @staticmethod
    def _authority_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
        allowed = {
            "schema_id",
            "schema_version",
            "snapshot_id",
            "constitution_id",
            "constitution_version",
            "constitution_sha256",
            "product_authorities",
            "candidate_authorities",
            "canonical_program_status_id",
            "issued_by",
        }
        reject_unknown(payload, allowed, "AuthoritySnapshot")
        result = {
            "schema_id": require_string(payload.get("schema_id"), "schema_id"),
            "schema_version": require_string(payload.get("schema_version"), "schema_version"),
            "snapshot_id": require_string(payload.get("snapshot_id"), "snapshot_id"),
            "constitution_id": require_string(payload.get("constitution_id"), "constitution_id"),
            "constitution_version": require_string(payload.get("constitution_version"), "constitution_version"),
            "constitution_sha256": require_sha(payload.get("constitution_sha256"), "constitution_sha256"),
            "product_authorities": [require_authority(item, f"product_authorities[{i}]") for i, item in enumerate(payload.get("product_authorities", []))],
            "candidate_authorities": [require_authority(item, f"candidate_authorities[{i}]") for i, item in enumerate(payload.get("candidate_authorities", []))],
            "canonical_program_status_id": require_string(payload.get("canonical_program_status_id"), "canonical_program_status_id"),
            "issued_by": require_string(payload.get("issued_by"), "issued_by"),
        }
        if not result["product_authorities"]:
            raise PipelineValidationError("product_authorities must be non-empty")
        if result["snapshot_id"] != semantic_identity("authority-snapshot", {k: v for k, v in result.items() if k != "snapshot_id"}):
            raise PipelineValidationError("snapshot_id does not match canonical authority content")
        return result

    @staticmethod
    def _program_status(payload: Mapping[str, Any], index: int) -> dict[str, Any]:
        allowed = {
            "projection_id",
            "product_id",
            "product_version",
            "canonical",
            "implementation_coverage",
            "story_completion",
            "evidence_closure",
            "external_proof_complete",
            "production_authorized",
            "certified",
            "source_sha256",
        }
        reject_unknown(payload, allowed, f"ProgramStatusProjection[{index}]")
        return {
            "projection_id": require_string(payload.get("projection_id"), f"status[{index}].projection_id"),
            "product_id": require_string(payload.get("product_id"), f"status[{index}].product_id"),
            "product_version": require_string(payload.get("product_version"), f"status[{index}].product_version"),
            "canonical": bool(payload.get("canonical", False)),
            "implementation_coverage": require_string(payload.get("implementation_coverage"), f"status[{index}].implementation_coverage"),
            "story_completion": require_string(payload.get("story_completion"), f"status[{index}].story_completion"),
            "evidence_closure": require_string(payload.get("evidence_closure"), f"status[{index}].evidence_closure"),
            "external_proof_complete": bool(payload.get("external_proof_complete", False)),
            "production_authorized": bool(payload.get("production_authorized", False)),
            "certified": bool(payload.get("certified", False)),
            "source_sha256": require_sha(payload.get("source_sha256"), f"status[{index}].source_sha256"),
        }

    @staticmethod
    def _status_conflicts(canonical: Mapping[str, Any], projections: list[Mapping[str, Any]]) -> list[dict[str, str]]:
        conflicts: list[dict[str, str]] = []
        for projection in projections:
            if projection["canonical"]:
                continue
            for field in ("production_authorized", "certified"):
                if projection[field] and not canonical[field]:
                    conflicts.append({
                        "product_id": str(projection["product_id"]),
                        "field": field,
                        "canonical_value": str(canonical[field]).lower(),
                        "projection_value": str(projection[field]).lower(),
                        "resolution": "CANONICAL_PROGRAM_CONTROL_WINS",
                    })
        return sorted(conflicts, key=lambda item: (item["product_id"], item["field"]))

    @staticmethod
    def _source_record(payload: Mapping[str, Any]) -> dict[str, Any]:
        allowed = {
            "source_record_id",
            "archive_id",
            "relative_path",
            "byte_length",
            "sha256",
            "source_class",
            "origin_repository",
            "license_evidence_refs",
            "dependency_manifest_ref",
            "disposition_decision_id",
        }
        reject_unknown(payload, allowed, "BrownfieldSourceRecord")
        source_class = require_string(payload.get("source_class"), "source_class")
        if source_class not in {item.value for item in SourceClass}:
            raise PipelineValidationError("unsupported source_class")
        result = {
            "archive_id": require_string(payload.get("archive_id"), "archive_id"),
            "relative_path": require_relative_path(payload.get("relative_path"), "relative_path"),
            "byte_length": require_int(payload.get("byte_length"), "byte_length"),
            "sha256": require_sha(payload.get("sha256"), "sha256"),
            "source_class": source_class,
            "origin_repository": require_string(payload.get("origin_repository"), "origin_repository"),
            "license_evidence_refs": require_string_list(payload.get("license_evidence_refs", []), "license_evidence_refs"),
            "dependency_manifest_ref": payload.get("dependency_manifest_ref", "NOT_APPLICABLE"),
            "disposition_decision_id": require_string(payload.get("disposition_decision_id"), "disposition_decision_id"),
        }
        if result["dependency_manifest_ref"] != "NOT_APPLICABLE":
            result["dependency_manifest_ref"] = require_string(result["dependency_manifest_ref"], "dependency_manifest_ref")
        expected = semantic_identity("source-record", result)
        provided = require_string(payload.get("source_record_id"), "source_record_id")
        if provided != expected:
            raise PipelineValidationError("source_record_id does not match canonical source bytes")
        return {"source_record_id": provided, **result}

    @staticmethod
    def _source_decision(payload: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
        allowed = {
            "decision_id",
            "source_record_id",
            "disposition",
            "target_paths",
            "replacement_reason",
            "behavior_preservation_refs",
            "authority_exclusions",
            "decided_by",
            "evidence_refs",
        }
        reject_unknown(payload, allowed, "SourceDispositionDecision")
        disposition = require_string(payload.get("disposition"), "disposition")
        if disposition not in {item.value for item in SourceDisposition}:
            raise PipelineValidationError("unsupported source disposition")
        targets = [require_relative_path(item, f"target_paths[{index}]") for index, item in enumerate(payload.get("target_paths", []))]
        if len(targets) != len(set(targets)) or targets != sorted(targets):
            raise PipelineValidationError("target_paths must be sorted and unique")
        if disposition != "ARCHIVE" and not targets:
            raise PipelineValidationError("non-ARCHIVE disposition requires target_paths")
        if disposition == "ARCHIVE" and targets:
            raise PipelineValidationError("ARCHIVE disposition cannot have target_paths")
        result = {
            "source_record_id": require_string(payload.get("source_record_id"), "source_record_id"),
            "disposition": disposition,
            "target_paths": targets,
            "replacement_reason": require_string(payload.get("replacement_reason", "NOT_APPLICABLE"), "replacement_reason"),
            "behavior_preservation_refs": require_string_list(payload.get("behavior_preservation_refs", []), "behavior_preservation_refs"),
            "authority_exclusions": require_string_list(payload.get("authority_exclusions", []), "authority_exclusions", non_empty=True),
            "decided_by": require_string(payload.get("decided_by"), "decided_by"),
            "evidence_refs": require_string_list(payload.get("evidence_refs", []), "evidence_refs", non_empty=True),
        }
        if result["source_record_id"] != source["source_record_id"]:
            raise PipelineValidationError("source decision references a different source record")
        if disposition == "REPLACE" and result["replacement_reason"] == "NOT_APPLICABLE":
            raise PipelineValidationError("REPLACE requires a replacement_reason")
        expected = semantic_identity("source-decision", result)
        provided = require_string(payload.get("decision_id"), "decision_id")
        if provided != expected:
            raise PipelineValidationError("decision_id does not match canonical decision bytes")
        return {"decision_id": provided, **result}

    @staticmethod
    def _admission_request(payload: Mapping[str, Any]) -> dict[str, Any]:
        allowed = {
            "request_id",
            "binding_id",
            "binding_version",
            "binding_sha256",
            "atomic_harness_definition_ref",
            "authority_snapshot_id",
            "program_status_id",
            "source_record_ids",
            "contract_refs",
            "category_id",
            "profile_id",
            "requested_claim",
        }
        reject_unknown(payload, allowed, "ExecutionBindingAdmissionRequest")
        result = {
            "binding_id": require_string(payload.get("binding_id"), "binding_id"),
            "binding_version": require_semver(payload.get("binding_version"), "binding_version"),
            "binding_sha256": require_sha(payload.get("binding_sha256"), "binding_sha256"),
            "atomic_harness_definition_ref": require_ref(payload.get("atomic_harness_definition_ref"), "atomic_harness_definition_ref"),
            "authority_snapshot_id": require_string(payload.get("authority_snapshot_id"), "authority_snapshot_id"),
            "program_status_id": require_string(payload.get("program_status_id"), "program_status_id"),
            "source_record_ids": require_string_list(payload.get("source_record_ids", []), "source_record_ids"),
            "contract_refs": require_ref_list(payload.get("contract_refs", []), "contract_refs"),
            "category_id": require_string(payload.get("category_id"), "category_id"),
            "profile_id": require_string(payload.get("profile_id"), "profile_id"),
            "requested_claim": require_string(payload.get("requested_claim"), "requested_claim"),
        }
        expected = semantic_identity("binding-admission-request", result)
        provided = require_string(payload.get("request_id"), "request_id")
        if provided != expected:
            raise PipelineValidationError("request_id does not match canonical request bytes")
        return {"request_id": provided, **result}
