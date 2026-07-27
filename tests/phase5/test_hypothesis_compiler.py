from __future__ import annotations
import copy
import pytest
from ._support import AUTHORITY,demo,ref
from cmf_activative_intelligence.domain import AirValidationError
from cmf_activative_intelligence.production_domain import EVALUATION_DIMENSIONS,HYPOTHESIS_GATES

@pytest.fixture(scope='module')
def ctx(tmp_path_factory):
    return demo(tmp_path_factory.mktemp('phase5-hypothesis'))

def test_reference_portfolio_is_diverse_gated_compared_and_promoted(ctx):
    app,result=ctx
    portfolio=app.repository.get_object(result['portfolio_ref']['object_id'])
    assert portfolio.payload['portfolio_state']=='PROMOTED'
    assert len(result['hypothesis_refs'])==3
    assert len(result['gate_receipt_refs'])==3
    comparison=app.repository.get_object(result['comparison_ref']['object_id'])
    assert comparison.payload['decision']=='DECISIVE_WINNER'
    assert comparison.payload['selected_hypothesis_ref']==result['selected_hypothesis_ref']
    assert app.repository.list_edges(result['portfolio_ref']['object_id'])

def test_duplicate_diversity_signatures_are_rejected(ctx):
    app,result=ctx
    current=app.repository.get_object(result['portfolio_ref']['object_id'])
    payload=copy.deepcopy(current.payload);payload.pop('supersedes_ref',None)
    payload['portfolio_id']='test:duplicate-portfolio';payload['portfolio_state']='OPEN'
    for k in ('stopping_receipt_ref','selected_hypothesis_ref','promotion_ref'):payload.pop(k,None)
    payload['gate_result_refs']=[];payload['comparative_evaluation_refs']=[]
    payload['candidate_refs']=[result['hypothesis_refs'][0],result['hypothesis_refs'][0]]
    payload['candidate_state_records']=[{'candidate_ref':result['hypothesis_refs'][0],'state':'PROPOSED','reason_codes':['TEST']},{'candidate_ref':result['hypothesis_refs'][0],'state':'PROPOSED','reason_codes':['TEST']}]
    with pytest.raises((ValueError,AirValidationError)):
        app.hypotheses.store_portfolio(payload,idempotency_key='duplicate-test')

def test_gate_requires_independent_evaluator(ctx):
    app,result=ctx
    with pytest.raises(AirValidationError):
        app.hypotheses.gate_hypothesis(receipt_id='test:bad-gate',version='1.0.0',authority=AUTHORITY,portfolio_ref=result['portfolio_ref'],hypothesis_ref=result['hypothesis_refs'][0],gate_profile_ref=ref('test:gate-profile'),evaluator_actor_id='same',producer_actor_id='same',outcomes={n:True for n in HYPOTHESIS_GATES},evidence_refs=[result['expression_moment_ref']],idempotency_key='bad-gate')

def test_comparison_requires_integer_micros(ctx):
    app,result=ctx
    scores={h['object_id']:{d:500_000 for d in EVALUATION_DIMENSIONS} for h in result['hypothesis_refs']};scores[result['hypothesis_refs'][0]['object_id']]['source_fidelity']=0.5
    with pytest.raises(ValueError):
        app.hypotheses.compare_portfolio(receipt_id='test:bad-comparison',version='1.0.0',authority=AUTHORITY,portfolio_ref=result['portfolio_ref'],evaluation_profile_ref=ref('test:eval'),evaluator_actor_id='eval',producer_actor_ids=['p1','p2','p3'],gate_receipt_refs=result['gate_receipt_refs'],candidate_scores=scores,decisive_margin_micros=1,idempotency_key='bad-comparison')
