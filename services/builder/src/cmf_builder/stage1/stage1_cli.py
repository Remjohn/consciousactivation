from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from cmf_builder.stage1.runner import Stage1Runner, RunConfig
from cmf_builder.stage1.input_receipt import compute_file_sha256

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="stage1-cli",
        description="Execute Stage 1 Visual Syntax Reconstruction for a single operator-selected harness.",
        allow_abbrev=False
    )
    parser.add_argument("--harness-id", required=True, help="ID of the harness selected by operator.")
    parser.add_argument("--source-zip", required=True, type=Path, help="Path to harness source zip.")
    parser.add_argument("--recorded-sha256", help="Recorded SHA-256 digest of source zip (defaults to current file hash if omitted).")
    parser.add_argument("--vision-model", default="google/gemini-2.5-flash", help="Vision LLM model identifier.")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1", help="Base URL for vision API endpoint.")
    parser.add_argument("--selected-by", default="operator", help="Identifier of operator who selected harness.")
    parser.add_argument("--output-dir", type=Path, default=Path("stage1_output"), help="Output directory for checkpoints and report.")
    parser.add_argument("--resume-from", help="Checkpoint name to resume from if prior checkpoint files exist.")

    args = parser.parse_args(argv)

    if not args.source_zip.exists():
        print(f"Error: source zip file not found at '{args.source_zip}'", file=sys.stderr)
        return 1

    recorded_hash = args.recorded_sha256
    if not recorded_hash:
        recorded_hash = compute_file_sha256(args.source_zip)

    config = RunConfig(
        harness_id=args.harness_id,
        source_zip_path=args.source_zip,
        recorded_sha256=recorded_hash,
        vision_model=args.vision_model,
        base_url=args.base_url,
        selected_by=args.selected_by,
        output_dir=args.output_dir,
        resume_from=args.resume_from
    )

    runner = Stage1Runner(config)
    result = runner.run()

    report_path = args.output_dir / f"{args.harness_id}_STAGE1_REPORT.json"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if result.contract_report:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result.contract_report, f, indent=2)
        print(f"STAGE 1 RUN COMPLETE: {args.harness_id}")
        print(f"Technical Status: {result.technical_status}")
        print(f"Contract Report saved to: {report_path}")
        return 0
    else:
        print(f"STAGE 1 RUN BLOCKED/FAILED: {args.harness_id}")
        print(f"Blocked Checkpoint: {result.blocked_at}")
        print(f"Technical Status: {result.technical_status}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
