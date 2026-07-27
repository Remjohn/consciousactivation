from __future__ import annotations
import argparse,json,os,subprocess,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=[ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src',ROOT/'05_ATOMIC_HARNESS_PIPELINE/src',ROOT/'06_INTERVIEW_EXPRESSION/src']
def run(command,env):
 p=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True);return {'command':[str(x) for x in command],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':'PASS' if p.returncode==0 else 'FAIL'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);a=ap.parse_args()
 with tempfile.TemporaryDirectory(prefix='ca-phase6-') as td:
  t=Path(td);env=dict(os.environ);env['PYTHONPATH']=os.pathsep.join(str(x) for x in SRC);env['CA_DATA_ROOT']=str(t/'data');env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONWARNINGS']='error::ResourceWarning';env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';(t/'pytest').mkdir(parents=True,exist_ok=True);checks=[]
  checks.append(run([sys.executable,'-m','compileall','-q','04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src','05_ATOMIC_HARNESS_PIPELINE/src','06_INTERVIEW_EXPRESSION/src','packages/ca_contracts/src','packages/ca_runtime/src'],env))
  paths=['tests/phase6','tests/phase5','tests/phase4','06_INTERVIEW_EXPRESSION/tests','tests/phase3','tests/phase2','tests/phase1','tests/traceability']
  with ThreadPoolExecutor(max_workers=len(paths)) as pool:
   fut=[]
   for pth in paths:
    e=dict(env);e['PYTHONPATH']=os.pathsep.join([str(ROOT/pth),*(str(x) for x in SRC)]);e['CA_DATA_ROOT']=str(t/'tests'/pth.replace('/','_'));fut.append(pool.submit(run,[sys.executable,'-m','pytest',pth,'-q','--basetemp',str(t/'pytest'/pth.replace('/','_'))],e))
   checks.extend(f.result() for f in fut)
  checks.append(run([sys.executable,'-m','cmf_pipeline','--database',str(t/'pipeline.sqlite3'),'phase6-demo','--json'],env))
  schemas=t/'schemas';checks.append(run([sys.executable,'-m','cmf_pipeline','export-schemas',str(schemas),'--json'],env));count=len(list(schemas.glob('*.json')))
  result='PASS' if all(x['result']=='PASS' for x in checks) and count>=31 else 'FAIL';report={'schema_version':'ca-phase06-validation-report/v1','validated_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'phase':'PHASE_06_COMPOSITION_MEDIA_RUNTIME','result':result,'checks':checks,'metadata':{'schema_file_count':count,'external_model_calls':0,'real_ffmpeg_execution':1,'skia_binding':'optional_with_reference_fallback','remotion_runtime_calls':0,'hyperframes_runtime_calls':0},'spec_scope':['TS-VID-001','TS-VID-002','TS-VID-003','TS-VID-004','TS-VID-005','TS-VID-006','TS-STA-001','TS-SPV-001','TS-CAR-001','TS-ANI-001','TS-EVAL-001','TS-EVAL-002','TS-EVAL-003'],'claim_ceiling':'PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE','full_spec_completion_claimed':False,'production_authorized':False,'certified':False,'format02_activated':False,'vae_stage5_started':False}
  rendered=json.dumps(report,indent=2,sort_keys=True)+'\n';print(rendered,end='');
  if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(rendered,encoding='utf-8')
  return 0 if result=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
