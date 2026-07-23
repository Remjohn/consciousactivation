from __future__ import annotations
import argparse,json,os,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=[ROOT/'tests/phase4',ROOT/'tests/phase3',ROOT/'tests/phase2',ROOT/'tests/phase1',ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src',ROOT/'05_ATOMIC_HARNESS_PIPELINE/src',ROOT/'06_INTERVIEW_EXPRESSION/src']
def run(cmd,env,cwd=ROOT):
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True);return {'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':'PASS' if p.returncode==0 else 'FAIL'}
def main():
 pa=argparse.ArgumentParser();pa.add_argument('--report',type=Path);args=pa.parse_args()
 with tempfile.TemporaryDirectory(prefix='ca-phase4-') as td:
  temp=Path(td);env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(str(p) for p in PATHS);env['CA_DATA_ROOT']=str(temp/'data');env['PYTHONDONTWRITEBYTECODE']='1'
  checks=[]
  checks.append(run([sys.executable,'-m','compileall','-q','06_INTERVIEW_EXPRESSION/src'],env))
  checks.append(run([sys.executable,'-m','pytest','tests/phase1','tests/phase2','tests/phase3','tests/phase4','06_INTERVIEW_EXPRESSION/tests','-q'],env))
  checks.append(run([sys.executable,'-m','conscious_activations_interview_expression','bootstrap','--json'],env))
  checks.append(run([sys.executable,'-m','conscious_activations_interview_expression','demo','--json'],env))
  schema=temp/'schemas';checks.append(run([sys.executable,'-m','conscious_activations_interview_expression','export-schemas',str(schema),'--json'],env))
  install=temp/'install';build=temp/'build';
  for source,target in [(ROOT/'packages/ca_contracts',build/'ca_contracts'),(ROOT/'packages/ca_runtime',build/'ca_runtime'),(ROOT/'06_INTERVIEW_EXPRESSION',build/'ie')]: shutil.copytree(source,target,ignore=shutil.ignore_patterns('build','dist','*.egg-info','__pycache__','*.pyc'))
  checks.append(run([sys.executable,'-m','pip','install','--quiet','--no-deps','--no-build-isolation','--target',str(install),str(build/'ca_contracts'),str(build/'ca_runtime'),str(build/'ie')],env))
  clean=dict(env);clean['PYTHONPATH']=str(install);clean['CA_DATA_ROOT']=str(temp/'clean-data');checks.append(run([sys.executable,'-m','conscious_activations_interview_expression','demo','--json'],clean))
  schema_count=len(list(schema.glob('*.json'))) if schema.exists() else 0
  result='PASS' if all(c['result']=='PASS' for c in checks) and schema_count==13 else 'FAIL'
  report={'schema_version':'ca-phase04-validation-report/v1','validated_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'phase':'PHASE_04_INTERVIEW_EXPRESSION_SOURCE_INGESTION','result':result,'checks':checks,'metadata':{'schema_file_count':schema_count,'expected_schema_file_count':13},'spec_scope':['TS-INT-001','TS-INT-002','TS-INT-003','TS-INT-004','TS-INT-005','TS-INT-006','TS-INT-007'],'claim_ceiling':'PHASE_04_INTERVIEW_EXPRESSION_DEVELOPMENT_EVIDENCE','external_model_calls':0,'production_authorized':False,'certified':False,'format02_activated':False,'vae_stage5_started':False}
  rendered=json.dumps(report,indent=2,sort_keys=True)+'\n';print(rendered,end='')
  if args.report: args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered,encoding='utf-8')
  return 0 if result=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
