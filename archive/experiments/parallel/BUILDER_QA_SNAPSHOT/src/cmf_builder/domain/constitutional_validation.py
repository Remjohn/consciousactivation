from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json


VALIDATION_SCHEMA_ID = "cmf-builder-constitutional-validation/v1"
VALIDATION_SCHEMA_VERSION = "1.0.0"
VALIDATION_RECEIPT_SCHEMA_ID = "cmf-builder-constitutional-validation-receipt/v1"
POLICY_PATH = "governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml"
POLICY_SHA256 = "328c2ec7a57de1bcc892631a2190a38d8f8e61972cbcb397c867a312f993b4ff"
CONSTITUTION_PATH = (
    "sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md"
)
CONSTITUTION_SHA256 = (
    "21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b"
)
BUILDER_PRD_AMENDMENT_PATH = (
    "docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md"
)
BUILDER_PRD_AMENDMENT_SHA256 = (
    "11445848904b61a72fbe500f6a184084e153419a2844243c0bca5f31ef87506c"
)
AUTHORITY_ORDER = (
    "explicit_current_human_direction",
    "activative_intelligence_constitution_v1_1",
    "builder_prd_v1_2_and_binding_amendment",
    "accepted_builder_decisions_with_current_effect_metadata",
    "builder_governance_registries_and_contract_schemas",
    "accepted_adrs_and_technical_specifications",
    "planning_inventory_epics_stories_and_implementation",
)
HARD_GATES = ("HG-001", "HG-004", "HG-005", "HG-015")
FORBIDDEN_BEHAVIORS = (
    "silent_lower_authority_override",
    "silent_semantic_compression",
    "downstream_semantic_invention",
)
RICH_LINEAGE_KEYS = (
    "identity_dna_ref",
    "context_premise_ref",
    "resonance_ref",
    "matrix_of_edging_ref",
    "activative_intelligence_pack_ref",
)


class ConstitutionalValidationError(Exception):
    code = "ConstitutionalValidationError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ConstitutionalPolicyInvalid(ConstitutionalValidationError):
    code = "ConstitutionalPolicyInvalid"


class ConstitutionalConflict(ConstitutionalValidationError):
    code = "ConstitutionalConflict"

    def __init__(
        self, message: str, *, findings: tuple["ArtifactConsistencyFinding", ...]
    ) -> None:
        super().__init__(
            message,
            finding_codes=tuple(item.code for item in findings),
            artifact_paths=tuple(
                sorted({item.artifact_path for item in findings if item.artifact_path})
            ),
            ir_node_paths=tuple(
                sorted({path for item in findings for path in item.ir_node_paths})
            ),
        )
        self.findings = findings


class ConstitutionalValidationInvalidatedError(ConstitutionalValidationError):
    code = "ConstitutionalValidationInvalidated"


@dataclass(frozen=True, slots=True)
class ConstitutionalPrecedencePolicy:
    source_path: str
    source_hash: str
    constitution_path: str
    constitution_version: str
    constitution_hash: str
    builder_prd_amendment_path: str
    builder_prd_version: str
    builder_prd_amendment_hash: str
    authority_order: tuple[str, ...]
    conflict_action: str
    hard_gates: tuple[str, ...]
    forbidden_behaviors: tuple[str, ...]
    harness_development_law: str
    runtime_law: str
    rich_lineage_keys: tuple[str, ...]
    builder_ownership: tuple[str, ...]
    builder_exclusions: tuple[str, ...]

    def validate(self) -> None:
        if (
            self.source_path != POLICY_PATH
            or self.source_hash != POLICY_SHA256
            or self.constitution_path != CONSTITUTION_PATH
            or self.constitution_version != "1.1.0"
            or self.constitution_hash != CONSTITUTION_SHA256
            or self.builder_prd_amendment_path != BUILDER_PRD_AMENDMENT_PATH
            or self.builder_prd_version != "1.2"
            or self.builder_prd_amendment_hash != BUILDER_PRD_AMENDMENT_SHA256
            or self.authority_order != AUTHORITY_ORDER
            or self.conflict_action != "BLOCK_AND_EMIT_DECISION_REQUEST"
            or self.hard_gates != HARD_GATES
            or self.forbidden_behaviors != FORBIDDEN_BEHAVIORS
            or self.harness_development_law != "Visual Syntax First"
            or self.runtime_law != "Activation First"
            or self.rich_lineage_keys != RICH_LINEAGE_KEYS
            or self.builder_ownership
            != ("compile", "validate", "preserve_lineage", "emit_capsule_and_handoff")
            or self.builder_exclusions
            != (
                "interview_execution",
                "visual_asset_editor_runtime",
                "delegation_protocol_runtime",
                "identity_dna_merge",
            )
        ):
            raise ConstitutionalPolicyInvalid(
                "The precedence policy does not match the accepted closed contract."
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "source_path": self.source_path,
            "source_hash": self.source_hash,
            "constitution": {
                "path": self.constitution_path,
                "version": self.constitution_version,
                "hash": self.constitution_hash,
            },
            "builder_prd": {
                "amendment_path": self.builder_prd_amendment_path,
                "version": self.builder_prd_version,
                "amendment_hash": self.builder_prd_amendment_hash,
            },
            "authority_order": list(self.authority_order),
            "conflict_action": self.conflict_action,
            "hard_gates": list(self.hard_gates),
            "forbidden_behaviors": list(self.forbidden_behaviors),
            "harness_development_law": self.harness_development_law,
            "runtime_law": self.runtime_law,
            "rich_lineage_keys": list(self.rich_lineage_keys),
            "builder_ownership": list(self.builder_ownership),
            "builder_exclusions": list(self.builder_exclusions),
        }


@dataclass(frozen=True, slots=True)
class ArtifactConsistencyFinding:
    code: str
    severity: str
    message: str
    artifact_path: str | None
    ir_node_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.code.strip()
            or self.severity not in {"ERROR", "WARNING"}
            or not self.message.strip()
            or tuple(sorted(set(self.ir_node_paths))) != self.ir_node_paths
        ):
            raise ConstitutionalValidationError("A validation finding is malformed.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "artifact_path": self.artifact_path,
            "ir_node_paths": list(self.ir_node_paths),
        }


@dataclass(frozen=True, slots=True)
class ConstitutionalValidationReport:
    report_id: str
    report_hash: str
    schema_id: str
    schema_version: str
    run_id: str
    ir_id: str
    ir_hash: str
    artifact_set_id: str
    manifest_id: str
    manifest_hash: str
    policy_path: str
    policy_hash: str
    constitution_hash: str
    builder_prd_amendment_hash: str
    authority_order: tuple[str, ...]
    coverage: tuple[str, ...]
    governed_node_count: int
    rich_lineage_paths: tuple[str, ...]
    findings: tuple[ArtifactConsistencyFinding, ...]
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        ir_id: str,
        ir_hash: str,
        artifact_set_id: str,
        manifest_id: str,
        manifest_hash: str,
        policy: ConstitutionalPrecedencePolicy,
        coverage: tuple[str, ...],
        governed_node_count: int,
        rich_lineage_paths: tuple[str, ...],
        findings: tuple[ArtifactConsistencyFinding, ...] = (),
    ) -> "ConstitutionalValidationReport":
        policy.validate()
        if findings:
            raise ConstitutionalConflict(
                "A passing validation report cannot contain findings.", findings=findings
            )
        candidate = cls(
            report_id="pending",
            report_hash="pending",
            schema_id=VALIDATION_SCHEMA_ID,
            schema_version=VALIDATION_SCHEMA_VERSION,
            run_id=run_id,
            ir_id=ir_id,
            ir_hash=ir_hash,
            artifact_set_id=artifact_set_id,
            manifest_id=manifest_id,
            manifest_hash=manifest_hash,
            policy_path=policy.source_path,
            policy_hash=policy.source_hash,
            constitution_hash=policy.constitution_hash,
            builder_prd_amendment_hash=policy.builder_prd_amendment_hash,
            authority_order=policy.authority_order,
            coverage=coverage,
            governed_node_count=governed_node_count,
            rich_lineage_paths=rich_lineage_paths,
            findings=(),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            report_id=f"constitutional-report_{digest}",
            report_hash=f"sha256:{digest}",
        )
        result.validate()
        return result

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "artifact_set_id": self.artifact_set_id,
            "manifest_id": self.manifest_id,
            "manifest_hash": self.manifest_hash,
            "policy_path": self.policy_path,
            "policy_hash": self.policy_hash,
            "constitution_hash": self.constitution_hash,
            "builder_prd_amendment_hash": self.builder_prd_amendment_hash,
            "authority_order": list(self.authority_order),
            "coverage": list(self.coverage),
            "governed_node_count": self.governed_node_count,
            "rich_lineage_paths": list(self.rich_lineage_paths),
            "findings": [item.canonical_dict() for item in self.findings],
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())

    def validate(self) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != VALIDATION_SCHEMA_ID
            or self.schema_version != VALIDATION_SCHEMA_VERSION
            or self.policy_path != POLICY_PATH
            or self.policy_hash != POLICY_SHA256
            or self.constitution_hash != CONSTITUTION_SHA256
            or self.builder_prd_amendment_hash != BUILDER_PRD_AMENDMENT_SHA256
            or self.authority_order != AUTHORITY_ORDER
            or not self.coverage
            or tuple(sorted(set(self.coverage))) != self.coverage
            or self.governed_node_count < 1
            or tuple(sorted(set(self.rich_lineage_paths))) != self.rich_lineage_paths
            or self.findings
            or self.outcome != "PASS"
            or self.report_id != f"constitutional-report_{digest}"
            or self.report_hash != f"sha256:{digest}"
        ):
            raise ConstitutionalValidationError(
                "Constitutional validation report identity or outcome is invalid."
            )


@dataclass(frozen=True, slots=True)
class ConstitutionalValidationReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    report_id: str
    report_hash: str
    artifact_set_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        run_id: str,
        report: ConstitutionalValidationReport,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "ConstitutionalValidationReceipt":
        report.validate()
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=VALIDATION_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=run_id,
            report_id=report.report_id,
            report_hash=report.report_hash,
            artifact_set_id=report.artifact_set_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            receipt_id=f"constitutional-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "report_id": self.report_id,
                "report_hash": self.report_hash,
                "artifact_set_id": self.artifact_set_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "outcome": self.outcome,
            }
        )

    def validate(self, report: ConstitutionalValidationReport) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != VALIDATION_RECEIPT_SCHEMA_ID
            or self.run_id != report.run_id
            or self.report_id != report.report_id
            or self.report_hash != report.report_hash
            or self.artifact_set_id != report.artifact_set_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.outcome != "PASS"
            or self.receipt_id != f"constitutional-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise ConstitutionalValidationError(
                "Constitutional validation receipt does not match its report."
            )


@dataclass(frozen=True, slots=True)
class ConstitutionalValidationInvalidation:
    invalidation_id: str
    invalidation_hash: str
    report_ref: str
    artifact_set_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        report_ref: str,
        artifact_set_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "ConstitutionalValidationInvalidation":
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            report_ref=report_ref,
            artifact_set_ref=artifact_set_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                report_ref,
                artifact_set_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise ConstitutionalValidationError(
                "Constitutional invalidation identity is incomplete."
            )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "report_ref": self.report_ref,
                "artifact_set_ref": self.artifact_set_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
