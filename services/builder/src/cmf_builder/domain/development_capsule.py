from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Mapping, Sequence

from cmf_builder.domain.atomic_harness_definition import AtomicHarnessDefinition
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    AtomicContentHarnessValidationReport,
)


CAPSULE_SCHEMA_ID = "cmf-builder-versioned-traceable-development-capsule/v1"
CAPSULE_RECEIPT_SCHEMA_ID = "cmf-builder-development-capsule-receipt/v1"
CAPSULE_INVALIDATION_SCHEMA_ID = "cmf-builder-development-capsule-invalidation/v1"
CAPSULE_INPUT_PATH = (
    "development-capsules/ST-11.01/SYNTHETIC_DEVELOPMENT_CAPSULE_INPUT.json"
)
CAPSULE_INPUT_SHA256 = (
    "fbfd88e0242df4be892676afa8b1a6360dd1dfc4a52e36fc749e8d0f5c93905a"
)
CAPSULE_PROFILE_ID = "synthetic_text_normalization_v1"
CAPSULE_VERSION = "1.0.0"
CAPSULE_MODE = "SYNTHETIC_BUILDER_PROOF"
CAPSULE_OUTCOME = "VERSIONED_TRACEABLE_SYNTHETIC_DEVELOPMENT_CAPSULE_GENERATED"
OWNED_OBLIGATIONS = ("D029", "FR-151", "FR-152", "FR-153", "FR-154", "FR-155")
DIRECT_DEPENDENCIES = ("ST-03.05", "ST-04.05", "ST-05.02", "ST-07.04")
REQUIRED_CAPSULE_SECTIONS = (
    "accepted_requirements",
    "authority",
    "atomic_harness_definition",
    "upstream_lineage",
    "architecture_and_responsibility_boundaries",
    "contracts_and_compatibility",
    "justified_scaffolding",
    "examples_and_fixtures",
    "acceptance_criteria_and_tests",
    "observability",
    "rollback_and_invalidation",
    "implementation_scope",
    "prohibited_scope",
    "dependency_order",
    "completion_receipt_contract",
)
REQUIRED_TEST_CLASSES = (
    "acceptance",
    "negative_contract",
    "authority",
    "traceability",
    "determinism",
    "portability",
    "idempotency",
    "replay",
    "invalidation",
    "observability",
    "rollback",
    "architecture_boundary",
)
REQUIRED_CONTRACT_VERSIONS = (
    ("AtomicContentHarnessValidationReport", "1.0.0"),
    ("AtomicHarnessDefinition", "1.0.0"),
    ("DevelopmentCapsule", "1.0.0"),
    ("StoryCompletionReceipt", "1.0.0"),
)


class DevelopmentCapsuleError(Exception):
    code = "DevelopmentCapsuleError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class DevelopmentCapsuleInputInvalid(DevelopmentCapsuleError):
    code = "DevelopmentCapsuleInputInvalid"


class DevelopmentCapsuleTraceInvalid(DevelopmentCapsuleError):
    code = "DevelopmentCapsuleTraceInvalid"


class DevelopmentCapsuleAuthorityInvalid(DevelopmentCapsuleError):
    code = "DevelopmentCapsuleAuthorityInvalid"


class DevelopmentCapsuleScopeInvalid(DevelopmentCapsuleError):
    code = "DevelopmentCapsuleScopeInvalid"


class DevelopmentCapsuleInvalidatedError(DevelopmentCapsuleError):
    code = "DevelopmentCapsuleInvalidated"


@dataclass(frozen=True, slots=True)
class DevelopmentCapsuleReference:
    reference_id: str
    reference_kind: str
    version: str
    content_hash: str
    provenance: str

    def validate(self) -> None:
        if (
            not all(
                value.strip()
                for value in (
                    self.reference_id,
                    self.reference_kind,
                    self.version,
                    self.content_hash,
                    self.provenance,
                )
            )
            or not _is_sha256(self.content_hash)
            or _is_absolute_path(self.reference_id)
            or _is_absolute_path(self.provenance)
        ):
            raise DevelopmentCapsuleTraceInvalid(
                "Every capsule reference must be portable, versioned and hash-pinned.",
                reference_id=self.reference_id,
            )

    def canonical_dict(self) -> dict[str, str]:
        return {
            "reference_id": self.reference_id,
            "reference_kind": self.reference_kind,
            "version": self.version,
            "content_hash": self.content_hash,
            "provenance": self.provenance,
        }


@dataclass(frozen=True, slots=True)
class DevelopmentCapsuleSection:
    section_id: str
    summary: str
    reference_ids: tuple[str, ...]
    evidence_hashes: tuple[str, ...]

    def validate(self, known_reference_ids: frozenset[str]) -> None:
        if (
            self.section_id not in REQUIRED_CAPSULE_SECTIONS
            or not self.summary.strip()
            or not self.reference_ids
            or tuple(sorted(set(self.reference_ids))) != self.reference_ids
            or not set(self.reference_ids).issubset(known_reference_ids)
            or not self.evidence_hashes
            or tuple(sorted(set(self.evidence_hashes))) != self.evidence_hashes
            or any(not _is_sha256(value) for value in self.evidence_hashes)
        ):
            raise DevelopmentCapsuleTraceInvalid(
                "Every capsule section needs canonical references and immutable evidence.",
                section_id=self.section_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "section_id": self.section_id,
            "summary": self.summary,
            "reference_ids": list(self.reference_ids),
            "evidence_hashes": list(self.evidence_hashes),
        }


@dataclass(frozen=True, slots=True)
class VersionedTraceableDevelopmentCapsule:
    capsule_id: str
    capsule_hash: str
    schema_id: str
    schema_version: str
    capsule_version: str
    active_mode: str
    profile_id: str
    run_id: str
    definition_id: str
    definition_hash: str
    validation_id: str
    validation_hash: str
    input_path: str
    input_hash: str
    obligation_ids: tuple[str, ...]
    dependency_order: tuple[str, ...]
    contract_versions: tuple[tuple[str, str], ...]
    references: tuple[DevelopmentCapsuleReference, ...]
    sections: tuple[DevelopmentCapsuleSection, ...]
    scaffolding: tuple[tuple[str, str], ...]
    test_classes: tuple[str, ...]
    lineage: tuple[str, ...]
    authority_identity: str
    internal_compatibility: str
    external_target_compatibility: str
    repository_owned: bool
    synthetic: bool
    category_neutral: bool
    production_eligible: bool
    certified: bool
    certification_state: str
    external_skills_required: int
    external_runtimes_required: int
    generated_product_implementation: bool
    completion_receipt_contract: str
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        definition: AtomicHarnessDefinition,
        validation: AtomicContentHarnessValidationReport,
        capsule_input: Mapping[str, object],
        authority_identity: str,
    ) -> "VersionedTraceableDevelopmentCapsule":
        _validate_input_contract(capsule_input)
        validation.validate(definition)
        references = _build_references(
            definition=definition,
            validation=validation,
            capsule_input=capsule_input,
        )
        reference_by_kind: dict[str, tuple[DevelopmentCapsuleReference, ...]] = {}
        for kind in (
            "authority",
            "requirement",
            "technical_spec",
            "accepted_adr",
            "dependency_receipt",
            "fixture",
            "atomic_harness_definition",
            "atomic_content_harness_validation",
        ):
            reference_by_kind[kind] = tuple(
                item for item in references if item.reference_kind == kind
            )
        input_hash = f"sha256:{CAPSULE_INPUT_SHA256}"

        def section(
            section_id: str,
            summary: str,
            selected: Sequence[DevelopmentCapsuleReference],
            extra_hashes: Sequence[str] = (),
        ) -> DevelopmentCapsuleSection:
            ids = tuple(sorted({item.reference_id for item in selected}))
            hashes = tuple(
                sorted({*(item.content_hash for item in selected), *extra_hashes})
            )
            return DevelopmentCapsuleSection(section_id, summary, ids, hashes)

        authority_refs = (
            *reference_by_kind["authority"],
            *reference_by_kind["technical_spec"],
            *reference_by_kind["accepted_adr"],
        )
        definition_refs = reference_by_kind["atomic_harness_definition"]
        validation_refs = reference_by_kind["atomic_content_harness_validation"]
        dependency_refs = reference_by_kind["dependency_receipt"]
        fixture_refs = reference_by_kind["fixture"]
        requirement_refs = reference_by_kind["requirement"]
        all_refs = tuple(references)
        sections = (
            section("accepted_requirements", "six_confirmed_owned_obligations_are_traced", requirement_refs, (input_hash,)),
            section("authority", "constitution_builder_v1_2_specs_and_adrs_are_hash_bound", authority_refs),
            section("atomic_harness_definition", "exact_validated_synthetic_definition_is_pinned", (*definition_refs, *validation_refs)),
            section("upstream_lineage", "complete_definition_and_validation_lineage_is_preserved", (*definition_refs, *validation_refs, *dependency_refs), tuple(value for value in definition.lineage if _is_sha256(value))),
            section("architecture_and_responsibility_boundaries", "module_phase_authority_and_external_boundaries_are_explicit", (*reference_by_kind["technical_spec"], *reference_by_kind["accepted_adr"], *definition_refs)),
            section("contracts_and_compatibility", "typed_contract_versions_and_compatibility_are_resolved", (*definition_refs, *validation_refs), (input_hash,)),
            section("justified_scaffolding", "only_three_synthetic_implementation_scaffolds_are_justified", requirement_refs, (input_hash,)),
            section("examples_and_fixtures", "four_repository_owned_examples_and_fixtures_are_hash_pinned", fixture_refs),
            section("acceptance_criteria_and_tests", "executable_acceptance_negative_and_lifecycle_test_classes_are declared", fixture_refs, (input_hash,)),
            section("observability", "deterministic_story_scoped_observations_are_required", (*validation_refs, *requirement_refs), (input_hash,)),
            section("rollback_and_invalidation", "atomic_failure_and_non_destructive_invalidation_are_required", (*dependency_refs, *validation_refs), (input_hash,)),
            section("implementation_scope", "only_the_synthetic_text_normalization_harness_is_in_scope", (*definition_refs, *requirement_refs), (input_hash,)),
            section("prohibited_scope", "external_products_runtime_production_and_certification_are_prohibited", (*authority_refs, *validation_refs), (input_hash,)),
            section("dependency_order", "four_BF_AM_009_predecessor_receipts_are_ordered_and_pinned", dependency_refs),
            section("completion_receipt_contract", "story_completion_evidence_contract_is_explicit", (*requirement_refs, *validation_refs), (input_hash,)),
        )
        scaffold = tuple(
            sorted(
                (str(item["path"]), str(item["reason"]))
                for item in _mapping_sequence(capsule_input, "scaffolding")
            )
        )
        lineage = tuple(
            sorted(
                {
                    *definition.lineage,
                    definition.definition_id,
                    definition.definition_hash,
                    validation.report_id,
                    validation.report_hash,
                    *(item.content_hash for item in all_refs),
                }
            )
        )
        candidate = cls(
            capsule_id="pending",
            capsule_hash="pending",
            schema_id=CAPSULE_SCHEMA_ID,
            schema_version="1.0.0",
            capsule_version=CAPSULE_VERSION,
            active_mode=CAPSULE_MODE,
            profile_id=CAPSULE_PROFILE_ID,
            run_id=definition.run_id,
            definition_id=definition.definition_id,
            definition_hash=definition.definition_hash,
            validation_id=validation.report_id,
            validation_hash=validation.report_hash,
            input_path=CAPSULE_INPUT_PATH,
            input_hash=input_hash,
            obligation_ids=OWNED_OBLIGATIONS,
            dependency_order=DIRECT_DEPENDENCIES,
            contract_versions=tuple(sorted(
                (str(key), str(value))
                for key, value in _mapping(capsule_input, "contract_versions").items()
            )),
            references=references,
            sections=sections,
            scaffolding=scaffold,
            test_classes=tuple(str(item) for item in _sequence(capsule_input, "test_classes")),
            lineage=lineage,
            authority_identity=authority_identity,
            internal_compatibility=validation.internal_compatibility,
            external_target_compatibility=validation.external_target_compatibility,
            repository_owned=True,
            synthetic=True,
            category_neutral=True,
            production_eligible=False,
            certified=False,
            certification_state="synthetic_not_certifiable",
            external_skills_required=0,
            external_runtimes_required=0,
            generated_product_implementation=False,
            completion_receipt_contract=str(
                capsule_input.get("completion_receipt_contract", "")
            ),
            outcome=CAPSULE_OUTCOME,
        )
        candidate.validate(definition, validation, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            capsule_id=f"development-capsule_{digest}",
            capsule_hash=f"sha256:{digest}",
        )
        result.validate(definition, validation)
        return result

    def validate(
        self,
        definition: AtomicHarnessDefinition,
        validation: AtomicContentHarnessValidationReport,
        *,
        verify_identity: bool = True,
    ) -> None:
        validation.validate(definition)
        reference_ids = tuple(item.reference_id for item in self.references)
        for item in self.references:
            item.validate()
        known = frozenset(reference_ids)
        for item in self.sections:
            item.validate(known)
        required_lineage = {
            *definition.lineage,
            definition.definition_id,
            definition.definition_hash,
            validation.report_id,
            validation.report_hash,
        }
        if (
            self.schema_id != CAPSULE_SCHEMA_ID
            or self.schema_version != "1.0.0"
            or self.capsule_version != CAPSULE_VERSION
            or self.active_mode != CAPSULE_MODE
            or self.profile_id != CAPSULE_PROFILE_ID
            or self.run_id != definition.run_id
            or self.definition_id != definition.definition_id
            or self.definition_hash != definition.definition_hash
            or self.validation_id != validation.report_id
            or self.validation_hash != validation.report_hash
            or self.input_path != CAPSULE_INPUT_PATH
            or self.input_hash != f"sha256:{CAPSULE_INPUT_SHA256}"
            or self.obligation_ids != OWNED_OBLIGATIONS
            or self.dependency_order != DIRECT_DEPENDENCIES
            or self.contract_versions != REQUIRED_CONTRACT_VERSIONS
            or tuple(item.section_id for item in self.sections)
            != REQUIRED_CAPSULE_SECTIONS
            or tuple(sorted(set(reference_ids))) != reference_ids
            or self.test_classes != REQUIRED_TEST_CLASSES
            or len(self.scaffolding) != 3
            or any(not path.strip() or not reason.strip() for path, reason in self.scaffolding)
            or any(_is_absolute_path(path) for path, _ in self.scaffolding)
            or not required_lineage.issubset(set(self.lineage))
            or not self.authority_identity.strip()
            or self.internal_compatibility != "PASS"
            or self.external_target_compatibility != EXTERNAL_TARGET_COMPATIBILITY
            or not self.repository_owned
            or not self.synthetic
            or not self.category_neutral
            or self.production_eligible
            or self.certified
            or self.certification_state != "synthetic_not_certifiable"
            or self.external_skills_required
            or self.external_runtimes_required
            or self.generated_product_implementation
            or self.completion_receipt_contract
            != "cmf-builder-story-completion-receipt/v1"
            or self.outcome != CAPSULE_OUTCOME
            or definition.production_eligible
            or definition.certified
            or definition.external_skill_count
            or definition.external_runtime_count
            or definition.execution_performed
            or not definition.synthetic_not_certifiable
            or validation.production_eligible
            or validation.certified
            or not validation.synthetic_not_certifiable
        ):
            raise DevelopmentCapsuleTraceInvalid(
                "The Development Capsule is incomplete, inconsistent or broadened."
            )
        portable_values = (
            *self.lineage,
            *(item.reference_id for item in self.references),
            *(path for path, _ in self.scaffolding),
        )
        if any(_is_absolute_path(value) for value in portable_values):
            raise DevelopmentCapsuleScopeInvalid(
                "Portable Development Capsule evidence contains a machine-local path."
            )
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.capsule_id != f"development-capsule_{digest}"
                or self.capsule_hash != f"sha256:{digest}"
            ):
                raise DevelopmentCapsuleTraceInvalid(
                    "Development Capsule identity is not reproducible."
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "capsule_version": self.capsule_version,
            "active_mode": self.active_mode,
            "profile_id": self.profile_id,
            "run_id": self.run_id,
            "definition_id": self.definition_id,
            "definition_hash": self.definition_hash,
            "validation_id": self.validation_id,
            "validation_hash": self.validation_hash,
            "input_path": self.input_path,
            "input_hash": self.input_hash,
            "obligation_ids": list(self.obligation_ids),
            "dependency_order": list(self.dependency_order),
            "contract_versions": {key: value for key, value in self.contract_versions},
            "references": [item.canonical_dict() for item in self.references],
            "sections": [item.canonical_dict() for item in self.sections],
            "scaffolding": [
                {"path": path, "reason": reason} for path, reason in self.scaffolding
            ],
            "test_classes": list(self.test_classes),
            "lineage": list(self.lineage),
            "authority_identity": self.authority_identity,
            "internal_compatibility": self.internal_compatibility,
            "external_target_compatibility": self.external_target_compatibility,
            "repository_owned": self.repository_owned,
            "synthetic": self.synthetic,
            "category_neutral": self.category_neutral,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "certification_state": self.certification_state,
            "external_skills_required": self.external_skills_required,
            "external_runtimes_required": self.external_runtimes_required,
            "generated_product_implementation": self.generated_product_implementation,
            "completion_receipt_contract": self.completion_receipt_contract,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class DevelopmentCapsuleReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    capsule_id: str
    capsule_hash: str
    definition_id: str
    definition_hash: str
    validation_id: str
    validation_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    section_count: int
    reference_count: int
    obligation_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        capsule: VersionedTraceableDevelopmentCapsule,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "DevelopmentCapsuleReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=CAPSULE_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=capsule.run_id,
            capsule_id=capsule.capsule_id,
            capsule_hash=capsule.capsule_hash,
            definition_id=capsule.definition_id,
            definition_hash=capsule.definition_hash,
            validation_id=capsule.validation_id,
            validation_hash=capsule.validation_hash,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            section_count=len(capsule.sections),
            reference_count=len(capsule.references),
            obligation_count=len(capsule.obligation_ids),
            outcome=CAPSULE_OUTCOME,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"development-capsule-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(capsule)
        return result

    def validate(self, capsule: VersionedTraceableDevelopmentCapsule) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != CAPSULE_RECEIPT_SCHEMA_ID
            or self.run_id != capsule.run_id
            or self.capsule_id != capsule.capsule_id
            or self.capsule_hash != capsule.capsule_hash
            or self.definition_id != capsule.definition_id
            or self.definition_hash != capsule.definition_hash
            or self.validation_id != capsule.validation_id
            or self.validation_hash != capsule.validation_hash
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.section_count != len(capsule.sections)
            or self.reference_count != len(capsule.references)
            or self.obligation_count != len(capsule.obligation_ids)
            or self.outcome != CAPSULE_OUTCOME
            or self.receipt_id != f"development-capsule-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise DevelopmentCapsuleTraceInvalid(
                "Development Capsule receipt does not match its immutable capsule."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "capsule_id": self.capsule_id,
                "capsule_hash": self.capsule_hash,
                "definition_id": self.definition_id,
                "definition_hash": self.definition_hash,
                "validation_id": self.validation_id,
                "validation_hash": self.validation_hash,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "section_count": self.section_count,
                "reference_count": self.reference_count,
                "obligation_count": self.obligation_count,
                "outcome": self.outcome,
            }
        )


@dataclass(frozen=True, slots=True)
class DevelopmentCapsuleInvalidation:
    invalidation_id: str
    invalidation_hash: str
    schema_id: str
    capsule_ref: str
    validation_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        capsule_ref: str,
        validation_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "DevelopmentCapsuleInvalidation":
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                capsule_ref,
                validation_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise DevelopmentCapsuleInputInvalid(
                "Capsule invalidation requires complete authority and lineage."
            )
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            schema_id=CAPSULE_INVALIDATION_SCHEMA_ID,
            capsule_ref=capsule_ref,
            validation_ref=validation_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "schema_id": self.schema_id,
                "capsule_ref": self.capsule_ref,
                "validation_ref": self.validation_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _validate_input_contract(value: Mapping[str, object]) -> None:
    classification = _mapping(value, "classification")
    compatibility = _mapping(value, "compatibility")
    if (
        value.get("schema_version")
        != "cmf-builder-synthetic-development-capsule-input/v1"
        or value.get("story_id") != "ST-11.01"
        or value.get("active_mode") != CAPSULE_MODE
        or value.get("capsule_profile") != CAPSULE_PROFILE_ID
        or value.get("capsule_version") != CAPSULE_VERSION
        or tuple(_sequence(value, "required_sections")) != REQUIRED_CAPSULE_SECTIONS
        or tuple(_sequence(value, "owned_obligations")) != OWNED_OBLIGATIONS
        or tuple(_sequence(value, "direct_dependencies")) != DIRECT_DEPENDENCIES
        or tuple(_sequence(value, "test_classes")) != REQUIRED_TEST_CLASSES
        or tuple(
            sorted(
                (str(key), str(item))
                for key, item in _mapping(value, "contract_versions").items()
            )
        )
        != REQUIRED_CONTRACT_VERSIONS
        or compatibility.get("atomic_content_harness_internal") != "PASS"
        or compatibility.get("external_target")
        != EXTERNAL_TARGET_COMPATIBILITY
        or not classification.get("repository_owned")
        or not classification.get("synthetic")
        or not classification.get("category_neutral")
        or classification.get("production_eligible")
        or classification.get("certified")
        or classification.get("certification_state")
        != "synthetic_not_certifiable"
        or classification.get("external_skills_required") != 0
        or classification.get("external_runtimes_required") != 0
        or value.get("completion_receipt_contract")
        != "cmf-builder-story-completion-receipt/v1"
        or value.get("expected_outcome") != CAPSULE_OUTCOME
        or len(_mapping_sequence(value, "authority_references")) != 2
        or len(_mapping_sequence(value, "requirement_references")) != 3
        or len(_mapping_sequence(value, "technical_spec_references")) != 5
        or len(_mapping_sequence(value, "accepted_adr_references")) != 5
        or len(_mapping_sequence(value, "dependency_receipts")) != 4
        or len(_mapping_sequence(value, "examples_and_fixtures")) != 4
        or len(_mapping_sequence(value, "scaffolding")) != 3
    ):
        raise DevelopmentCapsuleInputInvalid(
            "Synthetic Development Capsule input is incomplete or broadened."
        )
    for key in (
        "authority_references",
        "requirement_references",
        "technical_spec_references",
        "accepted_adr_references",
        "dependency_receipts",
        "examples_and_fixtures",
    ):
        for item in _mapping_sequence(value, key):
            if (
                not str(item.get("path", "")).strip()
                or not _is_sha256(f"sha256:{item.get('sha256', '')}")
            ):
                raise DevelopmentCapsuleInputInvalid(
                    "Every generated-capsule input reference must be hash-pinned.",
                    reference_group=key,
                )
    for item in _mapping_sequence(value, "scaffolding"):
        if not str(item.get("path", "")).strip() or not str(
            item.get("reason", "")
        ).strip():
            raise DevelopmentCapsuleInputInvalid(
                "Every scaffold requires a governed implementation reason."
            )


def _build_references(
    *,
    definition: AtomicHarnessDefinition,
    validation: AtomicContentHarnessValidationReport,
    capsule_input: Mapping[str, object],
) -> tuple[DevelopmentCapsuleReference, ...]:
    references: list[DevelopmentCapsuleReference] = []
    groups = (
        ("authority_references", "authority"),
        ("requirement_references", "requirement"),
        ("technical_spec_references", "technical_spec"),
        ("accepted_adr_references", "accepted_adr"),
        ("dependency_receipts", "dependency_receipt"),
        ("examples_and_fixtures", "fixture"),
    )
    for key, kind in groups:
        for item in _mapping_sequence(capsule_input, key):
            identifier = str(item.get("id") or item.get("story_id") or "1.0.0")
            references.append(
                DevelopmentCapsuleReference(
                    reference_id=str(item["path"]),
                    reference_kind=kind,
                    version=identifier,
                    content_hash=f"sha256:{item['sha256']}",
                    provenance=CAPSULE_INPUT_PATH,
                )
            )
    references.extend(
        (
            DevelopmentCapsuleReference(
                reference_id=definition.definition_id,
                reference_kind="atomic_harness_definition",
                version=definition.harness_version,
                content_hash=definition.definition_hash,
                provenance=definition.ir_id,
            ),
            DevelopmentCapsuleReference(
                reference_id=validation.report_id,
                reference_kind="atomic_content_harness_validation",
                version=validation.schema_version,
                content_hash=validation.report_hash,
                provenance=definition.definition_id,
            ),
        )
    )
    result = tuple(sorted(references, key=lambda item: item.reference_id))
    if len({item.reference_id for item in result}) != len(result):
        raise DevelopmentCapsuleTraceInvalid(
            "Capsule references contain duplicate identities."
        )
    return result


def _mapping(value: Mapping[str, object], key: str) -> Mapping[str, object]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise DevelopmentCapsuleInputInvalid(f"{key} must be a mapping.")
    return item


def _sequence(value: Mapping[str, object], key: str) -> tuple[object, ...]:
    item = value.get(key)
    if not isinstance(item, list):
        raise DevelopmentCapsuleInputInvalid(f"{key} must be a list.")
    return tuple(item)


def _mapping_sequence(
    value: Mapping[str, object], key: str
) -> tuple[Mapping[str, object], ...]:
    items = _sequence(value, key)
    if any(not isinstance(item, Mapping) for item in items):
        raise DevelopmentCapsuleInputInvalid(f"{key} entries must be mappings.")
    return tuple(item for item in items if isinstance(item, Mapping))


def _is_sha256(value: str) -> bool:
    if not value.startswith("sha256:") or len(value) != 71:
        return False
    try:
        int(value[7:], 16)
    except ValueError:
        return False
    return True


def _is_absolute_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return normalized.startswith("/") or ":/" in normalized


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
