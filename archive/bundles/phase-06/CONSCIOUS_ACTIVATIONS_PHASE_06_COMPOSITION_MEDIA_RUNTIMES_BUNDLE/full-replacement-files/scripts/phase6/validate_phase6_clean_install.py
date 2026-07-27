from __future__ import annotations
import argparse,json,os,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(cmd,env,cwd=ROOT):
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True);return {'command':[str(x) for x in cmd],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':'PASS' if p.returncode==0 else 'FAIL'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);a=ap.parse_args()
 with tempfile.TemporaryDirectory(prefix='ca-phase6-install-') as td:
  t=Path(td);install=t/'install';build=t/'build';sources=[(ROOT/'packages/ca_contracts',build/'contracts'),(ROOT/'packages/ca_runtime',build/'runtime'),(ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME',build/'air'),(ROOT/'05_ATOMIC_HARNESS_PIPELINE',build/'pipeline'),(ROOT/'06_INTERVIEW_EXPRESSION',build/'interview')]
  for s,d in sources:shutil.copytree(s,d,ignore=shutil.ignore_patterns('build','dist','*.egg-info','__pycache__','*.pyc','.pytest_cache'))
  env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONWARNINGS']='error::ResourceWarning';env['PIP_DISABLE_PIP_VERSION_CHECK']='1';checks=[run([sys.executable,'-m','pip','install','--quiet','--no-deps','--no-build-isolation','--target',str(install),*(str(d) for _,d in sources)],env)]
  clean=dict(env);clean['PYTHONPATH']=str(install);clean['CA_DATA_ROOT']=str(t/'data');checks.append(run([sys.executable,'-m','cmf_pipeline','--database',str(t/'db.sqlite3'),'phase6-demo','--json'],clean))
  result='PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL';report={'schema_version':'ca-phase06-clean-install-report/v1','validated_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'result':result,'checks':checks,'claim_ceiling':'PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE'};rendered=json.dumps(report,indent=2,sort_keys=True)+'\n';print(rendered,end='');
  if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(rendered,encoding='utf-8')
  return 0 if result=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
