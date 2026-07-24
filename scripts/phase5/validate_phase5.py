from __future__ import annotations
import argparse,json,os,shutil,subprocess,sys,tempfile,warnings
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=[ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src',ROOT/'05_ATOMIC_HARNESS_PIPELINE/src',ROOT/'06_INTERVIEW_EXPRESSION/src']

def run(cmd,env,cwd=ROOT,timeout=180):
    import time
    started=time.monotonic()
    print('[phase5-validate] '+ ' '.join(str(x) for x in cmd), file=sys.stderr, flush=True)
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
    elapsed=round(time.monotonic()-started,3)
    print(f'[phase5-validate] result={p.returncode} elapsed={elapsed}s', file=sys.stderr, flush=True)
    return {'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'elapsed_seconds':elapsed,'result':'PASS' if p.returncode==0 else 'FAIL'}

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--report',type=Path);args=pa.parse_args()
    with tempfile.TemporaryDirectory(prefix='ca-phase5-') as td:
        temp=Path(td);env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(str(p) for p in PATHS);env['CA_DATA_ROOT']=str(temp/'data');env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONWARNINGS']='error::ResourceWarning'
        checks=[]
        checks.append(run([sys.executable,'-m','compileall','-q','04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src','06_INTERVIEW_EXPRESSION/src'],env))
        suites=['tests/phase1','tests/phase2','tests/phase3','tests/phase4','tests/phase5','06_INTERVIEW_EXPRESSION/tests']
        for suite in suites:
            suite_env=dict(env)
            suite_env['PYTHONPATH']=os.pathsep.join([env['PYTHONPATH'],str(ROOT/suite)])
            checks.append(run([sys.executable,'-m','pytest',suite,'-q'],suite_env,timeout=180))
        checks.append(run([sys.executable,'-m','cmf_activative_intelligence','bootstrap','--json'],env))
        checks.append(run([sys.executable,'-m','cmf_activative_intelligence','demo','--json'],env,timeout=120))
        checks.append(run([sys.executable,'-m','cmf_activative_intelligence','production-demo','--interview-database',str(temp/'ie.sqlite3'),'--json'],env,timeout=180))
        schema=temp/'schemas';checks.append(run([sys.executable,'-m','cmf_activative_intelligence','export-schemas',str(schema),'--json'],env))
        install=temp/'install';build=temp/'build'
        for source,target in [(ROOT/'packages/ca_contracts',build/'ca_contracts'),(ROOT/'packages/ca_runtime',build/'ca_runtime'),(ROOT/'06_INTERVIEW_EXPRESSION',build/'ie'),(ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME',build/'air')]:
            shutil.copytree(source,target,ignore=shutil.ignore_patterns('build','dist','*.egg-info','__pycache__','*.pyc','.pytest_cache'))
        checks.append(run([sys.executable,'-m','pip','install','--quiet','--no-deps','--no-build-isolation','--target',str(install),str(build/'ca_contracts'),str(build/'ca_runtime'),str(build/'ie'),str(build/'air')],env,timeout=180))
        clean=dict(env);clean['PYTHONPATH']=str(install);clean['CA_DATA_ROOT']=str(temp/'clean-data')
        checks.append(run([sys.executable,'-m','cmf_activative_intelligence','production-demo','--interview-database',str(temp/'clean-ie.sqlite3'),'--json'],clean,timeout=180))
        schema_count=len(list(schema.glob('*.schema.json'))) if schema.exists() else 0
        manifest_count=1 if (schema/'SCHEMA_MANIFEST.json').is_file() else 0
        result='PASS' if all(c['result']=='PASS' for c in checks) and schema_count==38 and manifest_count==1 else 'FAIL'
        report={'schema_version':'ca-phase05-validation-report/v1','validated_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'phase':'PHASE_05_SEMANTIC_PRODUCTION_COMPILER','result':result,'checks':checks,'metadata':{'schema_file_count':schema_count,'expected_schema_file_count':38,'schema_manifest_count':manifest_count},'spec_scope':['TS-AIR-003','TS-AIR-015','TS-AIR-016'],'claim_ceiling':'PHASE_05_SEMANTIC_PRODUCTION_COMPILER_DEVELOPMENT_EVIDENCE','external_model_calls':0,'composition_or_rendering_performed':False,'production_authorized':False,'certified':False,'format02_activated':False,'vae_stage5_started':False}
        rendered=json.dumps(report,indent=2,sort_keys=True)+'\n';print(rendered,end='')
        if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered,encoding='utf-8')
        return 0 if result=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
