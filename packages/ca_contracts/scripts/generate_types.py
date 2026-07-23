from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

HEADER_PY = """# Generated from activative-production-spine JSON Schemas.
# Do not edit manually.
from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

"""

HEADER_TS = """// Generated from activative-production-spine JSON Schemas.
// Do not edit manually.

"""

def class_name(title: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z]+", " ", title).strip()
    return "".join(part[:1].upper() + part[1:] for part in cleaned.split())

def ref_title(ref: str, schemas: dict[str, dict[str, Any]]) -> str:
    filename = Path(ref).name
    return class_name(schemas[filename]["title"])

def py_type(node: dict[str, Any], schemas: dict[str, dict[str, Any]]) -> str:
    if "$ref" in node:
        return ref_title(node["$ref"], schemas)
    if "oneOf" in node:
        parts = [py_type(part, schemas) for part in node["oneOf"]]
        dedup = list(dict.fromkeys(parts))
        return " | ".join(dedup)
    t = node.get("type")
    if isinstance(t, list):
        parts = []
        for item in t:
            parts.append(py_type({**node, "type": item}, schemas))
        return " | ".join(dict.fromkeys(parts))
    if "enum" in node:
        values = ", ".join(repr(value) for value in node["enum"])
        return f"Literal[{values}]"
    if t == "string":
        return "str"
    if t == "integer":
        return "int"
    if t == "boolean":
        return "bool"
    if t == "null":
        return "None"
    if t == "array":
        return f"tuple[{py_type(node['items'], schemas)}, ...]"
    if t == "object":
        return "dict[str, object]"
    raise ValueError(f"Unsupported Python schema node: {node}")

def ts_type(node: dict[str, Any], schemas: dict[str, dict[str, Any]]) -> str:
    if "$ref" in node:
        return ref_title(node["$ref"], schemas)
    if "oneOf" in node:
        return " | ".join(dict.fromkeys(ts_type(part, schemas) for part in node["oneOf"]))
    t = node.get("type")
    if isinstance(t, list):
        return " | ".join(dict.fromkeys(ts_type({**node, "type": item}, schemas) for item in t))
    if "enum" in node:
        return " | ".join(json.dumps(value) for value in node["enum"])
    if t == "string":
        return "string"
    if t == "integer":
        return "number"
    if t == "boolean":
        return "boolean"
    if t == "null":
        return "null"
    if t == "array":
        return f"ReadonlyArray<{ts_type(node['items'], schemas)}>"
    if t == "object":
        return "Readonly<Record<string, unknown>>"
    raise ValueError(f"Unsupported TypeScript schema node: {node}")

def load_schemas(schema_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    registry_path = schema_dir / "CONTRACT_REGISTRY.json"
    if not registry_path.exists():
        registry_path = schema_dir.parent / "registry" / "CONTRACT_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    schemas: dict[str, dict[str, Any]] = {}
    for entry in registry["schemas"]:
        filename = Path(entry["path"]).name
        schemas[filename] = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
    return schemas, registry

def generate_python(schemas: dict[str, dict[str, Any]], registry: dict[str, Any]) -> str:
    lines = [HEADER_PY]
    for entry in registry["schemas"]:
        schema = schemas[Path(entry["path"]).name]
        name = class_name(schema["title"])
        required = set(schema.get("required", []))
        lines.append(f"class {name}(TypedDict):\n")
        for field, field_schema in schema["properties"].items():
            typ = py_type(field_schema, schemas)
            if field not in required:
                typ = f"NotRequired[{typ}]"
            lines.append(f"    {field}: {typ}\n")
        lines.append("\n")
    return "".join(lines)

def generate_typescript(schemas: dict[str, dict[str, Any]], registry: dict[str, Any]) -> str:
    lines = [HEADER_TS]
    for entry in registry["schemas"]:
        schema = schemas[Path(entry["path"]).name]
        name = class_name(schema["title"])
        required = set(schema.get("required", []))
        lines.append(f"export interface {name} {{\n")
        for field, field_schema in schema["properties"].items():
            optional = "" if field in required else "?"
            lines.append(f"  readonly {field}{optional}: {ts_type(field_schema, schemas)};\n")
        lines.append("}\n\n")
    return "".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schemas", type=Path, required=True)
    parser.add_argument("--python-out", type=Path, required=True)
    parser.add_argument("--typescript-out", type=Path, required=True)
    args = parser.parse_args()

    schemas, registry = load_schemas(args.schemas)
    py = generate_python(schemas, registry)
    ts = generate_typescript(schemas, registry)
    args.python_out.parent.mkdir(parents=True, exist_ok=True)
    args.typescript_out.parent.mkdir(parents=True, exist_ok=True)
    args.python_out.write_text(py, encoding="utf-8", newline="\n")
    args.typescript_out.write_text(ts, encoding="utf-8", newline="\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
