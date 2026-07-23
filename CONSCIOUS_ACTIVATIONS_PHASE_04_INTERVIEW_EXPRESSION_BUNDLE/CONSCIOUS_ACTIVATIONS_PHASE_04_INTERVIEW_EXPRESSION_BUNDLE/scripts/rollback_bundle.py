from __future__ import annotations
import argparse, json
from pathlib import Path
from apply_bundle import rollback_from_receipt

def main():
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,required=True); p.add_argument("--bundle-id",default="CA-PHASE04-INTERVIEW-EXPRESSION-2026-07-23"); p.add_argument("--force",action="store_true"); a=p.parse_args()
    repo=a.repo.resolve(); state=repo/".conscious-activations"/"bundle-state"/a.bundle_id; receipt_path=state/"apply_receipt.json"
    if not receipt_path.is_file(): raise SystemExit(f"apply receipt not found: {receipt_path}")
    receipt=json.loads(receipt_path.read_text()); rollback_from_receipt(repo,receipt,force=a.force); receipt["result"]="ROLLED_BACK"; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n"); print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
