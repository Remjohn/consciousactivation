from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from ca_contracts import canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_int, require_ref, require_string, require_string_list, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository
from .geometry import BBox, GeometryValidator
from .pretext import PretextEngine

class CompositionIRService:
    def __init__(self,repository:PipelineRepository): self.repository=repository;self.geometry=GeometryValidator();self.pretext=PretextEngine()
    def compile(self,request:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        required={'composition_kind','semantic_program_ref','final_script_ref','primitive_coalition_ref','archetype_coalition_ref','activation_transfer_contract_ref','canvas','pages','wrong_reading_locks','profile_id'}
        if not isinstance(request,Mapping) or set(request)!=required: raise PipelineValidationError('composition request invalid shape')
        refs={f:require_ref(request[f],f) for f in ('semantic_program_ref','final_script_ref','primitive_coalition_ref','archetype_coalition_ref','activation_transfer_contract_ref')}
        kind=require_string(request['composition_kind'],'composition_kind')
        if kind not in {'SUPERVISUAL','CAROUSEL','ANIMATION_SCENE'}: raise PipelineValidationError('unsupported composition kind')
        canvas=request['canvas']
        if not isinstance(canvas,Mapping) or set(canvas)!={'width_px','height_px','background_rgb'}: raise PipelineValidationError('canvas invalid')
        width=require_int(canvas['width_px'],'canvas.width_px',minimum=1);height=require_int(canvas['height_px'],'canvas.height_px',minimum=1)
        rgb=canvas['background_rgb']
        if not isinstance(rgb,list) or len(rgb)!=3 or any(not isinstance(x,int) or isinstance(x,bool) or x<0 or x>255 for x in rgb): raise PipelineValidationError('background_rgb invalid')
        pages=[]
        for pi,p in enumerate(request['pages']):
            if not isinstance(p,Mapping) or set(p)!={'page_id','sequence_role','viewer_state_goal','negative_space_regions','elements'}: raise PipelineValidationError(f'pages[{pi}] invalid')
            elements=[]
            for ei,e in enumerate(p['elements']):
                required_element={'element_id','element_type','semantic_role','syntax_role','bbox','why','z_index','text','font_size_px','foreground_rgb','background_rgb','overlap_allowed','source_refs','protected_properties'}
                if not isinstance(e,Mapping) or set(e)!=required_element: raise PipelineValidationError(f'pages[{pi}].elements[{ei}] invalid')
                box=BBox.from_mapping(e['bbox'])
                text=e['text'];font_size=require_int(e['font_size_px'],'font_size_px',minimum=1)
                measurement='NOT_APPLICABLE'
                if text!='NOT_APPLICABLE':
                    text=require_string(text,'text')
                    pxw=max(1,box.width*width//1_000_000);pxh=max(1,box.height*height//1_000_000)
                    measurement=self.pretext.fit(text,pxw,pxh,font_size).to_dict()
                    if not measurement['fits']: raise PipelineValidationError(f"text does not fit element {e['element_id']}")
                elements.append({
                    'element_id':require_string(e['element_id'],'element_id'),'element_type':require_string(e['element_type'],'element_type'),
                    'semantic_role':require_string(e['semantic_role'],'semantic_role'),'syntax_role':require_string(e['syntax_role'],'syntax_role'),
                    'bbox':box.to_dict(),'why':require_string(e['why'],'why'),'z_index':require_int(e['z_index'],'z_index'),
                    'text':text,'font_size_px':font_size,'text_measurement':measurement,
                    'foreground_rgb':e['foreground_rgb'],'background_rgb':e['background_rgb'],'overlap_allowed':bool(e['overlap_allowed']),
                    'source_refs':[require_ref(r,'source_ref') for r in e['source_refs']],
                    'protected_properties':require_string_list(e['protected_properties'],'protected_properties'),
                })
            elements.sort(key=lambda x:(x['z_index'],x['element_id']))
            geometry=self.geometry.validate_elements(elements)
            if geometry['result']!='PASS': raise PipelineValidationError(f'composition geometry invalid: {geometry["violations"]}')
            regions=[BBox.from_mapping(r,f'negative_space_regions[{i}]').to_dict() for i,r in enumerate(p['negative_space_regions'])]
            pages.append({'page_id':require_string(p['page_id'],'page_id'),'sequence_role':require_string(p['sequence_role'],'sequence_role'),'viewer_state_goal':require_string(p['viewer_state_goal'],'viewer_state_goal'),'negative_space_regions':regions,'elements':elements,'geometry_receipt':geometry})
        if not pages: raise PipelineValidationError('composition requires pages')
        if kind=='SUPERVISUAL' and len(pages)!=1: raise PipelineValidationError('SuperVisual requires exactly one page')
        locks=require_string_list(request['wrong_reading_locks'],'wrong_reading_locks',non_empty=True)
        core={'composition_kind':kind,**refs,'profile_id':require_string(request['profile_id'],'profile_id'),'canvas':{'width_px':width,'height_px':height,'background_rgb':rgb},'pages':pages,'wrong_reading_locks':locks,'semantic_meaning_owned_by_pipeline':False,'production_authorized':False}
        reject_noncanonical(core)
        ir={'composition_id':semantic_identity('composition-ir',core),'composition_version':'1.0.0',**core}
        result=self.repository.store_object('composition_ir',ir,idempotency_key=idempotency_key,object_id=ir['composition_id'],lifecycle_state='COMPILED')
        for ref in refs.values(): self.repository.add_edge(ref['object_id'],ir['composition_id'],'composition_semantic_input')
        return result
