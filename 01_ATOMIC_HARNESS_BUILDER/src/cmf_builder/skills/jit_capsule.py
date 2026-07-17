from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import PurePath


class JITCapsuleError(ValueError):
    """The phase-local capsule cannot be assembled from governed inputs."""


class ContextClass(str, Enum):
    REQUIRED = "REQUIRED"
    CONDITIONAL_REQUIRED = "CONDITIONAL_REQUIRED"
    OPTIONAL = "OPTIONAL"
    FORBIDDEN = "FORBIDDEN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class ContextRequirement:
    context_id: str
    context_hash: str
    classification: ContextClass
    source_ref: str
    provenance_ref: str
    owning_responsibility: str
    consuming_phase: str
    inclusion_reason: str
    authority_ref: str
    condition_satisfied: bool = False
    not_applicable_reason: str | None = None

    def canonical_dict(self) -> dict[str, object]:
        values = (
            self.context_id,
            self.context_hash,
            self.source_ref,
            self.provenance_ref,
            self.owning_responsibility,
            self.consuming_phase,
            self.inclusion_reason,
            self.authority_ref,
        )
        if any(not value.strip() for value in values) or len(self.context_hash) != 64:
            raise JITCapsuleError("Context identity, hash, lineage, and ownership are required.")
        if self.classification is ContextClass.NOT_APPLICABLE and not (
            self.not_applicable_reason and self.not_applicable_reason.strip()
        ):
            raise JITCapsuleError("NOT_APPLICABLE context requires an explicit reason.")
        if self.classification is not ContextClass.NOT_APPLICABLE and self.not_applicable_reason:
            raise JITCapsuleError("Only NOT_APPLICABLE context may carry that justification.")
        return {
            "context_id": self.context_id,
            "context_hash": self.context_hash,
            "classification": self.classification.value,
            "source_ref": self.source_ref,
            "provenance_ref": self.provenance_ref,
            "owning_responsibility": self.owning_responsibility,
            "consuming_phase": self.consuming_phase,
            "inclusion_reason": self.inclusion_reason,
            "authority_ref": self.authority_ref,
            "condition_satisfied": self.condition_satisfied,
            "not_applicable_reason": self.not_applicable_reason,
        }


@dataclass(frozen=True, slots=True)
class PhaseLocalJITCapsule:
    capsule_id: str
    schema_version: str
    phase_id: str
    skill_id: str
    skill_version: str
    skill_package_hash: str
    minimum_context_ref: str
    minimum_context_hash: str
    selected_context: tuple[ContextRequirement, ...]
    applicability_decisions: tuple[ContextRequirement, ...]
    authority_refs: tuple[str, ...]
    input_contract_ref: str
    output_contract_ref: str
    acceptance_test_refs: tuple[str, ...]
    failure_and_stop_conditions: tuple[str, ...]
    observability_requirements: tuple[str, ...]
    rollback_requirements: tuple[str, ...]
    wrong_reading_locks: tuple[str, ...]
    semantic_lineage_refs: tuple[str, ...]
    evaluation_status: str
    production_eligible: bool
    certified: bool
    capsule_hash: str

    @classmethod
    def assemble(
        cls,
        *,
        phase_id: str,
        skill_id: str,
        skill_version: str,
        skill_package_hash: str,
        minimum_context_ref: str,
        minimum_context_hash: str,
        requirements: tuple[ContextRequirement, ...],
        supplied_context_ids: tuple[str, ...],
        authority_refs: tuple[str, ...],
        input_contract_ref: str,
        output_contract_ref: str,
        acceptance_test_refs: tuple[str, ...],
        failure_and_stop_conditions: tuple[str, ...],
        observability_requirements: tuple[str, ...],
        rollback_requirements: tuple[str, ...],
        wrong_reading_locks: tuple[str, ...],
        semantic_lineage_refs: tuple[str, ...],
        evaluation_status: str,
    ) -> "PhaseLocalJITCapsule":
        scalar_values = (
            phase_id,
            skill_id,
            skill_version,
            skill_package_hash,
            minimum_context_ref,
            minimum_context_hash,
            input_contract_ref,
            output_contract_ref,
        )
        if any(not value.strip() for value in scalar_values):
            raise JITCapsuleError("Capsule pins and phase contracts are required.")
        if len(skill_package_hash) != 64 or len(minimum_context_hash) != 64:
            raise JITCapsuleError("Skill and context hashes must be exact SHA-256 pins.")
        if evaluation_status != "development_validated":
            raise JITCapsuleError("Only development-validated skill evidence can enter this capsule.")
        collections = (
            authority_refs,
            acceptance_test_refs,
            failure_and_stop_conditions,
            observability_requirements,
            rollback_requirements,
            wrong_reading_locks,
            semantic_lineage_refs,
        )
        if any(not values or any(not value.strip() for value in values) for values in collections):
            raise JITCapsuleError("Authority, tests, failure, observation, rollback, locks, and lineage are required.")
        if len(set(supplied_context_ids)) != len(supplied_context_ids):
            raise JITCapsuleError("Duplicate supplied context identity is forbidden.")
        indexed: dict[str, ContextRequirement] = {}
        for requirement in requirements:
            requirement.canonical_dict()
            if requirement.context_id in indexed:
                raise JITCapsuleError("Conflicting context requirements are forbidden.")
            indexed[requirement.context_id] = requirement
        required_ids = {
            item.context_id
            for item in requirements
            if item.classification is ContextClass.REQUIRED
            or (
                item.classification is ContextClass.CONDITIONAL_REQUIRED
                and item.condition_satisfied
            )
        }
        supplied_ids = set(supplied_context_ids)
        missing = required_ids - supplied_ids
        if missing:
            raise JITCapsuleError(f"Mandatory phase context is missing: {sorted(missing)}")
        unknown = supplied_ids - set(indexed)
        if unknown:
            raise JITCapsuleError(f"Unjustified phase context is forbidden: {sorted(unknown)}")
        forbidden = {
            item.context_id
            for item in requirements
            if item.classification in {ContextClass.FORBIDDEN, ContextClass.NOT_APPLICABLE}
            or (
                item.classification is ContextClass.CONDITIONAL_REQUIRED
                and not item.condition_satisfied
            )
        } & supplied_ids
        if forbidden:
            raise JITCapsuleError(f"Forbidden or inapplicable context was supplied: {sorted(forbidden)}")
        optional = {
            item.context_id
            for item in requirements
            if item.classification is ContextClass.OPTIONAL
        } & supplied_ids
        if optional:
            raise JITCapsuleError(
                f"Optional context is excluded from the minimum phase capsule: {sorted(optional)}"
            )
        selected = tuple(sorted((indexed[item] for item in supplied_ids), key=lambda item: item.context_id))
        decisions = tuple(sorted(requirements, key=lambda item: item.context_id))
        payload = {
            "schema": "cmf-builder-phase-local-jit-capsule/v1",
            "phase_id": phase_id,
            "skill": {"id": skill_id, "version": skill_version, "package_hash": skill_package_hash},
            "minimum_context": {"ref": minimum_context_ref, "hash": minimum_context_hash},
            "selected_context": [item.canonical_dict() for item in selected],
            "applicability_decisions": [item.canonical_dict() for item in decisions],
            "authority_refs": sorted(set(authority_refs)),
            "input_contract_ref": input_contract_ref,
            "output_contract_ref": output_contract_ref,
            "acceptance_test_refs": sorted(set(acceptance_test_refs)),
            "failure_and_stop_conditions": sorted(set(failure_and_stop_conditions)),
            "observability_requirements": sorted(set(observability_requirements)),
            "rollback_requirements": sorted(set(rollback_requirements)),
            "wrong_reading_locks": sorted(set(wrong_reading_locks)),
            "semantic_lineage_refs": sorted(set(semantic_lineage_refs)),
            "evaluation_status": evaluation_status,
            "production_eligible": False,
            "certified": False,
        }
        _reject_machine_paths(payload)
        digest = sha256(_canonical_bytes(payload)).hexdigest()
        return cls(
            capsule_id=f"jit:{skill_id}:{phase_id}:{digest[:24]}",
            schema_version="1.0.0",
            phase_id=phase_id,
            skill_id=skill_id,
            skill_version=skill_version,
            skill_package_hash=skill_package_hash,
            minimum_context_ref=minimum_context_ref,
            minimum_context_hash=minimum_context_hash,
            selected_context=selected,
            applicability_decisions=decisions,
            authority_refs=tuple(payload["authority_refs"]),
            input_contract_ref=input_contract_ref,
            output_contract_ref=output_contract_ref,
            acceptance_test_refs=tuple(payload["acceptance_test_refs"]),
            failure_and_stop_conditions=tuple(payload["failure_and_stop_conditions"]),
            observability_requirements=tuple(payload["observability_requirements"]),
            rollback_requirements=tuple(payload["rollback_requirements"]),
            wrong_reading_locks=tuple(payload["wrong_reading_locks"]),
            semantic_lineage_refs=tuple(payload["semantic_lineage_refs"]),
            evaluation_status=evaluation_status,
            production_eligible=False,
            certified=False,
            capsule_hash=digest,
        )

    def canonical_dict(self) -> dict[str, object]:
        payload = {
            "schema": "cmf-builder-phase-local-jit-capsule/v1",
            "phase_id": self.phase_id,
            "skill": {"id": self.skill_id, "version": self.skill_version, "package_hash": self.skill_package_hash},
            "minimum_context": {"ref": self.minimum_context_ref, "hash": self.minimum_context_hash},
            "selected_context": [item.canonical_dict() for item in self.selected_context],
            "applicability_decisions": [item.canonical_dict() for item in self.applicability_decisions],
            "authority_refs": list(self.authority_refs),
            "input_contract_ref": self.input_contract_ref,
            "output_contract_ref": self.output_contract_ref,
            "acceptance_test_refs": list(self.acceptance_test_refs),
            "failure_and_stop_conditions": list(self.failure_and_stop_conditions),
            "observability_requirements": list(self.observability_requirements),
            "rollback_requirements": list(self.rollback_requirements),
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "semantic_lineage_refs": list(self.semantic_lineage_refs),
            "evaluation_status": self.evaluation_status,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
        }
        if sha256(_canonical_bytes(payload)).hexdigest() != self.capsule_hash:
            raise JITCapsuleError("The JIT capsule hash has drifted.")
        return {**payload, "capsule_id": self.capsule_id, "capsule_hash": self.capsule_hash}


def _canonical_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _reject_machine_paths(payload: object) -> None:
    text = json.dumps(payload, sort_keys=True)
    for token in text.replace("\\\\", "/").split('"'):
        if token.startswith(("C:/", "D:/", "/home/", "/Users/")) or PurePath(token).is_absolute():
            raise JITCapsuleError("Portable capsule content cannot contain an absolute path.")
