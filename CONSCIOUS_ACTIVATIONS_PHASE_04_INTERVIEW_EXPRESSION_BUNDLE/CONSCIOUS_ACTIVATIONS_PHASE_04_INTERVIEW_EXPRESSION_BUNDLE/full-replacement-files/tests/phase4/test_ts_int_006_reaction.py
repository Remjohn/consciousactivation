from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError, EvidenceGapError

def test_exact_outcome_vocabulary_and_independent_evaluator(tmp_path):
 app,pref,_=imported_app(tmp_path);span=make_source_span(source_ref=pref,start_ms=100,end_ms=500,speaker_id='guest')
 o=app.reactions.record_observation(source_package_ref=pref,trigger_ref='NOT_APPLICABLE',source_spans=[span],modality_coverage={'audio':'PRESENT','video':'PRESENT','transcript':'PRESENT','operator_observation':'NOT_APPLICABLE'},observation_kind='STATE_CHANGE_OBSERVED',epistemic_state='OBSERVED',actor_id='producer',value={'x':'y'},idempotency_key='o')
 with pytest.raises(ValidationError,match='independent'):
  app.reactions.create_receipt(source_package_ref=pref,delivered_call_ref='NOT_APPLICABLE',pressure_decision_ref='NOT_APPLICABLE',observation_refs=[ref(o)],outcome='STATE_TRANSITION',counteractivation={'state':'NOT_OBSERVED'},uncertainty={'level':'LOW'},evaluator_id='producer',producer_id='producer',planned_observed_delta={'planning_state':'ABSENT_NOT_CREATED'},alternatives=[],idempotency_key='r')
 r=app.reactions.create_receipt(source_package_ref=pref,delivered_call_ref='NOT_APPLICABLE',pressure_decision_ref='NOT_APPLICABLE',observation_refs=[ref(o)],outcome='STATE_TRANSITION',counteractivation={'state':'NOT_OBSERVED'},uncertainty={'level':'LOW'},evaluator_id='eval',producer_id='producer',planned_observed_delta={'planning_state':'ABSENT_NOT_CREATED'},alternatives=['UNEXPECTED_EDGE'],idempotency_key='r2')
 assert r['object']['payload']['expression_moment_auto_approved'] is False

def test_capture_gap_is_not_activation_null(tmp_path):
 app,pref,_=imported_app(tmp_path);span=make_source_span(source_ref=pref,start_ms=100,end_ms=500,speaker_id='guest')
 with pytest.raises(EvidenceGapError): app.reactions.record_observation(source_package_ref=pref,trigger_ref='NOT_APPLICABLE',source_spans=[span],modality_coverage={'audio':'ABSENT_NOT_CAPTURED','video':'ABSENT_NOT_CAPTURED','transcript':'ABSENT_NOT_CAPTURED','operator_observation':'ABSENT_NOT_CAPTURED'},observation_kind='UNKNOWN',epistemic_state='OBSERVED',actor_id='p',value={},idempotency_key='o')

def test_silence_requires_silence_event(tmp_path):
 app,pref,_=imported_app(tmp_path);span=make_source_span(source_ref=pref,start_ms=100,end_ms=500,speaker_id='guest')
 o=app.reactions.record_observation(source_package_ref=pref,trigger_ref='NOT_APPLICABLE',source_spans=[span],modality_coverage={'audio':'PRESENT','video':'NOT_APPLICABLE','transcript':'PRESENT','operator_observation':'NOT_APPLICABLE'},observation_kind='FLAT_TEXT',epistemic_state='OBSERVED',actor_id='p',value={},idempotency_key='o')
 with pytest.raises(ValidationError,match='SILENCE'): app.reactions.create_receipt(source_package_ref=pref,delivered_call_ref='NOT_APPLICABLE',pressure_decision_ref='NOT_APPLICABLE',observation_refs=[ref(o)],outcome='SILENCE',counteractivation={'state':'UNKNOWN'},uncertainty={'level':'HIGH'},evaluator_id='e',producer_id='p',planned_observed_delta={},alternatives=[],idempotency_key='r')
