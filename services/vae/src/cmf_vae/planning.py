from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256
from ca_delegation_rc4 import ContractSet

from .errors import VAEValidationError
from .repository import VAERepository
from .validation import reject_noncanonical, semantic_id


class DemandAdmissionService:
    def __init__(self, repository: VAERepository, contracts: ContractSet):
        self.repository=repository; self.contracts=contracts

    def admit(self, demand: Mapping[str,Any], *, idempotency_key: str) -> dict[str,Any]:
        payload=dict(demand); self.contracts.validate("visual-asset-demand",payload)
        encoded=str(payload).lower()
        if "format02" in encoded or "format_02" in encoded:
            raise VAEValidationError("Format 02 remains deferred and cannot enter Phase 8")
        lineage=payload["activative_semantic_lineage"]
        if payload["source_provenance"]["source_kind"]=="interview_expression":
            if not lineage["reaction_receipt_refs"] or not lineage["expression_moment_refs"]:
                raise VAEValidationError("interview_expression demand requires Reaction Receipt and Expression Moment provenance")
        demand_sha=canonical_sha256(payload)
        demand_ref={"request_id":payload["request_id"],"version":payload["version"],"payload_hash":"sha256:"+demand_sha,"canonical_ref":f"cmf-contract://demands/{payload['request_id']}/{payload['version']}"}
        stored=self.repository.store_object("visual_asset_demand",payload,object_id=f"demand:{payload['request_id']}:{payload['version']}",version="1.0.0",lifecycle_state="ACCEPTED",idempotency_key=idempotency_key)
        return {"demand_ref":demand_ref,"stored_object":stored,"admission_status":"ACCEPTED","delegation_release":self.contracts.version,"production_authorized":False}


class ProductionPlanCompiler:
    def __init__(self, repository: VAERepository): self.repository=repository

    def compile(self, demand: Mapping[str,Any], demand_ref: Mapping[str,Any], *, idempotency_key: str, include_geometry_reference: bool = False) -> dict[str,Any]:
        stages=[
            {"stage_id":"stage:segmentation","sequence":10,"stage_kind":"SEGMENTATION","required_capability_kind":"SEGMENTATION","required_features":[],"inputs":["source_evidence"],"outputs":["mask","geometry_pack"],"quality_round":0},
            {"stage_id":"stage:matting","sequence":20,"stage_kind":"MATTING","required_capability_kind":"MATTING","required_features":[],"inputs":["mask"],"outputs":["alpha_cutout"],"quality_round":0},
            {"stage_id":"stage:materialization","sequence":30,"stage_kind":"MATERIALIZATION","required_capability_kind":"MATERIALIZATION","required_features":[],"inputs":["alpha_cutout","visual_semantic_pack"],"outputs":["candidate_asset"],"quality_round":1},
            {"stage_id":"stage:evaluation","sequence":40,"stage_kind":"EVALUATION","required_capability_kind":"EVALUATION","required_features":[],"inputs":["candidate_asset","composition_intent"],"outputs":["evaluation_receipt"],"quality_round":1},
        ]
        if include_geometry_reference:
            stages.insert(2,{"stage_id":"stage:geometry-reference","sequence":25,"stage_kind":"GEOMETRY_REFERENCE","required_capability_kind":"GEOMETRY_REFERENCE","required_features":[],"inputs":["identity_continuity","composition_intent"],"outputs":["geometry_reference"],"quality_round":0})
        plan_core={
            "demand_ref":dict(demand_ref),
            "asset_family":demand["asset_classification"]["family"],
            "asset_subtype":demand["asset_classification"]["subtype"],
            "category_profile_ref":demand["category_profile"],
            "format_profile_ref":demand["format_profile"],
            "source_provenance":demand["source_provenance"],
            "semantic_lineage":demand["activative_semantic_lineage"],
            "activation_contract":demand["activation_contract"],
            "visual_semantic_pack":demand["visual_semantic_pack"],
            "visual_narrative_program":demand["visual_narrative_program"],
            "feature_contracts":demand["feature_contracts"],
            "wrong_reading_locks":demand["wrong_reading_locks"],
            "composition_intent":demand["composition_intent"],
            "delivery":demand["delivery"],
            "evaluation_policy":demand["evaluation_policy"],
            "execution_policy":demand["execution_policy"],
            "stages":stages,
            "provider_bindings":"NOT_APPLICABLE_UNTIL_WORKCELL_COMPILATION",
            "semantic_values_owned_by_vae":False,
            "production_authorized":False,
        }
        reject_noncanonical(plan_core)
        plan={"plan_id":semantic_id("visual-production-plan",plan_core),"plan_version":"1.0.0",**plan_core}
        stored=self.repository.store_object("visual_production_plan",plan,object_id=plan["plan_id"],version="1.0.0",lifecycle_state="PLANNED",idempotency_key=idempotency_key)
        self.repository.add_edge(stored["object_id"],stored["object_id"],"self_identity")
        self.repository.add_edge(f"demand:{demand['request_id']}:{demand['version']}",plan["plan_id"],"compiled_into")
        return stored
