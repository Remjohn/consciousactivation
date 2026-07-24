from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument('--backup-dir',type=Path,required=True); p.add_argument('--restore-dir',type=Path,required=True); a=p.parse_args(); m=json.loads((a.backup_dir/'BACKUP_MANIFEST.json').read_text()); a.restore_dir.mkdir(parents=True,exist_ok=True)
 for e in m['files']:
  src=a.backup_dir/e['path'];
  if sha(src)!=e['sha256']: raise SystemExit(f"backup hash mismatch: {e['path']}")
  dst=a.restore_dir/e['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
 print(json.dumps({'result':'PASS','restored_files':m['file_count']},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
