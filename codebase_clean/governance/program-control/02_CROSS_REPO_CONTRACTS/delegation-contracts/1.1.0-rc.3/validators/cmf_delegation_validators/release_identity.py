"""Release-wide identity consistency and stale-package declaration validation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .paths import LAYOUT, ROOT


EXPECTED_PACKAGE_VERSION = "1.1.0-rc.3"
EXPECTED_PYTHON_PACKAGE_VERSION = "1.1.0rc3"
EXPECTED_PROTOCOL_VERSION = "1.0"
EXPECTED_VISUAL_ASSET_DEMAND_VERSION = "1.1"
EXPECTED_COMPATIBILITY_PROFILE_VERSION = "1.0"
EXPECTED_COMPATIBILITY_MANIFEST_ID = "cmf-delegation-contracts-1-1-0-rc-3"
HISTORICAL_MARKER = "historical_evidence: true"
HISTORICAL_PATHS = {
    "CONTRACT_CHANGELOG.md",
    "RC2_CONVERGENCE_REJECTION_REPORT.md",
}


class ReleaseIdentityError(ValueError):
    """Raised when active release identity declarations do not converge."""


def stale_package_tokens() -> tuple[str, ...]:
    """Build forbidden tokens without embedding them literally in this shipped scanner."""

    result: list[str] = []
    for candidate in (1, 2):
        result.extend(
            [
                f"1.1.0-rc.{candidate}",
                f"1.1.0rc{candidate}",
                f"cmf-delegation-contracts-1-1-0-rc-{candidate}",
                f"compatibility-profile-1-1-0-rc-{candidate}",
                f"compatibility_profile_1_1_0_rc_{candidate}",
                f"compatibility-profile-rc{candidate}",
            ]
        )
    return tuple(result)


def scan_stale_package_declarations(root: Path = ROOT) -> list[str]:
    """Scan every UTF-8 file and reject stale active package identifiers."""

    violations: list[str] = []
    forbidden = stale_package_tokens()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        matches = sorted({token for token in forbidden if token in text})
        if not matches:
            continue
        if relative in HISTORICAL_PATHS and HISTORICAL_MARKER in text:
            continue
        violations.append(f"{relative}: {', '.join(matches)}")
    return violations


def _structured_identity_violations(root: Path) -> tuple[list[str], int]:
    violations: list[str] = []
    structured_files = 0

    def walk(value: Any, relative: str, pointer: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_pointer = f"{pointer}/{key}"
                if (
                    key == "package_version"
                    and isinstance(child, str)
                    and child != EXPECTED_PACKAGE_VERSION
                ):
                    violations.append(
                        f"{relative}{child_pointer}: expected {EXPECTED_PACKAGE_VERSION!r}, got {child!r}"
                    )
                if key == "manifest_id" and isinstance(child, str) and child.startswith(
                    "cmf-delegation-contracts-"
                ) and child != EXPECTED_COMPATIBILITY_MANIFEST_ID:
                    violations.append(
                        f"{relative}{child_pointer}: expected {EXPECTED_COMPATIBILITY_MANIFEST_ID!r}, got {child!r}"
                    )
                walk(child, relative, child_pointer)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, relative, f"{pointer}/{index}")

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".yaml", ".yml"}:
            continue
        relative = path.relative_to(root).as_posix()
        try:
            if path.suffix.lower() == ".json":
                value = json.loads(path.read_text(encoding="utf-8"))
            else:
                value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
            violations.append(f"{relative}: structured parse failure: {exc}")
            continue
        structured_files += 1
        walk(value, relative)
    return violations, structured_files


def _load_json(root: Path, relative: str) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _require_equal(errors: list[str], label: str, actual: object, expected: object) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def validate_release_identity(root: Path = ROOT, layout: str = LAYOUT) -> dict[str, object]:
    """Validate every current package/version axis and all released stale tokens."""

    errors = scan_stale_package_declarations(root)
    structured_errors, structured_files = _structured_identity_violations(root)
    errors.extend(structured_errors)

    registry = _load_json(root, "contracts/registry.json")
    compatibility = _load_json(root, "compatibility/manifest.json")
    profile = _load_json(root, "compatibility/profile.json")
    package_json = _load_json(root, "contracts/package.json")
    format_manifest = _load_json(root, "fixtures/format02/manifest.json")

    _require_equal(errors, "registry.package_version", registry.get("package_version"), EXPECTED_PACKAGE_VERSION)
    _require_equal(errors, "registry.protocol_version", registry.get("protocol_version"), EXPECTED_PROTOCOL_VERSION)
    _require_equal(errors, "compatibility.package_version", compatibility.get("package_version"), EXPECTED_PACKAGE_VERSION)
    _require_equal(errors, "profile.package_version", profile.get("package_version"), EXPECTED_PACKAGE_VERSION)
    _require_equal(
        errors,
        "profile.profile_version",
        profile.get("profile_version"),
        EXPECTED_COMPATIBILITY_PROFILE_VERSION,
    )
    _require_equal(errors, "profile.protocol_version", profile.get("protocol_version"), EXPECTED_PROTOCOL_VERSION)
    _require_equal(
        errors,
        "profile.visual_asset_demand_version",
        profile.get("visual_asset_demand_version"),
        EXPECTED_VISUAL_ASSET_DEMAND_VERSION,
    )
    _require_equal(errors, "contracts/package.json version", package_json.get("version"), EXPECTED_PACKAGE_VERSION)
    _require_equal(errors, "fixtures/format02 package_version", format_manifest.get("package_version"), EXPECTED_PACKAGE_VERSION)

    for relative in ("contracts/pyproject.toml", "validators/pyproject.toml"):
        text = (root / relative).read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*"([^"]+)"', text, flags=re.MULTILINE)
        _require_equal(
            errors,
            f"{relative} project.version",
            match.group(1) if match else None,
            EXPECTED_PYTHON_PACKAGE_VERSION,
        )

    python_init = (root / "contracts/generated/python/cmf_delegation_contracts/__init__.py").read_text(
        encoding="utf-8"
    )
    python_types = (root / "contracts/generated/python/cmf_delegation_contracts/types.py").read_text(
        encoding="utf-8"
    )
    typescript = (root / "contracts/generated/typescript/index.ts").read_text(encoding="utf-8")
    generated_declarations = {
        f'__version__ = "{EXPECTED_PACKAGE_VERSION}"': python_init,
        f'PACKAGE_VERSION = "{EXPECTED_PACKAGE_VERSION}"': python_types,
        f'PROTOCOL_VERSION = "{EXPECTED_PROTOCOL_VERSION}"': python_types,
        f'VISUAL_ASSET_DEMAND_VERSION = "{EXPECTED_VISUAL_ASSET_DEMAND_VERSION}"': python_types,
        f'COMPATIBILITY_PROFILE_VERSION = "{EXPECTED_COMPATIBILITY_PROFILE_VERSION}"': python_types,
        f'export const PACKAGE_VERSION = "{EXPECTED_PACKAGE_VERSION}" as const;': typescript,
        f'export const PROTOCOL_VERSION = "{EXPECTED_PROTOCOL_VERSION}" as const;': typescript,
        f'export const VISUAL_ASSET_DEMAND_VERSION = "{EXPECTED_VISUAL_ASSET_DEMAND_VERSION}" as const;': typescript,
        f'export const COMPATIBILITY_PROFILE_VERSION = "{EXPECTED_COMPATIBILITY_PROFILE_VERSION}" as const;': typescript,
    }
    for declaration, text in generated_declarations.items():
        if declaration not in text:
            errors.append(f"generated metadata missing: {declaration}")

    messages = {item["message_type"]: item for item in registry["messages"]}
    for message_type, item in messages.items():
        expected_message_version = (
            EXPECTED_VISUAL_ASSET_DEMAND_VERSION
            if message_type == "visual-asset-demand"
            else EXPECTED_PROTOCOL_VERSION
        )
        _require_equal(
            errors,
            f"registry {message_type} message_version",
            item.get("message_version"),
            expected_message_version,
        )
        expected_schema_suffix = f"/{message_type}/{expected_message_version}/schema.json"
        if not item.get("schema_id", "").endswith(expected_schema_suffix):
            errors.append(f"registry {message_type} schema_id does not end with {expected_schema_suffix}")
        schema = _load_json(root, item["schema_path"])
        _require_equal(
            errors,
            f"schema {message_type} message version",
            schema.get("x-cmf-message-version"),
            expected_message_version,
        )
        _require_equal(errors, f"schema {message_type} id", schema.get("$id"), item.get("schema_id"))

    compatibility_entry = messages["compatibility-manifest"]
    _require_equal(
        errors,
        "compatibility-manifest message version",
        compatibility_entry["message_version"],
        EXPECTED_COMPATIBILITY_PROFILE_VERSION,
    )
    submission_receipt = _load_json(root, "contracts/examples/submission-validation-receipt.example.json")
    negotiated_profile = submission_receipt["negotiated_profile"]
    _require_equal(
        errors,
        "negotiated compatibility profile version",
        negotiated_profile.get("version"),
        EXPECTED_COMPATIBILITY_PROFILE_VERSION,
    )

    migration = _load_json(root, "compatibility/migrations/visual-asset-demand-v1-to-v1.1.json")
    source_kind_migration = _load_json(
        root, "compatibility/migrations/visual-asset-demand-v1.1-source-kind-classification.json"
    )
    _require_equal(errors, "V1 migration target", migration.get("target"), "visual-asset-demand@1.1")
    _require_equal(
        errors,
        "source-kind migration target",
        source_kind_migration.get("target"),
        "visual-asset-demand@1.1",
    )

    if layout == "SOURCE":
        source_manifest = _load_json(root, "contracts/source-manifest.json")
        _require_equal(
            errors,
            "source manifest package_version",
            source_manifest.get("package_version"),
            EXPECTED_PACKAGE_VERSION,
        )
    else:
        receipt = _load_json(root, "RELEASE_RECEIPT.json")
        release_manifest = _load_json(root, "contracts/release-manifest.json")
        for label, value in (("receipt", receipt), ("release manifest", release_manifest)):
            _require_equal(errors, f"{label} package_version", value.get("package_version"), EXPECTED_PACKAGE_VERSION)
            _require_equal(errors, f"{label} protocol_version", value.get("protocol_version"), EXPECTED_PROTOCOL_VERSION)
            _require_equal(
                errors,
                f"{label} compatibility_profile_version",
                value.get("compatibility_profile_version"),
                EXPECTED_COMPATIBILITY_PROFILE_VERSION,
            )
        _require_equal(
            errors,
            "release manifest visual_asset_demand_version",
            release_manifest.get("visual_asset_demand_version"),
            EXPECTED_VISUAL_ASSET_DEMAND_VERSION,
        )
        _require_equal(
            errors,
            "receipt visual-asset-demand version",
            receipt.get("message_versions", {}).get("visual-asset-demand"),
            EXPECTED_VISUAL_ASSET_DEMAND_VERSION,
        )

    if errors:
        raise ReleaseIdentityError("Release identity validation failed:\n- " + "\n- ".join(errors))
    utf8_files = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        utf8_files += 1
    return {
        "package_version": EXPECTED_PACKAGE_VERSION,
        "protocol_version": EXPECTED_PROTOCOL_VERSION,
        "visual_asset_demand_version": EXPECTED_VISUAL_ASSET_DEMAND_VERSION,
        "compatibility_profile_version": EXPECTED_COMPATIBILITY_PROFILE_VERSION,
        "utf8_files_scanned": utf8_files,
        "structured_files_scanned": structured_files,
        "stale_active_declarations": 0,
    }
