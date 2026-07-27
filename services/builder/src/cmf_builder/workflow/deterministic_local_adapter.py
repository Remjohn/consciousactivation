"""Execution-free deterministic local workflow adapter for ST-09.01."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

from .actor_explicit_contracts import ActorExplicitWorkflowIR

_SHA=re.compile(r"^[0-9a-f]{64}$")


class LocalAdapterError(ValueError):
    def __init__(self,code:str,message:str,**context:object):super().__init__(message);self.code=code;self.context=dict(context)


def _canonical(value:Any)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def _hash(value:Any)->str:return hashlib.sha256(_canonical(value)).hexdigest()
def _text(value:object,name:str)->None:
    if not isinstance(value,str) or not value.strip():raise LocalAdapterError("MISSING_GOVERNED_FIELD",f"{name} required")
def _sha(value:object,name:str)->None:
    if not isinstance(value,str) or not _SHA.fullmatch(value):raise LocalAdapterError("INVALID_IMMUTABLE_IDENTITY",f"{name} must be SHA-256")


@dataclass(frozen=True)
class WorkflowProfile:
    profile_id:str;profile_version:str;profile_sha256:str;registry_version:str;request_classifications:tuple[str,...];target_profiles:tuple[str,...];risk_states:tuple[str,...];promotion_status:str="DEVELOPMENT_ONLY"
    def __post_init__(self):
        _text(self.profile_id,"profile_id");_text(self.profile_version,"profile_version");_sha(self.profile_sha256,"profile_sha256");_text(self.registry_version,"registry_version")
        if not self.request_classifications or not self.target_profiles or not self.risk_states:raise LocalAdapterError("INCOMPLETE_ROUTING_PROFILE","routing dimensions required")
        if self.promotion_status!="DEVELOPMENT_ONLY":raise LocalAdapterError("PRODUCTION_PROMOTION_PROHIBITED","profile is development-only")
    @property
    def profile_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"profile_id":self.profile_id,"profile_version":self.profile_version,"profile_sha256":self.profile_sha256,"registry_version":self.registry_version,"request_classifications":list(self.request_classifications),"target_profiles":list(self.target_profiles),"risk_states":list(self.risk_states),"promotion_status":"DEVELOPMENT_ONLY"}


@dataclass(frozen=True)
class RoutingRequest:
    request_id:str;request_classification:str;target_profile:str;risk_state:str;registry_version:str
    def as_dict(self)->dict[str,str]:return {"request_id":self.request_id,"request_classification":self.request_classification,"target_profile":self.target_profile,"risk_state":self.risk_state,"registry_version":self.registry_version}


@dataclass(frozen=True)
class LocalCompilationReceipt:
    workflow_identity:str;adapter_identity:str;command_id:str;canonical_workflow_sha256:str;execution_performed:bool=False
    @property
    def receipt_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,Any]:return {"workflow_identity":self.workflow_identity,"adapter_identity":self.adapter_identity,"command_id":self.command_id,"canonical_workflow_sha256":self.canonical_workflow_sha256,"execution_performed":False}


@dataclass(frozen=True)
class ProfileRegistrationReceipt:
    profile_identity:str;registry_version:str;adapter_identity:str;command_id:str
    @property
    def receipt_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,str]:return {"profile_identity":self.profile_identity,"registry_version":self.registry_version,"adapter_identity":self.adapter_identity,"command_id":self.command_id}


@dataclass(frozen=True)
class RoutingDecision:
    request_id:str;profile_id:str;profile_identity:str;registry_version:str;adapter_identity:str
    @property
    def decision_identity(self)->str:return _hash(self.as_dict())
    def as_dict(self)->dict[str,str]:return {"request_id":self.request_id,"profile_id":self.profile_id,"profile_identity":self.profile_identity,"registry_version":self.registry_version,"adapter_identity":self.adapter_identity}


class DeterministicLocalWorkflowAdapter:
    allowed_operations=("compile","validate","register_profile","select_profile","query_compiled_contract")
    external_engine=False;network_access=False;workflow_execution=False;agent_execution=False;external_product_execution=False
    temporal_conformance="EXTERNAL_VALIDATION_PENDING"

    def __init__(self,adapter_id:str,adapter_version:str):
        _text(adapter_id,"adapter_id");_text(adapter_version,"adapter_version")
        self.adapter_id=adapter_id;self.adapter_version=adapter_version
        self._compiled:dict[str,ActorExplicitWorkflowIR]={};self._profiles:dict[str,WorkflowProfile]={};self._commands:dict[str,str]={};self._command_results:dict[str,object]={}

    @property
    def adapter_identity(self)->str:return _hash({"adapter_id":self.adapter_id,"adapter_version":self.adapter_version,"allowed_operations":list(self.allowed_operations),"external_engine":False,"network_access":False,"execution":False})

    def _idempotent(self,command_id:str,payload:str,result_factory):
        _text(command_id,"command_id")
        if command_id in self._commands:
            if self._commands[command_id]!=payload:raise LocalAdapterError("CONFLICTING_COMMAND_PAYLOAD","command id already bound")
            return self._command_results[command_id]
        result=result_factory();self._commands[command_id]=payload;self._command_results[command_id]=result;return result

    def compile(self,workflow_ir:ActorExplicitWorkflowIR,command_id:str)->LocalCompilationReceipt:
        payload=workflow_ir.workflow_identity
        def build():
            workflow_ir.as_dict();self._compiled[workflow_ir.workflow_identity]=workflow_ir
            return LocalCompilationReceipt(workflow_ir.workflow_identity,self.adapter_identity,command_id,hashlib.sha256(_canonical(workflow_ir.as_dict())).hexdigest(),False)
        return self._idempotent(command_id,payload,build)

    def validate(self,workflow_ir:ActorExplicitWorkflowIR)->bool:workflow_ir.as_dict();return True

    def query_compiled_contract(self,workflow_identity:str)->ActorExplicitWorkflowIR:
        if workflow_identity not in self._compiled:raise LocalAdapterError("UNKNOWN_COMPILED_WORKFLOW","workflow not registered")
        return self._compiled[workflow_identity]

    def register_profile(self,profile:WorkflowProfile,command_id:str)->ProfileRegistrationReceipt:
        payload=profile.profile_identity
        def build():
            key=f"{profile.registry_version}:{profile.profile_id}"
            existing=self._profiles.get(key)
            if existing and existing.profile_identity!=profile.profile_identity:raise LocalAdapterError("IMMUTABLE_PROFILE_CONFLICT","profile version cannot mutate")
            self._profiles[key]=profile
            return ProfileRegistrationReceipt(profile.profile_identity,profile.registry_version,self.adapter_identity,command_id)
        return self._idempotent(command_id,payload,build)

    def select_profile(self,request:RoutingRequest)->RoutingDecision:
        matches=sorted((p for p in self._profiles.values() if p.registry_version==request.registry_version and request.request_classification in p.request_classifications and request.target_profile in p.target_profiles and request.risk_state in p.risk_states),key=lambda p:p.profile_id)
        if not matches:raise LocalAdapterError("NO_DETERMINISTIC_ROUTE","no exact profile match")
        if len(matches)>1:raise LocalAdapterError("NONDETERMINISTIC_ROUTING","multiple exact profiles",candidate_profile_ids=tuple(p.profile_id for p in matches))
        selected=matches[0];return RoutingDecision(request.request_id,selected.profile_id,selected.profile_identity,request.registry_version,self.adapter_identity)
