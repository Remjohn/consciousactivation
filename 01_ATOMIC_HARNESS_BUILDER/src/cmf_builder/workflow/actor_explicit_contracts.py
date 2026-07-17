"""Actor-explicit, execution-free workflow contracts for ST-09.01."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re
from typing import Any

_SHA = re.compile(r"^[0-9a-f]{64}$")


class WorkflowContractError(ValueError):
    def __init__(self, code: str, message: str, **context: object):
        super().__init__(message); self.code = code; self.context = dict(context)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _text(value: object, name: str, code: str = "MISSING_GOVERNED_FIELD") -> None:
    if not isinstance(value, str) or not value.strip(): raise WorkflowContractError(code, f"{name} required")


def _sha(value: object, name: str) -> None:
    if not isinstance(value, str) or not _SHA.fullmatch(value): raise WorkflowContractError("INVALID_IMMUTABLE_IDENTITY", f"{name} must be SHA-256")


class ActorKind(str, Enum):
    HUMAN_NODE = "HUMAN_NODE"
    GOVERNED_AGENT_NODE = "GOVERNED_AGENT_NODE"
    DETERMINISTIC_CODE_NODE = "DETERMINISTIC_CODE_NODE"
    EXTERNAL_BOUNDARY_NODE = "EXTERNAL_BOUNDARY_NODE"

class AuthorityStatus(str,Enum):
    ACTIVE="ACTIVE"
    SUPERSEDED="SUPERSEDED"
    INVALIDATED="INVALIDATED"

class WorkflowAction(str,Enum):
    COMPILE="COMPILE"
    INVALIDATE="INVALIDATE"


@dataclass(frozen=True)
class WorkflowNode:
    node_id: str
    actor_kind: ActorKind
    owner: str | tuple[str,...]
    input_contract: str
    output_contract: str
    authority_requirement: str
    dependency_node_ids: tuple[str, ...]
    execution_preconditions: tuple[str, ...]
    completion_condition: str
    rejection_behavior: str
    retry_eligible: bool
    checkpoint_behavior: str
    cancellation_behavior: str
    failure_owner: str
    declared_downstream_nodes: tuple[str, ...]
    producer_output_validation_ref: str
    actor_rationale: str = "explicit responsibility ownership"
    human_decision_reissued: bool = False
    external_execution_requested: bool = False

    def __post_init__(self) -> None:
        _text(self.node_id, "node_id")
        if not isinstance(self.actor_kind,ActorKind):raise WorkflowContractError("AMBIGUOUS_ACTOR_OWNERSHIP","exactly one actor kind required")
        if isinstance(self.owner,tuple):raise WorkflowContractError("AMBIGUOUS_ACTOR_OWNERSHIP","one primary owner required")
        if not isinstance(self.owner,str) or not self.owner.strip():raise WorkflowContractError("MISSING_ACTOR_OWNER","owner required")
        if any(token in self.owner for token in ("|", ",", ";")): raise WorkflowContractError("AMBIGUOUS_ACTOR_OWNERSHIP", "one primary owner required")
        for value, name in ((self.actor_rationale,"actor_rationale"),(self.input_contract,"input_contract"),(self.output_contract,"output_contract"),(self.authority_requirement,"authority_requirement"),(self.completion_condition,"completion_condition"),(self.rejection_behavior,"rejection_behavior"),(self.checkpoint_behavior,"checkpoint_behavior"),(self.cancellation_behavior,"cancellation_behavior"),(self.failure_owner,"failure_owner"),(self.producer_output_validation_ref,"producer_output_validation_ref")): _text(value,name)
        if self.human_decision_reissued:raise WorkflowContractError("HUMAN_DECISION_REPLAY_PROHIBITED","historical human decisions cannot be reissued")
        if self.external_execution_requested:raise WorkflowContractError("EXTERNAL_EXECUTION_PROHIBITED","external boundary is declarative only")

    def as_dict(self) -> dict[str, Any]:
        return {"node_id":self.node_id,"actor_kind":self.actor_kind.value,"owner":self.owner,"actor_rationale":self.actor_rationale,"input_contract":self.input_contract,"output_contract":self.output_contract,"authority_requirement":self.authority_requirement,"dependency_node_ids":list(self.dependency_node_ids),"execution_preconditions":list(self.execution_preconditions),"completion_condition":self.completion_condition,"rejection_behavior":self.rejection_behavior,"retry_eligible":self.retry_eligible,"checkpoint_behavior":self.checkpoint_behavior,"cancellation_behavior":self.cancellation_behavior,"failure_owner":self.failure_owner,"declared_downstream_nodes":list(self.declared_downstream_nodes),"producer_output_validation_ref":self.producer_output_validation_ref,"human_decision_reissued":False,"external_execution_requested":False}


@dataclass(frozen=True)
class WorkflowEdge:
    source_node_id: str
    target_node_id: str
    payload_contract: str
    condition: str
    validated_output_required: bool = True

    def __post_init__(self) -> None:
        for value,name in ((self.source_node_id,"source_node_id"),(self.target_node_id,"target_node_id"),(self.payload_contract,"payload_contract"),(self.condition,"condition")): _text(value,name)

    def as_dict(self) -> dict[str, Any]:
        return {"source_node_id":self.source_node_id,"target_node_id":self.target_node_id,"payload_contract":self.payload_contract,"condition":self.condition,"validated_output_required":self.validated_output_required}


@dataclass(frozen=True,init=False)
class WorkflowAuthority:
    authority_id:str;authority_version:str;authority_sha256:str;permitted_actions:tuple[WorkflowAction,...];applicable_scope:tuple[str,...];status:AuthorityStatus=AuthorityStatus.ACTIVE

    def __init__(self,authority_id:str,authority_version:str|None=None,authority_sha256:str|None=None,permitted_actions:tuple[WorkflowAction,...]|None=None,applicable_scope:tuple[str,...]|None=None,status:AuthorityStatus=AuthorityStatus.ACTIVE,*,version:str|None=None,sha256:str|None=None,scope:tuple[str,...]|None=None):
        object.__setattr__(self,"authority_id",authority_id);object.__setattr__(self,"authority_version",authority_version or version or "");object.__setattr__(self,"authority_sha256",authority_sha256 or sha256 or "");object.__setattr__(self,"permitted_actions",permitted_actions or (WorkflowAction.COMPILE,WorkflowAction.INVALIDATE));object.__setattr__(self,"applicable_scope",applicable_scope or scope or ());object.__setattr__(self,"status",status);self.__post_init__()

    def __post_init__(self) -> None:
        _text(self.authority_id,"authority_id");_text(self.authority_version,"authority_version");_sha(self.authority_sha256,"authority_sha256")
        if not self.permitted_actions or not self.applicable_scope: raise WorkflowContractError("MISSING_AUTHORITY","authority scope and actions required")

    @property
    def authority_identity(self) -> str: return canonical_sha256(self.as_dict())
    def as_dict(self) -> dict[str,Any]: return {"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"permitted_actions":[x.value for x in self.permitted_actions],"applicable_scope":list(self.applicable_scope),"status":self.status.value}


@dataclass(frozen=True)
class ActorExplicitWorkflowIR:
    workflow_id: str
    workflow_version: str
    profile_ref:str
    nodes: tuple[WorkflowNode, ...]
    edges: tuple[WorkflowEdge, ...]
    entry_node_ids:tuple[str,...]
    terminal_node_ids:tuple[str,...]
    source_graph_hashes:tuple[str,...]
    promotion_status:str
    authority: WorkflowAuthority
    command_identity:str
    adapter_kind:str="deterministic_local_development_adapter"
    external_engine: bool = False
    workflow_execution:bool=False
    agent_execution:bool=False
    temporal_conformance: str = "EXTERNAL_VALIDATION_PENDING"
    full_ADR_006_satisfaction:bool=False
    production_ready: bool = False
    certified: bool = False
    _integrity_anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _text(self.workflow_id,"workflow_id");_text(self.workflow_version,"workflow_version")
        _sha(self.profile_ref,"profile_ref")
        for item in self.source_graph_hashes: _sha(item,"source_graph_hash")
        if self.promotion_status!="development_only":raise WorkflowContractError("PRODUCTION_PROMOTION_PROHIBITED","development-only profile required")
        if self.external_engine or self.production_ready or self.certified: raise WorkflowContractError("PRODUCTION_OR_EXTERNAL_EXECUTION_PROHIBITED","offline workflow cannot promote")
        object.__setattr__(self,"_integrity_anchor",canonical_sha256(self._payload()))

    def _payload(self) -> dict[str,Any]:
        return {"workflow_id":self.workflow_id,"workflow_version":self.workflow_version,"profile_ref":self.profile_ref,"nodes":[item.as_dict() for item in sorted(self.nodes,key=lambda x:x.node_id)],"edges":[item.as_dict() for item in sorted(self.edges,key=lambda x:(x.source_node_id,x.target_node_id))],"entry_node_ids":list(self.entry_node_ids),"terminal_node_ids":list(self.terminal_node_ids),"source_graph_hashes":list(self.source_graph_hashes),"promotion_status":"development_only","authority":{**self.authority.as_dict(),"authority_identity":self.authority.authority_identity},"command_identity":self.command_identity,"adapter_kind":"deterministic_local_development_adapter","external_engine":False,"workflow_execution":False,"agent_execution":False,"temporal_conformance":"EXTERNAL_VALIDATION_PENDING","full_ADR_006_satisfaction":False,"production_ready":False,"certified":False}

    @property
    def workflow_identity(self) -> str: return canonical_sha256(self._payload())
    def as_dict(self) -> dict[str,Any]:
        payload=self._payload();identity=canonical_sha256(payload)
        if identity!=self._integrity_anchor: raise WorkflowContractError("MUTATED_GOVERNED_OBJECT","workflow inputs changed after compilation")
        payload["workflow_identity"]=identity;return payload


def _assert_acyclic(nodes: tuple[WorkflowNode,...], edges: tuple[WorkflowEdge,...]) -> None:
    graph={node.node_id:[] for node in nodes}
    indegree={node.node_id:0 for node in nodes}
    for edge in edges: graph[edge.source_node_id].append(edge.target_node_id);indegree[edge.target_node_id]+=1
    ready=sorted(node for node,count in indegree.items() if count==0);visited=0
    while ready:
        current=ready.pop(0);visited+=1
        for target in graph[current]:
            indegree[target]-=1
            if indegree[target]==0: ready.append(target);ready.sort()
    if visited!=len(nodes): raise WorkflowContractError("CYCLIC_WORKFLOW","workflow must be acyclic")


def _compile_payload(*,workflow_id:str,workflow_version:str,profile_ref:str,nodes:tuple[WorkflowNode,...],edges:tuple[WorkflowEdge,...],entry_node_ids:tuple[str,...],terminal_node_ids:tuple[str,...],source_graph_hashes:tuple[str,...],promotion_status:str)->dict[str,Any]:
    return {"workflow_id":workflow_id,"workflow_version":workflow_version,"profile_ref":profile_ref,"nodes":[x.as_dict() for x in sorted(nodes,key=lambda x:x.node_id)],"edges":[x.as_dict() for x in sorted(edges,key=lambda x:(x.source_node_id,x.target_node_id))],"entry_node_ids":list(entry_node_ids),"terminal_node_ids":list(terminal_node_ids),"source_graph_hashes":list(source_graph_hashes),"promotion_status":promotion_status}

def compute_workflow_compile_payload_sha256(**values:Any)->str:return canonical_sha256(_compile_payload(**values))

def compile_actor_explicit_workflow(*,workflow_id:str,workflow_version:str,nodes:tuple[WorkflowNode,...],edges:tuple[WorkflowEdge,...],authority:WorkflowAuthority,profile_ref:str|None=None,entry_node_ids:tuple[str,...]=(),terminal_node_ids:tuple[str,...]=(),source_graph_hashes:tuple[str,...]=(),promotion_status:str="development_only",command:WorkflowCommand|None=None,source_refs:tuple[str,...]=(),predecessor_receipts:tuple[str,...]=())->ActorExplicitWorkflowIR:
    if profile_ref is None:profile_ref=hashlib.sha256(f"{workflow_id}:{workflow_version}:local-profile".encode()).hexdigest()
    if not entry_node_ids:entry_node_ids=tuple(sorted(n.node_id for n in nodes if not n.dependency_node_ids))
    if not terminal_node_ids:terminal_node_ids=tuple(sorted(n.node_id for n in nodes if not n.declared_downstream_nodes))
    if not source_graph_hashes:source_graph_hashes=tuple((*source_refs,*predecessor_receipts))
    if authority.status is not AuthorityStatus.ACTIVE:raise WorkflowContractError("INACTIVE_AUTHORITY","authority inactive")
    if WorkflowAction.COMPILE not in authority.permitted_actions:raise WorkflowContractError("UNAUTHORIZED_ACTION","compile not permitted")
    expected_resource=hashlib.sha256(f"{workflow_id}:{workflow_version}:{profile_ref}".encode()).hexdigest()
    expected_payload=compute_workflow_compile_payload_sha256(workflow_id=workflow_id,workflow_version=workflow_version,profile_ref=profile_ref,nodes=nodes,edges=edges,entry_node_ids=entry_node_ids,terminal_node_ids=terminal_node_ids,source_graph_hashes=source_graph_hashes,promotion_status=promotion_status)
    if command is None:command=WorkflowCommand("compile-local-workflow",WorkflowAction.COMPILE,expected_resource,expected_payload,authority.authority_identity)
    if command.action is not WorkflowAction.COMPILE:raise WorkflowContractError("UNAUTHORIZED_ACTION","compile not permitted")
    if command.resource_id!=expected_resource:raise WorkflowContractError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=expected_payload:raise WorkflowContractError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    if command.expected_authority_identity!=authority.authority_identity:raise WorkflowContractError("AUTHORITY_IDENTITY_MISMATCH","authority mismatch")
    if len(nodes)<2: raise WorkflowContractError("MONOLITHIC_WORKFLOW_PROHIBITED","workflow requires explicit responsibility nodes")
    by_id={node.node_id:node for node in nodes}
    if len(by_id)!=len(nodes): raise WorkflowContractError("DUPLICATE_WORKFLOW_NODE","node ids must be unique")
    for edge in edges:
        if edge.source_node_id not in by_id or edge.target_node_id not in by_id: raise WorkflowContractError("UNDECLARED_HANDOFF","edge endpoint missing")
        source,target=by_id[edge.source_node_id],by_id[edge.target_node_id]
        if edge.target_node_id not in source.declared_downstream_nodes or edge.source_node_id not in target.dependency_node_ids: raise WorkflowContractError("UNDECLARED_HANDOFF","handoff not declared by both nodes")
        if not edge.validated_output_required or not source.producer_output_validation_ref: raise WorkflowContractError("UNVALIDATED_OUTPUT_ADVANCEMENT","validated output required")
    for node in nodes:
        if node.human_decision_reissued:raise WorkflowContractError("HUMAN_DECISION_REPLAY_PROHIBITED","historical human decisions cannot be reissued")
        if node.external_execution_requested:raise WorkflowContractError("EXTERNAL_EXECUTION_PROHIBITED","external boundary is declarative only")
    _assert_acyclic(nodes,edges)
    for edge in edges:
        source,target=by_id[edge.source_node_id],by_id[edge.target_node_id]
        if source.output_contract!=edge.payload_contract or target.input_contract!=edge.payload_contract:raise WorkflowContractError("INCOMPATIBLE_HANDOFF_CONTRACT","typed handoff mismatch")
    if set(entry_node_ids)!={n.node_id for n in nodes if not n.dependency_node_ids}:raise WorkflowContractError("INVALID_ENTRY_NODE_SET","entry nodes must match graph")
    if set(terminal_node_ids)!={n.node_id for n in nodes if not n.declared_downstream_nodes}:raise WorkflowContractError("INVALID_TERMINAL_NODE_SET","terminal nodes must match graph")
    return ActorExplicitWorkflowIR(workflow_id,workflow_version,profile_ref,tuple(nodes),tuple(edges),tuple(entry_node_ids),tuple(terminal_node_ids),tuple(source_graph_hashes),promotion_status,authority,command.command_identity)


@dataclass(frozen=True)
class WorkflowCommand:
    command_id:str;action:WorkflowAction;resource_id:str;payload_sha256:str;expected_authority_identity:str
    @property
    def command_identity(self)->str:return canonical_sha256({"command_id":self.command_id,"action":self.action.value,"resource_id":self.resource_id,"payload_sha256":self.payload_sha256,"expected_authority_identity":self.expected_authority_identity})


@dataclass(frozen=True)
class WorkflowInvalidationReceipt:
    prior_workflow_identity:str;affected_scope:tuple[str,...];active_after:bool;historical_workflow_preserved:bool;reevaluation_requires_new_workflow:bool;command_identity:str;authority_identity:str
    @property
    def invalidation_identity(self)->str:return canonical_sha256(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"prior_workflow_identity":self.prior_workflow_identity,"affected_scope":list(self.affected_scope),"active_after":False,"historical_workflow_preserved":True,"reevaluation_requires_new_workflow":True,"command_identity":self.command_identity,"authority_identity":self.authority_identity}


def validate_repeat_workflow_ir(existing:ActorExplicitWorkflowIR,repeated:ActorExplicitWorkflowIR)->ActorExplicitWorkflowIR:
    existing.as_dict();repeated.as_dict()
    if existing.workflow_identity!=repeated.workflow_identity:raise WorkflowContractError("CONFLICTING_REPEAT_COMMAND","workflow payload differs")
    return existing


def compute_workflow_invalidation_payload_sha256(*,prior_workflow_identity:str,affected_scope:tuple[str,...])->str:return canonical_sha256({"prior_workflow_identity":prior_workflow_identity,"affected_scope":list(affected_scope)})


def invalidate_workflow_ir(workflow:ActorExplicitWorkflowIR,command:WorkflowCommand,authority:WorkflowAuthority,affected_scope:tuple[str,...])->WorkflowInvalidationReceipt:
    workflow.as_dict();expected=compute_workflow_invalidation_payload_sha256(prior_workflow_identity=workflow.workflow_identity,affected_scope=affected_scope)
    if authority.status is not AuthorityStatus.ACTIVE:raise WorkflowContractError("INACTIVE_AUTHORITY","authority inactive")
    if command.action not in authority.permitted_actions:raise WorkflowContractError("UNAUTHORIZED_ACTION","action not permitted")
    if command.resource_id!=workflow.workflow_identity:raise WorkflowContractError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=expected:raise WorkflowContractError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    if command.expected_authority_identity!=authority.authority_identity:raise WorkflowContractError("AUTHORITY_IDENTITY_MISMATCH","authority mismatch")
    return WorkflowInvalidationReceipt(workflow.workflow_identity,tuple(affected_scope),False,True,True,command.command_identity,authority.authority_identity)
