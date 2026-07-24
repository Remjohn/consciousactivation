from __future__ import annotations
import copy
import pytest
from ._support import demo
from cmf_activative_intelligence.domain import AirValidationError

@pytest.fixture(scope='module')
def ctx(tmp_path_factory):
    return demo(tmp_path_factory.mktemp('phase5-derivative'))

def test_final_script_requires_operator_approval_before_composition(ctx):
    app,result=ctx;history=app.repository.history(result['approved_final_script_ref']['object_id'])
    assert len(history)==2 and history[0].payload['operator_approved'] is False and history[0].payload['composition_eligible'] is False
    assert history[1].payload['operator_approved'] is True and history[1].payload['composition_eligible'] is True and history[1].epistemic_state=='operator_confirmed'

def test_format02_profile_is_rejected(ctx):
    app,result=ctx;program=app.repository.get_object(result['derivative_program_refs']['source_short']['object_id']);payload=copy.deepcopy(program.payload);payload['program_id']='test:format02-program';payload['profile_id']='format02_minimal_coach_theatre'
    with pytest.raises(AirValidationError):app.derivatives.store_program(payload,idempotency_key='format02-denied')

def test_animation_scene_package_is_reusable_and_does_not_activate_format02(ctx):
    app,result=ctx;package=app.repository.get_object(result['animation_scene_package_ref']['object_id']);assert package.payload['format02_activated'] is False
    roles=set(package.payload['scenes'][0]['reuse_roles']);assert {'SHORT_BROLL','CAROUSEL_SLIDE','SUPERVISUAL_ELEMENT','ANIMATION_SHORT'}<=roles
    intent=package.payload['scenes'][0]['visual_requirement_intents'][0];assert intent['authority_class']=='NONAUTHORITATIVE_REQUIREMENT_INTENT';assert 'provider' not in intent and 'model' not in intent

def test_semantic_package_preserves_all_governing_refs(ctx):
    app,result=ctx;package=app.repository.get_object(result['semantic_production_package_ref']['object_id'])
    assert package.payload['approved_final_script_ref']==result['approved_final_script_ref'];assert package.payload['animation_scene_package_ref']==result['animation_scene_package_ref'];assert package.payload['activation_transfer_contract_ref']==result['activation_transfer_contract_ref']
