from __future__ import annotations
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
for p in reversed([
    ROOT/'packages/ca_contracts/src', ROOT/'packages/ca_runtime/src',
    ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src', ROOT/'05_ATOMIC_HARNESS_PIPELINE/src',
    ROOT/'06_INTERVIEW_EXPRESSION/src']):
    s=str(p)
    if s not in sys.path: sys.path.insert(0,s)

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.production_demo import run_production_demo

AUTHORITY={
    'authority_id':'ca-program-control-v2.1-candidate',
    'authority_version':'2.1.0-candidate',
    'authority_sha256':'a'*64,
    'authority_state':'candidate_not_current',
}

def ref(object_id:str,sha:str|None=None,version:str='1.0.0'):
    return {'object_id':object_id,'version':version,'sha256':sha or 'b'*64}

def stored_ref(value):
    o=value['object'] if 'object' in value else value
    return {'object_id':o['object_id'],'version':o.get('semantic_version',o.get('version','1.0.0')),'sha256':o.get('canonical_sha256',o.get('sha256'))}

def demo(tmp_path):
    air=tmp_path/'air.sqlite3'; ie=tmp_path/'ie.sqlite3'
    result=run_production_demo(air,ie)
    return AirApplication(air),result
