from __future__ import annotations
import subprocess,tempfile
from pathlib import Path
from typing import Any
from ca_contracts import bytes_sha256, canonical_sha256
from .application import PipelineApplication
from .media import FFmpegSourceLedRenderer, RemotionBindingCompiler, HyperFramesBindingCompiler, RenderedVideoEvaluator
from .composition import SkiaStaticRenderer, SuperVisualService, CarouselService, AnimationSceneRealizer
from .evaluation import RenderReparseService


def ref(object_id:str,seed:str):return {'object_id':object_id,'version':'1.0.0','sha256':canonical_sha256({'seed':seed})}

def generate_source(path:Path):
    proc=subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','testsrc2=size=360x640:rate=30','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','4','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(path)],text=True,capture_output=True)
    if proc.returncode!=0:raise RuntimeError(proc.stderr)

def run_phase6_demo(database_path:str|Path|None=None,output_dir:str|Path|None=None)->dict[str,Any]:
    with tempfile.TemporaryDirectory(prefix='ca-phase6-demo-') as temp:
        root=Path(temp);out=Path(output_dir) if output_dir else root/'artifacts';out.mkdir(parents=True,exist_ok=True);source=root/'interview.mp4';generate_source(source)
        app=PipelineApplication(database_path or root/'pipeline.sqlite3');app.initialize()
        source_reg=app.source_media.register(source_path=source,logical_uri='media/interview.mp4',source_package_ref=ref('ie:source-package','source'),transcript_alignment_ref=ref('ie:transcript','transcript'),visual_index_ref=ref('ie:visual-index','visual'),restrictions=['operator_source_authority'],idempotency_key='phase6-source')['object']['payload']
        words=[{'word_id':'w1','text':'YOU','start_ms':200,'end_ms':500,'speaker_id':'guest','protected_tail_ms':0},{'word_id':'w2','text':'CAN','start_ms':500,'end_ms':800,'speaker_id':'guest','protected_tail_ms':0},{'word_id':'w3','text':'CHANGE','start_ms':1000,'end_ms':1400,'speaker_id':'guest','protected_tail_ms':100},{'word_id':'w4','text':'TODAY','start_ms':2000,'end_ms':2500,'speaker_id':'guest','protected_tail_ms':100}]
        edl=app.edls.compile(source_registration_ref=ref(source_reg['registration_id'],'registration'),expression_moment_ref=ref('ie:moment','moment'),words=words,selections=[{'selection_id':'sel-1','start_word_id':'w1','end_word_id':'w2','function':'HOOK','cut_in_class':'WORD_BOUNDARY','cut_out_class':'WORD_BOUNDARY','authorized_reorder':False},{'selection_id':'sel-2','start_word_id':'w3','end_word_id':'w4','function':'CLAIM','cut_in_class':'WORD_BOUNDARY','cut_out_class':'AUDIO_EVENT_BOUNDARY','authorized_reorder':False}],allow_reorder=False,idempotency_key='phase6-edl')['object']['payload']
        duration=edl['output_duration_ms']
        request={'derivative_job_ref':ref('job:short','job'),'source_registration_ref':ref(source_reg['registration_id'],'registration'),'semantic_production_package_ref':ref('air:semantic-package','semantic'),'final_script_ref':ref('air:final-script','script'),'activation_transfer_contract_ref':ref('air:transfer','transfer'),'harness_binding_ref':ref('binding:format07','binding'),'canvas':{'width':360,'height':640,'fps_numerator':30,'fps_denominator':1,'duration_ms':duration},'timebase':{'numerator':1,'denominator':1000},'tracks':[{'track_id':'track:a-roll','track_type':'VIDEO','role':'PRIMARY_A_ROLL_SPINE','z_index':0,'elements':[{'element_id':f"a-roll:{i}",'kind':'SOURCE_SEGMENT','output_start_ms':e['output_start_ms'],'output_end_ms':e['output_end_ms'],'semantic_role':'SOURCE_EXPRESSION','sequence_role':e['function'],'source_registration_ref':ref(source_reg['registration_id'],'registration'),'source_start_ms':e['source_start_ms'],'source_end_ms':e['source_end_ms'],'artifact_ref':'NOT_APPLICABLE','generated_slot_state':'NOT_APPLICABLE','bbox_intent_ref':'NOT_APPLICABLE','text':'NOT_APPLICABLE'} for i,e in enumerate(edl['entries'])]}],'evaluation_profile_ref':ref('eval:video','eval'),'wrong_reading_locks':['do_not_replace_source_expression']}
        program=app.video_programs.compile(request,idempotency_key='phase6-program')['object']['payload']
        renderer=FFmpegSourceLedRenderer();video=renderer.render(source_path=source,edl=edl,output_dir=out,logical_output_uri='video/source-led-short.mp4')
        artifact_ref={'object_id':video['manifest']['artifact_id'],'version':'1.0.0','sha256':video['manifest']['sha256']}
        video_eval=RenderedVideoEvaluator().evaluate(artifact_path=video['output_path'],artifact_ref=artifact_ref,program=program,edl=edl,producer_actor_id='ffmpeg-runtime',evaluator_actor_id='independent-render-evaluator',evidence_dir=out/'cut-evidence')
        refs={'semantic_program_ref':ref('air:derivative','derivative'),'final_script_ref':ref('air:final-script','script'),'primitive_coalition_ref':ref('air:primitive-coalition','primitive'),'archetype_coalition_ref':ref('air:archetype','archetype'),'activation_transfer_contract_ref':ref('air:transfer','transfer')}
        base_page={'page_id':'page-1','sequence_role':'CLAIM','viewer_state_goal':'RECOGNITION','negative_space_regions':[{'x':500000,'y':50000,'width':450000,'height':250000}],'elements':[{'element_id':'title','element_type':'TEXT','semantic_role':'IDENTITY_ANCHOR','syntax_role':'PRIMARY_CLAIM','bbox':{'x':50000,'y':100000,'width':850000,'height':300000},'why':'Establish the approved source-backed claim with dominant hierarchy.','z_index':1,'text':'YOU CAN CHANGE TODAY','font_size_px':42,'foreground_rgb':[255,255,255],'background_rgb':[20,40,80],'overlap_allowed':False,'source_refs':[ref('ie:moment','moment')],'protected_properties':['edge_integrity','source_fidelity']} ]}
        composition=app.compositions.compile({'composition_kind':'SUPERVISUAL',**refs,'canvas':{'width_px':600,'height_px':800,'background_rgb':[10,20,40]},'pages':[base_page],'wrong_reading_locks':['do_not_flatten_identity'],'profile_id':'supervisual_reference'},idempotency_key='phase6-supervisual')['object']['payload']
        sv=SuperVisualService().render(composition,out,'static/supervisual.png')
        carousel_pages=[]
        for i,text in enumerate(['YOU CAN CHANGE','THE TENSION IS REAL','TAKE THE FIRST STEP'],1):
            p={**base_page,'page_id':f'page-{i}','sequence_role':f'SEQUENCE_{i}','elements':[dict(base_page['elements'][0],element_id=f'title-{i}',text=text)]};carousel_pages.append(p)
        carousel_ir=app.compositions.compile({'composition_kind':'CAROUSEL',**refs,'canvas':{'width_px':600,'height_px':800,'background_rgb':[10,20,40]},'pages':carousel_pages,'wrong_reading_locks':['do_not_flatten_identity'],'profile_id':'carousel_reference'},idempotency_key='phase6-carousel')['object']['payload']
        carousel=CarouselService().render(carousel_ir,out,'static/carousel')
        anim_page={**base_page,'page_id':'scene-1','elements':[dict(base_page['elements'][0],element_id='subject',syntax_role='MOTION_SUBJECT',text='MOVE')]}
        anim_ir=app.compositions.compile({'composition_kind':'ANIMATION_SCENE',**refs,'canvas':{'width_px':360,'height_px':640,'background_rgb':[5,5,20]},'pages':[anim_page],'wrong_reading_locks':['generated_performance_is_not_real_reaction'],'profile_id':'animation_scene_reference'},idempotency_key='phase6-animation-ir')['object']['payload']
        scene_package={'animation_scene_package_id':'air:animation-scene-package','animation_scene_package_version':'1.0.0','scenes':[{'scene_id':'scene-1'}]}
        animation=AnimationSceneRealizer().realize(scene_package=scene_package,composition=anim_ir,output_dir=out/'animation',logical_uri='animation/scene.mp4',frame_count=12,fps=12)
        static_ref={'object_id':sv['manifest']['artifact_id'],'version':'1.0.0','sha256':sv['manifest']['sha256']}
        reparse=RenderReparseService().reparse_static(artifact_path=sv['output_path'],artifact_ref=static_ref,composition=composition)
        remotion=RemotionBindingCompiler().compile(program=program,composition_id='SourceLedShort',runtime_ref=ref('runtime:remotion','remotion'))
        hyper=HyperFramesBindingCompiler().compile(program=program,block_registry_ref=ref('registry:hyperframes','hyperframes'),block_ids=['claim-card'])
        return {'source_registration_id':source_reg['registration_id'],'edl_id':edl['edl_id'],'video_program_id':program['program_id'],'video_artifact':video['manifest'],'video_evaluation':video_eval,'supervisual_artifact':sv['manifest'],'carousel_artifact':carousel['manifest'],'animation_artifact':animation['manifest'],'static_reparse':reparse,'remotion_binding':remotion,'hyperframes_binding':hyper,'output_files':sorted(str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()),'claim_ceiling':'PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE'}
