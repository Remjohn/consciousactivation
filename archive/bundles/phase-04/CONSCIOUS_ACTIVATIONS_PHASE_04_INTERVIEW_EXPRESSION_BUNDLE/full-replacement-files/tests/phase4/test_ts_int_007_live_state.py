from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError, AuthorityError, StateError, ConflictError

def start(tmp_path):
 app,pref,_=imported_app(tmp_path)
 result=app.live.start(source_package_ref=pref,iac_ref={'object_id':'iac','version':'1','sha256':'a'*64},binding_ref={'object_id':'binding','version':'1','sha256':'b'*64},interviewer_id='interviewer',allowed_actions=['RESET','LAND','STOP','CANCEL','PAUSE','RESUME'],idempotency_key='start')
 return app,result['snapshot']['session_id'],result

def test_air_proposal_is_not_delivery(tmp_path):
 app,sid,start_result=start(tmp_path)
 snap=app.repository.latest_snapshot(sid)
 app.live.acknowledge_air_proposal(sid,proposal_ref={'object_id':'proposal','version':'1','sha256':'c'*64},snapshot_ref={'object_id':sid,'version':'1','sha256':snap['sha256']},observation_watermark=snap['sequence'],idempotency_key='ack')
 current=app.repository.latest_snapshot(sid)['snapshot'];assert current['delivered_call_refs']==[]

def test_spontaneous_call_and_human_reaction(tmp_path):
 app,sid,_=start(tmp_path)
 d=app.live.deliver_call(sid,origin='SPONTANEOUS_HUMAN',exact_expression='What changed for you?',actor_id='interviewer',proposal_ref='NOT_APPLICABLE',pressure_units=1,idempotency_key='call')
 assert d['snapshot']['delivered_call_refs']
 with pytest.raises(AuthorityError): app.live.record_interviewer_reaction(sid,reaction_text='I felt curious',actor_id='interviewer',human_attested=False,evidence_refs=[],idempotency_key='rx')
 r=app.live.record_interviewer_reaction(sid,reaction_text='I felt curious',actor_id='interviewer',human_attested=True,evidence_refs=[],idempotency_key='rx2')
 assert r['snapshot']['reaction_refs']

def test_pause_reset_land_and_terminal_guards(tmp_path):
 app,sid,_=start(tmp_path)
 app.live.transition(sid,action='PAUSE',actor_id='i',evidence_refs=[],idempotency_key='p')
 with pytest.raises(StateError): app.live.deliver_call(sid,origin='SPONTANEOUS_HUMAN',exact_expression='x',actor_id='i',proposal_ref='NOT_APPLICABLE',pressure_units=0,idempotency_key='c')
 app.live.transition(sid,action='RESUME',actor_id='i',evidence_refs=[],idempotency_key='resume')
 landed=app.live.transition(sid,action='LAND',actor_id='i',evidence_refs=[],idempotency_key='land')
 assert landed['snapshot']['landing_state']=='RECORDED_WITHOUT_OUTCOME_CLAIM'
 with pytest.raises(StateError): app.live.transition(sid,action='RESET',actor_id='i',evidence_refs=[],idempotency_key='late')

def test_replay_hash_chain(tmp_path):
 app,sid,_=start(tmp_path);app.live.transition(sid,action='STOP',actor_id='i',evidence_refs=[],idempotency_key='stop')
 replay=app.live.replay(sid);assert replay['hash_chain_valid'] is True and replay['event_count']==2

def test_start_is_idempotent_and_requires_terminal_routes(tmp_path):
 app,pref,_=imported_app(tmp_path)
 with pytest.raises(ValidationError):
  app.live.start(source_package_ref=pref,iac_ref={'object_id':'iac','version':'1','sha256':'a'*64},binding_ref={'object_id':'binding','version':'1','sha256':'b'*64},interviewer_id='interviewer',allowed_actions=['STOP'],idempotency_key='bad')
 first=app.live.start(source_package_ref=pref,iac_ref={'object_id':'iac','version':'1','sha256':'a'*64},binding_ref={'object_id':'binding','version':'1','sha256':'b'*64},interviewer_id='interviewer',allowed_actions=['RESET','LAND','STOP','CANCEL'],idempotency_key='start-idem')
 second=app.live.start(source_package_ref=pref,iac_ref={'object_id':'iac','version':'1','sha256':'a'*64},binding_ref={'object_id':'binding','version':'1','sha256':'b'*64},interviewer_id='interviewer',allowed_actions=['RESET','LAND','STOP','CANCEL'],idempotency_key='start-idem')
 assert second['idempotent_replay'] is True
 assert first['event_id']==second['event_id']
