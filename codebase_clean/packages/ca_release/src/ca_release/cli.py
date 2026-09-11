from __future__ import annotations
import argparse,json
from pathlib import Path
from .pilot import run_phase9_pilot


def main(argv=None)->int:
    parser=argparse.ArgumentParser(prog='ca-release');sub=parser.add_subparsers(dest='command',required=True)
    pilot=sub.add_parser('pilot');pilot.add_argument('--repo',required=True);pilot.add_argument('--output-dir',required=True);pilot.add_argument('--json',action='store_true')
    args=parser.parse_args(argv)
    if args.command=='pilot':
        result=run_phase9_pilot(Path(args.repo),Path(args.output_dir));print(json.dumps(result,indent=2,sort_keys=True) if args.json else '\n'.join(f'{k}: {v}' for k,v in result.items()));return 0
    return 2
