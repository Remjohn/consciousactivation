"""Workflow profile lifecycle contracts for OD-AM-002 / ST-09.07.

This module implements only offline development-mode workflow profile
versioning, migration, rollback, hotfix, and invalidation semantics.  It does
not deploy workflows, authorize production, or close external evidence gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class WorkflowProfileLifecycleError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class ProfileLifecycleState(str, Enum):
    DRAFT = "DRAFT"
    DEVELOPMENT_VALIDATED = "DEVELOPMENT_VALIDATED"
    PROMOTION_PENDING = "PROMOTION_PENDING"
    PROMOTED_DEVELOPMENT = "PROMOTED_DEVELOPMENT"
    SUPERSEDED = "SUPERSEDED"
    ROLLBACK_PENDING = "ROLLBACK_PENDING"
    ROLLED_BACK = "ROLLED_BACK"
    HOTFIX_PENDING = "HOTFIX_PENDING"
    HOTFIX_APPLIED_DEVELOPMENT = "HOTFIX_APPLIED_DEVELOPMENT"
    INVALIDATED = "INVALIDATED"


class LifecycleAction(str, Enum):
    CREATE = "CREATE"
    MIGRATE = "MIGRATE"
    REQUEST_PROMOTION = "REQUEST_PROMOTION"
    PROMOTE_DEVELOPMENT = "PROMOTE_DEVELOPMENT"
    REQUEST_ROLLBACK = "REQUEST_ROLLBACK"
    ROLLBACK = "ROLLBACK"
    REQUEST_HOTFIX = "REQUEST_HOTFIX"
    APPLY_HOTFIX = "APPLY_HOTFIX"
    INVALIDATE = "INVALIDATE"


class ActorType(str, Enum):
    HUMAN = "HUMAN"
    GOVERNED_AGENT = "GOVERNED_AGENT"
    DETERMINISTIC_CODE = "DETERMINISTIC_CODE"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise WorkflowProfileLifecycleError("MISSING_GOVERNED_FIELD", f"{name} is required")


def _tuple(value: tuple[Any, ...], name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise WorkflowProfileLifecycleError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class ProfileAuthority:
    authority_id: str
    authority_sha256: str
    actor_type: ActorType
    permitted_actions: tuple[LifecycleAction, ...]
    scope: tuple[str, ...]
    production_authority: bool = False
    certification_authority: bool = False

    def __post_init__(self) -> None:
        _text(self.authority_id, "authority_id")
        _text(self.authority_sha256, "authority_sha256")
        _tuple(self.permitted_actions, "permitted_actions")
        _tuple(self.scope, "scope")
        if self.production_authority or self.certification_authority:
            raise WorkflowProfileLifecycleError("PRODUCTION_OR_CERTIFICATION_AUTHORITY_PROHIBITED", "OD-AM-002 is offline development only")

    @property
    def authority_identity(self) -> str:
        return sha256_of(
            {
                "authority_id": self.authority_id,
                "authority_sha256": self.authority_sha256,
                "actor_type": self.actor_type.value,
                "permitted_actions": [action.value for action in self.permitted_actions],
                "scope": list(self.scope),
                "production_authority": False,
                "certification_authority": False,
            }
        )


@dataclass(frozen=True)
class WorkflowProfileVersion:
    profile_id: str
    version: str
    state: ProfileLifecycleState
    workflow_graph_identity: str
    compatibility_evidence_refs: tuple[str, ...]
    migration_evidence_refs: tuple[str, ...]
    predecessor_profile_identity: str | None
    supersedes_profile_identity: str | None
    rollback_target_identity: str | None
    authority_identity: str
    evidence_refs: tuple[str, ...]
    invalidated_descendants: tuple[str, ...] = ()
    production_ready: bool = False
    certified: bool = False
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for value, name in (
            (self.profile_id, "profile_id"),
            (self.version, "version"),
            (self.workflow_graph_identity, "workflow_graph_identity"),
            (self.authority_identity, "authority_identity"),
        ):
            _text(value, name)
        _tuple(self.evidence_refs, "evidence_refs")
        if self.production_ready or self.certified:
            raise WorkflowProfileLifecycleError("FALSE_READINESS_CLAIM", "workflow profile lifecycle cannot claim production readiness or certification")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "version": self.version,
            "state": self.state.value,
            "workflow_graph_identity": self.workflow_graph_identity,
            "compatibility_evidence_refs": list(self.compatibility_evidence_refs),
            "migration_evidence_refs": list(self.migration_evidence_refs),
            "predecessor_profile_identity": self.predecessor_profile_identity,
            "supersedes_profile_identity": self.supersedes_profile_identity,
            "rollback_target_identity": self.rollback_target_identity,
            "authority_identity": self.authority_identity,
            "evidence_refs": list(self.evidence_refs),
            "invalidated_descendants": list(self.invalidated_descendants),
            "production_ready": False,
            "certified": False,
        }

    @property
    def profile_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise WorkflowProfileLifecycleError("MUTATED_GOVERNED_OBJECT", "profile version changed after creation")
        payload["profile_identity"] = sha256_of(payload)
        return payload


@dataclass(frozen=True)
class LifecycleCommand:
    command_id: str
    action: LifecycleAction
    profile_identity: str
    payload_sha256: str
    expected_authority_identity: str

    @property
    def command_identity(self) -> str:
        return sha256_of(
            {
                "command_id": self.command_id,
                "action": self.action.value,
                "profile_identity": self.profile_identity,
                "payload_sha256": self.payload_sha256,
                "expected_authority_identity": self.expected_authority_identity,
            }
        )


@dataclass(frozen=True)
class LifecycleReceipt:
    action: LifecycleAction
    source_profile_identity: str
    resulting_profile_identity: str
    authority_identity: str
    evidence_refs: tuple[str, ...]
    excluded_scope: tuple[str, ...]
    limitations: tuple[str, ...]

    @property
    def receipt_identity(self) -> str:
        return sha256_of(
            {
                "action": self.action.value,
                "source_profile_identity": self.source_profile_identity,
                "resulting_profile_identity": self.resulting_profile_identity,
                "authority_identity": self.authority_identity,
                "evidence_refs": list(self.evidence_refs),
                "excluded_scope": list(self.excluded_scope),
                "limitations": list(self.limitations),
            }
        )


def _require_authority(authority: ProfileAuthority, action: LifecycleAction, *, human_required: bool = False) -> None:
    if action not in authority.permitted_actions:
        raise WorkflowProfileLifecycleError("ACTION_NOT_AUTHORIZED", f"{action.value} is not authorized")
    if human_required and authority.actor_type is not ActorType.HUMAN:
        raise WorkflowProfileLifecycleError("HUMAN_AUTHORITY_REQUIRED", "agent or code authority cannot approve this lifecycle action")


def request_promotion(profile: WorkflowProfileVersion, authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.REQUEST_PROMOTION, human_required=True)
    if profile.state is not ProfileLifecycleState.DEVELOPMENT_VALIDATED:
        raise WorkflowProfileLifecycleError("PROFILE_NOT_DEVELOPMENT_VALIDATED", "only development-validated profiles may request promotion")
    _tuple(profile.compatibility_evidence_refs, "compatibility_evidence_refs")
    result = WorkflowProfileVersion(
        profile.profile_id,
        f"{profile.version}+promotion-request",
        ProfileLifecycleState.PROMOTION_PENDING,
        profile.workflow_graph_identity,
        profile.compatibility_evidence_refs,
        profile.migration_evidence_refs,
        profile.profile_identity,
        None,
        None,
        authority.authority_identity,
        profile.evidence_refs + ("promotion:human-authority",),
    )
    return result, _receipt(LifecycleAction.REQUEST_PROMOTION, profile, result, authority)


def promote_development(profile: WorkflowProfileVersion, authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.PROMOTE_DEVELOPMENT, human_required=True)
    if profile.state is not ProfileLifecycleState.PROMOTION_PENDING:
        raise WorkflowProfileLifecycleError("PROMOTION_REQUEST_REQUIRED", "promotion must follow an attributable human promotion request")
    result = WorkflowProfileVersion(
        profile.profile_id,
        f"{profile.version}+development",
        ProfileLifecycleState.PROMOTED_DEVELOPMENT,
        profile.workflow_graph_identity,
        profile.compatibility_evidence_refs,
        profile.migration_evidence_refs,
        profile.profile_identity,
        None,
        None,
        authority.authority_identity,
        profile.evidence_refs + ("promotion:development-only",),
    )
    return result, _receipt(LifecycleAction.PROMOTE_DEVELOPMENT, profile, result, authority)


def migrate_profile(profile: WorkflowProfileVersion, new_version: str, migration_evidence_refs: tuple[str, ...], authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.MIGRATE)
    _text(new_version, "new_version")
    _tuple(migration_evidence_refs, "migration_evidence_refs")
    result = WorkflowProfileVersion(
        profile.profile_id,
        new_version,
        ProfileLifecycleState.DEVELOPMENT_VALIDATED,
        profile.workflow_graph_identity,
        profile.compatibility_evidence_refs,
        migration_evidence_refs,
        profile.profile_identity,
        profile.profile_identity,
        None,
        authority.authority_identity,
        profile.evidence_refs + migration_evidence_refs,
    )
    return result, _receipt(LifecycleAction.MIGRATE, profile, result, authority)


def rollback_profile(profile: WorkflowProfileVersion, rollback_target: WorkflowProfileVersion, authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.ROLLBACK, human_required=True)
    if profile.state is ProfileLifecycleState.INVALIDATED:
        raise WorkflowProfileLifecycleError("INVALIDATED_PROFILE_CANNOT_ROLLBACK", "invalidated profile cannot be rollback source")
    if rollback_target.profile_id != profile.profile_id:
        raise WorkflowProfileLifecycleError("ROLLBACK_TARGET_MISMATCH", "rollback target must be the same profile")
    if rollback_target.profile_identity not in {profile.predecessor_profile_identity, profile.supersedes_profile_identity}:
        raise WorkflowProfileLifecycleError("EXACT_ROLLBACK_TARGET_REQUIRED", "rollback requires exact governed target identity")
    result = WorkflowProfileVersion(
        profile.profile_id,
        f"{profile.version}+rollback",
        ProfileLifecycleState.ROLLED_BACK,
        rollback_target.workflow_graph_identity,
        rollback_target.compatibility_evidence_refs,
        rollback_target.migration_evidence_refs,
        profile.profile_identity,
        None,
        rollback_target.profile_identity,
        authority.authority_identity,
        profile.evidence_refs + ("rollback:non-destructive",),
    )
    return result, _receipt(LifecycleAction.ROLLBACK, profile, result, authority)


def apply_hotfix(profile: WorkflowProfileVersion, hotfix_id: str, evidence_refs: tuple[str, ...], authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.APPLY_HOTFIX, human_required=True)
    _text(hotfix_id, "hotfix_id")
    _tuple(evidence_refs, "evidence_refs")
    if profile.state is ProfileLifecycleState.INVALIDATED:
        raise WorkflowProfileLifecycleError("INVALIDATED_PROFILE_CANNOT_HOTFIX", "invalidated profile cannot be hotfixed")
    result = WorkflowProfileVersion(
        profile.profile_id,
        f"{profile.version}+hotfix.{hotfix_id}",
        ProfileLifecycleState.HOTFIX_APPLIED_DEVELOPMENT,
        profile.workflow_graph_identity,
        profile.compatibility_evidence_refs,
        profile.migration_evidence_refs,
        profile.profile_identity,
        profile.profile_identity,
        None,
        authority.authority_identity,
        profile.evidence_refs + evidence_refs,
    )
    return result, _receipt(LifecycleAction.APPLY_HOTFIX, profile, result, authority)


def invalidate_profile(profile: WorkflowProfileVersion, descendant_refs: tuple[str, ...], authority: ProfileAuthority) -> tuple[WorkflowProfileVersion, LifecycleReceipt]:
    _require_authority(authority, LifecycleAction.INVALIDATE)
    _tuple(descendant_refs, "descendant_refs")
    result = WorkflowProfileVersion(
        profile.profile_id,
        f"{profile.version}+invalidated",
        ProfileLifecycleState.INVALIDATED,
        profile.workflow_graph_identity,
        profile.compatibility_evidence_refs,
        profile.migration_evidence_refs,
        profile.profile_identity,
        None,
        None,
        authority.authority_identity,
        profile.evidence_refs + ("invalidation:descendant-cascade",),
        descendant_refs,
    )
    return result, _receipt(LifecycleAction.INVALIDATE, profile, result, authority)


def _receipt(action: LifecycleAction, source: WorkflowProfileVersion, result: WorkflowProfileVersion, authority: ProfileAuthority) -> LifecycleReceipt:
    return LifecycleReceipt(
        action=action,
        source_profile_identity=source.profile_identity,
        resulting_profile_identity=result.profile_identity,
        authority_identity=authority.authority_identity,
        evidence_refs=result.evidence_refs,
        excluded_scope=("production_deployment", "certification", "external_provider_validation"),
        limitations=("offline_development_only", "implementation_receipt_not_story_completion"),
    )
