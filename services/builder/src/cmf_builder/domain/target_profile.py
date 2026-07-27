from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Iterable, Mapping


AUTHORIZED_TARGET_ID = "atomic_content_harness"
AUTHORIZED_CATEGORY_ID = "2d_character_animation"
AUTHORIZED_PROFILE_ID = "format02_minimal_coach_theatre"
AUTHORIZED_CANONICAL_PATH = "2d_character_animation/format02_minimal_coach_theatre"
GOVERNED_TARGET_IDS = frozenset(
    {
        AUTHORIZED_TARGET_ID,
        "visual_asset_editor",
        "content_asset_delegation_contract",
    }
)


class TargetProfileError(Exception):
    code = "TargetProfileError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class TargetSelectionRejected(TargetProfileError):
    code = "TargetSelectionRejected"


class UnsupportedTargetForAuthorizedSlice(TargetProfileError):
    code = "UnsupportedTargetForAuthorizedSlice"


class RegistryIntegrityError(TargetProfileError):
    code = "RegistryIntegrityError"


class UndeclaredSkillUseRejected(TargetProfileError):
    code = "UndeclaredSkillUseRejected"


class ImmutableProfileVersionRequired(TargetProfileError):
    code = "ImmutableProfileVersionRequired"


@dataclass(frozen=True, slots=True)
class SupplementalProofMetadata:
    proof_kind: str
    profile_source_hash: str
    synthetic: bool
    repository_owned: bool
    non_production: bool
    non_certified: bool
    builder_core_validation_only: bool
    category_binding_mode: str
    canonical_category_registry_membership: bool
    skill_registry_id: str
    skill_registry_version: str
    skill_registry_hash: str
    declared_skill_ids: tuple[str, ...]
    external_skills_required: bool
    dynamic_skill_discovery_allowed: bool
    later_external_skill_effect: str
    prohibited_integrations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.proof_kind != "synthetic_builder_core_proof":
            raise UnsupportedTargetForAuthorizedSlice(
                "Only the governed synthetic Builder Core proof kind is supported.",
                proof_kind=self.proof_kind,
            )
        if not _is_sha256_hex(self.profile_source_hash) or not _is_sha256_hex(
            self.skill_registry_hash
        ):
            raise RegistryIntegrityError(
                "Synthetic proof source hashes must be raw SHA-256 values.",
                profile_source_hash=self.profile_source_hash,
                skill_registry_hash=self.skill_registry_hash,
            )
        if not all(
            (
                self.synthetic,
                self.repository_owned,
                self.non_production,
                self.non_certified,
                self.builder_core_validation_only,
            )
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "Synthetic proof classification cannot be weakened."
            )
        if (
            self.category_binding_mode != "none"
            or self.canonical_category_registry_membership
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "The Builder Core proof must remain category-neutral.",
                category_binding_mode=self.category_binding_mode,
                canonical_category_registry_membership=(
                    self.canonical_category_registry_membership
                ),
            )
        if (
            self.external_skills_required
            or self.dynamic_skill_discovery_allowed
            or self.declared_skill_ids
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "The governed synthetic proof requires an explicit empty skill registry.",
                declared_skill_ids=self.declared_skill_ids,
                external_skills_required=self.external_skills_required,
                dynamic_skill_discovery_allowed=self.dynamic_skill_discovery_allowed,
            )
        if (
            self.later_external_skill_effect
            != "NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED"
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "A later external skill must require a new immutable Harness version."
            )
        if not self.skill_registry_id.strip() or not self.skill_registry_version.strip():
            raise RegistryIntegrityError("Skill registry identity and version are required.")
        required_prohibitions = {
            "Format02",
            "VAE",
            "Delegation_runtime",
            "Conversational_Activation",
            "Interview_Expression",
            "ReelCast",
            "GPU_or_ComfyUI",
            "VLM_evaluator",
            "external_provider",
            "production_publication",
        }
        missing = sorted(required_prohibitions - set(self.prohibited_integrations))
        if missing:
            raise UnsupportedTargetForAuthorizedSlice(
                "Synthetic proof integration prohibitions are incomplete.",
                missing_prohibitions=tuple(missing),
            )

    def require_skill(
        self, skill_id: str, *, dynamically_discovered: bool = False
    ) -> None:
        if dynamically_discovered or skill_id not in self.declared_skill_ids:
            raise UndeclaredSkillUseRejected(
                "Undeclared or dynamically discovered skill use is prohibited.",
                skill_id=skill_id,
                dynamically_discovered=dynamically_discovered,
                registry_id=self.skill_registry_id,
                registry_version=self.skill_registry_version,
            )

    def to_payload(self) -> dict[str, object]:
        return {
            "proof_kind": self.proof_kind,
            "profile_source_hash": self.profile_source_hash,
            "synthetic": self.synthetic,
            "repository_owned": self.repository_owned,
            "non_production": self.non_production,
            "non_certified": self.non_certified,
            "builder_core_validation_only": self.builder_core_validation_only,
            "category_binding_mode": self.category_binding_mode,
            "canonical_category_registry_membership": (
                self.canonical_category_registry_membership
            ),
            "skill_registry_id": self.skill_registry_id,
            "skill_registry_version": self.skill_registry_version,
            "skill_registry_hash": self.skill_registry_hash,
            "declared_skill_ids": self.declared_skill_ids,
            "external_skills_required": self.external_skills_required,
            "dynamic_skill_discovery_allowed": self.dynamic_skill_discovery_allowed,
            "later_external_skill_effect": self.later_external_skill_effect,
            "prohibited_integrations": self.prohibited_integrations,
        }

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "SupplementalProofMetadata":
        return cls(
            proof_kind=str(payload["proof_kind"]),
            profile_source_hash=str(payload["profile_source_hash"]),
            synthetic=_as_bool(payload["synthetic"]),
            repository_owned=_as_bool(payload["repository_owned"]),
            non_production=_as_bool(payload["non_production"]),
            non_certified=_as_bool(payload["non_certified"]),
            builder_core_validation_only=_as_bool(
                payload["builder_core_validation_only"]
            ),
            category_binding_mode=str(payload["category_binding_mode"]),
            canonical_category_registry_membership=_as_bool(
                payload["canonical_category_registry_membership"]
            ),
            skill_registry_id=str(payload["skill_registry_id"]),
            skill_registry_version=str(payload["skill_registry_version"]),
            skill_registry_hash=str(payload["skill_registry_hash"]),
            declared_skill_ids=tuple(
                str(value) for value in _as_tuple(payload["declared_skill_ids"])
            ),
            external_skills_required=_as_bool(payload["external_skills_required"]),
            dynamic_skill_discovery_allowed=_as_bool(
                payload["dynamic_skill_discovery_allowed"]
            ),
            later_external_skill_effect=str(payload["later_external_skill_effect"]),
            prohibited_integrations=tuple(
                str(value) for value in _as_tuple(payload["prohibited_integrations"])
            ),
        )


@dataclass(frozen=True, slots=True)
class TargetProfile:
    target_id: str
    category_id: str
    profile_id: str
    canonical_path: str
    version: str
    compiler_id: str
    compatibility_state: str
    production_certified: bool
    required_work: tuple[str, ...]
    lifecycle_edges: tuple[tuple[str, str], ...]
    transition_prerequisites: tuple[tuple[str, tuple[str, ...]], ...]
    supplemental_proof: SupplementalProofMetadata | None = None

    def __post_init__(self) -> None:
        if self.target_id not in GOVERNED_TARGET_IDS:
            raise TargetSelectionRejected(
                "Target identity is not governed.", target_id=self.target_id
            )
        if self.production_certified:
            raise UnsupportedTargetForAuthorizedSlice(
                "The bounded run-governance slice cannot claim production certification.",
                profile_id=self.profile_id,
            )
        if not self.required_work:
            raise TargetSelectionRejected(
                "A target profile must expose required work.", profile_id=self.profile_id
            )
        if self.supplemental_proof is not None:
            if (
                self.target_id != AUTHORIZED_TARGET_ID
                or self.category_id != "none_test_only"
                or self.profile_id != "synthetic_text_normalization_v1"
                or self.compatibility_state != "builder_core_validation_only"
            ):
                raise UnsupportedTargetForAuthorizedSlice(
                    "Synthetic proof identity does not match the authorized capsule.",
                    target_id=self.target_id,
                    category_id=self.category_id,
                    profile_id=self.profile_id,
                    compatibility_state=self.compatibility_state,
                )

    @property
    def profile_hash(self) -> str:
        payload = json.dumps(
            self.to_payload(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return f"sha256:{sha256(payload).hexdigest()}"

    def allows_transition(self, current: str, target: str) -> bool:
        return (current, target) in self.lifecycle_edges

    def required_prerequisites(self, target: str) -> frozenset[str]:
        for state, requirements in self.transition_prerequisites:
            if state == target:
                return frozenset(requirements)
        return frozenset()

    def require_skill(
        self, skill_id: str, *, dynamically_discovered: bool = False
    ) -> None:
        if self.supplemental_proof is None:
            raise UndeclaredSkillUseRejected(
                "This target profile has no declared synthetic proof skill registry.",
                skill_id=skill_id,
                profile_id=self.profile_id,
            )
        self.supplemental_proof.require_skill(
            skill_id, dynamically_discovered=dynamically_discovered
        )

    def validate_skill_change(
        self,
        *,
        candidate_profile_version: str,
        candidate_skill_ids: tuple[str, ...],
    ) -> None:
        if self.supplemental_proof is None:
            raise UnsupportedTargetForAuthorizedSlice(
                "Synthetic proof skill-change validation requires proof metadata."
            )
        if (
            tuple(candidate_skill_ids) != self.supplemental_proof.declared_skill_ids
            and candidate_profile_version == self.version
        ):
            raise ImmutableProfileVersionRequired(
                "Adding a skill requires a new immutable Harness or profile version.",
                current_profile_version=self.version,
                candidate_profile_version=candidate_profile_version,
                candidate_skill_ids=tuple(candidate_skill_ids),
            )

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "target_id": self.target_id,
            "category_id": self.category_id,
            "profile_id": self.profile_id,
            "canonical_path": self.canonical_path,
            "profile_version": self.version,
            "compiler_id": self.compiler_id,
            "compatibility_state": self.compatibility_state,
            "production_certified": self.production_certified,
            "required_work": self.required_work,
            "lifecycle_edges": tuple(f"{source}>{target}" for source, target in self.lifecycle_edges),
            "transition_prerequisites": tuple(
                f"{state}:{','.join(requirements)}"
                for state, requirements in self.transition_prerequisites
            ),
        }
        if self.supplemental_proof is not None:
            payload.update(self.supplemental_proof.to_payload())
        return payload

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "TargetProfile":
        edges = tuple(
            tuple(str(edge).split(">", 1))
            for edge in _as_tuple(payload["lifecycle_edges"])
        )
        prerequisites: list[tuple[str, tuple[str, ...]]] = []
        for item in _as_tuple(payload["transition_prerequisites"]):
            state, separator, values = str(item).partition(":")
            requirements = tuple(value for value in values.split(",") if value) if separator else ()
            prerequisites.append((state, requirements))
        supplemental_proof = (
            SupplementalProofMetadata.from_payload(payload)
            if "proof_kind" in payload
            else None
        )
        return cls(
            target_id=str(payload["target_id"]),
            category_id=str(payload["category_id"]),
            profile_id=str(payload["profile_id"]),
            canonical_path=str(payload["canonical_path"]),
            version=str(payload["profile_version"]),
            compiler_id=str(payload["compiler_id"]),
            compatibility_state=str(payload["compatibility_state"]),
            production_certified=bool(payload["production_certified"]),
            required_work=tuple(str(value) for value in _as_tuple(payload["required_work"])),
            lifecycle_edges=tuple((str(source), str(target)) for source, target in edges),
            transition_prerequisites=tuple(prerequisites),
            supplemental_proof=supplemental_proof,
        )


def validate_single_target(target_ids: Iterable[str]) -> str:
    selected = tuple(target_ids)
    if len(selected) != 1:
        raise TargetSelectionRejected(
            "Exactly one compilation target is required.",
            target_count=len(selected),
            target_ids=selected,
        )
    target_id = selected[0]
    if target_id not in GOVERNED_TARGET_IDS:
        raise TargetSelectionRejected(
            "The selected target is not in the governed target registry.",
            target_id=target_id,
        )
    return target_id


def _as_tuple(value: object) -> tuple[object, ...]:
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    raise TargetSelectionRejected("Expected an immutable sequence in target-profile payload.")


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    raise TargetSelectionRejected("Expected a boolean in target-profile payload.")


def _is_sha256_hex(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))
