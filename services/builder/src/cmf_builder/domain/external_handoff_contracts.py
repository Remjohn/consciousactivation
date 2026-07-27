from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Mapping, Sequence

from cmf_builder.domain.category_syntax import GovernedRef


VAE_TARGET = "visual_asset_editor"
DELEGATION_TARGET = "content_asset_delegation_contract"
EXTERNAL_TARGETS = frozenset({VAE_TARGET, DELEGATION_TARGET})
DELEGATION_VERSION = "1.1.0-rc.4"
DELEGATION_RELEASE_DIGEST = "sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44"
DELEGATION_TRUST = "local_unsigned_release_candidate"
ST_07_02_COMPLETION_RECEIPT_SHA256 = "ee13f9b6601ab1b166f16d2d30fb043f1441745d9e8146248d2d6d7d08caa681"
SYNTHETIC_DEFINITION_ID = "atomic-harness-definition_086b1273b9a5cdb60c84f2bd3694c21e2af356646a2b918ecefb8c22ff441adc"
SYNTHETIC_DEFINITION_SHA256 = "086b1273b9a5cdb60c84f2bd3694c21e2af356646a2b918ecefb8c22ff441adc"
SYNTHETIC_DEFINITION_RECEIPT_ID = "atomic-harness-definition-receipt_cc7c85739cf7bb256b7f19646bac1d7026520c9a4833f3e969ecfa1c6119bca5"
SYNTHETIC_DEFINITION_RECEIPT_SHA256 = "cc7c85739cf7bb256b7f19646bac1d7026520c9a4833f3e969ecfa1c6119bca5"
EXTERNAL_VALIDATION_PENDING = "EXTERNAL_VALIDATION_PENDING"
LOCAL_VALIDATION_ONLY = "BUILDER_LOCAL_CONTRACT_VALIDATION_ONLY"
LOCAL_TEST_DOUBLE_ONLY = "LOCAL_TEST_DOUBLE_ONLY"
_SHA256 = re.compile(r"^[a-f0-9]{64}$")

_SOURCE_KIND_MAP: Mapping[str, str] = {
    "Interview Expression": "interview_expression",
    "ReelCast": "interview_expression",
    "Public Comment": "public_comment",
    "Reply / DM": "direct_message_reply",
    "Live premise": "live_premise",
    "Research-derived synthesis": "research_synthesis",
    "Legacy migration": "legacy_migrated",
}
_GOVERNED_SOURCE_KINDS = frozenset(
    {
        "interview_expression",
        "public_comment",
        "direct_message_reply",
        "authored_source",
        "operator_supplied",
        "live_premise",
        "research_synthesis",
        "legacy_migrated",
    }
)
_REQUIRED_LINEAGE = frozenset(
    {
        "activative_intelligence_pack",
        "identity_dna",
        "context_premise",
        "resonance_map",
        "matrix_edge_product",
        "activative_call",
        "activation_contract",
        "visual_semantic_pack",
        "visual_narrative_program",
        "feature_contract",
        "somatic_route",
        "composition_intent",
    }
)
STRUCTURAL_LINEAGE_CLASSIFICATION = (
    "STRUCTURAL_SYNTHETIC_LOCAL_FIXTURE_NOT_PARENT_MEANING_OR_REAL_PROFILE_EVIDENCE"
)
INTERVIEW_PLACEHOLDER_CLASSIFICATION = (
    "NON_PERSONAL_STRUCTURAL_PLACEHOLDERS_NOT_HUMAN_TRUTH"
)
INTERVIEW_NOT_APPLICABLE = "NOT_APPLICABLE_NON_INTERVIEW_SOURCE"
_STRUCTURAL_FIXTURE_AUTHORITY = "Atomic Harness Builder OD structural fixture authority"
_INTERVIEW_PLACEHOLDER_AUTHORITY = "ST-07.03 non-personal structural placeholder authority"


def _fixture_ref(role: str, *, authority: str, prefix: str) -> GovernedRef:
    object_id = f"{prefix}-{role}-v1"
    payload = (
        f"{object_id}|1.0.0|{authority}|{role}|"
        f"{SYNTHETIC_DEFINITION_SHA256}|{SYNTHETIC_DEFINITION_RECEIPT_SHA256}"
    )
    return GovernedRef(
        object_id=object_id,
        version="1.0.0",
        sha256=sha256(payload.encode()).hexdigest(),
        authority=authority,
        lineage_role=role,
    )


OD_STRUCTURAL_LINEAGE_FIXTURE_REFS = tuple(
    _fixture_ref(role, authority=_STRUCTURAL_FIXTURE_AUTHORITY, prefix="od-st0703-structural")
    for role in sorted(_REQUIRED_LINEAGE)
)
OD_INTERVIEW_PLACEHOLDER_REFS = tuple(
    _fixture_ref(role, authority=_INTERVIEW_PLACEHOLDER_AUTHORITY, prefix="od-st0703-non-personal")
    for role in ("expression_moment", "reaction_receipt")
)


def structural_lineage_fixture_ref(role: str) -> GovernedRef:
    try:
        return next(ref for ref in OD_STRUCTURAL_LINEAGE_FIXTURE_REFS if ref.lineage_role == role)
    except StopIteration as error:
        raise HandoffContractRejected("Requested structural fixture role is not governed.") from error


def interview_structural_placeholder_ref(role: str) -> GovernedRef:
    try:
        return next(ref for ref in OD_INTERVIEW_PLACEHOLDER_REFS if ref.lineage_role == role)
    except StopIteration as error:
        raise HandoffContractRejected("Requested interview placeholder role is not governed.") from error


OD_STRUCTURAL_LINEAGE_MANIFEST_HASH = "sha256:" + sha256(
    (
        json.dumps(
            {
                "schema_version": "cmf-builder-od-structural-lineage-fixture/v1",
                "classification": STRUCTURAL_LINEAGE_CLASSIFICATION,
                "st_07_02_definition_hash": f"sha256:{SYNTHETIC_DEFINITION_SHA256}",
                "st_07_02_definition_receipt_hash": f"sha256:{SYNTHETIC_DEFINITION_RECEIPT_SHA256}",
                "st_07_02_completion_receipt_sha256": ST_07_02_COMPLETION_RECEIPT_SHA256,
                "refs": [ref.canonical_dict() for ref in OD_STRUCTURAL_LINEAGE_FIXTURE_REFS],
                "interview_placeholders": [ref.canonical_dict() for ref in OD_INTERVIEW_PLACEHOLDER_REFS],
                "real_profile_evidence": False,
                "human_truth": False,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode()
).hexdigest()


class ExternalHandoffError(ValueError):
    pass


class HandoffContractRejected(ExternalHandoffError):
    pass


class SourceProvenanceRejected(HandoffContractRejected):
    pass


class WrongReadingLockRejected(HandoffContractRejected):
    pass


class HandoffAuthorityRejected(ExternalHandoffError):
    pass


@dataclass(frozen=True, slots=True)
class SourceProvenance:
    builder_source: str
    evidence_ref: GovernedRef
    authoritative_classification: str | None = None
    migration_receipt_ref: GovernedRef | None = None

    def __post_init__(self) -> None:
        _text(self.builder_source, "builder_source")
        self.evidence_ref.validate()
        if self.evidence_ref.lineage_role != "source_provenance":
            raise SourceProvenanceRejected("Source provenance requires its exact governed evidence role.")
        if self.authoritative_classification is not None:
            _text(self.authoritative_classification, "authoritative_classification")
        if self.migration_receipt_ref is not None:
            self.migration_receipt_ref.validate()
            if self.migration_receipt_ref.lineage_role != "migration_receipt":
                raise SourceProvenanceRejected("Legacy source requires a traceable migration receipt.")

    @property
    def source_kind(self) -> str:
        if self.builder_source == "Operator-authored source":
            if self.authoritative_classification not in {"authored_source", "operator_supplied"}:
                raise SourceProvenanceRejected(
                    "Ambiguous operator source must be authoritatively classified; guessing is prohibited."
                )
            result = self.authoritative_classification
        else:
            result = _SOURCE_KIND_MAP.get(self.builder_source)
            if result is None:
                raise SourceProvenanceRejected("Unknown or unsupported source kind is prohibited.")
            if self.authoritative_classification not in {None, result}:
                raise SourceProvenanceRejected("Source classification contradicts authoritative evidence.")
        if result == "legacy_migrated" and self.migration_receipt_ref is None:
            raise SourceProvenanceRejected("Legacy migration requires a traceable migration receipt.")
        if result not in _GOVERNED_SOURCE_KINDS:
            raise SourceProvenanceRejected("Source kind is not governed by the pinned mapping.")
        return result

    def canonical_dict(self) -> dict[str, object]:
        return {
            "builder_source": self.builder_source,
            "source_kind": self.source_kind,
            "evidence_ref": self.evidence_ref.canonical_dict(),
            "migration_receipt_ref": (
                None if self.migration_receipt_ref is None else self.migration_receipt_ref.canonical_dict()
            ),
        }


@dataclass(frozen=True, slots=True)
class WrongReadingLock:
    lock_id: str
    statement: str
    meaning_hash: str
    scope_paths: tuple[str, ...]
    enforcement_level: int

    def __post_init__(self) -> None:
        _text(self.lock_id, "lock_id")
        _text(self.statement, "statement")
        _digest(self.meaning_hash, "meaning_hash")
        if not self.scope_paths or len(set(self.scope_paths)) != len(self.scope_paths):
            raise WrongReadingLockRejected("Wrong-reading-lock scope must be non-empty and unique.")
        for value in self.scope_paths:
            _text(value, "scope_path")
        if type(self.enforcement_level) is not int or self.enforcement_level < 1:
            raise WrongReadingLockRejected("Wrong-reading-lock enforcement must be a positive level.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "lock_id": self.lock_id,
            "statement": self.statement,
            "meaning_hash": self.meaning_hash,
            "scope_paths": list(sorted(self.scope_paths)),
            "enforcement_level": self.enforcement_level,
        }


@dataclass(frozen=True, slots=True)
class ExternalHandoffInput:
    request_id: str
    request_version: str
    target_id: str
    run_ref: GovernedRef
    atomic_harness_definition_ref: GovernedRef
    atomic_harness_definition_receipt_ref: GovernedRef
    st_07_02_completion_receipt_sha256: str
    source: SourceProvenance
    semantic_lineage: tuple[GovernedRef, ...]
    wrong_reading_locks: tuple[WrongReadingLock, ...]
    inherited_parent_locks: tuple[WrongReadingLock, ...]
    authority_ref: GovernedRef
    local_contract_pin: str
    production_ready: bool = False
    certified: bool = False


@dataclass(frozen=True, slots=True)
class CompiledExternalHandoffRequest:
    request_id: str
    request_version: str
    target_id: str
    run_ref: GovernedRef
    atomic_harness_definition_ref: GovernedRef
    atomic_harness_definition_receipt_ref: GovernedRef
    st_07_02_completion_receipt_sha256: str
    source_kind: str
    source_provenance_ref: GovernedRef
    semantic_lineage: tuple[GovernedRef, ...]
    structural_lineage_manifest_hash: str
    structural_lineage_classification: str
    interview_provenance_classification: str
    wrong_reading_locks: tuple[WrongReadingLock, ...]
    inherited_parent_locks: tuple[WrongReadingLock, ...]
    authority_ref: GovernedRef
    local_contract_pin: str
    external_contract_digest: str | None
    external_contract_trust: str | None
    external_compatibility: str
    request_hash: str
    canonical_bytes: bytes
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        _text(self.request_id, "request_id")
        _text(self.request_version, "request_version")
        if self.target_id not in EXTERNAL_TARGETS:
            raise HandoffContractRejected("Compiled handoff target is not governed.")
        for ref, role in (
            (self.run_ref, "builder_run"),
            (self.atomic_harness_definition_ref, "atomic_harness_definition"),
            (self.atomic_harness_definition_receipt_ref, "atomic_harness_definition_receipt"),
            (self.source_provenance_ref, "source_provenance"),
            (self.authority_ref, "handoff_authority"),
        ):
            ref.validate()
            if ref.lineage_role != role:
                raise HandoffAuthorityRejected(f"Expected exact {role} reference.")
        if (
            self.atomic_harness_definition_ref.object_id != SYNTHETIC_DEFINITION_ID
            or self.atomic_harness_definition_ref.version != "1.0.0"
            or self.atomic_harness_definition_ref.sha256 != SYNTHETIC_DEFINITION_SHA256
            or self.atomic_harness_definition_ref.authority != "Atomic Harness Builder"
            or self.atomic_harness_definition_receipt_ref.object_id != SYNTHETIC_DEFINITION_RECEIPT_ID
            or self.atomic_harness_definition_receipt_ref.version != "1.0.0"
            or self.atomic_harness_definition_receipt_ref.sha256 != SYNTHETIC_DEFINITION_RECEIPT_SHA256
            or self.atomic_harness_definition_receipt_ref.authority != "Atomic Harness Builder"
            or self.st_07_02_completion_receipt_sha256 != ST_07_02_COMPLETION_RECEIPT_SHA256
        ):
            raise HandoffContractRejected("Handoff is not bound to the exact frozen ST-07.02 parent evidence.")
        if self.source_kind not in _GOVERNED_SOURCE_KINDS:
            raise SourceProvenanceRejected("Compiled source kind is not governed.")
        _validate_lineage(self.semantic_lineage, self.source_kind)
        expected_interview_classification = (
            INTERVIEW_PLACEHOLDER_CLASSIFICATION
            if self.source_kind == "interview_expression"
            else INTERVIEW_NOT_APPLICABLE
        )
        if (
            self.structural_lineage_manifest_hash != OD_STRUCTURAL_LINEAGE_MANIFEST_HASH
            or self.structural_lineage_classification != STRUCTURAL_LINEAGE_CLASSIFICATION
            or self.interview_provenance_classification != expected_interview_classification
        ):
            raise HandoffContractRejected("Structural lineage fixture classification or manifest identity drifted.")
        _validate_locks(self.wrong_reading_locks, self.inherited_parent_locks)
        if self.target_id == DELEGATION_TARGET:
            if (
                self.local_contract_pin != DELEGATION_VERSION
                or self.external_contract_digest != DELEGATION_RELEASE_DIGEST
                or self.external_contract_trust != DELEGATION_TRUST
            ):
                raise HandoffContractRejected("Delegation handoff does not preserve the exact RC4 identity and trust.")
        elif (
            self.local_contract_pin != "builder-local-vae-interface/v1"
            or self.external_contract_digest is not None
            or self.external_contract_trust is not None
        ):
            raise HandoffContractRejected("VAE local fixture cannot claim an external contract identity.")
        expected = _request_content(self)
        expected_bytes = _canonical_json(expected)
        if self.canonical_bytes != expected_bytes:
            raise HandoffContractRejected("Handoff canonical bytes do not match governed fields.")
        if self.request_hash != f"sha256:{sha256(expected_bytes).hexdigest()}":
            raise HandoffContractRejected("Handoff request identity does not match governed fields.")

    def canonical_dict(self) -> dict[str, object]:
        value = json.loads(self.canonical_bytes.decode("utf-8"))
        value["request_hash"] = self.request_hash
        return value


@dataclass(frozen=True, slots=True)
class LocalCompatibilityValidationReceipt:
    receipt_id: str
    request_identity: str
    target_profile_identity: str
    local_contract_pin: str
    external_contract_digest: str | None
    external_contract_trust: str | None
    mapping_identity: str
    structural_lineage_classification: str
    interview_provenance_classification: str
    input_hash: str
    output_hash: str
    validation_outcome: str
    limitations: tuple[str, ...]
    authority: str = LOCAL_VALIDATION_ONLY
    external_compatibility: str = EXTERNAL_VALIDATION_PENDING

    def __post_init__(self) -> None:
        if self.authority != LOCAL_VALIDATION_ONLY or self.external_compatibility != EXTERNAL_VALIDATION_PENDING:
            raise HandoffAuthorityRejected("Local validation cannot represent external compatibility.")
        for value in (self.request_identity, self.input_hash, self.output_hash):
            _digest(value, "receipt hash")
        if self.request_identity != self.input_hash:
            raise HandoffContractRejected("Local validation input does not link to the request.")
        if self.target_profile_identity == DELEGATION_TARGET:
            if (
                self.local_contract_pin != DELEGATION_VERSION
                or self.external_contract_digest != DELEGATION_RELEASE_DIGEST
                or self.external_contract_trust != DELEGATION_TRUST
            ):
                raise HandoffContractRejected("Local receipt does not preserve the exact RC4 identity and trust.")
        elif self.target_profile_identity == VAE_TARGET:
            if (
                self.local_contract_pin != "builder-local-vae-interface/v1"
                or self.external_contract_digest is not None
                or self.external_contract_trust is not None
            ):
                raise HandoffContractRejected("VAE local receipt cannot claim an external contract identity.")
        else:
            raise HandoffContractRejected("Local validation target is not governed.")
        if self.mapping_identity != "builder-local-lossless-mapping/v1":
            raise HandoffContractRejected("Local mapping identity is not governed.")
        expected_output = f"sha256:{sha256((self.input_hash + ':local-fixture-validation/v1').encode()).hexdigest()}"
        if self.output_hash != expected_output:
            raise HandoffContractRejected("Local validation output identity is not reproducible.")
        if self.validation_outcome != "PASS_LOCAL_CONTRACT_FIXTURE":
            raise HandoffContractRejected("Local validation receipt has an unsupported outcome.")
        if self.structural_lineage_classification != STRUCTURAL_LINEAGE_CLASSIFICATION:
            raise HandoffContractRejected("Local receipt lost the structural fixture classification.")
        if self.interview_provenance_classification not in {
            INTERVIEW_PLACEHOLDER_CLASSIFICATION,
            INTERVIEW_NOT_APPLICABLE,
        }:
            raise HandoffContractRejected("Local receipt has an unsupported interview classification.")
        expected_limitations = (
            "NO_EXTERNAL_ACCEPTANCE",
            "NO_RUNTIME_VALIDATION",
            "NO_CERTIFICATION",
            "STRUCTURAL_FIXTURE_NOT_PARENT_MEANING_OR_REAL_PROFILE_EVIDENCE",
            (
                "INTERVIEW_PROVENANCE_NON_PERSONAL_PLACEHOLDERS_NOT_HUMAN_TRUTH"
                if self.interview_provenance_classification == INTERVIEW_PLACEHOLDER_CLASSIFICATION
                else "INTERVIEW_PROVENANCE_NOT_APPLICABLE"
            ),
        )
        if self.limitations != expected_limitations:
            raise HandoffContractRejected("Local validation must preserve the exact governed limitations.")
        core = self.identity_dict()
        expected_id = f"ST-07.03:LocalValidation:{sha256(_canonical_json(core)).hexdigest()}"
        if self.receipt_id != expected_id:
            raise HandoffContractRejected("Local validation receipt identity is not deterministic.")

    def identity_dict(self) -> dict[str, object]:
        return {
            "request_identity": self.request_identity,
            "target_profile_identity": self.target_profile_identity,
            "local_contract_pin": self.local_contract_pin,
            "external_contract_digest": self.external_contract_digest,
            "external_contract_trust": self.external_contract_trust,
            "mapping_identity": self.mapping_identity,
            "structural_lineage_classification": self.structural_lineage_classification,
            "interview_provenance_classification": self.interview_provenance_classification,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "validation_outcome": self.validation_outcome,
            "limitations": list(self.limitations),
            "authority": self.authority,
            "external_compatibility": self.external_compatibility,
        }


def compile_external_handoff(value: ExternalHandoffInput) -> CompiledExternalHandoffRequest:
    _text(value.request_id, "request_id")
    _text(value.request_version, "request_version")
    if value.target_id not in EXTERNAL_TARGETS:
        raise HandoffContractRejected("Only the distinct VAE and Delegation external targets are supported.")
    for ref, role in ((value.run_ref, "builder_run"), (value.authority_ref, "handoff_authority")):
        ref.validate()
        if ref.lineage_role != role:
            raise HandoffAuthorityRejected(f"Expected exact {role} reference.")
    for ref, role in (
        (value.atomic_harness_definition_ref, "atomic_harness_definition"),
        (value.atomic_harness_definition_receipt_ref, "atomic_harness_definition_receipt"),
    ):
        ref.validate()
        if ref.lineage_role != role:
            raise HandoffContractRejected(f"Expected exact {role} parent reference.")
    if (
        value.atomic_harness_definition_ref.object_id != SYNTHETIC_DEFINITION_ID
        or value.atomic_harness_definition_ref.version != "1.0.0"
        or value.atomic_harness_definition_ref.sha256 != SYNTHETIC_DEFINITION_SHA256
        or value.atomic_harness_definition_ref.authority != "Atomic Harness Builder"
        or value.atomic_harness_definition_receipt_ref.object_id != SYNTHETIC_DEFINITION_RECEIPT_ID
        or value.atomic_harness_definition_receipt_ref.version != "1.0.0"
        or value.atomic_harness_definition_receipt_ref.sha256 != SYNTHETIC_DEFINITION_RECEIPT_SHA256
        or value.atomic_harness_definition_receipt_ref.authority != "Atomic Harness Builder"
        or value.st_07_02_completion_receipt_sha256 != ST_07_02_COMPLETION_RECEIPT_SHA256
    ):
        raise HandoffContractRejected("Input is not bound to the exact governed ST-07.02 parent tuple.")
    if value.production_ready or value.certified:
        raise HandoffContractRejected("Local handoffs cannot claim production readiness or certification.")
    if value.target_id == DELEGATION_TARGET:
        if value.local_contract_pin != DELEGATION_VERSION:
            raise HandoffContractRejected("Delegation handoff requires the exact RC4 pin.")
    elif value.local_contract_pin != "builder-local-vae-interface/v1":
        raise HandoffContractRejected("VAE handoff requires the exact Builder-local interface fixture pin.")
    source_kind = value.source.source_kind
    lineage = _validate_lineage(value.semantic_lineage, source_kind)
    locks = _validate_locks(value.wrong_reading_locks, value.inherited_parent_locks)
    provisional = {
        "schema_version": "cmf-builder-local-external-handoff/v1",
        "request_id": value.request_id,
        "request_version": value.request_version,
        "target_id": value.target_id,
        "run_ref": value.run_ref.canonical_dict(),
        "atomic_harness_definition_ref": value.atomic_harness_definition_ref.canonical_dict(),
        "atomic_harness_definition_receipt_ref": value.atomic_harness_definition_receipt_ref.canonical_dict(),
        "st_07_02_completion_receipt_sha256": value.st_07_02_completion_receipt_sha256,
        "source_kind": source_kind,
        "source_provenance_ref": value.source.evidence_ref.canonical_dict(),
        "semantic_lineage": [ref.canonical_dict() for ref in lineage],
        "structural_lineage_manifest_hash": OD_STRUCTURAL_LINEAGE_MANIFEST_HASH,
        "structural_lineage_classification": STRUCTURAL_LINEAGE_CLASSIFICATION,
        "interview_provenance_classification": (
            INTERVIEW_PLACEHOLDER_CLASSIFICATION
            if source_kind == "interview_expression"
            else INTERVIEW_NOT_APPLICABLE
        ),
        "wrong_reading_locks": [item.canonical_dict() for item in locks],
        "inherited_parent_locks": [item.canonical_dict() for item in sorted(value.inherited_parent_locks, key=lambda item: item.lock_id)],
        "authority_ref": value.authority_ref.canonical_dict(),
        "local_contract_pin": value.local_contract_pin,
        "external_contract_digest_or_NOT_APPLICABLE": (
            DELEGATION_RELEASE_DIGEST if value.target_id == DELEGATION_TARGET else "NOT_APPLICABLE"
        ),
        "external_contract_trust_or_NOT_APPLICABLE": (
            DELEGATION_TRUST if value.target_id == DELEGATION_TARGET else "NOT_APPLICABLE"
        ),
        "external_compatibility": EXTERNAL_VALIDATION_PENDING,
        "production_ready": False,
        "certified": False,
    }
    canonical = _canonical_json(provisional)
    return CompiledExternalHandoffRequest(
        request_id=value.request_id,
        request_version=value.request_version,
        target_id=value.target_id,
        run_ref=value.run_ref,
        atomic_harness_definition_ref=value.atomic_harness_definition_ref,
        atomic_harness_definition_receipt_ref=value.atomic_harness_definition_receipt_ref,
        st_07_02_completion_receipt_sha256=value.st_07_02_completion_receipt_sha256,
        source_kind=source_kind,
        source_provenance_ref=value.source.evidence_ref,
        semantic_lineage=lineage,
        structural_lineage_manifest_hash=OD_STRUCTURAL_LINEAGE_MANIFEST_HASH,
        structural_lineage_classification=STRUCTURAL_LINEAGE_CLASSIFICATION,
        interview_provenance_classification=(
            INTERVIEW_PLACEHOLDER_CLASSIFICATION
            if source_kind == "interview_expression"
            else INTERVIEW_NOT_APPLICABLE
        ),
        wrong_reading_locks=locks,
        inherited_parent_locks=tuple(sorted(value.inherited_parent_locks, key=lambda item: item.lock_id)),
        authority_ref=value.authority_ref,
        local_contract_pin=value.local_contract_pin,
        external_contract_digest=(DELEGATION_RELEASE_DIGEST if value.target_id == DELEGATION_TARGET else None),
        external_contract_trust=(DELEGATION_TRUST if value.target_id == DELEGATION_TARGET else None),
        external_compatibility=EXTERNAL_VALIDATION_PENDING,
        request_hash=f"sha256:{sha256(canonical).hexdigest()}",
        canonical_bytes=canonical,
    )


def validate_local_contract(request: CompiledExternalHandoffRequest) -> LocalCompatibilityValidationReceipt:
    output_hash = f"sha256:{sha256((request.request_hash + ':local-fixture-validation/v1').encode()).hexdigest()}"
    core = {
        "request_identity": request.request_hash,
        "target_profile_identity": request.target_id,
        "local_contract_pin": request.local_contract_pin,
        "external_contract_digest": request.external_contract_digest,
        "external_contract_trust": request.external_contract_trust,
        "mapping_identity": "builder-local-lossless-mapping/v1",
        "structural_lineage_classification": request.structural_lineage_classification,
        "interview_provenance_classification": request.interview_provenance_classification,
        "input_hash": request.request_hash,
        "output_hash": output_hash,
        "validation_outcome": "PASS_LOCAL_CONTRACT_FIXTURE",
        "limitations": [
            "NO_EXTERNAL_ACCEPTANCE",
            "NO_RUNTIME_VALIDATION",
            "NO_CERTIFICATION",
            "STRUCTURAL_FIXTURE_NOT_PARENT_MEANING_OR_REAL_PROFILE_EVIDENCE",
            (
                "INTERVIEW_PROVENANCE_NON_PERSONAL_PLACEHOLDERS_NOT_HUMAN_TRUTH"
                if request.interview_provenance_classification == INTERVIEW_PLACEHOLDER_CLASSIFICATION
                else "INTERVIEW_PROVENANCE_NOT_APPLICABLE"
            ),
        ],
        "authority": LOCAL_VALIDATION_ONLY,
        "external_compatibility": EXTERNAL_VALIDATION_PENDING,
    }
    return LocalCompatibilityValidationReceipt(
        receipt_id=f"ST-07.03:LocalValidation:{sha256(_canonical_json(core)).hexdigest()}",
        request_identity=request.request_hash,
        target_profile_identity=request.target_id,
        local_contract_pin=request.local_contract_pin,
        external_contract_digest=request.external_contract_digest,
        external_contract_trust=request.external_contract_trust,
        mapping_identity="builder-local-lossless-mapping/v1",
        structural_lineage_classification=request.structural_lineage_classification,
        interview_provenance_classification=request.interview_provenance_classification,
        input_hash=request.request_hash,
        output_hash=output_hash,
        validation_outcome="PASS_LOCAL_CONTRACT_FIXTURE",
        limitations=(
            "NO_EXTERNAL_ACCEPTANCE",
            "NO_RUNTIME_VALIDATION",
            "NO_CERTIFICATION",
            "STRUCTURAL_FIXTURE_NOT_PARENT_MEANING_OR_REAL_PROFILE_EVIDENCE",
            (
                "INTERVIEW_PROVENANCE_NON_PERSONAL_PLACEHOLDERS_NOT_HUMAN_TRUTH"
                if request.interview_provenance_classification == INTERVIEW_PLACEHOLDER_CLASSIFICATION
                else "INTERVIEW_PROVENANCE_NOT_APPLICABLE"
            ),
        ),
    )


def _validate_lineage(refs: Sequence[GovernedRef], source_kind: str) -> tuple[GovernedRef, ...]:
    if not refs:
        raise HandoffContractRejected("Structured semantic lineage cannot be empty or flattened into notes.")
    for ref in refs:
        ref.validate()
        if ref.lineage_role in {"notes", "generic_notes"}:
            raise HandoffContractRejected("Required semantic lineage cannot be flattened into notes.")
    keys = [(ref.lineage_role, ref.object_id, ref.version, ref.sha256) for ref in refs]
    if len(keys) != len(set(keys)):
        raise HandoffContractRejected("Duplicate semantic lineage is prohibited.")
    roles = {ref.lineage_role for ref in refs}
    unsupported = roles - (_REQUIRED_LINEAGE | {"reaction_receipt", "expression_moment"})
    if unsupported:
        raise HandoffContractRejected(
            f"Unsupported structural lineage roles are prohibited: {sorted(unsupported)}"
        )
    missing = _REQUIRED_LINEAGE - roles
    if missing:
        raise HandoffContractRejected(f"Missing required structured lineage: {sorted(missing)}")
    expected_by_role = {ref.lineage_role: ref for ref in OD_STRUCTURAL_LINEAGE_FIXTURE_REFS}
    for role in _REQUIRED_LINEAGE:
        matches = tuple(ref for ref in refs if ref.lineage_role == role)
        if len(matches) != 1 or matches[0] != expected_by_role[role]:
            raise HandoffContractRejected(
                f"Lineage role {role} must use its exact OD structural fixture identity."
            )
    if source_kind == "interview_expression" and not {
        "reaction_receipt",
        "expression_moment",
    }.issubset(roles):
        raise HandoffContractRejected(
            "Interview expression requires non-empty Reaction Receipt and Expression Moment references."
        )
    placeholder_by_role = {ref.lineage_role: ref for ref in OD_INTERVIEW_PLACEHOLDER_REFS}
    for role in ("reaction_receipt", "expression_moment"):
        matches = tuple(ref for ref in refs if ref.lineage_role == role)
        if matches and (len(matches) != 1 or matches[0] != placeholder_by_role[role]):
            raise HandoffAuthorityRejected(
                "Interview provenance accepts only exact non-personal structural placeholders, never claimed human truth."
            )
    return tuple(sorted(refs, key=lambda ref: (ref.lineage_role, ref.object_id, ref.version, ref.sha256)))


def _validate_locks(
    locks: Sequence[WrongReadingLock], parent_locks: Sequence[WrongReadingLock]
) -> tuple[WrongReadingLock, ...]:
    if not locks:
        raise WrongReadingLockRejected("Semantically transformative demand requires wrong-reading locks.")
    by_id = {item.lock_id: item for item in locks}
    if len(by_id) != len(locks):
        raise WrongReadingLockRejected("Wrong-reading lock identities must be unique.")
    for parent in parent_locks:
        derivative = by_id.get(parent.lock_id)
        if derivative is None:
            raise WrongReadingLockRejected("A derivative cannot remove an inherited wrong-reading lock.")
        if derivative.meaning_hash != parent.meaning_hash:
            raise WrongReadingLockRejected("A derivative cannot weaken inherited lock meaning.")
        if not set(parent.scope_paths).issubset(derivative.scope_paths):
            raise WrongReadingLockRejected("A derivative cannot narrow inherited lock scope.")
        if derivative.enforcement_level < parent.enforcement_level:
            raise WrongReadingLockRejected("A derivative cannot weaken inherited enforcement.")
    return tuple(sorted(locks, key=lambda item: item.lock_id))


def _request_content(value: CompiledExternalHandoffRequest) -> dict[str, object]:
    if value.target_id not in EXTERNAL_TARGETS or value.external_compatibility != EXTERNAL_VALIDATION_PENDING:
        raise HandoffContractRejected("Handoff target or compatibility state is not governed.")
    if value.production_ready or value.certified:
        raise HandoffContractRejected("Local handoff cannot claim readiness or certification.")
    return {
        "schema_version": "cmf-builder-local-external-handoff/v1",
        "request_id": value.request_id,
        "request_version": value.request_version,
        "target_id": value.target_id,
        "run_ref": value.run_ref.canonical_dict(),
        "atomic_harness_definition_ref": value.atomic_harness_definition_ref.canonical_dict(),
        "atomic_harness_definition_receipt_ref": value.atomic_harness_definition_receipt_ref.canonical_dict(),
        "st_07_02_completion_receipt_sha256": value.st_07_02_completion_receipt_sha256,
        "source_kind": value.source_kind,
        "source_provenance_ref": value.source_provenance_ref.canonical_dict(),
        "semantic_lineage": [ref.canonical_dict() for ref in value.semantic_lineage],
        "structural_lineage_manifest_hash": value.structural_lineage_manifest_hash,
        "structural_lineage_classification": value.structural_lineage_classification,
        "interview_provenance_classification": value.interview_provenance_classification,
        "wrong_reading_locks": [item.canonical_dict() for item in value.wrong_reading_locks],
        "inherited_parent_locks": [item.canonical_dict() for item in value.inherited_parent_locks],
        "authority_ref": value.authority_ref.canonical_dict(),
        "local_contract_pin": value.local_contract_pin,
        "external_contract_digest_or_NOT_APPLICABLE": (
            "NOT_APPLICABLE" if value.external_contract_digest is None else value.external_contract_digest
        ),
        "external_contract_trust_or_NOT_APPLICABLE": (
            "NOT_APPLICABLE" if value.external_contract_trust is None else value.external_contract_trust
        ),
        "external_compatibility": value.external_compatibility,
        "production_ready": value.production_ready,
        "certified": value.certified,
    }


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise HandoffContractRejected(f"{field} must be a canonical non-empty string.")
    return value


def _digest(value: object, field: str) -> str:
    text = _text(value, field)
    if not text.startswith("sha256:") or _SHA256.fullmatch(text.split(":", 1)[1]) is None:
        raise HandoffContractRejected(f"{field} must be an exact SHA-256 identity.")
    return text


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
