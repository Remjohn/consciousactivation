from pathlib import Path
import hashlib, json, sys
root = Path(__file__).resolve().parents[2]
required = [
    root/'00_START_HERE.md',
    root/'CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md',
    root/'CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md',
    root/'01_ATOMIC_HARNESS_BUILDER/AGENTS.md',
    root/'02_VISUAL_ASSET_EDITOR/AGENTS.md',
    root/'03_DELEGATION_PROTOCOL/AGENTS.md',
]
missing=[str(p.relative_to(root)) for p in required if not p.exists()]
for repo in ['01_ATOMIC_HARNESS_BUILDER','02_VISUAL_ASSET_EDITOR','03_DELEGATION_PROTOCOL']:
    d=root/repo/'docs/constitutional-alignment'
    for name in ['ALIGNMENT_CHARTER.md','REQUIREMENT_DELTA.csv','ARTIFACT_IMPACT_MATRIX.csv','PATCH_BATCHES.yaml','VALIDATION_REPORT.md']:
        p=d/name
        if not p.exists(): missing.append(str(p.relative_to(root)))
files=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name != 'WORKSPACE_MANIFEST.json':
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        files.append({'path':str(p.relative_to(root)).replace('\\','/'),'sha256':h,'size_bytes':p.stat().st_size})
manifest={'workspace':'CONSCIOUS_ACTIVATIONS','validation':'PASS' if not missing else 'FAIL','missing':missing,'file_count':len(files),'files':files}
(root/'WORKSPACE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'validation':manifest['validation'],'file_count':len(files),'missing':missing},indent=2))
sys.exit(1 if missing else 0)
