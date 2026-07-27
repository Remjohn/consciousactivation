from __future__ import annotations
import argparse, csv, gc, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_01_03_TRACEABILITY'

def sha(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()

def run_suite(path:str)->dict:
 env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONWARNINGS']='error::ResourceWarning'
 p=subprocess.run([sys.executable,'-m','unittest','discover','-s',path,'-p','test_*.py'],cwd=ROOT,text=True,capture_output=True,env=env)
 return {'path':path,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'resource_warning':'ResourceWarning' in p.stderr}

def main()->int:
 parser=argparse.ArgumentParser(); parser.add_argument('--report',type=Path); args=parser.parse_args()
 data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text(encoding='utf-8'))
 failures=[]
 for spec in data['specs']:
  p=ROOT/spec['spec_path']
  if not p.is_file(): failures.append(f"missing spec {spec['spec_path']}")
  elif sha(p)!=spec['spec_sha256']: failures.append(f"spec hash drift {spec['spec_id']}")
  for field in ('implementation_paths','test_paths'):
   for raw in filter(None,spec[field].split(';')):
    rel=raw.split('::')[0]
    if not (ROOT/rel).exists(): failures.append(f"missing {field} path {rel}")
 for ac in data['acceptance_criteria']:
  if not any(s['spec_id']==ac['spec_id'] for s in data['specs']): failures.append(f"orphan AC {ac['spec_id']} {ac['ac_id']}")
 suites=[run_suite('tests/phase1'),run_suite('tests/phase2'),run_suite('tests/phase3'),run_suite('tests/traceability')]
 for s in suites:
  if s['returncode']!=0: failures.append(f"suite failed {s['path']}")
  if s['resource_warning']: failures.append(f"resource warning {s['path']}")
 result={'schema_version':'ca-phase01-03-traceability-validation/v1','result':'PASS' if not failures else 'FAIL','specs':len(data['specs']),'acceptance_criteria':len(data['acceptance_criteria']),'gaps':len(data['gaps']),'test_suites':suites,'failures':failures}
 if args.report:
  args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2,sort_keys=True))
 return 0 if not failures else 2
if __name__=='__main__': raise SystemExit(main())
