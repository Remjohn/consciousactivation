from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for path in [ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'packages/ca_delegation_rc4/src',ROOT/'packages/ca_release/src',ROOT/'services/air/src',ROOT/'services/pipeline/src',ROOT/'services/interview/src',ROOT/'services/vae/src']:
    sys.path.insert(0,str(path))
from ca_release.pilot import run_phase9_pilot

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args();result=run_phase9_pilot(ROOT,args.output_dir);print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
