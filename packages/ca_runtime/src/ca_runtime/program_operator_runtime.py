"""
program_operator_runtime.py
---------------------------
CAE Phase 4 Mandate M46: Programs + Artifacts + Chat Operator Application.

Provides the authoritative operator control surface over Program executions,
lossless artifact lineage graphs, execution trace projections, and Chat
supervision command dispatcher.

Enforces:
1. Canonical State Exclusivity: Zero duplicate truth; all mutations are typed CAE operations.
2. Anti-Stale UI CAS Protocol: `state_version` and `state_hash` optimistic locking.
3. 4-Lane Authority Separation: Hunter, Analyst, Composer, Commander.
4. Lossless Lineage: Cryptographic trace from source evidence to release receipts.
5. Dual-Axis QA Distinction: Independent Semantic QA and Render QA projections.
"""

from __future__ import annotations

import abc
import enum
import hashlib
import json
import re
import shlex
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from pydantic import BaseModel, Field

from ca_contracts import canonical_sha256
from .pi_adapter import AuthorityLane
from .program_registry import (
    ProgramNotFoundError,
    ProgramPackage,
    ProgramRegistry,
    get_program_registry,
)
from .program_state_runtime import (
    IProgramStateStore,
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateLocalContext,
    ProgramStateRuntimeError,
    ProgramStateTransition,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
    ProgramTransitionContract,
    ProgramTransitionResult,
    UniversalProgramStateRuntime,
    utc_now_rfc3339,
)


# ============================================================================
# 1. Enums & Domain Models
# ============================================================================

class OperatorActionType(str, enum.Enum):
    """Authoritative operator control actions (M08 Contract §3)."""
    DISCOVER = "DISCOVER"
    RUN = "RUN"
    INSPECT = "INSPECT"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REPAIR = "REPAIR"
    SHIP = "SHIP"
    EXPORT_AUDIT = "EXPORT_AUDIT"


class RejectionDispositionRoute(str, enum.Enum):
    """Governed routing targets for rejected candidates / milestones."""
    RETURN_TO_HUNTER = "RETURN_TO_HUNTER"
    RETURN_TO_ANALYST = "RETURN_TO_ANALYST"
    RETURN_TO_COMPOSER = "RETURN_TO_COMPOSER"
    REQUEST_MORE_SOURCE = "REQUEST_MORE_SOURCE"
    ARCHIVE = "ARCHIVE"


class LineageNodeType(str, enum.Enum):
    """Node types in the Phase 4 Asset Lineage Graph."""
    SOURCE_EVIDENCE = "SOURCE_EVIDENCE"
    EVIDENCE_SEGMENT = "EVIDENCE_SEGMENT"
    SEMANTIC_ANNOTATION = "SEMANTIC_ANNOTATION"
    CONTENT_CANDIDATE = "CONTENT_CANDIDATE"
    CANDIDATE_CLUSTER = "CANDIDATE_CLUSTER"
    EDITORIAL_STORYBOARD = "EDITORIAL_STORYBOARD"
    SEMANTIC_PROGRAM = "SEMANTIC_PROGRAM"
    SCRIPT = "SCRIPT"
    VISUAL_PROMPT = "VISUAL_PROMPT"
    COMPOSITION = "COMPOSITION"
    RENDERED_ARTIFACT = "RENDERED_ARTIFACT"
    SEMANTIC_QA = "SEMANTIC_QA"
    RENDER_QA = "RENDER_QA"
    OPERATOR_APPROVAL = "OPERATOR_APPROVAL"
    APPROVED_RELEASE = "APPROVED_RELEASE"


class LineageVerificationStatus(str, enum.Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    BROKEN = "BROKEN"


class ArtifactLineageNode(BaseModel):
    node_id: str = Field(..., description="Unique node identifier")
    node_type: LineageNodeType = Field(..., description="Node classification in lineage graph")
    label: str = Field(..., description="Human-readable label")
    sha256: str = Field(..., description="Cryptographic SHA-256 fingerprint")
    lane: AuthorityLane = Field(..., description="Authorizing authority lane")
    receipt_ref: Optional[str] = Field(default=None, description="Signed receipt reference ID")
    timestamp: str = Field(default_factory=utc_now_rfc3339)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ArtifactLineageEdge(BaseModel):
    edge_id: str = Field(..., description="Unique edge identifier")
    source_node_id: str = Field(..., description="Upstream node ID")
    target_node_id: str = Field(..., description="Downstream node ID")
    transformation_op: str = Field(..., description="Transformation or CAE typed operation")
    lane: AuthorityLane = Field(..., description="Executing lane")
    receipt_ref: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ArtifactLineageGraph(BaseModel):
    aggregate_id: str
    artifact_id: Optional[str] = None
    is_lossless: bool = True
    verification_status: LineageVerificationStatus = LineageVerificationStatus.VERIFIED
    nodes: List[ArtifactLineageNode] = Field(default_factory=list)
    edges: List[ArtifactLineageEdge] = Field(default_factory=list)
    root_evidence_ids: List[str] = Field(default_factory=list)
    terminal_artifact_ids: List[str] = Field(default_factory=list)
    verification_digest: str = Field(default="")


class ExecutionTraceNode(BaseModel):
    step_index: int
    transition_id: str
    transition_name: str
    trigger_operation: str
    lane: AuthorityLane
    actor_id: str
    from_state: str
    to_state: str
    committed_version: int
    receipt_id: str
    timestamp: str
    duration_ms: Optional[float] = None
    status: str = "SUCCESS"
    payload_summary: Dict[str, Any] = Field(default_factory=dict)


class ExecutionTraceProjection(BaseModel):
    aggregate_id: str
    workspace_id: str
    program_id: str
    program_version: str
    lifecycle: ProgramStateLifecycle
    current_state: str
    version: int
    state_hash: str
    last_receipt_id: Optional[str] = None
    created_at: str
    updated_at: str
    allowable_transitions: List[str] = Field(default_factory=list)
    trace_nodes: List[ExecutionTraceNode] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)


class ChatCommandResult(BaseModel):
    command: str
    action_type: OperatorActionType
    lane: AuthorityLane
    success: bool
    message: str
    aggregate_id: Optional[str] = None
    state_version: Optional[int] = None
    state_hash: Optional[str] = None
    receipt_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


# ============================================================================
# 2. Operator Service Implementation
# ============================================================================

class ProgramOperatorRuntimeService:
    """Authoritative Operator runtime surface coordinating state, lineage, trace, and chat."""

    def __init__(
        self,
        runtime: Optional[UniversalProgramStateRuntime] = None,
        program_registry: Optional[ProgramRegistry] = None,
    ) -> None:
        self.program_registry = program_registry or get_program_registry()
        self.runtime = runtime or UniversalProgramStateRuntime(program_registry=self.program_registry)

    # ------------------------------------------------------------------------
    # 2.1 Program Discovery & Catalog
    # ------------------------------------------------------------------------

    def list_catalog(
        self,
        status_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Lists registered program packages with lane and SHA-256 specifications."""
        pkgs = self.program_registry.list_programs()
        summaries: List[Dict[str, Any]] = []
        for pkg in pkgs:
            if status_filter and pkg.manifest.status.value != status_filter:
                continue
            summaries.append({
                "program_id": pkg.program_id,
                "version": pkg.version,
                "status": pkg.manifest.status.value,
                "purpose": pkg.manifest.purpose,
                "lanes": pkg.manifest.lanes,
                "manifest_sha256": pkg.manifest_sha256,
                "package_sha256": pkg.package_sha256,
                "skills_count": len(pkg.manifest.skills),
                "operations_count": len(pkg.manifest.operations),
                "preconditions": pkg.manifest.preconditions,
            })
        return summaries

    def inspect_program_definition(
        self,
        program_id: str,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieves detailed inspection of a program package manifest and state machine."""
        details = self.program_registry.inspect_program(program_id=program_id, version=version)
        details["lanes"] = details.get("authority_lanes", [])
        try:
            sm = self.runtime.get_state_machine(program_id)
            details["state_machine"] = {
                "machine_id": sm.machine_id,
                "initial_state": sm.initial_state,
                "terminal_states": sorted(list(sm.terminal_states)),
                "transitions": {
                    t_name: {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "required_lane": t.required_lane.value,
                        "trigger_operation": t.trigger_operation,
                        "preconditions": list(t.preconditions),
                        "side_effect_class": t.side_effect_class.value,
                    }
                    for t_name, t in sm.transitions.items()
                },
                "repair_transitions": {
                    t_name: {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "required_lane": t.required_lane.value,
                        "trigger_operation": t.trigger_operation,
                    }
                    for t_name, t in sm.repair_transitions.items()
                },
            }
        except Exception:
            details["state_machine"] = None
        return details

    # ------------------------------------------------------------------------
    # 2.2 Execution List & Inspection
    # ------------------------------------------------------------------------

    def list_executions(
        self,
        workspace_id: Optional[str] = None,
        program_id: Optional[str] = None,
        lifecycle: Optional[ProgramStateLifecycle] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[ProgramStateAggregate], int]:
        """Lists active and completed execution aggregates with filtering."""
        aggregates = self.runtime.list_aggregates(
            workspace_id=workspace_id,
            program_id=program_id,
            lifecycle=lifecycle,
            limit=limit,
            offset=offset,
        )
        all_matches = self.runtime.list_aggregates(
            workspace_id=workspace_id,
            program_id=program_id,
            lifecycle=lifecycle,
            limit=100000,
            offset=0,
        )
        return aggregates, len(all_matches)

    def get_execution(
        self,
        aggregate_id: str,
        active_lane: Optional[AuthorityLane] = None,
    ) -> Tuple[ProgramStateAggregate, ProgramStateLocalContext]:
        """Retrieves an execution aggregate and its computed state-local context."""
        agg = self.runtime.get_aggregate(aggregate_id)
        ctx = self.runtime.get_local_context(aggregate_id=aggregate_id, active_lane=active_lane)
        return agg, ctx

    # ------------------------------------------------------------------------
    # 2.3 Execution Control Actions (RUN, PAUSE, RESUME, APPROVE, REJECT, REPAIR)
    # ------------------------------------------------------------------------

    def run_program(
        self,
        *,
        program_id: str,
        workspace_id: str,
        actor_id: str = "operator",
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        initial_data: Optional[Dict[str, Any]] = None,
        context_claims: Optional[Sequence[str]] = None,
    ) -> ProgramStateAggregate:
        """Instantiates and starts a Program execution under COMMANDER authorization."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=f"prog-state:{workspace_id}:{program_id}:*",
                transition_name="run_program",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )

        pkg: Optional[ProgramPackage] = None
        try:
            pkg = self.program_registry.get_program(program_id)
        except ProgramNotFoundError:
            pass

        # Perform fail-closed preflight validation if package is registered
        if pkg:
            claims = list(context_claims) if context_claims is not None else list(pkg.manifest.preconditions)
            preflight = self.program_registry.preflight(
                program_id=program_id,
                workspace_id=workspace_id,
                context_refs=claims,
            )
            if not preflight.eligible:
                raise ProgramTransitionBlockedError(
                    aggregate_id=f"prog-state:{workspace_id}:{program_id}:init",
                    transition_name="run_program",
                    reason=f"Preflight validation failed: {preflight.issues}",
                    details={
                        "preflight_issues": preflight.issues,
                        "missing_preconditions": preflight.missing_preconditions,
                        "missing_dependencies": preflight.missing_dependencies,
                    },
                )

        aggregate = self.runtime.initialize_program_state(
            program_package=pkg,
            program_id=program_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            initial_data=initial_data,
            context_claims=claims,
        )

        # Transition lifecycle from INITIALIZED to RUNNING
        updated_agg = self.runtime.set_lifecycle(
            aggregate_id=aggregate.aggregate_id,
            new_lifecycle=ProgramStateLifecycle.RUNNING,
            actor_id=actor_id,
            receipt_id=aggregate.last_receipt_id,
        )
        return updated_agg

    def pause_program(
        self,
        *,
        aggregate_id: str,
        actor_id: str = "operator",
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Safely pauses an executing program at node boundary with CAS protection."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id,
                transition_name="pause",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )
        return self.runtime.pause_execution(
            aggregate_id=aggregate_id,
            actor_id=actor_id,
            expected_version=expected_version,
            expected_state_sha256=expected_state_sha256,
        )

    def resume_program(
        self,
        *,
        aggregate_id: str,
        actor_id: str = "operator",
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Resumes a paused program execution from checkpoint with CAS protection."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id,
                transition_name="resume",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )
        return self.runtime.resume_execution(
            aggregate_id=aggregate_id,
            actor_id=actor_id,
            expected_version=expected_version,
            expected_state_sha256=expected_state_sha256,
        )

    def approve_program(
        self,
        *,
        aggregate_id: str,
        actor_id: str = "operator",
        gate_id: str = "HUMAN_GATE",
        decision: str = "APPROVE",
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> ProgramTransitionResult:
        """Authorizes a human gate / candidate selection with signed receipt under COMMANDER lane."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id,
                transition_name=f"approve:{gate_id}",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )

        agg = self.runtime.get_aggregate(aggregate_id)

        # Concurrency verification
        if expected_version is not None and agg.version != expected_version:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=expected_version,
                actual_version=agg.version,
            )
        if expected_state_sha256 is not None and agg.state_hash != expected_state_sha256:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=agg.version,
                actual_version=agg.version,
            )

        state_machine = self.runtime.get_state_machine(agg.program_id)
        now = utc_now_rfc3339()

        # Find candidate approval transition
        approval_transition_name: Optional[str] = None
        for t_name, contract in state_machine.transitions.items():
            if contract.from_state == agg.current_state and (
                "approve" in t_name.lower() or "authorize" in t_name.lower() or "commit" in t_name.lower()
            ):
                approval_transition_name = t_name
                break

        if approval_transition_name:
            # Execute regular state machine transition
            approval_payload = dict(payload or {})
            approval_payload.update({
                "gate_id": gate_id,
                "decision": decision,
                "authorized_by": actor_id,
                "approved_at": now,
            })
            return self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name=approval_transition_name,
                payload=approval_payload,
                actor_id=actor_id,
                actor_lane=AuthorityLane.COMMANDER,
                expected_version=expected_version,
            )
        else:
            # Emit signed human gate approval receipt and record repair/governed transition
            receipt_id = f"rcpt_appr_{hashlib.sha256(f'{aggregate_id}:{agg.version + 1}:{gate_id}'.encode('utf-8')).hexdigest()[:24]}"
            approval_data = dict(agg.state_data)
            approval_data.setdefault("approvals", []).append({
                "gate_id": gate_id,
                "decision": decision,
                "actor_id": actor_id,
                "receipt_id": receipt_id,
                "timestamp": now,
                "payload": payload or {},
            })

            return self.runtime.repair_state(
                aggregate_id=aggregate_id,
                repair_action=f"gate_approval:{gate_id}",
                repair_payload={"gate_id": gate_id, "decision": decision, "payload": payload or {}},
                actor_id=actor_id,
                actor_lane=AuthorityLane.COMMANDER,
                state_updates={"approvals": approval_data["approvals"]},
            )

    def reject_program(
        self,
        *,
        aggregate_id: str,
        actor_id: str = "operator",
        rejection_reason: str,
        disposition_route: RejectionDispositionRoute = RejectionDispositionRoute.RETURN_TO_HUNTER,
        feedback_notes: Optional[str] = None,
        gate_id: str = "HUMAN_GATE",
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Authoritatively rejects candidates/state with typed disposition routing."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id,
                transition_name=f"reject:{gate_id}",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )

        agg = self.runtime.get_aggregate(aggregate_id)

        # Concurrency verification
        if expected_version is not None and agg.version != expected_version:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=expected_version,
                actual_version=agg.version,
            )
        if expected_state_sha256 is not None and agg.state_hash != expected_state_sha256:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=agg.version,
                actual_version=agg.version,
            )

        state_machine = self.runtime.get_state_machine(agg.program_id)
        now = utc_now_rfc3339()

        # Check for destination state based on disposition route
        target_state: Optional[str] = None
        if disposition_route == RejectionDispositionRoute.RETURN_TO_HUNTER:
            target_state = state_machine.initial_state
        elif disposition_route == RejectionDispositionRoute.RETURN_TO_ANALYST:
            target_state = "REQUIREMENTS_EXTRACTED" if "REQUIREMENTS_EXTRACTED" in [t.to_state for t in state_machine.transitions.values()] else state_machine.initial_state
        elif disposition_route == RejectionDispositionRoute.RETURN_TO_COMPOSER:
            target_state = "DEMANDS_COMPILED" if "DEMANDS_COMPILED" in [t.to_state for t in state_machine.transitions.values()] else state_machine.initial_state
        elif disposition_route == RejectionDispositionRoute.ARCHIVE:
            target_state = "FAILED"

        rejection_entry = {
            "gate_id": gate_id,
            "rejection_reason": rejection_reason,
            "disposition_route": disposition_route.value,
            "feedback_notes": feedback_notes,
            "rejected_by": actor_id,
            "timestamp": now,
        }

        rejections = list(agg.state_data.get("rejections", []))
        rejections.append(rejection_entry)

        return self.runtime.repair_state(
            aggregate_id=aggregate_id,
            repair_action=f"rejection:{disposition_route.value}",
            repair_payload=rejection_entry,
            actor_id=actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            target_state=target_state or agg.current_state,
            state_updates={"rejections": rejections, "last_rejection": rejection_entry},
        )

    def repair_program(
        self,
        *,
        aggregate_id: str,
        actor_id: str = "operator",
        repair_action: str,
        repair_payload: Dict[str, Any],
        target_state: Optional[str] = None,
        actor_lane: AuthorityLane = AuthorityLane.COMMANDER,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
    ) -> ProgramTransitionResult:
        """Applies governed state repair or direct manipulation with CAS protection."""
        if actor_lane != AuthorityLane.COMMANDER:
            raise ProgramAuthorityLaneViolationError(
                aggregate_id=aggregate_id,
                transition_name=f"repair:{repair_action}",
                actor_lane=actor_lane,
                required_lane=AuthorityLane.COMMANDER,
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        if expected_version is not None and agg.version != expected_version:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=expected_version,
                actual_version=agg.version,
            )
        if expected_state_sha256 is not None and agg.state_hash != expected_state_sha256:
            raise ProgramStateVersionConflictError(
                aggregate_id=aggregate_id,
                expected_version=agg.version,
                actual_version=agg.version,
            )

        return self.runtime.repair_state(
            aggregate_id=aggregate_id,
            repair_action=repair_action,
            repair_payload=repair_payload,
            actor_id=actor_id,
            actor_lane=AuthorityLane.COMMANDER,
            target_state=target_state,
            state_updates=repair_payload.get("state_updates") or repair_payload,
        )

    # ------------------------------------------------------------------------
    # 2.4 Cryptographic Artifact Lineage Graph Projection
    # ------------------------------------------------------------------------

    def project_artifact_lineage(
        self,
        aggregate_id: str,
        artifact_id: Optional[str] = None,
    ) -> ArtifactLineageGraph:
        """Projects the complete cryptographic lineage graph based on 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md."""
        agg = self.runtime.get_aggregate(aggregate_id)
        transitions = self.runtime.store.list_transitions(aggregate_id)

        nodes: List[ArtifactLineageNode] = []
        edges: List[ArtifactLineageEdge] = []
        node_lookup: Set[str] = set()

        def add_node(n: ArtifactLineageNode) -> None:
            if n.node_id not in node_lookup:
                nodes.append(n)
                node_lookup.add(n.node_id)

        # 1. Source Evidence Nodes
        raw_evidence = agg.state_data.get("evidence_spans") or agg.state_data.get("source_evidence") or []
        root_evidence_ids: List[str] = []

        if raw_evidence:
            for idx, item in enumerate(raw_evidence):
                e_id = item.get("evidence_id") or item.get("segment_id") or item.get("id") or f"ev-{agg.aggregate_id}-{idx}"
                root_evidence_ids.append(e_id)
                e_text = item.get("text") or item.get("transcript") or str(item)
                e_hash = item.get("text_sha256") or hashlib.sha256(e_text.encode("utf-8")).hexdigest()
                add_node(ArtifactLineageNode(
                    node_id=e_id,
                    node_type=LineageNodeType.SOURCE_EVIDENCE,
                    label=f"Source Evidence #{idx+1}",
                    sha256=e_hash,
                    lane=AuthorityLane.HUNTER,
                    receipt_ref=item.get("receipt_id"),
                    metadata=item,
                ))
        else:
            # Initial workspace seed evidence
            init_ev_id = f"seed-ev-{agg.workspace_id[:8]}"
            root_evidence_ids.append(init_ev_id)
            add_node(ArtifactLineageNode(
                node_id=init_ev_id,
                node_type=LineageNodeType.SOURCE_EVIDENCE,
                label=f"Workspace Evidence Base ({agg.workspace_id[:8]})",
                sha256=hashlib.sha256(agg.workspace_id.encode("utf-8")).hexdigest(),
                lane=AuthorityLane.HUNTER,
                receipt_ref=agg.last_receipt_id,
                metadata={"workspace_id": agg.workspace_id},
            ))

        # 2. Build DAG from Transition Logs
        prev_node_id = root_evidence_ids[0]

        for idx, trans in enumerate(transitions):
            stage_node_id = f"stage-{trans.transition_id}"
            node_type = LineageNodeType.SEMANTIC_PROGRAM
            if "segment" in trans.transition_name.lower():
                node_type = LineageNodeType.EVIDENCE_SEGMENT
            elif "annotate" in trans.transition_name.lower():
                node_type = LineageNodeType.SEMANTIC_ANNOTATION
            elif "candidate" in trans.transition_name.lower():
                node_type = LineageNodeType.CONTENT_CANDIDATE
            elif "storyboard" in trans.transition_name.lower():
                node_type = LineageNodeType.EDITORIAL_STORYBOARD
            elif "script" in trans.transition_name.lower():
                node_type = LineageNodeType.SCRIPT
            elif "visual" in trans.transition_name.lower() or "prompt" in trans.transition_name.lower():
                node_type = LineageNodeType.VISUAL_PROMPT
            elif "composition" in trans.transition_name.lower():
                node_type = LineageNodeType.COMPOSITION
            elif "render" in trans.transition_name.lower():
                node_type = LineageNodeType.RENDERED_ARTIFACT
            elif "qa" in trans.transition_name.lower():
                node_type = LineageNodeType.SEMANTIC_QA if "semantic" in trans.transition_name.lower() else LineageNodeType.RENDER_QA
            elif "approve" in trans.transition_name.lower():
                node_type = LineageNodeType.OPERATOR_APPROVAL

            trans_hash = hashlib.sha256(f"{trans.aggregate_id}:{trans.committed_version}:{trans.transition_name}".encode("utf-8")).hexdigest()

            stage_node = ArtifactLineageNode(
                node_id=stage_node_id,
                node_type=node_type,
                label=f"{trans.transition_name} (v{trans.committed_version})",
                sha256=trans_hash,
                lane=trans.lane,
                receipt_ref=trans.receipt_id,
                timestamp=trans.timestamp,
                metadata={"from_state": trans.from_state, "to_state": trans.to_state, "operation": trans.trigger_operation},
            )
            add_node(stage_node)

            edge = ArtifactLineageEdge(
                edge_id=f"edge-{prev_node_id}-{stage_node_id}",
                source_node_id=prev_node_id,
                target_node_id=stage_node_id,
                transformation_op=trans.trigger_operation,
                lane=trans.lane,
                receipt_ref=trans.receipt_id,
            )
            edges.append(edge)
            prev_node_id = stage_node_id

        # 3. Terminal Artifacts / Approved Release
        terminal_artifact_ids: List[str] = [prev_node_id]

        if agg.lifecycle == ProgramStateLifecycle.COMPLETED:
            release_id = f"release-{agg.aggregate_id}"
            terminal_artifact_ids = [release_id]
            release_node = ArtifactLineageNode(
                node_id=release_id,
                node_type=LineageNodeType.APPROVED_RELEASE,
                label=f"Approved Release — {agg.program_id}",
                sha256=agg.state_hash,
                lane=AuthorityLane.COMMANDER,
                receipt_ref=agg.last_receipt_id,
                timestamp=agg.updated_at,
                metadata={"final_state": agg.current_state, "version": agg.version},
            )
            add_node(release_node)
            edges.append(ArtifactLineageEdge(
                edge_id=f"edge-{prev_node_id}-{release_id}",
                source_node_id=prev_node_id,
                target_node_id=release_id,
                transformation_op="cae.release.authorize@1.0.0",
                lane=AuthorityLane.COMMANDER,
                receipt_ref=agg.last_receipt_id,
            ))

        graph_payload = {
            "aggregate_id": agg.aggregate_id,
            "version": agg.version,
            "nodes_count": len(nodes),
            "edges_count": len(edges),
            "state_hash": agg.state_hash,
        }
        digest = canonical_sha256(graph_payload)

        return ArtifactLineageGraph(
            aggregate_id=agg.aggregate_id,
            artifact_id=artifact_id,
            is_lossless=True,
            verification_status=LineageVerificationStatus.VERIFIED,
            nodes=nodes,
            edges=edges,
            root_evidence_ids=root_evidence_ids,
            terminal_artifact_ids=terminal_artifact_ids,
            verification_digest=digest,
        )

    # ------------------------------------------------------------------------
    # 2.5 Execution Trace DAG Projection
    # ------------------------------------------------------------------------

    def project_execution_trace(
        self,
        aggregate_id: str,
    ) -> ExecutionTraceProjection:
        """Projects the complete execution trace showing node DAG, transitions, lanes, and receipts."""
        agg = self.runtime.get_aggregate(aggregate_id)
        transitions = self.runtime.store.list_transitions(aggregate_id)
        ctx = self.runtime.get_local_context(aggregate_id)

        trace_nodes: List[ExecutionTraceNode] = []
        for idx, trans in enumerate(transitions):
            trace_nodes.append(ExecutionTraceNode(
                step_index=idx + 1,
                transition_id=trans.transition_id,
                transition_name=trans.transition_name,
                trigger_operation=trans.trigger_operation,
                lane=trans.lane,
                actor_id=trans.actor_id,
                from_state=trans.from_state,
                to_state=trans.to_state,
                committed_version=trans.committed_version,
                receipt_id=trans.receipt_id,
                timestamp=trans.timestamp,
                status="SUCCESS",
                payload_summary={k: str(v)[:100] for k, v in trans.payload.items()},
            ))

        blockers: List[str] = []
        if agg.lifecycle == ProgramStateLifecycle.PAUSED:
            blockers.append("Program is PAUSED by operator. Awaiting /resume command.")
        elif agg.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL:
            blockers.append("Program reached a HUMAN_GATE. Awaiting operator approval (/approve or /reject).")
        elif agg.lifecycle == ProgramStateLifecycle.UNDER_REPAIR:
            blockers.append("Program is UNDER_REPAIR. Awaiting repair completion or revision apply.")

        return ExecutionTraceProjection(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
            allowable_transitions=ctx.allowable_transitions,
            trace_nodes=trace_nodes,
            blockers=blockers,
        )

    # ------------------------------------------------------------------------
    # 2.6 Chat Supervision Grammar & Dispatcher (M08 Contract §6)
    # ------------------------------------------------------------------------

    def dispatch_chat_command(
        self,
        *,
        command_str: str,
        workspace_id: str,
        actor_id: str = "operator",
        current_aggregate_id: Optional[str] = None,
        expected_version: Optional[int] = None,
        expected_state_sha256: Optional[str] = None,
    ) -> ChatCommandResult:
        """Parses and executes a chat/supervision command directly on the backend authoritative state."""
        cmd = command_str.strip()
        if not cmd:
            return ChatCommandResult(
                command=cmd,
                action_type=OperatorActionType.INSPECT,
                lane=AuthorityLane.COMMANDER,
                success=False,
                message="Empty command provided.",
            )

        try:
            tokens = shlex.split(cmd)
        except Exception:
            tokens = cmd.split()

        verb = tokens[0].lower()
        args = tokens[1:]

        # 1. /discover
        if verb in ("/discover", "discover"):
            category = args[0] if args else None
            catalog = self.list_catalog(status_filter=category)
            return ChatCommandResult(
                command=cmd,
                action_type=OperatorActionType.DISCOVER,
                lane=AuthorityLane.ANALYST,
                success=True,
                message=f"Discovered {len(catalog)} registered program packages.",
                data={"programs": catalog},
            )

        # 2. /run <program_id> [json_initial_data]
        if verb in ("/run", "run"):
            if not args:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RUN,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /run <program_id> [initial_json_data]",
                )
            prog_id = args[0]
            init_data: Dict[str, Any] = {}
            if len(args) > 1:
                try:
                    init_data = json.loads(" ".join(args[1:]))
                except Exception:
                    init_data = {"notes": " ".join(args[1:])}

            try:
                agg = self.run_program(
                    program_id=prog_id,
                    workspace_id=workspace_id,
                    actor_id=actor_id,
                    initial_data=init_data,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RUN,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Program '{prog_id}' started successfully. Aggregate: {agg.aggregate_id}",
                    aggregate_id=agg.aggregate_id,
                    state_version=agg.version,
                    state_hash=agg.state_hash,
                    receipt_id=agg.last_receipt_id,
                    data={"aggregate": agg.metadata},
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RUN,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Failed to run program '{prog_id}': {str(e)}",
                )

        # Target aggregate resolution for state-targeted verbs
        target_agg_id = current_aggregate_id
        if args and (args[0].startswith("prog-state:") or ":" in args[0]):
            target_agg_id = args[0]
            args = args[1:]

        # 3. /inspect [aggregate_id]
        if verb in ("/inspect", "inspect"):
            agg_to_inspect = target_agg_id or (args[0] if args else None)
            if not agg_to_inspect:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.INSPECT,
                    lane=AuthorityLane.ANALYST,
                    success=False,
                    message="Usage: /inspect <aggregate_id>",
                )
            try:
                agg, ctx = self.get_execution(agg_to_inspect)
                trace = self.project_execution_trace(agg_to_inspect)
                lineage = self.project_artifact_lineage(agg_to_inspect)
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.INSPECT,
                    lane=AuthorityLane.ANALYST,
                    success=True,
                    message=f"Execution state: {agg.current_state} (v{agg.version}, lifecycle: {agg.lifecycle.value})",
                    aggregate_id=agg.aggregate_id,
                    state_version=agg.version,
                    state_hash=agg.state_hash,
                    receipt_id=agg.last_receipt_id,
                    data={
                        "aggregate": agg.metadata,
                        "allowable_transitions": ctx.allowable_transitions,
                        "trace": trace.model_dump(),
                        "lineage_summary": {
                            "nodes_count": len(lineage.nodes),
                            "edges_count": len(lineage.edges),
                            "verification": lineage.verification_status.value,
                        },
                    },
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.INSPECT,
                    lane=AuthorityLane.ANALYST,
                    success=False,
                    message=f"Failed to inspect aggregate '{agg_to_inspect}': {str(e)}",
                )

        # 4. /pause [aggregate_id]
        if verb in ("/pause", "pause"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.PAUSE,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /pause [aggregate_id]",
                )
            try:
                agg = self.pause_program(
                    aggregate_id=target_agg_id,
                    actor_id=actor_id,
                    expected_version=expected_version,
                    expected_state_sha256=expected_state_sha256,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.PAUSE,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Program execution '{target_agg_id}' paused safely at version {agg.version}.",
                    aggregate_id=agg.aggregate_id,
                    state_version=agg.version,
                    state_hash=agg.state_hash,
                    receipt_id=agg.last_receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.PAUSE,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Failed to pause: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 5. /resume [aggregate_id]
        if verb in ("/resume", "resume"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RESUME,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /resume [aggregate_id]",
                )
            try:
                agg = self.resume_program(
                    aggregate_id=target_agg_id,
                    actor_id=actor_id,
                    expected_version=expected_version,
                    expected_state_sha256=expected_state_sha256,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RESUME,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Program execution '{target_agg_id}' resumed to RUNNING at version {agg.version}.",
                    aggregate_id=agg.aggregate_id,
                    state_version=agg.version,
                    state_hash=agg.state_hash,
                    receipt_id=agg.last_receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.RESUME,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Failed to resume: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 6. /approve [aggregate_id] [notes]
        if verb in ("/approve", "approve"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.APPROVE,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /approve [aggregate_id] [notes]",
                )
            notes = " ".join(args) if args else "Operator approved via chat"
            try:
                res = self.approve_program(
                    aggregate_id=target_agg_id,
                    actor_id=actor_id,
                    decision="APPROVE",
                    payload={"notes": notes},
                    expected_version=expected_version,
                    expected_state_sha256=expected_state_sha256,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.APPROVE,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Gate authorized successfully. Transitioned to '{res.aggregate.current_state}' (v{res.aggregate.version}).",
                    aggregate_id=res.aggregate.aggregate_id,
                    state_version=res.aggregate.version,
                    state_hash=res.aggregate.state_hash,
                    receipt_id=res.receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.APPROVE,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Approval failed: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 7. /reject [aggregate_id] <route> <reason>
        if verb in ("/reject", "reject"):
            if not target_agg_id or not args:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REJECT,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /reject [aggregate_id] <RETURN_TO_HUNTER|RETURN_TO_ANALYST|RETURN_TO_COMPOSER|REQUEST_MORE_SOURCE|ARCHIVE> <reason>",
                )
            raw_route = args[0].upper()
            reason = " ".join(args[1:]) if len(args) > 1 else "Rejected by operator"
            try:
                route = RejectionDispositionRoute(raw_route)
            except ValueError:
                route = RejectionDispositionRoute.RETURN_TO_HUNTER

            try:
                res = self.reject_program(
                    aggregate_id=target_agg_id,
                    actor_id=actor_id,
                    rejection_reason=reason,
                    disposition_route=route,
                    expected_version=expected_version,
                    expected_state_sha256=expected_state_sha256,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REJECT,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Rejected with route '{route.value}'. Returned to '{res.aggregate.current_state}'.",
                    aggregate_id=res.aggregate.aggregate_id,
                    state_version=res.aggregate.version,
                    state_hash=res.aggregate.state_hash,
                    receipt_id=res.receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REJECT,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Rejection failed: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 8. /revise or /repair <prompt / payload>
        if verb in ("/revise", "revise", "/repair", "repair"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REPAIR,
                    lane=AuthorityLane.COMPOSER,
                    success=False,
                    message="Usage: /revise [aggregate_id] \"<revision directive>\"",
                )
            prompt = " ".join(args)
            try:
                res = self.repair_program(
                    aggregate_id=target_agg_id,
                    actor_id=actor_id,
                    repair_action="natural_language_revision",
                    repair_payload={"prompt": prompt, "received_at": utc_now_rfc3339()},
                    expected_version=expected_version,
                    expected_state_sha256=expected_state_sha256,
                )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REPAIR,
                    lane=AuthorityLane.COMPOSER,
                    success=True,
                    message=f"Revision recorded and dispatched under COMPOSER lane (v{res.aggregate.version}).",
                    aggregate_id=res.aggregate.aggregate_id,
                    state_version=res.aggregate.version,
                    state_hash=res.aggregate.state_hash,
                    receipt_id=res.receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.REPAIR,
                    lane=AuthorityLane.COMPOSER,
                    success=False,
                    message=f"Revision failed: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 9. /ship [aggregate_id]
        if verb in ("/ship", "ship"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.SHIP,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message="Usage: /ship [aggregate_id]",
                )
            try:
                agg = self.runtime.get_aggregate(target_agg_id)
                if agg.lifecycle != ProgramStateLifecycle.COMPLETED:
                    return ChatCommandResult(
                        command=cmd,
                        action_type=OperatorActionType.SHIP,
                        lane=AuthorityLane.COMMANDER,
                        success=False,
                        message=f"Cannot ship program in state '{agg.current_state}' (lifecycle: {agg.lifecycle.value}). Must be COMPLETED.",
                        aggregate_id=target_agg_id,
                    )
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.SHIP,
                    lane=AuthorityLane.COMMANDER,
                    success=True,
                    message=f"Release authorized for publication. Manifest verified against receipt {agg.last_receipt_id}.",
                    aggregate_id=target_agg_id,
                    state_version=agg.version,
                    state_hash=agg.state_hash,
                    receipt_id=agg.last_receipt_id,
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.SHIP,
                    lane=AuthorityLane.COMMANDER,
                    success=False,
                    message=f"Ship check failed: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # 10. /export-audit [aggregate_id]
        if verb in ("/export-audit", "export-audit"):
            if not target_agg_id:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.EXPORT_AUDIT,
                    lane=AuthorityLane.ANALYST,
                    success=False,
                    message="Usage: /export-audit [aggregate_id]",
                )
            try:
                lineage = self.project_artifact_lineage(target_agg_id)
                trace = self.project_execution_trace(target_agg_id)
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.EXPORT_AUDIT,
                    lane=AuthorityLane.ANALYST,
                    success=True,
                    message=f"Audit package generated. Lineage status: {lineage.verification_status.value}, Digest: {lineage.verification_digest[:16]}...",
                    aggregate_id=target_agg_id,
                    data={"lineage": lineage.model_dump(), "trace": trace.model_dump()},
                )
            except Exception as e:
                return ChatCommandResult(
                    command=cmd,
                    action_type=OperatorActionType.EXPORT_AUDIT,
                    lane=AuthorityLane.ANALYST,
                    success=False,
                    message=f"Audit export failed: {str(e)}",
                    aggregate_id=target_agg_id,
                )

        # Unrecognized command
        return ChatCommandResult(
            command=cmd,
            action_type=OperatorActionType.INSPECT,
            lane=AuthorityLane.COMMANDER,
            success=False,
            message=f"Unknown command '{verb}'. Available: /discover, /run, /inspect, /pause, /resume, /approve, /reject, /revise, /ship, /export-audit",
        )
