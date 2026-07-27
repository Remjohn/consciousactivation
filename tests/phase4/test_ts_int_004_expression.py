from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError, StateError

def setup_all(tmp_path):
 app,pref,_=imported_app(tmp_path);aligned,packed,ar,pr=build_transcript(app,pref);visual,vr=build_visual(app,pref)
 phrase=packed['object']['payload']['phrases'][-1]
 po=app.repository.store_object('packed_phrase',{'phrase_id':phrase['phrase_id'],'version':'1.0.0',**phrase},object_id=phrase['phrase_id'],idempotency_key='phrase',lifecycle_state='VALIDATED');phr=ref(po)
 span=make_source_span(source_ref=pref,start_ms=1500,end_ms=3500,speaker_id='guest')
 return app,pref,packed,vr,phr,span

def test_imported_cannot_fabricate_planned_tag(tmp_path):
 app,pref,_,_,_,span=setup_all(tmp_path)
 with pytest.raises(ValidationError): app.expression.create_tag(source_package_ref=pref,tag='planned-edge',epistemic_state='PLANNED',source_spans=[span],actor_id='x',evidence_refs=[],rationale='no',idempotency_key='tag')

def test_moment_requires_operator_approval(tmp_path):
 app,pref,packed,vr,phr,span=setup_all(tmp_path)
 m=app.expression.propose_moment(source_package_ref=pref,phrase_refs=[phr],source_spans=[span],keyframe_refs=[{'object_id':'k','version':'1','sha256':'c'*64}],reaction_receipt_refs=[],candidate_reason='candidate',proposer_id='hunter',idempotency_key='m')
 assert m['object']['payload']['lifecycle_state']=='CANDIDATE'
 approved=app.expression.decide_moment(m['object']['object_id'],decision='APPROVE',operator_id='op',rationale='source-backed',idempotency_key='approve')
 assert approved['object']['payload']['epistemic_state']=='OPERATOR_CONFIRMED'
 with pytest.raises(StateError): app.expression.decide_moment(m['object']['object_id'],decision='REJECT',operator_id='op',rationale='late',idempotency_key='reject')

def test_rejected_moment_is_preserved(tmp_path):
 app,pref,_,_,phr,span=setup_all(tmp_path)
 m=app.expression.propose_moment(source_package_ref=pref,phrase_refs=[phr],source_spans=[span],keyframe_refs=[],reaction_receipt_refs=[],candidate_reason='candidate',proposer_id='hunter',idempotency_key='m')
 rejected=app.expression.decide_moment(m['object']['object_id'],decision='REJECT',operator_id='op',rationale='wrong read',idempotency_key='r')
 assert rejected['object']['payload']['lifecycle_state']=='REJECTED'
 assert app.repository.get_object(m['object']['object_id'],revision=1)['payload']['lifecycle_state']=='CANDIDATE'

def test_observed_tag_and_anchor_hit_preserve_exact_source_evidence(tmp_path):
 app,pref,_,_,phr,span=setup_all(tmp_path)
 tag=app.expression.create_tag(source_package_ref=pref,tag='identity-shift',epistemic_state='OBSERVED',source_spans=[span],actor_id='analyst',evidence_refs=[phr],rationale='exact phrase',idempotency_key='tag-observed')
 hit=app.expression.create_anchor_hit(source_package_ref=pref,phrase_refs=[phr],source_spans=[span],anchor_kind='FELT_TRUTH',epistemic_state='OBSERVED',evidence_refs=[ref(tag)],actor_id='analyst',idempotency_key='hit')
 assert tag['object']['payload']['epistemic_state']=='OBSERVED'
 assert hit['object']['payload']['source_spans']==[span]
 assert hit['object']['payload']['phrase_refs']==[phr]
