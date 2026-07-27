from __future__ import annotations
import argparse,json,shutil
from pathlib import Path
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,required=True); args=ap.parse_args(); repo=args.repo.resolve(); state=repo/'.conscious-activations/bundle-state/CA-PHASE01-03-TRACEABILITY-GAP-CLOSURE-2026-07-23'; receipt=json.loads((state/'apply_receipt.json').read_text())
 for rec in reversed(receipt['files']):
  dst=repo/rec['path']; backup=Path(rec['backup']) if rec['backup'] else None
  if backup and backup.exists(): dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(backup,dst)
  elif dst.exists(): dst.unlink()
 shutil.rmtree(state)
 print('PASS')
if __name__=='__main__': main()
