from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTAINER_ROOT = REPO_ROOT / "intelligence" / "containers"
COMPONENT_ROOT = REPO_ROOT / "intelligence" / "components"
RUNTIME_ASSET_ROOT = REPO_ROOT / "intelligence" / "scene_intelligence" / "runtime"
SCENE_RESEARCH_OVERLAY_PATH = REPO_ROOT / "intelligence" / "scene_intelligence" / "source" / "scene_builder_research_overlay.json"
COGNITIVE_RHYTHM_VALIDATOR_PATH = REPO_ROOT / "intelligence" / "gates" / "cognitive_rhythm_validator.scene_builder.runtime.json"

CONTAINER_CONTRACT_SCHEMA_ID = "cmf.container.contract/v1"
CONTAINER_RULES_SCHEMA_ID = "cmf.container.rules/v1"
COMPONENT_SPEC_SCHEMA_ID = "cmf.component.spec/v1"
COMPONENT_RULES_SCHEMA_ID = "cmf.component.rules/v1"
SCENE_INTELLIGENCE_RUNTIME_SCHEMA_ID = "cmf.scene.intelligence.runtime/v1"

CONTAINER_CONTRACT_REQUIRED_KEYS = {
    "$schema": str,
    "schema_id": str,
    "container_id": str,
    "name": str,
    "version": str,
    "arc_order": int,
    "narrative_role": str,
    "neural_targets": list,
    "transportation_state": dict,
    "cls_budget": dict,
    "asl_seconds": dict,
    "color_temperature_kelvin": dict,
    "pad_target": dict,
    "motion_palette": list,
    "duration_share_of_video": dict,
    "detection_mode": str,
    "prediction_error_budget": dict,
    "compatible_components": list,
    "hard_requirements": list,
    "default_component": str,
}

CONTAINER_RULES_REQUIRED_KEYS = {
    "schema": str,
    "schema_id": str,
    "container_id": str,
    "enabled": bool,
    "priority": dict,
    "enforcement": dict,
    "applies_to": dict,
    "required_sequence": dict,
}

COMPONENT_SPEC_REQUIRED_KEYS = {
    "$schema": str,
    "schema_id": str,
    "component_id": str,
    "scene_number": int,
    "name": str,
    "version": str,
    "function": str,
    "compatible_containers": list,
    "cls_footprint": dict,
    "required_asset_types": list,
    "template_variants": list,
    "effect_dependencies": list,
    "selection_signals": list,
    "audio_profile": dict,
    "fallback_behavior": str,
}

COMPONENT_RULES_REQUIRED_KEYS = {
    "schema": str,
    "schema_id": str,
    "component_id": str,
    "enabled": bool,
    "selection_priority": dict,
    "enforcement": dict,
    "applies_to": dict,
}

RUNTIME_ASSET_CONFIG = {
    "scene_builder": {
        "asset_id": "SIRT-SCENE-BUILDER-v1",
        "compile_target": "SCENE_BUILDER",
        "path": RUNTIME_ASSET_ROOT / "scene_builder.runtime.json",
    },
    "editor_regeneration": {
        "asset_id": "SIRT-EDITOR-REGEN-v1",
        "compile_target": "EDITOR_REGENERATION",
        "path": RUNTIME_ASSET_ROOT / "editor_regeneration.runtime.json",
    },
}

ARC_STAGE_CONTAINER_MAP = {
    "OPENING": "HOOK",
    "HOOK": "HOOK",
    "SETUP": "SETUP",
    "RISING_ACTION": "CHALLENGE",
    "CHALLENGE": "CHALLENGE",
    "TENSION": "CHALLENGE",
    "TURNING_POINT": "TURNING_POINT",
    "CLIMAX": "TURNING_POINT",
    "RESOLUTION": "RESOLUTION",
    "VISION": "VISION",
    "ENDING": "VISION",
    "OUTRO": "VISION",
}

ALL_CONTAINER_IDS = tuple(
    sorted(
        path.name
        for path in CONTAINER_ROOT.iterdir()
        if path.is_dir() and (path / "contract.json").exists()
    )
)
ALL_COMPONENT_IDS = tuple(
    sorted(
        path.name
        for path in COMPONENT_ROOT.iterdir()
        if path.is_dir() and (path / "spec.json").exists()
    )
)


class SceneIntelligenceValidationError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload or {}


def _load_scene_research_overlay() -> dict[str, Any]:
    return _load_json(SCENE_RESEARCH_OVERLAY_PATH)


def _load_cognitive_rhythm_validator() -> dict[str, Any]:
    return _load_json(COGNITIVE_RHYTHM_VALIDATOR_PATH)


def _merge_scene_template_defaults(template_id: str, template: dict[str, Any], family_defaults: dict[str, Any]) -> dict[str, Any]:
    merged = dict(family_defaults)
    merged.update(template)
    merged["template_id"] = template_id
    return merged


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


def validate_container_contract(payload: dict[str, Any], container_id: str) -> None:
    errors = _validate_required_keys(payload, CONTAINER_CONTRACT_REQUIRED_KEYS, f"{container_id} contract")
    if payload.get("schema_id") != CONTAINER_CONTRACT_SCHEMA_ID:
        errors.append(f"{container_id} contract schema_id must be '{CONTAINER_CONTRACT_SCHEMA_ID}'")
    if payload.get("container_id") != container_id:
        errors.append(f"{container_id} contract container_id mismatch")
    if payload.get("default_component") not in payload.get("compatible_components", []):
        errors.append(f"{container_id} contract default_component must be listed in compatible_components")
    if payload.get("detection_mode") not in {"TENSION", "VULNERABILITY", "RECOGNITION"}:
        errors.append(f"{container_id} contract detection_mode is invalid")

    transportation_state = payload.get("transportation_state", {})
    if not isinstance(transportation_state.get("phase"), str):
        errors.append(f"{container_id} contract transportation_state.phase must be a string")
    if not isinstance(transportation_state.get("target_depth"), (int, float)):
        errors.append(f"{container_id} contract transportation_state.target_depth must be numeric")
    elif not 0 <= float(transportation_state["target_depth"]) <= 1:
        errors.append(f"{container_id} contract transportation_state.target_depth must be between 0 and 1")
    if not isinstance(transportation_state.get("reentry_required"), bool):
        errors.append(f"{container_id} contract transportation_state.reentry_required must be boolean")

    prediction_error_budget = payload.get("prediction_error_budget", {})
    if not isinstance(prediction_error_budget.get("target"), (int, float)):
        errors.append(f"{container_id} contract prediction_error_budget.target must be numeric")
    elif not 0 <= float(prediction_error_budget["target"]) <= 1:
        errors.append(f"{container_id} contract prediction_error_budget.target must be between 0 and 1")
    if not isinstance(prediction_error_budget.get("max"), (int, float)):
        errors.append(f"{container_id} contract prediction_error_budget.max must be numeric")
    elif not 0 <= float(prediction_error_budget["max"]) <= 1:
        errors.append(f"{container_id} contract prediction_error_budget.max must be between 0 and 1")
    if isinstance(prediction_error_budget.get("target"), (int, float)) and isinstance(
        prediction_error_budget.get("max"), (int, float)
    ):
        if float(prediction_error_budget["target"]) > float(prediction_error_budget["max"]):
            errors.append(f"{container_id} contract prediction_error_budget.target must not exceed max")
    if not isinstance(prediction_error_budget.get("strategy"), str):
        errors.append(f"{container_id} contract prediction_error_budget.strategy must be a string")

    if errors:
        raise SceneIntelligenceValidationError("; ".join(errors))


def validate_container_rules(payload: dict[str, Any], container_id: str) -> None:
    errors = _validate_required_keys(payload, CONTAINER_RULES_REQUIRED_KEYS, f"{container_id} rules")
    if payload.get("schema_id") != CONTAINER_RULES_SCHEMA_ID:
        errors.append(f"{container_id} rules schema_id must be '{CONTAINER_RULES_SCHEMA_ID}'")
    if payload.get("container_id") != container_id:
        errors.append(f"{container_id} rules container_id mismatch")

    priority = payload.get("priority", {})
    if not isinstance(priority.get("tier"), str):
        errors.append(f"{container_id} rules priority.tier must be a string")
    if not isinstance(priority.get("rank"), int):
        errors.append(f"{container_id} rules priority.rank must be an integer")

    applies_to = payload.get("applies_to", {})
    if not isinstance(applies_to.get("stages"), list) or not applies_to.get("stages"):
        errors.append(f"{container_id} rules applies_to.stages must be a non-empty list")

    required_sequence = payload.get("required_sequence", {})
    if not isinstance(required_sequence.get("previous", []), list):
        errors.append(f"{container_id} rules required_sequence.previous must be a list")
    if not isinstance(required_sequence.get("next", []), list):
        errors.append(f"{container_id} rules required_sequence.next must be a list")

    if errors:
        raise SceneIntelligenceValidationError("; ".join(errors))


def validate_component_spec(payload: dict[str, Any], component_id: str) -> None:
    errors = _validate_required_keys(payload, COMPONENT_SPEC_REQUIRED_KEYS, f"{component_id} spec")
    if payload.get("schema_id") != COMPONENT_SPEC_SCHEMA_ID:
        errors.append(f"{component_id} spec schema_id must be '{COMPONENT_SPEC_SCHEMA_ID}'")
    if payload.get("component_id") != component_id:
        errors.append(f"{component_id} spec component_id mismatch")
    if not payload.get("compatible_containers"):
        errors.append(f"{component_id} spec must declare at least one compatible container")
    if errors:
        raise SceneIntelligenceValidationError("; ".join(errors))


def validate_component_rules(payload: dict[str, Any], component_id: str) -> None:
    errors = _validate_required_keys(payload, COMPONENT_RULES_REQUIRED_KEYS, f"{component_id} rules")
    if payload.get("schema_id") != COMPONENT_RULES_SCHEMA_ID:
        errors.append(f"{component_id} rules schema_id must be '{COMPONENT_RULES_SCHEMA_ID}'")
    if payload.get("component_id") != component_id:
        errors.append(f"{component_id} rules component_id mismatch")

    selection_priority = payload.get("selection_priority", {})
    if not isinstance(selection_priority.get("tier"), str):
        errors.append(f"{component_id} rules selection_priority.tier must be a string")
    if not isinstance(selection_priority.get("rank"), int):
        errors.append(f"{component_id} rules selection_priority.rank must be an integer")

    applies_to = payload.get("applies_to", {})
    if not isinstance(applies_to.get("stages"), list) or not applies_to.get("stages"):
        errors.append(f"{component_id} rules applies_to.stages must be a non-empty list")
    if not isinstance(applies_to.get("containers"), list) or not applies_to.get("containers"):
        errors.append(f"{component_id} rules applies_to.containers must be a non-empty list")

    if errors:
        raise SceneIntelligenceValidationError("; ".join(errors))


def load_container_package(container_id: str) -> dict[str, Any]:
    package_dir = CONTAINER_ROOT / container_id
    contract_path = package_dir / "contract.json"
    rules_path = package_dir / "rules.yaml"

    missing = [str(path) for path in [contract_path, rules_path] if not path.exists()]
    if missing:
        raise SceneIntelligenceValidationError(f"{container_id} package missing files: {', '.join(missing)}")

    contract = _load_json(contract_path)
    rules = _load_yaml(rules_path)

    validate_container_contract(contract, container_id)
    validate_container_rules(rules, container_id)

    return {
        "container_id": container_id,
        "contract": contract,
        "rules": rules,
        "paths": {
            "package_dir": str(package_dir),
            "contract": str(contract_path),
            "rules": str(rules_path),
        },
    }


def load_component_package(component_id: str) -> dict[str, Any]:
    package_dir = COMPONENT_ROOT / component_id
    spec_path = package_dir / "spec.json"
    rules_path = package_dir / "rules.yaml"

    missing = [str(path) for path in [spec_path, rules_path] if not path.exists()]
    if missing:
        raise SceneIntelligenceValidationError(f"{component_id} package missing files: {', '.join(missing)}")

    spec = _load_json(spec_path)
    rules = _load_yaml(rules_path)

    validate_component_spec(spec, component_id)
    validate_component_rules(rules, component_id)

    return {
        "component_id": component_id,
        "spec": spec,
        "rules": rules,
        "paths": {
            "package_dir": str(package_dir),
            "spec": str(spec_path),
            "rules": str(rules_path),
        },
    }


def build_scene_intelligence_runtime(
    stage_name: str,
    container_ids: list[str] | None = None,
    component_ids: list[str] | None = None,
) -> dict[str, Any]:
    container_ids = container_ids or list(ALL_CONTAINER_IDS)
    component_ids = component_ids or list(ALL_COMPONENT_IDS)

    containers = {}
    for container_id in container_ids:
        package = load_container_package(container_id)
        if stage_name not in package["rules"].get("applies_to", {}).get("stages", []):
            continue
        containers[container_id] = package

    components = {}
    for component_id in component_ids:
        package = load_component_package(component_id)
        if stage_name not in package["rules"].get("applies_to", {}).get("stages", []):
            continue
        components[component_id] = package

    container_component_index = {}
    for container_id, container_package in containers.items():
        compatible_components = []
        for component_id in container_package["contract"].get("compatible_components", []):
            component_package = components.get(component_id)
            if not component_package:
                continue
            if container_id not in component_package["spec"].get("compatible_containers", []):
                continue
            if container_id not in component_package["rules"].get("applies_to", {}).get("containers", []):
                continue
            compatible_components.append(component_id)
        default_component = container_package["contract"].get("default_component")
        container_component_index[container_id] = sorted(
            compatible_components,
            key=lambda component_id: (
                0 if component_id == default_component else 1,
                components[component_id]["rules"].get("selection_priority", {}).get("rank", 999),
            ),
        )

    evidence_refs = []
    for package in containers.values():
        evidence_refs.extend([package["paths"]["contract"], package["paths"]["rules"]])
    for package in components.values():
        evidence_refs.extend([package["paths"]["spec"], package["paths"]["rules"]])

    research_overlay = _load_scene_research_overlay()
    family_defaults = research_overlay.get("scene_family_defaults", {})
    scene_templates = {}
    container_template_index: dict[str, list[str]] = {}
    for template_id, template in research_overlay.get("scene_templates", {}).items():
        container_id = template.get("container_id")
        if container_id not in containers:
            continue
        preferred_components = [
            component_id
            for component_id in template.get("preferred_components", [])
            if component_id in components
        ]
        if template.get("preferred_components") and not preferred_components:
            continue
        merged_template = _merge_scene_template_defaults(
            template_id,
            {
                **template,
                "preferred_components": preferred_components or template.get("preferred_components", []),
            },
            family_defaults.get(container_id, {}),
        )
        scene_templates[template_id] = merged_template
        container_template_index.setdefault(container_id, []).append(template_id)

    for container_id, template_ids in container_template_index.items():
        container_template_index[container_id] = sorted(
            template_ids,
            key=lambda template_id: (
                scene_templates[template_id].get("base_cls", 99),
                template_id,
            ),
        )

    effect_library = {
        effect_id: {
            "effect_id": effect_id,
            **effect_payload,
        }
        for effect_id, effect_payload in research_overlay.get("effect_library", {}).items()
    }
    cognitive_rhythm_validator = _load_cognitive_rhythm_validator()
    evidence_refs.extend(
        [
            str(SCENE_RESEARCH_OVERLAY_PATH),
            str(COGNITIVE_RHYTHM_VALIDATOR_PATH),
        ]
    )

    return {
        "stage": stage_name,
        "validation_contract": {
            "container_contract_schema_id": CONTAINER_CONTRACT_SCHEMA_ID,
            "container_rules_schema_id": CONTAINER_RULES_SCHEMA_ID,
            "component_spec_schema_id": COMPONENT_SPEC_SCHEMA_ID,
            "component_rules_schema_id": COMPONENT_RULES_SCHEMA_ID,
        },
        "arc_stage_container_map": ARC_STAGE_CONTAINER_MAP,
        "active_containers": sorted(containers.keys()),
        "active_components": sorted(components.keys()),
        "containers": containers,
        "components": components,
        "container_component_index": container_component_index,
        "research_contracts": {
            "scene_template_contract": research_overlay.get("scene_template_contract", {}),
            "effect_contract": research_overlay.get("effect_contract", {}),
        },
        "scene_templates": scene_templates,
        "container_template_index": container_template_index,
        "effect_library": effect_library,
        "scoring_models": research_overlay.get("scoring_models", {}),
        "cognitive_rhythm_validator": cognitive_rhythm_validator,
        "evidence_refs": sorted(set(evidence_refs)),
    }


def compile_scene_intelligence_runtime_asset(
    stage_name: str,
    container_ids: list[str] | None = None,
    component_ids: list[str] | None = None,
) -> dict[str, Any]:
    if stage_name not in RUNTIME_ASSET_CONFIG:
        raise SceneIntelligenceValidationError(f"Unsupported runtime stage for scene intelligence compilation: {stage_name}")

    runtime = build_scene_intelligence_runtime(stage_name, container_ids, component_ids)
    asset_config = RUNTIME_ASSET_CONFIG[stage_name]
    asset_path = asset_config["path"]
    asset_path.parent.mkdir(parents=True, exist_ok=True)

    asset = {
        "schema_id": SCENE_INTELLIGENCE_RUNTIME_SCHEMA_ID,
        "asset_id": asset_config["asset_id"],
        "version": "1.0.0",
        "compile_target": asset_config["compile_target"],
        "runtime_stage": stage_name,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "validation_contract": runtime["validation_contract"],
        "arc_stage_container_map": runtime["arc_stage_container_map"],
        "active_containers": runtime["active_containers"],
        "active_components": runtime["active_components"],
        "container_component_index": runtime["container_component_index"],
        "containers": {
            container_id: {
                "contract": {
                    "name": package["contract"]["name"],
                    "arc_order": package["contract"]["arc_order"],
                    "narrative_role": package["contract"]["narrative_role"],
                    "neural_targets": package["contract"]["neural_targets"],
                    "transportation_state": package["contract"]["transportation_state"],
                    "cls_budget": package["contract"]["cls_budget"],
                    "asl_seconds": package["contract"]["asl_seconds"],
                    "color_temperature_kelvin": package["contract"]["color_temperature_kelvin"],
                    "pad_target": package["contract"]["pad_target"],
                    "motion_palette": package["contract"]["motion_palette"],
                    "duration_share_of_video": package["contract"]["duration_share_of_video"],
                    "detection_mode": package["contract"]["detection_mode"],
                    "prediction_error_budget": package["contract"]["prediction_error_budget"],
                    "compatible_components": package["contract"]["compatible_components"],
                    "hard_requirements": package["contract"]["hard_requirements"],
                    "default_component": package["contract"]["default_component"],
                },
                "rules": {
                    "priority": package["rules"].get("priority", {}),
                    "enforcement": package["rules"].get("enforcement", {}),
                    "applies_to": package["rules"].get("applies_to", {}),
                    "required_sequence": package["rules"].get("required_sequence", {}),
                    "warn_conditions": package["rules"].get("warn_conditions", []),
                    "route_hints": package["rules"].get("route_hints", {}),
                },
            }
            for container_id, package in runtime["containers"].items()
        },
        "components": {
            component_id: {
                "spec": {
                    "scene_number": package["spec"]["scene_number"],
                    "name": package["spec"]["name"],
                    "function": package["spec"]["function"],
                    "compatible_containers": package["spec"]["compatible_containers"],
                    "cls_footprint": package["spec"]["cls_footprint"],
                    "required_asset_types": package["spec"]["required_asset_types"],
                    "template_variants": package["spec"]["template_variants"],
                    "effect_dependencies": package["spec"]["effect_dependencies"],
                    "selection_signals": package["spec"]["selection_signals"],
                    "audio_profile": package["spec"]["audio_profile"],
                    "fallback_behavior": package["spec"]["fallback_behavior"],
                },
                "rules": {
                    "selection_priority": package["rules"].get("selection_priority", {}),
                    "enforcement": package["rules"].get("enforcement", {}),
                    "applies_to": package["rules"].get("applies_to", {}),
                    "incompatibilities": package["rules"].get("incompatibilities", []),
                    "warn_conditions": package["rules"].get("warn_conditions", []),
                    "route_hints": package["rules"].get("route_hints", {}),
                },
            }
            for component_id, package in runtime["components"].items()
        },
        "research_contracts": runtime["research_contracts"],
        "scene_templates": runtime["scene_templates"],
        "container_template_index": runtime["container_template_index"],
        "effect_library": runtime["effect_library"],
        "cognitive_rhythm_validator": {
            **runtime["cognitive_rhythm_validator"],
            "asset_path": str(COGNITIVE_RHYTHM_VALIDATOR_PATH),
        },
        "scoring_models": runtime["scoring_models"],
        "evidence_refs": runtime["evidence_refs"],
    }
    asset_path.write_text(json.dumps(asset, indent=2), encoding="utf-8")
    asset["asset_path"] = str(asset_path)
    return asset


def load_compiled_scene_intelligence_runtime_asset(
    stage_name: str,
    container_ids: list[str] | None = None,
    component_ids: list[str] | None = None,
) -> dict[str, Any]:
    asset = compile_scene_intelligence_runtime_asset(stage_name, container_ids, component_ids)
    loaded = _load_json(Path(asset["asset_path"]))
    loaded["asset_path"] = asset["asset_path"]
    return loaded