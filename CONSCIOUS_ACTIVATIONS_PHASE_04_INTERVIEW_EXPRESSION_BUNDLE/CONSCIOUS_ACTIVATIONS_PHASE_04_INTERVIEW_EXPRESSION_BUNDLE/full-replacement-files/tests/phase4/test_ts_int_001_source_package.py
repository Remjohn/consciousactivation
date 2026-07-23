from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError, StateError, ConflictError

def test_imported_admission_preserves_absent_planning(tmp_path):
 app,pref,admitted=imported_app(tmp_path)
 assert admitted['object']['payload']['planning_lineage']=={'state':'ABSENT_NOT_CREATED'}
 assert admitted['object']['payload']['derivative_eligible'] is False

def test_brief_led_hash_mismatch_fails(tmp_path):
 app=InterviewExpressionApplication(tmp_path/'db.sqlite3');app.initialize()
 m=make_media_asset(logical_uri='workspace://x/v.mp4',sha256='a'*64,bytes_count=1,media_type='video/mp4',technical={'duration_ms':1})
 with pytest.raises(ValidationError,match='INT_ARMED_PLAN_HASH_MISMATCH'):
  app.source_packages.admit({'workspace_id':'w','project_id':'p','admission_mode':'BRIEF_LED','source_kind':'INTERVIEW_EXPRESSION','media_assets':[m],'source_authority':{'operator_id':'o','authority_scope':'DEV','assertion_id':'a'},'planning_lineage':{'state':'PRESENT_VERIFIED','brief_ref':{'object_id':'b','version':'1','sha256':'b'*64},'planned_aip_ref':{'object_id':'p','version':'1','sha256':'c'*64},'iac_ref':{'object_id':'i','version':'1','sha256':'d'*64},'arm_receipt_ref':{'object_id':'r','version':'1','sha256':'e'*64},'planned_object_digests':{'brief':'f'*64,'planned_aip':'c'*64,'iac':'d'*64}}},idempotency_key='x')

def test_portable_uri_required(tmp_path):
 app=InterviewExpressionApplication(tmp_path/'db.sqlite3');app.initialize()
 with pytest.raises(ValidationError): make_media_asset(logical_uri='C:/private/video.mp4',sha256='a'*64,bytes_count=2,media_type='video/mp4',technical={})

def test_publish_requires_reaction_and_moment(tmp_path):
 app,pref,_=imported_app(tmp_path)
 with pytest.raises(StateError): app.source_packages.publish(pref['object_id'],archive_only=False,idempotency_key='pub')
 archived=app.source_packages.publish(pref['object_id'],archive_only=True,idempotency_key='archive')
 assert archived['object']['payload']['lifecycle_state']=='ARCHIVE_ACCEPTED'

def test_idempotency_and_conflict(tmp_path):
 app,pref,first=imported_app(tmp_path)
 app2,pref2,second=app,pref,app.source_packages.admit(first['object']['payload'] | {},idempotency_key='other') if False else (None,None,None)
 # exact retry uses original command fixture
 media=first['object']['payload']['media_assets'][0]
 cmd={'workspace_id':'ws','project_id':'prj','admission_mode':'IMPORTED','source_kind':'INTERVIEW_EXPRESSION','media_assets':[media],'source_authority':{'operator_id':'op','authority_scope':'DEVELOPMENT_TEST','assertion_id':'assert-1'},'planning_lineage':{'state':'ABSENT_NOT_CREATED'}}
 retry=app.source_packages.admit(cmd,idempotency_key='admit')
 assert retry['idempotent_replay'] is True
 cmd['project_id']='changed'
 with pytest.raises(ConflictError): app.source_packages.admit(cmd,idempotency_key='admit')

def test_valid_brief_led_admission_preserves_exact_plan_refs(tmp_path):
 app=InterviewExpressionApplication(tmp_path/'db.sqlite3');app.initialize()
 m=make_media_asset(logical_uri='workspace://brief/v.mp4',sha256='1'*64,bytes_count=5,media_type='video/mp4',technical={'duration_ms':1000})
 brief={'object_id':'brief','version':'1.0.0','sha256':'2'*64}
 planned={'object_id':'planned','version':'1.0.0','sha256':'3'*64}
 iac={'object_id':'iac','version':'1.0.0','sha256':'4'*64}
 arm={'object_id':'arm','version':'1.0.0','sha256':'5'*64}
 admitted=app.source_packages.admit({'workspace_id':'w','project_id':'p','admission_mode':'BRIEF_LED','source_kind':'INTERVIEW_EXPRESSION','media_assets':[m],'source_authority':{'operator_id':'o','authority_scope':'DEV','assertion_id':'a'},'planning_lineage':{'state':'PRESENT_VERIFIED','brief_ref':brief,'planned_aip_ref':planned,'iac_ref':iac,'arm_receipt_ref':arm,'planned_object_digests':{'brief':brief['sha256'],'planned_aip':planned['sha256'],'iac':iac['sha256']}}},idempotency_key='brief')
 assert admitted['object']['payload']['planning_lineage']['brief_ref']==brief
 assert admitted['object']['payload']['planning_lineage']['planned_aip_ref']==planned


def test_component_binding_versions_package_and_preserves_history(tmp_path):
 app,pref,admitted=imported_app(tmp_path)
 component={'object_id':'component','version':'1.0.0','sha256':'6'*64}
 bound=app.source_packages.bind_component(pref['object_id'],'transcript_alignment',component,idempotency_key='bind',expected_revision=admitted['object']['revision'])
 assert bound['object']['revision']==admitted['object']['revision']+1
 assert bound['object']['payload']['components']['transcript_alignment']['state']=='BOUND'
 historical=app.repository.get_object(pref['object_id'],revision=admitted['object']['revision'])
 assert historical['payload']['components']['transcript_alignment']['state']=='PENDING_REQUIRED_COMPONENT'


def test_required_interview_evidence_cannot_be_not_applicable(tmp_path):
 app,pref,_=imported_app(tmp_path)
 with pytest.raises(ValidationError):
  app.source_packages.mark_not_applicable(pref['object_id'],'reaction_receipts','none',idempotency_key='na')
