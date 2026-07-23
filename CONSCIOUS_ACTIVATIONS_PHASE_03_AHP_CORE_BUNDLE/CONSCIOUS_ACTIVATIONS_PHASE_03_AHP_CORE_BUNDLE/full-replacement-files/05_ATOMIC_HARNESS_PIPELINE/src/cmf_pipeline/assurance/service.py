from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256, validate_payload

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref, require_ref_list, require_string, require_string_list, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository


class AssuranceService:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def execution_fingerprint(
        self,
        *,
        contract_release_ref: Mapping[str, Any],
        implementation_ref: Mapping[str, Any],
        runtime_ref: Mapping[str, Any],
        tool_refs: list[Mapping[str, Any]],
        evaluator_ref: Mapping[str, Any] | None,
        model_ref: Mapping[str, Any] | None,
        hardware_profile: str,
        precision: str,
    ) -> dict[str, Any]:
        core = {
            "contract_release_ref": require_ref(contract_release_ref, "contract_release_ref"),
            "implementation_ref": require_ref(implementation_ref, "implementation_ref"),
            "runtime_ref": require_ref(runtime_ref, "runtime_ref"),
            "tool_refs": require_ref_list(tool_refs, "tool_refs"),
            "evaluator_ref": require_ref(evaluator_ref, "evaluator_ref") if evaluator_ref else None,
            "model_ref": require_ref(model_ref, "model_ref") if model_ref else None,
            "hardware_profile": require_string(hardware_profile, "hardware_profile"),
            "precision": require_string(precision, "precision"),
        }
        fingerprint_id = semantic_identity("execution-stack", core)
        payload = {"fingerprint_id": fingerprint_id, **core, "canonical_sha256": canonical_sha256(core)}
        validate_payload("execution-stack-fingerprint", payload)
        return payload

    def sandbox_declaration(
        self,
        *,
        implementation_ref: Mapping[str, Any],
        allowed_actions: list[str],
        forbidden_actions: list[str],
        allowed_relative_paths: list[str],
        network_policy: str,
        secret_reference_ids: list[str],
        resource_limits: Mapping[str, int],
    ) -> dict[str, Any]:
        allowed = require_string_list(sorted(allowed_actions), "allowed_actions")
        forbidden = require_string_list(sorted(forbidden_actions), "forbidden_actions")
        overlap = sorted(set(allowed) & set(forbidden))
        if overlap:
            raise PipelineValidationError(f"sandbox actions overlap: {overlap}")
        if any(value < 0 for value in resource_limits.values()) or any(isinstance(value, bool) for value in resource_limits.values()):
            raise PipelineValidationError("resource limits must be non-negative integers")
        core = {
            "implementation_ref": require_ref(implementation_ref, "implementation_ref"),
            "allowed_actions": allowed,
            "forbidden_actions": forbidden,
            "allowed_relative_paths": require_string_list(sorted(allowed_relative_paths), "allowed_relative_paths"),
            "network_policy": require_string(network_policy, "network_policy"),
            "secret_reference_ids": require_string_list(sorted(secret_reference_ids), "secret_reference_ids"),
            "resource_limits": dict(sorted(resource_limits.items())),
            "raw_secret_values_included": False,
            "production_isolation_claimed": False,
        }
        return {"sandbox_declaration_id": semantic_identity("sandbox", core), "sandbox_version": "1.0.0", **core}

    def assurance_check(
        self,
        *,
        target_ref: Mapping[str, Any],
        fingerprint: Mapping[str, Any],
        sandbox: Mapping[str, Any],
        observed_contract_release_ref: Mapping[str, Any],
    ) -> dict[str, Any]:
        target = require_ref(target_ref, "target_ref")
        observed = require_ref(observed_contract_release_ref, "observed_contract_release_ref")
        findings = []
        if fingerprint["contract_release_ref"] != observed:
            findings.append("CONTRACT_RELEASE_DRIFT")
        if sandbox["implementation_ref"] != fingerprint["implementation_ref"]:
            findings.append("SANDBOX_IMPLEMENTATION_MISMATCH")
        core = {
            "target_ref": target,
            "fingerprint_id": fingerprint["fingerprint_id"],
            "sandbox_declaration_id": sandbox["sandbox_declaration_id"],
            "findings": sorted(findings),
            "result": "PASS" if not findings else "FAIL",
            "production_assurance_claimed": False,
        }
        return {"assurance_receipt_id": semantic_identity("assurance", core), **core}

    def record_incident(
        self,
        *,
        incident_type: str,
        severity: str,
        target_ref: Mapping[str, Any],
        details: Mapping[str, Any],
        containment_state: str = "CONTAINED_DEVELOPMENT_SCOPE",
    ) -> dict[str, Any]:
        core = {
            "incident_type": require_string(incident_type, "incident_type"),
            "severity": require_string(severity, "severity"),
            "target_ref": require_ref(target_ref, "target_ref"),
            "details": dict(details),
            "containment_state": require_string(containment_state, "containment_state"),
        }
        incident = {"incident_id": semantic_identity("pipeline-incident", core), **core}
        self.repository.initialize()
        from ca_contracts import canonical_json_text, utc_now_rfc3339
        with self.repository._connect() as connection:
            connection.execute(
                """
                INSERT INTO pipeline_incidents(
                    incident_id, severity, incident_type, target_ref_json,
                    containment_state, details_json, created_at_utc
                ) VALUES(?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(incident_id) DO NOTHING
                """,
                (
                    incident["incident_id"],
                    incident["severity"],
                    incident["incident_type"],
                    canonical_json_text(incident["target_ref"]),
                    incident["containment_state"],
                    canonical_json_text(incident["details"]),
                    utc_now_rfc3339(),
                ),
            )
        return incident
