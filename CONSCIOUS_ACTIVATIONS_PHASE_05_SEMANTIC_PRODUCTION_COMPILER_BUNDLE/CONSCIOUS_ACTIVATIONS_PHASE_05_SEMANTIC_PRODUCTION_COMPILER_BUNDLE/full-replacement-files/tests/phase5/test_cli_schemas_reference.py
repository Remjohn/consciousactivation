from __future__ import annotations
import json,os,subprocess,sys
import pytest
from ._support import ROOT,demo
from cmf_activative_intelligence.domain import schema_registry,supported_object_types

@pytest.fixture(scope='module')
def result(tmp_path_factory):
    return demo(tmp_path_factory.mktemp('phase5-reference'))[1]

def test_schema_registry_contains_phase5_types():
    types=set(supported_object_types());assert len(types)==38;assert {'activation_hypothesis','final_script_package','activation_transfer_contract','semantic_production_package'}<=types;assert set(schema_registry())==types

def test_production_demo_is_deterministic_and_bounded(result):
    assert result['demo_id']=='phase5-semantic-production-compiler-demo';assert result['external_model_calls']==0;assert result['composition_rendered'] is False;assert result['format02_activated'] is False;assert result['production_authorized'] is False

def test_cli_production_demo(tmp_path):
    env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(str(x) for x in [ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src',ROOT/'06_INTERVIEW_EXPRESSION/src'])
    completed=subprocess.run([sys.executable,'-m','cmf_activative_intelligence','--database',str(tmp_path/'air.sqlite3'),'production-demo','--interview-database',str(tmp_path/'ie.sqlite3'),'--json'],cwd=ROOT,env=env,text=True,capture_output=True,timeout=90)
    assert completed.returncode==0,completed.stderr;data=json.loads(completed.stdout);assert data['semantic_production_package_ref']['object_id']=='demo:semantic-production-package'
