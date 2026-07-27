from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SUBSYSTEM_ROOT = REPO_ROOT / "intelligence" / "subsystems"
RUNTIME_ASSET_ROOT = SUBSYSTEM_ROOT / "runtime"

CONFIG_SCHEMA_ID = "cmf.subsystem.config/v1"
RULES_SCHEMA_ID = "cmf.subsystem.rules/v1"

CONFIG_REQUIRED_KEYS = {
    "$schema": str,
    "schema_id": str,
    "subsystem_id": str,
    "name": str,
    "version": str,
    "priority_tier": str,
    "research_basis": list,
    "inputs": list,
    "outputs": list,
    "thresholds": dict,
    "default_action_on_fail": str,
}

RULES_REQUIRED_KEYS = {
    "schema": str,
    "schema_id": str,
    "subsystem_id": str,
    "enabled": bool,
    "priority": dict,
    "enforcement": dict,
    "applies_to": dict,
}

RUNTIME_ASSET_CONFIG = {
    "scene_builder": {
        "asset_id": "SSRT-SCENE-BUILDER-v1",
        "compile_target": "SCENE_BUILDER",
        "path": RUNTIME_ASSET_ROOT / "scene_builder.runtime.json",
    },
    "editor_regeneration": {
        "asset_id": "SSRT-EDITOR-REGEN-v1",
        "compile_target": "EDITOR_REGENERATION",
        "path": RUNTIME_ASSET_ROOT / "editor_regeneration.runtime.json",
    },
}

ALL_SUBSYSTEM_IDS = tuple(
    sorted(path.name for path in SUBSYSTEM_ROOT.glob("CS-*") if path.is_dir())
)

STAGE_SUBSYSTEM_ID_MAP = {
    "scene_builder": list(ALL_SUBSYSTEM_IDS),
    "editor_regeneration": list(ALL_SUBSYSTEM_IDS),
}


class SubsystemValidationError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload or {}


def _validate_required_keys(payload: dict[str, Any], required_keys: dict[str, type], label: str) -> list[str]:
    errors = []
    for key, expected_type in required_keys.items():
        if key not in payload:
            errors.append(f"missing required key '{key}' in {label}")
            continue
        if not isinstance(payload[key], expected_type):
            errors.append(
                f"key '{key}' in {label} must be {expected_type.__name__}, got {type(payload[key]).__name__}"
            )
    return errors


def validate_subsystem_config(payload: dict[str, Any], subsystem_id: str) -> None:
    errors = _validate_required_keys(payload, CONFIG_REQUIRED_KEYS, f"{subsystem_id} config")
    if payload.get("schema_id") != CONFIG_SCHEMA_ID:
        errors.append(f"{subsystem_id} config schema_id must be '{CONFIG_SCHEMA_ID}'")
    if payload.get("subsystem_id") != subsystem_id:
        errors.append(f"{subsystem_id} config subsystem_id mismatch")
    if payload.get("default_action_on_fail") not in {"PASS", "REVISE", "BLOCK"}:
        errors.append(f"{subsystem_id} config default_action_on_fail must be PASS, REVISE, or BLOCK")
    if not payload.get("research_basis"):
        errors.append(f"{subsystem_id} config must declare at least one research_basis entry")
    if not payload.get("inputs"):
        errors.append(f"{subsystem_id} config must declare at least one input")
    if not payload.get("outputs"):
        errors.append(f"{subsystem_id} config must declare at least one output")
    if not payload.get("thresholds"):
        errors.append(f"{subsystem_id} config must declare at least one threshold")
    if errors:
        raise SubsystemValidationError("; ".join(errors))


def validate_subsystem_rules(payload: dict[str, Any], subsystem_id: str) -> None:
    errors = _validate_required_keys(payload, RULES_REQUIRED_KEYS, f"{subsystem_id} rules")
    if payload.get("schema_id") != RULES_SCHEMA_ID:
        errors.append(f"{subsystem_id} rules schema_id must be '{RULES_SCHEMA_ID}'")
    if payload.get("subsystem_id") != subsystem_id:
        errors.append(f"{subsystem_id} rules subsystem_id mismatch")

    priority = payload.get("priority", {})
    if not isinstance(priority.get("tier"), str):
        errors.append(f"{subsystem_id} rules priority.tier must be a string")
    if not isinstance(priority.get("rank"), int):
        errors.append(f"{subsystem_id} rules priority.rank must be an integer")

    enforcement = payload.get("enforcement", {})
    if enforcement.get("mode") not in {"pass_on_fail", "revise_on_fail", "block_on_fail"}:
        errors.append(f"{subsystem_id} rules enforcement.mode is invalid")
    if enforcement.get("default_result") not in {"PASS", "REVISE", "BLOCK"}:
        errors.append(f"{subsystem_id} rules enforcement.default_result is invalid")

    applies_to = payload.get("applies_to", {})
    if not isinstance(applies_to.get("stages"), list) or not applies_to["stages"]:
        errors.append(f"{subsystem_id} rules applies_to.stages must be a non-empty list")
    if not isinstance(applies_to.get("containers"), list):
        errors.append(f"{subsystem_id} rules applies_to.containers must be a list")

    if errors:
        raise SubsystemValidationError("; ".join(errors))


def load_subsystem_package(subsystem_id: str) -> dict[str, Any]:
    package_dir = SUBSYSTEM_ROOT / subsystem_id
    config_path = package_dir / "config.json"
    rules_path = package_dir / "rules.yaml"
    skill_path = package_dir / "SKILL.md"
    intelligence_path = package_dir / "intelligence.md"

    missing = [
        str(path)
        for path in [config_path, rules_path, skill_path, intelligence_path]
        if not path.exists()
    ]
    if missing:
        raise SubsystemValidationError(f"{subsystem_id} package missing files: {', '.join(missing)}")

    config = _load_json(config_path)
    rules = _load_yaml(rules_path)

    validate_subsystem_config(config, subsystem_id)
    validate_subsystem_rules(rules, subsystem_id)

    return {
        "subsystem_id": subsystem_id,
        "config": config,
        "rules": rules,
        "paths": {
            "package_dir": str(package_dir),
            "config": str(config_path),
            "rules": str(rules_path),
            "skill": str(skill_path),
            "intelligence": str(intelligence_path),
        },
    }


def build_subsystem_runtime(stage_name: str, subsystem_ids: list[str] | None = None) -> dict[str, Any]:
    if subsystem_ids is None:
        subsystem_ids = STAGE_SUBSYSTEM_ID_MAP.get(stage_name, list(ALL_SUBSYSTEM_IDS))

    packages = {}
    for subsystem_id in subsystem_ids:
        package = load_subsystem_package(subsystem_id)
        stages = package["rules"].get("applies_to", {}).get("stages", [])
        if stage_name not in stages:
            continue
        packages[subsystem_id] = package

    thresholds = {
        subsystem_id: package["config"]["thresholds"]
        for subsystem_id, package in packages.items()
    }
    evidence_refs = []
    for package in packages.values():
        evidence_refs.extend([
            package["paths"]["config"],
            package["paths"]["rules"],
        ])

    return {
        "stage": stage_name,
        "validation_contract": {
            "config_schema_id": CONFIG_SCHEMA_ID,
            "rules_schema_id": RULES_SCHEMA_ID,
        },
        "active_subsystems": sorted(packages.keys()),
        "packages": packages,
        "thresholds": thresholds,
        "evidence_refs": evidence_refs,
    }


def compile_subsystem_runtime_asset(stage_name: str, subsystem_ids: list[str] | None = None) -> dict[str, Any]:
    if stage_name not in RUNTIME_ASSET_CONFIG:
        raise SubsystemValidationError(f"Unsupported runtime stage for subsystem compilation: {stage_name}")

    runtime = build_subsystem_runtime(stage_name, subsystem_ids)
    asset_config = RUNTIME_ASSET_CONFIG[stage_name]
    asset_path = asset_config["path"]
    asset_path.parent.mkdir(parents=True, exist_ok=True)

    asset = {
        "asset_id": asset_config["asset_id"],
        "version": "1.0.0",
        "compile_target": asset_config["compile_target"],
        "runtime_stage": stage_name,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "validation_contract": runtime["validation_contract"],
        "active_subsystems": runtime["active_subsystems"],
        "thresholds": runtime["thresholds"],
        "packages": {
            subsystem_id: {
                "name": package["config"]["name"],
                "priority_tier": package["config"]["priority_tier"],
                "default_action_on_fail": package["config"]["default_action_on_fail"],
                "thresholds": package["config"]["thresholds"],
                "applies_to": package["rules"]["applies_to"],
                "enforcement": package["rules"]["enforcement"],
                "rules": {
                    "priority": package["rules"].get("priority", {}),
                    "block_conditions": package["rules"].get("block_conditions", []),
                    "warn_conditions": package["rules"].get("warn_conditions", []),
                    "route_hints": package["rules"].get("route_hints", {}),
                    "coordinates_with": package["rules"].get("coordinates_with", []),
                    "evaluation_order": package["rules"].get("evaluation_order", {}),
                },
            }
            for subsystem_id, package in runtime["packages"].items()
        },
        "evidence_refs": sorted(set(runtime["evidence_refs"])),
    }
    asset_path.write_text(json.dumps(asset, indent=2), encoding="utf-8")
    asset["asset_path"] = str(asset_path)
    return asset


def load_compiled_subsystem_runtime_asset(stage_name: str, subsystem_ids: list[str] | None = None) -> dict[str, Any]:
    asset = compile_subsystem_runtime_asset(stage_name, subsystem_ids)
    loaded = _load_json(Path(asset["asset_path"]))
    loaded["asset_path"] = asset["asset_path"]
    return loaded