from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Sequence

from ca_contracts import canonical_json_bytes, canonical_sha256

from .domain.errors import PipelineBudgetError, PipelineValidationError
from .domain.validation import reject_noncanonical, require_int, require_ref, require_string, require_string_list

_TOKEN = re.compile(r"[A-Za-z0-9_:-]+")
_ALLOWED_AUTHORITY = {"current", "candidate_not_current"}
_ALLOWED_LIFECYCLE = {"ACTIVE", "VALIDATED", "APPROVED", "SHADOW", "EXPERIMENTAL"}
_ALLOWED_SOURCE_KINDS = {
    "program_control",
    "air_semantic",
    "interview_expression",
    "pipeline_execution",
    "visual_asset",
    "human_resolution",
    "skill",
    "steering_recipe",
    "failure_precedent",
    "implementation",
}


def _tokens(value: str) -> set[str]:
    return {token.lower() for token in _TOKEN.findall(value)}


def _sorted_refs(value: Sequence[Mapping[str, Any]], field: str) -> list[dict[str, str]]:
    refs = [require_ref(item, f"{field}[{index}]") for index, item in enumerate(value)]
    refs.sort(key=lambda item: item["object_id"])
    if len({item["object_id"] for item in refs}) != len(refs):
        raise PipelineValidationError(f"{field} contains duplicate object IDs")
    return refs


def validate_projection(payload: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "projection_id", "object_ref", "source_kind", "authority_state", "lifecycle_state",
        "title", "summary", "category_ids", "format_profile_ids", "role_ids", "tags",
        "relationship_edges", "evidence_refs", "reaction_receipt_refs", "expression_moment_refs",
        "contradicts_ids", "supersedes_ids", "failed_alternative", "evidence_quality_micros",
        "permitted_action_ids", "content_sha256",
    }
    unknown = sorted(set(payload) - required)
    missing = sorted(required - set(payload))
    if missing or unknown:
        raise PipelineValidationError(f"knowledge projection fields invalid; missing={missing}, unknown={unknown}")
    projection_id = require_string(payload["projection_id"], "projection_id")
    source_kind = require_string(payload["source_kind"], "source_kind")
    if source_kind not in _ALLOWED_SOURCE_KINDS:
        raise PipelineValidationError("RET-SOURCE-KIND-UNKNOWN")
    authority_state = require_string(payload["authority_state"], "authority_state")
    lifecycle_state = require_string(payload["lifecycle_state"], "lifecycle_state")
    if authority_state not in _ALLOWED_AUTHORITY:
        raise PipelineValidationError("projection authority_state is not eligible")
    if lifecycle_state not in _ALLOWED_LIFECYCLE | {"SUPERSEDED", "REJECTED", "RETIRED"}:
        raise PipelineValidationError("projection lifecycle_state is unknown")
    if not isinstance(payload["failed_alternative"], bool):
        raise PipelineValidationError("failed_alternative must be boolean")
    evidence_quality = require_int(payload["evidence_quality_micros"], "evidence_quality_micros", minimum=0)
    if evidence_quality > 1_000_000:
        raise PipelineValidationError("evidence_quality_micros must be <= 1000000")
    result = {
        "projection_id": projection_id,
        "object_ref": require_ref(payload["object_ref"], "object_ref"),
        "source_kind": source_kind,
        "authority_state": authority_state,
        "lifecycle_state": lifecycle_state,
        "title": require_string(payload["title"], "title"),
        "summary": require_string(payload["summary"], "summary"),
        "category_ids": require_string_list(list(payload["category_ids"]), "category_ids", sorted_unique=False),
        "format_profile_ids": require_string_list(list(payload["format_profile_ids"]), "format_profile_ids", sorted_unique=False),
        "role_ids": require_string_list(list(payload["role_ids"]), "role_ids", sorted_unique=False),
        "tags": require_string_list(list(payload["tags"]), "tags", sorted_unique=False),
        "relationship_edges": sorted(
            [
                {
                    "relation_type": require_string(edge["relation_type"], "relationship_edges.relation_type"),
                    "target_id": require_string(edge["target_id"], "relationship_edges.target_id"),
                }
                for edge in payload["relationship_edges"]
            ],
            key=lambda item: (item["relation_type"], item["target_id"]),
        ),
        "evidence_refs": _sorted_refs(payload["evidence_refs"], "evidence_refs"),
        "reaction_receipt_refs": _sorted_refs(payload["reaction_receipt_refs"], "reaction_receipt_refs"),
        "expression_moment_refs": _sorted_refs(payload["expression_moment_refs"], "expression_moment_refs"),
        "contradicts_ids": sorted(require_string_list(list(payload["contradicts_ids"]), "contradicts_ids", sorted_unique=False)),
        "supersedes_ids": sorted(require_string_list(list(payload["supersedes_ids"]), "supersedes_ids", sorted_unique=False)),
        "failed_alternative": payload["failed_alternative"],
        "evidence_quality_micros": evidence_quality,
        "permitted_action_ids": sorted(require_string_list(list(payload["permitted_action_ids"]), "permitted_action_ids", sorted_unique=False)),
        "content_sha256": require_string(payload["content_sha256"], "content_sha256"),
    }
    if source_kind == "interview_expression" and (
        not result["reaction_receipt_refs"] or not result["expression_moment_refs"]
    ):
        raise PipelineValidationError("RET-PROVENANCE-INCOMPLETE")
    reject_noncanonical(result)
    return result


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    capsule: dict[str, Any]
    receipt: dict[str, Any]


class AuthorityFirstRetrievalService:
    """Deterministic authority-first retrieval and Minimum Complete Context compiler.

    Dense ranking is an optional advisory integer signal. Eligibility always runs before
    the dense adapter and the adapter receives eligible candidate IDs only.
    """

    def __init__(self, repository, dense_adapter: Callable[[str, Sequence[dict[str, Any]]], Mapping[str, int]] | None = None):
        self.repository = repository
        self.dense_adapter = dense_adapter

    def register_projection(self, payload: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        normalized = validate_projection(payload)
        return self.repository.store_object(
            "knowledge_projection",
            normalized,
            object_id=normalized["projection_id"],
            idempotency_key=idempotency_key,
            lifecycle_state=normalized["lifecycle_state"],
            authority_state=normalized["authority_state"],
        )

    @staticmethod
    def _eligible(item: Mapping[str, Any], request: Mapping[str, Any]) -> tuple[bool, list[str]]:
        reasons: list[str] = []
        if item["authority_state"] not in _ALLOWED_AUTHORITY:
            reasons.append("AUTHORITY_INELIGIBLE")
        if item["lifecycle_state"] not in _ALLOWED_LIFECYCLE:
            reasons.append("LIFECYCLE_INELIGIBLE")
        category_id = request.get("category_id")
        if category_id and item["category_ids"] and category_id not in item["category_ids"]:
            reasons.append("CATEGORY_MISMATCH")
        profile_id = request.get("format_profile_id")
        if profile_id and item["format_profile_ids"] and profile_id not in item["format_profile_ids"]:
            reasons.append("FORMAT_PROFILE_MISMATCH")
        role_id = request.get("role_id")
        if role_id and item["role_ids"] and role_id not in item["role_ids"]:
            reasons.append("ROLE_MISMATCH")
        required_source_kinds = set(request.get("required_source_kinds", []))
        if required_source_kinds and item["source_kind"] not in required_source_kinds:
            reasons.append("SOURCE_KIND_MISMATCH")
        required_tags = set(request.get("required_tags", []))
        if required_tags and not required_tags.issubset(set(item["tags"])):
            reasons.append("TAG_REQUIREMENT_UNSATISFIED")
        required_actions = set(request.get("required_action_ids", []))
        if required_actions and not required_actions.issubset(set(item["permitted_action_ids"])):
            reasons.append("ACTION_REQUIREMENT_UNSATISFIED")
        if item["source_kind"] == "interview_expression" and (
            not item["reaction_receipt_refs"] or not item["expression_moment_refs"]
        ):
            reasons.append("RET-PROVENANCE-INCOMPLETE")
        return (not reasons, reasons)

    @staticmethod
    def _score(query: str, item: Mapping[str, Any], dense_score: int) -> dict[str, int]:
        query_tokens = _tokens(query)
        title_tokens = _tokens(item["title"])
        summary_tokens = _tokens(item["summary"])
        tag_tokens = {token.lower() for token in item["tags"]}
        exact = 1_000_000 if query.lower() in item["title"].lower() else 0
        lexical = min(1_000_000, (len(query_tokens & (title_tokens | summary_tokens)) * 1_000_000) // max(1, len(query_tokens)))
        tag = min(1_000_000, (len(query_tokens & tag_tokens) * 1_000_000) // max(1, len(query_tokens)))
        graph = min(1_000_000, len(item["relationship_edges"]) * 100_000)
        evidence = int(item["evidence_quality_micros"])
        dense = max(0, min(1_000_000, int(dense_score)))
        total = exact * 5 + lexical * 4 + tag * 3 + graph + evidence * 2 + dense * 2
        return {
            "exact_micros": exact,
            "lexical_micros": lexical,
            "tag_micros": tag,
            "graph_micros": graph,
            "evidence_micros": evidence,
            "dense_micros": dense,
            "fused_score": total,
        }

    def compile_capsule(self, request: Mapping[str, Any], *, idempotency_key: str) -> RetrievalResult:
        required = {
            "request_id", "query_text", "role_id", "category_id", "format_profile_id",
            "required_source_kinds", "required_tags", "required_action_ids", "required_projection_ids",
            "include_contradictions", "include_failed_alternatives", "budget_bytes", "allowed_tool_ids",
            "forbidden_action_ids", "stopping_law_id", "source_package_ref",
        }
        missing = sorted(required - set(request))
        unknown = sorted(set(request) - required)
        if missing or unknown:
            raise PipelineValidationError(f"retrieval request fields invalid; missing={missing}, unknown={unknown}")
        query = require_string(request["query_text"], "query_text")
        budget = require_int(request["budget_bytes"], "budget_bytes", minimum=1)
        normalized_request = {
            "request_id": require_string(request["request_id"], "request_id"),
            "query_text": query,
            "role_id": require_string(request["role_id"], "role_id"),
            "category_id": require_string(request["category_id"], "category_id"),
            "format_profile_id": require_string(request["format_profile_id"], "format_profile_id"),
            "required_source_kinds": sorted(require_string_list(list(request["required_source_kinds"]), "required_source_kinds", sorted_unique=False)),
            "required_tags": sorted(require_string_list(list(request["required_tags"]), "required_tags", sorted_unique=False)),
            "required_action_ids": sorted(require_string_list(list(request["required_action_ids"]), "required_action_ids", sorted_unique=False)),
            "required_projection_ids": sorted(require_string_list(list(request["required_projection_ids"]), "required_projection_ids", sorted_unique=False)),
            "include_contradictions": bool(request["include_contradictions"]),
            "include_failed_alternatives": bool(request["include_failed_alternatives"]),
            "budget_bytes": budget,
            "allowed_tool_ids": sorted(require_string_list(list(request["allowed_tool_ids"]), "allowed_tool_ids", sorted_unique=False)),
            "forbidden_action_ids": sorted(require_string_list(list(request["forbidden_action_ids"]), "forbidden_action_ids", sorted_unique=False)),
            "stopping_law_id": require_string(request["stopping_law_id"], "stopping_law_id"),
            "source_package_ref": require_ref(request["source_package_ref"], "source_package_ref"),
        }
        reject_noncanonical(normalized_request)
        stored = self.repository.list_objects(object_type="knowledge_projection")
        projections = [validate_projection(item["payload"]) for item in stored]
        eligible: list[dict[str, Any]] = []
        exclusions: list[dict[str, Any]] = []
        for item in projections:
            accepted, reasons = self._eligible(item, normalized_request)
            if accepted:
                eligible.append(item)
            else:
                exclusions.append({"projection_id": item["projection_id"], "reason_codes": sorted(reasons)})
        eligible_ids = {item["projection_id"] for item in eligible}
        for required_id in normalized_request["required_projection_ids"]:
            if required_id not in eligible_ids:
                raise PipelineValidationError(f"required projection is unavailable or ineligible: {required_id}")
        dense_scores: Mapping[str, int] = {}
        if self.dense_adapter:
            dense_scores = self.dense_adapter(query, tuple(sorted(eligible, key=lambda item: item["projection_id"])))
            if set(dense_scores) - eligible_ids:
                raise PipelineValidationError("RET-INELIGIBLE-RANKED")
        ranked: list[dict[str, Any]] = []
        for item in eligible:
            scores = self._score(query, item, int(dense_scores.get(item["projection_id"], 0)))
            ranked.append({"projection": item, "scores": scores})
        ranked.sort(key=lambda row: (-row["scores"]["fused_score"], row["projection"]["projection_id"]))

        by_id = {row["projection"]["projection_id"]: row for row in ranked}
        selected_ids: list[str] = []
        for required_id in normalized_request["required_projection_ids"]:
            if required_id not in selected_ids:
                selected_ids.append(required_id)
        for kind in normalized_request["required_source_kinds"]:
            match = next((row for row in ranked if row["projection"]["source_kind"] == kind), None)
            if match and match["projection"]["projection_id"] not in selected_ids:
                selected_ids.append(match["projection"]["projection_id"])
        if not selected_ids and ranked:
            selected_ids.append(ranked[0]["projection"]["projection_id"])
        if normalized_request["include_failed_alternatives"]:
            failed = next((row for row in ranked if row["projection"]["failed_alternative"]), None)
            if failed and failed["projection"]["projection_id"] not in selected_ids:
                selected_ids.append(failed["projection"]["projection_id"])
        if normalized_request["include_contradictions"]:
            contradiction_targets: set[str] = set()
            for selected_id in list(selected_ids):
                contradiction_targets.update(by_id[selected_id]["projection"]["contradicts_ids"])
            for target in sorted(contradiction_targets):
                if target in by_id and target not in selected_ids:
                    selected_ids.append(target)
            if selected_ids and not any(by_id[item]["projection"]["contradicts_ids"] for item in selected_ids):
                raise PipelineValidationError("RET-CONTRADICTION-MISSING")

        selected = [by_id[item]["projection"] for item in selected_ids]
        coverage = {
            "required_projection_ids": normalized_request["required_projection_ids"],
            "covered_source_kinds": sorted({item["source_kind"] for item in selected}),
            "contradiction_coverage": normalized_request["include_contradictions"],
            "failed_alternative_coverage": any(item["failed_alternative"] for item in selected),
        }
        capsule_without_hash = {
            "capsule_id": f"jit-capsule:{canonical_sha256({'request': normalized_request, 'selected_ids': selected_ids})}",
            "capsule_version": "1.0.0",
            "request_id": normalized_request["request_id"],
            "role_id": normalized_request["role_id"],
            "source_package_ref": normalized_request["source_package_ref"],
            "selected_items": selected,
            "coverage_proof": coverage,
            "allowed_tool_ids": normalized_request["allowed_tool_ids"],
            "forbidden_action_ids": normalized_request["forbidden_action_ids"],
            "stopping_law_id": normalized_request["stopping_law_id"],
            "authority_first": True,
            "dense_adapter_used": self.dense_adapter is not None,
            "minimum_complete_context": True,
        }
        encoded = canonical_json_bytes(capsule_without_hash)
        if len(encoded) > budget:
            raise PipelineBudgetError(
                f"RET-BUDGET-UNSATISFIABLE: required={len(encoded)}, budget={budget}, selected={selected_ids}"
            )
        capsule = {**capsule_without_hash, "capsule_sha256": canonical_sha256(capsule_without_hash), "encoded_bytes": len(encoded)}
        rank_snapshot = [
            {"projection_id": row["projection"]["projection_id"], **row["scores"]}
            for row in ranked
        ]
        receipt_without_hash = {
            "receipt_id": f"retrieval-receipt:{canonical_sha256({'request': normalized_request, 'capsule_sha256': capsule['capsule_sha256']})}",
            "request": normalized_request,
            "eligible_candidate_ids": sorted(eligible_ids),
            "exclusions": sorted(exclusions, key=lambda item: item["projection_id"]),
            "rank_snapshot": rank_snapshot,
            "selected_projection_ids": selected_ids,
            "capsule_ref": {"object_id": capsule["capsule_id"], "version": "1.0.0", "sha256": capsule["capsule_sha256"]},
            "result": "PASS",
        }
        receipt = {**receipt_without_hash, "receipt_sha256": canonical_sha256(receipt_without_hash)}
        self.repository.store_object("jit_execution_capsule_v2", capsule, object_id=capsule["capsule_id"], idempotency_key=f"{idempotency_key}:capsule", lifecycle_state="ACTIVE")
        self.repository.store_object("retrieval_receipt", receipt, object_id=receipt["receipt_id"], idempotency_key=f"{idempotency_key}:receipt", lifecycle_state="PASS")
        return RetrievalResult(capsule=capsule, receipt=receipt)
