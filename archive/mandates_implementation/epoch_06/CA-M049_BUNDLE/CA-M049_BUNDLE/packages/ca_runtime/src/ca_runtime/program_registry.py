"""Program Package Discovery and Registry for Conscious Activation Engine (CAE).

Governed by Phase 2 Mandate M14 (TS-CAE-PROG-001, 22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md)
and CA-M049 / INV-REG-001 (Program Registry Immutability Requirement).

Provides strongly typed Program manifest loading, package integrity hashing,
four authority lane validation, flat passive skill verification, dependency checks,
fail-closed preflight inspection, and durable immutable registration of released
program packages (manifest + package digests pinned; same-version overwrite rejected).
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
import yaml

from ca_contracts import canonical_json_text, canonical_sha256

logger = logging.getLogger("ca_runtime.program_registry")

# SemVer 2.0.0 official regular expression
SEMVER_REGEX = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

CANONICAL_AUTHORITY_LANES: Set[str] = {"HUNTER", "ANALYST", "COMPOSER", "COMMANDER"}

# Statuses that are considered released / immutable under INV-REG-001.
IMMUTABLE_STATUSES: Set[str] = {"RELEASED", "ACTIVE"}


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class ProgramRegistryError(RuntimeError):
    """Base error for Program Registry and Package Discovery operations."""

    def __init__(self, message: str, *, reason_code: str = "PROGRAM_REGISTRY_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class ProgramNotFoundError(ProgramRegistryError):
    """Program ID was not found in the registry."""

    def __init__(self, program_id: str, version: Optional[str] = None):
        ver_str = f"@{version}" if version else ""
        super().__init__(
            f"Program '{program_id}{ver_str}' not found in registry",
            reason_code="PROGRAM_NOT_FOUND",
            details={"program_id": program_id, "version": version},
        )


class ProgramConflictError(ProgramRegistryError):
    """Program ID and version conflict with an existing registered program."""

    def __init__(self, program_id: str, version: str):
        super().__init__(
            f"Program '{program_id}' version '{version}' already registered",
            reason_code="PROGRAM_CONFLICT",
            details={"program_id": program_id, "version": version},
        )


class ProgramImmutabilityError(ProgramRegistryError):
    """Attempt to overwrite, patch, or mutate a released/immutable program package (INV-REG-001)."""

    def __init__(
        self,
        program_id: str,
        version: str,
        *,
        reason: str = "released package identity cannot be overwritten",
        existing_manifest_sha256: Optional[str] = None,
        existing_package_sha256: Optional[str] = None,
        attempted_manifest_sha256: Optional[str] = None,
        attempted_package_sha256: Optional[str] = None,
    ):
        super().__init__(
            f"INV-REG-001: Program '{program_id}' version '{version}' is immutable: {reason}",
            reason_code="PROGRAM_IMMUTABILITY_VIOLATION",
            details={
                "program_id": program_id,
                "version": version,
                "reason": reason,
                "existing_manifest_sha256": existing_manifest_sha256,
                "existing_package_sha256": existing_package_sha256,
                "attempted_manifest_sha256": attempted_manifest_sha256,
                "attempted_package_sha256": attempted_package_sha256,
            },
        )


class ProgramDigestMismatchError(ProgramRegistryError):
    """Stored/pinned digests do not match recomputed package or manifest bytes."""

    def __init__(
        self,
        program_id: str,
        version: str,
        *,
        field: str,
        expected: str,
        actual: str,
    ):
        super().__init__(
            f"Digest mismatch for '{program_id}@{version}' on {field}: "
            f"expected {expected[:16]}…, got {actual[:16]}…",
            reason_code="PROGRAM_DIGEST_MISMATCH",
            details={
                "program_id": program_id,
                "version": version,
                "field": field,
                "expected": expected,
                "actual": actual,
            },
        )


class ProgramManifestValidationError(ProgramRegistryError):
    """Program manifest failed schema or structural validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="MANIFEST_VALIDATION_ERROR", details=details)


class InvalidAuthorityLaneError(ProgramManifestValidationError):
    """Program declares an invalid, unknown, or collapsed authority lane."""

    def __init__(self, program_id: str, invalid_lanes: Sequence[str]):
        super().__init__(
            f"Program '{program_id}' declared invalid authority lanes: {list(invalid_lanes)}. "
            f"Permitted lanes are strictly: {sorted(CANONICAL_AUTHORITY_LANES)}",
            details={"program_id": program_id, "invalid_lanes": list(invalid_lanes)},
        )


class SkillNestingViolationError(ProgramManifestValidationError):
    """Skill package violates the flat, passive skill constitution rule."""

    def __init__(self, program_id: str, skill_name: str, reason: str):
        super().__init__(
            f"Program '{program_id}' skill '{skill_name}' violates passive/flat constitution: {reason}",
            details={"program_id": program_id, "skill_name": skill_name, "reason": reason},
        )


class MissingProgramDependencyError(ProgramRegistryError):
    """A required program dependency is missing or version-incompatible."""

    def __init__(self, program_id: str, missing_dependency: str, required_version: Optional[str] = None):
        req_str = f" ({required_version})" if required_version else ""
        super().__init__(
            f"Program '{program_id}' is missing required dependency: '{missing_dependency}{req_str}'",
            reason_code="MISSING_DEPENDENCY",
            details={"program_id": program_id, "missing_dependency": missing_dependency, "required_version": required_version},
        )


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class ProgramStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    RELEASED = "RELEASED"  # CA-M049 / INV-REG-001: immutable released identity
    DEPRECATED = "DEPRECATED"
    QUARANTINED = "QUARANTINED"


class SkillBinding(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    path: str = Field(..., description="Relative path within package to skill directory or SKILL.md")
    sha256: Optional[str] = Field(default=None, description="SHA-256 hash of SKILL.md")
    version: Optional[str] = Field(default="1.0.0")


class ProgramDependency(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    program_id: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    version_requirement: Optional[str] = Field(default=None, description="SemVer requirement e.g. ^1.0.0 or exact")
    sha256: Optional[str] = Field(default=None, description="Expected package SHA-256 hash")


class ProgramManifest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., pattern=r"^[a-z0-9_-]+$", min_length=2, max_length=128)
    version: str = Field(..., description="SemVer version string")
    status: ProgramStatus = Field(default=ProgramStatus.ACTIVE)
    purpose: str = Field(..., min_length=5)
    operator_entrypoint: Optional[str] = Field(default=None)

    inputs: List[str] = Field(default_factory=list)
    preconditions: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)

    harness: Optional[str] = Field(default=None)
    state_machine: Optional[str] = Field(default=None)

    lanes: List[str] = Field(default_factory=list, description="Must be a subset of HUNTER, ANALYST, COMPOSER, COMMANDER")
    agents: List[Any] = Field(default_factory=list, description="Agent names, versioned strings (e.g. Agent@1.0.0), or dicts")
    subagents: List[str] = Field(default_factory=list)
    skills: List[SkillBinding] = Field(default_factory=list)
    operations: List[str] = Field(default_factory=list)

    tools: List[str] = Field(default_factory=list)
    connections: List[str] = Field(default_factory=list)
    hooks: List[str] = Field(default_factory=list)
    extensions: List[str] = Field(default_factory=list)
    evals: List[str] = Field(default_factory=list)
    operator_gates: List[str] = Field(default_factory=list)
    recovery: List[str] = Field(default_factory=list)
    receipts: List[str] = Field(default_factory=list)
    dependencies: List[ProgramDependency] = Field(default_factory=list)

    @field_validator("version")
    @classmethod
    def validate_semver(cls, v: str) -> str:
        if not SEMVER_REGEX.match(v):
            raise ValueError(f"Program version '{v}' is not a valid SemVer 2.0.0 string")
        return v

    @field_validator("lanes")
    @classmethod
    def validate_authority_lanes(cls, lanes: List[str]) -> List[str]:
        invalid = [lane for lane in lanes if lane not in CANONICAL_AUTHORITY_LANES]
        if invalid:
            raise ValueError(
                f"Invalid authority lanes: {invalid}. Permitted: {sorted(CANONICAL_AUTHORITY_LANES)}"
            )
        return lanes

    def get_agent_references(self) -> List[Tuple[str, Optional[str]]]:
        """Extracts (agent_id, version_or_none) for all declared agents."""
        refs: List[Tuple[str, Optional[str]]] = []
        for a in self.agents:
            if isinstance(a, str):
                if "@" in a:
                    aid, aver = a.split("@", 1)
                    refs.append((aid.strip(), aver.strip()))
                else:
                    refs.append((a.strip(), None))
            elif isinstance(a, dict):
                aid = a.get("agent_id", a.get("name", ""))
                aver = a.get("version", a.get("version_requirement", None))
                refs.append((str(aid).strip(), str(aver).strip() if aver else None))
        return refs

    def validate_agent_bindings(self, agent_resolver: Optional[Any] = None) -> Dict[str, Any]:
        """Validates all referenced agents against the canonical AgentRegistry.
        
        Enforces:
        1. Referenced agent exists in registry.
        2. Referenced agent is in APPROVED or ACTIVE lifecycle state.
        3. Referenced agent's Authority Lane is included in the program's declared lanes.
        """
        from ca_runtime.agent_registry import (
            AgentLifecycleState,
            AgentNotFoundError,
            AgentLifecycleViolationError,
            AgentLaneMismatchError,
            get_agent_resolver,
        )

        resolver = agent_resolver or get_agent_resolver()
        validated_agents: Dict[str, Any] = {}

        for aid, aver in self.get_agent_references():
            if not aid:
                continue
            agent_def = resolver.resolve(aid, version=aver, min_lifecycle=AgentLifecycleState.APPROVED)
            if agent_def.authority_lane.value not in self.lanes:
                raise AgentLaneMismatchError(
                    agent_def.agent_id,
                    agent_def.authority_lane.value,
                    f"Program declared lanes: {self.lanes}",
                )
            validated_agents[f"{aid}@{agent_def.version}"] = agent_def

        return validated_agents

    def with_status(self, status: ProgramStatus) -> "ProgramManifest":
        """Return a new frozen manifest with updated status (does not mutate self)."""
        data = self.model_dump()
        data["status"] = status
        return ProgramManifest.model_validate(data)


class ProgramPackage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    program_id: str
    version: str
    package_root: str
    manifest: ProgramManifest
    manifest_sha256: str
    package_sha256: str
    skills_inventory: Dict[str, str] = Field(default_factory=dict, description="skill_name -> file_sha256")
    discovered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def is_immutable(self) -> bool:
        """True when this package identity is under INV-REG-001 protection."""
        return self.manifest.status.value in IMMUTABLE_STATUSES

    def with_status(self, status: ProgramStatus) -> "ProgramPackage":
        """Return a new frozen package with updated manifest status (pins unchanged)."""
        new_manifest = self.manifest.with_status(status)
        return ProgramPackage(
            program_id=self.program_id,
            version=self.version,
            package_root=self.package_root,
            manifest=new_manifest,
            manifest_sha256=self.manifest_sha256,
            package_sha256=self.package_sha256,
            skills_inventory=dict(self.skills_inventory),
            discovered_at=self.discovered_at,
        )

    def pinned_digests(self) -> Mapping[str, str]:
        """Return a read-only view of the digests bound to this package identity."""
        return MappingProxyType({
            "manifest_sha256": self.manifest_sha256,
            "package_sha256": self.package_sha256,
        })


class ProgramPreflightResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    program_id: str
    version: str
    eligible: bool
    workspace_id: str
    authority_lane_checks: Dict[str, bool]
    missing_dependencies: List[str] = Field(default_factory=list)
    missing_preconditions: List[str] = Field(default_factory=list)
    unverified_capabilities: List[str] = Field(default_factory=list)
    issues: List[str] = Field(default_factory=list)
    preflight_digest: str
    # CA-M049: digests observed at preflight for later execution pinning
    pinned_manifest_sha256: Optional[str] = None
    pinned_package_sha256: Optional[str] = None


# ---------------------------------------------------------------------------
# Program Package Discovery & Registry Service
# ---------------------------------------------------------------------------

def compute_file_sha256(file_path: Path) -> str:
    """Computes the SHA-256 hex digest of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_package_composite_sha256(package_root: Path) -> Tuple[str, Dict[str, str]]:
    """Recursively computes a composite deterministic SHA-256 hash across all package files.
    
    Returns (package_sha256, relative_file_hashes).
    """
    file_hashes: Dict[str, str] = {}
    
    # Sort files deterministically by relative POSIX path
    for file_path in sorted(package_root.rglob("*")):
        if file_path.is_file():
            # Skip hidden files or caches
            if any(part.startswith(".") or part == "__pycache__" for part in file_path.parts):
                continue
            rel_path = file_path.relative_to(package_root).as_posix()
            file_hashes[rel_path] = compute_file_sha256(file_path)

    composite_hasher = hashlib.sha256()
    for path, digest in sorted(file_hashes.items()):
        composite_hasher.update(f"{path}:{digest}\n".encode("utf-8"))
        
    return composite_hasher.hexdigest(), file_hashes


class ProgramRegistry:
    """In-memory and filesystem-backed Registry for governed CAE Program Packages."""

    def __init__(self, discovery_roots: Optional[Sequence[Path]] = None):
        self._discovery_roots: List[Path] = list(discovery_roots or [])
        # Keyed by (program_id, version) and secondary index by program_id (pointing to latest)
        self._programs_by_version: Dict[Tuple[str, str], ProgramPackage] = {}
        self._programs_latest: Dict[str, ProgramPackage] = {}
        self._frozen: bool = False

    @property
    def discovery_roots(self) -> Tuple[Path, ...]:
        return tuple(self._discovery_roots)

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        """Make the registry accept no further registrations (INV-REG-001 seal)."""
        self._frozen = True
        logger.info("ProgramRegistry frozen (INV-REG-001 seal)")

    def add_discovery_root(self, root: Path) -> None:
        if self._frozen:
            raise ProgramImmutabilityError(
                "*", "*", reason="registry is frozen; discovery roots cannot be modified"
            )
        if root not in self._discovery_roots:
            self._discovery_roots.append(root)

    def parse_manifest_file(self, manifest_path: Path) -> Tuple[ProgramManifest, str]:
        """Parses and validates a program_manifest.yaml or program_manifest.json file."""
        if not manifest_path.exists():
            raise ProgramManifestValidationError(f"Manifest file not found: {manifest_path}")

        try:
            content_bytes = manifest_path.read_bytes()
            manifest_sha256 = hashlib.sha256(content_bytes).hexdigest()

            if manifest_path.suffix.lower() in (".yaml", ".yml"):
                raw_data = yaml.safe_load(content_bytes.decode("utf-8"))
            elif manifest_path.suffix.lower() == ".json":
                raw_data = json.loads(content_bytes.decode("utf-8"))
            else:
                raise ProgramManifestValidationError(f"Unsupported manifest format: {manifest_path.name}")

            if not isinstance(raw_data, dict):
                raise ProgramManifestValidationError("Manifest root must be an object")

            # Support nested 'program' key or flat manifest
            program_data = raw_data.get("program", raw_data)
            manifest = ProgramManifest.model_validate(program_data)
            return manifest, manifest_sha256

        except Exception as e:
            if isinstance(e, ProgramManifestValidationError):
                raise
            raise ProgramManifestValidationError(f"Failed to parse manifest at {manifest_path}: {e}") from e

    def inspect_and_validate_package(self, package_root: Path) -> ProgramPackage:
        """Inspects a package directory, validates manifests, skills, and produces a ProgramPackage."""
        if not package_root.is_dir():
            raise ProgramManifestValidationError(f"Package root is not a directory: {package_root}")

        # Locate manifest
        manifest_candidates = [
            package_root / "program_manifest.yaml",
            package_root / "program_manifest.yml",
            package_root / "program_manifest.json",
        ]
        manifest_path = next((p for p in manifest_candidates if p.exists()), None)
        if not manifest_path:
            raise ProgramManifestValidationError(
                f"No program_manifest.(yaml|json) found in package root: {package_root}"
            )

        manifest, manifest_sha256 = self.parse_manifest_file(manifest_path)
        package_sha256, file_hashes = compute_package_composite_sha256(package_root)

        # Validate Flat Passive Skills
        skills_inventory: Dict[str, str] = {}
        for skill_binding in manifest.skills:
            skill_path = package_root / skill_binding.path
            if not skill_path.exists():
                raise SkillNestingViolationError(
                    manifest.id, skill_binding.name, f"Skill file does not exist at {skill_binding.path}"
                )

            # Check if it's a directory or SKILL.md
            if skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if not skill_md.exists():
                    raise SkillNestingViolationError(
                        manifest.id, skill_binding.name, f"SKILL.md missing in directory {skill_binding.path}"
                    )
                # Check for nested subagents or skills inside this skill directory
                if (skill_path / "skills").exists() or (skill_path / "subagents").exists():
                    raise SkillNestingViolationError(
                        manifest.id, skill_binding.name, "Skill directory contains nested skills or subagents (forbidden)"
                    )
                skill_file_hash = compute_file_sha256(skill_md)
            else:
                skill_file_hash = compute_file_sha256(skill_path)

            skills_inventory[skill_binding.name] = skill_file_hash

        package = ProgramPackage(
            program_id=manifest.id,
            version=manifest.version,
            package_root=str(package_root.resolve()),
            manifest=manifest,
            manifest_sha256=manifest_sha256,
            package_sha256=package_sha256,
            skills_inventory=skills_inventory,
        )
        return package

    def _assert_not_frozen(self, operation: str) -> None:
        if self._frozen:
            raise ProgramImmutabilityError(
                "*", "*", reason=f"registry is frozen; refused operation: {operation}"
            )

    def register(self, package: ProgramPackage, allow_overwrite: bool = False) -> None:
        """Registers an inspected program package under INV-REG-001 rules.

        Rules:
        1. If registry is frozen → always reject.
        2. If (program_id, version) already exists and is immutable (RELEASED/ACTIVE)
           → always reject (ProgramImmutabilityError), even with allow_overwrite=True.
        3. If existing is mutable and allow_overwrite=False → ProgramConflictError.
        4. New identity always accepted.
        """
        self._assert_not_frozen("register")

        key = (package.program_id, package.version)
        if key in self._programs_by_version:
            existing = self._programs_by_version[key]
            if existing.is_immutable():
                raise ProgramImmutabilityError(
                    package.program_id,
                    package.version,
                    reason=(
                        f"existing status is {existing.manifest.status.value}; "
                        "released/active package identity cannot be overwritten "
                        "(use a new SemVer version for promotion)"
                    ),
                    existing_manifest_sha256=existing.manifest_sha256,
                    existing_package_sha256=existing.package_sha256,
                    attempted_manifest_sha256=package.manifest_sha256,
                    attempted_package_sha256=package.package_sha256,
                )
            if not allow_overwrite:
                raise ProgramConflictError(package.program_id, package.version)

        self._programs_by_version[key] = package
        self._programs_latest[package.program_id] = package
        logger.info(
            "Registered program: %s v%s status=%s (manifest=%s package=%s)",
            package.program_id,
            package.version,
            package.manifest.status.value,
            package.manifest_sha256[:12],
            package.package_sha256[:12],
        )

    def release(self, program_id: str, version: Optional[str] = None) -> ProgramPackage:
        """Promote a registered package to RELEASED status (immutable), preserving pins."""
        self._assert_not_frozen("release")
        pkg = self.get_program(program_id, version)
        if pkg.manifest.status == ProgramStatus.RELEASED:
            return pkg
        if pkg.manifest.status == ProgramStatus.QUARANTINED:
            raise ProgramImmutabilityError(
                program_id,
                pkg.version,
                reason="QUARANTINED packages cannot be promoted to RELEASED",
                existing_manifest_sha256=pkg.manifest_sha256,
                existing_package_sha256=pkg.package_sha256,
            )
        released = pkg.with_status(ProgramStatus.RELEASED)
        key = (released.program_id, released.version)
        self._programs_by_version[key] = released
        self._programs_latest[released.program_id] = released
        logger.info(
            "Released program: %s v%s (pinned manifest=%s package=%s)",
            released.program_id,
            released.version,
            released.manifest_sha256[:12],
            released.package_sha256[:12],
        )
        return released

    def verify_package_integrity(
        self,
        program_id: str,
        version: Optional[str] = None,
        *,
        recompute_from_disk: bool = True,
    ) -> ProgramPackage:
        """Verify pinned digests match package on disk; raise ProgramDigestMismatchError on mismatch."""
        pkg = self.get_program(program_id, version)
        if not recompute_from_disk:
            return pkg
        root = Path(pkg.package_root)
        if not root.is_dir():
            raise ProgramDigestMismatchError(
                pkg.program_id, pkg.version,
                field="package_root", expected=pkg.package_root, actual=f"<missing:{root}>",
            )
        current = self.inspect_and_validate_package(root)
        if current.manifest_sha256 != pkg.manifest_sha256:
            raise ProgramDigestMismatchError(
                pkg.program_id, pkg.version,
                field="manifest_sha256", expected=pkg.manifest_sha256, actual=current.manifest_sha256,
            )
        if current.package_sha256 != pkg.package_sha256:
            raise ProgramDigestMismatchError(
                pkg.program_id, pkg.version,
                field="package_sha256", expected=pkg.package_sha256, actual=current.package_sha256,
            )
        return pkg

    def get_pinned_digests(self, program_id: str, version: Optional[str] = None) -> Mapping[str, str]:
        """Return the immutable digest pins for a registered program identity."""
        return self.get_program(program_id, version).pinned_digests()

    def discover(self, search_paths: Optional[Sequence[Path]] = None) -> List[ProgramPackage]:
        """Discovers and registers packages; will not overwrite RELEASED/ACTIVE with different digests."""
        self._assert_not_frozen("discover")
        roots = list(search_paths or self._discovery_roots)
        discovered: List[ProgramPackage] = []

        for root in roots:
            if not root.exists() or not root.is_dir():
                logger.warning("Discovery root does not exist: %s", root)
                continue

            # Look for subdirectories containing a program_manifest.* or root itself
            candidates: List[Path] = []
            if any((root / f"program_manifest.{ext}").exists() for ext in ("yaml", "yml", "json")):
                candidates.append(root)

            for child in sorted(root.iterdir()):
                if child.is_dir():
                    if any((child / f"program_manifest.{ext}").exists() for ext in ("yaml", "yml", "json")):
                        candidates.append(child)

            for candidate in candidates:
                try:
                    pkg = self.inspect_and_validate_package(candidate)
                    key = (pkg.program_id, pkg.version)
                    if key in self._programs_by_version and self._programs_by_version[key].is_immutable():
                        existing = self._programs_by_version[key]
                        if (
                            existing.manifest_sha256 != pkg.manifest_sha256
                            or existing.package_sha256 != pkg.package_sha256
                        ):
                            logger.error(
                                "INV-REG-001: refusing to overwrite immutable %s@%s during discovery",
                                pkg.program_id, pkg.version,
                            )
                            continue
                        discovered.append(existing)
                        continue
                    self.register(pkg, allow_overwrite=True)
                    discovered.append(pkg)
                except ProgramImmutabilityError as e:
                    logger.error("Failed to load program package at %s (immutability): %s", candidate, e)
                except Exception as e:
                    logger.error("Failed to load program package at %s: %s", candidate, e)

        return discovered

    discover_and_register_all = discover

    def list_programs(self, status: Optional[ProgramStatus] = None) -> List[ProgramPackage]:
        """Lists all registered programs (latest version per program ID), optionally filtered by status."""
        results = list(self._programs_latest.values())
        if status:
            results = [p for p in results if p.manifest.status == status]
        return sorted(results, key=lambda p: p.program_id)

    def get_program(self, program_id: str, version: Optional[str] = None) -> ProgramPackage:
        """Retrieves a registered program by ID and optional SemVer version."""
        if version:
            key = (program_id, version)
            if key not in self._programs_by_version:
                raise ProgramNotFoundError(program_id, version)
            return self._programs_by_version[key]
        else:
            if program_id not in self._programs_latest:
                raise ProgramNotFoundError(program_id)
            return self._programs_latest[program_id]

    def inspect_program(self, program_id: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Returns detailed inspection metadata for a program package."""
        pkg = self.get_program(program_id, version)
        return {
            "program_id": pkg.program_id,
            "version": pkg.version,
            "status": pkg.manifest.status.value,
            "purpose": pkg.manifest.purpose,
            "package_root": pkg.package_root,
            "manifest_sha256": pkg.manifest_sha256,
            "package_sha256": pkg.package_sha256,
            "immutable": pkg.is_immutable(),
            "authority_lanes": pkg.manifest.lanes,
            "skills": [
                {"name": s.name, "path": s.path, "sha256": pkg.skills_inventory.get(s.name)}
                for s in pkg.manifest.skills
            ],
            "operations": pkg.manifest.operations,
            "inputs": pkg.manifest.inputs,
            "preconditions": pkg.manifest.preconditions,
            "outputs": pkg.manifest.outputs,
            "artifacts": pkg.manifest.artifacts,
            "dependencies": [d.model_dump() for d in pkg.manifest.dependencies],
            "hooks": pkg.manifest.hooks,
            "operator_gates": pkg.manifest.operator_gates,
            "recovery": pkg.manifest.recovery,
            "discovered_at": pkg.discovered_at,
        }

    def preflight(
        self,
        program_id: str,
        workspace_id: str,
        context_refs: Optional[Sequence[str]] = None,
        version: Optional[str] = None,
        *,
        require_integrity: bool = False,
    ) -> ProgramPreflightResult:
        """Performs a fail-closed preflight check on a program package for an operator session.
        
        Validates:
        1. Workspace ID is valid.
        2. Program package exists and is ACTIVE.
        3. Authority lanes are valid and non-empty.
        4. Declared dependencies exist in registry.
        5. Required preconditions are accounted for in context_refs.
        """
        pkg = self.get_program(program_id, version)
        context_set = set(context_refs or [])
        issues: List[str] = []
        missing_deps: List[str] = []
        missing_preconditions: List[str] = []
        lane_checks: Dict[str, bool] = {}

        # 1. Workspace check
        if not workspace_id or not workspace_id.strip():
            issues.append("Workspace ID is required for program execution")

        # 2. Program status check
        if pkg.manifest.status == ProgramStatus.QUARANTINED:
            issues.append(f"Program '{program_id}' is QUARANTINED and cannot be executed")
        elif pkg.manifest.status == ProgramStatus.DEPRECATED:
            issues.append(f"Program '{program_id}' is DEPRECATED")

        # 3. Authority lanes check
        if not pkg.manifest.lanes:
            issues.append("Program declares no authority lanes")
        for lane in pkg.manifest.lanes:
            valid = lane in CANONICAL_AUTHORITY_LANES
            lane_checks[lane] = valid
            if not valid:
                issues.append(f"Invalid authority lane: {lane}")

        # 4. Dependency resolution check
        for dep in pkg.manifest.dependencies:
            if dep.program_id not in self._programs_latest:
                missing_deps.append(dep.program_id)
                issues.append(f"Missing dependency: {dep.program_id}")
            elif dep.version_requirement:
                dep_pkg = self._programs_latest[dep.program_id]
                if dep.version_requirement != dep_pkg.version and not dep_pkg.version.startswith(dep.version_requirement.lstrip("^~")):
                    missing_deps.append(f"{dep.program_id}@{dep.version_requirement}")
                    issues.append(
                        f"Incompatible dependency version for {dep.program_id}: requires {dep.version_requirement}, found {dep_pkg.version}"
                    )

        # 5. Preconditions check
        for pre in pkg.manifest.preconditions:
            if pre not in context_set:
                missing_preconditions.append(pre)
                issues.append(f"Unsatisfied precondition: {pre}")

        # 6. Optional integrity check (CA-M049)
        if require_integrity:
            try:
                self.verify_package_integrity(program_id, version or pkg.version, recompute_from_disk=True)
            except ProgramDigestMismatchError as e:
                issues.append(str(e))
            except Exception as e:
                issues.append(f"Integrity verification failed: {e}")

        eligible = len(issues) == 0

        preflight_payload = {
            "program_id": pkg.program_id,
            "version": pkg.version,
            "workspace_id": workspace_id,
            "package_sha256": pkg.package_sha256,
            "manifest_sha256": pkg.manifest_sha256,
            "eligible": eligible,
            "issues": issues,
        }
        preflight_digest = canonical_sha256(preflight_payload)

        return ProgramPreflightResult(
            program_id=pkg.program_id,
            version=pkg.version,
            eligible=eligible,
            workspace_id=workspace_id,
            authority_lane_checks=lane_checks,
            missing_dependencies=missing_deps,
            missing_preconditions=missing_preconditions,
            unverified_capabilities=[],
            issues=issues,
            preflight_digest=preflight_digest,
            pinned_manifest_sha256=pkg.manifest_sha256,
            pinned_package_sha256=pkg.package_sha256,
        )


# Global default program registry instance
_default_registry: Optional[ProgramRegistry] = None


def get_program_registry(discovery_roots: Optional[Sequence[Path]] = None) -> ProgramRegistry:
    """Returns or initializes the singleton default ProgramRegistry."""
    global _default_registry
    if _default_registry is None:
        default_root = Path("programs").resolve()
        roots = list(discovery_roots or [])
        if default_root.exists() and default_root not in roots:
            roots.append(default_root)
        _default_registry = ProgramRegistry(discovery_roots=roots)
        if roots:
            _default_registry.discover()
    return _default_registry
