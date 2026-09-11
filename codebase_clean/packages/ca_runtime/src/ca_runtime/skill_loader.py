"""CAE JIT Skill Loader, Maturity Gating, and Package-Local Context Resolution.

Governed by:
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md
- 02_PHASE_2_RUNTIME_FOUNDATION/M22_skill_loader_maturity_context_resolution.md

Core Constitutional Laws:
1. A Canonical Skill is a passive, versioned, flat capability specification—never an autonomous agent.
2. Skills compose flatly; no Skill may invoke another Skill (Skill-to-Skill invocation is impossible).
3. Strict 4 Authority Lanes: HUNTER, ANALYST, COMPOSER, COMMANDER.
4. Strict fail-closed Maturity Gating: DRAFT, REVOKED, and DEPRECATED skills cannot execute in production.
5. Context Precedence:
   CAE Constitutions > Operator Authorization > Program/Harness Policy > Local CAE.md/AGENTS.md > Agent Instructions > Skill Content.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import (
    CANONICAL_AUTHORITY_LANES,
    ProgramPackage,
    ProgramRegistry,
    compute_file_sha256,
    get_program_registry,
)

logger = logging.getLogger("ca_runtime.skill_loader")


# ---------------------------------------------------------------------------
# Typed Exceptions
# ---------------------------------------------------------------------------

class SkillLoaderError(Exception):
    """Base exception for skill loader and maturity violations."""
    pass


class SkillNotFoundError(SkillLoaderError):
    """Raised when a requested skill cannot be found in the registry or package."""
    pass


class SkillFrontmatterParseError(SkillLoaderError):
    """Raised when SKILL.md frontmatter is missing, malformed, or invalid."""
    pass


class MaturityGateViolationError(SkillLoaderError):
    """Raised when a skill's maturity state does not satisfy the execution gate."""
    pass


class UnapprovedSkillExecutionError(MaturityGateViolationError):
    """Raised when an unapproved (DRAFT, REVOKED, DEPRECATED) skill execution is attempted."""
    pass


class SkillAuthorityMismatchError(SkillLoaderError):
    """Raised when a skill is executed in an unassigned or unauthorized Authority Lane."""
    pass


class SkillNestingError(SkillLoaderError):
    """Raised when a skill attempts to nest sub-skills or subagents in violation of the flat constitution."""
    pass


class SkillToSkillInvocationProhibitedError(SkillLoaderError):
    """Raised when a runtime execution context attempts to invoke a Skill from inside a Skill frame."""
    pass


# ---------------------------------------------------------------------------
# Enums and Data Models
# ---------------------------------------------------------------------------

class SkillMaturityState(str, Enum):
    """Canonical lifecycle and maturity states for Skills."""
    DRAFT = "DRAFT"
    PROTOTYPE = "PROTOTYPE"
    EVALUATED = "EVALUATED"
    STABLE = "STABLE"
    DEPRECATED = "DEPRECATED"
    REVOKED = "REVOKED"


# Non-executable states in production
NON_EXECUTABLE_MATURITY_STATES: Set[SkillMaturityState] = {
    SkillMaturityState.DRAFT,
    SkillMaturityState.REVOKED,
    SkillMaturityState.DEPRECATED,
}

# Production eligible states
PRODUCTION_EXECUTABLE_MATURITY_STATES: Set[SkillMaturityState] = {
    SkillMaturityState.STABLE,
    SkillMaturityState.EVALUATED,
}


class SkillMetadata(BaseModel):
    """Structured, hash-pinned metadata parsed from SKILL.md frontmatter."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+(-[a-zA-Z0-9_.-]+)?$")
    description: str = Field(..., min_length=3)
    maturity: SkillMaturityState = Field(default=SkillMaturityState.STABLE)
    lanes: List[AuthorityLane] = Field(
        default_factory=lambda: [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMPOSER, AuthorityLane.COMMANDER],
        description="Permitted Authority Lanes for this skill",
    )
    purpose: Optional[str] = Field(default=None)
    triggers: List[str] = Field(default_factory=list, description="Keywords or event trigger patterns")
    inputs: List[str] = Field(default_factory=list, description="Declared input artifact/data contracts")
    outputs: List[str] = Field(default_factory=list, description="Declared output artifact/data contracts")
    allowed_tools: List[str] = Field(default_factory=list, description="Explicitly permitted tool IDs")
    forbidden_actions: List[str] = Field(default_factory=list, description="Explicitly prohibited action IDs")
    sha256: str = Field(..., description="SHA-256 hash of the complete SKILL.md content")


class SkillPackageContext(BaseModel):
    """Package-local context resolved from the governing Program package directory."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    package_root: str
    cae_constitution: Optional[str] = Field(default=None, description="Content of package-local CAE.md")
    cae_constitution_sha256: Optional[str] = Field(default=None)
    agents_guidance: Optional[str] = Field(default=None, description="Content of package-local AGENTS.md")
    agents_guidance_sha256: Optional[str] = Field(default=None)
    instructions: Optional[str] = Field(default=None, description="Content of package-local instructions.md")
    instructions_sha256: Optional[str] = Field(default=None)


class LoadedSkill(BaseModel):
    """In-memory representation of a fully parsed, hash-pinned Canonical Skill."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    metadata: SkillMetadata
    body_markdown: str
    skill_path: str
    package_context: Optional[SkillPackageContext] = Field(default=None)
    loaded_at: str = Field(default_factory=utc_now_rfc3339)


class SkillExecutionContextCapsule(BaseModel):
    """Compiled JIT Context Capsule satisfying constitutional precedence rules.
    
    Context Precedence Hierarchy:
    1. CAE Constitutions
    2. Operator Authorization (Workspace + Grant)
    3. Program / Harness Policy
    4. Local CAE.md / AGENTS.md
    5. Agent Instructions
    6. Skill Content (passive instructions & metadata)
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    capsule_id: str
    skill_name: str
    skill_version: str
    skill_sha256: str
    workspace_id: str
    lane: AuthorityLane
    operator_grant_id: Optional[str] = None
    
    # Layer 1: CAE Constitution
    cae_constitution_ref: str
    
    # Layer 2: Tenancy & Operator Authority
    tenancy_layer: Dict[str, Any]
    
    # Layer 3: Program / Harness Policy
    program_policy_layer: Dict[str, Any]
    
    # Layer 4: Local CAE.md & AGENTS.md
    local_governance_layer: Dict[str, Any]
    
    # Layer 5: Agent Instructions
    instructions_layer: Dict[str, Any]
    
    # Layer 6: Passive Skill Content
    skill_layer: Dict[str, Any]
    
    # Capsule verification digest
    composite_digest: str
    compiled_at: str = Field(default_factory=utc_now_rfc3339)


# ---------------------------------------------------------------------------
# Markdown & Frontmatter Parser
# ---------------------------------------------------------------------------

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_skill_markdown(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """Parses a SKILL.md file, separating YAML frontmatter from Markdown body.
    
    If no frontmatter is present, extracts metadata using standard Markdown heuristics.
    """
    match = FRONTMATTER_REGEX.match(raw_text)
    if match:
        frontmatter_raw, body = match.groups()
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
            if not isinstance(frontmatter, dict):
                raise SkillFrontmatterParseError("Frontmatter YAML must parse to a mapping")
            return frontmatter, body.strip()
        except yaml.YAMLError as e:
            raise SkillFrontmatterParseError(f"Malformed YAML frontmatter: {e}") from e
    
    # Fallback: extract title/description from markdown headers if frontmatter is omitted
    lines = raw_text.strip().splitlines()
    title = "unnamed_skill"
    description = ""
    for line in lines:
        line_clean = line.strip()
        if line_clean.startswith("# "):
            title = line_clean[2:].strip().lower().replace(" ", "_").replace("-", "_")
        elif not description and line_clean and not line_clean.startswith("#"):
            description = line_clean
            
    fallback_fm = {
        "name": title,
        "description": description or f"Canonical skill {title}",
        "version": "1.0.0",
        "maturity": "STABLE",
    }
    return fallback_fm, raw_text.strip()


# ---------------------------------------------------------------------------
# Package Context Resolver
# ---------------------------------------------------------------------------

def resolve_package_context(package_root: Path) -> SkillPackageContext:
    """Resolves package-local governance files (CAE.md, AGENTS.md, instructions.md)."""
    cae_md_path = package_root / "CAE.md"
    cae_content = cae_md_path.read_text(encoding="utf-8") if cae_md_path.exists() else None
    cae_sha = hashlib.sha256(cae_content.encode("utf-8")).hexdigest() if cae_content else None

    agents_md_path = package_root / "AGENTS.md"
    agents_content = agents_md_path.read_text(encoding="utf-8") if agents_md_path.exists() else None
    agents_sha = hashlib.sha256(agents_content.encode("utf-8")).hexdigest() if agents_content else None

    instr_md_path = package_root / "instructions.md"
    instr_content = instr_md_path.read_text(encoding="utf-8") if instr_md_path.exists() else None
    instr_sha = hashlib.sha256(instr_content.encode("utf-8")).hexdigest() if instr_content else None

    return SkillPackageContext(
        package_root=str(package_root.resolve()),
        cae_constitution=cae_content,
        cae_constitution_sha256=cae_sha,
        agents_guidance=agents_content,
        agents_guidance_sha256=agents_sha,
        instructions=instr_content,
        instructions_sha256=instr_sha,
    )


# ---------------------------------------------------------------------------
# Skill Loader Service
# ---------------------------------------------------------------------------

class SkillLoader:
    """Loads, validates, hash-pins, and compiles Canonical Skills JIT."""

    def __init__(self, program_registry: Optional[ProgramRegistry] = None):
        self._registry = program_registry or get_program_registry()
        self._loaded_skills_cache: Dict[Tuple[str, str], LoadedSkill] = {}

    def load_skill_from_path(
        self,
        skill_file_or_dir: Path,
        package_root: Optional[Path] = None,
    ) -> LoadedSkill:
        """Loads a SKILL.md file or directory, validating flat constitution and hash pinning."""
        if not skill_file_or_dir.exists():
            raise SkillNotFoundError(f"Skill path does not exist: {skill_file_or_dir}")

        if skill_file_or_dir.is_dir():
            # Check for forbidden nesting
            if (skill_file_or_dir / "skills").exists() or (skill_file_or_dir / "subagents").exists():
                raise SkillNestingError(
                    f"Skill directory at {skill_file_or_dir} violates flat constitution (contains nested skills or subagents)"
                )
            skill_md_path = skill_file_or_dir / "SKILL.md"
            if not skill_md_path.exists():
                raise SkillNotFoundError(f"SKILL.md not found in directory: {skill_file_or_dir}")
        else:
            skill_md_path = skill_file_or_dir

        raw_bytes = skill_md_path.read_bytes()
        skill_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        raw_text = raw_bytes.decode("utf-8")

        frontmatter, body_markdown = parse_skill_markdown(raw_text)

        # Parse and validate maturity
        maturity_raw = frontmatter.get("maturity", "STABLE")
        if isinstance(maturity_raw, str):
            try:
                maturity = SkillMaturityState(maturity_raw.upper())
            except ValueError:
                maturity = SkillMaturityState.DRAFT
        else:
            maturity = SkillMaturityState.STABLE

        # Parse authority lanes
        lanes_raw = frontmatter.get("lanes", [])
        parsed_lanes: List[AuthorityLane] = []
        if lanes_raw:
            for l in lanes_raw:
                l_str = str(l).upper()
                if l_str in CANONICAL_AUTHORITY_LANES:
                    parsed_lanes.append(AuthorityLane(l_str))
        if not parsed_lanes:
            parsed_lanes = [
                AuthorityLane.HUNTER,
                AuthorityLane.ANALYST,
                AuthorityLane.COMPOSER,
                AuthorityLane.COMMANDER,
            ]

        metadata = SkillMetadata(
            name=str(frontmatter.get("name", skill_md_path.parent.name if skill_file_or_dir.is_dir() else skill_md_path.stem)),
            version=str(frontmatter.get("version", "1.0.0")),
            description=str(frontmatter.get("description", "Canonical passive skill")),
            maturity=maturity,
            lanes=parsed_lanes,
            purpose=frontmatter.get("purpose"),
            triggers=list(frontmatter.get("triggers", [])),
            inputs=list(frontmatter.get("inputs", [])),
            outputs=list(frontmatter.get("outputs", [])),
            allowed_tools=list(frontmatter.get("allowed_tools", [])),
            forbidden_actions=list(frontmatter.get("forbidden_actions", [])),
            sha256=skill_sha256,
        )

        package_context = resolve_package_context(package_root) if package_root and package_root.is_dir() else None

        loaded = LoadedSkill(
            metadata=metadata,
            body_markdown=body_markdown,
            skill_path=str(skill_md_path.resolve()),
            package_context=package_context,
        )
        return loaded

    def resolve_skill(
        self,
        program_id: str,
        skill_name: str,
        version: Optional[str] = None,
    ) -> LoadedSkill:
        """Resolves a skill by name within a registered Program Package."""
        pkg = self._registry.get_program(program_id, version)
        pkg_root = Path(pkg.package_root)

        matching_binding = next((s for s in pkg.manifest.skills if s.name == skill_name), None)
        if not matching_binding:
            raise SkillNotFoundError(f"Skill '{skill_name}' is not declared in program '{program_id}'")

        skill_path = pkg_root / matching_binding.path
        loaded = self.load_skill_from_path(skill_path, package_root=pkg_root)
        
        # Verify hash pinning if declared in binding or package inventory
        expected_sha = matching_binding.sha256 or pkg.skills_inventory.get(skill_name)
        if expected_sha and loaded.metadata.sha256 != expected_sha:
            raise SkillLoaderError(
                f"Skill '{skill_name}' hash mismatch! Expected {expected_sha[:12]}, found {loaded.metadata.sha256[:12]}"
            )

        cache_key = (f"{program_id}:{skill_name}", loaded.metadata.version)
        self._loaded_skills_cache[cache_key] = loaded
        return loaded


# ---------------------------------------------------------------------------
# Context Precedence Compilation
# ---------------------------------------------------------------------------

def compile_skill_context_capsule(
    skill: LoadedSkill,
    workspace_id: str,
    lane: AuthorityLane,
    operator_grant_id: Optional[str] = None,
    program_id: Optional[str] = None,
    additional_preconditions: Optional[Sequence[str]] = None,
) -> SkillExecutionContextCapsule:
    """Compiles a deterministic JIT Context Capsule adhering strictly to context precedence."""
    # Precedence Layer 1: CAE Constitution
    cae_constitution_ref = "CAE_ACTIVATE_CONSTITUTION_v1.1"
    
    # Precedence Layer 2: Tenancy & Operator Authorization
    tenancy_layer = {
        "workspace_id": workspace_id,
        "operator_grant_id": operator_grant_id,
        "lane": lane.value,
        "evaluated_at": utc_now_rfc3339(),
    }
    
    # Precedence Layer 3: Program / Harness Policy
    program_policy_layer = {
        "program_id": program_id or "autonomous_evaluation_context",
        "allowed_lanes": [l.value for l in skill.metadata.lanes],
        "preconditions": list(additional_preconditions or []),
    }
    
    # Precedence Layer 4: Local CAE.md & AGENTS.md
    local_governance_layer = {
        "has_local_cae": bool(skill.package_context and skill.package_context.cae_constitution),
        "local_cae_sha256": skill.package_context.cae_constitution_sha256 if skill.package_context else None,
        "has_local_agents": bool(skill.package_context and skill.package_context.agents_guidance),
        "local_agents_sha256": skill.package_context.agents_guidance_sha256 if skill.package_context else None,
    }
    
    # Precedence Layer 5: Agent Instructions
    instructions_layer = {
        "has_instructions": bool(skill.package_context and skill.package_context.instructions),
        "instructions_sha256": skill.package_context.instructions_sha256 if skill.package_context else None,
    }
    
    # Precedence Layer 6: Passive Skill Content & Metadata
    skill_layer = {
        "name": skill.metadata.name,
        "version": skill.metadata.version,
        "maturity": skill.metadata.maturity.value,
        "sha256": skill.metadata.sha256,
        "allowed_tools": skill.metadata.allowed_tools,
        "forbidden_actions": skill.metadata.forbidden_actions,
    }
    
    composite_payload = {
        "skill_name": skill.metadata.name,
        "skill_version": skill.metadata.version,
        "skill_sha256": skill.metadata.sha256,
        "workspace_id": workspace_id,
        "lane": lane.value,
        "operator_grant_id": operator_grant_id,
        "cae_constitution_ref": cae_constitution_ref,
        "tenancy_layer": tenancy_layer,
        "program_policy_layer": program_policy_layer,
        "local_governance_layer": local_governance_layer,
        "instructions_layer": instructions_layer,
        "skill_layer": skill_layer,
    }
    composite_digest = canonical_sha256(composite_payload)
    capsule_id = f"capsule-{skill.metadata.name}-{composite_digest[:16]}"
    
    return SkillExecutionContextCapsule(
        capsule_id=capsule_id,
        skill_name=skill.metadata.name,
        skill_version=skill.metadata.version,
        skill_sha256=skill.metadata.sha256,
        workspace_id=workspace_id,
        lane=lane,
        operator_grant_id=operator_grant_id,
        cae_constitution_ref=cae_constitution_ref,
        tenancy_layer=tenancy_layer,
        program_policy_layer=program_policy_layer,
        local_governance_layer=local_governance_layer,
        instructions_layer=instructions_layer,
        skill_layer=skill_layer,
        composite_digest=composite_digest,
    )


# ---------------------------------------------------------------------------
# Passive Skill Execution Guard & Maturity Gate
# ---------------------------------------------------------------------------

class PassiveSkillExecutionEnvironment:
    """Hermetic execution frame for passive skills that strictly prohibits Skill-to-Skill invocation."""

    def __init__(self, skill: LoadedSkill, capsule: SkillExecutionContextCapsule):
        self.skill = skill
        self.capsule = capsule
        self._is_active = True

    def invoke_skill(self, *args, **kwargs) -> Any:
        """Explicitly prohibited API operation."""
        raise SkillToSkillInvocationProhibitedError(
            f"Skill '{self.skill.metadata.name}' attempted to invoke another Skill! "
            "Skill-to-Skill invocation is strictly prohibited by the Canonical Skill Authoring Constitution."
        )


def execute_passive_skill(
    skill: LoadedSkill,
    capsule: SkillExecutionContextCapsule,
    runner_fn: Callable[[PassiveSkillExecutionEnvironment, Dict[str, Any]], Dict[str, Any]],
    inputs: Optional[Dict[str, Any]] = None,
    allow_prototype_sandbox: bool = False,
) -> Dict[str, Any]:
    """Executes a passive Canonical Skill with strict maturity gating and anti-nesting protection.
    
    Enforces:
    1. Maturity gating: DRAFT, REVOKED, and DEPRECATED skills fail closed.
    2. Authority lane validation: Capsule lane must be in skill's permitted lanes.
    3. Hermetic execution environment: Invoking other skills inside runner_fn raises error.
    4. Deterministic output contract.
    """
    # 1. Maturity Gate
    maturity = skill.metadata.maturity
    if maturity in NON_EXECUTABLE_MATURITY_STATES:
        raise UnapprovedSkillExecutionError(
            f"Cannot execute skill '{skill.metadata.name}' with maturity state '{maturity.value}'. "
            f"Non-executable states: {[s.value for s in NON_EXECUTABLE_MATURITY_STATES]}"
        )

    if maturity == SkillMaturityState.PROTOTYPE and not allow_prototype_sandbox:
        raise MaturityGateViolationError(
            f"Skill '{skill.metadata.name}' is in PROTOTYPE state and requires explicit sandbox authorization."
        )

    # 2. Authority Lane Check
    if capsule.lane not in skill.metadata.lanes:
        raise SkillAuthorityMismatchError(
            f"Skill '{skill.metadata.name}' does not permit execution in Authority Lane '{capsule.lane.value}'. "
            f"Permitted lanes: {[l.value for l in skill.metadata.lanes]}"
        )

    # 3. Hermetic Environment Setup
    env = PassiveSkillExecutionEnvironment(skill, capsule)

    # 4. Execute passive runner
    try:
        output = runner_fn(env, inputs or {})
        if not isinstance(output, dict):
            raise SkillLoaderError(f"Skill runner must return a dict output, got {type(output)}")
        return {
            "status": "COMPLETED",
            "skill_name": skill.metadata.name,
            "skill_version": skill.metadata.version,
            "capsule_id": capsule.capsule_id,
            "lane": capsule.lane.value,
            "output": output,
            "execution_sha256": canonical_sha256(output),
        }
    except SkillToSkillInvocationProhibitedError:
        raise
    except Exception as e:
        logger.error("Error executing passive skill %s: %s", skill.metadata.name, e)
        raise
