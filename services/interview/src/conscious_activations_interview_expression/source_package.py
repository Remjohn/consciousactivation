from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .canonical import immutable_ref, require_enum, require_ref, require_string, semantic_id
from .domain import ADMISSION_MODES, SOURCE_KINDS, component_slot, validate_planning_lineage
from .errors import StateError, ValidationError
from .repository import InterviewRepository

COMPONENT_NAMES = ["transcript_alignment", "packed_phrase_transcript", "visual_structure_index", "reaction_receipts", "expression_moments", "asset_package_spec", "observed_evidence_pack"]


class SourcePackageService:
    def __init__(self, repository: InterviewRepository):
        self.repository = repository

    def admit(self, command: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        required = {"workspace_id", "project_id", "admission_mode", "source_kind", "media_assets", "source_authority", "planning_lineage"}
        if set(command) != required:
            raise ValidationError("source admission command contains unknown or missing fields")
        mode = require_enum(command["admission_mode"], ADMISSION_MODES, "admission_mode")
        kind = require_enum(command["source_kind"], SOURCE_KINDS, "source_kind")
        media = command["media_assets"]
        if not isinstance(media, list) or not media:
            raise ValidationError("media_assets must be non-empty")
        for item in media:
            if not isinstance(item, Mapping) or not item.get("asset_id") or not item.get("sha256"):
                raise ValidationError("media asset is not admitted")
        authority = command["source_authority"]
        if not isinstance(authority, Mapping) or set(authority) != {"operator_id", "authority_scope", "assertion_id"}:
            raise ValidationError("source_authority has invalid shape")
        planning = validate_planning_lineage(mode, command["planning_lineage"])
        core = {
            "workspace_id": require_string(command["workspace_id"], "workspace_id"),
            "project_id": require_string(command["project_id"], "project_id"),
            "admission_mode": mode,
            "source_kind": kind,
            "media_assets": sorted([dict(item) for item in media], key=lambda x: x["asset_id"]),
            "source_authority": {k: require_string(authority[k], f"source_authority.{k}") for k in sorted(authority)},
            "planning_lineage": planning,
        }
        package_id = semantic_id("ie:source-package", core)
        components = {name: component_slot(state="PENDING_REQUIRED_COMPONENT", reason="AWAITING_COMPONENT") for name in COMPONENT_NAMES}
        package = {"package_id": package_id, "package_version": "1.0.0", **core, "components": components, "tag_assertion_refs": [], "lifecycle_state": "ADMITTED", "derivative_eligible": False, "production_authorized": False, "certified": False}
        result = self.repository.store_object("canonical_interview_source_package", package, object_id=package_id, idempotency_key=idempotency_key, lifecycle_state="ADMITTED")
        for asset in media:
            self.repository.add_edge(asset["asset_id"], package_id, "media_source_of")
        return result

    def bind_component(self, package_id: str, component_name: str, component_ref: Mapping[str, Any], *, idempotency_key: str, expected_revision: int | None = None) -> dict[str, Any]:
        if component_name not in COMPONENT_NAMES:
            raise ValidationError("unknown component slot")
        current = self.repository.get_object(package_id)
        package = dict(current["payload"])
        package["components"] = {k: dict(v) for k, v in package["components"].items()}
        package["components"][component_name] = component_slot(state="BOUND", ref=component_ref)
        package["lifecycle_state"] = "COMPONENTS_IN_PROGRESS"
        package["derivative_eligible"] = False
        result = self.repository.store_object("canonical_interview_source_package", package, object_id=package_id, idempotency_key=idempotency_key, lifecycle_state=package["lifecycle_state"], expected_revision=expected_revision)
        self.repository.add_edge(component_ref["object_id"], package_id, f"bound_{component_name}")
        return result

    def mark_not_applicable(self, package_id: str, component_name: str, reason: str, *, idempotency_key: str) -> dict[str, Any]:
        if component_name not in COMPONENT_NAMES:
            raise ValidationError("unknown component slot")
        current = self.repository.get_object(package_id)
        package = dict(current["payload"]); package["components"] = {k: dict(v) for k,v in package["components"].items()}
        if package["source_kind"] == "INTERVIEW_EXPRESSION" and component_name in {"reaction_receipts", "expression_moments"}:
            raise ValidationError("required interview-expression component cannot be NOT_APPLICABLE")
        package["components"][component_name] = component_slot(state="NOT_APPLICABLE", reason=reason)
        return self.repository.store_object("canonical_interview_source_package", package, object_id=package_id, idempotency_key=idempotency_key, lifecycle_state=package["lifecycle_state"])

    def publish(self, package_id: str, *, archive_only: bool, idempotency_key: str) -> dict[str, Any]:
        current = self.repository.get_object(package_id)
        package = dict(current["payload"])
        components = package["components"]
        reaction_bound = components["reaction_receipts"]["state"] == "BOUND"
        moment_bound = components["expression_moments"]["state"] == "BOUND"
        if archive_only:
            package["lifecycle_state"] = "ARCHIVE_ACCEPTED"
            package["derivative_eligible"] = False
        else:
            if package["source_kind"] == "INTERVIEW_EXPRESSION" and not (reaction_bound and moment_bound):
                raise StateError("publication requires Reaction Receipt and Expression Moment refs")
            package["lifecycle_state"] = "PUBLISHED_DERIVATIVE_ELIGIBLE"
            package["derivative_eligible"] = True
        return self.repository.store_object("canonical_interview_source_package", package, object_id=package_id, idempotency_key=idempotency_key, lifecycle_state=package["lifecycle_state"], expected_revision=current["revision"])

    def invalidate_component(self, package_id: str, component_name: str, reason: str, *, idempotency_key: str) -> dict[str, Any]:
        current = self.repository.get_object(package_id)
        package = dict(current["payload"]); package["components"] = {k: dict(v) for k,v in package["components"].items()}
        slot = package["components"].get(component_name)
        if not slot or slot["state"] != "BOUND":
            raise StateError("only a bound component may be invalidated")
        invalidated_ref = slot["ref"]
        package["components"][component_name] = component_slot(state="INVALIDATED", reason=reason)
        package["lifecycle_state"] = "COMPONENTS_IN_PROGRESS"; package["derivative_eligible"] = False
        result = self.repository.store_object("canonical_interview_source_package", package, object_id=package_id, idempotency_key=idempotency_key, lifecycle_state=package["lifecycle_state"], expected_revision=current["revision"])
        return {**result, "invalidated_ref": invalidated_ref, "descendants": self.repository.descendants(invalidated_ref["object_id"])}

    @staticmethod
    def ref(stored: Mapping[str, Any]) -> dict[str, str]:
        obj=stored["object"] if "object" in stored else stored
        return {"object_id": obj["object_id"], "version": obj["version"], "sha256": obj["sha256"]}
