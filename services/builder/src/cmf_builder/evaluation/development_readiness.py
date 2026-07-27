"""Evidence-backed, development-only readiness receipts for ST-08.06."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import hashlib, json, re
from typing import Any

STORY_ID="ST-08.06"
READINESS_DIMENSIONS=("evidence_saturation","atomicity","constitutional_authority","Harness_IR_consistency","phases","contexts","contracts","modules","skill_maturity","benchmark_results","repair_coverage","observability","budgets","target_specific_requirements")
_SHA=re.compile(r"^[0-9a-f]{64}$")
class DevelopmentReadinessError(ValueError):
    def __init__(self,code:str,message:str,**context:object): super().__init__(message);self.code=code;self.context=dict(context)
def canonical_json_bytes(v:Any)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def canonical_sha256(v:Any)->str:return hashlib.sha256(canonical_json_bytes(v)).hexdigest()
def _text(v,n):
    if not isinstance(v,str) or not v.strip():raise DevelopmentReadinessError("MISSING_GOVERNED_FIELD",f"{n} required")
def _sha(v,n):
    if not isinstance(v,str) or not _SHA.fullmatch(v):raise DevelopmentReadinessError("INVALID_IMMUTABLE_IDENTITY",f"{n} must be SHA-256")
def _strings(v,n):
    if not isinstance(v,tuple) or not v:raise DevelopmentReadinessError("MISSING_GOVERNED_FIELD",f"{n} required")
    for x in v:_text(x,n)

class MaturityState(str,Enum): DEVELOPMENT_VALIDATED="development_validated"
DevelopmentMaturity=MaturityState
class ReadinessDimensionStatus(str,Enum): PASS="pass";FAIL="fail";UNRESOLVED="unresolved";NOT_APPLICABLE="not_applicable"
DimensionStatus=ReadinessDimensionStatus
class HardGateStatus(str,Enum): PASS="pass";FAIL="fail"
class AuthorizationOutcome(str,Enum):
    AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION="AUTHORIZED_FOR_OD_AM_001_DEVELOPMENT_IMPLEMENTATION"
    AUTHORIZED_FOR_PROTOTYPE_ONLY="AUTHORIZED_FOR_PROTOTYPE_ONLY"
    NEEDS_RATIFICATION="NEEDS_RATIFICATION"
    BLOCKED_EVIDENCE="BLOCKED_EVIDENCE"
    BLOCKED_SKILL_MATURITY="BLOCKED_SKILL_MATURITY"
    BLOCKED_BENCHMARK="BLOCKED_BENCHMARK"
    BLOCKED_ARCHITECTURE="BLOCKED_ARCHITECTURE"
    BLOCKED_AUTHORITY="BLOCKED_AUTHORITY"
    BLOCKED_HARD_GATE="BLOCKED_HARD_GATE"

@dataclass(frozen=True)
class EvidenceReference:
    ref_id:str;version:str;sha256:str;evidence_class:str;subject_identity:str
    def __post_init__(self):_text(self.ref_id,"ref_id");_text(self.version,"version");_sha(self.sha256,"sha256");_text(self.evidence_class,"evidence_class");_sha(self.subject_identity,"subject_identity")
    @property
    def reference_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"ref_id":self.ref_id,"version":self.version,"sha256":self.sha256,"evidence_class":self.evidence_class,"subject_identity":self.subject_identity}
ReadinessDimensionEvidence=EvidenceReference
@dataclass(frozen=True)
class ReadinessDimensionAssessment:
    dimension:str;status:ReadinessDimensionStatus;evidence_refs:tuple[EvidenceReference,...];limitation:str;failure_context:str;not_applicable_basis:EvidenceReference|None
    def __post_init__(self):
        if self.dimension not in READINESS_DIMENSIONS:raise DevelopmentReadinessError("UNKNOWN_READINESS_DIMENSION","dimension unknown")
        if not self.evidence_refs:raise DevelopmentReadinessError("MISSING_DIMENSION_EVIDENCE","evidence required")
        if not self.limitation:raise DevelopmentReadinessError("MISSING_DIMENSION_LIMITATION","limitation required")
        if self.status is ReadinessDimensionStatus.NOT_APPLICABLE and (self.not_applicable_basis is None or self.not_applicable_basis.evidence_class!="authoritative_target_profile_basis"):raise DevelopmentReadinessError("MISSING_NOT_APPLICABLE_AUTHORITY_BASIS","authoritative N/A basis required")
    @property
    def assessment_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"dimension":self.dimension,"status":self.status.value,"evidence_refs":[x.as_dict() for x in self.evidence_refs],"limitation":self.limitation,"failure_context":self.failure_context,"not_applicable_basis":None if self.not_applicable_basis is None else self.not_applicable_basis.as_dict()}
@dataclass(frozen=True)
class HardGateAssessment:
    gate_id:str;status:HardGateStatus;evidence_refs:tuple[EvidenceReference,...];failure_context:str
    def __post_init__(self):
        if self.gate_id not in {"HG-009","HG-010"}:raise DevelopmentReadinessError("UNKNOWN_HARD_GATE","unknown hard gate")
        if not self.evidence_refs:raise DevelopmentReadinessError("MISSING_HARD_GATE_EVIDENCE","hard gate evidence required")
    def as_dict(self):return {"gate_id":self.gate_id,"status":self.status.value,"evidence_refs":[x.as_dict() for x in self.evidence_refs],"failure_context":self.failure_context}
@dataclass(frozen=True)
class ReadinessSubject:
    subject_id:str;subject_version:str;subject_sha256:str;target_category:str;target_profile:str
    def __post_init__(self):_text(self.subject_id,"subject_id");_text(self.subject_version,"subject_version");_sha(self.subject_sha256,"subject_sha256");_text(self.target_category,"target_category");_text(self.target_profile,"target_profile")
    @property
    def subject_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"subject_id":self.subject_id,"subject_version":self.subject_version,"subject_sha256":self.subject_sha256,"target_category":self.target_category,"target_profile":self.target_profile}
@dataclass(frozen=True)
class ReadinessAuthority:
    authority_id:str;authority_version:str;authority_sha256:str;applicable_scope:tuple[str,...];signatory_refs:tuple[str,...]
    def __post_init__(self):_text(self.authority_id,"authority_id");_text(self.authority_version,"authority_version");_sha(self.authority_sha256,"authority_sha256");_strings(self.applicable_scope,"applicable_scope");[_sha(x,"signatory_ref") for x in self.signatory_refs]
    @property
    def authority_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"applicable_scope":list(self.applicable_scope),"signatory_refs":list(self.signatory_refs)}

@dataclass(frozen=True)
class DevelopmentReadinessReceipt:
    subject:ReadinessSubject;maturity:MaturityState;outcome:AuthorizationOutcome;dimensions:tuple[ReadinessDimensionAssessment,...];hard_gates:tuple[HardGateAssessment,...];exact_evidence_refs:tuple[EvidenceReference,...];predecessor_receipts:tuple[str,...];authority:ReadinessAuthority;applicable_scope:tuple[str,...];excluded_scope:tuple[str,...];limitations:tuple[str,...];unresolved_gates:tuple[str,...];invalidation_conditions:tuple[str,...];implementation_completion:str;evidence_closure:str;runtime_authorization:str;deployment_authorization:str;external_provider_validation:str;human_reaction_validation:str;production_ready:bool;certified:bool
    _integrity_anchor:str=field(init=False,repr=False,compare=False)
    def __post_init__(self):
        if not isinstance(self.maturity,MaturityState):raise DevelopmentReadinessError("MATURITY_EXCEEDS_DEVELOPMENT_CEILING","OD maturity ceiling exceeded")
        names=tuple(x.dimension for x in self.dimensions);missing=tuple(x for x in READINESS_DIMENSIONS if x not in names)
        if set(names)!=set(READINESS_DIMENSIONS) or len(names)!=len(READINESS_DIMENSIONS):raise DevelopmentReadinessError("INCOMPLETE_READINESS_DIMENSION_COVERAGE","all dimensions required",missing_dimensions=missing)
        gates={x.gate_id:x for x in self.hard_gates}
        if set(gates)!={"HG-009","HG-010"}:raise DevelopmentReadinessError("INCOMPLETE_HARD_GATE_COVERAGE","hard gates required")
        required={"constitutional_authority":AuthorizationOutcome.BLOCKED_AUTHORITY,"skill_maturity":AuthorizationOutcome.BLOCKED_SKILL_MATURITY,"benchmark_results":AuthorizationOutcome.BLOCKED_BENCHMARK,"evidence_saturation":AuthorizationOutcome.BLOCKED_EVIDENCE}
        for d,o in required.items():
            item=next(x for x in self.dimensions if x.dimension==d)
            if item.status in {ReadinessDimensionStatus.FAIL,ReadinessDimensionStatus.UNRESOLVED} and self.outcome is not o:raise DevelopmentReadinessError("OUTCOME_CONTRADICTS_READINESS_EVIDENCE","outcome contradicts evidence",required_outcome=o.value,dimension=d)
        for gate,out in (("HG-009",AuthorizationOutcome.BLOCKED_HARD_GATE),("HG-010",AuthorizationOutcome.BLOCKED_ARCHITECTURE)):
            if gates[gate].status is HardGateStatus.FAIL and self.outcome is not out:raise DevelopmentReadinessError("OUTCOME_CONTRADICTS_HARD_GATE","hard gate forces block",gate_id=gate,required_outcome=out.value)
        if any(item.status is ReadinessDimensionStatus.PASS and any(ref.evidence_class=="document_or_schema_presence" for ref in item.evidence_refs) for item in self.dimensions):raise DevelopmentReadinessError("DOCUMENT_PRESENCE_IS_NOT_READINESS","document presence cannot prove readiness")
        if self.production_ready:raise DevelopmentReadinessError("PRODUCTION_AUTHORIZATION_PROHIBITED","production claim prohibited")
        if self.certified:raise DevelopmentReadinessError("CERTIFICATION_PROHIBITED","certification claim prohibited")
        if self.evidence_closure!="pending":raise DevelopmentReadinessError("EVIDENCE_CLOSURE_NOT_PROVEN","evidence closure remains open")
        if self.runtime_authorization!="not_authorized":raise DevelopmentReadinessError("RUNTIME_AUTHORIZATION_PROHIBITED","runtime authorization not granted")
        if self.deployment_authorization!="not_authorized":raise DevelopmentReadinessError("DEPLOYMENT_AUTHORIZATION_PROHIBITED","deployment authorization not granted")
        if self.external_provider_validation!="pending":raise DevelopmentReadinessError("PROVIDER_VALIDATION_WITHOUT_EXECUTION","provider evidence absent")
        if self.human_reaction_validation!="pending":raise DevelopmentReadinessError("HUMAN_REACTION_VALIDATION_WITHOUT_EVIDENCE","human evidence absent")
        if not self.authority.signatory_refs:raise DevelopmentReadinessError("MISSING_SIGNATORY_AUTHORITY","signatory authority required")
        if self.authority.applicable_scope!=("OD_AM_001_OFFLINE_DEVELOPMENT",) or self.applicable_scope!=("OD_AM_001_OFFLINE_DEVELOPMENT",):raise DevelopmentReadinessError("AUTHORITY_SCOPE_MISMATCH","authority must match bounded offline scope")
        for x in self.predecessor_receipts:_sha(x,"predecessor_receipt")
        _strings(self.applicable_scope,"applicable_scope");_strings(self.excluded_scope,"excluded_scope");_strings(self.limitations,"limitations");_strings(self.unresolved_gates,"unresolved_gates");_strings(self.invalidation_conditions,"invalidation_conditions")
        object.__setattr__(self,"_integrity_anchor",canonical_sha256(self._payload()))
    @property
    def receipt_identity(self):return canonical_sha256(self._payload())
    def _payload(self):return {"subject":{**self.subject.as_dict(),"subject_identity":self.subject.subject_identity},"maturity":self.maturity.value,"outcome":self.outcome.value,"dimensions":[x.as_dict() for x in sorted(self.dimensions,key=lambda x:READINESS_DIMENSIONS.index(x.dimension))],"hard_gates":[x.as_dict() for x in sorted(self.hard_gates,key=lambda x:x.gate_id)],"exact_evidence_refs":[x.as_dict() for x in self.exact_evidence_refs],"predecessor_receipts":list(self.predecessor_receipts),"authority":{**self.authority.as_dict(),"authority_identity":self.authority.authority_identity},"applicable_scope":list(self.applicable_scope),"excluded_scope":list(self.excluded_scope),"limitations":list(self.limitations),"unresolved_gates":list(self.unresolved_gates),"invalidation_conditions":list(self.invalidation_conditions),"implementation_completion":self.implementation_completion,"evidence_closure":self.evidence_closure,"runtime_authorization":self.runtime_authorization,"deployment_authorization":self.deployment_authorization,"external_provider_validation":self.external_provider_validation,"human_reaction_validation":self.human_reaction_validation,"production_ready":False,"certified":False}
    def as_dict(self):
        p=self._payload();identity=canonical_sha256(p)
        if identity!=self._integrity_anchor:raise DevelopmentReadinessError("MUTATED_GOVERNED_OBJECT","governed receipt bytes changed after construction")
        p["receipt_identity"]=identity;return p

AUTHORIZATION_AXES=("implementation","evidence","runtime","deployment","production","certification","provider_validation","human_reaction_validation")
class AuthorizationAxisStatus(str,Enum): IMPLEMENTED_DEVELOPMENT_PASS="IMPLEMENTED_DEVELOPMENT_PASS";PENDING="pending";NOT_AUTHORIZED="not_authorized";FALSE="false"
@dataclass(frozen=True)
class AuthorizationAxis:
    axis_id:str;status:AuthorizationAxisStatus;evidence_refs:tuple[str,...];limitation:str
    def __post_init__(self):
        if self.axis_id not in AUTHORIZATION_AXES:raise DevelopmentReadinessError("UNKNOWN_AUTHORIZATION_AXIS","axis unknown")
        for x in self.evidence_refs:_sha(x,"axis_evidence")
        _text(self.limitation,"axis_limitation")
    def as_dict(self):return {"axis_id":self.axis_id,"status":self.status.value,"evidence_refs":list(self.evidence_refs),"limitation":self.limitation}
@dataclass(frozen=True)
class PrototypeAuthorizationTerms:
    empirical_question:str;allowed_implementation_scope:tuple[str,...];permitted_artifacts:tuple[str,...];provisional_decisions:tuple[str,...];required_evidence_return:tuple[str,...];disposal_or_migration_policy:str;budget_and_stop_conditions:tuple[str,...];promotion_conditions:tuple[str,...];expiry_or_completion_condition:str;prohibited_claims:tuple[str,...]
    def as_dict(self):return {"empirical_question":self.empirical_question,"allowed_implementation_scope":list(self.allowed_implementation_scope),"permitted_artifacts":list(self.permitted_artifacts),"provisional_decisions":list(self.provisional_decisions),"required_evidence_return":list(self.required_evidence_return),"disposal_or_migration_policy":self.disposal_or_migration_policy,"budget_and_stop_conditions":list(self.budget_and_stop_conditions),"promotion_conditions":list(self.promotion_conditions),"expiry_or_completion_condition":self.expiry_or_completion_condition,"prohibited_claims":list(self.prohibited_claims)}
@dataclass(frozen=True)
class AuthorizationAuthority:
    authority_id:str;authority_version:str;authority_sha256:str;authorized_subject_identity:str;permitted_outcomes:tuple[AuthorizationOutcome,...];allowed_scope:tuple[str,...];invalidation_conditions:tuple[str,...]
    @property
    def authority_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"authorized_subject_identity":self.authorized_subject_identity,"permitted_outcomes":[x.value for x in self.permitted_outcomes],"allowed_scope":list(self.allowed_scope),"invalidation_conditions":list(self.invalidation_conditions)}
@dataclass(frozen=True)
class AuthorizationCommand:
    command_id:str;subject_identity:str;outcome:AuthorizationOutcome;payload_sha256:str;expected_authority_identity:str
@dataclass(frozen=True)
class DevelopmentAuthorizationReceipt:
    subject_identity:str;outcome:AuthorizationOutcome;maturity_state:str;authorization_axes:tuple[AuthorizationAxis,...];allowed_scope:tuple[str,...];prohibited_scope:tuple[str,...];limitations:tuple[str,...];expiry_or_completion_conditions:tuple[str,...];predecessor_receipts:tuple[str,...];prototype_terms:PrototypeAuthorizationTerms;authority_identity:str;command_identity:str;evidence_gate_closed:bool=False;production_ready:bool=False;certified:bool=False
    @property
    def receipt_identity(self):return canonical_sha256(self._payload())
    def _payload(self):return {"subject_identity":self.subject_identity,"outcome":self.outcome.value,"maturity_state":self.maturity_state,"authorization_axes":[x.as_dict() for x in sorted(self.authorization_axes,key=lambda x:AUTHORIZATION_AXES.index(x.axis_id))],"allowed_scope":list(self.allowed_scope),"prohibited_scope":list(self.prohibited_scope),"limitations":list(self.limitations),"expiry_or_completion_conditions":list(self.expiry_or_completion_conditions),"predecessor_receipts":list(self.predecessor_receipts),"prototype_terms":self.prototype_terms.as_dict(),"authority_identity":self.authority_identity,"command_identity":self.command_identity,"evidence_gate_closed":False,"production_ready":False,"certified":False}
    def as_dict(self):p=self._payload();p["receipt_identity"]=canonical_sha256(p);return p
def _auth_payload(**v):return {"subject_identity":v["subject_identity"],"outcome":v["outcome"].value,"maturity_state":v["maturity_state"],"authorization_axes":[x.as_dict() for x in sorted(v["authorization_axes"],key=lambda x:x.axis_id)],"allowed_scope":list(v["allowed_scope"]),"prohibited_scope":list(v["prohibited_scope"]),"limitations":list(v["limitations"]),"expiry_or_completion_conditions":list(v["expiry_or_completion_conditions"]),"predecessor_receipts":list(v["predecessor_receipts"]),"prototype_terms":v["prototype_terms"].as_dict()}
def compute_authorization_payload_sha256(**v):return canonical_sha256(_auth_payload(**v))
def issue_development_authorization_receipt(*,subject_identity,outcome,maturity_state,authorization_axes,allowed_scope,prohibited_scope,limitations,expiry_or_completion_conditions,predecessor_receipts,prototype_terms,command,authority):
    if maturity_state!="development_validated":raise DevelopmentReadinessError("MATURITY_EXCEEDS_OD_AM_001_MAXIMUM","maturity too high")
    ids=[x.axis_id for x in authorization_axes]
    if len(ids)!=len(set(ids)):raise DevelopmentReadinessError("DUPLICATE_AUTHORIZATION_AXIS","duplicate axis")
    missing=[x for x in AUTHORIZATION_AXES if x not in ids]
    if missing:raise DevelopmentReadinessError("MISSING_AUTHORIZATION_AXIS","all axes required",missing=missing)
    axes={x.axis_id:x for x in authorization_axes}
    forbidden=(("production","PRODUCTION_AUTHORIZATION_PROHIBITED"),("certification","CERTIFICATION_AUTHORIZATION_PROHIBITED"),("provider_validation","PROVIDER_VALIDATION_WITHOUT_EXECUTION"),("human_reaction_validation","HUMAN_REACTION_VALIDATION_WITHOUT_EVIDENCE"))
    for axis,code in forbidden:
        if axes[axis].status is AuthorizationAxisStatus.IMPLEMENTED_DEVELOPMENT_PASS:raise DevelopmentReadinessError(code,"unproven promotion")
    if subject_identity!=authority.authorized_subject_identity:raise DevelopmentReadinessError("AUTHORIZATION_SUBJECT_MISMATCH","subject mismatch")
    if outcome not in authority.permitted_outcomes:raise DevelopmentReadinessError("AUTHORIZATION_OUTCOME_NOT_PERMITTED","outcome not permitted")
    if not set(allowed_scope).issubset(authority.allowed_scope):raise DevelopmentReadinessError("AUTHORIZATION_SCOPE_EXCEEDS_AUTHORITY","scope too broad")
    payload=compute_authorization_payload_sha256(subject_identity=subject_identity,outcome=outcome,maturity_state=maturity_state,authorization_axes=authorization_axes,allowed_scope=allowed_scope,prohibited_scope=prohibited_scope,limitations=limitations,expiry_or_completion_conditions=expiry_or_completion_conditions,predecessor_receipts=predecessor_receipts,prototype_terms=prototype_terms)
    if command.payload_sha256!=payload:raise DevelopmentReadinessError("COMMAND_PAYLOAD_MISMATCH","payload mismatch")
    if command.expected_authority_identity!=authority.authority_identity:raise DevelopmentReadinessError("AUTHORITY_IDENTITY_MISMATCH","authority mismatch")
    command_identity=canonical_sha256({"command_id":command.command_id,"subject_identity":command.subject_identity,"outcome":command.outcome.value,"payload_sha256":command.payload_sha256,"expected_authority_identity":command.expected_authority_identity})
    return DevelopmentAuthorizationReceipt(subject_identity,outcome,maturity_state,tuple(authorization_axes),tuple(allowed_scope),tuple(prohibited_scope),tuple(limitations),tuple(expiry_or_completion_conditions),tuple(predecessor_receipts),prototype_terms,authority.authority_identity,command_identity)

class ReadinessAction(str,Enum):
    ISSUE="ISSUE"
    INVALIDATE="INVALIDATE"
    REVOKE="REVOKE"

class AuthorityStatus(str,Enum):
    ACTIVE="ACTIVE"
    SUPERSEDED="SUPERSEDED"
    INVALIDATED="INVALIDATED"

@dataclass(frozen=True)
class ReadinessLifecycleAuthority:
    authority_id:str;authority_version:str;authority_sha256:str;permitted_actions:tuple[ReadinessAction,...];status:AuthorityStatus=AuthorityStatus.ACTIVE
    def __post_init__(self):
        _text(self.authority_id,"authority_id");_text(self.authority_version,"authority_version");_sha(self.authority_sha256,"authority_sha256")
        if not self.permitted_actions:raise DevelopmentReadinessError("MISSING_GOVERNED_FIELD","permitted_actions required")
    @property
    def authority_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"authority_id":self.authority_id,"authority_version":self.authority_version,"authority_sha256":self.authority_sha256,"permitted_actions":[x.value for x in self.permitted_actions],"status":self.status.value}

@dataclass(frozen=True)
class ReadinessCommand:
    command_id:str;action:ReadinessAction;resource_id:str;payload_sha256:str;expected_authority_identity:str
    def __post_init__(self):
        _text(self.command_id,"command_id");_sha(self.resource_id,"resource_id");_sha(self.payload_sha256,"payload_sha256");_sha(self.expected_authority_identity,"expected_authority_identity")
    @property
    def command_identity(self):return canonical_sha256(self.as_dict())
    def as_dict(self):return {"command_id":self.command_id,"action":self.action.value,"resource_id":self.resource_id,"payload_sha256":self.payload_sha256,"expected_authority_identity":self.expected_authority_identity}

@dataclass(frozen=True)
class ReadinessRejectionReceipt:
    error_code:str;command_id:str;payload_sha256:str;authority_identity:str;partial_state_count:int=0
    @property
    def rejection_identity(self):return canonical_sha256(self._payload())
    def _payload(self):return {"error_code":self.error_code,"command_id":self.command_id,"payload_sha256":self.payload_sha256,"authority_identity":self.authority_identity,"partial_state_count":0}
    def as_dict(self):
        value=self._payload();value["rejection_identity"]=canonical_sha256(value);return value

@dataclass(frozen=True)
class ReadinessTransitionReceipt:
    action:ReadinessAction;prior_receipt_identity:str;affected_scope:tuple[str,...];active_after:bool;historical_receipt_preserved:bool;reevaluation_requires_new_receipt:bool;command_identity:str;authority_identity:str
    @property
    def transition_identity(self):return canonical_sha256(self._payload())
    def _payload(self):return {"action":self.action.value,"prior_receipt_identity":self.prior_receipt_identity,"affected_scope":list(self.affected_scope),"active_after":self.active_after,"historical_receipt_preserved":self.historical_receipt_preserved,"reevaluation_requires_new_receipt":self.reevaluation_requires_new_receipt,"command_identity":self.command_identity,"authority_identity":self.authority_identity}
    def as_dict(self):
        value=self._payload();value["transition_identity"]=canonical_sha256(value);return value

def _require_lifecycle_authority(authority:ReadinessLifecycleAuthority,action:ReadinessAction)->None:
    if authority.status is not AuthorityStatus.ACTIVE:raise DevelopmentReadinessError("INACTIVE_AUTHORITY","authority is not active")
    if action not in authority.permitted_actions:raise DevelopmentReadinessError("UNAUTHORIZED_ACTION","authority does not permit action")

def _validate_readiness_command(command:ReadinessCommand,*,action:ReadinessAction,resource_id:str,payload_sha256:str,authority:ReadinessLifecycleAuthority)->None:
    _require_lifecycle_authority(authority,action)
    if command.action is not action:raise DevelopmentReadinessError("UNAUTHORIZED_ACTION","command action mismatch")
    if command.resource_id!=resource_id:raise DevelopmentReadinessError("COMMAND_RESOURCE_MISMATCH","command resource mismatch")
    if command.payload_sha256!=payload_sha256:raise DevelopmentReadinessError("COMMAND_PAYLOAD_MISMATCH","command payload mismatch")
    if command.expected_authority_identity!=authority.authority_identity:raise DevelopmentReadinessError("AUTHORITY_IDENTITY_MISMATCH","command authority mismatch")

def compute_readiness_issue_payload_sha256(receipt:DevelopmentReadinessReceipt)->str:
    return canonical_sha256(receipt.as_dict())

def issue_development_readiness_receipt(receipt:DevelopmentReadinessReceipt,command:ReadinessCommand,authority:ReadinessLifecycleAuthority)->DevelopmentReadinessReceipt:
    payload=compute_readiness_issue_payload_sha256(receipt)
    _validate_readiness_command(command,action=ReadinessAction.ISSUE,resource_id=receipt.receipt_identity,payload_sha256=payload,authority=authority)
    return receipt

def validate_repeat_readiness_receipt(existing:DevelopmentReadinessReceipt,repeated:DevelopmentReadinessReceipt)->DevelopmentReadinessReceipt:
    existing.as_dict();repeated.as_dict()
    if existing.receipt_identity!=repeated.receipt_identity:raise DevelopmentReadinessError("CONFLICTING_REPEAT_COMMAND","repeat payload differs")
    return existing

def compute_readiness_transition_payload_sha256(*,prior_receipt_identity:str,action:ReadinessAction,affected_scope:tuple[str,...])->str:
    return canonical_sha256({"prior_receipt_identity":prior_receipt_identity,"action":action.value,"affected_scope":list(affected_scope)})

def _transition_readiness_receipt(receipt:DevelopmentReadinessReceipt,command:ReadinessCommand,authority:ReadinessLifecycleAuthority,affected_scope:tuple[str,...],action:ReadinessAction)->ReadinessTransitionReceipt:
    receipt.as_dict();_strings(affected_scope,"affected_scope")
    payload=compute_readiness_transition_payload_sha256(prior_receipt_identity=receipt.receipt_identity,action=action,affected_scope=affected_scope)
    _validate_readiness_command(command,action=action,resource_id=receipt.receipt_identity,payload_sha256=payload,authority=authority)
    return ReadinessTransitionReceipt(action,receipt.receipt_identity,tuple(affected_scope),False,True,True,command.command_identity,authority.authority_identity)

def invalidate_readiness_receipt(receipt:DevelopmentReadinessReceipt,command:ReadinessCommand,authority:ReadinessLifecycleAuthority,affected_scope:tuple[str,...])->ReadinessTransitionReceipt:
    return _transition_readiness_receipt(receipt,command,authority,affected_scope,ReadinessAction.INVALIDATE)

def revoke_readiness_receipt(receipt:DevelopmentReadinessReceipt,command:ReadinessCommand,authority:ReadinessLifecycleAuthority,affected_scope:tuple[str,...])->ReadinessTransitionReceipt:
    return _transition_readiness_receipt(receipt,command,authority,affected_scope,ReadinessAction.REVOKE)

def build_readiness_rejection_receipt(*,error:DevelopmentReadinessError,command_id:str,payload_sha256:str,authority_identity:str)->ReadinessRejectionReceipt:
    return ReadinessRejectionReceipt(error.code,command_id,payload_sha256,authority_identity,0)
