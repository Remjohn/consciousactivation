from __future__ import annotations

from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

from .domain.errors import PipelineAuthorityError, PipelineNotFound, PipelineValidationError
from .domain.validation import reject_noncanonical, require_ref, require_string, require_string_list

_SKILL_STATES = {"PROPOSED", "VALIDATED", "SHADOW", "PRODUCTION", "DEPRECATED", "RETIRED"}
_RECIPE_STATES = {"PROPOSED", "EXPERIMENTAL", "VALIDATED", "SHADOW", "PRODUCTION", "DEPRECATED", "RETIRED"}


def _refs(value: Sequence[Mapping[str, Any]], field: str) -> list[dict[str, str]]:
    refs = [require_ref(item, f"{field}[{index}]") for index, item in enumerate(value)]
    refs.sort(key=lambda item: item["object_id"])
    if len({item["object_id"] for item in refs}) != len(refs):
        raise PipelineValidationError(f"{field} contains duplicate refs")
    return refs


class SkillRegistry:
    def __init__(self, repository):
        self.repository = repository

    def register_skill(self, payload: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        required = {
            "skill_id", "version", "title", "purpose", "authority_owner", "lifecycle_state",
            "category_ids", "format_profile_ids", "entry_condition_ids", "output_contract_ids",
            "allowed_tool_ids", "forbidden_action_ids", "invariant_locks", "recipe_family_ids",
            "source_refs", "evaluation_profile_refs",
        }
        missing = sorted(required - set(payload)); unknown = sorted(set(payload) - required)
        if missing or unknown: raise PipelineValidationError(f"skill fields invalid; missing={missing}, unknown={unknown}")
        state = require_string(payload["lifecycle_state"], "lifecycle_state")
        if state not in _SKILL_STATES: raise PipelineValidationError("unknown skill lifecycle state")
        normalized = {
            "skill_id": require_string(payload["skill_id"], "skill_id"),
            "version": require_string(payload["version"], "version"),
            "title": require_string(payload["title"], "title"),
            "purpose": require_string(payload["purpose"], "purpose"),
            "authority_owner": require_string(payload["authority_owner"], "authority_owner"),
            "lifecycle_state": state,
            "category_ids": sorted(require_string_list(list(payload["category_ids"]), "category_ids", sorted_unique=False)),
            "format_profile_ids": sorted(require_string_list(list(payload["format_profile_ids"]), "format_profile_ids", sorted_unique=False)),
            "entry_condition_ids": sorted(require_string_list(list(payload["entry_condition_ids"]), "entry_condition_ids", sorted_unique=False)),
            "output_contract_ids": sorted(require_string_list(list(payload["output_contract_ids"]), "output_contract_ids", sorted_unique=False)),
            "allowed_tool_ids": sorted(require_string_list(list(payload["allowed_tool_ids"]), "allowed_tool_ids", sorted_unique=False)),
            "forbidden_action_ids": sorted(require_string_list(list(payload["forbidden_action_ids"]), "forbidden_action_ids", sorted_unique=False)),
            "invariant_locks": sorted(require_string_list(list(payload["invariant_locks"]), "invariant_locks", sorted_unique=False)),
            "recipe_family_ids": sorted(require_string_list(list(payload["recipe_family_ids"]), "recipe_family_ids", sorted_unique=False)),
            "source_refs": _refs(payload["source_refs"], "source_refs"),
            "evaluation_profile_refs": _refs(payload["evaluation_profile_refs"], "evaluation_profile_refs"),
        }
        reject_noncanonical(normalized)
        return self.repository.store_object("canonical_skill", normalized, object_id=normalized["skill_id"], idempotency_key=idempotency_key, lifecycle_state=state)

    def register_recipe(self, payload: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        required = {
            "recipe_id", "version", "skill_id", "recipe_family_id", "lifecycle_state",
            "primitive_coalition_ref", "coalition_signature_ref", "edge_product_ref", "category_ids",
            "format_profile_ids", "failure_codes", "applicability_tags", "protected_properties",
            "operations", "evidence_refs", "control_comparison_refs", "regression_case_refs", "limitations",
        }
        missing = sorted(required - set(payload)); unknown = sorted(set(payload) - required)
        if missing or unknown: raise PipelineValidationError(f"recipe fields invalid; missing={missing}, unknown={unknown}")
        state = require_string(payload["lifecycle_state"], "lifecycle_state")
        if state not in _RECIPE_STATES: raise PipelineValidationError("unknown recipe lifecycle state")
        if state == "PRODUCTION":
            raise PipelineAuthorityError("development runtime cannot promote a Steering Recipe to production")
        operations=[]
        for index, operation in enumerate(payload["operations"]):
            if set(operation) != {"tool_id", "tool_version", "arguments", "preconditions", "expected_effect"}:
                raise PipelineValidationError(f"operations[{index}] has invalid fields")
            normalized_op={
                "tool_id": require_string(operation["tool_id"], "tool_id"),
                "tool_version": require_string(operation["tool_version"], "tool_version"),
                "arguments": dict(operation["arguments"]),
                "preconditions": sorted(require_string_list(list(operation["preconditions"]), "preconditions", sorted_unique=False)),
                "expected_effect": require_string(operation["expected_effect"], "expected_effect"),
            }
            reject_noncanonical(normalized_op); operations.append(normalized_op)
        normalized={
            "recipe_id":require_string(payload["recipe_id"],"recipe_id"),
            "version":require_string(payload["version"],"version"),
            "skill_id":require_string(payload["skill_id"],"skill_id"),
            "recipe_family_id":require_string(payload["recipe_family_id"],"recipe_family_id"),
            "lifecycle_state":state,
            "primitive_coalition_ref":require_ref(payload["primitive_coalition_ref"],"primitive_coalition_ref"),
            "coalition_signature_ref":require_ref(payload["coalition_signature_ref"],"coalition_signature_ref"),
            "edge_product_ref":require_ref(payload["edge_product_ref"],"edge_product_ref"),
            "category_ids":sorted(require_string_list(list(payload["category_ids"]),"category_ids",sorted_unique=False)),
            "format_profile_ids":sorted(require_string_list(list(payload["format_profile_ids"]),"format_profile_ids",sorted_unique=False)),
            "failure_codes":sorted(require_string_list(list(payload["failure_codes"]),"failure_codes",sorted_unique=False)),
            "applicability_tags":sorted(require_string_list(list(payload["applicability_tags"]),"applicability_tags",sorted_unique=False)),
            "protected_properties":sorted(require_string_list(list(payload["protected_properties"]),"protected_properties",sorted_unique=False)),
            "operations":operations,
            "evidence_refs":_refs(payload["evidence_refs"],"evidence_refs"),
            "control_comparison_refs":_refs(payload["control_comparison_refs"],"control_comparison_refs"),
            "regression_case_refs":_refs(payload["regression_case_refs"],"regression_case_refs"),
            "limitations":sorted(require_string_list(list(payload["limitations"]),"limitations",sorted_unique=False)),
        }
        reject_noncanonical(normalized)
        skill=self.repository.get_object(normalized["skill_id"])
        if skill["object_type"] != "canonical_skill": raise PipelineValidationError("recipe skill_id does not identify a canonical skill")
        return self.repository.store_object("steering_recipe", normalized, object_id=normalized["recipe_id"], idempotency_key=idempotency_key, lifecycle_state=state)

    def register_transformation_contract(self, payload: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        required={"contract_id","version","input_contract_ids","output_contract_ids","required_invariants","allowed_transformation_classes","forbidden_transformations","evaluation_profile_refs","source_refs"}
        missing=sorted(required-set(payload)); unknown=sorted(set(payload)-required)
        if missing or unknown: raise PipelineValidationError(f"transformation contract fields invalid; missing={missing}, unknown={unknown}")
        normalized={
            "contract_id":require_string(payload["contract_id"],"contract_id"),
            "version":require_string(payload["version"],"version"),
            "input_contract_ids":sorted(require_string_list(list(payload["input_contract_ids"]),"input_contract_ids",sorted_unique=False)),
            "output_contract_ids":sorted(require_string_list(list(payload["output_contract_ids"]),"output_contract_ids",sorted_unique=False)),
            "required_invariants":sorted(require_string_list(list(payload["required_invariants"]),"required_invariants",sorted_unique=False)),
            "allowed_transformation_classes":sorted(require_string_list(list(payload["allowed_transformation_classes"]),"allowed_transformation_classes",sorted_unique=False)),
            "forbidden_transformations":sorted(require_string_list(list(payload["forbidden_transformations"]),"forbidden_transformations",sorted_unique=False)),
            "evaluation_profile_refs":_refs(payload["evaluation_profile_refs"],"evaluation_profile_refs"),
            "source_refs":_refs(payload["source_refs"],"source_refs"),
        }
        reject_noncanonical(normalized)
        return self.repository.store_object("transformation_contract",normalized,object_id=normalized["contract_id"],idempotency_key=idempotency_key,lifecycle_state="VALIDATED")

    def resolve(self, *, skill_id: str, category_id: str, format_profile_id: str, failure_codes: Sequence[str], applicability_tags: Sequence[str], idempotency_key: str) -> dict[str, Any]:
        skill=self.repository.get_object(skill_id)
        if skill["object_type"] != "canonical_skill": raise PipelineNotFound(f"canonical skill not found: {skill_id}")
        sp=skill["payload"]
        if sp["category_ids"] and category_id not in sp["category_ids"]: raise PipelineValidationError("skill category mismatch")
        if sp["format_profile_ids"] and format_profile_id not in sp["format_profile_ids"]: raise PipelineValidationError("skill format mismatch")
        failures=set(failure_codes); tags=set(applicability_tags)
        candidates=[]
        for item in self.repository.list_objects(object_type="steering_recipe"):
            rp=item["payload"]
            if rp["skill_id"] != skill_id or rp["lifecycle_state"] not in {"VALIDATED","SHADOW","EXPERIMENTAL"}: continue
            if rp["category_ids"] and category_id not in rp["category_ids"]: continue
            if rp["format_profile_ids"] and format_profile_id not in rp["format_profile_ids"]: continue
            if rp["failure_codes"] and not set(rp["failure_codes"]).intersection(failures): continue
            if rp["applicability_tags"] and not set(rp["applicability_tags"]).issubset(tags): continue
            score=(2_000_000 if rp["lifecycle_state"]=="VALIDATED" else 1_000_000)+len(rp["evidence_refs"])*100_000+len(rp["control_comparison_refs"])*200_000
            candidates.append((score,rp["recipe_id"],rp))
        candidates.sort(key=lambda row:(-row[0],row[1]))
        selected=[row[2] for row in candidates[:3]]
        payload={
            "resolution_id":f"skill-resolution:{canonical_sha256({'skill_id':skill_id,'category_id':category_id,'format_profile_id':format_profile_id,'failure_codes':sorted(failures),'tags':sorted(tags),'recipes':[r['recipe_id'] for r in selected]})}",
            "skill_ref":{"object_id":skill["object_id"],"version":skill["semantic_version"],"sha256":skill["canonical_sha256"]},
            "selected_recipe_ids":[item["recipe_id"] for item in selected],
            "allowed_tool_ids":sp["allowed_tool_ids"],
            "forbidden_action_ids":sp["forbidden_action_ids"],
            "invariant_locks":sp["invariant_locks"],
            "category_id":category_id,
            "format_profile_id":format_profile_id,
            "failure_codes":sorted(failures),
            "applicability_tags":sorted(tags),
            "result":"PASS" if selected else "PASS_NO_RECIPE_REQUIRED",
        }
        payload["resolution_sha256"]=canonical_sha256(payload)
        return self.repository.store_object("skill_resolution",payload,object_id=payload["resolution_id"],idempotency_key=idempotency_key,lifecycle_state="ACTIVE")
