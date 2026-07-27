from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument('--source-dir',type=Path,required=True); p.add_argument('--backup-dir',type=Path,required=True); a=p.parse_args(); a.backup_dir.mkdir(parents=True,exist_ok=True); files=[]
 for src in sorted(a.source_dir.rglob('*')):
  if src.is_file():
   rel=src.relative_to(a.source_dir); dst=a.backup_dir/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); files.append({'path':rel.as_posix(),'bytes':src.stat().st_size,'sha256':sha(src)})
 manifest={'schema_version':'ca-local-backup/v1','file_count':len(files),'files':files,'production_authorized':False}; (a.backup_dir/'BACKUP_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n'); print(json.dumps(manifest,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
