from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def verify(bundle):
 manifest=json.loads((bundle/'PACKAGE_MANIFEST.json').read_text()); failures=[]
 for item in manifest['files']:
  p=bundle/item['path']
  if not p.is_file(): failures.append('missing '+item['path'])
  elif p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: failures.append('drift '+item['path'])
 return {'result':'PASS' if not failures else 'FAIL','files':len(manifest['files']),'failures':failures}
if __name__=='__main__':
 b=Path(__file__).resolve().parents[1]; r=verify(b); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['result']=='PASS' else 2)
