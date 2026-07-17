"""Selective, immutable repair planning for the ST-08.05 offline branch."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib, json, re
from typing import Any

from .root_cause_diagnosis import (
    DiagnosticLayer, DiagnosisStatus, RepairAndInvalidationGraph, RepairField,
    RootCauseDiagnosis, RootCauseDiagnosisError,
)

STORY_ID = "ST-08.05"
_SHA = re.compile(r"^[0-9a-f]{64}$")

class SelectiveRepairError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message); self.code=code; self.context=dict(context)
RepairError = SelectiveRepairError

class RepairOwnerKind(str, Enum):
    BUILDER_OWNED_PHASE="Builder_owned_phase"
    BUILDER_OWNED_CAPABILITY="Builder_owned_capability"
    BUILDER_OWNED_CONTRACT_PROJECTION="Builder_owned_contract_projection"
class RepairAction(str, Enum):
    ACCEPT_DIAGNOSIS="accept_diagnosis"
    COMPILE_CANDIDATE="compile_candidate"
    COMMIT_CANDIDATE="commit_candidate"
    INVALIDATE="invalidate"
    ROLLBACK="rollback"
    ESCALATE="escalate"
    ISSUE="issue"
class RepairAuthorityStatus(str, Enum): ACTIVE="active"; SUPERSEDED="superseded"; INVALIDATED="invalidated"
class RerunRequirementKind(str, Enum): DIRECT_TEST="direct_test"; DESCENDANT_REGRESSION="descendant_regression"; BENCHMARK="benchmark"; PROTECTED_CASE="protected_case"
class RerunRequirementStatus(str, Enum): AVAILABLE="available"; BLOCKED="blocked"
class ProtectedCasePolicyStatus(str, Enum): NOT_APPLICABLE="not_applicable"; AUTHORIZED="authorized"; NOT_AUTHORIZED="not_authorized"
class LocalRerunStatus(str, Enum): PASS="pass"; FAIL="fail"; BLOCKED="blocked"
class EscalationTrigger(str, Enum):
    CONSTITUTIONAL_DECISION_CHANGE="constitutional_decision_change"
    BOUNDARY_BROADENING="boundary_broadening"
    STABLE_SKILL_CHANGE="stable_skill_change"
    CONTRADICTORY_DOCTRINE="contradictory_doctrine"
    REPEAT_LIMIT_REACHED="repeat_limit_reached"
    AMBIGUOUS_RESPONSIBILITY_OR_AUTHORITY="ambiguous_responsibility_or_authority"

def canonical_json_bytes(v: Any)->bytes: return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def canonical_sha256(v: Any)->str: return hashlib.sha256(canonical_json_bytes(v)).hexdigest()
def _sha(v:str,n:str)->None:
    if not isinstance(v,str) or not _SHA.fullmatch(v): raise SelectiveRepairError("INVALID_IMMUTABLE_IDENTITY",f"{n} must be SHA-256")
def _text(v:str,n:str)->None:
    if not isinstance(v,str) or not v.strip(): raise SelectiveRepairError("MISSING_GOVERNED_FIELD",f"{n} required")
def _authority(command, authority, action):
    if not isinstance(authority,RepairAuthority): raise SelectiveRepairError("INVALID_AUTHORITY_EVIDENCE","typed authority required")
    if authority.status is not RepairAuthorityStatus.ACTIVE: raise SelectiveRepairError("INACTIVE_AUTHORITY","authority inactive")
    if not isinstance(command,RepairCommand) or command.action is not action or action not in authority.permitted_actions: raise SelectiveRepairError("UNAUTHORIZED_ACTION","action unauthorized")
    if command.expected_authority_identity!=authority.authority_identity: raise SelectiveRepairError("AUTHORITY_IDENTITY_MISMATCH","authority mismatch")

@dataclass(frozen=True)
class RepairAuthority:
    authority_id:str; authority_version:str; authority_sha256:str; permitted_actions:tuple[RepairAction,...]; status:RepairAuthorityStatus=RepairAuthorityStatus.ACTIVE
    def __post_init__(self):
        _text(self.authority_id,"authority_id"); _text(self.authority_version,"authority_version"); _sha(self.authority_sha256,"authority_sha256")
        if not self.permitted_actions or any(not isinstance(x,RepairAction) for x in self.permitted_actions): raise SelectiveRepairError("INVALID_AUTHORITY_GRANT","typed grants required")
    @property
    def authority_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"permitted_actions":[x.value for x in self.permitted_actions],"status":self.status.value,"story_id":STORY_ID}
@dataclass(frozen=True)
class RepairCommand:
    command_id:str; action:RepairAction; resource_id:str; payload_sha256:str; expected_authority_identity:str
    def __post_init__(self):
        _text(self.command_id,"command_id")
        if not isinstance(self.action,RepairAction): raise SelectiveRepairError("INVALID_COMMAND_ACTION","typed action required")
        _sha(self.resource_id,"resource_id"); _sha(self.payload_sha256,"payload_sha256"); _sha(self.expected_authority_identity,"expected_authority_identity")
    @property
    def command_identity(self): return canonical_sha256({"command_id":self.command_id,"action":self.action.value,"resource_id":self.resource_id,"payload_sha256":self.payload_sha256,"expected_authority_identity":self.expected_authority_identity})
@dataclass(frozen=True)
class ImmutableRepairSubject:
    subject_id:str; subject_version:str; subject_sha256:str; active:bool; superseded:bool; invalidated:bool
    def __post_init__(self): _text(self.subject_id,"subject_id"); _text(self.subject_version,"subject_version"); _sha(self.subject_sha256,"subject_sha256")
    @property
    def subject_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"subject_id":self.subject_id,"subject_version":self.subject_version,"subject_sha256":self.subject_sha256,"active":self.active,"superseded":self.superseded,"invalidated":self.invalidated}
@dataclass(frozen=True)
class RepairFieldChange:
    layer:DiagnosticLayer; field_name:str; prior_value_sha256:str; proposed_value_sha256:str
    def __post_init__(self):
        if not isinstance(self.layer,DiagnosticLayer): raise SelectiveRepairError("INVALID_REPAIR_LAYER","typed layer required")
        _text(self.field_name,"field_name"); _sha(self.prior_value_sha256,"prior"); _sha(self.proposed_value_sha256,"proposed")
        if self.prior_value_sha256==self.proposed_value_sha256: raise SelectiveRepairError("NO_EFFECT_REPAIR","repair must change bytes")
    def as_dict(self): return {"layer":self.layer.value,"field_name":self.field_name,"prior_value_sha256":self.prior_value_sha256,"proposed_value_sha256":self.proposed_value_sha256}

@dataclass(frozen=True)
class AcceptedDiagnosis:
    status:str; diagnosis_identity:str; diagnosis_version:str; graph_identity:str; failure_id:str; stable_failure_code:str; selected_root_cause:str; confidence_basis:tuple[str,...]; smallest_responsible_layer:DiagnosticLayer; responsible_owner:str; responsible_authority_ref:str; permitted_repair_fields:tuple[RepairField,...]; frozen_state:tuple[str,...]; affected_descendants:tuple[str,...]; targeted_regression_requirements:tuple[str,...]; rollback_conditions:tuple[str,...]; escalation_conditions:tuple[str,...]; command_identity:str; authority_identity:str; repair_executed:bool=False
    @property
    def acceptance_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"status":self.status,"diagnosis_identity":self.diagnosis_identity,"diagnosis_version":self.diagnosis_version,"graph_identity":self.graph_identity,"failure_id":self.failure_id,"stable_failure_code":self.stable_failure_code,"selected_root_cause":self.selected_root_cause,"confidence_basis":list(self.confidence_basis),"smallest_responsible_layer":self.smallest_responsible_layer.value,"responsible_owner":self.responsible_owner,"responsible_authority_ref":self.responsible_authority_ref,"permitted_repair_fields":[x.as_dict() for x in self.permitted_repair_fields],"frozen_state":list(self.frozen_state),"affected_descendants":list(self.affected_descendants),"targeted_regression_requirements":list(self.targeted_regression_requirements),"rollback_conditions":list(self.rollback_conditions),"escalation_conditions":list(self.escalation_conditions),"command_identity":self.command_identity,"authority_identity":self.authority_identity,"repair_executed":False}

def compute_accept_payload_sha256(*,diagnosis,graph):
    try: return canonical_sha256({"diagnosis_identity":diagnosis.diagnosis_identity,"graph_identity":graph.graph_identity})
    except RootCauseDiagnosisError as e: raise SelectiveRepairError("ALTERED_DIAGNOSIS",str(e)) from e
compute_accept_diagnosis_payload_sha256=compute_accept_payload_sha256
def accept_root_cause_diagnosis(*,diagnosis,graph,command,authority):
    _authority(command,authority,RepairAction.ACCEPT_DIAGNOSIS)
    try: diagnosis.as_dict(); graph.as_dict()
    except RootCauseDiagnosisError as e: raise SelectiveRepairError("ALTERED_DIAGNOSIS",str(e)) from e
    if diagnosis.status is not DiagnosisStatus.LOCALIZED: raise SelectiveRepairError("DIAGNOSIS_NOT_ACCEPTABLE","localized diagnosis required")
    if graph.root_cause_diagnosis_ref!=diagnosis.diagnosis_identity: raise SelectiveRepairError("DIAGNOSIS_GRAPH_MISMATCH","graph mismatch")
    if command.resource_id!=diagnosis.diagnosis_identity: raise SelectiveRepairError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=compute_accept_payload_sha256(diagnosis=diagnosis,graph=graph): raise SelectiveRepairError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    return AcceptedDiagnosis("ACCEPTED_ROOT_CAUSE",diagnosis.diagnosis_identity,diagnosis.diagnosis_version,graph.graph_identity,diagnosis.classification.failure_id,diagnosis.classification.stable_code,diagnosis.selected_root_cause,diagnosis.confidence_basis,diagnosis.smallest_supported_responsible_layer,diagnosis.responsible_owner,diagnosis.responsible_authority_ref,graph.permitted_repair_fields,graph.frozen_upstream_and_unaffected_state,graph.invalidated_descendant_set,graph.targeted_regression_suite,graph.rollback_requirements,graph.escalation_conditions,command.command_identity,authority.authority_identity)

@dataclass(frozen=True)
class SelectiveRepairCandidate:
    accepted_diagnosis_identity:str; graph_identity:str; owner_kind:RepairOwnerKind; responsible_unit:str; parent_subject_identity:str; parent_subject_version:str; parent_subject_sha256:str; candidate_version:str; field_changes:tuple[RepairFieldChange,...]; preserved_state:tuple[str,...]; affected_descendants:tuple[str,...]; command_identity:str; authority_identity:str; primary_responsible_units:tuple[str,...]; external_product_unit:None=None; whole_run_regenerated:bool=False; prior_bytes_mutated:bool=False; historical_state_deleted:bool=False; external_runtime_executed:bool=False; production_ready:bool=False; certified:bool=False
    @property
    def candidate_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"accepted_diagnosis_identity":self.accepted_diagnosis_identity,"graph_identity":self.graph_identity,"owner_kind":self.owner_kind.value,"responsible_unit":self.responsible_unit,"parent_subject_identity":self.parent_subject_identity,"parent_subject_version":self.parent_subject_version,"parent_subject_sha256":self.parent_subject_sha256,"candidate_version":self.candidate_version,"field_changes":[x.as_dict() for x in self.field_changes],"preserved_state":list(self.preserved_state),"affected_descendants":list(self.affected_descendants),"command_identity":self.command_identity,"authority_identity":self.authority_identity,"primary_responsible_units":list(self.primary_responsible_units),"external_product_unit":None,"whole_run_regenerated":False,"prior_bytes_mutated":False,"historical_state_deleted":False,"external_runtime_executed":False,"production_ready":False,"certified":False}
RepairCandidate=SelectiveRepairCandidate
def _candidate_payload(accepted_diagnosis,graph,owner_kind,responsible_unit,parent_subject,candidate_version,field_changes,preserved_state): return {"accepted":accepted_diagnosis.acceptance_identity,"graph":graph.graph_identity,"owner_kind":getattr(owner_kind,"value",owner_kind),"responsible_unit":responsible_unit,"parent":parent_subject.subject_identity,"candidate_version":candidate_version,"field_changes":[x.as_dict() for x in field_changes],"preserved_state":list(preserved_state)}
def compute_candidate_payload_sha256(**kw): return canonical_sha256(_candidate_payload(**kw))
def compile_selective_repair_candidate(*,accepted_diagnosis,graph,owner_kind,responsible_unit,parent_subject,candidate_version,field_changes,preserved_state,command,authority):
    _authority(command,authority,RepairAction.COMPILE_CANDIDATE)
    if not isinstance(owner_kind,RepairOwnerKind): raise SelectiveRepairError("EXTERNAL_PRODUCT_REPAIR_PROHIBITED","Builder owner required")
    if not isinstance(responsible_unit,str) or not responsible_unit.strip(): raise SelectiveRepairError("EXACTLY_ONE_RESPONSIBLE_UNIT_REQUIRED","one unit required")
    if responsible_unit!=graph.responsible_phase_or_capability: raise SelectiveRepairError("INVALID_RESPONSIBLE_UNIT","unit mismatch")
    if not parent_subject.active or parent_subject.superseded or parent_subject.invalidated: raise SelectiveRepairError("INACTIVE_PARENT_VERSION","active parent required")
    if candidate_version==parent_subject.subject_version: raise SelectiveRepairError("NEW_CANDIDATE_VERSION_REQUIRED","new version required")
    if not field_changes: raise SelectiveRepairError("MISSING_REPAIR_FIELD_CHANGE","field change required")
    allowed={(x.layer,x.field_name) for x in graph.permitted_repair_fields}
    if any((x.layer,x.field_name) not in allowed for x in field_changes): raise SelectiveRepairError("REPAIR_FIELD_OUTSIDE_DIAGNOSED_SCOPE","field outside diagnosis")
    if set(preserved_state)!=set(graph.frozen_upstream_and_unaffected_state): raise SelectiveRepairError("PRESERVED_STATE_MISMATCH","frozen state mismatch")
    payload=_candidate_payload(accepted_diagnosis,graph,owner_kind,responsible_unit,parent_subject,candidate_version,field_changes,preserved_state)
    if command.resource_id!=parent_subject.subject_identity: raise SelectiveRepairError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=canonical_sha256(payload): raise SelectiveRepairError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    return SelectiveRepairCandidate(accepted_diagnosis.acceptance_identity,graph.graph_identity,owner_kind,responsible_unit,parent_subject.subject_identity,parent_subject.subject_version,parent_subject.subject_sha256,candidate_version,tuple(field_changes),tuple(sorted(preserved_state)),graph.invalidated_descendant_set,command.command_identity,authority.authority_identity,(responsible_unit,))

@dataclass(frozen=True)
class RerunRequirement:
    suite_id:str; target_identity:str; kind:RerunRequirementKind; status:RerunRequirementStatus; blocked_reason:str|None=None; protected_case_policy_ref:str|None=None
    def __post_init__(self):
        _text(self.suite_id,"suite_id"); _text(self.target_identity,"target_identity")
        if self.status is RerunRequirementStatus.BLOCKED and not self.blocked_reason: raise SelectiveRepairError("MISSING_BLOCKED_REQUIREMENT_REASON","blocked reason required")
@dataclass(frozen=True)
class AdjacentUnitEvidence:
    parent_identity:str; child_identity:str; relation:str; reason:str
@dataclass(frozen=True)
class BoundedRerunPlan:
    repair_candidate_identity:str; graph_identity:str; responsible_unit:str; affected_descendants:tuple[str,...]; included_adjacency_evidence:tuple[AdjacentUnitEvidence,...]; excluded_adjacency_evidence:tuple[AdjacentUnitEvidence,...]; requirements:tuple[RerunRequirement,...]; blocked_requirements:tuple[RerunRequirement,...]; applicable_benchmark_refs:tuple[str,...]; protected_case_policy_status:ProtectedCasePolicyStatus; execution_order:tuple[str,...]; stop_conditions:tuple[str,...]; result_receipt_requirements:tuple[str,...]; completion_status:str; external_runtime_executed:bool=False; production_ready:bool=False; certified:bool=False
    @property
    def plan_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"repair_candidate_identity":self.repair_candidate_identity,"graph_identity":self.graph_identity,"responsible_unit":self.responsible_unit,"affected_descendants":list(self.affected_descendants),"included_adjacency_evidence":[x.__dict__ for x in self.included_adjacency_evidence],"excluded_adjacency_evidence":[x.__dict__ for x in self.excluded_adjacency_evidence],"requirements":[{"suite_id":x.suite_id,"target_identity":x.target_identity,"kind":x.kind.value,"status":x.status.value,"blocked_reason":x.blocked_reason,"protected_case_policy_ref":x.protected_case_policy_ref} for x in self.requirements],"blocked_requirements":[x.suite_id for x in self.blocked_requirements],"applicable_benchmark_refs":list(self.applicable_benchmark_refs),"protected_case_policy_status":self.protected_case_policy_status.value,"execution_order":list(self.execution_order),"stop_conditions":list(self.stop_conditions),"result_receipt_requirements":list(self.result_receipt_requirements),"completion_status":self.completion_status,"external_runtime_executed":False,"production_ready":False,"certified":False}
def compile_bounded_rerun_plan(*,candidate,graph,requirements,applicable_benchmark_refs,protected_case_policy_status,execution_order,stop_conditions,result_receipt_requirements,external_execution_requested=False):
    if external_execution_requested: raise SelectiveRepairError("EXTERNAL_RUNTIME_PROHIBITED","external execution prohibited")
    req=tuple(sorted(requirements,key=lambda x:x.suite_id)); ids={x.suite_id for x in req}
    if not set(graph.targeted_regression_suite).issubset(ids): raise SelectiveRepairError("MISSING_REQUIRED_REGRESSION","required suite omitted")
    for x in req:
        if x.status is RerunRequirementStatus.BLOCKED and not x.blocked_reason: raise SelectiveRepairError("MISSING_BLOCKED_REQUIREMENT_REASON","blocked reason required")
        if x.kind is RerunRequirementKind.PROTECTED_CASE and protected_case_policy_status is not ProtectedCasePolicyStatus.AUTHORIZED: raise SelectiveRepairError("PROTECTED_CASE_NOT_AUTHORIZED","policy required")
    inc=tuple(AdjacentUnitEvidence(x.parent_identity,x.child_identity,x.relation,"dependency-proven affected descendant") for x in graph.dependency_edges if x.child_identity in graph.invalidated_descendant_set)
    exc=tuple(AdjacentUnitEvidence(x.parent_identity,x.child_identity,x.relation,"independent or unaffected branch remains frozen") for x in graph.dependency_edges if x.child_identity not in graph.invalidated_descendant_set)
    blocked=tuple(x for x in req if x.status is RerunRequirementStatus.BLOCKED)
    return BoundedRerunPlan(candidate.candidate_identity,graph.graph_identity,graph.responsible_phase_or_capability,graph.invalidated_descendant_set,inc,exc,req,blocked,tuple(applicable_benchmark_refs),protected_case_policy_status,tuple(execution_order),tuple(stop_conditions),tuple(result_receipt_requirements),"BLOCKED_REQUIRED_RESULTS" if blocked else "READY_FOR_LOCAL_RERUN")

@dataclass(frozen=True)
class LocalRerunResult:
    suite_id:str; status:LocalRerunStatus; result_sha256:str
    def __post_init__(self): _text(self.suite_id,"suite_id"); _sha(self.result_sha256,"result_sha256")
    @property
    def result_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"suite_id":self.suite_id,"status":self.status.value,"result_sha256":self.result_sha256}

@dataclass(frozen=True)
class RepairCommitReceipt:
    candidate:SelectiveRepairCandidate; plan:BoundedRerunPlan; local_results:tuple[LocalRerunResult,...]; observations:tuple[str,...]; command_identity:str; authority_identity:str; commit_payload_sha256:str; candidate_anchor:str; result_anchors:tuple[str,...]; status:str="COMMITTED_DEVELOPMENT_CANDIDATE"; active:bool=True; required_suite_coverage_complete:bool=True; external_runtime_executed:bool=False; production_ready:bool=False; certified:bool=False
    @property
    def receipt_identity(self): return canonical_sha256(self._payload())
    def _payload(self): return {"candidate_identity":self.candidate.candidate_identity,"plan_identity":self.plan.plan_identity,"local_results":[x.as_dict() for x in self.local_results],"observations":list(self.observations),"command_identity":self.command_identity,"authority_identity":self.authority_identity,"commit_payload_sha256":self.commit_payload_sha256,"status":self.status,"active":self.active,"required_suite_coverage_complete":True,"external_runtime_executed":False,"production_ready":False,"certified":False}
    def as_dict(self):
        if self.candidate.candidate_identity!=self.candidate_anchor or tuple(x.result_identity for x in self.local_results)!=self.result_anchors: raise SelectiveRepairError("MUTATED_GOVERNED_OBJECT","nested governed value changed")
        p=self._payload(); p["receipt_identity"]=canonical_sha256(p); return p

def compute_commit_payload_sha256(*,candidate,plan,results,observations): return canonical_sha256({"candidate_identity":candidate.candidate_identity,"plan_identity":plan.plan_identity,"results":[x.as_dict() for x in results],"observations":list(observations)})
def issue_repair_commit_receipt(*,candidate,plan,results,observations,command,authority):
    _authority(command,authority,RepairAction.COMMIT_CANDIDATE)
    if plan.repair_candidate_identity!=candidate.candidate_identity: raise SelectiveRepairError("CANDIDATE_PLAN_MISMATCH","plan mismatch")
    required={x.suite_id for x in plan.requirements}; actual={x.suite_id for x in results}
    if required-actual: raise SelectiveRepairError("MISSING_REQUIRED_RERUN_RESULT","result omitted")
    if actual-required: raise SelectiveRepairError("UNPLANNED_RERUN_RESULT","unplanned result")
    for result in results:
        if result.status is LocalRerunStatus.FAIL: raise SelectiveRepairError("REQUIRED_REGRESSION_FAILED","required result failed")
        if result.status is LocalRerunStatus.BLOCKED: raise SelectiveRepairError("REQUIRED_REGRESSION_BLOCKED","required result blocked")
    payload=compute_commit_payload_sha256(candidate=candidate,plan=plan,results=results,observations=observations)
    if command.resource_id!=candidate.candidate_identity: raise SelectiveRepairError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=payload: raise SelectiveRepairError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    if any(not x.startswith(f"{STORY_ID}:") for x in observations): raise SelectiveRepairError("INVALID_OBSERVATION","Story scoped observation required")
    return RepairCommitReceipt(candidate,plan,tuple(results),tuple(observations),command.command_identity,authority.authority_identity,payload,candidate.candidate_identity,tuple(x.result_identity for x in results))

@dataclass(frozen=True)
class RepairEscalationReceipt:
    candidate_identity:str; trigger:EscalationTrigger; affected_authority_sha256:str; required_decision:str; options:tuple[str,...]; evidence_refs:tuple[str,...]; command_identity:str; authority_identity:str; automation_frozen:bool=True; production_ready:bool=False; certified:bool=False
    @property
    def receipt_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"candidate_identity":self.candidate_identity,"trigger":self.trigger.value,"affected_authority_sha256":self.affected_authority_sha256,"required_decision":self.required_decision,"options":list(self.options),"evidence_refs":list(self.evidence_refs),"command_identity":self.command_identity,"authority_identity":self.authority_identity,"automation_frozen":True,"production_ready":False,"certified":False}
def compute_escalation_payload_sha256(*,candidate,trigger,affected_authority_sha256,required_decision,options,evidence_refs): return canonical_sha256({"candidate_identity":candidate.candidate_identity,"trigger":trigger.value,"affected_authority_sha256":affected_authority_sha256,"required_decision":required_decision,"options":list(options),"evidence_refs":list(evidence_refs)})
def issue_repair_escalation_receipt(*,candidate,trigger,affected_authority_sha256,required_decision,options,evidence_refs,command,authority):
    _authority(command,authority,RepairAction.ESCALATE)
    if not required_decision: raise SelectiveRepairError("MISSING_REQUIRED_DECISION","decision required")
    if not options: raise SelectiveRepairError("MISSING_ESCALATION_OPTIONS","options required")
    if not evidence_refs: raise SelectiveRepairError("MISSING_ESCALATION_EVIDENCE","evidence required")
    p=compute_escalation_payload_sha256(candidate=candidate,trigger=trigger,affected_authority_sha256=affected_authority_sha256,required_decision=required_decision,options=options,evidence_refs=evidence_refs)
    if command.resource_id!=candidate.candidate_identity: raise SelectiveRepairError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=p: raise SelectiveRepairError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    return RepairEscalationReceipt(candidate.candidate_identity,trigger,affected_authority_sha256,required_decision,tuple(options),tuple(evidence_refs),command.command_identity,authority.authority_identity)

@dataclass(frozen=True)
class RepairTransitionReceipt:
    prior_receipt_identity:str; action:RepairAction; invalidated_descendants:tuple[str,...]; restored_parent_identity:str|None; command_identity:str; authority_identity:str; active_after:bool=False; historical_candidate_preserved:bool=True; historical_receipt_preserved:bool=True
    @property
    def transition_identity(self): return canonical_sha256(self.as_dict())
    def as_dict(self): return {"prior_receipt_identity":self.prior_receipt_identity,"action":self.action.value,"invalidated_descendants":list(self.invalidated_descendants),"restored_parent_identity":self.restored_parent_identity,"command_identity":self.command_identity,"authority_identity":self.authority_identity,"active_after":False,"historical_candidate_preserved":True,"historical_receipt_preserved":True}
def compute_transition_payload_sha256(*,prior_receipt_identity,action,affected_descendants,restored_parent_identity): return canonical_sha256({"prior_receipt_identity":prior_receipt_identity,"action":action.value,"affected_descendants":list(affected_descendants),"restored_parent_identity":restored_parent_identity})
def _transition(receipt,command,authority,action,affected_descendants,restored_parent_identity):
    _authority(command,authority,action)
    if tuple(affected_descendants)!=receipt.candidate.affected_descendants: raise SelectiveRepairError("INVALIDATION_SCOPE_BROADER_THAN_DIAGNOSIS","scope differs")
    p=compute_transition_payload_sha256(prior_receipt_identity=receipt.receipt_identity,action=action,affected_descendants=affected_descendants,restored_parent_identity=restored_parent_identity)
    if command.resource_id!=receipt.receipt_identity: raise SelectiveRepairError("COMMAND_RESOURCE_MISMATCH","resource mismatch")
    if command.payload_sha256!=p: raise SelectiveRepairError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    return RepairTransitionReceipt(receipt.receipt_identity,action,tuple(affected_descendants),restored_parent_identity,command.command_identity,authority.authority_identity)
def invalidate_repair_receipt(receipt,command,authority,*,affected_descendants=None): return _transition(receipt,command,authority,RepairAction.INVALIDATE,tuple(affected_descendants or receipt.candidate.affected_descendants),None)
def rollback_repair_receipt(receipt,command,authority): return _transition(receipt,command,authority,RepairAction.ROLLBACK,receipt.candidate.affected_descendants,receipt.candidate.parent_subject_identity)
def validate_repeat_repair_receipt(existing,repeated):
    if existing.receipt_identity!=repeated.receipt_identity: raise SelectiveRepairError("CONFLICTING_REPEAT_COMMAND","repeat differs")
    return existing
@dataclass(frozen=True)
class RepairRejectionReceipt:
    error_code:str; command_id:str; payload_sha256:str; authority_identity:str|None; partial_state_count:int=0
    @property
    def rejection_identity(self): return canonical_sha256(self.__dict__)
def build_repair_rejection_receipt(*,error,command_id,payload_sha256,authority_identity): return RepairRejectionReceipt(error.code,command_id,payload_sha256,authority_identity)
