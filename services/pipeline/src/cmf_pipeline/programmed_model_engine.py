from __future__ import annotations

from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

from .domain.errors import PipelineAuthorityError, PipelineNotFound, PipelineValidationError
from .domain.validation import reject_noncanonical, require_int, require_ref, require_string, require_string_list

_ARTIFACT_STATES={"PROPOSED","SHADOW","VALIDATED","DEPRECATED","RETIRED"}
_CLAIM_STATES={"PROPOSED","SHADOW","VALIDATED","REJECTED","SUPERSEDED"}


def _refs(value: Sequence[Mapping[str, Any]], field: str) -> list[dict[str,str]]:
    refs=[require_ref(item,f"{field}[{i}]") for i,item in enumerate(value)]; refs.sort(key=lambda x:x["object_id"]); return refs


class ProgrammedModelRegistry:
    def __init__(self, repository): self.repository=repository

    def register_artifact(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        required={"model_artifact_id","version","artifact_ref","model_family","architecture","parameter_count","quantization","runtime_ids","tokenizer_ref","training_dataset_refs","evaluation_dataset_refs","applicability_envelope","lifecycle_state","limitations","source_authority_refs"}
        missing=sorted(required-set(payload)); unknown=sorted(set(payload)-required)
        if missing or unknown: raise PipelineValidationError(f"model artifact fields invalid; missing={missing}, unknown={unknown}")
        state=require_string(payload["lifecycle_state"],"lifecycle_state")
        if state not in _ARTIFACT_STATES: raise PipelineValidationError("unknown model artifact state")
        normalized={
            "model_artifact_id":require_string(payload["model_artifact_id"],"model_artifact_id"),
            "version":require_string(payload["version"],"version"),
            "artifact_ref":require_ref(payload["artifact_ref"],"artifact_ref"),
            "model_family":require_string(payload["model_family"],"model_family"),
            "architecture":require_string(payload["architecture"],"architecture"),
            "parameter_count":require_int(payload["parameter_count"],"parameter_count",minimum=0),
            "quantization":require_string(payload["quantization"],"quantization"),
            "runtime_ids":sorted(require_string_list(list(payload["runtime_ids"]),"runtime_ids",sorted_unique=False)),
            "tokenizer_ref":require_ref(payload["tokenizer_ref"],"tokenizer_ref"),
            "training_dataset_refs":_refs(payload["training_dataset_refs"],"training_dataset_refs"),
            "evaluation_dataset_refs":_refs(payload["evaluation_dataset_refs"],"evaluation_dataset_refs"),
            "applicability_envelope":dict(payload["applicability_envelope"]),
            "lifecycle_state":state,
            "limitations":sorted(require_string_list(list(payload["limitations"]),"limitations",sorted_unique=False)),
            "source_authority_refs":_refs(payload["source_authority_refs"],"source_authority_refs"),
        }
        reject_noncanonical(normalized)
        return self.repository.store_object("programmed_model_artifact",normalized,object_id=normalized["model_artifact_id"],idempotency_key=idempotency_key,lifecycle_state=state)

    def register_claim(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        required={"claim_id","model_artifact_ref","claim_type","lifecycle_state","applicability_envelope","benchmark_ref","evaluator_ref","metric_name","threshold_micros","observed_micros","failure_limit_micros","fallback_mode","limitations","evidence_refs"}
        missing=sorted(required-set(payload)); unknown=sorted(set(payload)-required)
        if missing or unknown: raise PipelineValidationError(f"model claim fields invalid; missing={missing}, unknown={unknown}")
        state=require_string(payload["lifecycle_state"],"lifecycle_state")
        if state not in _CLAIM_STATES: raise PipelineValidationError("unknown model claim state")
        normalized={
            "claim_id":require_string(payload["claim_id"],"claim_id"),
            "model_artifact_ref":require_ref(payload["model_artifact_ref"],"model_artifact_ref"),
            "claim_type":require_string(payload["claim_type"],"claim_type"),
            "lifecycle_state":state,
            "applicability_envelope":dict(payload["applicability_envelope"]),
            "benchmark_ref":require_ref(payload["benchmark_ref"],"benchmark_ref"),
            "evaluator_ref":require_ref(payload["evaluator_ref"],"evaluator_ref"),
            "metric_name":require_string(payload["metric_name"],"metric_name"),
            "threshold_micros":require_int(payload["threshold_micros"],"threshold_micros",minimum=0),
            "observed_micros":require_int(payload["observed_micros"],"observed_micros",minimum=0),
            "failure_limit_micros":require_int(payload["failure_limit_micros"],"failure_limit_micros",minimum=0),
            "fallback_mode":require_string(payload["fallback_mode"],"fallback_mode"),
            "limitations":sorted(require_string_list(list(payload["limitations"]),"limitations",sorted_unique=False)),
            "evidence_refs":_refs(payload["evidence_refs"],"evidence_refs"),
        }
        reject_noncanonical(normalized)
        artifact=self.repository.get_object(normalized["model_artifact_ref"]["object_id"])
        if artifact["canonical_sha256"] != normalized["model_artifact_ref"]["sha256"]: raise PipelineValidationError("model artifact hash mismatch")
        return self.repository.store_object("programmed_model_claim",normalized,object_id=normalized["claim_id"],idempotency_key=idempotency_key,lifecycle_state=state)

    def register_program(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        required={"model_program_id","version","claim_ref","input_contract_id","output_contract_id","skill_refs","steering_recipe_refs","allowed_tool_ids","forbidden_action_ids","fallback_mode","escalation_conditions","runtime_requirements","lifecycle_state"}
        missing=sorted(required-set(payload)); unknown=sorted(set(payload)-required)
        if missing or unknown: raise PipelineValidationError(f"model program fields invalid; missing={missing}, unknown={unknown}")
        state=require_string(payload["lifecycle_state"],"lifecycle_state")
        if state=="PRODUCTION": raise PipelineAuthorityError("development runtime cannot authorize production Programmed Models")
        normalized={
            "model_program_id":require_string(payload["model_program_id"],"model_program_id"),
            "version":require_string(payload["version"],"version"),
            "claim_ref":require_ref(payload["claim_ref"],"claim_ref"),
            "input_contract_id":require_string(payload["input_contract_id"],"input_contract_id"),
            "output_contract_id":require_string(payload["output_contract_id"],"output_contract_id"),
            "skill_refs":_refs(payload["skill_refs"],"skill_refs"),
            "steering_recipe_refs":_refs(payload["steering_recipe_refs"],"steering_recipe_refs"),
            "allowed_tool_ids":sorted(require_string_list(list(payload["allowed_tool_ids"]),"allowed_tool_ids",sorted_unique=False)),
            "forbidden_action_ids":sorted(require_string_list(list(payload["forbidden_action_ids"]),"forbidden_action_ids",sorted_unique=False)),
            "fallback_mode":require_string(payload["fallback_mode"],"fallback_mode"),
            "escalation_conditions":sorted(require_string_list(list(payload["escalation_conditions"]),"escalation_conditions",sorted_unique=False)),
            "runtime_requirements":dict(payload["runtime_requirements"]),
            "lifecycle_state":state,
        }
        reject_noncanonical(normalized)
        claim=self.repository.get_object(normalized["claim_ref"]["object_id"])
        if claim["canonical_sha256"] != normalized["claim_ref"]["sha256"]: raise PipelineValidationError("claim hash mismatch")
        return self.repository.store_object("programmed_model_program",normalized,object_id=normalized["model_program_id"],idempotency_key=idempotency_key,lifecycle_state=state)

    @staticmethod
    def _matches(envelope:Mapping[str,Any],context:Mapping[str,Any])->bool:
        field_map={
            "category_ids":"category_id",
            "format_profile_ids":"format_profile_id",
            "role_ids":"role_id",
            "task_types":"task_type",
        }
        for field,context_field in field_map.items():
            required=set(envelope.get(field,[])); observed=context.get(context_field)
            if required and observed not in required: return False
        return True

    def resolve(self,context:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        required={"request_id","claim_type","category_id","format_profile_id","role_id","task_type","available_runtime_ids","maximum_parameter_count","required_tool_ids","allowed_lifecycle_states"}
        missing=sorted(required-set(context)); unknown=sorted(set(context)-required)
        if missing or unknown: raise PipelineValidationError(f"resolver context invalid; missing={missing}, unknown={unknown}")
        available=set(context["available_runtime_ids"]); required_tools=set(context["required_tool_ids"]); max_params=require_int(context["maximum_parameter_count"],"maximum_parameter_count",minimum=0)
        candidates=[]
        for program_obj in self.repository.list_objects(object_type="programmed_model_program"):
            program=program_obj["payload"]
            if program["lifecycle_state"] not in set(context["allowed_lifecycle_states"]): continue
            claim_obj=self.repository.get_object(program["claim_ref"]["object_id"]); claim=claim_obj["payload"]
            if claim["claim_type"] != context["claim_type"] or claim["lifecycle_state"] not in {"SHADOW","VALIDATED"}: continue
            if not self._matches(claim["applicability_envelope"],context): continue
            artifact_obj=self.repository.get_object(claim["model_artifact_ref"]["object_id"]); artifact=artifact_obj["payload"]
            if artifact["parameter_count"]>max_params: continue
            if not set(artifact["runtime_ids"]).intersection(available): continue
            if not required_tools.issubset(set(program["allowed_tool_ids"])): continue
            if claim["observed_micros"]<claim["threshold_micros"]: continue
            rank=(artifact["parameter_count"],-claim["observed_micros"],program["model_program_id"])
            candidates.append((rank,program_obj,claim_obj,artifact_obj))
        candidates.sort(key=lambda row:row[0])
        if candidates:
            _,program_obj,claim_obj,artifact_obj=candidates[0]
            result={"resolution_id":f"model-resolution:{canonical_sha256({'request':dict(context),'program':program_obj['object_id']})}","request_id":context["request_id"],"decision":"RESOLVED_SHADOW_OR_VALIDATED","model_program_ref":{"object_id":program_obj["object_id"],"version":program_obj["semantic_version"],"sha256":program_obj["canonical_sha256"]},"claim_ref":{"object_id":claim_obj["object_id"],"version":claim_obj["semantic_version"],"sha256":claim_obj["canonical_sha256"]},"model_artifact_ref":{"object_id":artifact_obj["object_id"],"version":artifact_obj["semantic_version"],"sha256":artifact_obj["canonical_sha256"]},"fallback_mode":program_obj["payload"]["fallback_mode"],"production_authorized":False}
        else:
            result={"resolution_id":f"model-resolution:{canonical_sha256({'request':dict(context),'fallback':'deterministic_or_human'})}","request_id":context["request_id"],"decision":"FALLBACK_REQUIRED","model_program_ref":"NOT_APPLICABLE","claim_ref":"NOT_APPLICABLE","model_artifact_ref":"NOT_APPLICABLE","fallback_mode":"DETERMINISTIC_OR_HUMAN","production_authorized":False}
        result["resolution_sha256"]=canonical_sha256(result)
        return self.repository.store_object("programmed_model_resolution",result,object_id=result["resolution_id"],idempotency_key=idempotency_key,lifecycle_state="ACTIVE")
