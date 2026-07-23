from _support import *
from conscious_activations_interview_expression.errors import ValidationError
import pytest

def test_inventory_only_consumes_approved_moments(tmp_path):
 app,pref,_=imported_app(tmp_path);a,p,ar,pr=build_transcript(app,pref);v,vr=build_visual(app,pref)
 phrase=p['object']['payload']['phrases'][-1];po=app.repository.store_object('packed_phrase',{'phrase_id':phrase['phrase_id'],'version':'1.0.0',**phrase},object_id=phrase['phrase_id'],idempotency_key='phrase',lifecycle_state='VALIDATED');phr=ref(po);span=make_source_span(source_ref=pref,start_ms=1500,end_ms=3500,speaker_id='guest')
 m=app.expression.propose_moment(source_package_ref=pref,phrase_refs=[phr],source_spans=[span],keyframe_refs=[],reaction_receipt_refs=[],candidate_reason='x',proposer_id='h',idempotency_key='m')
 with pytest.raises(ValidationError): app.inventory.compile(source_package_ref=pref,expression_moment_refs=[ref(m)],phrase_pack_ref=pr,visual_index_ref=vr,reaction_receipt_refs=[],idempotency_key='inv')
 approved=app.expression.decide_moment(m['object']['object_id'],decision='APPROVE',operator_id='op',rationale='yes',idempotency_key='a')
 inv=app.inventory.compile(source_package_ref=pref,expression_moment_refs=[ref(approved)],phrase_pack_ref=pr,visual_index_ref=vr,reaction_receipt_refs=[],idempotency_key='inv2')
 assert inv['object']['payload']['semantic_programs_created'] is False
 assert inv['object']['payload']['final_scripts_created'] is False
 assert inv['object']['payload']['quote_candidates']

def test_observed_pack_keeps_interview_and_air_ownership_separate(tmp_path):
 app,pref,_=imported_app(tmp_path)
 pack=app.inventory.observed_evidence_pack(source_package_ref=pref,expression_moment_refs=[],reaction_receipt_refs=[],tag_assertion_refs=[],idempotency_key='observed')
 payload=pack['object']['payload']
 assert payload['owner']=='INTERVIEW_EXPRESSION'
 assert payload['semantic_interpretation_owner']=='ACTIVATIVE_INTELLIGENCE_RUNTIME'
 assert payload['production_authorized'] is False
