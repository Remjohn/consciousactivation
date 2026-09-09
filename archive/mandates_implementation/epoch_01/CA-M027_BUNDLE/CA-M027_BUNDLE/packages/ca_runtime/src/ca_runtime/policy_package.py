"""Declarative Policy Rule Packages for Conscious Activation Engine (CAE).

Mandate: CA-M027 / Q26 / FR-AUTH-002
Stage: 12 Human Authorization

Provides versioned, inspectable, schema-validated policy packages that express
layer-specific delegation, escalation conditions, and evidence prerequisites
in a structured, deterministic form. Packages are machine-readable YAML/JSON,
carry a canonical identity digest, and are consumed by the runtime without
relying on prose parsing, hidden defaults, or model interpretation.

Critical invariant: a package cannot silently weaken constitutional requirements.
Historical packages are preserved by immutable revision; mutation in place is
prohibited.

State grammar:
  UNLOADED/UNKNOWN_POLICY_PACKAGE
    → load + schema-validate + semantic-validate + canonicalize
    → LOADED_VALID_POLICY_PACKAGE (with identity/digest)
    → (runtime consume / authorize)
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ca_contracts import canonical_json_text, canonical_sha256

logger = logging.getLogger("ca_runtime.policy_package")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEMVER_REGEX = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

CANONICAL_AUTHORITY_LANES: Set[str] = {"HUNTER", "ANALYST", "COMPOSER", "COMMANDER"}

# Schema identity for policy packages (versioned)
POLICY_PACKAGE_SCHEMA_ID = "cae.policy_rule_package"
POLICY_PACKAGE_SCHEMA_VERSION = "1.0.0"

# Constitutional hard rules that packages must not weaken.
# A package that attempts to lower the required lane below the constitutional
# minimum, or to drop a required evidence class for these operations, is rejected.
CONSTITUTIONAL_MINIMUMS: Dict[str, Dict[str, Any]] = {
    "approve": {
        "min_authority_lane": "COMMANDER",
        "required_evidence_classes": ["OPERATOR_DECISION", "EXECUTABLE"],
    },
    "create_transfer_contract": {
        "min_authority_lane": "COMMANDER",
        "required_evidence_classes": ["OPERATOR_DECISION"],
    },
    "ship_release": {
        "min_authority_lane": "COMMANDER",
        "required_evidence_classes": ["OPERATOR_DECISION", "EXECUTABLE"],
    },
    "mutate_historical_policy": {
        "min_authority_lane": "COMMANDER",
        "required_evidence_classes": ["OPERATOR_DECISION"],
        "prohibited": True,
    },
}

LANE_RANK: Dict[str, int] = {
    "HUNTER": 1,
    "ANALYST": 2,
    "COMPOSER": 3,
    "COMMANDER": 4,
}


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class PolicyPackageError(RuntimeError):
    """Base error for policy package load / validation / consumption."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "POLICY_PACKAGE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class PolicyPackageNotFoundError(PolicyPackageError):
    def __init__(self, package_id: str, version: Optional[str] = None):
        ver = f"@{version}" if version else ""
        super().__init__(
            f"Policy package '{package_id}{ver}' not found",
            reason_code="POLICY_PACKAGE_NOT_FOUND",
            details={"package_id": package_id, "version": version},
        )


class PolicyPackageSchemaError(PolicyPackageError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="POLICY_PACKAGE_SCHEMA_INVALID",
            details=details or {},
        )


class PolicyPackageSemanticError(PolicyPackageError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="POLICY_PACKAGE_SEMANTIC_INVALID",
            details=details or {},
        )


class ConstitutionalWeakeningError(PolicyPackageError):
    """Raised when a package would silently weaken a constitutional requirement."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="CONSTITUTIONAL_WEAKENING_REJECTED",
            details=details or {},
        )


class PolicyPackageConflictError(PolicyPackageError):
    def __init__(self, package_id: str, version: str):
        super().__init__(
            f"Policy package '{package_id}@{version}' already registered (immutable)",
            reason_code="POLICY_PACKAGE_CONFLICT",
            details={"package_id": package_id, "version": version},
        )


class PolicyAuthorizationDeniedError(PolicyPackageError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="POLICY_AUTHORIZATION_DENIED",
            details=details or {},
        )


# ---------------------------------------------------------------------------
# Typed Models
# ---------------------------------------------------------------------------

class EvidencePrerequisite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_class: str = Field(..., min_length=1)
    required: bool = True
    locator_hint: Optional[str] = None


class EscalationCondition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    condition_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    escalate_to_lane: str
    trigger: str = Field(..., min_length=1)

    @field_validator("escalate_to_lane")
    @classmethod
    def _lane_ok(cls, v: str) -> str:
        if v not in CANONICAL_AUTHORITY_LANES:
            raise ValueError(f"escalate_to_lane must be one of {sorted(CANONICAL_AUTHORITY_LANES)}")
        return v


class AuthorizationPredicate(BaseModel):
    """Typed authorization predicate. Explicit; no free-form prose authority."""

    model_config = ConfigDict(extra="forbid")

    predicate_id: str = Field(..., min_length=1)
    operation: str = Field(..., min_length=1)
    required_authority_lane: str
    actor_class: Optional[str] = None
    evidence_prerequisites: List[EvidencePrerequisite] = Field(default_factory=list)
    escalation_conditions: List[EscalationCondition] = Field(default_factory=list)
    allow_delegation: bool = False
    notes: Optional[str] = None

    @field_validator("required_authority_lane")
    @classmethod
    def _lane_ok(cls, v: str) -> str:
        if v not in CANONICAL_AUTHORITY_LANES:
            raise ValueError(f"required_authority_lane must be one of {sorted(CANONICAL_AUTHORITY_LANES)}")
        return v


class ConstitutionalDependency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dependency_id: str = Field(..., min_length=1)
    ref: str = Field(..., min_length=1)
    immutable: bool = True
    digest: Optional[str] = None


class PolicyRulePackageManifest(BaseModel):
    """Canonical declarative policy rule package (YAML/JSON)."""

    model_config = ConfigDict(extra="forbid")

    schema_id: str = Field(default=POLICY_PACKAGE_SCHEMA_ID)
    schema_version: str = Field(default=POLICY_PACKAGE_SCHEMA_VERSION)
    package_id: str = Field(..., min_length=1, pattern=r"^[a-z][a-z0-9_]*$")
    version: str
    status: str = Field(default="ACTIVE")
    applicable_program: Optional[str] = None
    scope: Optional[str] = None
    description: Optional[str] = None
    rules: List[AuthorizationPredicate] = Field(default_factory=list)
    constitutional_dependencies: List[ConstitutionalDependency] = Field(default_factory=list)
    # Explicit compatibility contract: unknown fields are rejected (extra=forbid).

    @field_validator("version")
    @classmethod
    def _semver(cls, v: str) -> str:
        if not SEMVER_REGEX.match(v):
            raise ValueError(f"version must be valid SemVer 2.0.0: {v}")
        return v

    @field_validator("schema_version")
    @classmethod
    def _schema_semver(cls, v: str) -> str:
        if not SEMVER_REGEX.match(v):
            raise ValueError(f"schema_version must be valid SemVer: {v}")
        return v

    @field_validator("status")
    @classmethod
    def _status_ok(cls, v: str) -> str:
        allowed = {"ACTIVE", "DEPRECATED", "REVOKED", "DRAFT"}
        if v not in allowed:
            raise ValueError(f"status must be one of {sorted(allowed)}")
        return v

    @model_validator(mode="after")
    def _non_empty_rules_when_active(self) -> "PolicyRulePackageManifest":
        if self.status == "ACTIVE" and not self.rules:
            raise ValueError("ACTIVE policy packages must declare at least one rule")
        return self


class LoadedPolicyPackage(BaseModel):
    """Runtime-loaded, validated, identity-bearing policy package."""

    model_config = ConfigDict(extra="forbid")

    manifest: PolicyRulePackageManifest
    identity_digest: str  # canonical sha256 of the normalized package body
    source_path: Optional[str] = None
    revision: int = 1  # immutable revision counter for the (package_id, version) identity
    loaded_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Semantic validation (constitutional non-weakening)
# ---------------------------------------------------------------------------

def _lane_rank(lane: str) -> int:
    return LANE_RANK.get(lane, 0)


def validate_constitutional_non_weakening(manifest: PolicyRulePackageManifest) -> None:
    """Reject packages that would lower constitutional minimum authority or evidence.

    A package may only *raise* requirements (higher lane rank, additional evidence).
    It may never lower them for constitutionally protected operations.
    """
    for rule in manifest.rules:
        op = rule.operation
        if op not in CONSTITUTIONAL_MINIMUMS:
            continue
        mins = CONSTITUTIONAL_MINIMUMS[op]

        if mins.get("prohibited") and rule.allow_delegation:
            raise ConstitutionalWeakeningError(
                f"Rule '{rule.predicate_id}' attempts to allow delegation of prohibited operation '{op}'",
                details={"operation": op, "predicate_id": rule.predicate_id},
            )

        min_lane = mins.get("min_authority_lane")
        if min_lane and _lane_rank(rule.required_authority_lane) < _lane_rank(min_lane):
            raise ConstitutionalWeakeningError(
                f"Rule '{rule.predicate_id}' weakens required lane for '{op}': "
                f"{rule.required_authority_lane} < constitutional minimum {min_lane}",
                details={
                    "operation": op,
                    "predicate_id": rule.predicate_id,
                    "declared_lane": rule.required_authority_lane,
                    "constitutional_min": min_lane,
                },
            )

        required_classes = set(mins.get("required_evidence_classes") or [])
        declared = {ep.evidence_class for ep in rule.evidence_prerequisites if ep.required}
        missing = required_classes - declared
        if missing:
            raise ConstitutionalWeakeningError(
                f"Rule '{rule.predicate_id}' omits constitutionally required evidence classes for '{op}': {sorted(missing)}",
                details={
                    "operation": op,
                    "predicate_id": rule.predicate_id,
                    "missing_evidence_classes": sorted(missing),
                },
            )


def validate_no_duplicate_rule_ids(manifest: PolicyRulePackageManifest) -> None:
    seen: Set[str] = set()
    for rule in manifest.rules:
        if rule.predicate_id in seen:
            raise PolicyPackageSemanticError(
                f"Duplicate predicate_id '{rule.predicate_id}'",
                details={"predicate_id": rule.predicate_id},
            )
        seen.add(rule.predicate_id)


# ---------------------------------------------------------------------------
# Canonical identity / digest
# ---------------------------------------------------------------------------

def compute_package_identity_digest(manifest: PolicyRulePackageManifest) -> str:
    """Deterministic canonical SHA-256 of the package body (excluding runtime metadata)."""
    body = {
        "schema_id": manifest.schema_id,
        "schema_version": manifest.schema_version,
        "package_id": manifest.package_id,
        "version": manifest.version,
        "status": manifest.status,
        "applicable_program": manifest.applicable_program,
        "scope": manifest.scope,
        "description": manifest.description,
        "rules": [r.model_dump(mode="json") for r in manifest.rules],
        "constitutional_dependencies": [d.model_dump(mode="json") for d in manifest.constitutional_dependencies],
    }
    return canonical_sha256(body)


# ---------------------------------------------------------------------------
# Load / parse
# ---------------------------------------------------------------------------

def parse_policy_package_dict(data: Mapping[str, Any]) -> PolicyRulePackageManifest:
    """Parse and schema-validate a raw dict into a PolicyRulePackageManifest."""
    try:
        return PolicyRulePackageManifest.model_validate(data)
    except Exception as e:
        raise PolicyPackageSchemaError(
            f"Policy package schema validation failed: {e}",
            details={"error": str(e)},
        ) from e


def load_policy_package_from_path(path: Union[str, Path]) -> LoadedPolicyPackage:
    """Load, schema-validate, semantic-validate, and identity a policy package from disk."""
    p = Path(path)
    if not p.is_file():
        raise PolicyPackageNotFoundError(str(p))

    raw_text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(raw_text)
    elif p.suffix.lower() == ".json":
        data = json.loads(raw_text)
    else:
        # try yaml first, then json
        try:
            data = yaml.safe_load(raw_text)
        except Exception:
            data = json.loads(raw_text)

    if not isinstance(data, dict):
        raise PolicyPackageSchemaError(
            "Policy package root must be a mapping",
            details={"path": str(p)},
        )

    manifest = parse_policy_package_dict(data)
    validate_no_duplicate_rule_ids(manifest)
    validate_constitutional_non_weakening(manifest)

    digest = compute_package_identity_digest(manifest)
    from ca_contracts import utc_now_rfc3339

    return LoadedPolicyPackage(
        manifest=manifest,
        identity_digest=digest,
        source_path=str(p.resolve()),
        revision=1,
        loaded_at=utc_now_rfc3339(),
    )


# ---------------------------------------------------------------------------
# Immutable registry (revision-preserving)
# ---------------------------------------------------------------------------

@dataclass
class PolicyPackageRevisionRecord:
    package_id: str
    version: str
    revision: int
    identity_digest: str
    source_path: Optional[str]
    loaded_at: Optional[str]
    manifest_snapshot: Dict[str, Any]


class PolicyPackageRegistry:
    """In-memory registry of loaded policy packages.

    Keyed by (package_id, version). New loads of the same (id, version) with a
    different digest are rejected (immutability). A new version creates a new
    immutable entry. Historical records are retained.
    """

    def __init__(self) -> None:
        self._by_id_version: Dict[Tuple[str, str], LoadedPolicyPackage] = {}
        self._history: List[PolicyPackageRevisionRecord] = []

    def register(self, loaded: LoadedPolicyPackage) -> LoadedPolicyPackage:
        key = (loaded.manifest.package_id, loaded.manifest.version)
        existing = self._by_id_version.get(key)
        if existing is not None:
            if existing.identity_digest != loaded.identity_digest:
                raise PolicyPackageConflictError(
                    loaded.manifest.package_id, loaded.manifest.version
                )
            # identical digest → already registered, return existing
            return existing

        # assign revision = 1 + max existing revisions for this package_id
        prior = [r for r in self._history if r.package_id == loaded.manifest.package_id]
        next_rev = (max((r.revision for r in prior), default=0) + 1)
        loaded = loaded.model_copy(update={"revision": next_rev})

        self._by_id_version[key] = loaded
        self._history.append(
            PolicyPackageRevisionRecord(
                package_id=loaded.manifest.package_id,
                version=loaded.manifest.version,
                revision=loaded.revision,
                identity_digest=loaded.identity_digest,
                source_path=loaded.source_path,
                loaded_at=loaded.loaded_at,
                manifest_snapshot=loaded.manifest.model_dump(mode="json"),
            )
        )
        logger.info(
            "Registered policy package %s@%s rev=%s digest=%s",
            loaded.manifest.package_id,
            loaded.manifest.version,
            loaded.revision,
            loaded.identity_digest[:12],
        )
        return loaded

    def get(self, package_id: str, version: Optional[str] = None) -> LoadedPolicyPackage:
        if version is not None:
            key = (package_id, version)
            if key not in self._by_id_version:
                raise PolicyPackageNotFoundError(package_id, version)
            return self._by_id_version[key]
        # latest by revision
        candidates = [
            p for (pid, _), p in self._by_id_version.items() if pid == package_id
        ]
        if not candidates:
            raise PolicyPackageNotFoundError(package_id)
        return max(candidates, key=lambda p: p.revision)

    def history(self, package_id: str) -> List[PolicyPackageRevisionRecord]:
        return [r for r in self._history if r.package_id == package_id]

    def list_packages(self) -> List[LoadedPolicyPackage]:
        return list(self._by_id_version.values())


# Module-level default registry (process-scoped)
_default_registry: Optional[PolicyPackageRegistry] = None


def get_policy_package_registry() -> PolicyPackageRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = PolicyPackageRegistry()
    return _default_registry


def reset_policy_package_registry() -> None:
    """Test helper: clear the default registry."""
    global _default_registry
    _default_registry = PolicyPackageRegistry()


# ---------------------------------------------------------------------------
# Runtime consumption: authorization check
# ---------------------------------------------------------------------------

@dataclass
class AuthorizationRequest:
    operation: str
    actor_lane: str
    actor_class: Optional[str] = None
    provided_evidence_classes: Sequence[str] = field(default_factory=list)
    package_id: Optional[str] = None
    package_version: Optional[str] = None


@dataclass
class AuthorizationDecision:
    allowed: bool
    reason_code: str
    matched_predicate_id: Optional[str] = None
    package_identity_digest: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


def authorize(
    request: AuthorizationRequest,
    package: LoadedPolicyPackage,
) -> AuthorizationDecision:
    """Evaluate an authorization request against a loaded policy package.

    Fail-closed: if no matching rule exists, or evidence is insufficient, or
    lane is insufficient, deny.
    """
    if request.actor_lane not in CANONICAL_AUTHORITY_LANES:
        return AuthorizationDecision(
            allowed=False,
            reason_code="INVALID_ACTOR_LANE",
            details={"actor_lane": request.actor_lane},
        )

    matching = [
        r for r in package.manifest.rules if r.operation == request.operation
    ]
    if not matching:
        return AuthorizationDecision(
            allowed=False,
            reason_code="NO_MATCHING_RULE",
            package_identity_digest=package.identity_digest,
            details={"operation": request.operation},
        )

    # Prefer the highest-rank required lane rule that the actor can satisfy
    matching_sorted = sorted(
        matching, key=lambda r: _lane_rank(r.required_authority_lane), reverse=True
    )

    for rule in matching_sorted:
        if _lane_rank(request.actor_lane) < _lane_rank(rule.required_authority_lane):
            continue
        if rule.actor_class and request.actor_class and rule.actor_class != request.actor_class:
            continue

        required_ev = {
            ep.evidence_class
            for ep in rule.evidence_prerequisites
            if ep.required
        }
        provided = set(request.provided_evidence_classes)
        missing = required_ev - provided
        if missing:
            continue

        return AuthorizationDecision(
            allowed=True,
            reason_code="AUTHORIZED",
            matched_predicate_id=rule.predicate_id,
            package_identity_digest=package.identity_digest,
            details={
                "operation": request.operation,
                "actor_lane": request.actor_lane,
                "required_lane": rule.required_authority_lane,
            },
        )

    return AuthorizationDecision(
        allowed=False,
        reason_code="INSUFFICIENT_AUTHORITY_OR_EVIDENCE",
        package_identity_digest=package.identity_digest,
        details={
            "operation": request.operation,
            "actor_lane": request.actor_lane,
            "candidate_rules": [r.predicate_id for r in matching],
        },
    )


def authorize_via_registry(
    request: AuthorizationRequest,
    registry: Optional[PolicyPackageRegistry] = None,
) -> AuthorizationDecision:
    """Resolve package from registry and authorize."""
    reg = registry or get_policy_package_registry()
    if not request.package_id:
        return AuthorizationDecision(
            allowed=False,
            reason_code="PACKAGE_ID_REQUIRED",
            details={},
        )
    try:
        pkg = reg.get(request.package_id, request.package_version)
    except PolicyPackageNotFoundError as e:
        return AuthorizationDecision(
            allowed=False,
            reason_code=e.reason_code,
            details=e.details,
        )
    return authorize(request, pkg)


# ---------------------------------------------------------------------------
# Discovery helpers (compatibility with program packages)
# ---------------------------------------------------------------------------

def discover_policy_packages(roots: Sequence[Union[str, Path]]) -> List[LoadedPolicyPackage]:
    """Discover policy packages under program directories.

    Convention: <root>/<program_id>/policy/policy_package.yaml
                or <root>/<program_id>/policy/*.yaml
    """
    found: List[LoadedPolicyPackage] = []
    for root in roots:
        root_p = Path(root)
        if not root_p.is_dir():
            continue
        for prog_dir in sorted(root_p.iterdir()):
            if not prog_dir.is_dir():
                continue
            policy_dir = prog_dir / "policy"
            if not policy_dir.is_dir():
                continue
            for candidate in sorted(policy_dir.glob("*.yaml")) + sorted(policy_dir.glob("*.yml")) + sorted(policy_dir.glob("*.json")):
                try:
                    loaded = load_policy_package_from_path(candidate)
                    found.append(loaded)
                except PolicyPackageError as e:
                    logger.warning("Skipping invalid policy package %s: %s", candidate, e)
    return found


def load_and_register_from_program_root(
    programs_root: Union[str, Path],
    registry: Optional[PolicyPackageRegistry] = None,
) -> List[LoadedPolicyPackage]:
    """Discover and register all valid policy packages under a programs root."""
    reg = registry or get_policy_package_registry()
    loaded_list = discover_policy_packages([programs_root])
    registered: List[LoadedPolicyPackage] = []
    for lp in loaded_list:
        registered.append(reg.register(lp))
    return registered
