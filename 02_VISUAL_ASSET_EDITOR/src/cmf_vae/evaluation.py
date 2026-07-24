from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .errors import VAEValidationError
from .png import dimensions
from .storage import ContentAddressedStore
from .validation import semantic_id


class TechnicalEvaluator:
    def __init__(self, store: ContentAddressedStore): self.store=store

    def evaluate(self, *, artifact_record: Mapping[str,Any], demand: Mapping[str,Any], geometry: Mapping[str,Any], producer_actor_id: str, evaluator_actor_id: str) -> dict[str,Any]:
        if producer_actor_id==evaluator_actor_id: raise VAEValidationError("producer cannot be its own independent evaluator")
        data,metadata=self.store.get(artifact_record["sha256"])
        width,height=dimensions(data)
        expected=demand["delivery"]
        checks=[
            {"check_id":"ARTIFACT_HASH","result":"PASS" if metadata["sha256"]==artifact_record["sha256"] else "FAIL"},
            {"check_id":"MEDIA_TYPE","result":"PASS" if metadata["media_type"]=="image/png" else "FAIL"},
            {"check_id":"DIMENSIONS","result":"PASS" if width==expected["width_px"] and height==expected["height_px"] else "FAIL"},
            {"check_id":"GEOMETRY_PRESENT","result":"PASS" if geometry.get("subject_bbox") and geometry.get("negative_space_regions") else "FAIL"},
            {"check_id":"WRONG_READING_LOCKS_PRESENT","result":"PASS" if demand["wrong_reading_locks"] else "FAIL"},
        ]
        hard_fail=any(item["result"]!="PASS" for item in checks)
        core={"artifact_ref":artifact_record["resource_ref"],"demand_request_id":demand["request_id"],"producer_actor_id":producer_actor_id,"evaluator_actor_id":evaluator_actor_id,"profile_state":"SPECIFIED_NOT_CERTIFIED","deterministic_checks":checks,"hard_gate_result":"FAIL" if hard_fail else "PASS","verdict":"FAIL" if hard_fail else "PASS_TECHNICAL_REFERENCE","production_eligible":False,"independent_vlm_executed":False}
        return {"evaluation_id":semantic_id("vae-evaluation",core),"evaluation_version":"1.0.0",**core}


class RepairPlanner:
    ALLOWED={"TEXT_COLLISION":{"action":"ADJUST_BBOX","owner":"VISUAL_ASSET_EDITOR"},"MASK_EDGE_ARTIFACT":{"action":"RERUN_MATTING_WITH_BOUNDED_DELTA","owner":"VISUAL_ASSET_EDITOR"},"SOURCE_TIME_BOUNDARY":{"action":"REFER_TO_PIPELINE","owner":"ATOMIC_HARNESS_PIPELINE"},"SEMANTIC_INTENT_CONFLICT":{"action":"REQUEST_DEMAND_AMENDMENT","owner":"ACTIVATIVE_INTELLIGENCE_RUNTIME"}}

    def plan(self, *, target_ref: Mapping[str,Any], failure_code: str, evidence_refs: list[Mapping[str,Any]], attempt_number: int, maximum_attempts: int, preserved_properties: list[str]) -> dict[str,Any]:
        if failure_code not in self.ALLOWED: raise VAEValidationError("unknown repair failure code")
        if attempt_number>maximum_attempts: raise VAEValidationError("repair-attempt ceiling exceeded")
        route=self.ALLOWED[failure_code]
        core={"target_ref":dict(target_ref),"failure_code":failure_code,"evidence_refs":[dict(item) for item in evidence_refs],"action":route["action"],"responsible_product":route["owner"],"attempt_number":attempt_number,"maximum_attempts":maximum_attempts,"preserved_properties":sorted(set(preserved_properties)),"descendant_only":True,"quality_threshold_lowering_allowed":False,"semantic_mutation_allowed":False,"global_regeneration_allowed":False,"escalation_required":attempt_number==maximum_attempts or route["owner"]!="VISUAL_ASSET_EDITOR"}
        return {"repair_plan_id":semantic_id("vae-repair-plan",core),"repair_plan_version":"1.0.0",**core}
