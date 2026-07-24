from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from ca_contracts import canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_int, require_ref, require_string, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository

LAYER_BY_CODE={'CANVAS_DIMENSION_MISMATCH':'RUNTIME','VIDEO_STREAM_MISSING':'RUNTIME','BBOX_COLLISION':'PIPELINE_COMPOSITION','TEXT_OVERFLOW':'PIPELINE_COMPOSITION','SOURCE_LINEAGE_MISMATCH':'INTERVIEW_EXPRESSION','SEMANTIC_ROLE_MISMATCH':'ACTIVATIVE_INTELLIGENCE_RUNTIME','ASSET_REALIZATION_FAILURE':'VISUAL_ASSET_EDITOR','EVALUATOR_CONFLICT':'INDEPENDENT_EVALUATION'}
ALLOWED_ACTIONS={'SHIFT_BBOX','REDUCE_FONT_SIZE','ADD_AUDIO_FADE','SHIFT_CUT_TO_WORD_BOUNDARY','RERENDER_RUNTIME','ESCALATE_OWNER'}

class BoundedRepairService:
    def __init__(self,repository:PipelineRepository): self.repository=repository
    def diagnose(self, failures:list[Mapping[str,Any]])->dict[str,Any]:
        diagnoses=[]
        for i,f in enumerate(failures):
            code=require_string(f.get('code'),f'failures[{i}].code');layer=LAYER_BY_CODE.get(code,'UNKNOWN_REQUIRES_TRIAGE')
            diagnoses.append({'failure_code':code,'responsible_layer':layer,'evidence_refs':[require_ref(r,'evidence_ref') for r in f.get('evidence_refs',[])],'repairable_by_pipeline':layer in {'RUNTIME','PIPELINE_COMPOSITION'}})
        return {'diagnoses':diagnoses,'ambiguous':any(x['responsible_layer']=='UNKNOWN_REQUIRES_TRIAGE' for x in diagnoses)}
    def plan(self, *, target_ref:Mapping[str,Any], diagnosis:Mapping[str,Any], action:str, parameters:Mapping[str,Any], preserved_refs:list[Mapping[str,Any]], attempt_number:int, maximum_attempts:int, idempotency_key:str)->dict[str,Any]:
        target=require_ref(target_ref,'target_ref');action=require_string(action,'action')
        if action not in ALLOWED_ACTIONS:raise PipelineValidationError('unsupported repair action')
        attempt=require_int(attempt_number,'attempt_number',minimum=1);maximum=require_int(maximum_attempts,'maximum_attempts',minimum=1)
        if attempt>maximum:raise PipelineValidationError('repair attempt limit exceeded')
        if diagnosis.get('responsible_layer') not in {'RUNTIME','PIPELINE_COMPOSITION'} and action!='ESCALATE_OWNER':raise PipelineValidationError('Pipeline cannot repair another owner layer')
        preserved=[require_ref(r,'preserved_ref') for r in preserved_refs];preserved.sort(key=lambda x:x['object_id'])
        if any(r['object_id']==target['object_id'] for r in preserved):raise PipelineValidationError('target cannot also be preserved')
        core={'target_ref':target,'diagnosis':dict(diagnosis),'action':action,'parameters':dict(parameters),'preserved_refs':preserved,'attempt_number':attempt,'maximum_attempts':maximum,'descendant_only':True,'upstream_semantic_mutation':False,'production_authorized':False}
        reject_noncanonical(core)
        plan={'repair_plan_id':semantic_identity('bounded-repair-plan',core),'repair_plan_version':'1.0.0',**core}
        return self.repository.store_object('bounded_repair_plan',plan,idempotency_key=idempotency_key,object_id=plan['repair_plan_id'],lifecycle_state='PLANNED')
