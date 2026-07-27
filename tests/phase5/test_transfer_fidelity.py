from __future__ import annotations
import copy
import pytest
from ._support import demo
from cmf_activative_intelligence.domain import AirValidationError

@pytest.fixture(scope='module')
def ctx(tmp_path_factory):
    return demo(tmp_path_factory.mktemp('phase5-transfer'))

def test_transfer_contract_and_checkpoint_pass(ctx):
    app,result=ctx;contract=app.repository.get_object(result['activation_transfer_contract_ref']['object_id']);assert len(contract.payload['must_survive_properties'])==3;assert all(p['hard_gate'] for p in contract.payload['must_survive_properties'])
    checkpoint=app.repository.get_object(result['transfer_checkpoint_ref']['object_id']);assert checkpoint.payload['deterministic_pass'] is True
    evaluation=app.repository.get_object(result['transfer_evaluation_ref']['object_id']);assert evaluation.payload['verdict']=='PASS';assert app.repository.list_edges(contract.object_id)

def test_checkpoint_cannot_pass_with_failed_property(ctx):
    app,result=ctx;checkpoint=app.repository.get_object(result['transfer_checkpoint_ref']['object_id']);payload=copy.deepcopy(checkpoint.payload);payload['receipt_id']='test:failed-checkpoint';payload['property_results'][0]['result']='FAIL'
    with pytest.raises(AirValidationError):app.transfer.store_checkpoint(payload,idempotency_key='failed-checkpoint')

def test_voice_rewrite_lineage_requires_voice_dna(ctx):
    app,_=ctx;lineages=app.repository.list_current(object_type='source_transformation_lineage');rewrite=next(x for x in lineages if x.payload['transformation_class']=='VOICE_DNA_REWRITE');payload=copy.deepcopy(rewrite.payload);payload['lineage_id']='test:bad-rewrite-lineage';payload.pop('voice_dna_ref')
    with pytest.raises(AirValidationError):app.transfer.store_lineage(payload,idempotency_key='bad-rewrite')
