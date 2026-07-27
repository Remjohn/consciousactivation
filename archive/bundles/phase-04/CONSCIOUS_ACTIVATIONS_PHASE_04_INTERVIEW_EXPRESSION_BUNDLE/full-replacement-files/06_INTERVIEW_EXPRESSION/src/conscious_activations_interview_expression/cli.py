from __future__ import annotations
import argparse, json, tempfile
from pathlib import Path
from ca_runtime.paths import default_database_path
from ca_runtime.cli import bootstrap_transition, product_status
from . import PRODUCT_ID
from .application import InterviewExpressionApplication
from .demo import run_demo
from .schema_export import export_schemas

def main(argv: list[str]|None=None) -> int:
    parser=argparse.ArgumentParser(prog="cmf-interview"); parser.add_argument("--database",type=Path,default=default_database_path(PRODUCT_ID)); sub=parser.add_subparsers(dest="command",required=True)
    for name in ["bootstrap","health","status","demo"]:
        p=sub.add_parser(name); p.add_argument("--json",action="store_true")
    p=sub.add_parser("export-schemas"); p.add_argument("output",type=Path); p.add_argument("--json",action="store_true")
    args=parser.parse_args(argv)
    if args.command=="bootstrap":
        app = InterviewExpressionApplication(args.database)
        app.initialize()
        command, command_payload, event, event_payload, receipt = bootstrap_transition(PRODUCT_ID, app.repository.foundation_database().product_version)
        result = app.repository.foundation_database().record_transition(
            command_envelope=command, command_payload=command_payload,
            event_envelope=event, event_payload=event_payload,
            receipt_envelope=receipt,
        )
    elif args.command=="health":
        result=InterviewExpressionApplication(args.database).repository.health()
    elif args.command=="status":
        result=product_status(PRODUCT_ID, InterviewExpressionApplication(args.database).repository.foundation_database().product_version)
        result.update({"lifecycle_state":"phase_04_interview_expression_core","claim_ceiling":"PHASE_04_INTERVIEW_EXPRESSION_DEVELOPMENT_EVIDENCE"})
    elif args.command=="demo": result=run_demo(args.database)
    else: result={"files":export_schemas(args.output),"output":str(args.output)}
    print(json.dumps(result,indent=2,sort_keys=True)); return 0
