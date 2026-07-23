from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from verify_bundle import sha,verify
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,required=True); ap.add_argument('--dry-run',action='store_true'); ap.add_argument('--skip-tests',action='store_true'); args=ap.parse_args()
 repo=args.repo.resolve(); bundle=Path(__file__).resolve().parents[1]
 if not (repo/'CMF_PROGRAM_CONTROL').is_dir(): raise SystemExit('not a Conscious Activations repo')
 if verify(bundle)['result']!='PASS': raise SystemExit('bundle invalid')
 base=json.loads((bundle/'BASELINE_LOCK.json').read_text()); ops=json.loads((bundle/'FILE_OPERATIONS.json').read_text())['operations']; failures=[]
 for item in base['required_existing_files']:
  p=repo/item['path'];
  if not p.is_file(): failures.append('missing '+item['path'])
  elif sha(p)!=item['sha256']: failures.append('baseline drift '+item['path'])
 for op in ops:
  p=repo/op['path']
  if op['operation']=='create' and p.exists() and sha(p)!=op['new_sha256']: failures.append('create collision '+op['path'])
  if op['operation']=='replace' and (not p.exists() or sha(p)!=op['old_sha256']): failures.append('replace drift '+op['path'])
 print(json.dumps({'result':'PASS' if not failures else 'FAIL','operations':len(ops),'failures':failures},indent=2))
 if failures:return 2
 if args.dry_run:return 0
 state=repo/'.conscious-activations/bundle-state/CA-PHASE01-03-TRACEABILITY-GAP-CLOSURE-2026-07-23'; backups=state/'backups'; backups.mkdir(parents=True,exist_ok=False)
 applied=[]
 try:
  for op in ops:
   src=bundle/'full-replacement-files'/op['path']; dst=repo/op['path']; dst.parent.mkdir(parents=True,exist_ok=True)
   backup=None
   if dst.exists(): backup=backups/op['path']; backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(dst,backup)
   shutil.copy2(src,dst); applied.append({'path':op['path'],'operation':op['operation'],'backup':str(backup) if backup else None,'new_sha256':op['new_sha256']})
  (state/'apply_receipt.json').write_text(json.dumps({'bundle_id':base['bundle_id'],'files':applied},indent=2)+'\n')
  if not args.skip_tests:
   p=subprocess.run([sys.executable,str(repo/'scripts/traceability/validate_phase1_3_traceability.py'),'--report',str(state/'validation_report.json')],cwd=repo)
   if p.returncode: raise RuntimeError('validation failed')
 except Exception:
  for rec in reversed(applied):
   dst=repo/rec['path']; backup=Path(rec['backup']) if rec['backup'] else None
   if backup and backup.exists(): shutil.copy2(backup,dst)
   elif dst.exists(): dst.unlink()
  raise
 return 0
if __name__=='__main__': raise SystemExit(main())
