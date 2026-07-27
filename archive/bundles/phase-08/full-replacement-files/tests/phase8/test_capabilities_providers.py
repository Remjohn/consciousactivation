from __future__ import annotations
import json,sys
from pathlib import Path
import pytest
from _support import compile_demand,delegation_root
from ca_contracts import canonical_sha256
from cmf_vae.application import VAEApplication
from cmf_vae.capabilities import WorkcellCompiler,default_registry
from cmf_vae.comfyui import ComfyUIGraphCompiler
from cmf_vae.errors import CapabilityGap,VAEValidationError
from cmf_vae.providers import ExternalCommandProvider,ReferenceProviders
from cmf_vae.storage import ContentAddressedStore

def plan(tmp_path):
    app=VAEApplication(tmp_path/'db.sqlite3',tmp_path/'store',delegation_root()); app.initialize(); d=compile_demand(64,64)['demand']; adm=app.admission.admit(d,idempotency_key='a'); return app, d, app.plans.compile(d,adm['demand_ref'],idempotency_key='p',include_geometry_reference=True)['payload']

def test_14_workcell_requires_independent_evaluator(tmp_path):
    app,d,p=plan(tmp_path)
    with pytest.raises(VAEValidationError): WorkcellCompiler(app.capabilities).compile(p,producer_actor_id='same',evaluator_actor_id='same')

def test_15_workcell_is_deterministic(tmp_path):
    app,d,p=plan(tmp_path); a=app.workcells.compile(p,producer_actor_id='p',evaluator_actor_id='e'); b=app.workcells.compile(p,producer_actor_id='p',evaluator_actor_id='e'); assert a==b; assert all(x['provider_id'] for x in a['stage_bindings'])

def test_16_comfyui_graph_is_locked_and_compiler_only(tmp_path):
    app,d,p=plan(tmp_path); w=app.workcells.compile(p,producer_actor_id='p',evaluator_actor_id='e'); store=ContentAddressedStore(tmp_path/'art'); x=store.put(b'x',logical_uri='x.bin',media_type='application/octet-stream'); bundle=ComfyUIGraphCompiler().compile(plan=p,workcell=w,input_refs=[x['resource_ref']]); ComfyUIGraphCompiler().validate(bundle); assert bundle['runtime_execution_authorized'] is False

def test_17_comfyui_mutable_policy_is_rejected(tmp_path):
    app,d,p=plan(tmp_path); w=app.workcells.compile(p,producer_actor_id='p',evaluator_actor_id='e'); store=ContentAddressedStore(tmp_path/'art'); x=store.put(b'x',logical_uri='x.bin',media_type='application/octet-stream'); bundle=ComfyUIGraphCompiler().compile(plan=p,workcell=w,input_refs=[x['resource_ref']]); bundle['graph']['execution_policy']['network_fetch_allowed']=True; bundle['graph_sha256']=canonical_sha256(bundle['graph'])
    with pytest.raises(VAEValidationError): ComfyUIGraphCompiler().validate(bundle)

def test_18_external_command_adapter_contract(tmp_path,fake_provider_script):
    request={'hello':'world'}; provider=ExternalCommandProvider(provider_id='FAKE_PROVIDER',command_template=[sys.executable,str(fake_provider_script),'{request}','{response}']); result=provider.execute(request,tmp_path/'out'); assert result['executed']; assert result['response']['request_sha256']==canonical_sha256(request)

def test_19_external_command_identity_mismatch_rejected(tmp_path):
    script=tmp_path/'bad.py'; script.write_text('import json,sys;open(sys.argv[2],"w").write(json.dumps({"provider_id":"WRONG","request_sha256":"x"}))')
    provider=ExternalCommandProvider(provider_id='EXPECTED',command_template=[sys.executable,str(script),'{request}','{response}'])
    with pytest.raises(CapabilityGap): provider.execute({'x':1},tmp_path/'out')

def test_20_gnm_is_geometry_only(tmp_path):
    providers=ReferenceProviders(ContentAddressedStore(tmp_path/'s')); good=providers.gnm_geometry(demand_id='d',purpose='GEOMETRY_REFERENCE',head_pose={'yaw':0},gaze={'x':0},logical_uri='g.json'); assert good['geometry']['identity_authority'] is False
    with pytest.raises(VAEValidationError): providers.gnm_geometry(demand_id='d',purpose='IDENTITY_TRUTH',head_pose={'yaw':0},gaze={'x':0},logical_uri='bad.json')
