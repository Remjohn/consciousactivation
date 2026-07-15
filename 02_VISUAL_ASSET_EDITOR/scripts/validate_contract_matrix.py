from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "docs" / "contracts" / "CONTRACT_COMPATIBILITY_MATRIX.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare the VAE compatibility matrix with a Delegation registry.")
    parser.add_argument("registry", type=Path, help="Path to packages/contracts/registry.json")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()

    matrix = yaml.safe_load(args.matrix.read_text(encoding="utf-8"))
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    errors: list[str] = []

    matrix_rows = matrix.get("messages", [])
    registry_rows = registry.get("messages", [])
    matrix_types = [row["message_type"] for row in matrix_rows]
    registry_types = [row["message_type"] for row in registry_rows]
    if len(matrix_types) != len(set(matrix_types)):
        errors.append("duplicate matrix message types")
    if len(registry_types) != len(set(registry_types)):
        errors.append("duplicate registry message types")

    matrix_by_type = {row["message_type"]: row for row in matrix_rows}
    registry_by_type = {row["message_type"]: row for row in registry_rows}
    authority_snapshot = matrix.get("registered_authority_snapshot", {})
    for message_type in sorted(set(registry_by_type) - set(matrix_by_type)):
        errors.append(f"missing matrix message: {message_type}")
    for message_type in sorted(set(matrix_by_type) - set(registry_by_type)):
        errors.append(f"orphan matrix message: {message_type}")

    package_root = args.registry.resolve().parents[2]
    for message_type in sorted(set(matrix_by_type) & set(registry_by_type)):
        matrix_row = matrix_by_type[message_type]
        registry_row = registry_by_type[message_type]
        expected_hash = registry_row["schema_hash"].removeprefix("sha256:")
        if str(matrix_row["message_version"]) != str(registry_row["message_version"]):
            errors.append(f"version mismatch: {message_type}")
        if matrix_row["schema"] != registry_row["schema_path"]:
            errors.append(f"schema path mismatch: {message_type}")
        if matrix_row["schema_sha256"] != expected_hash:
            errors.append(f"schema hash mismatch: {message_type}")
        schema_path = package_root / registry_row["schema_path"]
        if not schema_path.is_file():
            errors.append(f"missing schema file: {message_type}")
        elif hashlib.sha256(schema_path.read_bytes()).hexdigest() != expected_hash:
            errors.append(f"registry-to-file hash mismatch: {message_type}")
        authority = authority_snapshot.get(message_type)
        if not authority:
            errors.append(f"missing authority snapshot: {message_type}")
        else:
            if authority.get("producers") != registry_row.get("allowed_producers"):
                errors.append(f"producer mismatch: {message_type}")
            if authority.get("consumers") != registry_row.get("consumers"):
                errors.append(f"consumer mismatch: {message_type}")

    for message_type in sorted(set(authority_snapshot) - set(registry_by_type)):
        errors.append(f"orphan authority snapshot: {message_type}")

    allowed = set(matrix["verdict_semantics"]["allowed"])
    verdicts = Counter(row["compatibility_verdict"] for row in matrix_rows)
    for verdict in verdicts:
        if verdict not in allowed:
            errors.append(f"unsupported verdict: {verdict}")
    declared = matrix.get("supersession", {}).get("compatibility_summary", {})
    if {key: verdicts.get(key, 0) for key in allowed} != {key: declared.get(key, 0) for key in allowed}:
        errors.append("declared compatibility summary does not match message verdicts")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "matrix_messages": len(matrix_rows),
        "registry_messages": len(registry_rows),
        "verdicts": dict(sorted(verdicts.items())),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
