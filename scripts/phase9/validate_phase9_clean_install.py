from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
PACKAGES=[ROOT/'packages/ca_contracts',ROOT/'packages/ca_runtime',ROOT/'packages/ca_delegation_rc4',ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME',ROOT/'05_ATOMIC_HARNESS_PIPELINE',ROOT/'06_INTERVIEW_EXPRESSION',ROOT/'02_VISUAL_ASSET_EDITOR',ROOT/'packages/ca_release']

def run(command:list[str],env:dict[str,str],timeout:int=2400)->dict[str,Any]:
    p=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True,timeout=timeout)
    return {'command':command,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':'PASS' if p.returncode==0 else 'FAIL'}

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path);args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='ca-p9-install-') as td:
        temp=Path(td);install=temp/'install';build=temp/'build';checks=[]
        env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONWARNINGS']='error::ResourceWarning';env['PIP_DISABLE_PIP_VERSION_CHECK']='1'
        copies=[]
        for source in PACKAGES:
            dest=build/source.name;shutil.copytree(source,dest,ignore=shutil.ignore_patterns('build','dist','*.egg-info','__pycache__','*.pyc','.pytest_cache','node_modules'));copies.append(dest)
        checks.append(run([sys.executable,'-m','pip','install','--quiet','--no-deps','--no-build-isolation','--target',str(install),*(str(p) for p in copies)],env))
        pilot=temp/'pilot';clean=dict(env);clean['PYTHONPATH']=str(install);clean['CA_DATA_ROOT']=str(temp/'data')
        checks.append(run([sys.executable,'-m','ca_release','pilot','--repo',str(ROOT),'--output-dir',str(pilot),'--json'],clean))
        files=[pilot/'PILOT_RECEIPT.json',pilot/'release/RELEASE_MANIFEST.json',pilot/'PHASE_09_REFERENCE_EVIDENCE.zip']
        ok=all(p.is_file() for p in files)
        checks.append({'command':['internal','clean-install-pilot'],'returncode':0 if ok else 1,'stdout':json.dumps({'files':[str(p) for p in files],'all_exist':ok}), 'stderr':'','result':'PASS' if ok else 'FAIL'})
        result='PASS' if all(c['result']=='PASS' for c in checks) else 'FAIL'
        report={'schema_version':'ca-phase09-clean-install-report/v1','validated_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'result':result,'checks':checks,'installed_package_count':len(PACKAGES),'claim_ceiling':'PHASE_09_FINAL_INTEGRATED_DEVELOPMENT_CANDIDATE','production_authorized':False,'certified':False}
        rendered=json.dumps(report,indent=2,sort_keys=True)+'\n';print(rendered,end='')
        if args.report: args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered,encoding='utf-8')
        return 0 if result=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
