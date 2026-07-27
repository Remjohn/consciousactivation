from _support import ref
import pytest
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineValidationError

def words():return [{'word_id':'w1','text':'A','start_ms':100,'end_ms':300,'speaker_id':'g','protected_tail_ms':0},{'word_id':'w2','text':'B','start_ms':300,'end_ms':600,'speaker_id':'g','protected_tail_ms':50},{'word_id':'w3','text':'C','start_ms':1000,'end_ms':1300,'speaker_id':'g','protected_tail_ms':0}]
def test_word_boundary_edl_and_program(tmp_path):
 app=PipelineApplication(tmp_path/'db.sqlite3');app.initialize()
 edl=app.edls.compile(source_registration_ref=ref('source','s'),expression_moment_ref=ref('moment','m'),words=words(),selections=[{'selection_id':'s1','start_word_id':'w1','end_word_id':'w2','function':'HOOK','cut_in_class':'WORD_BOUNDARY','cut_out_class':'AUDIO_EVENT_BOUNDARY','authorized_reorder':False}],allow_reorder=False,idempotency_key='edl')['object']['payload']
 assert edl['entries'][0]['source_end_ms']==650
 req={'derivative_job_ref':ref('job','j'),'source_registration_ref':ref('source','s'),'semantic_production_package_ref':ref('semantic','x'),'final_script_ref':ref('script','x'),'activation_transfer_contract_ref':ref('transfer','x'),'harness_binding_ref':ref('binding','x'),'canvas':{'width':360,'height':640,'fps_numerator':30,'fps_denominator':1,'duration_ms':edl['output_duration_ms']},'timebase':{'numerator':1,'denominator':1000},'tracks':[{'track_id':'v','track_type':'VIDEO','role':'PRIMARY_A_ROLL_SPINE','z_index':0,'elements':[{'element_id':'e','kind':'SOURCE_SEGMENT','output_start_ms':0,'output_end_ms':edl['output_duration_ms'],'semantic_role':'SOURCE','sequence_role':'HOOK','source_registration_ref':ref('source','s'),'source_start_ms':100,'source_end_ms':650,'artifact_ref':'NOT_APPLICABLE','generated_slot_state':'NOT_APPLICABLE','bbox_intent_ref':'NOT_APPLICABLE','text':'NOT_APPLICABLE'}]}],'evaluation_profile_ref':ref('eval','x'),'wrong_reading_locks':['keep_source']}
 program=app.video_programs.compile(req,idempotency_key='program')['object']['payload'];assert program['tracks'][0]['role']=='PRIMARY_A_ROLL_SPINE';assert app.video_programs.projection(program['program_id'])['read_only']
def test_reorder_denied(tmp_path):
 app=PipelineApplication(tmp_path/'db.sqlite3');app.initialize()
 with pytest.raises(PipelineValidationError):app.edls.compile(source_registration_ref=ref('source','s'),expression_moment_ref=ref('moment','m'),words=words(),selections=[{'selection_id':'s1','start_word_id':'w3','end_word_id':'w3','function':'A','cut_in_class':'WORD_BOUNDARY','cut_out_class':'WORD_BOUNDARY','authorized_reorder':False},{'selection_id':'s2','start_word_id':'w1','end_word_id':'w2','function':'B','cut_in_class':'WORD_BOUNDARY','cut_out_class':'WORD_BOUNDARY','authorized_reorder':False}],allow_reorder=False,idempotency_key='bad')
