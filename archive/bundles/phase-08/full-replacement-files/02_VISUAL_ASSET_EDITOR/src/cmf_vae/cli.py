from __future__ import annotations
import argparse,json,os
from pathlib import Path
from .application import VAEApplication
from .phase8_demo import run_phase8_demo
from .schema_export import export_schemas

def default_delegation(repo: Path) -> Path: return repo/"03_DELEGATION_PROTOCOL"/"delegation-contracts"/"1.1.0-rc.4"
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,default=Path(os.environ.get("CA_REPO_ROOT",Path.cwd())))
    sub=p.add_subparsers(dest="command",required=True)
    h=sub.add_parser("health"); h.add_argument("--db",type=Path); h.add_argument("--storage",type=Path)
    d=sub.add_parser("demo"); d.add_argument("--output-dir",type=Path,required=True)
    s=sub.add_parser("export-schemas"); s.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args(); repo=a.repo.resolve(); delegation=default_delegation(repo)
    if a.command=="health":
        app=VAEApplication(a.db or repo/".conscious-activations/vae.sqlite3",a.storage or repo/".conscious-activations/vae-storage",delegation); app.initialize(); print(json.dumps(app.status(),indent=2,sort_keys=True)); return 0
    if a.command=="demo": print(json.dumps(run_phase8_demo(a.output_dir,delegation),indent=2,sort_keys=True)); return 0
    print(json.dumps(export_schemas(a.output_dir),indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
