from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from ca_contracts import canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref, require_string, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository

class EvaluationService:
    def __init__(self,repository:PipelineRepository): self.repository=repository
    def evaluate(self, *, artifact_ref:Mapping[str,Any], semantic_context_refs:list[Mapping[str,Any]], profile:Mapping[str,Any], deterministic_checks:list[Mapping[str,Any]], judgment_dimensions:list[Mapping[str,Any]], producer_actor_id:str, evaluator_actor_id:str, idempotency_key:str)->dict[str,Any]:
        artifact=require_ref(artifact_ref,'artifact_ref');producer=require_string(producer_actor_id,'producer_actor_id');evaluator=require_string(evaluator_actor_id,'evaluator_actor_id')
        if producer==evaluator: raise PipelineValidationError('EVAL_EVALUATOR_NOT_INDEPENDENT')
        required_profile={'profile_id','profile_version','profile_sha256','required_deterministic_checks','required_judgment_dimensions','hard_gates','certification_state'}
        if not isinstance(profile,Mapping) or set(profile)!=required_profile: raise PipelineValidationError('evaluation profile invalid')
        check_map={require_string(c['check_id'],'check_id'):dict(c) for c in deterministic_checks}
        dimension_map={require_string(d['dimension_id'],'dimension_id'):dict(d) for d in judgment_dimensions}
        missing_checks=sorted(set(profile['required_deterministic_checks'])-set(check_map));missing_dims=sorted(set(profile['required_judgment_dimensions'])-set(dimension_map))
        blockers=[]
        if missing_checks:blockers.append({'code':'MISSING_DETERMINISTIC_CHECKS','items':missing_checks})
        if missing_dims:blockers.append({'code':'MISSING_JUDGMENT_DIMENSIONS','items':missing_dims})
        hard_failures=[]
        for gate in profile['hard_gates']:
            if gate in check_map and check_map[gate].get('result')!='PASS': hard_failures.append(gate)
            elif gate in dimension_map and dimension_map[gate].get('result')!='PASS': hard_failures.append(gate)
            elif gate not in check_map and gate not in dimension_map: hard_failures.append(gate)
        if blockers: verdict='BLOCKED'
        elif hard_failures: verdict='FAIL'
        else: verdict='PASS'
        context=[require_ref(x,f'semantic_context_refs[{i}]') for i,x in enumerate(semantic_context_refs)]
        context.sort(key=lambda x:x['object_id'])
        core={'artifact_ref':artifact,'semantic_context_refs':context,'profile':dict(profile),'deterministic_checks':sorted(check_map.values(),key=lambda x:x['check_id']),'judgment_dimensions':sorted(dimension_map.values(),key=lambda x:x['dimension_id']),'producer_actor_id':producer,'evaluator_actor_id':evaluator,'blockers':blockers,'hard_failures':hard_failures,'verdict':verdict,'production_eligible':False,'evaluator_certified':profile['certification_state']=='CERTIFIED' and False}
        reject_noncanonical(core)
        receipt={'evaluation_receipt_id':semantic_identity('evaluation-receipt',core),'evaluation_receipt_version':'1.0.0',**core}
        result=self.repository.store_object('independent_evaluation_receipt',receipt,idempotency_key=idempotency_key,object_id=receipt['evaluation_receipt_id'],lifecycle_state=verdict)
        self.repository.add_edge(artifact['object_id'],receipt['evaluation_receipt_id'],'evaluated_artifact')
        return result
