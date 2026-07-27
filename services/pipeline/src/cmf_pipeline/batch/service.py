from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import (
    reject_noncanonical,
    require_int,
    require_ref,
    require_string,
    require_string_list,
    semantic_identity,
)
from ..workflow.infrastructure.repository import PipelineRepository


class ContentBatchService:
    DERIVATIVE_TYPES = {
        "SOURCE_LED_SHORT",
        "CAROUSEL",
        "SUPERVISUAL",
        "ANIMATION_SCENE_PACKAGE",
        "ANIMATION_SHORT",
    }

    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def compile_batch(
        self,
        request: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        required = {
            "source_package_ref",
            "observed_activative_pack_ref",
            "harness_binding_ref",
            "brand_context_ref",
            "routes",
            "shared_analysis_refs",
            "campaign_id",
        }
        if set(request) != required:
            raise PipelineValidationError("content batch request contains unknown or missing fields")
        source_ref = require_ref(request["source_package_ref"], "source_package_ref")
        observed_ref = require_ref(request["observed_activative_pack_ref"], "observed_activative_pack_ref")
        harness_ref = require_ref(request["harness_binding_ref"], "harness_binding_ref")
        brand_ref = require_ref(request["brand_context_ref"], "brand_context_ref")
        shared_analysis = [require_ref(item, f"shared_analysis_refs[{index}]") for index, item in enumerate(request["shared_analysis_refs"])]
        if [item["object_id"] for item in shared_analysis] != sorted(item["object_id"] for item in shared_analysis):
            raise PipelineValidationError("shared_analysis_refs must be sorted")
        routes = request["routes"]
        if not isinstance(routes, list) or not routes:
            raise PipelineValidationError("routes must be a non-empty list")
        jobs = [self._compile_job(item, index, source_ref, harness_ref) for index, item in enumerate(routes)]
        job_ids = [item["job_id"] for item in jobs]
        if len(job_ids) != len(set(job_ids)):
            raise PipelineValidationError("derivative jobs must be unique")
        jobs.sort(key=lambda item: (item["priority"], item["derivative_type"], item["job_id"]))
        core = {
            "campaign_id": require_string(request["campaign_id"], "campaign_id"),
            "source_package_ref": source_ref,
            "observed_activative_pack_ref": observed_ref,
            "harness_binding_ref": harness_ref,
            "brand_context_ref": brand_ref,
            "shared_analysis_refs": shared_analysis,
            "jobs": jobs,
            "state": "COMPILED",
            "semantic_values_owned_by_pipeline": False,
            "production_authorized": False,
        }
        batch = {
            "batch_id": semantic_identity("content-batch", core),
            "batch_version": "1.0.0",
            **core,
        }
        result = self.repository.store_object(
            "source_backed_content_batch",
            batch,
            idempotency_key=idempotency_key,
            object_id=batch["batch_id"],
            lifecycle_state="COMPILED",
        )
        self.repository.add_edge(source_ref["object_id"], batch["batch_id"], "source_of_batch")
        self.repository.add_edge(observed_ref["object_id"], batch["batch_id"], "observed_activation_input")
        self.repository.add_edge(harness_ref["object_id"], batch["batch_id"], "execution_binding")
        self.repository.add_edge(brand_ref["object_id"], batch["batch_id"], "brand_context_input")
        for job in jobs:
            self.repository.store_object(
                "derivative_job",
                job,
                idempotency_key=f"{idempotency_key}:job:{job['job_id']}",
                object_id=job["job_id"],
                lifecycle_state="PENDING",
            )
            self.repository.add_edge(batch["batch_id"], job["job_id"], "contains_derivative_job")
            self.repository.add_edge(job["semantic_program_ref"]["object_id"], job["job_id"], "semantic_program_input")
            self.repository.add_edge(job["final_script_ref"]["object_id"], job["job_id"], "approved_final_script_input")
            self.repository.add_edge(job["activation_transfer_contract_ref"]["object_id"], job["job_id"], "activation_transfer_input")
        return result

    def _compile_job(
        self,
        route: Any,
        index: int,
        source_ref: Mapping[str, str],
        harness_ref: Mapping[str, str],
    ) -> dict[str, Any]:
        required = {
            "route_id",
            "derivative_type",
            "semantic_program_ref",
            "final_script_ref",
            "archetype_coalition_ref",
            "primitive_coalition_ref",
            "activation_transfer_contract_ref",
            "source_spans",
            "animation_scene_package_ref",
            "priority",
            "not_applicable_reason",
        }
        if not isinstance(route, Mapping) or set(route) != required:
            raise PipelineValidationError(f"routes[{index}] contains unknown or missing fields")
        derivative_type = require_string(route["derivative_type"], f"routes[{index}].derivative_type")
        if derivative_type not in self.DERIVATIVE_TYPES:
            raise PipelineValidationError(f"routes[{index}] has unsupported derivative type")
        route_id = require_string(route["route_id"], f"routes[{index}].route_id")
        if "format02" in route_id.lower() or "format02" in derivative_type.lower():
            raise PipelineValidationError("Format 02 remains deferred")
        semantic_ref = require_ref(route["semantic_program_ref"], f"routes[{index}].semantic_program_ref")
        final_ref = require_ref(route["final_script_ref"], f"routes[{index}].final_script_ref")
        archetype_ref = require_ref(route["archetype_coalition_ref"], f"routes[{index}].archetype_coalition_ref")
        primitive_ref = require_ref(route["primitive_coalition_ref"], f"routes[{index}].primitive_coalition_ref")
        transfer_ref = require_ref(route["activation_transfer_contract_ref"], f"routes[{index}].activation_transfer_contract_ref")
        source_spans = self._source_spans(route["source_spans"], index, source_ref)
        animation_ref: dict[str, str] | str
        if route["animation_scene_package_ref"] == "NOT_APPLICABLE":
            animation_ref = "NOT_APPLICABLE"
        else:
            animation_ref = require_ref(route["animation_scene_package_ref"], f"routes[{index}].animation_scene_package_ref")
        if animation_ref == "NOT_APPLICABLE" and derivative_type in {"ANIMATION_SCENE_PACKAGE", "ANIMATION_SHORT"}:
            raise PipelineValidationError("animation derivative requires animation_scene_package_ref")
        not_applicable_reason = route["not_applicable_reason"]
        if not_applicable_reason != "NOT_APPLICABLE":
            not_applicable_reason = require_string(not_applicable_reason, f"routes[{index}].not_applicable_reason")
        priority = require_int(route["priority"], f"routes[{index}].priority")
        core = {
            "route_id": route_id,
            "derivative_type": derivative_type,
            "source_package_ref": dict(source_ref),
            "source_spans": source_spans,
            "semantic_program_ref": semantic_ref,
            "final_script_ref": final_ref,
            "archetype_coalition_ref": archetype_ref,
            "primitive_coalition_ref": primitive_ref,
            "activation_transfer_contract_ref": transfer_ref,
            "harness_binding_ref": dict(harness_ref),
            "animation_scene_package_ref": animation_ref,
            "priority": priority,
            "not_applicable_reason": not_applicable_reason,
            "state": "PENDING",
        }
        reject_noncanonical(core)
        return {"job_id": semantic_identity("derivative-job", core), "job_version": "1.0.0", **core}

    @staticmethod
    def _source_spans(value: Any, index: int, source_ref: Mapping[str, str]) -> list[dict[str, Any]]:
        if not isinstance(value, list) or not value:
            raise PipelineValidationError(f"routes[{index}].source_spans must be non-empty")
        result = []
        for span_index, span in enumerate(value):
            required = {"source_id", "source_version", "source_sha256", "start_ms", "end_ms", "speaker_id"}
            if not isinstance(span, Mapping) or set(span) != required:
                raise PipelineValidationError(f"routes[{index}].source_spans[{span_index}] has invalid shape")
            start = require_int(span["start_ms"], "start_ms")
            end = require_int(span["end_ms"], "end_ms")
            if end <= start:
                raise PipelineValidationError("source span end_ms must be greater than start_ms")
            if span["source_id"] != source_ref["object_id"] or span["source_sha256"] != source_ref["sha256"]:
                raise PipelineValidationError("source span must bind to the batch source package")
            result.append(
                {
                    "source_id": require_string(span["source_id"], "source_id"),
                    "source_version": require_string(span["source_version"], "source_version"),
                    "source_sha256": require_string(span["source_sha256"], "source_sha256"),
                    "start_ms": start,
                    "end_ms": end,
                    "speaker_id": require_string(span["speaker_id"], "speaker_id"),
                }
            )
        return sorted(result, key=lambda item: (item["start_ms"], item["end_ms"], item["speaker_id"]))
