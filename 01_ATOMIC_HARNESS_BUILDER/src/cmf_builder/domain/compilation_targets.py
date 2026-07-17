from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Mapping, Sequence

from cmf_builder.domain.category_syntax import GovernedRef


TARGET_IDS = (
    "atomic_content_harness",
    "visual_asset_editor",
    "content_asset_delegation_contract",
)
TARGET_ID_SET = frozenset(TARGET_IDS)
NOT_APPLICABLE = "NOT_APPLICABLE"
EXTERNAL_VALIDATION_PENDING = "EXTERNAL_VALIDATION_PENDING"
DELEGATION_VERSION = "1.1.0-rc.4"
DELEGATION_TRUST = "local_unsigned_release_candidate"
UNCERTIFIED_DEVELOPMENT_ONLY = "UNCERTIFIED_DEVELOPMENT_ONLY"
_TARGET_POLICIES: Mapping[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "atomic_content_harness": (
        ("category_profile_extension", "activative_intelligence_extension"),
        ("no_external_runtime", "no_external_authority_borrowing"),
    ),
    "visual_asset_editor": (
        ("visual_semantic_mapping", "visual_narrative_mapping"),
        ("no_image_generation", "no_external_runtime", "no_semantic_mutation"),
    ),
    "content_asset_delegation_contract": (
        (DELEGATION_TRUST, "delegation_rc4_mapping"),
        ("no_shared_schema_ownership", "no_transport", "no_runtime"),
    ),
}
_EXTERNAL_SNAPSHOT_AUTHORITIES = {
    "visual_asset_editor": "Visual Asset Editor product authority",
    "content_asset_delegation_contract": "Delegation Protocol product authority",
}
_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
_SHA256 = re.compile(r"^[a-f0-9]{64}$")


class CompilationTargetError(ValueError):
    pass


class TargetRegistryRejected(CompilationTargetError):
    pass


class TargetSelectionRejected(CompilationTargetError):
    pass


class TargetAuthorityRejected(CompilationTargetError):
    pass


class TargetVersionConflict(CompilationTargetError):
    pass


@dataclass(frozen=True, slots=True)
class CompilationTargetProfile:
    target_id: str
    target_version: str
    product_owner: str
    execution_owner: str
    source_profile_ref: GovernedRef
    ir_projection_ref: GovernedRef
    genesis_graph_ref: GovernedRef
    compiler_ref: GovernedRef
    artifact_set_ref: GovernedRef
    evaluation_gate_ref: GovernedRef
    compatibility_state: str
    certification_scope: str
    required_extensions: tuple[str, ...]
    explicit_prohibitions: tuple[str, ...]
    interface_snapshot_ref: GovernedRef | None
    authority_ref: GovernedRef
    provenance: tuple[GovernedRef, ...]
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        if self.target_id not in TARGET_ID_SET:
            raise TargetRegistryRejected("Target identity is not one of the three governed targets.")
        _require_version(self.target_version, "target_version")
        for value, field in (
            (self.product_owner, "product_owner"),
            (self.execution_owner, "execution_owner"),
            (self.compatibility_state, "compatibility_state"),
            (self.certification_scope, "certification_scope"),
        ):
            _require_text(value, field)
        for ref, role in (
            (self.source_profile_ref, "source_profile"),
            (self.ir_projection_ref, "ir_projection"),
            (self.genesis_graph_ref, "genesis_graph"),
            (self.compiler_ref, "compiler"),
            (self.artifact_set_ref, "artifact_set"),
            (self.evaluation_gate_ref, "evaluation_gate"),
            (self.authority_ref, "target_authority"),
        ):
            _validate_ref(ref, role)
        _validate_distinct_profile_boundary(self)
        if self.certification_scope != UNCERTIFIED_DEVELOPMENT_ONLY:
            raise TargetRegistryRejected(
                "Target certification scope must remain exact uncertified development-only."
            )
        expected_extensions, expected_prohibitions = _TARGET_POLICIES[self.target_id]
        if (
            tuple(sorted(self.required_extensions)) != tuple(sorted(expected_extensions))
            or tuple(sorted(self.explicit_prohibitions))
            != tuple(sorted(expected_prohibitions))
        ):
            raise TargetRegistryRejected(
                "Target extensions and prohibitions must match the exact governed target policy."
            )
        if not self.required_extensions or not self.explicit_prohibitions:
            raise TargetRegistryRejected(
                "Target extensions and explicit prohibitions must both be non-empty."
            )
        if len(set(self.required_extensions)) != len(self.required_extensions):
            raise TargetRegistryRejected("Target extensions must be unique.")
        if len(set(self.explicit_prohibitions)) != len(self.explicit_prohibitions):
            raise TargetRegistryRejected("Target prohibitions must be unique.")
        for value in self.required_extensions + self.explicit_prohibitions:
            _require_text(value, "target boundary item")
        if not self.provenance:
            raise TargetRegistryRejected("Target profile provenance cannot be empty.")
        for ref in self.provenance:
            ref.validate()
        if self.production_ready or self.certified:
            raise TargetRegistryRejected(
                "Offline target profiles cannot claim production readiness or certification."
            )

    @property
    def profile_hash(self) -> str:
        return f"sha256:{sha256(_canonical_json(self.canonical_dict())).hexdigest()}"

    def canonical_dict(self) -> dict[str, object]:
        return {
            "target_id": self.target_id,
            "target_version": self.target_version,
            "product_owner": self.product_owner,
            "execution_owner": self.execution_owner,
            "source_profile_ref": self.source_profile_ref.canonical_dict(),
            "ir_projection_ref": self.ir_projection_ref.canonical_dict(),
            "genesis_graph_ref": self.genesis_graph_ref.canonical_dict(),
            "compiler_ref": self.compiler_ref.canonical_dict(),
            "artifact_set_ref": self.artifact_set_ref.canonical_dict(),
            "evaluation_gate_ref": self.evaluation_gate_ref.canonical_dict(),
            "compatibility_state": self.compatibility_state,
            "certification_scope": self.certification_scope,
            "required_extensions": list(sorted(self.required_extensions)),
            "explicit_prohibitions": list(sorted(self.explicit_prohibitions)),
            "interface_snapshot_ref_or_NOT_APPLICABLE": (
                NOT_APPLICABLE
                if self.interface_snapshot_ref is None
                else self.interface_snapshot_ref.canonical_dict()
            ),
            "authority_ref": self.authority_ref.canonical_dict(),
            "provenance": [
                ref.canonical_dict() for ref in _sorted_refs(self.provenance)
            ],
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class CompilationTargetRegistry:
    registry_id: str
    registry_version: str
    profiles: tuple[CompilationTargetProfile, ...]
    authority_ref: GovernedRef
    registry_hash: str
    canonical_bytes: bytes
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        _require_text(self.registry_id, "registry_id")
        _require_version(self.registry_version, "registry_version")
        _validate_ref(self.authority_ref, "target_authority")
        ordered = tuple(sorted(self.profiles, key=lambda profile: profile.target_id))
        if ordered != self.profiles:
            raise TargetRegistryRejected("Target profiles must use canonical target ordering.")
        ids = tuple(profile.target_id for profile in ordered)
        if len(ordered) != 3 or frozenset(ids) != TARGET_ID_SET or len(set(ids)) != 3:
            raise TargetRegistryRejected(
                "The registry must contain exactly the three governed target identities."
            )
        if any(profile.authority_ref != self.authority_ref for profile in ordered):
            raise TargetAuthorityRejected(
                "Every target profile must bind the exact registry authority."
            )
        if self.production_ready or self.certified:
            raise TargetRegistryRejected(
                "The compilation-target registry cannot claim production readiness or certification."
            )
        expected_bytes = _canonical_json(
            _registry_content(
                registry_id=self.registry_id,
                registry_version=self.registry_version,
                profiles=ordered,
                authority_ref=self.authority_ref,
            )
        )
        expected_hash = f"sha256:{sha256(expected_bytes).hexdigest()}"
        if self.canonical_bytes != expected_bytes or self.registry_hash != expected_hash:
            raise TargetRegistryRejected(
                "Registry canonical bytes or immutable identity do not match governed content."
            )

    def canonical_dict(self) -> dict[str, object]:
        value = json.loads(self.canonical_bytes.decode("utf-8"))
        value["registry_hash"] = self.registry_hash
        return value


@dataclass(frozen=True, slots=True)
class TargetSelection:
    run_id: str
    target_id: str
    profile_hash: str
    registry_hash: str
    authority_identity: str
    selection_hash: str
    compatibility_state: str
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        _require_text(self.run_id, "run_id")
        if self.target_id not in TARGET_ID_SET:
            raise TargetSelectionRejected("Selection target identity is not governed.")
        for value, field in (
            (self.profile_hash, "profile_hash"),
            (self.registry_hash, "registry_hash"),
            (self.selection_hash, "selection_hash"),
        ):
            _require_digest(value, field)
        _require_text(self.authority_identity, "authority_identity")
        expected_compatibility = (
            "BUILDER_LOCAL_STRUCTURAL"
            if self.target_id == "atomic_content_harness"
            else EXTERNAL_VALIDATION_PENDING
        )
        if self.compatibility_state != expected_compatibility:
            raise TargetSelectionRejected("Selection compatibility state contradicts its target.")
        if self.production_ready or self.certified:
            raise TargetSelectionRejected("Selection cannot claim readiness or certification.")
        expected_hash = f"sha256:{sha256(_canonical_json(self.identity_dict())).hexdigest()}"
        if self.selection_hash != expected_hash:
            raise TargetSelectionRejected("Selection identity does not match its governed payload.")

    def identity_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "target_id": self.target_id,
            "profile_hash": self.profile_hash,
            "registry_hash": self.registry_hash,
            "authority_identity": self.authority_identity,
            "compatibility_state": self.compatibility_state,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class TargetSelectionReceipt:
    receipt_id: str
    run_id: str
    target_id: str
    registry_hash: str
    profile_hash: str
    selection_hash: str
    authority_identity: str
    compatibility_state: str
    outcome: str
    failure_context: str
    event_name: str = "ST-07.01:OutcomeVerified"

    def __post_init__(self) -> None:
        if self.target_id not in TARGET_ID_SET:
            raise TargetSelectionRejected("Receipt target identity is not governed.")
        for value, field in (
            (self.registry_hash, "registry_hash"),
            (self.profile_hash, "profile_hash"),
            (self.selection_hash, "selection_hash"),
        ):
            _require_digest(value, field)
        expected_compatibility = (
            "BUILDER_LOCAL_STRUCTURAL"
            if self.target_id == "atomic_content_harness"
            else EXTERNAL_VALIDATION_PENDING
        )
        if self.compatibility_state != expected_compatibility:
            raise TargetSelectionRejected("Receipt compatibility state contradicts its target.")
        expected_id = (
            "ST-07.01:TargetSelection:"
            f"{sha256(_canonical_json(self.identity_dict())).hexdigest()}"
        )
        if self.receipt_id != expected_id:
            raise TargetSelectionRejected("Selection receipt identity does not match selection.")
        if self.outcome != "OUTCOME_VERIFIED" or self.failure_context != "NONE":
            raise TargetSelectionRejected("Successful selection receipt has a false outcome.")
        if self.event_name != "ST-07.01:OutcomeVerified":
            raise TargetSelectionRejected("Selection receipt event is not governed.")

    @property
    def receipt_hash(self) -> str:
        return f"sha256:{sha256(_canonical_json(self.canonical_dict())).hexdigest()}"

    def canonical_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "run_id": self.run_id,
            "target_id": self.target_id,
            "registry_hash": self.registry_hash,
            "profile_hash": self.profile_hash,
            "selection_hash": self.selection_hash,
            "authority_identity": self.authority_identity,
            "compatibility_state": self.compatibility_state,
            "outcome": self.outcome,
            "failure_context": self.failure_context,
            "event_name": self.event_name,
        }

    def identity_dict(self) -> dict[str, object]:
        value = self.canonical_dict()
        value.pop("receipt_id")
        return value


@dataclass(frozen=True, slots=True)
class TargetSelectionResult:
    selection: TargetSelection
    receipt: TargetSelectionReceipt

    def __post_init__(self) -> None:
        for field in (
            "run_id",
            "target_id",
            "registry_hash",
            "profile_hash",
            "selection_hash",
            "authority_identity",
            "compatibility_state",
        ):
            if getattr(self.selection, field) != getattr(self.receipt, field):
                raise TargetSelectionRejected(
                    f"Selection result has mismatched {field} linkage."
                )


def compile_target_registry(
    *,
    registry_id: str,
    registry_version: str,
    profiles: Sequence[CompilationTargetProfile],
    authority_ref: GovernedRef,
) -> CompilationTargetRegistry:
    _require_text(registry_id, "registry_id")
    _require_version(registry_version, "registry_version")
    _validate_ref(authority_ref, "target_authority")
    ordered = tuple(sorted(profiles, key=lambda profile: profile.target_id))
    ids = tuple(profile.target_id for profile in ordered)
    if len(ordered) != 3 or frozenset(ids) != TARGET_ID_SET or len(set(ids)) != 3:
        raise TargetRegistryRejected(
            "The registry must contain exactly the three governed target identities."
        )
    if any(profile.authority_ref != authority_ref for profile in ordered):
        raise TargetAuthorityRejected(
            "Every target profile must bind the exact registry authority."
        )
    content = _registry_content(
        registry_id=registry_id,
        registry_version=registry_version,
        profiles=ordered,
        authority_ref=authority_ref,
    )
    canonical_bytes = _canonical_json(content)
    return CompilationTargetRegistry(
        registry_id=registry_id,
        registry_version=registry_version,
        profiles=ordered,
        authority_ref=authority_ref,
        registry_hash=f"sha256:{sha256(canonical_bytes).hexdigest()}",
        canonical_bytes=canonical_bytes,
    )


def _registry_content(
    *,
    registry_id: str,
    registry_version: str,
    profiles: Sequence[CompilationTargetProfile],
    authority_ref: GovernedRef,
) -> dict[str, object]:
    return {
        "schema_version": "cmf-builder-compilation-target-registry/v1",
        "registry_id": registry_id,
        "registry_version": registry_version,
        "target_count": 3,
        "target_ids": list(TARGET_IDS),
        "profiles": [profile.canonical_dict() for profile in profiles],
        "authority_ref": authority_ref.canonical_dict(),
        "universal_target_supported": False,
        "external_compatibility": EXTERNAL_VALIDATION_PENDING,
        "production_ready": False,
        "certified": False,
    }


def select_compilation_target(
    *,
    run_id: str,
    registry: CompilationTargetRegistry,
    requested_target_ids: Sequence[str],
    actor_id: str,
) -> TargetSelectionResult:
    _require_text(run_id, "run_id")
    if actor_id != registry.authority_ref.authority:
        raise TargetAuthorityRejected(
            "Target selection actor does not match the governed registry authority."
        )
    requested = tuple(requested_target_ids)
    if len(requested) != 1:
        raise TargetSelectionRejected("Exactly one compilation target is required.")
    target_id = requested[0]
    if target_id not in TARGET_ID_SET:
        raise TargetSelectionRejected("Unknown or aliased compilation target is prohibited.")
    profile = next(item for item in registry.profiles if item.target_id == target_id)
    core = {
        "run_id": run_id,
        "target_id": target_id,
        "profile_hash": profile.profile_hash,
        "registry_hash": registry.registry_hash,
        "authority_identity": actor_id,
        "compatibility_state": profile.compatibility_state,
        "production_ready": False,
        "certified": False,
    }
    selection_hash = f"sha256:{sha256(_canonical_json(core)).hexdigest()}"
    selection = TargetSelection(
        run_id=run_id,
        target_id=target_id,
        profile_hash=profile.profile_hash,
        registry_hash=registry.registry_hash,
        authority_identity=actor_id,
        compatibility_state=profile.compatibility_state,
        selection_hash=selection_hash,
    )
    receipt_values = {
        "run_id": run_id,
        "target_id": target_id,
        "registry_hash": registry.registry_hash,
        "profile_hash": profile.profile_hash,
        "selection_hash": selection_hash,
        "authority_identity": actor_id,
        "compatibility_state": profile.compatibility_state,
        "outcome": "OUTCOME_VERIFIED",
        "failure_context": "NONE",
        "event_name": "ST-07.01:OutcomeVerified",
    }
    receipt = TargetSelectionReceipt(
        receipt_id=(
            "ST-07.01:TargetSelection:"
            f"{sha256(_canonical_json(receipt_values)).hexdigest()}"
        ),
        run_id=run_id,
        target_id=target_id,
        registry_hash=registry.registry_hash,
        profile_hash=profile.profile_hash,
        selection_hash=selection_hash,
        authority_identity=actor_id,
        compatibility_state=profile.compatibility_state,
        outcome="OUTCOME_VERIFIED",
        failure_context="NONE",
    )
    return TargetSelectionResult(selection, receipt)


def migrate_target_registry(
    previous: CompilationTargetRegistry,
    *,
    new_version: str,
    profiles: Sequence[CompilationTargetProfile],
    authority_ref: GovernedRef,
) -> CompilationTargetRegistry:
    if new_version == previous.registry_version:
        raise TargetVersionConflict("A registry migration requires a new immutable version.")
    candidate = compile_target_registry(
        registry_id=previous.registry_id,
        registry_version=new_version,
        profiles=profiles,
        authority_ref=authority_ref,
    )
    if tuple(profile.target_id for profile in candidate.profiles) != tuple(
        profile.target_id for profile in previous.profiles
    ):
        raise TargetRegistryRejected("Target migration cannot flatten or replace target identities.")
    return candidate


def _validate_distinct_profile_boundary(profile: CompilationTargetProfile) -> None:
    expected: Mapping[str, tuple[str, str, str]] = {
        "atomic_content_harness": (
            "Atomic Harness Builder",
            "compiled_harness_owner_not_ST_07_01",
            "BUILDER_LOCAL_STRUCTURAL",
        ),
        "visual_asset_editor": (
            "Visual Asset Editor product authority",
            "external_visual_asset_editor",
            EXTERNAL_VALIDATION_PENDING,
        ),
        "content_asset_delegation_contract": (
            "Delegation Protocol product authority",
            "external_delegation_protocol",
            EXTERNAL_VALIDATION_PENDING,
        ),
    }
    owner, execution_owner, compatibility = expected[profile.target_id]
    if (
        profile.product_owner != owner
        or profile.execution_owner != execution_owner
        or profile.compatibility_state != compatibility
    ):
        raise TargetRegistryRejected(
            "Target ownership, execution ownership, or compatibility was flattened."
        )
    if profile.target_id == "atomic_content_harness":
        if profile.interface_snapshot_ref is not None:
            raise TargetRegistryRejected(
                "The Builder-owned target must declare its external interface snapshot NOT_APPLICABLE."
            )
    else:
        if profile.interface_snapshot_ref is None:
            raise TargetRegistryRejected("External targets require a hash-pinned interface snapshot.")
        expected_role = (
            "vae_interface_snapshot"
            if profile.target_id == "visual_asset_editor"
            else "delegation_interface_snapshot"
        )
        _validate_ref(profile.interface_snapshot_ref, expected_role)
        expected_authority = _EXTERNAL_SNAPSHOT_AUTHORITIES[profile.target_id]
        if profile.interface_snapshot_ref.authority != expected_authority:
            raise TargetAuthorityRejected(
                "External target interface snapshot must carry its external owning authority."
            )
    if profile.target_id == "content_asset_delegation_contract":
        snapshot = profile.interface_snapshot_ref
        assert snapshot is not None
        if snapshot.version != DELEGATION_VERSION or DELEGATION_TRUST not in profile.required_extensions:
            raise TargetRegistryRejected("Delegation target must preserve the exact RC4 unsigned candidate pin.")


def _validate_ref(ref: GovernedRef, expected_role: str) -> None:
    ref.validate()
    if ref.lineage_role != expected_role:
        raise TargetRegistryRejected(f"Expected governed reference role {expected_role}.")


def _sorted_refs(refs: Sequence[GovernedRef]) -> tuple[GovernedRef, ...]:
    keys = [(item.lineage_role, item.object_id, item.version, item.sha256) for item in refs]
    if len(keys) != len(set(keys)):
        raise TargetRegistryRejected("Target provenance contains duplicate references.")
    return tuple(
        sorted(refs, key=lambda item: (item.lineage_role, item.object_id, item.version, item.sha256))
    )


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise TargetRegistryRejected(f"{field} must be a non-empty canonical string.")
    return value


def _require_version(value: object, field: str) -> str:
    text = _require_text(value, field)
    if _SEMVER.fullmatch(text) is None:
        raise TargetRegistryRejected(f"{field} must be an immutable semantic version.")
    return text


def _require_digest(value: object, field: str) -> str:
    text = _require_text(value, field)
    if not text.startswith("sha256:") or _SHA256.fullmatch(text.split(":", 1)[1]) is None:
        raise TargetSelectionRejected(f"{field} must be an exact SHA-256 identity.")
    return text


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")
