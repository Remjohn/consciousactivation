"""Synthetic manual-shadow routing and parity contracts for ST-09.02."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re
from typing import Any

from .actor_explicit_contracts import ActorKind, WorkflowNode

SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL="SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL"
SHADOW_STEP_KINDS=("human_action","agent_judgment","deterministic_operation","handoff","condition","failure","cost_observation","artifact_observation")
_SHA=re.compile(r"^[0-9a-f]{64}$")

class ManualShadowError(ValueError):
    def __init__(self,code:str,message:str,**context:object):super().__init__(message);self.code=code;self.context=dict(context)
ShadowRoutingError=ManualShadowError

def canonical_json_bytes(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def _hash(value:Any)->str:return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
def _text(value:object,name:str)->None:
    if not isinstance(value,str) or not value.strip():raise ManualShadowError("MISSING_GOVERNED_FIELD",f"{name} required")
def _sha(value:object,name:str)->None:
    if not isinstance(value,str) or not _SHA.fullmatch(value):raise ManualShadowError("INVALID_IMMUTABLE_IDENTITY",f"{name} must be SHA-256")

class FixtureClassification(str,Enum):SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL=SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL
class ShadowStepKind(str,Enum):
    HUMAN_ACTION="human_action";AGENT_JUDGMENT="agent_judgment";DETERMINISTIC_OPERATION="deterministic_operation";HANDOFF="handoff";CONDITION="condition";FAILURE="failure";COST_OBSERVATION="cost_observation";ARTIFACT_OBSERVATION="artifact_observation"
class DivergenceClass(str,Enum):
    EXACT_AGREEMENT="EXACT_AGREEMENT";ACCEPTABLE_BOUNDED_DIFFERENCE="ACCEPTABLE_BOUNDED_DIFFERENCE";SEMANTIC_DIVERGENCE="SEMANTIC_DIVERGENCE";AUTHORITY_VIOLATION="AUTHORITY_VIOLATION";MISSING_REVIEWER="MISSING_REVIEWER";WITHDRAWN_REVIEWER_DISPOSITION="WITHDRAWN_REVIEWER_DISPOSITION";STALE_INPUT_SNAPSHOT="STALE_INPUT_SNAPSHOT";FAILED_PROPOSED_OUTPUT="FAILED_PROPOSED_OUTPUT"
class ShadowDisposition(str,Enum):
    PASS_EXACT_AGREEMENT="PASS_EXACT_AGREEMENT";PASS_ACCEPTABLE_BOUNDED_DIFFERENCE="PASS_ACCEPTABLE_BOUNDED_DIFFERENCE";FAIL_SEMANTIC_DIVERGENCE="FAIL_SEMANTIC_DIVERGENCE";FAIL_AUTHORITY_VIOLATION="FAIL_AUTHORITY_VIOLATION";BLOCKED_REVIEWER_EVIDENCE="BLOCKED_REVIEWER_EVIDENCE";BLOCKED_STALE_OR_FAILED_PROPOSAL="BLOCKED_STALE_OR_FAILED_PROPOSAL"

@dataclass(frozen=True)
class RouteRequest:
    request_type:str;compilation_target:str;run_state:str;risk_class:str;incident_class:str;registry_version:str;registry_sha256:str
    def __post_init__(self):
        for v,n in ((self.request_type,"request_type"),(self.compilation_target,"compilation_target"),(self.run_state,"run_state"),(self.risk_class,"risk_class"),(self.incident_class,"incident_class"),(self.registry_version,"registry_version")):_text(v,n)
        _sha(self.registry_sha256,"registry_sha256")

@dataclass(frozen=True)
class WorkflowProfile:
    profile_id:str;version:str;sha256:str;eligible_request_types:tuple[str,...];eligible_targets:tuple[str,...];allowed_risk_classes:tuple[str,...];active:bool;superseded:bool;authority_refs:tuple[str,...]
    def __post_init__(self):_text(self.profile_id,"profile_id");_text(self.version,"version");_sha(self.sha256,"sha256");[_sha(x,"authority_ref") for x in self.authority_refs]
    @property
    def profile_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"profile_id":self.profile_id,"version":self.version,"sha256":self.sha256,"eligible_request_types":list(self.eligible_request_types),"eligible_targets":list(self.eligible_targets),"allowed_risk_classes":list(self.allowed_risk_classes),"active":self.active,"superseded":self.superseded,"authority_refs":list(self.authority_refs)}

@dataclass(frozen=True)
class RouteDecision:
    selected_profile_id:str;selected_profile_version:str;profile_sha256:str;rule_identity:str;exact_rule_result:str;eligible_alternatives:tuple[str,...];selection_reason:str;authority_refs:tuple[str,...];routing_completed_before_execution:bool=True
    @property
    def decision_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"selected_profile_id":self.selected_profile_id,"selected_profile_version":self.selected_profile_version,"profile_sha256":self.profile_sha256,"rule_identity":self.rule_identity,"exact_rule_result":self.exact_rule_result,"eligible_alternatives":list(self.eligible_alternatives),"selection_reason":self.selection_reason,"authority_refs":list(self.authority_refs),"routing_completed_before_execution":True}

def route_workflow_before_execution(request:RouteRequest,profiles:tuple[WorkflowProfile,...])->RouteDecision:
    eligible=tuple(sorted((p for p in profiles if p.active and not p.superseded and request.request_type in p.eligible_request_types and request.compilation_target in p.eligible_targets and request.risk_class in p.allowed_risk_classes),key=lambda p:p.profile_id))
    if not eligible:raise ManualShadowError("UNMATCHED_WORKFLOW_PROFILE","no eligible workflow profile")
    if len(eligible)>1:raise ManualShadowError("AMBIGUOUS_HIGH_RISK_ROUTE" if request.risk_class.lower() in {"high","critical"} else "NONDETERMINISTIC_ROUTE","multiple eligible profiles",eligible=tuple(p.profile_id for p in eligible))
    p=eligible[0];rule=_hash({"request":request.__dict__,"profile":p.as_dict()})
    return RouteDecision(p.profile_id,p.version,p.sha256,rule,"EXACT_DETERMINISTIC_MATCH",(),"exact request target risk and active registry match",p.authority_refs,True)

@dataclass(frozen=True)
class ShadowStep:
    shadow_step_id:str;sequence_index:int;step_kind:ShadowStepKind;actor_kind:str;actor_identity:str;action_or_decision:str;input_refs:tuple[str,...];output_refs:tuple[str,...];authority_boundary:str;observed_condition:str;failure_context:str;cost_record:str;cost_not_applicable_basis:str;artifact_refs:tuple[str,...];mapped_workflow_node_id:str;exclusion_reason:str;provenance:str
    def __post_init__(self):
        _text(self.shadow_step_id,"shadow_step_id");_text(self.actor_kind,"actor_kind");_text(self.actor_identity,"actor_identity");_text(self.action_or_decision,"action_or_decision");_text(self.authority_boundary,"authority_boundary");_text(self.observed_condition,"observed_condition");_text(self.provenance,"provenance")
        if not self.mapped_workflow_node_id and not self.exclusion_reason:raise ManualShadowError("UNMAPPED_SHADOW_STEP","step requires node mapping or governed exclusion")
        if not self.cost_record and not self.cost_not_applicable_basis:raise ManualShadowError("MISSING_COST_OR_NOT_APPLICABLE_BASIS","cost state required")
    def as_dict(self)->dict[str,Any]:return {"shadow_step_id":self.shadow_step_id,"sequence_index":self.sequence_index,"step_kind":self.step_kind.value,"actor_kind":self.actor_kind,"actor_identity":self.actor_identity,"action_or_decision":self.action_or_decision,"input_refs":list(self.input_refs),"output_refs":list(self.output_refs),"authority_boundary":self.authority_boundary,"observed_condition":self.observed_condition,"failure_context":self.failure_context,"cost_record":self.cost_record,"cost_not_applicable_basis":self.cost_not_applicable_basis,"artifact_refs":list(self.artifact_refs),"mapped_workflow_node_id":self.mapped_workflow_node_id,"exclusion_reason":self.exclusion_reason,"provenance":self.provenance}

@dataclass(frozen=True)
class ManualShadowTrace:
    workflow_identity:str;node_identity:str;input_snapshot_ref:str;proposed_automated_output_ref:str;shadow_review_request_ref:str;reviewer_identity:str;reviewer_response:str;comparison:str;divergence_classification:str;final_disposition:str;authority_ref:str;observed_at:str;invalidation_state:str;steps:tuple[ShadowStep,...];fixture_classification:FixtureClassification=FixtureClassification.SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL;actual_expert_behavior:bool=False;real_manual_shadow_evidence:bool=False;production_ready:bool=False
    _anchor:str=field(init=False,repr=False,compare=False)
    def __post_init__(self):
        for value,name in ((self.workflow_identity,"workflow_identity"),(self.node_identity,"node_identity"),(self.input_snapshot_ref,"input_snapshot_ref"),(self.proposed_automated_output_ref,"proposed_output_ref"),(self.shadow_review_request_ref,"review_request_ref"),(self.comparison,"comparison"),(self.divergence_classification,"divergence_classification"),(self.final_disposition,"final_disposition"),(self.authority_ref,"authority_ref"),(self.observed_at,"observed_at"),(self.invalidation_state,"invalidation_state")):_text(value,name)
        if self.actual_expert_behavior or self.real_manual_shadow_evidence or self.production_ready:raise ManualShadowError("SYNTHETIC_FIXTURE_FALSE_AUTHORITY_CLAIM","synthetic fixture is not human approval")
        if tuple(x.sequence_index for x in self.steps)!=tuple(range(len(self.steps))):raise ManualShadowError("NON_CANONICAL_SHADOW_SEQUENCE","steps must be contiguous and ordered")
        if set(x.step_kind.value for x in self.steps)!=set(SHADOW_STEP_KINDS):raise ManualShadowError("INCOMPLETE_SHADOW_STEP_COVERAGE","all eight step kinds required")
        object.__setattr__(self,"_anchor",_hash(self._payload()))
    def _payload(self)->dict[str,Any]:return {"workflow_identity":self.workflow_identity,"node_identity":self.node_identity,"input_snapshot_ref":self.input_snapshot_ref,"proposed_automated_output_ref":self.proposed_automated_output_ref,"shadow_review_request_ref":self.shadow_review_request_ref,"reviewer_identity":self.reviewer_identity,"reviewer_response":self.reviewer_response,"comparison":self.comparison,"divergence_classification":self.divergence_classification,"final_disposition":self.final_disposition,"authority_ref":self.authority_ref,"observed_at":self.observed_at,"invalidation_state":self.invalidation_state,"steps":[x.as_dict() for x in self.steps],"fixture_classification":self.fixture_classification.value,"actual_expert_behavior":False,"real_manual_shadow_evidence":False,"human_approval_issued":False,"automation_promotion_available":False,"production_ready":False,"certified":False}
    @property
    def trace_identity(self)->str:return _hash(self._payload())
    def as_dict(self)->dict[str,Any]:
        p=self._payload();identity=_hash(p)
        if identity!=self._anchor:raise ManualShadowError("MUTATED_GOVERNED_OBJECT","trace changed after compilation")
        p["trace_identity"]=identity;return p

def compile_manual_shadow_trace(**values:Any)->ManualShadowTrace:return ManualShadowTrace(**values)

@dataclass(frozen=True)
class CodeResultReceipt:
    receipt_id:str;node_id:str;node_version:str;operation_kind:str;input_sha256:str;output_sha256:str;validator_identity:str;authority_refs:tuple[str,...];success:bool
    @property
    def receipt_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"receipt_id":self.receipt_id,"node_id":self.node_id,"node_version":self.node_version,"operation_kind":self.operation_kind,"input_sha256":self.input_sha256,"output_sha256":self.output_sha256,"validator_identity":self.validator_identity,"authority_refs":list(self.authority_refs),"success":self.success}

@dataclass(frozen=True)
class PhaseLocalCapsuleBinding:
    node_id:str;node_version:str;agent_adapter_ref:str;jit_capsule_id:str;jit_capsule_sha256:str;input_contract_version:str;output_contract_version:str;model_policy_ref:str;tool_permissions:tuple[str,...];skill_recipe_input_identity:str;skill_recipe_output_identity:str;evaluation_receipts:tuple[str,...];maturity_receipts:tuple[str,...];active:bool=True;scope:tuple[str,...]=()
    def __post_init__(self):
        _sha(self.jit_capsule_sha256,"jit_capsule_sha256")
        if not self.tool_permissions or "DEFAULT_DENY" not in self.tool_permissions:raise ManualShadowError("TOOL_PERMISSIONS_NOT_DEFAULT_DENY","least privilege required")
        if not self.evaluation_receipts or not self.maturity_receipts:raise ManualShadowError("UNEVALUATED_AGENT_CAPSULE","evaluation and maturity receipts required")

@dataclass(frozen=True)
class NodeBoundaryValidationReceipt:
    node_id:str;actor_kind:str;code_result_identity:str;capsule_identity:str;execution_performed:bool=False;network_used:bool=False;provider_used:bool=False
    @property
    def receipt_identity(self)->str:return _hash(self.__dict__)

def validate_node_execution_boundary(node:WorkflowNode,code_result_receipt:CodeResultReceipt|None=None,agent_capsule_binding:PhaseLocalCapsuleBinding|None=None)->NodeBoundaryValidationReceipt:
    if node.actor_kind is ActorKind.DETERMINISTIC_CODE_NODE:
        if agent_capsule_binding is not None:raise ManualShadowError("DETERMINISTIC_WORK_DELEGATED_TO_AGENT","code-owned work cannot enter agent capsule")
        if code_result_receipt is None or not code_result_receipt.success or code_result_receipt.node_id!=node.node_id:raise ManualShadowError("MISSING_EXACT_CODE_RESULT_RECEIPT","exact successful code receipt required")
        return NodeBoundaryValidationReceipt(node.node_id,node.actor_kind.value,code_result_receipt.receipt_identity,"",False,False,False)
    if node.actor_kind is ActorKind.GOVERNED_AGENT_NODE:
        if code_result_receipt is not None:raise ManualShadowError("ACTOR_BOUNDARY_CONFLICT","agent node cannot own code result")
        b=agent_capsule_binding
        if b is None or not b.active or b.node_id!=node.node_id or node.node_id not in b.scope:raise ManualShadowError("INVALID_PHASE_LOCAL_CAPSULE_BINDING","active exact scoped capsule required")
        identity=_hash(b.__dict__);return NodeBoundaryValidationReceipt(node.node_id,node.actor_kind.value,"",identity,False,False,False)
    if node.actor_kind is ActorKind.HUMAN_NODE:raise ManualShadowError("HUMAN_APPROVAL_NOT_PROVIDED","synthetic fixture cannot approve human node")
    return NodeBoundaryValidationReceipt(node.node_id,node.actor_kind.value,"","",False,False,False)

@dataclass(frozen=True)
class ImmutableInputSnapshot:
    snapshot_id:str;snapshot_version:str;snapshot_sha256:str;active:bool=True;superseded:bool=False;invalidated:bool=False
    @property
    def snapshot_identity(self)->str:return _hash(self.__dict__)
    def as_dict(self)->dict[str,Any]:return dict(self.__dict__)
class ProposedOutputStatus(str,Enum):PASS="PASS";FAIL="FAIL"
@dataclass(frozen=True)
class ProposedAutomatedOutput:
    output_id:str;output_version:str;output_sha256:str;status:ProposedOutputStatus;authority_identity:str
    @property
    def output_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"output_id":self.output_id,"output_version":self.output_version,"output_sha256":self.output_sha256,"status":self.status.value,"authority_identity":self.authority_identity}
@dataclass(frozen=True)
class ShadowReviewRequest:
    request_id:str;workflow_identity:str;node_identity:str;input_snapshot:ImmutableInputSnapshot;proposed_output:ProposedAutomatedOutput;fixture_classification:str;requested_reviewer_role:str;authority_requirement:str
    def __post_init__(self):
        if self.fixture_classification!=SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL:raise ManualShadowError("REAL_HUMAN_APPROVAL_NOT_PROVEN","only synthetic shadow fixtures are admitted")
    @property
    def request_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"request_id":self.request_id,"workflow_identity":self.workflow_identity,"node_identity":self.node_identity,"input_snapshot":self.input_snapshot.as_dict(),"proposed_output":self.proposed_output.as_dict(),"fixture_classification":self.fixture_classification,"requested_reviewer_role":self.requested_reviewer_role,"authority_requirement":self.authority_requirement}
class ReviewerDispositionStatus(str,Enum):ACTIVE="ACTIVE";WITHDRAWN="WITHDRAWN"
@dataclass(frozen=True)
class ReviewerDisposition:
    reviewer_identity:str;response:str;response_sha256:str;status:ReviewerDispositionStatus;authority_sha256:str;recorded_at:str
    @property
    def disposition_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"reviewer_identity":self.reviewer_identity,"response":self.response,"response_sha256":self.response_sha256,"status":self.status.value,"authority_sha256":self.authority_sha256,"recorded_at":self.recorded_at}

@dataclass(frozen=True)
class ManualShadowEvaluation:
    review_request:ShadowReviewRequest;reviewer_disposition:ReviewerDisposition|None;divergence_class:DivergenceClass;disposition:ShadowDisposition;comparison_sha256:str;comparison_summary:str;limitations:tuple[str,...]
    _anchor:str=field(init=False,repr=False,compare=False)
    def __post_init__(self):object.__setattr__(self,"_anchor",_hash(self._payload()))
    def _payload(self)->dict[str,Any]:return {"review_request":self.review_request.as_dict(),"reviewer_disposition":None if self.reviewer_disposition is None else self.reviewer_disposition.as_dict(),"divergence_class":self.divergence_class.value,"disposition":self.disposition.value,"comparison_sha256":self.comparison_sha256,"comparison_summary":self.comparison_summary,"limitations":list(self.limitations),"fixture_classification":SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL,"human_approval_issued":False,"real_manual_shadow_evidence":False,"automation_promotion_available":False,"open_evidence_gates":["manual_shadow_evidence","external_validation"],"production_ready":False,"certified":False}
    @property
    def evaluation_identity(self)->str:return _hash(self._payload())
    @property
    def receipt_identity(self)->str:return self.evaluation_identity
    @property
    def automation_promotion_available(self)->bool:return False
    def as_dict(self)->dict[str,Any]:
        p=self._payload();identity=_hash(p)
        if identity!=self._anchor:raise ManualShadowError("MUTATED_GOVERNED_OBJECT","evaluation changed")
        p["evaluation_identity"]=identity;return p

def compile_manual_shadow_evaluation(*,review_request:ShadowReviewRequest,reviewer_disposition:ReviewerDisposition|None,divergence_class:DivergenceClass,comparison_sha256:str,comparison_summary:str,limitations:tuple[str,...])->ManualShadowEvaluation:
    snapshot=review_request.input_snapshot;proposal=review_request.proposed_output
    stale=(not snapshot.active or snapshot.superseded or snapshot.invalidated)
    failed=proposal.status is ProposedOutputStatus.FAIL
    missing=reviewer_disposition is None
    withdrawn=reviewer_disposition is not None and reviewer_disposition.status is ReviewerDispositionStatus.WITHDRAWN
    if divergence_class is DivergenceClass.EXACT_AGREEMENT and (stale or failed or missing or withdrawn):raise ManualShadowError("DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE","agreement contradicts evidence")
    if divergence_class is DivergenceClass.STALE_INPUT_SNAPSHOT and not stale:raise ManualShadowError("DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE","snapshot is current")
    if divergence_class is DivergenceClass.FAILED_PROPOSED_OUTPUT and not failed:raise ManualShadowError("DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE","proposal passed")
    if divergence_class is DivergenceClass.MISSING_REVIEWER and not missing:raise ManualShadowError("DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE","reviewer exists")
    if divergence_class is DivergenceClass.WITHDRAWN_REVIEWER_DISPOSITION and not withdrawn:raise ManualShadowError("DISPOSITION_CONTRADICTS_SHADOW_EVIDENCE","reviewer active")
    mapping={DivergenceClass.EXACT_AGREEMENT:ShadowDisposition.PASS_EXACT_AGREEMENT,DivergenceClass.ACCEPTABLE_BOUNDED_DIFFERENCE:ShadowDisposition.PASS_ACCEPTABLE_BOUNDED_DIFFERENCE,DivergenceClass.SEMANTIC_DIVERGENCE:ShadowDisposition.FAIL_SEMANTIC_DIVERGENCE,DivergenceClass.AUTHORITY_VIOLATION:ShadowDisposition.FAIL_AUTHORITY_VIOLATION,DivergenceClass.MISSING_REVIEWER:ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE,DivergenceClass.WITHDRAWN_REVIEWER_DISPOSITION:ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE,DivergenceClass.STALE_INPUT_SNAPSHOT:ShadowDisposition.BLOCKED_STALE_OR_FAILED_PROPOSAL,DivergenceClass.FAILED_PROPOSED_OUTPUT:ShadowDisposition.BLOCKED_STALE_OR_FAILED_PROPOSAL}
    return ManualShadowEvaluation(review_request,reviewer_disposition,divergence_class,mapping[divergence_class],comparison_sha256,comparison_summary,tuple(limitations))

@dataclass(frozen=True)
class ManualShadowReceipt:
    review_request:ShadowReviewRequest;input_snapshot:ImmutableInputSnapshot;proposed_output:ProposedAutomatedOutput;reviewer:ReviewerDisposition|None;divergence_class:DivergenceClass;disposition:ShadowDisposition;comparison:str;authority_identity:str;predecessor_receipts:tuple[str,...];active:bool=True
    _anchor:str=field(init=False,repr=False,compare=False)
    def __post_init__(self):object.__setattr__(self,"_anchor",_hash(self._payload()))
    def _payload(self)->dict[str,Any]:return {"review_request":self.review_request.__dict__,"input_snapshot":self.input_snapshot.__dict__,"proposed_output":self.proposed_output.__dict__,"reviewer":None if self.reviewer is None else self.reviewer.__dict__,"divergence_class":self.divergence_class.value,"disposition":self.disposition.value,"comparison":self.comparison,"authority_identity":self.authority_identity,"predecessor_receipts":list(self.predecessor_receipts),"active":self.active,"fixture_classification":SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL,"human_approval_issued":False,"automation_promotion_available":False,"real_manual_shadow_evidence":False,"production_ready":False,"certified":False}
    @property
    def receipt_identity(self)->str:return _hash(self._payload())
    def as_dict(self)->dict[str,Any]:
        p=self._payload();identity=_hash(p)
        if identity!=self._anchor:raise ManualShadowError("MUTATED_GOVERNED_OBJECT","receipt changed")
        p["receipt_identity"]=identity;return p

def evaluate_manual_shadow(*,review_request:ShadowReviewRequest,input_snapshot:ImmutableInputSnapshot,proposed_output:ProposedAutomatedOutput,reviewer:ReviewerDisposition|None,divergence_class:DivergenceClass,comparison:str,authority_identity:str,predecessor_receipts:tuple[str,...])->ManualShadowReceipt:
    if review_request.fixture_classification!=SYNTHETIC_SHADOW_FIXTURE_NOT_HUMAN_APPROVAL:raise ManualShadowError("INVALID_FIXTURE_CLASSIFICATION","synthetic classification required")
    if review_request.input_snapshot_identity!=input_snapshot.snapshot_identity or review_request.proposed_output_identity!=proposed_output.output_identity:raise ManualShadowError("REVIEW_REQUEST_INPUT_MISMATCH","request references mismatch")
    if not input_snapshot.active or divergence_class is DivergenceClass.STALE_INPUT_SNAPSHOT:disposition=ShadowDisposition.BLOCKED_STALE_OR_FAILED_PROPOSAL
    elif proposed_output.status!="PASS" or divergence_class is DivergenceClass.FAILED_PROPOSED_OUTPUT:disposition=ShadowDisposition.BLOCKED_STALE_OR_FAILED_PROPOSAL
    elif reviewer is None or divergence_class is DivergenceClass.MISSING_REVIEWER:disposition=ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE
    elif reviewer.status=="WITHDRAWN" or divergence_class is DivergenceClass.WITHDRAWN_REVIEWER_DISPOSITION:disposition=ShadowDisposition.BLOCKED_REVIEWER_EVIDENCE
    elif divergence_class is DivergenceClass.EXACT_AGREEMENT:disposition=ShadowDisposition.PASS_EXACT_AGREEMENT
    elif divergence_class is DivergenceClass.ACCEPTABLE_BOUNDED_DIFFERENCE:disposition=ShadowDisposition.PASS_ACCEPTABLE_BOUNDED_DIFFERENCE
    elif divergence_class is DivergenceClass.SEMANTIC_DIVERGENCE:disposition=ShadowDisposition.FAIL_SEMANTIC_DIVERGENCE
    else:disposition=ShadowDisposition.FAIL_AUTHORITY_VIOLATION
    return ManualShadowReceipt(review_request,input_snapshot,proposed_output,reviewer,divergence_class,disposition,comparison,authority_identity,tuple(predecessor_receipts),disposition in {ShadowDisposition.PASS_EXACT_AGREEMENT,ShadowDisposition.PASS_ACCEPTABLE_BOUNDED_DIFFERENCE})

class ShadowAction(str,Enum):ISSUE="ISSUE";INVALIDATE="INVALIDATE";ROLLBACK="ROLLBACK"
class ShadowAuthorityStatus(str,Enum):ACTIVE="ACTIVE";SUPERSEDED="SUPERSEDED";INVALIDATED="INVALIDATED"
@dataclass(frozen=True,init=False)
class ShadowAuthority:
    authority_id:str;authority_version:str;authority_sha256:str;permitted_actions:tuple[ShadowAction,...];applicable_scope:tuple[str,...];status:ShadowAuthorityStatus=ShadowAuthorityStatus.ACTIVE
    def __init__(self,authority_id:str,authority_version:str,authority_sha256:str,permitted_actions:tuple[ShadowAction,...],applicable_scope:tuple[str,...],status:ShadowAuthorityStatus=ShadowAuthorityStatus.ACTIVE):
        object.__setattr__(self,"authority_id",authority_id);object.__setattr__(self,"authority_version",authority_version);object.__setattr__(self,"authority_sha256",authority_sha256);object.__setattr__(self,"permitted_actions",permitted_actions);object.__setattr__(self,"applicable_scope",applicable_scope);object.__setattr__(self,"status",status)
    @property
    def authority_identity(self)->str:return _hash({"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"permitted_actions":[x.value for x in self.permitted_actions],"applicable_scope":list(self.applicable_scope),"status":self.status.value})
@dataclass(frozen=True)
class ShadowCommand:
    command_id:str;action:ShadowAction;resource_id:str;payload_sha256:str;expected_authority_identity:str
    @property
    def command_identity(self)->str:return _hash({"command_id":self.command_id,"action":self.action.value,"resource_id":self.resource_id,"payload_sha256":self.payload_sha256,"expected_authority_identity":self.expected_authority_identity})
@dataclass(frozen=True)
class ShadowTransitionReceipt:
    action:ShadowAction;prior_receipt_identity:str;active_after:bool;historical_receipt_preserved:bool;command_identity:str;authority_identity:str
    @property
    def transition_identity(self)->str:return _hash(self.__dict__)

def compute_shadow_issue_payload_sha256(receipt:Any)->str:return _hash(receipt.as_dict())
def compute_shadow_transition_payload_sha256(prior_receipt_identity:str,action:ShadowAction)->str:return _hash({"prior_receipt_identity":prior_receipt_identity,"action":action.value})
def _check(command:ShadowCommand,authority:ShadowAuthority,action:ShadowAction,resource:str,payload:str):
    if authority.status is not ShadowAuthorityStatus.ACTIVE:raise ManualShadowError("INACTIVE_AUTHORITY","authority inactive")
    if action not in authority.permitted_actions or command.action is not action:raise ManualShadowError("UNAUTHORIZED_ACTION","action not permitted")
    if command.resource_id!=resource:raise ManualShadowError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=payload:raise ManualShadowError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    if command.expected_authority_identity!=authority.authority_identity:raise ManualShadowError("AUTHORITY_IDENTITY_MISMATCH","authority mismatch")
def issue_manual_shadow_receipt(receipt:Any,command:ShadowCommand,authority:ShadowAuthority)->Any:_check(command,authority,ShadowAction.ISSUE,receipt.receipt_identity,compute_shadow_issue_payload_sha256(receipt));return receipt
def validate_repeat_manual_shadow(existing:ManualShadowReceipt,repeated:ManualShadowReceipt)->ManualShadowReceipt:
    if existing.receipt_identity!=repeated.receipt_identity:raise ManualShadowError("CONFLICTING_REPEAT_COMMAND","payload differs")
    return existing
def _transition(receipt:ManualShadowReceipt,command:ShadowCommand,authority:ShadowAuthority,action:ShadowAction)->ShadowTransitionReceipt:
    receipt.as_dict();_check(command,authority,action,receipt.receipt_identity,compute_shadow_transition_payload_sha256(receipt.receipt_identity,action));return ShadowTransitionReceipt(action,receipt.receipt_identity,False,True,command.command_identity,authority.authority_identity)
def invalidate_manual_shadow_receipt(receipt:ManualShadowReceipt,command:ShadowCommand,authority:ShadowAuthority)->ShadowTransitionReceipt:return _transition(receipt,command,authority,ShadowAction.INVALIDATE)
def rollback_manual_shadow_receipt(receipt:ManualShadowReceipt,command:ShadowCommand,authority:ShadowAuthority)->ShadowTransitionReceipt:return _transition(receipt,command,authority,ShadowAction.ROLLBACK)
