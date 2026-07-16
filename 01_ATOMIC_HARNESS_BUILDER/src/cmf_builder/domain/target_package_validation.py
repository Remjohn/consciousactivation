from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.atomic_harness_definition import (
    CATEGORY_ADAPTER_REF,
    CLASSIFICATION,
    PROFILE_ID,
    REQUIRED_SECTIONS,
    TARGET_KIND,
    AtomicHarnessDefinition,
)


VALIDATION_REPORT_SCHEMA_ID = "cmf-builder-atomic-content-harness-validation/v1"
VALIDATION_RECEIPT_SCHEMA_ID = (
    "cmf-builder-atomic-content-harness-validation-receipt/v1"
)
VALIDATION_INVALIDATION_SCHEMA_ID = (
    "cmf-builder-atomic-content-harness-validation-invalidation/v1"
)
VALIDATOR_ID = "cmf-builder/atomic-content-harness-validator"
VALIDATOR_VERSION = "1.0.0"
VALIDATION_SCOPE = "ST-07.04_ATOMIC_CONTENT_HARNESS_ONLY"
VALIDATION_POLICY_PATH = (
    "development-capsules/ST-07.04/SYNTHETIC_TARGET_VALIDATION_POLICY.json"
)
VALIDATION_POLICY_SHA256 = (
    "c78e8c2cf384ea2c5fe88c05ebc2e88b88e7e9d650cec9c6cbc11017fa8b6481"
)
INTERNAL_COMPATIBILITY = "PASS"
EXTERNAL_TARGET_COMPATIBILITY = "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH"
VALIDATION_OUTCOME = "SYNTHETIC_ATOMIC_CONTENT_HARNESS_VALIDATED"
REQUIRED_VALIDATION_DIMENSIONS = (
    "artifact_set_completeness",
    "authority_and_lineage",
    "certification_scope",
    "determinism_and_portability",
    "evaluation_and_authorization_gates",
    "internal_compatibility",
    "target_profile_separation",
    "universal_profile_non_flattening",
)
FORBIDDEN_EXTERNAL_FIELD_TOKENS = (
    "delegation",
    "generic_notes",
    "visual_asset",
    "visual_semantic",
)


class TargetValidationError(Exception):
    code = "TargetValidationError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class TargetValidationInputInvalid(TargetValidationError):
    code = "TargetValidationInputInvalid"


class TargetValidationLineageInvalid(TargetValidationError):
    code = "TargetValidationLineageInvalid"


class TargetValidationAuthorityInvalid(TargetValidationError):
    code = "TargetValidationAuthorityInvalid"


class TargetValidationScopeInvalid(TargetValidationError):
    code = "TargetValidationScopeInvalid"


class TargetValidationInvalidatedError(TargetValidationError):
    code = "TargetValidationInvalidated"


@dataclass(frozen=True, slots=True)
class TargetArtifactValidationDimension:
    dimension_id: str
    verdict: str
    evidence_refs: tuple[str, ...]
    detail: str

    def validate(self) -> None:
        if (
            self.dimension_id not in REQUIRED_VALIDATION_DIMENSIONS
            or self.verdict != "PASS"
            or not self.evidence_refs
            or tuple(sorted(set(self.evidence_refs))) != self.evidence_refs
            or not self.detail.strip()
        ):
            raise TargetValidationInputInvalid(
                "Every target-validation dimension needs canonical PASS evidence.",
                dimension_id=self.dimension_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "dimension_id": self.dimension_id,
            "verdict": self.verdict,
            "evidence_refs": list(self.evidence_refs),
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class AtomicContentHarnessValidationReport:
    report_id: str
    report_hash: str
    schema_id: str
    schema_version: str
    validator_id: str
    validator_version: str
    scope: str
    run_id: str
    definition_id: str
    definition_hash: str
    policy_path: str
    policy_hash: str
    target_kind: str
    profile_id: str
    category_binding: str
    category_adapter_ref: str
    classification: tuple[str, ...]
    section_ids: tuple[str, ...]
    artifact_refs: tuple[str, ...]
    capability_ids: tuple[str, ...]
    module_ids: tuple[str, ...]
    phase_ids: tuple[str, ...]
    context_manifest_ids: tuple[str, ...]
    acceptance_test_declarations: tuple[str, ...]
    lineage: tuple[str, ...]
    dimensions: tuple[TargetArtifactValidationDimension, ...]
    internal_compatibility: str
    external_target_compatibility: str
    production_eligible: bool
    certified: bool
    synthetic_not_certifiable: bool
    authority_identity: str
    portability_status: str
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        definition: AtomicHarnessDefinition,
        authority_identity: str,
        definition_authority_identity: str | None = None,
    ) -> "AtomicContentHarnessValidationReport":
        try:
            definition.validate_compiler_contract()
        except Exception as error:
            raise TargetValidationLineageInvalid(
                "Target validation requires the governed definition compiler contract."
            ) from error
        if (
            definition_authority_identity is not None
            and definition.authority_identity != definition_authority_identity
        ):
            raise TargetValidationAuthorityInvalid(
                "Definition compiler authority differs from immutable run evidence."
            )
        evidence: Mapping[str, tuple[str, ...]] = {
            "artifact_set_completeness": (
                definition.artifact_manifest_hash,
                definition.definition_hash,
            ),
            "authority_and_lineage": (
                definition.constitutional_report_hash,
                definition.ratification_hash,
            ),
            "certification_scope": (
                definition.definition_hash,
                "synthetic_not_certifiable",
            ),
            "determinism_and_portability": (
                definition.definition_hash,
                definition.ir_hash,
            ),
            "evaluation_and_authorization_gates": (
                definition.constitutional_report_hash,
                definition.phase_graph_hash,
            ),
            "internal_compatibility": (
                definition.capability_graph_hash,
                definition.minimum_context_graph_hash,
                definition.module_graph_hash,
                definition.phase_graph_hash,
                definition.skill_necessity_decision_hash,
            ),
            "target_profile_separation": (
                CATEGORY_ADAPTER_REF,
                TARGET_KIND,
                definition.profile_source_hash,
            ),
            "universal_profile_non_flattening": (
                definition.definition_hash,
                definition.target_profile_ref,
            ),
        }
        details = {
            "artifact_set_completeness": "all_required_sections_and_artifacts_present",
            "authority_and_lineage": "complete_authoritative_lineage_reproduced",
            "certification_scope": "synthetic_nonproduction_noncertification_enforced",
            "determinism_and_portability": "canonical_path_free_bytes_reproduced",
            "evaluation_and_authorization_gates": "all_target_specific_gates_passed",
            "internal_compatibility": "capability_module_phase_context_skill_contracts_agree",
            "target_profile_separation": "atomic_content_harness_semantics_remain_explicit",
            "universal_profile_non_flattening": "external_target_fields_are_not_absorbed",
        }
        dimensions = tuple(
            TargetArtifactValidationDimension(
                dimension_id=name,
                verdict="PASS",
                evidence_refs=tuple(sorted(set(evidence[name]))),
                detail=details[name],
            )
            for name in REQUIRED_VALIDATION_DIMENSIONS
        )
        candidate = cls(
            report_id="pending",
            report_hash="pending",
            schema_id=VALIDATION_REPORT_SCHEMA_ID,
            schema_version="1.0.0",
            validator_id=VALIDATOR_ID,
            validator_version=VALIDATOR_VERSION,
            scope=VALIDATION_SCOPE,
            run_id=definition.run_id,
            definition_id=definition.definition_id,
            definition_hash=definition.definition_hash,
            policy_path=VALIDATION_POLICY_PATH,
            policy_hash=f"sha256:{VALIDATION_POLICY_SHA256}",
            target_kind=definition.target_kind,
            profile_id=definition.harness_id,
            category_binding=definition.category_binding,
            category_adapter_ref=definition.category_adapter_ref,
            classification=definition.classification,
            section_ids=tuple(item.section_id for item in definition.sections),
            artifact_refs=tuple(sorted({
                definition.artifact_manifest_id,
                definition.artifact_set_id,
                definition.definition_id,
                definition.ir_id,
            })),
            capability_ids=definition.capability_ids,
            module_ids=definition.module_ids,
            phase_ids=definition.phase_ids,
            context_manifest_ids=definition.context_manifest_ids,
            acceptance_test_declarations=definition.acceptance_test_declarations,
            lineage=tuple(sorted({*definition.lineage, definition.definition_id, definition.definition_hash})),
            dimensions=dimensions,
            internal_compatibility=INTERNAL_COMPATIBILITY,
            external_target_compatibility=EXTERNAL_TARGET_COMPATIBILITY,
            production_eligible=False,
            certified=False,
            synthetic_not_certifiable=True,
            authority_identity=authority_identity,
            portability_status="PASS_CANONICAL_MACHINE_PATH_FREE",
            outcome=VALIDATION_OUTCOME,
        )
        candidate.validate(definition, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            report_id=f"atomic-content-harness-validation_{digest}",
            report_hash=f"sha256:{digest}",
        )
        result.validate(definition)
        return result

    def validate(
        self,
        definition: AtomicHarnessDefinition,
        *,
        verify_identity: bool = True,
    ) -> None:
        try:
            definition.validate_compiler_contract()
        except Exception as error:
            raise TargetValidationLineageInvalid(
                "Target validation requires the governed definition compiler contract."
            ) from error
        for dimension in self.dimensions:
            dimension.validate()
        definition_digest = sha256(definition.canonical_bytes()).hexdigest()
        expected_lineage = tuple(
            sorted({*definition.lineage, definition.definition_id, definition.definition_hash})
        )
        expected_artifacts = tuple(sorted({
            definition.artifact_manifest_id,
            definition.artifact_set_id,
            definition.definition_id,
            definition.ir_id,
        }))
        field_names = _all_mapping_keys(definition.canonical_dict())
        if (
            definition.definition_id != f"atomic-harness-definition_{definition_digest}"
            or definition.definition_hash != f"sha256:{definition_digest}"
            or self.schema_id != VALIDATION_REPORT_SCHEMA_ID
            or self.schema_version != "1.0.0"
            or self.validator_id != VALIDATOR_ID
            or self.validator_version != VALIDATOR_VERSION
            or self.scope != VALIDATION_SCOPE
            or self.run_id != definition.run_id
            or self.definition_id != definition.definition_id
            or self.definition_hash != definition.definition_hash
            or self.policy_path != VALIDATION_POLICY_PATH
            or self.policy_hash != f"sha256:{VALIDATION_POLICY_SHA256}"
            or self.target_kind != TARGET_KIND
            or self.profile_id != PROFILE_ID
            or self.category_binding != "none"
            or self.category_adapter_ref != CATEGORY_ADAPTER_REF
            or self.classification != CLASSIFICATION
            or self.section_ids != REQUIRED_SECTIONS
            or tuple(item.dimension_id for item in self.dimensions)
            != REQUIRED_VALIDATION_DIMENSIONS
            or expected_artifacts != self.artifact_refs
            or self.capability_ids != definition.capability_ids
            or self.module_ids != definition.module_ids
            or self.phase_ids != definition.phase_ids
            or self.context_manifest_ids != definition.context_manifest_ids
            or self.acceptance_test_declarations
            != definition.acceptance_test_declarations
            or self.lineage != expected_lineage
            or self.internal_compatibility != INTERNAL_COMPATIBILITY
            or self.external_target_compatibility
            != EXTERNAL_TARGET_COMPATIBILITY
            or self.production_eligible
            or self.certified
            or not self.synthetic_not_certifiable
            or not self.authority_identity.strip()
            or self.portability_status != "PASS_CANONICAL_MACHINE_PATH_FREE"
            or self.outcome != VALIDATION_OUTCOME
            or definition.external_skill_count
            or definition.external_runtime_count
            or definition.execution_performed
            or definition.development_capsule_generated
            or definition.production_eligible
            or definition.certified
            or not definition.synthetic_not_certifiable
            or any(
                token in key.lower()
                for key in field_names
                for token in FORBIDDEN_EXTERNAL_FIELD_TOKENS
            )
        ):
            raise TargetValidationLineageInvalid(
                "The Atomic Content Harness validation report is incomplete or broadened."
            )
        portable_values = (*self.lineage, *self.artifact_refs)
        if any("\\" in value or ":/" in value.lower() for value in portable_values):
            raise TargetValidationScopeInvalid(
                "Portable validation evidence contains a machine-local path."
            )
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.report_id != f"atomic-content-harness-validation_{digest}"
                or self.report_hash != f"sha256:{digest}"
            ):
                raise TargetValidationLineageInvalid(
                    "Validation report identity is not reproducible."
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "validator_id": self.validator_id,
            "validator_version": self.validator_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "definition_id": self.definition_id,
            "definition_hash": self.definition_hash,
            "policy_path": self.policy_path,
            "policy_hash": self.policy_hash,
            "target_kind": self.target_kind,
            "profile_id": self.profile_id,
            "category_binding": self.category_binding,
            "category_adapter_ref": self.category_adapter_ref,
            "classification": list(self.classification),
            "section_ids": list(self.section_ids),
            "artifact_refs": list(self.artifact_refs),
            "capability_ids": list(self.capability_ids),
            "module_ids": list(self.module_ids),
            "phase_ids": list(self.phase_ids),
            "context_manifest_ids": list(self.context_manifest_ids),
            "acceptance_test_declarations": list(self.acceptance_test_declarations),
            "lineage": list(self.lineage),
            "dimensions": [item.canonical_dict() for item in self.dimensions],
            "internal_compatibility": self.internal_compatibility,
            "external_target_compatibility": self.external_target_compatibility,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "synthetic_not_certifiable": self.synthetic_not_certifiable,
            "authority_identity": self.authority_identity,
            "portability_status": self.portability_status,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class AtomicContentHarnessValidationReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    definition_id: str
    definition_hash: str
    report_id: str
    report_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    dimension_count: int
    section_count: int
    internal_compatibility: str
    external_target_compatibility: str
    synthetic_not_certifiable: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        report: AtomicContentHarnessValidationReport,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "AtomicContentHarnessValidationReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=VALIDATION_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=report.run_id,
            definition_id=report.definition_id,
            definition_hash=report.definition_hash,
            report_id=report.report_id,
            report_hash=report.report_hash,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            dimension_count=len(report.dimensions),
            section_count=len(report.section_ids),
            internal_compatibility=report.internal_compatibility,
            external_target_compatibility=report.external_target_compatibility,
            synthetic_not_certifiable=report.synthetic_not_certifiable,
            outcome=VALIDATION_OUTCOME,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"atomic-content-harness-validation-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(report)
        return result

    def validate(self, report: AtomicContentHarnessValidationReport) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != VALIDATION_RECEIPT_SCHEMA_ID
            or self.run_id != report.run_id
            or self.definition_id != report.definition_id
            or self.definition_hash != report.definition_hash
            or self.report_id != report.report_id
            or self.report_hash != report.report_hash
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.dimension_count != len(report.dimensions)
            or self.section_count != len(report.section_ids)
            or self.internal_compatibility != INTERNAL_COMPATIBILITY
            or self.external_target_compatibility != EXTERNAL_TARGET_COMPATIBILITY
            or not self.synthetic_not_certifiable
            or self.outcome != VALIDATION_OUTCOME
            or self.receipt_id
            != f"atomic-content-harness-validation-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise TargetValidationLineageInvalid(
                "Validation receipt does not match its immutable report."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "schema_id": self.schema_id,
            "command_id": self.command_id,
            "run_id": self.run_id,
            "definition_id": self.definition_id,
            "definition_hash": self.definition_hash,
            "report_id": self.report_id,
            "report_hash": self.report_hash,
            "authority_identity": self.authority_identity,
            "event_ids": list(self.event_ids),
            "stream_version": self.stream_version,
            "dimension_count": self.dimension_count,
            "section_count": self.section_count,
            "internal_compatibility": self.internal_compatibility,
            "external_target_compatibility": self.external_target_compatibility,
            "synthetic_not_certifiable": self.synthetic_not_certifiable,
            "outcome": self.outcome,
        })


@dataclass(frozen=True, slots=True)
class AtomicContentHarnessValidationInvalidation:
    invalidation_id: str
    invalidation_hash: str
    schema_id: str
    report_ref: str
    definition_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        report_ref: str,
        definition_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "AtomicContentHarnessValidationInvalidation":
        if not all(value.strip() for value in (
            invalidation_id,
            report_ref,
            definition_ref,
            upstream_invalidation_ref,
            reason,
            authority_identity,
        )):
            raise TargetValidationInputInvalid(
                "Validation invalidation requires complete authority and lineage."
            )
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            schema_id=VALIDATION_INVALIDATION_SCHEMA_ID,
            report_ref=report_ref,
            definition_ref=definition_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "invalidation_id": self.invalidation_id,
            "schema_id": self.schema_id,
            "report_ref": self.report_ref,
            "definition_ref": self.definition_ref,
            "upstream_invalidation_ref": self.upstream_invalidation_ref,
            "reason": self.reason,
            "authority_identity": self.authority_identity,
        })


def _all_mapping_keys(value: object) -> tuple[str, ...]:
    keys: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            keys.append(str(key))
            keys.extend(_all_mapping_keys(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            keys.extend(_all_mapping_keys(item))
    return tuple(keys)


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
