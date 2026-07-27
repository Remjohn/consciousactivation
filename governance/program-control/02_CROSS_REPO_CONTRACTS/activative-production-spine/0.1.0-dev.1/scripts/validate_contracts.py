from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validators" / "python"))

from validation import ContractValidationError, SchemaRegistry  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    registry = SchemaRegistry(ROOT / "schemas")
    failures: list[dict[str, str]] = []
    positive = 0
    negative = 0

    for path in sorted((ROOT / "fixtures" / "positive").glob("*.json")):
        schema_name = path.stem
        payload = json.loads(path.read_text(encoding="utf-8"))
        try:
            registry.validate(schema_name, payload)
            positive += 1
        except Exception as error:
            failures.append({"fixture": str(path.relative_to(ROOT)), "error": str(error)})

    for path in sorted((ROOT / "fixtures" / "negative").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        try:
            registry.validate(record["schema"], record["payload"])
        except ContractValidationError:
            negative += 1
        except Exception as error:
            failures.append({"fixture": str(path.relative_to(ROOT)), "error": f"unexpected error: {error}"})
        else:
            failures.append({"fixture": str(path.relative_to(ROOT)), "error": "negative fixture unexpectedly passed"})

    with tempfile.TemporaryDirectory(prefix="ca-contract-gen-") as temp_dir:
        temp = Path(temp_dir)
        command = [
            sys.executable,
            str(ROOT / "scripts" / "generate_types.py"),
            "--schemas",
            str(ROOT / "schemas"),
            "--python-out",
            str(temp / "generated.py"),
            "--typescript-out",
            str(temp / "contracts.ts"),
        ]
        subprocess.run(command, check=True)
        if (temp / "generated.py").read_bytes() != (ROOT / "generated" / "python" / "ca_contracts_generated.py").read_bytes():
            failures.append({"fixture": "generated/python", "error": "generated Python declarations drift"})
        if (temp / "contracts.ts").read_bytes() != (ROOT / "generated" / "typescript" / "contracts.ts").read_bytes():
            failures.append({"fixture": "generated/typescript", "error": "generated TypeScript declarations drift"})

    report = {
        "schema_version": "ca-contract-clean-room-validation/v1",
        "package": "activative-production-spine",
        "version": registry.version,
        "positive_fixtures_passed": positive,
        "negative_fixtures_rejected": negative,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
