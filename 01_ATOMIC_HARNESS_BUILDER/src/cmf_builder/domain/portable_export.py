from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping


DEFINITION_SCHEMA = "cmf-builder-atomic-harness-definition/v1"
COMPILER_ID = "cmf-builder/productized-manifest-compiler"
COMPILER_VERSION = "1.0.0"
AUTHORITY_CHAIN = (
    "activative_intelligence_constitution_v1_1",
    "builder_prd_v1_2",
    "PX-AM-001",
)
EXECUTION_PLAN = (
    "accept_governed_operator_manifest",
    "validate_atomic_boundary_and_contracts",
    "compile_atomic_harness_definition",
    "validate_acceptance_contracts",
    "package_portable_artifacts",
)


class PortableDefinitionInvalid(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class PortableAtomicHarnessDefinition:
    definition_id: str
    definition_hash: str
    content_bytes: bytes
    payload_bytes: bytes

    @classmethod
    def create(
        cls,
        *,
        manifest_id: str,
        manifest_version: str,
        manifest_hash: str,
        task_id: str,
        mode: str,
        normalized: Mapping[str, object],
        category_binding: Mapping[str, object],
    ) -> "PortableAtomicHarnessDefinition":
        task = normalized.get("task")
        activative = normalized.get("activative_input")
        if not isinstance(task, Mapping):
            raise PortableDefinitionInvalid("Governed task contract is missing.")
        if mode not in {"generic", "activative"}:
            raise PortableDefinitionInvalid("Manifest mode is not governed.")
        if (mode == "generic" and activative is not None) or (
            mode == "activative" and not isinstance(activative, Mapping)
        ):
            raise PortableDefinitionInvalid("Activative structure does not match manifest mode.")
        authority_ref = task.get("authority_ref")
        provenance_refs = task.get("provenance_refs")
        if not isinstance(authority_ref, str) or not isinstance(provenance_refs, list):
            raise PortableDefinitionInvalid("Authority or provenance evidence is missing.")
        if mode == "generic":
            classification = [
                "category_neutral",
                "generic_operator_manifest",
                "non_certified",
                "non_production",
            ]
        else:
            category_id = category_binding.get("category_id")
            if not isinstance(category_id, str) or not category_id:
                raise PortableDefinitionInvalid("Activative category binding is missing.")
            classification = [
                "canonical_category_bound",
                category_id,
                "activative_operator_manifest",
                "non_certified",
                "non_production",
            ]
        content: dict[str, object] = {
            "schema_id": DEFINITION_SCHEMA,
            "schema_version": "1.0.0",
            "compiler_id": COMPILER_ID,
            "compiler_version": COMPILER_VERSION,
            "amendment": "PX-AM-001",
            "manifest_id": manifest_id,
            "manifest_version": manifest_version,
            "manifest_hash": manifest_hash,
            "task_id": task_id,
            "mode": mode,
            "classification": classification,
            "category_binding": dict(category_binding),
            "atomic_boundary": task.get("atomic_boundary"),
            "goal": task.get("goal"),
            "success_condition": task.get("success_condition"),
            "input_contract": task.get("input_contract"),
            "output_contract": task.get("output_contract"),
            "minimum_complete_context": task.get("required_context"),
            "capability_requirements": task.get("capability_requirements"),
            "acceptance_tests": task.get("acceptance_tests"),
            "execution_plan": list(EXECUTION_PLAN),
            "authority_chain": [*AUTHORITY_CHAIN, authority_ref],
            "provenance_refs": provenance_refs,
            "activative_intelligence": activative,
            "external_skills_required": 0,
            "external_runtime_dependencies": [],
            "workflow_execution_performed": False,
            "production_eligible": False,
            "certified": False,
            "certification_state": "uncertified_nonproduction",
            "compatibility_status": "builder_contract_compatible_nonproduction",
            "lineage": [
                manifest_hash,
                authority_ref,
                *provenance_refs,
                *(
                    [str(category_binding["binding_hash"])]
                    if "binding_hash" in category_binding
                    else []
                ),
            ],
        }
        content_bytes = _canonical_json(content)
        digest = sha256(content_bytes).hexdigest()
        definition_id = f"atomic-harness-definition_{digest}"
        definition_hash = f"sha256:{digest}"
        payload_bytes = _canonical_json(
            {
                "artifact_type": "AtomicHarnessDefinition",
                "definition_id": definition_id,
                "definition_hash": definition_hash,
                "definition": content,
            }
        )
        result = cls(
            definition_id=definition_id,
            definition_hash=definition_hash,
            content_bytes=content_bytes,
            payload_bytes=payload_bytes,
        )
        result.validate()
        return result

    @classmethod
    def from_payload_bytes(cls, payload: bytes) -> "PortableAtomicHarnessDefinition":
        try:
            root = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PortableDefinitionInvalid("Definition payload is not canonical JSON.") from error
        if not isinstance(root, dict) or set(root) != {
            "artifact_type", "definition_id", "definition_hash", "definition"
        }:
            raise PortableDefinitionInvalid("Definition payload envelope is invalid.")
        content_bytes = _canonical_json(root["definition"])
        result = cls(
            definition_id=str(root["definition_id"]),
            definition_hash=str(root["definition_hash"]),
            content_bytes=content_bytes,
            payload_bytes=payload,
        )
        result.validate()
        return result

    @property
    def content(self) -> Mapping[str, object]:
        value = json.loads(self.content_bytes.decode("utf-8"))
        assert isinstance(value, dict)
        return value

    def validate(self) -> None:
        digest = sha256(self.content_bytes).hexdigest()
        content = self.content
        expected_payload = _canonical_json(
            {
                "artifact_type": "AtomicHarnessDefinition",
                "definition_id": self.definition_id,
                "definition_hash": self.definition_hash,
                "definition": content,
            }
        )
        mode = content.get("mode")
        activative = content.get("activative_intelligence")
        category_binding = content.get("category_binding")
        required = {
            "schema_id", "schema_version", "compiler_id", "compiler_version",
            "amendment", "manifest_id", "manifest_version", "manifest_hash",
            "task_id", "mode", "classification", "category_binding", "atomic_boundary", "goal",
            "success_condition", "input_contract", "output_contract",
            "minimum_complete_context", "capability_requirements", "acceptance_tests",
            "execution_plan", "authority_chain", "provenance_refs",
            "activative_intelligence", "external_skills_required",
            "external_runtime_dependencies", "workflow_execution_performed",
            "production_eligible", "certified", "certification_state",
            "compatibility_status", "lineage",
        }
        if (
            set(content) != required
            or content.get("schema_id") != DEFINITION_SCHEMA
            or content.get("compiler_id") != COMPILER_ID
            or content.get("amendment") != "PX-AM-001"
            or mode not in {"generic", "activative"}
            or (mode == "generic" and activative is not None)
            or (mode == "activative" and not isinstance(activative, dict))
            or not _valid_category_binding(mode, category_binding)
            or content.get("execution_plan") != list(EXECUTION_PLAN)
            or content.get("external_skills_required") != 0
            or content.get("external_runtime_dependencies") != []
            or content.get("workflow_execution_performed") is not False
            or content.get("production_eligible") is not False
            or content.get("certified") is not False
            or content.get("certification_state") != "uncertified_nonproduction"
            or self.definition_id != f"atomic-harness-definition_{digest}"
            or self.definition_hash != f"sha256:{digest}"
            or self.payload_bytes != expected_payload
        ):
            raise PortableDefinitionInvalid(
                "AtomicHarnessDefinition identity or governed semantics are invalid."
            )
        serialized = self.payload_bytes.decode("utf-8")
        if "\\" in serialized or ":/" in serialized.lower():
            raise PortableDefinitionInvalid("Definition contains a machine-local path.")


def _valid_category_binding(mode: object, value: object) -> bool:
    if not isinstance(value, dict):
        return False
    if mode == "generic":
        return value == {
            "applicability": "NOT_APPLICABLE",
            "basis": "GENERIC_NON_ACTIVATIVE_TASK",
            "category_id": None,
        }
    required = {
        "harness_id",
        "harness_version",
        "applicability",
        "category_id",
        "category_name",
        "category_registry_version",
        "category_registry_hash",
        "constitutional_authority_ref",
        "runtime_law",
        "harness_development_law",
        "semantic_lineage_refs",
        "wrong_reading_locks",
        "not_applicable_basis",
        "certification_state",
        "production_ready",
        "certified",
        "binding_hash",
    }
    return (
        set(value) == required
        and value.get("applicability") == "REQUIRED"
        and isinstance(value.get("category_id"), str)
        and value.get("runtime_law") == "Activation First"
        and value.get("harness_development_law") == "Visual Syntax First"
        and isinstance(value.get("semantic_lineage_refs"), list)
        and len(value["semantic_lineage_refs"]) >= 8
        and isinstance(value.get("wrong_reading_locks"), list)
        and bool(value["wrong_reading_locks"])
        and value.get("certification_state") == "STRUCTURAL_UNCERTIFIED"
        and value.get("production_ready") is False
        and value.get("certified") is False
    )


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
