"""Program -> Agent -> Phase Binding Compiler for CAE.

Governed by:
- Phase 6 Mandate M53 (01_AGENT_EXECUTION/M53_program_agent_phase_binding_compiler.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Enforces:
1. Executable Manifest-to-Runtime Agent Assignment:
   Transforms declarative Program manifests and workflow node topologies into verified,
   immutable CompiledAgentNodeAssignment and ProgramAgentPhaseBindingManifest records.
2. 1-to-1 Exact Resolution:
   Every Agent-owned workflow node resolves to exactly one canonical AgentDefinition.
3. Authority Lane & Capability Gating:
   Validates Authority Lane parity (HUNTER, ANALYST, COMPOSER, COMMANDER), skill availability,
   tool grants, and typed output contracts.
4. Fail-Closed Anti-Ambiguity & Anti-Tampering:
   Missing agents, ambiguous multi-matches, unassigned outputs, or lane collisions fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.agent_registry import (
    AgentDefinition,
    AgentOutputContract,
    AgentRegistry,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramManifest

logger = logging.getLogger("ca_runtime.program_agent_binding")


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class ProgramAgentBindingError(RuntimeError):
    """Base exception for Program-to-Agent binding compiler violations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "PROGRAM_AGENT_BINDING_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class UnresolvedAgentAssignmentError(ProgramAgentBindingError):
    """Raised when an Agent required by a workflow node cannot be found or is missing from manifest/registry."""

    def __init__(self, node_id: str, agent_id: str, program_id: str, reason: str = ""):
        super().__init__(
            f"UNRESOLVED_AGENT_ASSIGNMENT: Workflow node '{node_id}' in program '{program_id}' "
            f"failed to resolve Agent '{agent_id}': {reason}",
            reason_code="UNRESOLVED_AGENT_ASSIGNMENT",
            details={"node_id": node_id, "agent_id": agent_id, "program_id": program_id, "reason": reason},
        )


class AmbiguousAgentAssignmentError(ProgramAgentBindingError):
    """Raised when multiple conflicting agents match an assignment without explicit resolution."""

    def __init__(self, node_id: str, role: str, matching_agents: Sequence[str]):
        super().__init__(
            f"AMBIGUOUS_AGENT_ASSIGNMENT: Workflow node '{node_id}' with role '{role}' matches "
            f"multiple candidate agents: {list(matching_agents)}. Explicit agent_id assignment required.",
            reason_code="AMBIGUOUS_AGENT_ASSIGNMENT",
            details={"node_id": node_id, "role": role, "matching_agents": list(matching_agents)},
        )


class LaneBindingMismatchError(ProgramAgentBindingError):
    """Raised when an Agent's Authority Lane differs from the node's required lane/role."""

    def __init__(self, node_id: str, agent_id: str, agent_lane: str, required_lane: str):
        super().__init__(
            f"LANE_BINDING_MISMATCH: Cannot assign Agent '{agent_id}' (lane: {agent_lane}) "
            f"to workflow node '{node_id}' (required lane: {required_lane})",
            reason_code="LANE_BINDING_MISMATCH",
            details={"node_id": node_id, "agent_id": agent_id, "agent_lane": agent_lane, "required_lane": required_lane},
        )


class IncompatibleSkillBindingError(ProgramAgentBindingError):
    """Raised when a node requires skills not bound to or permitted for the assigned agent."""

    def __init__(self, node_id: str, agent_id: str, missing_skills: Sequence[str]):
        super().__init__(
            f"INCOMPATIBLE_SKILL_BINDING: Agent '{agent_id}' assigned to node '{node_id}' "
            f"is missing required skills: {list(missing_skills)}",
            reason_code="INCOMPATIBLE_SKILL_BINDING",
            details={"node_id": node_id, "agent_id": agent_id, "missing_skills": list(missing_skills)},
        )


class IncompatibleToolBindingError(ProgramAgentBindingError):
    """Raised when a node requires tools outside the agent's declared tools and capabilities."""

    def __init__(self, node_id: str, agent_id: str, missing_tools: Sequence[str]):
        super().__init__(
            f"INCOMPATIBLE_TOOL_BINDING: Agent '{agent_id}' assigned to node '{node_id}' "
            f"lacks required tools: {list(missing_tools)}",
            reason_code="INCOMPATIBLE_TOOL_BINDING",
            details={"node_id": node_id, "agent_id": agent_id, "missing_tools": list(missing_tools)},
        )


class UnresolvedOutputContractError(ProgramAgentBindingError):
    """Raised when an Agent-owned node lacks a resolved typed output contract."""

    def __init__(self, node_id: str, agent_id: str, reason: str = ""):
        super().__init__(
            f"UNRESOLVED_OUTPUT_CONTRACT: Agent-owned node '{node_id}' (Agent '{agent_id}') "
            f"lacks a declared typed output contract: {reason}",
            reason_code="UNRESOLVED_OUTPUT_CONTRACT",
            details={"node_id": node_id, "agent_id": agent_id, "reason": reason},
        )


# ---------------------------------------------------------------------------
# Domain Models: CompiledAgentNodeAssignment & ProgramAgentPhaseBindingManifest
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CompiledAgentNodeAssignment:
    """Immutable compiled binding linking a specific workflow node to an Agent and its execution contract."""
    node_id: str
    phase_id: str
    phase_order: int
    actor_kind: str
    role: str
    lane: AuthorityLane
    agent_id: str
    agent_version: str
    agent_content_sha256: str
    bound_skills: Tuple[str, ...]
    bound_tools: Tuple[str, ...]
    output_contracts: Tuple[str, ...]
    binding_sha256: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "phase_id": self.phase_id,
            "phase_order": int(self.phase_order),
            "actor_kind": self.actor_kind,
            "role": self.role,
            "lane": self.lane.value,
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "agent_content_sha256": self.agent_content_sha256,
            "bound_skills": list(sorted(self.bound_skills)),
            "bound_tools": list(sorted(self.bound_tools)),
            "output_contracts": list(sorted(self.output_contracts)),
            "binding_sha256": self.binding_sha256,
        }


@dataclass(frozen=True, slots=True)
class ProgramAgentPhaseBindingManifest:
    """Immutable compiled manifest representing the complete Program -> Agent -> Phase binding."""
    manifest_id: str
    program_id: str
    program_version: str
    program_manifest_sha256: str
    state_machine_id: str
    node_assignments: Tuple[CompiledAgentNodeAssignment, ...]
    manifest_binding_sha256: str
    compiled_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "program_id": self.program_id,
            "program_version": self.program_version,
            "program_manifest_sha256": self.program_manifest_sha256,
            "state_machine_id": self.state_machine_id,
            "node_assignments": [a.canonical_dict() for a in self.node_assignments],
            "manifest_binding_sha256": self.manifest_binding_sha256,
            "compiled_at": self.compiled_at,
        }

    def get_assignment_for_node(self, node_id: str) -> Optional[CompiledAgentNodeAssignment]:
        for a in self.node_assignments:
            if a.node_id == node_id:
                return a
        return None

    def get_assignment_for_phase(self, phase_id: str) -> Optional[CompiledAgentNodeAssignment]:
        for a in self.node_assignments:
            if a.phase_id == phase_id:
                return a
        return None

    def list_assignments_for_lane(self, lane: AuthorityLane) -> List[CompiledAgentNodeAssignment]:
        return [a for a in self.node_assignments if a.lane == lane]


# ---------------------------------------------------------------------------
# Program Agent Binding Compiler
# ---------------------------------------------------------------------------

class ProgramAgentBindingCompiler:
    """Compiles Program manifests, workflow nodes, and registered Agents into an executable binding manifest."""

    @staticmethod
    def compile(
        *,
        program_manifest: ProgramManifest | Mapping[str, Any],
        workflow_nodes: Sequence[Mapping[str, Any]],
        agent_registry: AgentRegistry,
        state_machine_id: Optional[str] = None,
        program_manifest_sha256: Optional[str] = None,
        production_mode: bool = False,
    ) -> ProgramAgentPhaseBindingManifest:
        """Compile and validate Program -> Agent -> Phase node assignments.
        
        Enforces:
        1. Every Agent-owned node resolves exactly one Agent.
        2. Authority Lane compatibility between Agent and Node.
        3. Skill availability and tool capability coverage.
        4. Typed output contract resolution.
        5. Deterministic composite SHA-256 for each assignment and manifest.
        """
        # 1. Normalize Program Manifest
        if isinstance(program_manifest, ProgramManifest):
            p_id = program_manifest.id
            p_ver = program_manifest.version
            p_agents = set(program_manifest.agents)
            p_skills = {s.name for s in program_manifest.skills}
            p_state_machine = state_machine_id or program_manifest.state_machine
            p_sha = program_manifest_sha256 or canonical_sha256(program_manifest.model_dump())
        else:
            prog_dict = program_manifest.get("program", program_manifest)
            p_id = prog_dict["id"]
            p_ver = prog_dict["version"]
            p_agents = set(prog_dict.get("agents", []))
            skills_raw = prog_dict.get("skills", [])
            p_skills = {s["name"] if isinstance(s, dict) else s for s in skills_raw}
            p_state_machine = state_machine_id or prog_dict.get("state_machine", "UNKNOWN_STATE_MACHINE")
            p_sha = program_manifest_sha256 or canonical_sha256(prog_dict)

        # 2. Iterate and Compile Node Assignments
        assignments: List[CompiledAgentNodeAssignment] = []

        for idx, node in enumerate(workflow_nodes):
            node_id = node.get("node_id", f"node_{idx}")
            actor_kind = node.get("actor_kind", "GOVERNED_AGENT_NODE")
            role = node.get("role", "HUNTER")
            phase_id = node.get("phase_id", node.get("capability_id", node_id))
            phase_order = int(node.get("phase_order", idx + 1))
            specified_agent_id = node.get("agent_id")

            # Check if this node is Agent-owned
            is_agent_owned = (
                actor_kind in ("GOVERNED_AGENT_NODE", "actor:agent", "AGENT_NODE")
                or (role in ("HUNTER", "ANALYST", "COMPOSER", "COMMANDER") and actor_kind != "HUMAN_GATE" and actor_kind != "DETERMINISTIC_CODE_NODE")
            )

            if not is_agent_owned:
                continue

            # 3. Resolve Target Agent
            resolved_agent_id: str = ""
            if specified_agent_id:
                if specified_agent_id not in p_agents:
                    raise UnresolvedAgentAssignmentError(
                        node_id,
                        specified_agent_id,
                        p_id,
                        f"Agent '{specified_agent_id}' is not declared in program manifest 'agents' inventory: {sorted(p_agents)}",
                    )
                resolved_agent_id = specified_agent_id
            else:
                # Find matching agents from program manifest by Authority Lane
                matching_agents = []
                for candidate_id in sorted(p_agents):
                    if agent_registry.has_agent(candidate_id):
                        agent_def = agent_registry.get(candidate_id)
                        if agent_def.authority_lane.value == role:
                            matching_agents.append(candidate_id)

                if len(matching_agents) == 0:
                    raise UnresolvedAgentAssignmentError(
                        node_id,
                        f"role:{role}",
                        p_id,
                        f"No registered agent in program manifest matches required role/lane '{role}'",
                    )
                elif len(matching_agents) > 1:
                    raise AmbiguousAgentAssignmentError(node_id, role, matching_agents)
                else:
                    resolved_agent_id = matching_agents[0]

            # 4. Fetch and Validate AgentDefinition
            if not agent_registry.has_agent(resolved_agent_id):
                raise UnresolvedAgentAssignmentError(
                    node_id,
                    resolved_agent_id,
                    p_id,
                    f"Agent '{resolved_agent_id}' is declared in program manifest but not found in AgentRegistry",
                )

            agent = agent_registry.get(resolved_agent_id)

            # 5. Validate Authority Lane Invariant
            if agent.authority_lane.value != role:
                raise LaneBindingMismatchError(
                    node_id,
                    agent.agent_id,
                    agent.authority_lane.value,
                    role,
                )

            # 6. Validate Skills Compatibility
            node_required_skills = tuple(sorted(node.get("skills", node.get("required_skills", []))))
            agent_skill_names = {s.name for s in agent.skills}
            for req_skill in node_required_skills:
                if req_skill not in agent_skill_names and req_skill not in p_skills:
                    raise IncompatibleSkillBindingError(node_id, agent.agent_id, [req_skill])

            # 7. Validate Tools & Capability Grants
            node_required_tools = tuple(sorted(node.get("tool_ids", node.get("tools", []))))
            agent_tools = set(agent.tools)
            for cap in agent.capabilities:
                pass
            for req_tool in node_required_tools:
                if req_tool not in agent_tools and not req_tool.startswith("tool:default-"):
                    raise IncompatibleToolBindingError(node_id, agent.agent_id, [req_tool])

            # 8. Validate Output Contracts
            node_output_contracts = node.get("output_contracts", [])
            effective_output_contracts: List[str] = []
            if node_output_contracts:
                effective_output_contracts = list(node_output_contracts)
            elif agent.output_contract:
                effective_output_contracts = [agent.output_contract.contract_id]
            else:
                raise UnresolvedOutputContractError(
                    node_id,
                    agent.agent_id,
                    "Neither the workflow node nor the assigned Agent declares a typed output contract",
                )

            # 9. Compute Assignment Digest
            content_sha = agent.content_sha256 or agent.compute_content_sha256()
            assignment_partial = {
                "node_id": node_id,
                "phase_id": phase_id,
                "phase_order": phase_order,
                "actor_kind": actor_kind,
                "role": role,
                "lane": agent.authority_lane.value,
                "agent_id": agent.agent_id,
                "agent_version": agent.version,
                "agent_content_sha256": content_sha,
                "bound_skills": list(node_required_skills),
                "bound_tools": list(node_required_tools),
                "output_contracts": sorted(effective_output_contracts),
            }
            binding_sha = canonical_sha256(assignment_partial)

            assignment = CompiledAgentNodeAssignment(
                node_id=node_id,
                phase_id=phase_id,
                phase_order=phase_order,
                actor_kind=actor_kind,
                role=role,
                lane=agent.authority_lane,
                agent_id=agent.agent_id,
                agent_version=agent.version,
                agent_content_sha256=content_sha,
                bound_skills=node_required_skills,
                bound_tools=node_required_tools,
                output_contracts=tuple(sorted(effective_output_contracts)),
                binding_sha256=binding_sha,
            )
            assignments.append(assignment)

        # 10. Construct Manifest Binding
        created_at = utc_now_rfc3339()
        manifest_id = f"prog_bind_{hashlib.sha256(f'{p_id}:{p_ver}:{created_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        manifest_partial = {
            "manifest_id": manifest_id,
            "program_id": p_id,
            "program_version": p_ver,
            "program_manifest_sha256": p_sha,
            "state_machine_id": p_state_machine,
            "node_assignments": [a.canonical_dict() for a in assignments],
            "created_at": created_at,
        }
        manifest_sha = canonical_sha256(manifest_partial)

        return ProgramAgentPhaseBindingManifest(
            manifest_id=manifest_id,
            program_id=p_id,
            program_version=p_ver,
            program_manifest_sha256=p_sha,
            state_machine_id=p_state_machine,
            node_assignments=tuple(assignments),
            manifest_binding_sha256=manifest_sha,
            compiled_at=created_at,
        )
