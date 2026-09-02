"""JIT Context Capsule + Agent Package Compilation Engine for CAE.

Governed by Phase 2 Mandate M18, 00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md,
00_CONTROL/27_PHASE2_CONTEXT_BUDGET_CONTRACT.md, 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md,
and CANONICAL_SKILL_AUTHORING_CONSTITUTION.md.

Enforces:
1. Context Precedence Hierarchy:
   CAE Constitutions > Operator Authorization > Program/Harness Policy > Local CAE.md/AGENTS.md > Agent Instructions > Skill Content.
2. Skill Maturity Gates:
   DRAFT skills are blocked from production execution. Only TESTED or STABLE skills enter production capsules.
3. Passive, Flat Skills:
   Skills are pure procedures (SKILL.md). No nested skills or sub-agents inside skills.
4. Explicit Capability Projections:
   Bound to workspace, authority lane, and security sandbox with zero ambient access.
5. Observable Context Inclusion & Exclusion Trace:
   Every invocation receipt records included items, omitted items, and token budget accounting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
import hashlib
import json
from pathlib import Path, PurePath
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.tenancy import TenancyError, TenancyViolationError


# ---------------------------------------------------------------------------
# Enums and Precedence Layers
# ---------------------------------------------------------------------------

class ContextPrecedenceLayer(IntEnum):
    """Authoritative context precedence hierarchy (lower value = higher precedence)."""
    CAE_CONSTITUTION = 1
    OPERATOR_AUTHORIZATION = 2
    PROGRAM_HARNESS_POLICY = 3
    LOCAL_GOVERNANCE = 4
    AGENT_INSTRUCTIONS = 5
    SKILL_PROCEDURE = 6


class SkillMaturity(str, Enum):
    """Maturity stages for Canonical Skills."""
    DRAFT = "DRAFT"
    TESTED = "TESTED"
    STABLE = "STABLE"
    QUARANTINED = "QUARANTINED"


class ContextExclusionReason(str, Enum):
    """Structured reason codes for intentionally omitted or blocked context."""
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    LANE_MISMATCH = "LANE_MISMATCH"
    INAPPLICABLE_PHASE = "INAPPLICABLE_PHASE"
    FORBIDDEN_BY_POLICY = "FORBIDDEN_BY_POLICY"
    OVERRIDDEN_BY_PRECEDENCE = "OVERRIDDEN_BY_PRECEDENCE"
    UNSATISFIED_PRECONDITION = "UNSATISFIED_PRECONDITION"
    UNCERTIFIED_SKILL = "UNCERTIFIED_SKILL"
    WORKSPACE_MISMATCH = "WORKSPACE_MISMATCH"


class CapabilityScope(str, Enum):
    """Explicit capability scopes from the Phase 2 Capability Security Matrix."""
    CAE_TYPED_OPERATION = "CAE_TYPED_OPERATION"
    POSTGRES_STORAGE = "POSTGRES_STORAGE"
    FILESYSTEM = "FILESYSTEM"
    PROCESS_CLI = "PROCESS_CLI"
    NETWORK = "NETWORK"
    SECRETS = "SECRETS"
    MCP_TOOL = "MCP_TOOL"


class AccessMode(str, Enum):
    """Access mode for capability projections."""
    READ_ONLY = "READ_ONLY"
    READ_WRITE = "READ_WRITE"
    WRITE_ONLY = "WRITE_ONLY"
    MUTATION_OPERATION = "MUTATION_OPERATION"


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class ContextCapsuleError(RuntimeError):
    """Base error for JIT Context Capsule and Package Compilation operations."""

    def __init__(self, message: str, *, reason_code: str = "CONTEXT_CAPSULE_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class SkillMaturityViolationError(ContextCapsuleError):
    """Raised when a Skill fails maturity gating (e.g. DRAFT used in production)."""

    def __init__(self, skill_id: str, maturity: SkillMaturity, required: str = "TESTED or STABLE"):
        super().__init__(
            f"Skill '{skill_id}' with maturity '{maturity.value}' is ineligible for production execution (requires {required})",
            reason_code="SKILL_MATURITY_VIOLATION",
            details={"skill_id": skill_id, "maturity": maturity.value, "required": required},
        )


class ContextNestingViolationError(ContextCapsuleError):
    """Raised when a Skill package violates the flat, passive skill rule by containing nested skills or sub-agents."""

    def __init__(self, skill_id: str, reason: str):
        super().__init__(
            f"Skill '{skill_id}' violates passive/flat constitution: {reason}",
            reason_code="SKILL_NESTING_VIOLATION",
            details={"skill_id": skill_id, "reason": reason},
        )


class ContextBudgetOverflowError(ContextCapsuleError):
    """Raised when context compilation exceeds the declared token budget."""

    def __init__(self, consumed: int, total_budget: int, overflow_section: str):
        super().__init__(
            f"Context token budget exceeded: consumed {consumed} tokens against budget of {total_budget} tokens in section '{overflow_section}'",
            reason_code="CONTEXT_BUDGET_OVERFLOW",
            details={"consumed": consumed, "total_budget": total_budget, "overflow_section": overflow_section},
        )


class ForbiddenContextError(ContextCapsuleError):
    """Raised when forbidden, unverified, or cross-boundary context is supplied."""

    def __init__(self, context_id: str, reason: str):
        super().__init__(
            f"Forbidden or unverified context blocked: '{context_id}' - {reason}",
            reason_code="FORBIDDEN_CONTEXT",
            details={"context_id": context_id, "reason": reason},
        )


class MissingContextError(ContextCapsuleError):
    """Raised when a mandatory context item is missing from assembly."""

    def __init__(self, missing_contexts: Sequence[str]):
        super().__init__(
            f"Mandatory context items missing for capsule assembly: {list(missing_contexts)}",
            reason_code="MISSING_MANDATORY_CONTEXT",
            details={"missing_contexts": list(missing_contexts)},
        )


class CapabilityResolutionError(ContextCapsuleError):
    """Raised when an agent capability projection cannot be resolved or violates security boundaries."""

    def __init__(self, capability_id: str, reason: str):
        super().__init__(
            f"Capability resolution failed for '{capability_id}': {reason}",
            reason_code="CAPABILITY_RESOLUTION_ERROR",
            details={"capability_id": capability_id, "reason": reason},
        )


class ContextPrecedenceConflictError(ContextCapsuleError):
    """Raised when lower-precedence instructions attempt to override constitutional invariants."""

    def __init__(self, lower_ref: str, higher_ref: str, invariant: str):
        super().__init__(
            f"Precedence conflict: '{lower_ref}' attempts to override constitutional invariant '{invariant}' from '{higher_ref}'",
            reason_code="PRECEDENCE_CONFLICT",
            details={"lower_ref": lower_ref, "higher_ref": higher_ref, "invariant": invariant},
        )


class PackageDriftError(ContextCapsuleError):
    """Raised when on-disk package files differ from the compiled component-hash manifest."""

    def __init__(self, agent_id: str, drift_details: Dict[str, Any]):
        super().__init__(
            f"Agent package '{agent_id}' has drifted from its compiled manifest: "
            f"{len(drift_details.get('modified', []))} modified, "
            f"{len(drift_details.get('missing', []))} missing, "
            f"{len(drift_details.get('added', []))} added",
            reason_code="PACKAGE_DRIFT",
            details={"agent_id": agent_id, **drift_details},
        )


class PackageQuarantinedError(ContextCapsuleError):
    """Raised when an agent package has been placed in quarantine and cannot be used."""

    def __init__(self, agent_id: str, reason: str):
        super().__init__(
            f"Agent package '{agent_id}' is quarantined: {reason}",
            reason_code="PACKAGE_QUARANTINED",
            details={"agent_id": agent_id, "quarantine_reason": reason},
        )


class PackageManifestValidationError(ContextCapsuleError):
    """Raised when agent_manifest.yaml or package metadata violates constitutional invariants."""

    def __init__(self, agent_id: str, reason: str):
        super().__init__(
            f"Agent package manifest validation failed for '{agent_id}': {reason}",
            reason_code="PACKAGE_MANIFEST_VALIDATION",
            details={"agent_id": agent_id, "reason": reason},
        )


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Deterministic token estimator (~4 characters per token heuristic)."""
    if not text:
        return 0
    words = len(re.findall(r"\w+|[^\w\s]", text, re.UNICODE))
    chars_est = (len(text) + 3) // 4
    return max(words, chars_est)


@dataclass(frozen=True, slots=True)
class ContextItem:
    """An individual governed context segment included in the JIT capsule."""
    context_id: str
    layer: ContextPrecedenceLayer
    source_ref: str
    content: str
    token_count: int
    inclusion_reason: str
    sha256: str

    @classmethod
    def create(
        cls,
        *,
        context_id: str,
        layer: ContextPrecedenceLayer,
        source_ref: str,
        content: str,
        inclusion_reason: str,
    ) -> "ContextItem":
        content_clean = content.strip()
        digest = hashlib.sha256(content_clean.encode("utf-8")).hexdigest()
        tokens = estimate_tokens(content_clean)
        return cls(
            context_id=context_id,
            layer=layer,
            source_ref=source_ref,
            content=content_clean,
            token_count=tokens,
            inclusion_reason=inclusion_reason,
            sha256=digest,
        )

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "layer": self.layer.name,
            "layer_order": self.layer.value,
            "source_ref": self.source_ref,
            "token_count": self.token_count,
            "inclusion_reason": self.inclusion_reason,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class ContextExclusionRecord:
    """Observable record of context intentionally omitted or blocked during compilation."""
    context_id: str
    layer: ContextPrecedenceLayer
    source_ref: str
    reason: ContextExclusionReason
    justification: str
    attempted_token_count: int

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "context_id": self.context_id,
            "layer": self.layer.name,
            "source_ref": self.source_ref,
            "reason": self.reason.value,
            "justification": self.justification,
            "attempted_token_count": self.attempted_token_count,
        }


@dataclass(frozen=True, slots=True)
class ContextBudgetReport:
    """Context token budget accounting per model invocation."""
    total_budget_tokens: int
    consumed_tokens: int
    remaining_tokens: int
    section_breakdown: Dict[str, int]
    overflow: bool

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "total_budget_tokens": self.total_budget_tokens,
            "consumed_tokens": self.consumed_tokens,
            "remaining_tokens": self.remaining_tokens,
            "section_breakdown": dict(sorted(self.section_breakdown.items())),
            "overflow": self.overflow,
        }


@dataclass(frozen=True, slots=True)
class CapabilityProjection:
    """Explicit capability projection for an agent."""
    capability_id: str
    owner_product: str
    scope: CapabilityScope
    mode: AccessMode
    workspace_bound: bool
    approval_required: bool
    sandbox_required: bool
    audit_mode: str
    bound_tools: Tuple[str, ...] = field(default_factory=tuple)
    mcp_servers: Tuple[str, ...] = field(default_factory=tuple)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "owner_product": self.owner_product,
            "scope": self.scope.value,
            "mode": self.mode.value,
            "workspace_bound": self.workspace_bound,
            "approval_required": self.approval_required,
            "sandbox_required": self.sandbox_required,
            "audit_mode": self.audit_mode,
            "bound_tools": list(sorted(self.bound_tools)),
            "mcp_servers": list(sorted(self.mcp_servers)),
        }


@dataclass(frozen=True, slots=True)
class SkillPackageRef:
    """Governed reference to a passive, flat Canonical Skill."""
    skill_id: str
    version: str
    maturity: SkillMaturity
    procedure_ref: str
    package_sha256: str
    allowed_tools: Tuple[str, ...] = field(default_factory=tuple)
    forbidden_actions: Tuple[str, ...] = field(default_factory=tuple)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "version": self.version,
            "maturity": self.maturity.value,
            "procedure_ref": self.procedure_ref,
            "package_sha256": self.package_sha256,
            "allowed_tools": list(sorted(self.allowed_tools)),
            "forbidden_actions": list(sorted(self.forbidden_actions)),
        }


@dataclass(frozen=True, slots=True)
class CompiledAgentPackage:
    """Immutable compiled manifest of an Eve-like agent package."""
    agent_id: str
    lane: AuthorityLane
    version: str
    package_root: str
    cae_governance_ref: str
    agents_guidance_ref: Optional[str]
    instructions_ref: str
    skills: Tuple[SkillPackageRef, ...]
    subagents: Tuple[str, ...]
    capabilities: Tuple[CapabilityProjection, ...]
    tools: Tuple[str, ...]
    connections: Tuple[str, ...]
    hooks: Tuple[str, ...]
    extensions: Tuple[str, ...]
    evals: Tuple[str, ...]
    package_sha256: str
    compiled_at: str
    component_hashes: Dict[str, str] = field(default_factory=dict)
    is_quarantined: bool = False
    quarantine_reason: Optional[str] = None
    quarantined_at: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "lane": self.lane.value,
            "version": self.version,
            "cae_governance_ref": self.cae_governance_ref,
            "agents_guidance_ref": self.agents_guidance_ref,
            "instructions_ref": self.instructions_ref,
            "skills": [s.canonical_dict() for s in sorted(self.skills, key=lambda s: s.skill_id)],
            "subagents": list(sorted(self.subagents)),
            "capabilities": [c.canonical_dict() for c in sorted(self.capabilities, key=lambda c: c.capability_id)],
            "tools": list(sorted(self.tools)),
            "connections": list(sorted(self.connections)),
            "hooks": list(sorted(self.hooks)),
            "extensions": list(sorted(self.extensions)),
            "evals": list(sorted(self.evals)),
            "component_hashes": dict(sorted(self.component_hashes.items())),
            "is_quarantined": self.is_quarantined,
            "quarantine_reason": self.quarantine_reason,
            "quarantined_at": self.quarantined_at,
            "package_sha256": self.package_sha256,
            "compiled_at": self.compiled_at,
        }

    def detect_drift(self, package_root: Optional[Path] = None) -> Tuple[bool, Dict[str, Any]]:
        """Detects whether on-disk files differ from the compiled component_hashes manifest.
        
        Returns (has_drift, drift_details) where drift_details lists:
        - modified: files whose sha256 changed
        - missing: files present in manifest but missing on disk
        - added: new files present on disk but not in manifest
        """
        root = package_root or Path(self.package_root)
        if not root.exists() or not root.is_dir():
            return True, {
                "error": f"Package root directory does not exist: {root}",
                "modified": [],
                "missing": list(self.component_hashes.keys()),
                "added": [],
                "has_drift": True,
            }

        current_hashes: Dict[str, str] = {}
        for file_path in sorted(root.rglob("*")):
            if file_path.is_file():
                if any(part.startswith(".") or part == "__pycache__" for part in file_path.parts):
                    continue
                rel_path = file_path.relative_to(root).as_posix()
                current_hashes[rel_path] = hashlib.sha256(file_path.read_bytes()).hexdigest()

        manifest_keys = set(self.component_hashes.keys())
        current_keys = set(current_hashes.keys())

        missing = sorted(manifest_keys - current_keys)
        added = sorted(current_keys - manifest_keys)
        modified: List[Dict[str, str]] = []

        for common_key in sorted(manifest_keys & current_keys):
            expected = self.component_hashes[common_key]
            actual = current_hashes[common_key]
            if expected != actual:
                modified.append({
                    "file": common_key,
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                })

        has_drift = bool(missing or added or modified)
        return has_drift, {
            "has_drift": has_drift,
            "modified": modified,
            "missing": missing,
            "added": added,
            "checked_at": utc_now_rfc3339(),
        }

    def verify_integrity(self, package_root: Optional[Path] = None) -> None:
        """Verifies package integrity against on-disk files and checks quarantine state.
        
        Raises PackageQuarantinedError if quarantined.
        Raises PackageDriftError if any drift is detected.
        """
        if self.is_quarantined:
            raise PackageQuarantinedError(self.agent_id, self.quarantine_reason or "Unspecified quarantine")

        has_drift, details = self.detect_drift(package_root)
        if has_drift:
            raise PackageDriftError(self.agent_id, details)

    def quarantine(self, reason: str) -> "CompiledAgentPackage":
        """Returns a new immutable CompiledAgentPackage marked as quarantined."""
        return CompiledAgentPackage(
            agent_id=self.agent_id,
            lane=self.lane,
            version=self.version,
            package_root=self.package_root,
            cae_governance_ref=self.cae_governance_ref,
            agents_guidance_ref=self.agents_guidance_ref,
            instructions_ref=self.instructions_ref,
            skills=self.skills,
            subagents=self.subagents,
            capabilities=self.capabilities,
            tools=self.tools,
            connections=self.connections,
            hooks=self.hooks,
            extensions=self.extensions,
            evals=self.evals,
            package_sha256=self.package_sha256,
            compiled_at=self.compiled_at,
            component_hashes=dict(self.component_hashes),
            is_quarantined=True,
            quarantine_reason=reason,
            quarantined_at=utc_now_rfc3339(),
        )

    def inspect(self) -> Dict[str, Any]:
        """Returns comprehensive inspection metadata including component-hash breakdown."""
        return {
            "agent_id": self.agent_id,
            "lane": self.lane.value,
            "version": self.version,
            "package_root": self.package_root,
            "package_sha256": self.package_sha256,
            "compiled_at": self.compiled_at,
            "is_quarantined": self.is_quarantined,
            "quarantine_reason": self.quarantine_reason,
            "quarantined_at": self.quarantined_at,
            "skills": [
                {
                    "skill_id": s.skill_id,
                    "version": s.version,
                    "maturity": s.maturity.value,
                    "sha256": s.package_sha256,
                    "procedure_ref": s.procedure_ref,
                }
                for s in self.skills
            ],
            "subagents": list(self.subagents),
            "capabilities": [c.canonical_dict() for c in self.capabilities],
            "tools": list(self.tools),
            "hooks": list(self.hooks),
            "component_hashes": dict(sorted(self.component_hashes.items())),
            "total_constituents": len(self.component_hashes),
        }

    def to_inspection_report(self) -> str:
        """Renders a structured markdown inspection report of the compiled package."""
        lines = [
            f"# Compiled Agent Package Inspection: {self.agent_id} (v{self.version})",
            f"- **Authority Lane:** `{self.lane.value}`",
            f"- **Package SHA-256:** `{self.package_sha256}`",
            f"- **Package Root:** `{self.package_root}`",
            f"- **Compiled At:** `{self.compiled_at}`",
            f"- **Quarantine Status:** `{'QUARANTINED (' + (self.quarantine_reason or '') + ')' if self.is_quarantined else 'CLEAN'}`",
            "",
            "## Constituents & Component Hashes",
        ]
        for rel_path, digest in sorted(self.component_hashes.items()):
            lines.append(f"- `{rel_path}`: `{digest}`")

        lines.append("")
        lines.append(f"## Bound Skills ({len(self.skills)})")
        for s in self.skills:
            lines.append(f"- **{s.skill_id}** (v{s.version}) [{s.maturity.value}] — `{s.package_sha256[:16]}...`")

        lines.append("")
        lines.append(f"## Bound Capabilities ({len(self.capabilities)})")
        for c in self.capabilities:
            lines.append(f"- `{c.capability_id}` ({c.scope.value}:{c.mode.value})")

        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class JITContextCapsule:
    """Fully compiled JIT context capsule delivered to model runtime."""
    capsule_id: str
    schema_version: str
    workspace_id: UUID
    lane: AuthorityLane
    actor_id: str
    program_id: str
    harness_id: str
    agent_id: str
    model_id: str
    assembled_prompt: str
    included_context: Tuple[ContextItem, ...]
    exclusion_trace: Tuple[ContextExclusionRecord, ...]
    budget_report: ContextBudgetReport
    skill_hashes: Dict[str, str]
    capability_projections: Tuple[CapabilityProjection, ...]
    capsule_sha256: str
    assembled_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        payload = {
            "schema_version": self.schema_version,
            "workspace_id": str(self.workspace_id),
            "lane": self.lane.value,
            "actor_id": self.actor_id,
            "program_id": self.program_id,
            "harness_id": self.harness_id,
            "agent_id": self.agent_id,
            "model_id": self.model_id,
            "included_context": [c.canonical_dict() for c in self.included_context],
            "exclusion_trace": [e.canonical_dict() for e in self.exclusion_trace],
            "budget_report": self.budget_report.canonical_dict(),
            "skill_hashes": dict(sorted(self.skill_hashes.items())),
            "capability_projections": [c.canonical_dict() for c in sorted(self.capability_projections, key=lambda c: c.capability_id)],
            "assembled_at": self.assembled_at,
        }
        computed_sha = canonical_sha256(payload)
        if computed_sha != self.capsule_sha256:
            raise ContextCapsuleError("JIT context capsule hash drifted from canonical payload")
        return {
            "capsule_id": self.capsule_id,
            "capsule_sha256": self.capsule_sha256,
            **payload,
        }


# ---------------------------------------------------------------------------
# Agent Package Compiler
# ---------------------------------------------------------------------------

class AgentPackageCompiler:
    """Compiles Eve-style agent directories into validated, immutable CompiledAgentPackages."""

    @staticmethod
    def compile(
        package_root: Path,
        *,
        agent_id: str,
        lane: AuthorityLane,
        version: str = "1.0.0",
        production_mode: bool = False,
        declared_capabilities: Optional[Sequence[CapabilityProjection]] = None,
    ) -> CompiledAgentPackage:
        """Inspects and compiles an agent directory.
        
        Validates:
        1. Required files: CAE.md, instructions.md exist.
        2. Optional AGENTS.md reconciled.
        3. Skills are flat (SKILL.md) and do not contain nested subagents or skills.
        4. In production mode, all skills must be TESTED or STABLE (not DRAFT).
        5. Computes composite deterministic package hash and component_hashes manifest.
        """
        if not package_root.exists() or not package_root.is_dir():
            raise ContextCapsuleError(f"Agent package root is not a directory: {package_root}")

        cae_md = package_root / "CAE.md"
        instructions_md = package_root / "instructions.md"
        agents_md = package_root / "AGENTS.md"

        if not cae_md.exists():
            raise ContextCapsuleError(f"Agent package missing required CAE.md at {cae_md}")
        if not instructions_md.exists():
            raise ContextCapsuleError(f"Agent package missing required instructions.md at {instructions_md}")

        # Scan and validate Skills
        skills_dir = package_root / "skills"
        skills: List[SkillPackageRef] = []
        if skills_dir.exists() and skills_dir.is_dir():
            for skill_path in sorted(skills_dir.iterdir()):
                if not skill_path.is_dir():
                    continue
                skill_id = skill_path.name
                skill_file = skill_path / "SKILL.md"
                if not skill_file.exists():
                    raise ContextNestingViolationError(skill_id, f"Missing SKILL.md in {skill_path}")

                # Anti-Nesting Checks: no nested skills or subagents
                if (skill_path / "skills").exists() or (skill_path / "subagents").exists():
                    raise ContextNestingViolationError(
                        skill_id, "Skill contains nested 'skills' or 'subagents' directory (forbidden)"
                    )

                # Parse skill manifest or metadata
                manifest_file = skill_path / "manifest.json"
                maturity = SkillMaturity.DRAFT
                allowed_tools: Tuple[str, ...] = ()
                forbidden_actions: Tuple[str, ...] = ()
                skill_version = "1.0.0"

                if manifest_file.exists():
                    try:
                        m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
                        maturity_str = m_data.get("maturity", "DRAFT").upper()
                        maturity = SkillMaturity(maturity_str) if maturity_str in SkillMaturity._value2member_map_ else SkillMaturity.DRAFT
                        allowed_tools = tuple(m_data.get("allowed_tools", []))
                        forbidden_actions = tuple(m_data.get("forbidden_actions", []))
                        skill_version = m_data.get("version", "1.0.0")
                    except Exception as e:
                        raise ContextCapsuleError(f"Failed to parse skill manifest at {manifest_file}: {e}") from e

                # Production Maturity Gate
                if production_mode and maturity == SkillMaturity.DRAFT:
                    raise SkillMaturityViolationError(skill_id, maturity)

                skill_sha256 = hashlib.sha256(skill_file.read_bytes()).hexdigest()
                skills.append(
                    SkillPackageRef(
                        skill_id=skill_id,
                        version=skill_version,
                        maturity=maturity,
                        procedure_ref=f"skills/{skill_id}/SKILL.md",
                        package_sha256=skill_sha256,
                        allowed_tools=allowed_tools,
                        forbidden_actions=forbidden_actions,
                    )
                )

        # Scan Subagents
        subagents_dir = package_root / "subagents"
        subagents: List[str] = []
        if subagents_dir.exists() and subagents_dir.is_dir():
            for sa_path in sorted(subagents_dir.iterdir()):
                if sa_path.is_dir() and (sa_path / "instructions.md").exists():
                    subagents.append(sa_path.name)

        # Scan other directories
        tools = _list_dir_names(package_root / "tools")
        connections = _list_dir_names(package_root / "connections")
        hooks = _list_dir_names(package_root / "hooks")
        extensions = _list_dir_names(package_root / "extensions")
        evals = _list_dir_names(package_root / "evals")

        # Compute package composite hash and constituent hashes
        file_hashes: Dict[str, str] = {}
        for file_path in sorted(package_root.rglob("*")):
            if file_path.is_file():
                if any(part.startswith(".") or part == "__pycache__" for part in file_path.parts):
                    continue
                rel_path = file_path.relative_to(package_root).as_posix()
                file_hashes[rel_path] = hashlib.sha256(file_path.read_bytes()).hexdigest()

        composite_hasher = hashlib.sha256()
        for path, digest in sorted(file_hashes.items()):
            composite_hasher.update(f"{path}:{digest}\n".encode("utf-8"))
        package_sha256 = composite_hasher.hexdigest()

        return CompiledAgentPackage(
            agent_id=agent_id,
            lane=lane,
            version=version,
            package_root=str(package_root.resolve()),
            cae_governance_ref="CAE.md",
            agents_guidance_ref="AGENTS.md" if agents_md.exists() else None,
            instructions_ref="instructions.md",
            skills=tuple(skills),
            subagents=tuple(subagents),
            capabilities=tuple(declared_capabilities or ()),
            tools=tuple(tools),
            connections=tuple(connections),
            hooks=tuple(hooks),
            extensions=tuple(extensions),
            evals=tuple(evals),
            package_sha256=package_sha256,
            compiled_at=utc_now_rfc3339(),
            component_hashes=file_hashes,
        )


def _list_dir_names(directory: Path) -> List[str]:
    if not directory.exists() or not directory.is_dir():
        return []
    return sorted([p.name for p in directory.iterdir() if p.is_dir() or p.suffix in (".py", ".json", ".yaml")])


# ---------------------------------------------------------------------------
# JIT Context Compiler
# ---------------------------------------------------------------------------

class JITContextCompiler:
    """Assembles JIT runtime context capsules with strict precedence, maturity gating, and budget accounting."""

    @staticmethod
    def assemble(
        *,
        workspace_id: UUID,
        lane: AuthorityLane,
        actor_id: str,
        program_id: str,
        harness_id: str,
        agent_id: str,
        model_id: str = "gemini-2.5-pro",
        total_token_budget: int = 128_000,
        constitutions: Sequence[Tuple[str, str, str]] = (),  # (id, source_ref, text)
        operator_grants: Sequence[Tuple[str, str, str]] = (),
        program_harness_policies: Sequence[Tuple[str, str, str]] = (),
        local_governance_cae_md: Optional[Tuple[str, str]] = None,  # (source_ref, text)
        local_guidance_agents_md: Optional[Tuple[str, str]] = None,  # (source_ref, text)
        agent_instructions: Optional[Tuple[str, str]] = None,  # (source_ref, text)
        skills: Sequence[Tuple[SkillPackageRef, str]] = (),  # (SkillRef, skill_procedure_text)
        artifacts: Sequence[Tuple[str, str, str]] = (),  # (id, source_ref, summary_text)
        mandatory_context_ids: Sequence[str] = (),
        forbidden_context_ids: Sequence[str] = (),
        supplied_candidate_context_ids: Optional[Sequence[str]] = None,
        production_mode: bool = False,
        capabilities: Sequence[CapabilityProjection] = (),
    ) -> JITContextCapsule:
        """Assembles prompt context adhering to the exact precedence hierarchy:
        
        1. CAE Constitutions
        2. Operator Authorization
        3. Program/Harness Policy
        4. Reconciled Local Governance (CAE.md > AGENTS.md)
        5. Agent Instructions
        6. Flat Skill Procedures
        7. Active Artifact References
        """
        included_items: List[ContextItem] = []
        exclusion_records: List[ContextExclusionRecord] = []
        section_breakdown: Dict[str, int] = {}
        consumed_tokens = 0
        skill_hashes: Dict[str, str] = {}

        candidate_ids = set(supplied_candidate_context_ids or [])
        forbidden_set = set(forbidden_context_ids)

        def _try_include_item(
            item: ContextItem,
            section_name: str,
            is_mandatory: bool = False,
        ) -> bool:
            nonlocal consumed_tokens
            if item.context_id in forbidden_set:
                exclusion_records.append(
                    ContextExclusionRecord(
                        context_id=item.context_id,
                        layer=item.layer,
                        source_ref=item.source_ref,
                        reason=ContextExclusionReason.FORBIDDEN_BY_POLICY,
                        justification=f"Context '{item.context_id}' is marked FORBIDDEN by active harness policy",
                        attempted_token_count=item.token_count,
                    )
                )
                if is_mandatory:
                    raise ForbiddenContextError(item.context_id, "Mandatory context is explicitly forbidden")
                return False

            if consumed_tokens + item.token_count > total_token_budget:
                if is_mandatory:
                    raise ContextBudgetOverflowError(
                        consumed=consumed_tokens + item.token_count,
                        total_budget=total_token_budget,
                        overflow_section=section_name,
                    )
                exclusion_records.append(
                    ContextExclusionRecord(
                        context_id=item.context_id,
                        layer=item.layer,
                        source_ref=item.source_ref,
                        reason=ContextExclusionReason.BUDGET_EXCEEDED,
                        justification=f"Item exceeds remaining token budget ({total_token_budget - consumed_tokens} remaining, requires {item.token_count})",
                        attempted_token_count=item.token_count,
                    )
                )
                return False

            included_items.append(item)
            consumed_tokens += item.token_count
            section_breakdown[section_name] = section_breakdown.get(section_name, 0) + item.token_count
            return True

        # Layer 1: CAE Constitutions
        for c_id, s_ref, c_text in constitutions:
            item = ContextItem.create(
                context_id=c_id,
                layer=ContextPrecedenceLayer.CAE_CONSTITUTION,
                source_ref=s_ref,
                content=c_text,
                inclusion_reason="Authoritative CAE constitution invariant",
            )
            _try_include_item(item, "1_constitutions", is_mandatory=True)

        # Layer 2: Operator Authorization & Grants
        for g_id, s_ref, g_text in operator_grants:
            item = ContextItem.create(
                context_id=g_id,
                layer=ContextPrecedenceLayer.OPERATOR_AUTHORIZATION,
                source_ref=s_ref,
                content=g_text,
                inclusion_reason="Active operator session authorization",
            )
            _try_include_item(item, "2_operator_grants", is_mandatory=True)

        # Layer 3: Program & Harness Policy
        for p_id, s_ref, p_text in program_harness_policies:
            item = ContextItem.create(
                context_id=p_id,
                layer=ContextPrecedenceLayer.PROGRAM_HARNESS_POLICY,
                source_ref=s_ref,
                content=p_text,
                inclusion_reason="Program and Harness governing policy",
            )
            _try_include_item(item, "3_program_harness_policies", is_mandatory=True)

        # Layer 4: Reconciled Local Governance (CAE.md outranks AGENTS.md)
        if local_governance_cae_md:
            s_ref, cae_text = local_governance_cae_md
            item = ContextItem.create(
                context_id="local_cae_governance",
                layer=ContextPrecedenceLayer.LOCAL_GOVERNANCE,
                source_ref=s_ref,
                content=cae_text,
                inclusion_reason="Local agent package CAE governance constraints",
            )
            _try_include_item(item, "4_local_governance", is_mandatory=True)

        if local_guidance_agents_md:
            s_ref, agents_text = local_guidance_agents_md
            item = ContextItem.create(
                context_id="local_agents_guidance",
                layer=ContextPrecedenceLayer.LOCAL_GOVERNANCE,
                source_ref=s_ref,
                content=agents_text,
                inclusion_reason="Local AGENTS operating guidance",
            )
            _try_include_item(item, "4_local_governance", is_mandatory=False)

        # Layer 5: Agent Instructions
        if agent_instructions:
            s_ref, inst_text = agent_instructions
            item = ContextItem.create(
                context_id=f"agent_instructions_{agent_id}",
                layer=ContextPrecedenceLayer.AGENT_INSTRUCTIONS,
                source_ref=s_ref,
                content=inst_text,
                inclusion_reason=f"Role behavioral instructions for agent '{agent_id}'",
            )
            _try_include_item(item, "5_agent_instructions", is_mandatory=True)

        # Layer 6: Flat Skill Procedures
        for s_ref_obj, s_procedure_text in skills:
            # Maturity Gating
            if production_mode and s_ref_obj.maturity == SkillMaturity.DRAFT:
                exclusion_records.append(
                    ContextExclusionRecord(
                        context_id=s_ref_obj.skill_id,
                        layer=ContextPrecedenceLayer.SKILL_PROCEDURE,
                        source_ref=s_ref_obj.procedure_ref,
                        reason=ContextExclusionReason.UNCERTIFIED_SKILL,
                        justification=f"DRAFT skill '{s_ref_obj.skill_id}' is blocked from production JIT capsule",
                        attempted_token_count=estimate_tokens(s_procedure_text),
                    )
                )
                raise SkillMaturityViolationError(s_ref_obj.skill_id, s_ref_obj.maturity)

            item = ContextItem.create(
                context_id=f"skill_{s_ref_obj.skill_id}",
                layer=ContextPrecedenceLayer.SKILL_PROCEDURE,
                source_ref=s_ref_obj.procedure_ref,
                content=s_procedure_text,
                inclusion_reason=f"Flat passive Canonical Skill '{s_ref_obj.skill_id}' v{s_ref_obj.version}",
            )
            if _try_include_item(item, "6_skills", is_mandatory=False):
                skill_hashes[s_ref_obj.skill_id] = item.sha256

        # Layer 7: Active Artifacts & Lineage Evidence
        for a_id, s_ref, a_text in artifacts:
            item = ContextItem.create(
                context_id=a_id,
                layer=ContextPrecedenceLayer.SKILL_PROCEDURE,
                source_ref=s_ref,
                content=a_text,
                inclusion_reason="Upstream causal artifact reference",
            )
            _try_include_item(item, "7_artifacts", is_mandatory=False)

        # Check Mandatory Contexts Coverage
        included_ids = {item.context_id for item in included_items}
        missing_mandatory = [m_id for m_id in mandatory_context_ids if m_id not in included_ids]
        if missing_mandatory:
            raise MissingContextError(missing_mandatory)

        # Construct Assembled Prompt Text in Strict Precedence Order
        prompt_sections: List[str] = []
        # Python's sort is stable, preserving insertion order within the same precedence layer
        sorted_included = sorted(included_items, key=lambda x: x.layer.value)
        
        current_layer: Optional[ContextPrecedenceLayer] = None
        for item in sorted_included:
            if item.layer != current_layer:
                current_layer = item.layer
                prompt_sections.append(f"\n# === {current_layer.name} (Precedence Level {current_layer.value}) ===\n")
            prompt_sections.append(f"## [{item.context_id}] (Source: {item.source_ref})\n{item.content}\n")

        assembled_prompt = "\n".join(prompt_sections)

        budget_report = ContextBudgetReport(
            total_budget_tokens=total_token_budget,
            consumed_tokens=consumed_tokens,
            remaining_tokens=total_token_budget - consumed_tokens,
            section_breakdown=section_breakdown,
            overflow=False,
        )

        capsule_core = {
            "schema_version": "1.0.0",
            "workspace_id": str(workspace_id),
            "lane": lane.value,
            "actor_id": actor_id,
            "program_id": program_id,
            "harness_id": harness_id,
            "agent_id": agent_id,
            "model_id": model_id,
            "included_context": [c.canonical_dict() for c in sorted_included],
            "exclusion_trace": [e.canonical_dict() for e in exclusion_records],
            "budget_report": budget_report.canonical_dict(),
            "skill_hashes": dict(sorted(skill_hashes.items())),
            "capability_projections": [c.canonical_dict() for c in sorted(capabilities, key=lambda c: c.capability_id)],
            "assembled_at": utc_now_rfc3339(),
        }
        capsule_digest = canonical_sha256(capsule_core)
        capsule_id = f"jit_capsule_{capsule_digest[:24]}"

        return JITContextCapsule(
            capsule_id=capsule_id,
            schema_version="1.0.0",
            workspace_id=workspace_id,
            lane=lane,
            actor_id=actor_id,
            program_id=program_id,
            harness_id=harness_id,
            agent_id=agent_id,
            model_id=model_id,
            assembled_prompt=assembled_prompt,
            included_context=tuple(sorted_included),
            exclusion_trace=tuple(exclusion_records),
            budget_report=budget_report,
            skill_hashes=skill_hashes,
            capability_projections=tuple(capabilities),
            capsule_sha256=capsule_digest,
            assembled_at=capsule_core["assembled_at"],
        )
