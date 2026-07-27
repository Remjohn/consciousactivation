"""Builder adapter implementations for the bounded Story slices."""

from __future__ import annotations

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)

__all__ = ["SQLiteProductizationRepository"]

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from cmf_builder.domain.target_profile import (
    AUTHORIZED_TARGET_ID,
    GOVERNED_TARGET_IDS,
    ImmutableProfileVersionRequired,
    RegistryIntegrityError,
    SupplementalProofMetadata,
    TargetProfile,
    UndeclaredSkillUseRejected,
    UnsupportedTargetForAuthorizedSlice,
    validate_single_target,
)


SYNTHETIC_PROFILE_ID = "synthetic_text_normalization_v1"
SYNTHETIC_CATEGORY_ID = "none_test_only"
SYNTHETIC_PROFILE_VERSION = "1.0.0"
SYNTHETIC_PROFILE_FIXTURE = Path(
    "development-capsules/ST-01.01-SYNTHETIC-PROOF/"
    "SYNTHETIC_TARGET_PROFILE_FIXTURE.yaml"
)
SYNTHETIC_PROFILE_FIXTURE_SHA256 = (
    "82f86a94e1183ee3d475277734b03eb5f2ab3d2bb7afe0520b8828105917337b"
)
EMPTY_SKILL_REGISTRY = Path(
    "governance/fixtures/synthetic-core/empty-skill-registry.yaml"
)
EMPTY_SKILL_REGISTRY_SHA256 = (
    "a4a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114"
)
EMPTY_SKILL_REGISTRY_SCHEMA = Path(
    "governance/schemas/empty-skill-registry.schema.json"
)
EMPTY_SKILL_REGISTRY_SCHEMA_SHA256 = (
    "e76be265d96df3c902a26989fa2c08309f6964bf96e4ac17ce850684de44f1c7"
)
EMPTY_SKILL_REGISTRY_POLICY = Path("governance/EMPTY_SKILL_REGISTRY_POLICY.yaml")
EMPTY_SKILL_REGISTRY_POLICY_SHA256 = (
    "260df1cb40655fe4f42d264bb73f3e6bda012b9fe6bd015a1b6ae153615f985c"
)

SYNTHETIC_REQUIRED_WORK = (
    "lock_governed_synthetic_task_definition",
    "validate_declared_atomic_boundary",
    "compile_canonical_harness_ir",
    "compile_atomic_harness_definition",
    "validate_atomic_harness_definition",
    "compile_development_capsule",
)
SYNTHETIC_PROHIBITED_INTEGRATIONS = (
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
)
EMPTY_REGISTRY_CAPABILITIES = (
    "governed_task_acceptance",
    "synthetic_target_profile_binding",
    "governed_run_lifecycle",
    "deterministic_contract_validation",
    "immutable_receipt_emission",
)


@dataclass(frozen=True, slots=True)
class GovernedEmptySkillRegistry:
    registry_id: str
    version: str
    source_hash: str
    capabilities: tuple[str, ...]
    skills: tuple[str, ...]
    external_skills_required: bool
    dynamic_skill_discovery_allowed: bool
    undeclared_skill_use: str
    later_external_skill_effect: str

    def __post_init__(self) -> None:
        if (
            self.registry_id != "builder-core-synthetic-empty-skill-registry"
            or self.version != "1.0.0"
            or self.source_hash != EMPTY_SKILL_REGISTRY_SHA256
            or self.capabilities != EMPTY_REGISTRY_CAPABILITIES
            or self.skills
            or self.external_skills_required
            or self.dynamic_skill_discovery_allowed
            or self.undeclared_skill_use != "FAIL_CLOSED"
            or self.later_external_skill_effect
            != "NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED"
        ):
            raise RegistryIntegrityError(
                "Empty skill registry semantics do not match the approved policy."
            )

    def require_skill(
        self, skill_id: str, *, dynamically_discovered: bool = False
    ) -> None:
        if dynamically_discovered or skill_id not in self.skills:
            raise UndeclaredSkillUseRejected(
                "Undeclared or dynamically discovered skill use is prohibited.",
                skill_id=skill_id,
                dynamically_discovered=dynamically_discovered,
                registry_id=self.registry_id,
                registry_version=self.version,
            )

    def validate_skill_change(
        self, *, candidate_version: str, candidate_skills: tuple[str, ...]
    ) -> None:
        if tuple(candidate_skills) != self.skills and candidate_version == self.version:
            raise ImmutableProfileVersionRequired(
                "Adding a skill requires a new immutable Harness or profile version.",
                current_version=self.version,
                candidate_version=candidate_version,
                candidate_skills=tuple(candidate_skills),
            )


class SyntheticProofTargetProfileRepository:
    """Loads only the immutable, category-neutral Builder Core proof profile."""

    def __init__(self, repository_root: Path) -> None:
        self._root = repository_root.resolve()

    def recognized_target_ids(self) -> frozenset[str]:
        return GOVERNED_TARGET_IDS

    def resolve(
        self,
        target_ids: tuple[str, ...],
        category_id: str,
        profile_id: str,
    ) -> TargetProfile:
        target_id = validate_single_target(target_ids)
        if (
            target_id != AUTHORIZED_TARGET_ID
            or category_id != SYNTHETIC_CATEGORY_ID
            or profile_id != SYNTHETIC_PROFILE_ID
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "The selected target/category/profile is outside the synthetic Builder Core proof.",
                target_id=target_id,
                category_id=category_id,
                profile_id=profile_id,
            )
        return self.load_authorized_profile()

    def load_authorized_profile(self) -> TargetProfile:
        fixture = self._read_verified(
            SYNTHETIC_PROFILE_FIXTURE, SYNTHETIC_PROFILE_FIXTURE_SHA256
        ).decode("utf-8")
        self._read_verified(
            EMPTY_SKILL_REGISTRY_POLICY, EMPTY_SKILL_REGISTRY_POLICY_SHA256
        )
        self._read_verified(
            EMPTY_SKILL_REGISTRY_SCHEMA, EMPTY_SKILL_REGISTRY_SCHEMA_SHA256
        )
        registry = self.load_empty_skill_registry()
        self._require_tokens(
            fixture,
            (
                "schema_version: cmf-builder-synthetic-proof-target-profile/v1",
                f"fixture_id: {SYNTHETIC_PROFILE_ID}",
                f'fixture_version: "{SYNTHETIC_PROFILE_VERSION}"',
                "synthetic: true",
                "repository_owned: true",
                "production_eligible: false",
                "certified: false",
                "purpose: Builder_Core_validation_only",
                f"compilation_target: {AUTHORIZED_TARGET_ID}",
                f"profile_id: {SYNTHETIC_PROFILE_ID}",
                "mode: none",
                "canonical_category_registry_membership: false",
                "external_skills_required: false",
                "dynamically_discovered_skills_allowed: false",
                "final_task_execution_by_builder: prohibited",
                *(f"- {item}" for item in SYNTHETIC_REQUIRED_WORK),
                *(f"- {item}" for item in SYNTHETIC_PROHIBITED_INTEGRATIONS),
            ),
            artifact="synthetic target-profile fixture",
        )
        proof = SupplementalProofMetadata(
            proof_kind="synthetic_builder_core_proof",
            profile_source_hash=SYNTHETIC_PROFILE_FIXTURE_SHA256,
            synthetic=True,
            repository_owned=True,
            non_production=True,
            non_certified=True,
            builder_core_validation_only=True,
            category_binding_mode="none",
            canonical_category_registry_membership=False,
            skill_registry_id=registry.registry_id,
            skill_registry_version=registry.version,
            skill_registry_hash=registry.source_hash,
            declared_skill_ids=registry.skills,
            external_skills_required=registry.external_skills_required,
            dynamic_skill_discovery_allowed=registry.dynamic_skill_discovery_allowed,
            later_external_skill_effect=registry.later_external_skill_effect,
            prohibited_integrations=SYNTHETIC_PROHIBITED_INTEGRATIONS,
        )
        return TargetProfile(
            target_id=AUTHORIZED_TARGET_ID,
            category_id=SYNTHETIC_CATEGORY_ID,
            profile_id=SYNTHETIC_PROFILE_ID,
            canonical_path=(
                "ST-01.01-SYNTHETIC-PROOF/synthetic_text_normalization_v1"
            ),
            version=SYNTHETIC_PROFILE_VERSION,
            compiler_id="run-governance/synthetic-proof/v1",
            compatibility_state="builder_core_validation_only",
            production_certified=False,
            required_work=SYNTHETIC_REQUIRED_WORK,
            lifecycle_edges=(
                ("CREATED", "SOURCE_DIAGNOSTIC"),
                ("SOURCE_DIAGNOSTIC", "SOURCE_LOCKED"),
                ("SOURCE_LOCKED", "ATOMICITY_RATIFICATION"),
                ("ATOMICITY_RATIFICATION", "GENESIS"),
            ),
            transition_prerequisites=(
                ("SOURCE_DIAGNOSTIC", ("target_profile_selected",)),
                ("SOURCE_LOCKED", ("source_lock_attached",)),
                ("ATOMICITY_RATIFICATION", ("atomic_boundary_ratified",)),
                ("GENESIS", ("canonical_harness_ir_compiled",)),
            ),
            supplemental_proof=proof,
        )

    def load_empty_skill_registry(self) -> GovernedEmptySkillRegistry:
        content = self._read_verified(
            EMPTY_SKILL_REGISTRY, EMPTY_SKILL_REGISTRY_SHA256
        ).decode("utf-8")
        self._require_tokens(
            content,
            (
                "schema_version: cmf-builder-empty-skill-registry/v1",
                "registry_id: builder-core-synthetic-empty-skill-registry",
                "version: 1.0.0",
                "status: ACTIVE_SYNTHETIC_PROOF_ONLY",
                "scope: ST-01.01-SYNTHETIC-PROOF",
                "skills: []",
                "external_skills_required: false",
                "dynamic_skill_discovery_allowed: false",
                "undeclared_skill_use: FAIL_CLOSED",
                "later_external_skill_effect: NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED",
                *(f"capability_id: {item}" for item in EMPTY_REGISTRY_CAPABILITIES),
            ),
            artifact="empty skill registry",
        )
        if content.count("owner_kind: builder_code") != len(
            EMPTY_REGISTRY_CAPABILITIES
        ) or content.count("determinism: deterministic") != len(
            EMPTY_REGISTRY_CAPABILITIES
        ):
            raise RegistryIntegrityError(
                "Every synthetic proof capability must be deterministic and Builder-code-owned."
            )
        return GovernedEmptySkillRegistry(
            registry_id="builder-core-synthetic-empty-skill-registry",
            version="1.0.0",
            source_hash=EMPTY_SKILL_REGISTRY_SHA256,
            capabilities=EMPTY_REGISTRY_CAPABILITIES,
            skills=(),
            external_skills_required=False,
            dynamic_skill_discovery_allowed=False,
            undeclared_skill_use="FAIL_CLOSED",
            later_external_skill_effect="NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED",
        )

    def _read_verified(self, relative: Path, expected_sha256: str) -> bytes:
        path = (self._root / relative).resolve()
        if self._root not in path.parents:
            raise RegistryIntegrityError(
                "Governed synthetic proof path escapes repository root.",
                path=relative.as_posix(),
            )
        try:
            content = path.read_bytes()
        except OSError as error:
            raise RegistryIntegrityError(
                "Governed synthetic proof input is unavailable.",
                path=relative.as_posix(),
            ) from error
        observed = sha256(content).hexdigest()
        if observed != expected_sha256:
            raise RegistryIntegrityError(
                "Governed synthetic proof hash does not match the Development Capsule.",
                path=relative.as_posix(),
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return content

    @staticmethod
    def _require_tokens(
        content: str, tokens: tuple[str, ...], *, artifact: str
    ) -> None:
        missing = tuple(token for token in tokens if token not in content)
        if missing:
            raise RegistryIntegrityError(
                f"Required semantics are absent from the governed {artifact}.",
                missing_tokens=missing,
            )
