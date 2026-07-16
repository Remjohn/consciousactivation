from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping

from cmf_builder.domain.atomicity import (
    AtomicityRatification,
    BoundaryStatus,
    DeclaredAtomicBoundary,
    DraftHarnessField,
    DraftHarnessModel,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.run import LifecycleState, Run


HARNESS_IR_SCHEMA_ID = "cmf-builder-harness-ir/v1"
HARNESS_IR_SCHEMA_VERSION = "1.0.0"
CONSTITUTION_REF = "activative-intelligence-constitution@1.1.0"
REQUIRED_SECTIONS = (
    "identity",
    "evidence",
    "syntax",
    "activative_semantics",
    "phases",
    "contexts",
    "contracts",
    "modules",
    "skills",
    "references",
    "evaluators",
    "repairs",
    "budgets",
    "implementation_units",
    "authorization",
)
ACTIVATIVE_LINEAGE_PATHS = (
    "activative_semantics.identity_dna_ref",
    "activative_semantics.context_premise_ref",
    "activative_semantics.resonance_ref",
    "activative_semantics.matrix_of_edging_ref",
    "activative_semantics.activative_intelligence_pack_ref",
)
FORBIDDEN_HARNESS_IR_FIELDS = frozenset(
    {"worker", "queue", "retry", "sandbox", "deployment", "workflow_ir"}
)


class HarnessIRError(Exception):
    code = "HarnessIRError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class GovernedValueInvalid(HarnessIRError):
    code = "GovernedValueInvalid"


class HarnessIRSchemaUnsupported(HarnessIRError):
    code = "HarnessIRSchemaUnsupported"


class AggregateBoundaryViolation(HarnessIRError):
    code = "AggregateBoundaryViolation"


class HarnessIRImmutable(HarnessIRError):
    code = "HarnessIRImmutable"


class HarnessIRAuthorityRejected(HarnessIRError):
    code = "HarnessIRAuthorityRejected"


class HarnessIRInvalidatedError(HarnessIRError):
    code = "HarnessIRInvalidated"


class HarnessIRStatus(str, Enum):
    DRAFT_PROVENANCE_COMPLETE = "DRAFT_PROVENANCE_COMPLETE"


@dataclass(frozen=True, slots=True)
class GovernedValue:
    path: str
    value: object
    knowledge_status: str
    authority_status: str
    evidence_refs: tuple[str, ...]
    decision_ref: str | None
    confidence: float | None
    disposition: str
    created_by: str
    value_version: str
    dependency_impact: tuple[str, ...]

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        required = (
            self.path,
            self.knowledge_status,
            self.authority_status,
            self.disposition,
            self.created_by,
            self.value_version,
        )
        if not all(value.strip() for value in required):
            raise GovernedValueInvalid("Governed value metadata is incomplete.", path=self.path)
        if "." not in self.path or not self.evidence_refs or not self.dependency_impact:
            raise GovernedValueInvalid(
                "Every material value requires a section path, provenance, and dependency impact.",
                path=self.path,
            )
        if any(not value.strip() for value in (*self.evidence_refs, *self.dependency_impact)):
            raise GovernedValueInvalid("Governed references cannot be empty.", path=self.path)
        if self.decision_ref is not None and not self.decision_ref.strip():
            raise GovernedValueInvalid("Decision references cannot be blank.", path=self.path)
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise GovernedValueInvalid("Confidence must be between zero and one.", path=self.path)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "value": _json_value(self.value),
            "knowledge_status": self.knowledge_status,
            "authority_status": self.authority_status,
            "evidence_refs": self.evidence_refs,
            "decision_ref": self.decision_ref,
            "confidence": self.confidence,
            "disposition": self.disposition,
            "created_by": self.created_by,
            "value_version": self.value_version,
            "dependency_impact": self.dependency_impact,
        }


@dataclass(frozen=True, slots=True)
class HarnessIRDeprecation:
    path: str
    replacement_guidance: str
    affected_consumers: tuple[str, ...]
    removal_gates: tuple[str, ...]
    regression_evidence: tuple[str, ...]

    def validate(self) -> None:
        if not self.path.strip() or not self.replacement_guidance.strip():
            raise HarnessIRSchemaUnsupported("Deprecation guidance is incomplete.")
        if not self.affected_consumers or not self.removal_gates or not self.regression_evidence:
            raise HarnessIRSchemaUnsupported("Deprecation requires consumers, gates, and regression evidence.")


@dataclass(frozen=True, slots=True)
class HarnessIRCompatibilityPolicy:
    schema_id: str = HARNESS_IR_SCHEMA_ID
    write_version: str = HARNESS_IR_SCHEMA_VERSION
    readable_versions: tuple[str, ...] = (HARNESS_IR_SCHEMA_VERSION,)
    migrations: tuple[str, ...] = ()
    deprecations: tuple[HarnessIRDeprecation, ...] = ()
    unsupported_version_behavior: str = "BLOCK_MISSING_EXPLICIT_MIGRATION"

    def validate(self) -> None:
        if self.schema_id != HARNESS_IR_SCHEMA_ID:
            raise HarnessIRSchemaUnsupported("Harness IR schema identity is unsupported.", schema_id=self.schema_id)
        if self.write_version != HARNESS_IR_SCHEMA_VERSION:
            raise HarnessIRSchemaUnsupported("Harness IR write version is unsupported.", version=self.write_version)
        if self.readable_versions != (HARNESS_IR_SCHEMA_VERSION,):
            raise HarnessIRSchemaUnsupported("Only the initial readable version is authorized.", readable_versions=self.readable_versions)
        if self.migrations:
            raise HarnessIRSchemaUnsupported("No prior-version migration is authorized in the initial registry.")
        if self.unsupported_version_behavior != "BLOCK_MISSING_EXPLICIT_MIGRATION":
            raise HarnessIRSchemaUnsupported("Unsupported versions must fail closed.")
        for item in self.deprecations:
            item.validate()

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "write_version": self.write_version,
            "readable_versions": self.readable_versions,
            "migrations": self.migrations,
            "deprecations": [
                {
                    "path": item.path,
                    "replacement_guidance": item.replacement_guidance,
                    "affected_consumers": item.affected_consumers,
                    "removal_gates": item.removal_gates,
                    "regression_evidence": item.regression_evidence,
                }
                for item in self.deprecations
            ],
            "unsupported_version_behavior": self.unsupported_version_behavior,
        }


@dataclass(frozen=True, slots=True)
class HarnessIRSection:
    name: str
    values: tuple[GovernedValue, ...]

    def __post_init__(self) -> None:
        if self.name not in REQUIRED_SECTIONS or not self.values:
            raise GovernedValueInvalid("Harness IR section is unknown or empty.", section=self.name)
        if tuple(sorted(self.values, key=lambda item: item.path)) != self.values:
            raise GovernedValueInvalid("Harness IR values must use canonical path order.", section=self.name)
        for item in self.values:
            if not item.path.startswith(f"{self.name}."):
                raise GovernedValueInvalid("Value path does not belong to its section.", path=item.path, section=self.name)

    def canonical_dict(self) -> dict[str, object]:
        return {"name": self.name, "values": [item.canonical_dict() for item in self.values]}


@dataclass(frozen=True, slots=True)
class HarnessIR:
    ir_id: str
    ir_hash: str
    schema_id: str
    schema_version: str
    revision: int
    run_id: str
    target_profile_ref: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    constitution_ref: str
    category_binding: str
    synthetic: bool
    repository_owned: bool
    production_eligible: bool
    certified: bool
    status: HarnessIRStatus
    compatibility: HarnessIRCompatibilityPolicy
    sections: tuple[HarnessIRSection, ...]

    @property
    def upstream_refs(self) -> tuple[str, ...]:
        return (self.source_lock_ref, self.boundary_ref, self.ratification_ref, self.model_ref)

    @property
    def material_values(self) -> tuple[GovernedValue, ...]:
        return tuple(value for section in self.sections for value in section.values)

    @classmethod
    def compile(
        cls,
        *,
        run: Run,
        source_lock: SourceLock,
        boundary: DeclaredAtomicBoundary,
        ratification: AtomicityRatification,
        model: DraftHarnessModel,
        compiled_by: str,
        schema_version: str = HARNESS_IR_SCHEMA_VERSION,
    ) -> "HarnessIR":
        if schema_version != HARNESS_IR_SCHEMA_VERSION:
            raise HarnessIRSchemaUnsupported("Requested Harness IR version is unsupported.", version=schema_version)
        cls._validate_upstream(run, source_lock, boundary, ratification, model)
        values = _compile_values(
            run=run,
            source_lock=source_lock,
            boundary=boundary,
            ratification=ratification,
            model=model,
            compiled_by=compiled_by,
        )
        sections = tuple(
            HarnessIRSection(
                name=name,
                values=tuple(sorted((item for item in values if item.path.startswith(f"{name}.")), key=lambda item: item.path)),
            )
            for name in REQUIRED_SECTIONS
        )
        compatibility = HarnessIRCompatibilityPolicy()
        compatibility.validate()
        profile = run.target_profile.supplemental_proof
        assert profile is not None
        candidate = cls(
            ir_id="pending",
            ir_hash="pending",
            schema_id=HARNESS_IR_SCHEMA_ID,
            schema_version=HARNESS_IR_SCHEMA_VERSION,
            revision=1,
            run_id=run.run_id,
            target_profile_ref=f"{run.target_profile.profile_id}@{run.target_profile.version}",
            source_lock_ref=source_lock.lock_id,
            boundary_ref=boundary.boundary_id,
            ratification_ref=ratification.ratification_id,
            model_ref=model.model_id,
            constitution_ref=CONSTITUTION_REF,
            category_binding="none_test_only",
            synthetic=profile.synthetic,
            repository_owned=profile.repository_owned,
            production_eligible=False,
            certified=False,
            status=HarnessIRStatus.DRAFT_PROVENANCE_COMPLETE,
            compatibility=compatibility,
            sections=sections,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            ir_id=f"harness-ir_{digest}",
            ir_hash=f"sha256:{digest}",
        )
        result.validate()
        return result

    @staticmethod
    def _validate_upstream(
        run: Run,
        source_lock: SourceLock,
        boundary: DeclaredAtomicBoundary,
        ratification: AtomicityRatification,
        model: DraftHarnessModel,
    ) -> None:
        _validate_source_lock_integrity(source_lock)
        _validate_boundary_integrity(boundary)
        _validate_ratification_integrity(ratification)
        _validate_model_integrity(model)
        profile = run.target_profile.supplemental_proof
        if (
            run.lifecycle_state is not LifecycleState.ATOMICITY_RATIFICATION
            or profile is None
            or not profile.synthetic
            or not profile.repository_owned
            or not profile.non_production
            or not profile.non_certified
            or profile.category_binding_mode != "none"
            or run.boundary_invalidation_ref is not None
        ):
            raise HarnessIRAuthorityRejected("Run is not an active governed synthetic atomicity package.")
        expected = (
            (run.run_id, source_lock.run_id),
            (run.source_lock_ref, source_lock.lock_id),
            (run.atomic_boundary_ref, boundary.boundary_id),
            (run.atomicity_ratification_ref, ratification.ratification_id),
            (run.draft_harness_model_ref, model.model_id),
            (boundary.source_lock_ref, source_lock.lock_id),
            (ratification.source_lock_ref, source_lock.lock_id),
            (ratification.boundary_ref, boundary.boundary_id),
            (model.source_lock_ref, source_lock.lock_id),
            (model.boundary_ref, boundary.boundary_id),
        )
        if any(left != right for left, right in expected):
            raise HarnessIRAuthorityRejected("Upstream identity lineage is inconsistent.", expected=expected)
        if (
            boundary.status is not BoundaryStatus.FROZEN
            or not boundary.synthetic
            or not boundary.repository_owned
            or boundary.production_eligible
            or boundary.certified
            or not ratification.human_id.strip()
            or not ratification.evidence_refs
        ):
            raise HarnessIRAuthorityRejected("Frozen boundary or human ratification is incomplete.")
        if not model.fields or any(not item.provenance for item in model.fields):
            raise GovernedValueInvalid("Draft Harness Model contains a value without provenance.")

    def validate(self) -> None:
        self.compatibility.validate()
        if (
            self.schema_id != HARNESS_IR_SCHEMA_ID
            or self.schema_version != HARNESS_IR_SCHEMA_VERSION
            or self.revision != 1
            or tuple(section.name for section in self.sections) != REQUIRED_SECTIONS
        ):
            raise HarnessIRSchemaUnsupported("Harness IR root contract is incompatible.")
        if not all((self.synthetic, self.repository_owned)) or self.production_eligible or self.certified:
            raise HarnessIRAuthorityRejected("Synthetic proof scope was weakened.")
        self.validate_candidate_paths(item.path for item in self.material_values)
        if len({item.path for item in self.material_values}) != len(self.material_values):
            raise GovernedValueInvalid("Harness IR material paths must be unique.")
        for item in self.material_values:
            item.validate()
        digest = sha256(self.canonical_bytes()).hexdigest()
        if self.ir_hash != f"sha256:{digest}" or self.ir_id != f"harness-ir_{digest}":
            raise HarnessIRImmutable("Harness IR identity does not match canonical content.")

    @staticmethod
    def validate_candidate_paths(paths: Iterable[str]) -> None:
        for path in paths:
            tokens = {token.lower() for token in path.replace("-", "_").split(".")}
            if tokens & FORBIDDEN_HARNESS_IR_FIELDS:
                raise AggregateBoundaryViolation("Workflow IR ownership cannot enter Harness IR.", path=path)

    def section(self, name: str) -> tuple[GovernedValue, ...]:
        for section in self.sections:
            if section.name == name:
                return section.values
        raise KeyError(name)

    def value(self, path: str) -> GovernedValue:
        for item in self.material_values:
            if item.path == path:
                return item
        raise KeyError(path)

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "schema_version": self.schema_version,
                "revision": self.revision,
                "run_id": self.run_id,
                "target_profile_ref": self.target_profile_ref,
                "source_lock_ref": self.source_lock_ref,
                "boundary_ref": self.boundary_ref,
                "ratification_ref": self.ratification_ref,
                "model_ref": self.model_ref,
                "constitution_ref": self.constitution_ref,
                "category_binding": self.category_binding,
                "synthetic": self.synthetic,
                "repository_owned": self.repository_owned,
                "production_eligible": self.production_eligible,
                "certified": self.certified,
                "status": self.status.value,
                "compatibility": self.compatibility.canonical_dict(),
                "sections": [section.canonical_dict() for section in self.sections],
            }
        )

    def require_new_revision(self, *, candidate_revision: int, candidate_bytes: bytes) -> None:
        if candidate_bytes != self.canonical_bytes() and candidate_revision == self.revision:
            raise HarnessIRImmutable("A same-revision semantic rewrite is prohibited.", ir_id=self.ir_id)


@dataclass(frozen=True, slots=True)
class HarnessIRCompilationReceipt:
    receipt_id: str
    command_id: str
    run_id: str
    ir_id: str
    ir_hash: str
    schema_version: str
    revision: int
    authority_identity: str
    upstream_refs: tuple[str, ...]
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str
    receipt_hash: str

    @classmethod
    def create(
        cls,
        *,
        receipt_id: str,
        command_id: str,
        run_id: str,
        ir: HarnessIR,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "HarnessIRCompilationReceipt":
        payload = {
            "receipt_id": receipt_id,
            "command_id": command_id,
            "run_id": run_id,
            "ir_id": ir.ir_id,
            "ir_hash": ir.ir_hash,
            "schema_version": ir.schema_version,
            "revision": ir.revision,
            "authority_identity": authority_identity,
            "upstream_refs": ir.upstream_refs,
            "event_ids": event_ids,
            "stream_version": stream_version,
            "outcome": "PASS",
        }
        return cls(**payload, receipt_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}")


@dataclass(frozen=True, slots=True)
class HarnessIRInvalidation:
    invalidation_id: str
    ir_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str
    new_revision_required: bool
    invalidation_hash: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        ir_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "HarnessIRInvalidation":
        payload = {
            "invalidation_id": invalidation_id,
            "ir_ref": ir_ref,
            "upstream_invalidation_ref": upstream_invalidation_ref,
            "reason": reason,
            "authority_identity": authority_identity,
            "new_revision_required": True,
        }
        return cls(**payload, invalidation_hash=f"sha256:{sha256(_canonical_json(payload)).hexdigest()}")


def _compile_values(
    *,
    run: Run,
    source_lock: SourceLock,
    boundary: DeclaredAtomicBoundary,
    ratification: AtomicityRatification,
    model: DraftHarnessModel,
    compiled_by: str,
) -> tuple[GovernedValue, ...]:
    model_fields = {item.name: item for item in model.fields}

    def from_model(section: str, path: str, field_name: str) -> GovernedValue:
        field = model_fields[field_name]
        return _governed(
            path=f"{section}.{path}",
            value=field.value,
            knowledge=field.knowledge_status.value,
            authority=field.authority_status.value,
            evidence=(*field.provenance, model.model_id, model.model_hash),
            decision=ratification.ratification_id if field.authority_status.value == "HUMAN_RATIFIED" else None,
            disposition=field.disposition,
            created_by=compiled_by,
        )

    def explicit(path: str, value: object, *, knowledge: str, authority: str, evidence: tuple[str, ...], disposition: str, decision: str | None = None) -> GovernedValue:
        return _governed(
            path=path,
            value=value,
            knowledge=knowledge,
            authority=authority,
            evidence=evidence,
            decision=decision,
            disposition=disposition,
            created_by=compiled_by,
        )

    common = (
        source_lock.lock_id,
        source_lock.aggregate_hash,
        boundary.boundary_id,
        boundary.content_hash,
        ratification.ratification_id,
        ratification.ratification_hash,
        model.model_id,
        model.model_hash,
        CONSTITUTION_REF,
    )
    values: list[GovernedValue] = [
        from_model("identity", "atomic_boundary", "atomic_boundary"),
        from_model("identity", "category_ownership", "category_ownership"),
        from_model("identity", "identity", "identity"),
        from_model("identity", "production_promise", "production_promise"),
        explicit("evidence.source_lock_ref", source_lock.lock_id, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(source_lock.aggregate_hash,), disposition="IMMUTABLE_SOURCE_LOCK"),
        explicit("evidence.boundary_ref", boundary.boundary_id, knowledge="LOCKED_EVIDENCE", authority="HUMAN_RATIFIED", evidence=(boundary.content_hash, ratification.ratification_hash), disposition="FROZEN", decision=ratification.ratification_id),
        explicit("evidence.ratification_ref", ratification.ratification_id, knowledge="LOCKED_EVIDENCE", authority="HUMAN_RATIFIED", evidence=(ratification.ratification_hash,), disposition="ATTRIBUTABLE_HUMAN_DECISION", decision=ratification.ratification_id),
        explicit("evidence.draft_harness_model_ref", model.model_id, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(model.model_hash,), disposition="IMMUTABLE_INPUT_MODEL"),
        from_model("syntax", "visual_syntax", "visual_syntax"),
        from_model("syntax", "composition_variables", "composition_variables"),
        from_model("syntax", "sequence_grammar", "sequence_grammar"),
        from_model("activative_semantics", "draft_activative_intelligence", "draft_activative_intelligence"),
        from_model("phases", "phase_hypotheses", "phase_hypotheses"),
        from_model("phases", "runtime_hypotheses", "runtime_hypotheses"),
        from_model("contracts", "inputs", "inputs"),
        from_model("contracts", "outputs", "outputs"),
        from_model("contracts", "invariants", "invariants"),
        from_model("contracts", "legal_variation", "legal_variation"),
        from_model("skills", "capabilities", "capabilities"),
        from_model("evaluators", "evaluation_hypotheses", "evaluation_hypotheses"),
        from_model("evaluators", "category_native_evaluation", "category_native_evaluation"),
        from_model("repairs", "repair_hypotheses", "repair_hypotheses"),
        from_model("repairs", "production_repair_policy", "production_repair_policy"),
    ]
    for path in ACTIVATIVE_LINEAGE_PATHS:
        values.append(explicit(path, None, knowledge="NOT_APPLICABLE", authority="NOT_APPLICABLE", evidence=(model.model_id, model.model_hash, boundary.input_hash), disposition="NOT_APPLICABLE_FOR_CATEGORY_NEUTRAL_SYNTHETIC_PROOF"))
    proof = run.target_profile.supplemental_proof
    assert proof is not None
    values.extend(
        (
            explicit("contexts.context_hypotheses", (), knowledge="HYPOTHESIS", authority="UNRATIFIED", evidence=(model.model_id, model.model_hash), disposition="DECISION_REQUIRED"),
            explicit("modules.module_hypotheses", (), knowledge="HYPOTHESIS", authority="UNRATIFIED", evidence=(model.model_id, model.model_hash), disposition="DECISION_REQUIRED"),
            explicit("skills.skill_registry_ref", f"{proof.skill_registry_id}@{proof.skill_registry_version}", knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(proof.skill_registry_hash,), disposition="GOVERNED_EMPTY_REGISTRY"),
            explicit("skills.external_skills_required", proof.external_skills_required, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(proof.skill_registry_hash,), disposition="DECLARED_FALSE"),
            explicit("references.source_lock", source_lock.lock_id, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=common, disposition="CANONICAL_REFERENCE"),
            explicit("references.atomic_boundary", boundary.boundary_id, knowledge="LOCKED_EVIDENCE", authority="HUMAN_RATIFIED", evidence=common, disposition="CANONICAL_REFERENCE", decision=ratification.ratification_id),
            explicit("references.ratification", ratification.ratification_id, knowledge="LOCKED_EVIDENCE", authority="HUMAN_RATIFIED", evidence=common, disposition="CANONICAL_REFERENCE", decision=ratification.ratification_id),
            explicit("references.draft_harness_model", model.model_id, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=common, disposition="CANONICAL_REFERENCE"),
            explicit("references.constitution", CONSTITUTION_REF, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(CONSTITUTION_REF,), disposition="GOVERNING_AUTHORITY"),
            explicit("budgets.budget_hypotheses", (), knowledge="HYPOTHESIS", authority="UNRATIFIED", evidence=(model.model_id, model.model_hash), disposition="DECISION_REQUIRED"),
            explicit("implementation_units.implementation_unit_hypotheses", (), knowledge="HYPOTHESIS", authority="UNRATIFIED", evidence=(model.model_id, model.model_hash), disposition="DECISION_REQUIRED"),
            explicit("authorization.atomic_boundary_ratification", ratification.ratification_id, knowledge="LOCKED_EVIDENCE", authority="HUMAN_RATIFIED", evidence=(ratification.ratification_hash,), disposition="BOUNDARY_AUTHORITY_ONLY", decision=ratification.ratification_id),
            explicit("authorization.model_status", model.status.value, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(model.model_hash,), disposition="UNRATIFIED_FIELDS_PRESERVED"),
            explicit("authorization.production_eligible", False, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(proof.profile_source_hash,), disposition="NON_PRODUCTION"),
            explicit("authorization.certified", False, knowledge="LOCKED_EVIDENCE", authority="SOURCE_LOCKED", evidence=(proof.profile_source_hash,), disposition="NON_CERTIFIED"),
        )
    )
    return tuple(values)


def _governed(
    *,
    path: str,
    value: object,
    knowledge: str,
    authority: str,
    evidence: tuple[str, ...],
    decision: str | None,
    disposition: str,
    created_by: str,
) -> GovernedValue:
    return GovernedValue(
        path=path,
        value=_freeze(value),
        knowledge_status=knowledge,
        authority_status=authority,
        evidence_refs=tuple(dict.fromkeys(evidence)),
        decision_ref=decision,
        confidence=None,
        disposition=disposition,
        created_by=created_by,
        value_version=HARNESS_IR_SCHEMA_VERSION,
        dependency_impact=(path,),
    )


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _json_value(value: object) -> object:
    if isinstance(value, tuple):
        if all(isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) for item in value):
            return {str(key): _json_value(item) for key, item in value}
        return [_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _validate_source_lock_integrity(source_lock: SourceLock) -> None:
    identity = {
        "run_id": source_lock.run_id,
        "source_profile_ref": source_lock.source_profile_ref,
        "source_profile_hash": source_lock.source_profile_hash,
        "target_profile_ref": source_lock.target_profile_ref,
        "target_candidate_ref": source_lock.target_candidate_ref,
        "ordered_descriptors": [
            item.identity_payload() for item in source_lock.ordered_descriptors
        ],
        "invalidates_lock_ref": source_lock.invalidates_lock_ref,
    }
    digest = sha256(_canonical_json(identity)).hexdigest()
    if (
        source_lock.lock_id != f"source-lock_{digest}"
        or source_lock.aggregate_hash != f"sha256:{digest}"
    ):
        raise HarnessIRAuthorityRejected(
            "Source Lock content no longer matches its immutable identity.",
            source_lock_ref=source_lock.lock_id,
        )


def _validate_boundary_integrity(boundary: DeclaredAtomicBoundary) -> None:
    payload = {
        "boundary_id": boundary.boundary_id,
        "version": boundary.version,
        "candidate_id": boundary.candidate_id,
        "boundary": boundary.boundary,
        "production_promise": boundary.production_promise,
        "input_hash": boundary.input_hash,
        "source_lock_ref": boundary.source_lock_ref,
        "category_binding": boundary.category_binding,
        "synthetic": boundary.synthetic,
        "repository_owned": boundary.repository_owned,
        "production_eligible": boundary.production_eligible,
        "certified": boundary.certified,
        "status": boundary.status.value,
    }
    expected = f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"
    if boundary.content_hash != expected:
        raise HarnessIRAuthorityRejected(
            "Frozen boundary content no longer matches its immutable hash.",
            boundary_ref=boundary.boundary_id,
        )


def _validate_ratification_integrity(ratification: AtomicityRatification) -> None:
    payload = {
        "ratification_id": ratification.ratification_id,
        "boundary_ref": ratification.boundary_ref,
        "selected_candidate": ratification.selected_candidate,
        "rejected_alternatives": ratification.rejected_alternatives,
        "evidence_refs": ratification.evidence_refs,
        "source_lock_ref": ratification.source_lock_ref,
        "human_id": ratification.human_id,
        "rationale": ratification.rationale,
        "accepted_risks": ratification.accepted_risks,
        "signed_at": ratification.signed_at.isoformat(),
    }
    expected = f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"
    if ratification.ratification_hash != expected:
        raise HarnessIRAuthorityRejected(
            "Human ratification content no longer matches its immutable hash.",
            ratification_ref=ratification.ratification_id,
        )


def _validate_model_integrity(model: DraftHarnessModel) -> None:
    payload = {
        "model_id": model.model_id,
        "boundary_ref": model.boundary_ref,
        "source_lock_ref": model.source_lock_ref,
        "fields": [
            {
                "name": field.name,
                "value": _atomicity_json_value(field.value),
                "authority_status": field.authority_status.value,
                "knowledge_status": field.knowledge_status.value,
                "provenance": field.provenance,
                "disposition": field.disposition,
            }
            for field in model.fields
        ],
        "unresolved_gaps": model.unresolved_gaps,
        "alternatives": model.alternatives,
        "decisions_required": model.decisions_required,
        "status": model.status.value,
    }
    expected = f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"
    if model.model_hash != expected:
        raise HarnessIRAuthorityRejected(
            "Draft Harness Model content no longer matches its immutable hash.",
            model_ref=model.model_id,
        )


def _atomicity_json_value(value: object) -> object:
    if isinstance(value, tuple):
        return [_atomicity_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
