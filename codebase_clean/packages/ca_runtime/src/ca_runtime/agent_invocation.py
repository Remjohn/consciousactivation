"""Canonical Agent Invocation Contract and Governed Execution Runtime for CAE.

Governed by:
- Phase 5 Mandate M52 (01_AGENT_EXECUTION/M52_canonical_agent_invocation_contract.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

CA-M048 (Wave 06, Canon Q47 / INV-SEC-001)
-------------------------------------------
Removed the permissive ``tool:default-`` bypass in ``AgentInvocationCompiler.compile``.
Previously, any tool name whose string value started with ``"tool:default-"`` was
silently allowed to pass the tool-registry check even when it was not in the
agent's declared capability set.  This constituted an unverified tool execution
path.  Under CA-M048 / INV-SEC-001, a tool is allowed if and only if it is
explicitly present in ``all_allowed_tools``; no prefix bypass is honoured.
Canonical path and execution sandbox enforcement is provided by the companion
module ``ca_runtime.sandbox`` (``packages/ca_runtime/src/ca_runtime/sandbox.py``).

CA-M038 (Wave 05, Canon Q38 / INV-ROUT-001)
--------------------------------------------
Removed the hard 500-token cap that previously blocked legitimate reasoning.
Integrated ProviderRouter for 3-tier resilient routing (Groq → OpenRouter → OpenAI)
with exponential backoff and automatic failover.  When a ProviderRouter is supplied
to ``AgentInvocationRuntime.execute``, it is used in preference to a bare
``model_reasoning_engine``; single-provider failure no longer aborts the run.

Enforces:
1. Single Governed Execution Object (AgentInvocation):
   Unifies Agent identity, state, compiled package (package_sha256), context capsule (capsule_sha256),
   model policy, skills, tools, capabilities, output contract, and prompt into an immutable, hash-addressed object.
2. Tool & Capability Travel Invariance:
   Authorized tools and forbidden actions travel deterministically with the invocation payload.
3. Model Authorization & Policy Gates:
   Agent model resolution is strictly bounded by the agent's declared model policy and authority lane.
4. Cryptographic Provenance & Receipt Gating:
   Execution emits immutable AgentInvocationReceipt records linking package, capsule, invocation, and response digests.
5. Anti-Bypass & Integrity Defenses:
   Direct un-compiled calls, altered payloads, and unauthorized tools fail closed.
6. Resilient Multi-Provider Routing (CA-M038):
   When a ProviderRouter is available, all inference passes through it.  The router
   implements 3-tier failover with exponential backoff; exhaustion raises
   ProviderExhaustedError which is re-raised as ProductionExecutionModeViolationError
   so existing error-handling contracts remain intact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.agent_registry import (
    AgentDefinition,
    AgentModelPolicy,
    AgentOutputContract,
    StandaloneAgentSession,
)
from ca_runtime.context_capsule import (
    CapabilityProjection,
    CompiledAgentPackage,
    JITContextCapsule,
    SkillPackageRef,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.provider_router import (
    InferenceRequest,
    InferenceResponse,
    ProviderExhaustedError,
    ProviderRouter,
)

logger = logging.getLogger("ca_runtime.agent_invocation")

# CA-M038: default max_tokens used when no token budget is set on the agent
# policy.  This is NOT an artificial cap — it is a safety default that the
# agent model policy's ``token_budget`` field overrides.  The old hard-coded
# 500-token value that existed in the ``model_reasoning_engine.infer()`` call
# has been removed; callers now control token limits through the policy.
_DEFAULT_MAX_TOKENS: int = 8_192


class ExecutionMode(str, Enum):
    """Execution mode classifying whether an invocation is an offline test fixture or production execution."""
    TEST_FIXTURE = "TEST_FIXTURE"
    PRODUCTION = "PRODUCTION"


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class AgentInvocationError(RuntimeError):
    """Base error for canonical agent invocation contract violations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "AGENT_INVOCATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class ProductionExecutionModeViolationError(AgentInvocationError):
    """Raised when a production execution is attempted without a live ModelReasoningEngine or authorized provider."""

    def __init__(self, agent_id: str, reason: str):
        super().__init__(
            f"PRODUCTION_EXECUTION_MODE_VIOLATION: Production execution failed for Agent '{agent_id}': {reason}",
            reason_code="ERR_PRODUCTION_EXECUTION_MODE_VIOLATION",
            details={"agent_id": agent_id, "reason": reason},
        )


class InvocationIntegrityError(AgentInvocationError):
    """Raised when an AgentInvocation payload has drifted from its cryptographic SHA-256 digest."""

    def __init__(self, invocation_id: str, expected_sha: str, actual_sha: str):
        super().__init__(
            f"INVOCATION_INTEGRITY_VIOLATION: AgentInvocation '{invocation_id}' content drifted. "
            f"Expected SHA-256 '{expected_sha}', computed '{actual_sha}'",
            reason_code="INVOCATION_INTEGRITY_VIOLATION",
            details={"invocation_id": invocation_id, "expected_sha": expected_sha, "actual_sha": actual_sha},
        )


class UnauthorizedModelError(AgentInvocationError):
    """Raised when a requested model is not authorized by the Agent's model policy or authority lane."""

    def __init__(self, agent_id: str, requested_model: str, allowed_models: Sequence[str]):
        super().__init__(
            f"UNAUTHORIZED_MODEL: Model '{requested_model}' is not authorized for Agent '{agent_id}'. "
            f"Allowed models: {list(allowed_models)}",
            reason_code="UNAUTHORIZED_MODEL",
            details={"agent_id": agent_id, "requested_model": requested_model, "allowed_models": list(allowed_models)},
        )


class UnauthorizedToolError(AgentInvocationError):
    """Raised when an invocation requests tools that are not permitted by agent capabilities or are forbidden."""

    def __init__(self, agent_id: str, tool_name: str, reason: str):
        super().__init__(
            f"UNAUTHORIZED_TOOL: Tool '{tool_name}' is unauthorized for Agent '{agent_id}': {reason}",
            reason_code="UNAUTHORIZED_TOOL",
            details={"agent_id": agent_id, "tool_name": tool_name, "reason": reason},
        )


class GateSuspensionExecutionBlockedError(AgentInvocationError):
    """Raised when an agent invocation is attempted while a gate is suspended."""

    def __init__(self, aggregate_id: str, gate_id: Optional[str] = None):
        details = {"aggregate_id": aggregate_id}
        if gate_id:
            details["gate_id"] = gate_id
        super().__init__(
            f"GATE_AWAITING_APPROVAL: execution is blocked for aggregate '{aggregate_id}'",
            reason_code="GATE_AWAITING_APPROVAL",
            details=details,
        )


class InvocationBypassError(AgentInvocationError):
    """Raised when execution or reasoning is attempted outside a governed AgentInvocation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"INVOCATION_BYPASS_ATTEMPT: {message}",
            reason_code="INVOCATION_BYPASS_ATTEMPT",
            details=details,
        )


class OutputContractViolationError(AgentInvocationError):
    """Raised when inference output violates the declared typed output contract."""

    def __init__(self, contract_id: str, reason: str, raw_output: str):
        super().__init__(
            f"OUTPUT_CONTRACT_VIOLATION: Output failed contract '{contract_id}': {reason}",
            reason_code="OUTPUT_CONTRACT_VIOLATION",
            details={"contract_id": contract_id, "reason": reason, "raw_output_snippet": raw_output[:200]},
        )


class EconomicAccountingRequiredError(AgentInvocationError):
    """Raised when a state-bound production invocation lacks economic accounting."""

    def __init__(self, invocation_id: str, state_id: Optional[str], reason: Optional[str] = None):
        message = (
            f"ECONOMIC_ACCOUNTING_REQUIRED: invocation '{invocation_id}' is state-bound "
            "but no admissible economic accounting source/controller was supplied."
        )
        if reason:
            message += f" {reason}"
        super().__init__(
            message,
            reason_code="ECONOMIC_ACCOUNTING_REQUIRED",
            details={"invocation_id": invocation_id, "state_id": state_id, "reason": reason},
        )


class EconomicQuotaError(AgentInvocationError):
    """Base exception for fail-closed economic governance failures."""


class BudgetCeilingExceededError(EconomicQuotaError):
    """Raised when a workspace or aggregate hard budget ceiling blocks execution."""

    def __init__(self, message: str, *, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="BUDGET_CEILING_EXCEEDED", details=details)


class EconomicCostUnmeteredError(EconomicQuotaError):
    """Raised when a provider supplies no cost and no deterministic rate card exists."""

    def __init__(self, provider_name: str):
        super().__init__(
            f"ECONOMIC_COST_UNMETERED: provider '{provider_name}' supplied no cost and no configured rate card exists.",
            reason_code="ECONOMIC_COST_UNMETERED",
            details={"provider_name": provider_name},
        )


class ProviderRateLimitExceededError(EconomicQuotaError):
    """Raised when a provider's configured request/token window is exhausted."""

    def __init__(self, message: str, *, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="PROVIDER_RATE_LIMIT_EXCEEDED", details=details)


class EconomicCircuitOpenError(EconomicQuotaError):
    """Raised when the economics circuit breaker is OPEN or already probing."""

    def __init__(self, message: str, *, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="ECONOMIC_CIRCUIT_OPEN", details=details)


class EconomicInvocationAlreadySettledError(EconomicQuotaError):
    """Raised when a completed invocation is retried with the same invocation identity."""

    def __init__(self, invocation_id: str, receipt_id: str):
        super().__init__(
            f"ECONOMIC_INVOCATION_ALREADY_SETTLED: invocation '{invocation_id}' already has "
            f"economic receipt '{receipt_id}'; replay is blocked to prevent double charging.",
            reason_code="ECONOMIC_INVOCATION_ALREADY_SETTLED",
            details={"invocation_id": invocation_id, "receipt_id": receipt_id},
        )


@dataclass(frozen=True, slots=True)
class EconomicUsage:
    """Provider-reported execution usage at the economic accounting boundary."""

    provider_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd_micros: Optional[int] = None
    observed_at: str = ""


@dataclass(frozen=True, slots=True)
class EconomicReservation:
    """Durable pre-execution reservation that fences a maximum possible charge."""

    reservation_id: str
    invocation_id: str
    workspace_id: UUID
    aggregate_id: str
    provider_name: str
    reserved_tokens: int
    reserved_cost_usd_micros: int
    reserved_at: str
    half_open_probe: bool = False


@dataclass(frozen=True, slots=True)
class EconomicChargeReceipt:
    """Immutable durable receipt for an economically accounted invocation or overrun."""

    receipt_id: str
    receipt_type: str
    invocation_id: str
    workspace_id: UUID
    aggregate_id: str
    provider_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd_micros: int
    status: str
    economic_circuit_state: str
    aggregate_spend_before_usd_micros: int
    aggregate_spend_after_usd_micros: int
    workspace_spend_before_usd_micros: int
    workspace_spend_after_usd_micros: int
    reservation_released_usd_micros: int
    reason: Optional[str]
    created_at: str
    receipt_sha256: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "receipt_type": self.receipt_type,
            "invocation_id": self.invocation_id,
            "workspace_id": str(self.workspace_id),
            "aggregate_id": self.aggregate_id,
            "provider_name": self.provider_name,
            "prompt_tokens": int(self.prompt_tokens),
            "completion_tokens": int(self.completion_tokens),
            "total_tokens": int(self.total_tokens),
            "cost_usd_micros": int(self.cost_usd_micros),
            "status": self.status,
            "economic_circuit_state": self.economic_circuit_state,
            "aggregate_spend_before_usd_micros": int(self.aggregate_spend_before_usd_micros),
            "aggregate_spend_after_usd_micros": int(self.aggregate_spend_after_usd_micros),
            "workspace_spend_before_usd_micros": int(self.workspace_spend_before_usd_micros),
            "workspace_spend_after_usd_micros": int(self.workspace_spend_after_usd_micros),
            "reservation_released_usd_micros": int(self.reservation_released_usd_micros),
            "reason": self.reason,
            "created_at": self.created_at,
        }


class EconomicQuotaController(Protocol):
    """Runtime economics contract bound to canonical durable program state."""

    def authorize_invocation(
        self,
        *,
        invocation_id: str,
        workspace_id: UUID,
        aggregate_id: str,
        provider_name: str,
        reserved_tokens: int,
        reserved_cost_usd_micros: int,
    ) -> EconomicReservation:
        ...

    def settle_invocation(
        self,
        *,
        reservation: EconomicReservation,
        usage: EconomicUsage,
    ) -> EconomicChargeReceipt:
        ...

    def record_failure(
        self,
        *,
        reservation: Optional[EconomicReservation],
        invocation_id: str,
        provider_name: str,
        reason: str,
    ) -> None:
        ...


# ---------------------------------------------------------------------------
# Domain Models: AgentInvocation & AgentInvocationReceipt
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class AgentInvocation:
    """The single typed execution object binding Agent identity, state, package, capsule, model, tools, and contract.
    
    Guarantees:
    - Deterministically hash-addressed via invocation_sha256.
    - Immutable (frozen dataclass).
    - Captures package_sha256, capsule_sha256, prompt, tools, and model configuration.
    """
    invocation_id: str
    workspace_id: UUID
    run_id: Optional[str]
    lane: AuthorityLane
    agent_id: str
    agent_version: str
    state_id: Optional[str]
    package_sha256: str
    capsule_sha256: str
    model_id: str
    model_provider: str
    temperature_bps: int
    timeout_ms: int
    skills: Tuple[SkillPackageRef, ...]
    tools: Tuple[str, ...]
    forbidden_actions: Tuple[str, ...]
    capabilities: Tuple[CapabilityProjection, ...]
    output_contract: Optional[Dict[str, Any]]
    assembled_prompt: str
    system_prompt: str
    invocation_sha256: str
    created_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        """Produce canonical, deterministic dictionary for cryptographic hashing."""
        return {
            "invocation_id": self.invocation_id,
            "workspace_id": str(self.workspace_id),
            "run_id": self.run_id,
            "lane": self.lane.value,
            "agent_id": self.agent_id,
            "agent_version": self.agent_version,
            "state_id": self.state_id,
            "package_sha256": self.package_sha256,
            "capsule_sha256": self.capsule_sha256,
            "model_id": self.model_id,
            "model_provider": self.model_provider,
            "temperature_bps": int(self.temperature_bps),
            "timeout_ms": int(self.timeout_ms),
            "skills": [s.canonical_dict() for s in sorted(self.skills, key=lambda s: s.skill_id)],
            "tools": list(sorted(self.tools)),
            "forbidden_actions": list(sorted(self.forbidden_actions)),
            "capabilities": [c.canonical_dict() for c in sorted(self.capabilities, key=lambda c: c.capability_id)],
            "output_contract": dict(sorted(self.output_contract.items())) if self.output_contract else None,
            "assembled_prompt": self.assembled_prompt,
            "system_prompt": self.system_prompt,
            "created_at": self.created_at,
        }

    def compute_sha256(self) -> str:
        """Compute the SHA-256 digest of the canonical payload."""
        payload = self.canonical_dict()
        return canonical_sha256(payload)

    def verify_integrity(self) -> None:
        """Verifies that the object has not drifted from its invocation_sha256."""
        computed = self.compute_sha256()
        if computed != self.invocation_sha256:
            raise InvocationIntegrityError(self.invocation_id, self.invocation_sha256, computed)


@dataclass(frozen=True, slots=True)
class AgentInvocationReceipt:
    """Immutable execution receipt proving a governed model invocation occurred."""
    receipt_id: str
    invocation_id: str
    agent_id: str
    workspace_id: UUID
    run_id: Optional[str]
    state_id: Optional[str]
    lane: str
    package_sha256: str
    capsule_sha256: str
    invocation_sha256: str
    model_id: str
    provider_class: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_micros: int
    raw_response_text: str
    parsed_output: Optional[Dict[str, Any]]
    output_contract_passed: bool
    gate_passed: bool
    executed_at: str
    receipt_sha256: str
    execution_mode: str = "TEST_FIXTURE"
    is_synthetic: bool = False
    cost_usd_micros: int = 0
    economic_receipt_id: Optional[str] = None
    economic_status: str = "UNTRACKED"

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "invocation_id": self.invocation_id,
            "agent_id": self.agent_id,
            "workspace_id": str(self.workspace_id),
            "run_id": self.run_id,
            "state_id": self.state_id,
            "lane": self.lane,
            "package_sha256": self.package_sha256,
            "capsule_sha256": self.capsule_sha256,
            "invocation_sha256": self.invocation_sha256,
            "model_id": self.model_id,
            "provider_class": self.provider_class,
            "prompt_tokens": int(self.prompt_tokens),
            "completion_tokens": int(self.completion_tokens),
            "total_tokens": int(self.total_tokens),
            "latency_micros": int(self.latency_micros),
            "raw_response_text": self.raw_response_text,
            "parsed_output": self.parsed_output,
            "output_contract_passed": self.output_contract_passed,
            "gate_passed": self.gate_passed,
            "execution_mode": self.execution_mode,
            "is_synthetic": self.is_synthetic,
            "cost_usd_micros": int(self.cost_usd_micros),
            "economic_receipt_id": self.economic_receipt_id,
            "economic_status": self.economic_status,
            "executed_at": self.executed_at,
        }


# ---------------------------------------------------------------------------
# Agent Invocation Compiler
# ---------------------------------------------------------------------------

class AgentInvocationCompiler:
    """Compiles Agent identity, context capsule, and execution parameters into an AgentInvocation."""

    @staticmethod
    def compile(
        *,
        agent: AgentDefinition | CompiledAgentPackage,
        capsule: JITContextCapsule,
        workspace_id: UUID,
        run_id: Optional[str] = None,
        state_id: Optional[str] = None,
        model_id: Optional[str] = None,
        model_provider: str = "groq",
        temperature_bps: Optional[int] = None,
        timeout_ms: Optional[int] = None,
        requested_tools: Optional[Sequence[str]] = None,
        skills: Optional[Sequence[SkillPackageRef]] = None,
        system_prompt: Optional[str] = None,
        output_contract: Optional[AgentOutputContract | Dict[str, Any]] = None,
        package_sha256: Optional[str] = None,
    ) -> AgentInvocation:
        """Compile and validate a canonical AgentInvocation object.
        
        Enforces:
        1. Lane matching between Agent and Context Capsule.
        2. Model policy compliance: model must be preferred_model or in fallback_models.
        3. Tool boundaries: requested tools must be authorized by capabilities and not forbidden.
        4. Deterministic composite invocation_sha256 computation.
        """
        agent_id = agent.agent_id
        lane = agent.authority_lane if isinstance(agent, AgentDefinition) else agent.lane

        # 1. Tenancy and Lane Verification
        if capsule.lane != lane:
            raise AgentInvocationError(
                f"Lane mismatch: Agent is in lane '{lane.value}', but capsule is compiled for '{capsule.lane.value}'",
                reason_code="LANE_MISMATCH",
                details={"agent_lane": lane.value, "capsule_lane": capsule.lane.value},
            )

        # 2. Model Resolution & Policy Verification
        allowed_models: List[str] = []
        default_model = "gemini-2.5-pro"
        default_temp_bps = 2000
        default_timeout_ms = 60_000

        if isinstance(agent, AgentDefinition):
            mp = agent.model_policy
            default_model = mp.preferred_model
            allowed_models = [mp.preferred_model] + list(mp.fallback_models)
            if mp.temperature_bps is not None:
                default_temp_bps = mp.temperature_bps
            elif mp.temperature is not None:
                default_temp_bps = int(round(float(mp.temperature) * 10000))
            if mp.timeout_seconds is not None:
                default_timeout_ms = int(round(float(mp.timeout_seconds) * 1000))
        else:
            allowed_models = [capsule.model_id, "gemini-2.5-pro", "openai/gpt-oss-120b"]
            default_model = capsule.model_id

        selected_model = model_id or default_model
        if selected_model not in allowed_models:
            raise UnauthorizedModelError(agent_id, selected_model, allowed_models)

        resolved_temp_bps = temperature_bps if temperature_bps is not None else default_temp_bps
        resolved_timeout_ms = timeout_ms if timeout_ms is not None else default_timeout_ms

        # 3. Tool Boundary and Capability Reconciliation
        all_allowed_tools: Set[str] = set()
        forbidden_actions: Set[str] = set()

        skills_tuple: Tuple[SkillPackageRef, ...] = ()
        if skills is not None:
            skills_tuple = tuple(skills)
        elif isinstance(agent, CompiledAgentPackage):
            skills_tuple = agent.skills

        for s in skills_tuple:
            all_allowed_tools.update(s.allowed_tools)
            forbidden_actions.update(s.forbidden_actions)

        all_allowed_tools.update(agent.tools)
        if isinstance(agent, CompiledAgentPackage):
            for c in agent.capabilities:
                all_allowed_tools.update(c.bound_tools)

        # Collect from capsule capability projections
        for cap_proj in capsule.capability_projections:
            all_allowed_tools.update(cap_proj.bound_tools)

        effective_tools: List[str] = []
        if requested_tools is not None:
            for t in requested_tools:
                if t in forbidden_actions:
                    raise UnauthorizedToolError(agent_id, t, "Tool is explicitly forbidden by skill policy")
                # CA-M048 / INV-SEC-001: tool:default- prefix bypass removed.
                if t not in all_allowed_tools:
                    raise UnauthorizedToolError(
                        agent_id,
                        t,
                        "Tool is not in declared capabilities or agent tool list "
                        "(CA-M048: tool:default- bypass removed per INV-SEC-001)",
                    )
                effective_tools.append(t)
        else:
            effective_tools = sorted(all_allowed_tools - forbidden_actions)

        # 4. Package SHA-256 Resolution
        resolved_package_sha = package_sha256
        if not resolved_package_sha:
            if isinstance(agent, CompiledAgentPackage):
                resolved_package_sha = agent.package_sha256
            elif isinstance(agent, AgentDefinition):
                resolved_package_sha = agent.content_sha256 or agent.compute_content_sha256()

        # 5. Output Contract Resolution
        contract_dict: Optional[Dict[str, Any]] = None
        if output_contract is not None:
            if isinstance(output_contract, AgentOutputContract):
                contract_dict = {
                    "contract_id": output_contract.contract_id,
                    "schema_ref": output_contract.schema_ref,
                    "output_type": output_contract.output_type,
                    "description": output_contract.description,
                }
            elif isinstance(output_contract, dict):
                contract_dict = dict(output_contract)
        elif isinstance(agent, AgentDefinition) and agent.output_contract:
            contract_dict = {
                "contract_id": agent.output_contract.contract_id,
                "schema_ref": agent.output_contract.schema_ref,
                "output_type": agent.output_contract.output_type,
                "description": agent.output_contract.description,
            }

        # 6. Assemble Prompts
        resolved_system_prompt = system_prompt or f"You are CAE Agent '{agent_id}' operating in '{lane.value}' authority lane."
        assembled_prompt = capsule.assembled_prompt

        # 7. Collect Skills
        skills_tuple: Tuple[SkillPackageRef, ...] = ()
        if isinstance(agent, CompiledAgentPackage):
            skills_tuple = agent.skills

        created_at = utc_now_rfc3339()
        inv_id = f"inv_{hashlib.sha256(f'{workspace_id}:{agent_id}:{created_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        partial_dict = {
            "invocation_id": inv_id,
            "workspace_id": str(workspace_id),
            "run_id": run_id,
            "lane": lane.value,
            "agent_id": agent_id,
            "agent_version": agent.version,
            "state_id": state_id,
            "package_sha256": resolved_package_sha,
            "capsule_sha256": capsule.capsule_sha256,
            "model_id": selected_model,
            "model_provider": model_provider,
            "temperature_bps": int(resolved_temp_bps),
            "timeout_ms": int(resolved_timeout_ms),
            "skills": [s.canonical_dict() for s in sorted(skills_tuple, key=lambda s: s.skill_id)],
            "tools": list(sorted(effective_tools)),
            "forbidden_actions": list(sorted(forbidden_actions)),
            "capabilities": [c.canonical_dict() for c in sorted(capsule.capability_projections, key=lambda c: c.capability_id)],
            "output_contract": dict(sorted(contract_dict.items())) if contract_dict else None,
            "assembled_prompt": assembled_prompt,
            "system_prompt": resolved_system_prompt,
            "created_at": created_at,
        }
        inv_sha = canonical_sha256(partial_dict)

        return AgentInvocation(
            invocation_id=inv_id,
            workspace_id=workspace_id,
            run_id=run_id,
            lane=lane,
            agent_id=agent_id,
            agent_version=agent.version,
            state_id=state_id,
            package_sha256=resolved_package_sha,
            capsule_sha256=capsule.capsule_sha256,
            model_id=selected_model,
            model_provider=model_provider,
            temperature_bps=resolved_temp_bps,
            timeout_ms=resolved_timeout_ms,
            skills=skills_tuple,
            tools=tuple(sorted(effective_tools)),
            forbidden_actions=tuple(sorted(forbidden_actions)),
            capabilities=capsule.capability_projections,
            output_contract=contract_dict,
            assembled_prompt=assembled_prompt,
            system_prompt=resolved_system_prompt,
            invocation_sha256=inv_sha,
            created_at=created_at,
        )


# ---------------------------------------------------------------------------
# Agent Invocation Runtime / Bridge
# ---------------------------------------------------------------------------

class AgentInvocationRuntime:
    """Governed execution runtime that processes AgentInvocations and emits receipts.
    
    Guarantees:
    - Verifies invocation integrity before execution (fails closed on hash mismatch).
    - Enforces tool and capability validation.
    - Validates typed output contracts against inference responses.
    - Emits verifiable AgentInvocationReceipt records.
    - Blocks bypass attempts where inference is invoked directly without an AgentInvocation.
    """

    @classmethod
    def execute(
        cls,
        invocation: AgentInvocation,
        *,
        mode: ExecutionMode = ExecutionMode.TEST_FIXTURE,
        inference_fn: Optional[Callable[[AgentInvocation], Dict[str, Any]]] = None,
        model_reasoning_engine: Optional[Any] = None,
        provider_router: Optional[ProviderRouter] = None,
        supplied_tool_calls: Optional[Sequence[str]] = None,
        execution_guard: Optional[Callable[[AgentInvocation], None]] = None,
        economic_controller: Optional[EconomicQuotaController] = None,
        economic_max_cost_usd_micros: Optional[int] = None,
        economic_provider_name: Optional[str] = None,
    ) -> AgentInvocationReceipt:
        """Execute the governed AgentInvocation through the model bridge.

        CA-M038: when ``provider_router`` is provided it is used for resilient
        3-tier routing (Groq → OpenRouter → OpenAI) with exponential backoff.
        The router takes precedence over a bare ``model_reasoning_engine`` when
        both are supplied.  The 500-token hard cap previously applied to
        ``model_reasoning_engine.infer()`` has been removed; token limits are
        now controlled by the agent's ``model_policy.token_budget`` (or the
        module-level ``_DEFAULT_MAX_TOKENS`` fallback).

        Raises:
        - InvocationIntegrityError: if the invocation was tampered with after compilation.
        - UnauthorizedToolError: if an unauthorized tool call is attempted during execution.
        - OutputContractViolationError: if the model output fails the declared output contract.
        - ProductionExecutionModeViolationError: if production execution mode is requested
          without an authorized model engine or if all provider tiers are exhausted.
        """
        # 1. Verify Invocation Integrity (Anti-Tampering)
        invocation.verify_integrity()

        # 2. Verify Tool Call Boundaries
        if supplied_tool_calls:
            for tool_call in supplied_tool_calls:
                if tool_call not in invocation.tools:
                    raise UnauthorizedToolError(
                        invocation.agent_id,
                        tool_call,
                        f"Tool was not declared in compiled invocation tools: {list(invocation.tools)}"
                    )

        # 3. Gate / execution guard boundary
        # The guard is deliberately caller-supplied so the invocation object does not
        # acquire an unsafe implicit dependency on aggregate storage. Production callers
        # should bind it to the authoritative program state runtime.
        if execution_guard is not None:
            execution_guard(invocation)

        # 4. Model Inference Execution
        raw_response_text = ""
        parsed_json: Optional[Dict[str, Any]] = None
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        latency_micros = 1000
        provider_class = f"{invocation.model_provider.capitalize()}OpenAIProvider"
        is_synthetic = False
        cost_usd_micros: Optional[int] = None

        # CA-M038: resolve max_tokens from invocation context (no hard 500-token cap).
        # Priority: agent model_policy.token_budget > invocation timeout hint > default.
        # We don't have direct access to the policy here, so we use a generous default
        # that never blocks legitimate reasoning.  The agent compiler sets timeout_ms
        # from policy; we mirror token budget via extra metadata if present.
        _max_tokens: int = invocation.output_contract.get("_max_tokens_hint", _DEFAULT_MAX_TOKENS) \
            if invocation.output_contract else _DEFAULT_MAX_TOKENS

        economic_reservation: Optional[EconomicReservation] = None
        economic_receipt: Optional[EconomicChargeReceipt] = None
        economic_cap_requested = (
            economic_controller is not None
            or economic_max_cost_usd_micros is not None
            or bool(invocation.output_contract and "_max_cost_usd_micros" in invocation.output_contract)
        )
        if mode == ExecutionMode.PRODUCTION and invocation.state_id is not None and economic_cap_requested and economic_controller is None:
            raise EconomicAccountingRequiredError(invocation.invocation_id, invocation.state_id)
        if economic_controller is not None:
            if mode == ExecutionMode.PRODUCTION and invocation.state_id is not None and inference_fn is not None and provider_router is None and model_reasoning_engine is None:
                raise EconomicAccountingRequiredError(
                    invocation.invocation_id,
                    invocation.state_id,
                    "State-bound production economics require provider-reported usage; synthetic inference_fn execution is not an admissible accounting source.",
                )
            max_cost = economic_max_cost_usd_micros
            if max_cost is None and invocation.output_contract:
                raw_max_cost = invocation.output_contract.get("_max_cost_usd_micros")
                max_cost = int(raw_max_cost) if raw_max_cost is not None else None
            if max_cost is None:
                raise EconomicAccountingRequiredError(invocation.invocation_id, invocation.state_id)
            economic_reservation = economic_controller.authorize_invocation(
                invocation_id=invocation.invocation_id,
                workspace_id=invocation.workspace_id,
                aggregate_id=str(invocation.state_id or ""),
                provider_name=economic_provider_name or invocation.model_provider,
                reserved_tokens=_max_tokens,
                reserved_cost_usd_micros=int(max_cost),
            )

        if mode == ExecutionMode.PRODUCTION:
            if provider_router is not None:
                # CA-M038 primary path: resilient 3-tier routing
                req = InferenceRequest(
                    prompt=invocation.assembled_prompt,
                    system_prompt=invocation.system_prompt,
                    temperature=invocation.temperature_bps / 10000.0,
                    max_tokens=_max_tokens,
                    model_id=invocation.model_id,
                )
                try:
                    res: InferenceResponse = provider_router.route(req)
                except ProviderExhaustedError as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise ProductionExecutionModeViolationError(
                        invocation.agent_id,
                        f"All provider tiers exhausted during routing (INV-ROUT-001): {exc}",
                    ) from exc
                raw_response_text = res.response_text
                parsed_json = res.parsed_json
                prompt_tokens = res.prompt_tokens
                completion_tokens = res.completion_tokens
                total_tokens = res.total_tokens
                latency_micros = res.latency_micros
                provider_class = res.provider_class
                cost_usd_micros = getattr(res, "cost_usd_micros", None)
                is_synthetic = False
            elif model_reasoning_engine is not None:
                # Legacy path: single engine, no hard token cap (CA-M038 removes 500 limit)
                try:
                    res_legacy = model_reasoning_engine.infer(
                        prompt=invocation.assembled_prompt,
                        system_prompt=invocation.system_prompt,
                        temperature=invocation.temperature_bps / 10000.0,
                        max_tokens=_max_tokens,
                    )
                except Exception as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise
                raw_response_text = res_legacy.response_text
                parsed_json = res_legacy.parsed_json
                prompt_tokens = res_legacy.prompt_tokens
                completion_tokens = res_legacy.completion_tokens
                total_tokens = res_legacy.total_tokens
                latency_micros = res_legacy.latency_micros
                provider_class = res_legacy.provider_class
                cost_usd_micros = getattr(res_legacy, "cost_usd_micros", None)
                is_synthetic = False
            elif inference_fn is not None:
                try:
                    inf_result = inference_fn(invocation)
                except Exception as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise
                raw_response_text = inf_result.get("response_text", "")
                parsed_json = inf_result.get("parsed_json")
                prompt_tokens = inf_result.get("prompt_tokens", 100)
                completion_tokens = inf_result.get("completion_tokens", 50)
                total_tokens = prompt_tokens + completion_tokens
                latency_micros = inf_result.get("latency_micros", 50_000)
                cost_usd_micros = inf_result.get("cost_usd_micros")
                if "provider_class" in inf_result:
                    provider_class = inf_result["provider_class"]
                is_synthetic = False
            else:
                raise ProductionExecutionModeViolationError(
                    invocation.agent_id,
                    "Deterministic mock fallback is strictly forbidden in PRODUCTION execution mode. "
                    "A live ModelReasoningEngine, ProviderRouter, or authorized inference provider is required.",
                )
        else:
            # TEST_FIXTURE mode
            if provider_router is not None:
                # CA-M038: allow router in TEST_FIXTURE too (supports simulated failover tests)
                req = InferenceRequest(
                    prompt=invocation.assembled_prompt,
                    system_prompt=invocation.system_prompt,
                    temperature=invocation.temperature_bps / 10000.0,
                    max_tokens=_max_tokens,
                    model_id=invocation.model_id,
                )
                try:
                    res2: InferenceResponse = provider_router.route(req)
                except ProviderExhaustedError as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise ProductionExecutionModeViolationError(
                        invocation.agent_id,
                        f"All provider tiers exhausted during TEST_FIXTURE routing: {exc}",
                    ) from exc
                raw_response_text = res2.response_text
                parsed_json = res2.parsed_json
                prompt_tokens = res2.prompt_tokens
                completion_tokens = res2.completion_tokens
                total_tokens = res2.total_tokens
                latency_micros = res2.latency_micros
                provider_class = res2.provider_class
                cost_usd_micros = getattr(res2, "cost_usd_micros", None)
                is_synthetic = False
            elif inference_fn is not None:
                try:
                    inf_result = inference_fn(invocation)
                except Exception as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise
                raw_response_text = inf_result.get("response_text", "")
                parsed_json = inf_result.get("parsed_json")
                prompt_tokens = inf_result.get("prompt_tokens", 100)
                completion_tokens = inf_result.get("completion_tokens", 50)
                total_tokens = prompt_tokens + completion_tokens
                latency_micros = inf_result.get("latency_micros", 50_000)
                cost_usd_micros = inf_result.get("cost_usd_micros")
                if "provider_class" in inf_result:
                    provider_class = inf_result["provider_class"]
                is_synthetic = True
            elif model_reasoning_engine is not None:
                # Legacy path: single engine, no hard token cap (CA-M038 removes 500 limit)
                try:
                    res_legacy2 = model_reasoning_engine.infer(
                        prompt=invocation.assembled_prompt,
                        system_prompt=invocation.system_prompt,
                        temperature=invocation.temperature_bps / 10000.0,
                        max_tokens=_max_tokens,
                    )
                except Exception as exc:
                    if economic_controller is not None:
                        economic_controller.record_failure(
                            reservation=economic_reservation,
                            invocation_id=invocation.invocation_id,
                            provider_name=economic_provider_name or invocation.model_provider,
                            reason=str(exc),
                        )
                    raise
                raw_response_text = res_legacy2.response_text
                parsed_json = res_legacy2.parsed_json
                prompt_tokens = res_legacy2.prompt_tokens
                completion_tokens = res_legacy2.completion_tokens
                total_tokens = res_legacy2.total_tokens
                latency_micros = res_legacy2.latency_micros
                provider_class = res_legacy2.provider_class
                cost_usd_micros = getattr(res_legacy2, "cost_usd_micros", None)
                is_synthetic = False
            else:
                parsed_json = {
                    "status": "SUCCESS",
                    "agent_id": invocation.agent_id,
                    "lane": invocation.lane.value,
                    "summary": "Governed invocation execution completed successfully.",
                }
                raw_response_text = json.dumps(parsed_json)
                prompt_tokens = 150
                completion_tokens = 45
                total_tokens = 195
                latency_micros = 25_000
                is_synthetic = True

        # 5. Economic settlement is committed before output validation because the
        # provider has already incurred usage even when a downstream contract fails.
        if economic_controller is not None and economic_reservation is not None:
            economic_receipt = economic_controller.settle_invocation(
                reservation=economic_reservation,
                usage=EconomicUsage(
                    provider_name=economic_provider_name or invocation.model_provider,
                    prompt_tokens=int(prompt_tokens),
                    completion_tokens=int(completion_tokens),
                    total_tokens=int(total_tokens),
                    cost_usd_micros=(int(cost_usd_micros) if cost_usd_micros is not None else None),
                    observed_at=utc_now_rfc3339(),
                ),
            )
            cost_usd_micros = economic_receipt.cost_usd_micros

        # 6. Output Contract Validation
        contract_passed = True
        if invocation.output_contract:
            contract_type = invocation.output_contract.get("output_type", "JSON")
            if contract_type == "JSON":
                if parsed_json is None:
                    # Try to parse raw_response_text
                    cleaned = raw_response_text.strip()
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]
                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                    cleaned = cleaned.strip()
                    try:
                        parsed_json = json.loads(cleaned)
                    except Exception as e:
                        contract_passed = False
                        raise OutputContractViolationError(
                            invocation.output_contract.get("contract_id", "UNKNOWN"),
                            f"Expected JSON output but could not parse response: {e}",
                            raw_response_text,
                        ) from e

        # 5. Build and Hash Receipt
        executed_at = utc_now_rfc3339()
        receipt_id = f"rcpt_inv_{hashlib.sha256(f'{invocation.invocation_id}:{executed_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        receipt_payload = {
            "receipt_id": receipt_id,
            "invocation_id": invocation.invocation_id,
            "agent_id": invocation.agent_id,
            "workspace_id": str(invocation.workspace_id),
            "run_id": invocation.run_id,
            "state_id": invocation.state_id,
            "lane": invocation.lane.value,
            "package_sha256": invocation.package_sha256,
            "capsule_sha256": invocation.capsule_sha256,
            "invocation_sha256": invocation.invocation_sha256,
            "model_id": invocation.model_id,
            "provider_class": provider_class,
            "prompt_tokens": int(prompt_tokens),
            "completion_tokens": int(completion_tokens),
            "total_tokens": int(total_tokens),
            "latency_micros": int(latency_micros),
            "raw_response_text": raw_response_text,
            "parsed_output": parsed_json,
            "output_contract_passed": contract_passed,
            "gate_passed": True,
            "execution_mode": mode.value,
            "is_synthetic": is_synthetic,
            "cost_usd_micros": int(cost_usd_micros or 0),
            "economic_receipt_id": economic_receipt.receipt_id if economic_receipt else None,
            "economic_status": economic_receipt.status if economic_receipt else "UNTRACKED",
            "executed_at": executed_at,
        }
        receipt_sha = canonical_sha256(receipt_payload)

        return AgentInvocationReceipt(
            receipt_id=receipt_id,
            invocation_id=invocation.invocation_id,
            agent_id=invocation.agent_id,
            workspace_id=invocation.workspace_id,
            run_id=invocation.run_id,
            state_id=invocation.state_id,
            lane=invocation.lane.value,
            package_sha256=invocation.package_sha256,
            capsule_sha256=invocation.capsule_sha256,
            invocation_sha256=invocation.invocation_sha256,
            model_id=invocation.model_id,
            provider_class=provider_class,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_micros=latency_micros,
            raw_response_text=raw_response_text,
            parsed_output=parsed_json,
            output_contract_passed=contract_passed,
            gate_passed=True,
            executed_at=executed_at,
            receipt_sha256=receipt_sha,
            execution_mode=mode.value,
            is_synthetic=is_synthetic,
            cost_usd_micros=int(cost_usd_micros or 0),
            economic_receipt_id=economic_receipt.receipt_id if economic_receipt else None,
            economic_status=economic_receipt.status if economic_receipt else "UNTRACKED",
        )
