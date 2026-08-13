"""
Stage 2 CLI for Visual Syntax Composition Compiler.
Executes Stage 2 compilation for specified harnesses.
"""

import argparse
from pathlib import Path
import sys
import json

from .runner import Stage2Runner, Stage2Config


def main():
    parser = argparse.ArgumentParser(description="Stage 2 Visual Syntax Composition Compiler CLI")
    parser.add_argument("--harness-id", type=str, help="Harness ID to compile")
    parser.add_argument("--stage1-report", type=str, help="Path to Stage 1 report JSON")
    parser.add_argument("--stage1-reports-dir", type=str, default="stage1_output", help="Directory containing Stage 1 reports")
    parser.add_argument("--output-dir", type=str, default="stage2_output", help="Output directory for Stage 2 specs and reports")
    parser.add_argument("--all", action="store_true", help="Compile all harnesses found in stage1-reports-dir")

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    if args.all:
        reports_dir = Path(args.stage1_reports_dir)
        if not reports_dir.exists():
            print(f"Error: Stage 1 reports directory not found: {reports_dir}")
            sys.exit(1)

        report_files = list(reports_dir.glob("*_STAGE1_REPORT.json"))
        if not report_files:
            report_files = list(reports_dir.glob("reports/*_STAGE1_REPORT.json"))

        print(f"Found {len(report_files)} Stage 1 reports in {reports_dir}")

        passed = 0
        failed = 0

        for r_file in sorted(report_files):
            h_id = r_file.name.replace("_STAGE1_REPORT.json", "")
            config = Stage2Config(
                harness_id=h_id,
                stage1_report_path=r_file,
                output_dir=output_dir
            )
            runner = Stage2Runner(config)
            res = runner.run()
            if res.stage2_complete:
                passed += 1
                print(f"[PASS] {h_id} -> dedup: {res.deduplication_hash}")
            else:
                failed += 1
                print(f"[FAIL] {h_id} -> {res.findings}")

        print(f"\nSummary: Total={len(report_files)} | PASS={passed} | FAIL={failed}")
        if failed > 0:
            sys.exit(1)

    elif args.harness_id and args.stage1_report:
        config = Stage2Config(
            harness_id=args.harness_id,
            stage1_report_path=Path(args.stage1_report),
            output_dir=output_dir
        )
        runner = Stage2Runner(config)
        res = runner.run()
        print(json.dumps({
            "harness_id": res.harness_id,
            "status": res.status,
            "stage2_complete": res.stage2_complete,
            "deduplication_hash": res.deduplication_hash,
            "spec_path": str(res.spec_path) if res.spec_path else None,
            "findings": res.findings
        }, indent=2))

        if not res.stage2_complete:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
