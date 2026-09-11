from __future__ import annotations
import copy
import pytest
from ._support import compile_demand,delegation_root,ref
from ca_delegation_rc4 import ContractSet
from cmf_pipeline.delegation import VisualDelegationService
from cmf_pipeline.domain.errors import PipelineValidationError
from cmf_vae.application import VAEApplication
from cmf_vae.errors import VAEValidationError

def test_01_exact_rc4_release_and_examples():
    contracts=ContractSet(delegation_root()); result=contracts.verify_release(); assert result['version']=='1.1.0-rc.4'; assert result['file_count']==163; assert contracts.validate_examples()>=20

def test_02_pipeline_compiles_valid_provider_neutral_demand():
    package=compile_demand(); assert package['delegation_release']=='1.1.0-rc.4'; assert 'format02' not in str(package['demand']).lower(); assert package['demand']['source_provenance']['source_kind']=='interview_expression'

def test_03_interview_lineage_is_required():
    svc=VisualDelegationService(delegation_root())
    with pytest.raises(PipelineValidationError):
        svc.compile_demand(source_package_ref=ref('s','s'),reaction_receipt_refs=[],expression_moment_refs=[],semantic_program_ref=ref('sem','s'),final_script_ref=ref('f','f'),primitive_coalition_ref=ref('p','p'),archetype_coalition_ref=ref('a','a'),activation_transfer_contract_ref=ref('t','t'),content_harness_ref=ref('h','h'),category_profile_ref=ref('c','c'),format_profile_ref=ref('fmt','fmt'),width_px=10,height_px=10,wrong_reading_locks=['lock'])

def test_04_vae_rejects_format02_even_if_schema_valid(tmp_path):
    app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); d=compile_demand()['demand']; d=copy.deepcopy(d); d['notes']='format02';
    with pytest.raises(VAEValidationError): app.admission.admit(d,idempotency_key='bad')

def test_05_result_acknowledgement_owns_consumption_authority(tmp_path):
    package=compile_demand(64,64); app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); flow=app.run_reference_job(demand=package['demand'],producer_actor_id='producer',evaluator_actor_id='evaluator',worker_id='worker')
    service=VisualDelegationService(delegation_root()); ack=service.acknowledge(demand=flow['admission']['demand_ref'],result=flow['result'],decision='ACCEPTED',consumption_authorized=True,evidence_ref=flow['artifact']['resource_ref']); assert ack['consumption_authorized'] is True; assert 'consumption_authorized' not in flow['result']
