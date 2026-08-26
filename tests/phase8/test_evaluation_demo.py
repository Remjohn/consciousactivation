from __future__ import annotations
import json
import pytest
from ._support import compile_demand,delegation_root,ref
from cmf_vae.application import VAEApplication
from cmf_vae.errors import VAEValidationError
from cmf_vae.phase8_demo import run_phase8_demo
from cmf_vae.schema_export import export_schemas

def test_21_reference_flow_produces_actual_png_and_result(tmp_path):
    package=compile_demand(96,96); app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); flow=app.run_reference_job(demand=package['demand'],producer_actor_id='producer',evaluator_actor_id='evaluator',worker_id='worker'); data,_=app.store.get(flow['artifact']['sha256']); assert data.startswith(b'\x89PNG'); assert flow['result']['completion_status']=='COMPLETE'; assert flow['evaluation']['production_eligible'] is False

def test_22_evaluator_independence_is_enforced(tmp_path):
    package=compile_demand(32,32); app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); adm=app.admission.admit(package['demand'],idempotency_key='a'); plan=app.plans.compile(package['demand'],adm['demand_ref'],idempotency_key='p')['payload']; art=app.providers.materialize(width=32,height=32,logical_uri='a.png',demand_id='d',wrong_reading_locks=['x'])['artifact']; geom=app.providers.segmentation(width=32,height=32,logical_uri='m.png',demand_id='d')['geometry']
    with pytest.raises(VAEValidationError): app.evaluator.evaluate(artifact_record=art,demand=package['demand'],geometry=geom,producer_actor_id='same',evaluator_actor_id='same')

def test_23_bounded_repair_never_changes_semantics(tmp_path):
    app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); plan=app.repairs.plan(target_ref=ref('asset','a'),failure_code='MASK_EDGE_ARTIFACT',evidence_refs=[ref('evidence','e')],attempt_number=1,maximum_attempts=2,preserved_properties=['identity','semantic_intent']); assert plan['semantic_mutation_allowed'] is False; assert plan['descendant_only'] is True

def test_24_demo_schemas_okf_and_control_tower(tmp_path):
    demo=run_phase8_demo(tmp_path/'demo',delegation_root()); assert demo['claim_ceiling']=='PHASE_08_DELEGATION_VAE_INTEGRATION_DEVELOPMENT_EVIDENCE'; assert (tmp_path/'demo/reference-visual-asset.png').is_file(); assert (tmp_path/'demo/visual-asset-result.md').is_file(); exported=export_schemas(tmp_path/'schemas'); assert exported['file_count']==17; assert (tmp_path/'schemas/visual_production_plan.schema.json').is_file()
