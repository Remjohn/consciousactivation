"""Canonical Agent Constitution, Schema, and Registry Engine for CAE.

Governed by:
- Phase 5 Mandate M49 (01_AGENT_EXECUTION/M49_canonical_agent_constitution_registry.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Enforces:
1. Agent as a First-Class, Independently Addressable Canonical Object.
2. Strict Four Non-Negotiable Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
3. Passive Flat Skills: Skills referenced by agents must be flat and passive (no skill-to-skill invocation).
4. Explicit Capability Projections: No ambient database mutations or un-projected permissions.
5. Deterministic Resolution and Identity Collision Defense:
   - Same (agent_id, version) resolves idempotently with identical content_sha256.
   - Attempting to register a diverging body under an existing (agent_id, version) raises AgentIdentityCollisionError.
6. Fail-Closed Lifecycle Gating:
   - DRAFT or QUARANTINED agents are rejected from production resolution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator
import yaml

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.context_capsule import AccessMode, CapabilityScope
from ca_runtime.pi_adapter import AuthorityLane

logger = logging.getLogger("ca_runtime.agent_registry")

# SemVer 2.0.0 regular expression
SEMVER_REGEX = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

# Agent ID naming pattern: PascalCase or snake_case with Agent suffix / prefix allowed
AGENT_ID_REGEX = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{2,127}$")


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class AgentRegistryError(RuntimeError):
    """Base exception for Agent Registry and Resolution operations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "AGENT_REGISTRY_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class AgentNotFoundError(AgentRegistryError):
    """Raised when an agent ID or version was not found in the registry."""

    def __init__(self, agent_id: str, version: Optional[str] = None):
        ver_str = f"@{version}" if version else ""
        super().__init__(
            f"Agent '{agent_id}{ver_str}' not found in registry",
            reason_code="AGENT_NOT_FOUND",
            details={"agent_id": agent_id, "version": version},
        )


class AgentIdentityCollisionError(AgentRegistryError):
    """Raised when registering an agent definition whose body conflicts with an existing version."""

    def __init__(self, agent_id: str, version: str, existing_sha256: str, attempted_sha256: str):
        super().__init__(
            f"IDENTITY_COLLISION: Agent '{agent_id}@{version}' already registered with content hash "
            f"'{existing_sha256}', but new definition has conflicting hash '{attempted_sha256}'",
            reason_code="AGENT_IDENTITY_COLLISION",
            details={
                "agent_id": agent_id,
                "version": version,
                "existing_sha256": existing_sha256,
                "attempted_sha256": attempted_sha256,
            },
        )


class AgentLifecycleViolationError(AgentRegistryError):
    """Raised when an agent's lifecycle state fails a required maturity or execution gate."""

    def __init__(self, agent_id: str, version: str, state: str, required_state: str = "APPROVED or ACTIVE"):
        super().__init__(
            f"LIFECYCLE_VIOLATION: Agent '{agent_id}@{version}' is in '{state}' state; "
            f"requires '{required_state}' for resolution",
            reason_code="AGENT_LIFECYCLE_VIOLATION",
            details={"agent_id": agent_id, "version": version, "state": state, "required_state": required_state},
        )


class AgentLaneMismatchError(AgentRegistryError):
    """Raised when an agent is bound or executed in an unassigned Authority Lane."""

    def __init__(self, agent_id: str, assigned_lane: str, expected_lane: str):
        super().__init__(
            f"LANE_MISMATCH: Agent '{agent_id}' is assigned to '{assigned_lane}' lane, "
            f"cannot be bound to '{expected_lane}' lane",
            reason_code="AGENT_LANE_MISMATCH",
            details={"agent_id": agent_id, "assigned_lane": assigned_lane, "expected_lane": expected_lane},
        )


class AgentCapabilityViolationError(AgentRegistryError):
    """Raised when an agent definition declares capabilities that violate its Authority Lane."""

    def __init__(self, agent_id: str, lane: str, capability_scope: str, reason: str):
        super().__init__(
            f"CAPABILITY_VIOLATION: Agent '{agent_id}' in lane '{lane}' violates capability rules: "
            f"scope '{capability_scope}' - {reason}",
            reason_code="AGENT_CAPABILITY_VIOLATION",
            details={"agent_id": agent_id, "lane": lane, "capability_scope": capability_scope, "reason": reason},
        )


class AgentQuarantinedError(AgentRegistryError):
    """Raised when attempting to resolve or execute a quarantined Agent."""

    def __init__(self, agent_id: str, version: str, reason: str = ""):
        super().__init__(
            f"AGENT_QUARANTINED: Agent '{agent_id}@{version}' is quarantined: {reason}",
            reason_code="AGENT_QUARANTINED",
            details={"agent_id": agent_id, "version": version, "quarantine_reason": reason},
        )


class AgentManifestValidationError(AgentRegistryError):
    """Raised when an agent manifest YAML or schema fails validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="MANIFEST_VALIDATION_ERROR", details=details)


# ---------------------------------------------------------------------------
# Enums and Domain Models
# ---------------------------------------------------------------------------

class AgentLifecycleState(str, Enum):
    """Governance lifecycle states for Canonical Agents."""
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    QUARANTINED = "QUARANTINED"
    RETIRED = "RETIRED"


PRODUCTION_RESOLVABLE_STATES: Set[AgentLifecycleState] = {
    AgentLifecycleState.APPROVED,
    AgentLifecycleState.ACTIVE,
}


class AgentModelPolicy(BaseModel):
    """Model policy governing temperature, context budget, and fallback models."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    preferred_model: str = Field(default="gemini-2.5-pro", min_length=2)
    temperature: Any = Field(default=0.2)
    temperature_bps: Optional[int] = Field(default=None)
    token_budget: int = Field(default=128_000, gt=0)
    fallback_models: List[str] = Field(default_factory=list)
    timeout_seconds: Any = Field(default=60)
    allowed_tool_choice: str = Field(default="AUTO")

    def canonical_dict(self) -> Dict[str, Any]:
        temp_val = float(self.temperature) if self.temperature is not None else 0.2
        temp_bps = self.temperature_bps if self.temperature_bps is not None else int(round(temp_val * 10000))
        timeout_int = int(round(float(self.timeout_seconds))) if self.timeout_seconds is not None else 60
        return {
            "preferred_model": self.preferred_model,
            "temperature_bps": temp_bps,
            "token_budget": self.token_budget,
            "fallback_models": sorted(self.fallback_models),
            "timeout_seconds": timeout_int,
            "allowed_tool_choice": self.allowed_tool_choice,
        }


class AgentPromptReference(BaseModel):
    """Governance references to prompt instructions, CAE.md root, and prompt hash."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    instructions_ref: str = Field(default="instructions.md", description="Relative path to instructions.md")
    cae_md_ref: str = Field(default="CAE.md", description="Relative path to governing CAE.md")
    system_prompt_template: Optional[str] = Field(default=None)
    prompt_sha256: Optional[str] = Field(default=None, description="SHA-256 hash of instructions file")


class SkillBindingRef(BaseModel):
    """Reference to a passive, flat Canonical Skill bound to an Agent."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    version: str = Field(default="1.0.0")
    sha256: Optional[str] = Field(default=None)
    required_maturity: str = Field(default="STABLE")
    path: Optional[str] = Field(default=None)


class AgentCapabilityGrant(BaseModel):
    """Explicit capability grant conforming to the Capability Security Matrix."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    scope: CapabilityScope
    mode: AccessMode
    target: str
    approval_required: bool = False


class AgentOutputContract(BaseModel):
    """Declared typed output contract for an Agent."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_id: str = Field(..., min_length=2)
    schema_ref: Optional[str] = Field(default=None)
    output_type: str = Field(default="JSON")
    description: Optional[str] = Field(default=None)


class SubagentPolicy(BaseModel):
    """Subagent delegation policy enforcing same-lane containment."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    allow_subagents: bool = Field(default=False)
    allowed_subagent_ids: List[str] = Field(default_factory=list)
    max_subagents: int = Field(default=0, ge=0)
    enforce_same_lane: bool = Field(default=True)


class AgentObservabilityPolicy(BaseModel):
    """Observability, logging, and receipt emission configuration."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    trace_level: str = Field(default="INFO")
    log_retention_days: int = Field(default=30, ge=1)
    include_budget_report: bool = Field(default=True)
    emit_receipts: bool = Field(default=True)


class AgentBindingRef(BaseModel):
    """Structured reference used by Programs or Sessions to bind a registered Agent."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    agent_id: str = Field(..., pattern=r"^[A-Za-z][A-Za-z0-9_-]{2,127}$")
    version_requirement: Optional[str] = Field(default=None, description="SemVer requirement e.g. 1.0.0 or >=1.0.0")
    sha256: Optional[str] = Field(default=None, description="Expected content SHA-256 hash")
    expected_lane: Optional[AuthorityLane] = Field(default=None)


# ---------------------------------------------------------------------------
# Canonical Agent Definition Model
# ---------------------------------------------------------------------------

class AgentDefinition(BaseModel):
    """Immutable, versioned canonical Agent specification.
    
    Represents an independently addressable reasoning entity on the Global Canonical Plane.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    agent_id: str = Field(..., min_length=2, max_length=128)
    version: str = Field(..., description="SemVer version string e.g. 1.0.0")
    name: str = Field(..., min_length=2)
    purpose: str = Field(..., min_length=5)
    authority_lane: AuthorityLane = Field(..., description="HUNTER, ANALYST, COMPOSER, COMMANDER")
    lifecycle_state: AgentLifecycleState = Field(default=AgentLifecycleState.APPROVED)
    model_policy: AgentModelPolicy = Field(default_factory=AgentModelPolicy)
    prompt_reference: AgentPromptReference = Field(default_factory=AgentPromptReference)
    cae_md_root: Optional[str] = Field(default=None)
    skills: List[SkillBindingRef] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    capabilities: List[AgentCapabilityGrant] = Field(default_factory=list)
    hooks: List[str] = Field(default_factory=list)
    harness_refs: List[str] = Field(default_factory=list)
    output_contract: Optional[AgentOutputContract] = Field(default=None)
    subagent_policy: SubagentPolicy = Field(default_factory=SubagentPolicy)
    observability_policy: AgentObservabilityPolicy = Field(default_factory=AgentObservabilityPolicy)
    content_sha256: str = Field(default="", description="Cryptographic SHA-256 of canonical definition")
    created_at: str = Field(default_factory=utc_now_rfc3339)
    updated_at: str = Field(default_factory=utc_now_rfc3339)

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        if not AGENT_ID_REGEX.match(v):
            raise ValueError(f"agent_id '{v}' must match pattern {AGENT_ID_REGEX.pattern}")
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        if not SEMVER_REGEX.match(v):
            raise ValueError(f"version '{v}' must be a valid SemVer 2.0.0 string")
        return v

    def canonical_dict(self) -> Dict[str, Any]:
        """Produce canonical, deterministic dictionary for cryptographic hashing."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "name": self.name,
            "purpose": self.purpose,
            "authority_lane": self.authority_lane.value,
            "lifecycle_state": self.lifecycle_state.value,
            "model_policy": self.model_policy.canonical_dict(),
            "prompt_reference": self.prompt_reference.model_dump(),
            "cae_md_root": self.cae_md_root,
            "skills": [s.model_dump() for s in sorted(self.skills, key=lambda x: x.name)],
            "tools": sorted(self.tools),
            "capabilities": [
                {
                    "scope": c.scope.value,
                    "mode": c.mode.value,
                    "target": c.target,
                    "approval_required": c.approval_required,
                }
                for c in sorted(self.capabilities, key=lambda x: (x.scope.value, x.target))
            ],
            "hooks": sorted(self.hooks),
            "harness_refs": sorted(self.harness_refs),
            "output_contract": self.output_contract.model_dump() if self.output_contract else None,
            "subagent_policy": self.subagent_policy.model_dump(),
            "observability_policy": self.observability_policy.model_dump(),
        }

    def compute_content_sha256(self) -> str:
        """Compute SHA-256 digest of the canonical definition payload."""
        payload = self.canonical_dict()
        return canonical_sha256(canonical_json_text(payload))

    def validate_invariants(self) -> None:
        """Enforce constitutional invariants and anti-reward hacking checks.
        
        Checks:
        1. Authority Lane must be one of the four non-negotiable lanes.
        2. Hunter / Analyst / Composer lanes cannot hold database mutation grants or operator gate grants.
        3. Skill names must not contain nested or recursive markers.
        4. Subagent policy must enforce same-lane containment.
        """
        # 1. Authority Lane Check
        if not isinstance(self.authority_lane, AuthorityLane):
            raise AgentLaneMismatchError(self.agent_id, str(self.authority_lane), "VALID_LANE")

        # 2. Capability Escalation / Mutation Boundary Check
        if self.authority_lane != AuthorityLane.COMMANDER:
            for cap in self.capabilities:
                if cap.mode in (AccessMode.MUTATION_OPERATION, AccessMode.WRITE_ONLY):
                    raise AgentCapabilityViolationError(
                        self.agent_id,
                        self.authority_lane.value,
                        cap.scope.value,
                        f"Non-COMMANDER lane '{self.authority_lane.value}' is forbidden from holding "
                        f"mutation access mode '{cap.mode.value}' on target '{cap.target}'",
                    )
                if cap.scope == CapabilityScope.CAE_TYPED_OPERATION and (
                    "provision" in cap.target or "grant" in cap.target or "release" in cap.target or "gate" in cap.target
                ):
                    raise AgentCapabilityViolationError(
                        self.agent_id,
                        self.authority_lane.value,
                        cap.scope.value,
                        f"Governance / Gate mutation operation '{cap.target}' is strictly reserved for COMMANDER lane",
                    )

        # 3. Flat Passive Skill Check
        for skill in self.skills:
            lower_name = skill.name.lower()
            if "nested" in lower_name or "recursive" in lower_name or "subagent" in lower_name:
                raise AgentManifestValidationError(
                    f"Agent '{self.agent_id}' references skill '{skill.name}' which violates "
                    f"flat passive skill constitution (nested/recursive markers prohibited)"
                )

        # 4. Subagent Same-Lane Policy
        if self.subagent_policy.allow_subagents and not self.subagent_policy.enforce_same_lane:
            raise AgentManifestValidationError(
                f"Agent '{self.agent_id}' subagent policy must enforce same-lane containment"
            )


# ---------------------------------------------------------------------------
# Canonical Agent Registry
# ---------------------------------------------------------------------------

class AgentRegistry:
    """Canonical registry holding immutable, versioned AgentDefinitions.
    
    Provides package discovery, deterministic registration, identity collision
    detection, quarantine management, and lane-filtered queries.
    """

    def __init__(self) -> None:
        # Key: (agent_id, version) -> AgentDefinition
        self._agents: Dict[Tuple[str, str], AgentDefinition] = {}
        self._quarantined: Dict[Tuple[str, str], str] = {}

    def register(self, agent: AgentDefinition) -> AgentDefinition:
        """Register an AgentDefinition in the registry.
        
        Idempotency:
        - Registering the exact same definition again succeeds idempotently.
        - Registering a conflicting definition under an existing (agent_id, version) raises AgentIdentityCollisionError.
        """
        # Validate constitutional invariants
        agent.validate_invariants()

        # Ensure content_sha256 is accurately computed
        computed_sha = agent.compute_content_sha256()
        if not agent.content_sha256 or agent.content_sha256 != computed_sha:
            # Recreate with computed hash
            agent_dict = agent.model_dump()
            agent_dict["content_sha256"] = computed_sha
            agent = AgentDefinition.model_validate(agent_dict)

        key = (agent.agent_id, agent.version)

        if key in self._quarantined:
            raise AgentQuarantinedError(agent.agent_id, agent.version, self._quarantined[key])

        if key in self._agents:
            existing = self._agents[key]
            if existing.content_sha256 != agent.content_sha256:
                raise AgentIdentityCollisionError(
                    agent_id=agent.agent_id,
                    version=agent.version,
                    existing_sha256=existing.content_sha256,
                    attempted_sha256=agent.content_sha256,
                )
            # Idempotent re-registration of identical definition
            return existing

        self._agents[key] = agent
        logger.info(f"Registered canonical Agent: {agent.agent_id}@{agent.version} [{agent.authority_lane.value}]")
        return agent

    def get(self, agent_id: str, version: Optional[str] = None) -> AgentDefinition:
        """Retrieve an AgentDefinition by ID and optional version.
        
        If version is omitted, returns the highest SemVer registered version.
        """
        if version:
            key = (agent_id, version)
            if key in self._quarantined:
                raise AgentQuarantinedError(agent_id, version, self._quarantined[key])
            if key not in self._agents:
                raise AgentNotFoundError(agent_id, version)
            return self._agents[key]

        # Version omitted: find all versions for agent_id
        matching = [a for (aid, ver), a in self._agents.items() if aid == agent_id]
        if not matching:
            raise AgentNotFoundError(agent_id)

        # Sort by SemVer (descending)
        def _semver_sort_key(ver_str: str) -> Tuple[int, int, int]:
            parts = ver_str.split("-")[0].split("+")[0].split(".")
            return (int(parts[0]), int(parts[1]), int(parts[2]))

        matching.sort(key=lambda a: _semver_sort_key(a.version), reverse=True)
        return matching[0]

    def has_agent(self, agent_id: str, version: Optional[str] = None) -> bool:
        """Check if an agent exists in the registry."""
        if version:
            return (agent_id, version) in self._agents
        return any(aid == agent_id for aid, ver in self._agents.keys())

    def list_agents(
        self,
        lane: Optional[AuthorityLane] = None,
        min_lifecycle: Optional[AgentLifecycleState] = None,
    ) -> List[AgentDefinition]:
        """List registered agents with optional lane and lifecycle filters."""
        result = list(self._agents.values())
        if lane:
            result = [a for a in result if a.authority_lane == lane]
        if min_lifecycle:
            resolvable_states = (
                PRODUCTION_RESOLVABLE_STATES
                if min_lifecycle in PRODUCTION_RESOLVABLE_STATES
                else {min_lifecycle}
            )
            result = [a for a in result if a.lifecycle_state in resolvable_states]
        result.sort(key=lambda a: (a.agent_id, a.version))
        return result

    def quarantine(self, agent_id: str, version: str, reason: str = "") -> None:
        """Quarantine an agent version to block all future resolutions."""
        key = (agent_id, version)
        self._quarantined[key] = reason
        if key in self._agents:
            agent = self._agents[key]
            # Mutate lifecycle state to QUARANTINED
            d = agent.model_dump()
            d["lifecycle_state"] = AgentLifecycleState.QUARANTINED.value
            d["updated_at"] = utc_now_rfc3339()
            self._agents[key] = AgentDefinition.model_validate(d)
        logger.warning(f"Quarantined Agent: {agent_id}@{version} - {reason}")

    def load_agent_package(self, package_dir: Path | str) -> AgentDefinition:
        """Load and register an Agent package directory containing `agent_manifest.yaml`."""
        p_dir = Path(package_dir).resolve()
        if not p_dir.exists() or not p_dir.is_dir():
            raise AgentManifestValidationError(f"Agent package directory does not exist: {p_dir}")

        manifest_file = p_dir / "agent_manifest.yaml"
        if not manifest_file.exists():
            manifest_file = p_dir / "agent_manifest.json"
        if not manifest_file.exists():
            raise AgentManifestValidationError(f"Missing agent manifest in package directory: {p_dir}")

        try:
            if manifest_file.suffix in (".yaml", ".yml"):
                raw_data = yaml.safe_load(manifest_file.read_text(encoding="utf-8"))
            else:
                raw_data = json.loads(manifest_file.read_text(encoding="utf-8"))
        except Exception as ex:
            raise AgentManifestValidationError(f"Failed to parse agent manifest at {manifest_file}: {ex}") from ex

        agent_data = raw_data.get("agent", raw_data)

        # Reconcile prompt files if present
        cae_md = p_dir / "CAE.md"
        instructions_md = p_dir / "instructions.md"

        prompt_ref = dict(agent_data.get("prompt_reference", {}))
        if instructions_md.exists():
            prompt_ref["instructions_ref"] = "instructions.md"
            prompt_sha = hashlib.sha256(instructions_md.read_bytes()).hexdigest()
            prompt_ref["prompt_sha256"] = prompt_sha
        if cae_md.exists():
            prompt_ref["cae_md_ref"] = "CAE.md"
            agent_data["cae_md_root"] = str(cae_md.relative_to(p_dir.parent).as_posix() if p_dir.parent else "CAE.md")

        agent_data["prompt_reference"] = prompt_ref

        # Validate and construct AgentDefinition
        agent_def = AgentDefinition.model_validate(agent_data)
        return self.register(agent_def)

    def discover_agents(self, root_dir: Path | str) -> int:
        """Discover and load all Agent packages under a root directory (e.g. `agents/`)."""
        r_dir = Path(root_dir).resolve()
        if not r_dir.exists() or not r_dir.is_dir():
            logger.warning(f"Agent discovery root directory not found: {r_dir}")
            return 0

        count = 0
        for item in sorted(r_dir.iterdir()):
            if item.is_dir():
                manifest_yaml = item / "agent_manifest.yaml"
                manifest_json = item / "agent_manifest.json"
                if manifest_yaml.exists() or manifest_json.exists():
                    try:
                        self.load_agent_package(item)
                        count += 1
                    except Exception as ex:
                        logger.error(f"Failed to load agent package at {item}: {ex}")
                        raise
        logger.info(f"Discovered {count} canonical agent packages from {r_dir}")
        return count

    def clear(self) -> None:
        """Clear all registered agents and quarantines."""
        self._agents.clear()
        self._quarantined.clear()


# ---------------------------------------------------------------------------
# Canonical Agent Resolver
# ---------------------------------------------------------------------------

class AgentResolver:
    """Deterministic Resolver for registered Canonical Agents."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def resolve(
        self,
        agent_id: str,
        version: Optional[str] = None,
        min_lifecycle: Optional[AgentLifecycleState] = AgentLifecycleState.APPROVED,
        expected_lane: Optional[AuthorityLane] = None,
    ) -> AgentDefinition:
        """Deterministically resolve an agent by ID and optional version constraint.
        
        Enforces:
        1. Agent must exist in registry.
        2. Agent must not be quarantined.
        3. Lifecycle state must satisfy min_lifecycle (defaults to APPROVED/ACTIVE).
        4. If expected_lane is provided, agent.authority_lane must match.
        """
        agent = self.registry.get(agent_id, version)

        # Lifecycle gate check
        if min_lifecycle is not None:
            if min_lifecycle in PRODUCTION_RESOLVABLE_STATES:
                if agent.lifecycle_state not in PRODUCTION_RESOLVABLE_STATES:
                    raise AgentLifecycleViolationError(
                        agent.agent_id,
                        agent.version,
                        agent.lifecycle_state.value,
                        required_state="APPROVED or ACTIVE",
                    )
            elif agent.lifecycle_state != min_lifecycle:
                raise AgentLifecycleViolationError(
                    agent.agent_id,
                    agent.version,
                    agent.lifecycle_state.value,
                    required_state=min_lifecycle.value,
                )

        # Authority Lane gate check
        if expected_lane is not None and agent.authority_lane != expected_lane:
            raise AgentLaneMismatchError(
                agent.agent_id,
                agent.authority_lane.value,
                expected_lane.value,
            )

        return agent


# ---------------------------------------------------------------------------
# Standalone Agent Session Binding Helper
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class StandaloneAgentSession:
    """Governed standalone session binding a registered Agent directly."""
    session_id: str
    workspace_id: UUID
    agent: AgentDefinition
    authority_lane: AuthorityLane
    created_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "workspace_id": str(self.workspace_id),
            "agent_id": self.agent.agent_id,
            "agent_version": self.agent.version,
            "authority_lane": self.authority_lane.value,
            "agent_sha256": self.agent.content_sha256,
            "created_at": self.created_at,
        }


def create_standalone_agent_session(
    agent: AgentDefinition,
    workspace_id: UUID,
    session_id: Optional[str] = None,
) -> StandaloneAgentSession:
    """Create an independently addressable standalone session binding a registered Agent."""
    if not isinstance(agent, AgentDefinition):
        raise ValueError(f"Expected AgentDefinition, got {type(agent)}")
    if not isinstance(workspace_id, UUID):
        raise ValueError(f"Expected workspace_id as UUID, got {type(workspace_id)}")

    # Standalone session enforces that agent is in resolvable state
    if agent.lifecycle_state not in PRODUCTION_RESOLVABLE_STATES:
        raise AgentLifecycleViolationError(
            agent.agent_id,
            agent.version,
            agent.lifecycle_state.value,
            required_state="APPROVED or ACTIVE",
        )

    s_id = session_id or f"standalone_{agent.agent_id}_{uuid4().hex[:8]}"
    return StandaloneAgentSession(
        session_id=s_id,
        workspace_id=workspace_id,
        agent=agent,
        authority_lane=agent.authority_lane,
    )


# ---------------------------------------------------------------------------
# Global Singleton Accessors
# ---------------------------------------------------------------------------

_GLOBAL_AGENT_REGISTRY: Optional[AgentRegistry] = None


def get_agent_registry() -> AgentRegistry:
    """Retrieve the global singleton AgentRegistry."""
    global _GLOBAL_AGENT_REGISTRY
    if _GLOBAL_AGENT_REGISTRY is None:
        _GLOBAL_AGENT_REGISTRY = AgentRegistry()
    return _GLOBAL_AGENT_REGISTRY


def get_agent_resolver() -> AgentResolver:
    """Retrieve an AgentResolver wrapping the global singleton registry."""
    return AgentResolver(get_agent_registry())


def reset_global_agent_registry() -> None:
    """Reset the global singleton registry (for test isolation)."""
    global _GLOBAL_AGENT_REGISTRY
    if _GLOBAL_AGENT_REGISTRY is not None:
        _GLOBAL_AGENT_REGISTRY.clear()
    _GLOBAL_AGENT_REGISTRY = None
