from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .errors import CapabilityGap, VAEValidationError
from .validation import reject_noncanonical, require_string, semantic_id


class CapabilityRegistry:
    def __init__(self):
        self._profiles: dict[str,dict[str,Any]]={}

    def register(self, profile: Mapping[str,Any]) -> dict[str,Any]:
        required={"capability_id","provider_id","capability_kind","execution_mode","evidence_state","certified","production_authorized","priority","supported_asset_families","required_features","runtime_ref","configured"}
        if set(profile)!=required: raise VAEValidationError("capability profile has unknown or missing fields")
        value=dict(profile); reject_noncanonical(value)
        cid=require_string(value["capability_id"],"capability_id")
        if cid in self._profiles and self._profiles[cid]!=value: raise VAEValidationError("capability identity collision")
        self._profiles[cid]=value
        return dict(value)

    def get(self, capability_id: str) -> dict[str,Any]:
        try:return dict(self._profiles[capability_id])
        except KeyError as exc: raise CapabilityGap(f"unknown capability: {capability_id}") from exc

    def all(self) -> list[dict[str,Any]]:
        return [dict(self._profiles[key]) for key in sorted(self._profiles)]

    def resolve(self, kind: str, *, asset_family: str, required_features: list[str], preferred_ids: list[str] | None = None) -> dict[str,Any]:
        preferences=preferred_ids or []
        candidates=[]
        for p in self._profiles.values():
            if p["capability_kind"]!=kind or not p["configured"]: continue
            if asset_family not in p["supported_asset_families"] and "*" not in p["supported_asset_families"]: continue
            if not set(required_features)<=set(p["required_features"]): continue
            candidates.append(p)
        if not candidates: raise CapabilityGap(f"no eligible capability for {kind}")
        candidates.sort(key=lambda p:(0 if p["capability_id"] in preferences else 1,p["priority"],p["capability_id"]))
        return dict(candidates[0])


def default_registry() -> CapabilityRegistry:
    registry=CapabilityRegistry()
    base={"evidence_state":"DEVELOPMENT_REFERENCE","certified":False,"production_authorized":False,"priority":100,"supported_asset_families":["*"],"required_features":[],"runtime_ref":{"object_id":"runtime:python-reference","version":"1.0.0","sha256":"0"*64},"configured":True}
    for cid,provider,kind,mode,priority in [
        ("reference.segment.v1","CMF_REFERENCE","SEGMENTATION","LOCAL_REFERENCE",10),
        ("reference.matting.v1","CMF_REFERENCE","MATTING","LOCAL_REFERENCE",10),
        ("reference.raster.v1","CMF_REFERENCE","MATERIALIZATION","LOCAL_REFERENCE",10),
        ("comfyui.compiler.v1","CMF_VAE","WORKFLOW_COMPILATION","COMPILER_ONLY",10),
        ("reference.gnm-geometry.v1","CMF_REFERENCE","GEOMETRY_REFERENCE","LOCAL_REFERENCE",20),
        ("technical.evaluator.v1","CMF_VAE","EVALUATION","LOCAL_DETERMINISTIC",10),
    ]:
        registry.register({**base,"capability_id":cid,"provider_id":provider,"capability_kind":kind,"execution_mode":mode,"priority":priority})
    return registry


class WorkcellCompiler:
    def __init__(self, registry: CapabilityRegistry): self.registry=registry

    def compile(self, plan: Mapping[str,Any], *, producer_actor_id: str, evaluator_actor_id: str, preferred_capability_ids: list[str] | None = None) -> dict[str,Any]:
        if producer_actor_id==evaluator_actor_id: raise VAEValidationError("materializer and evaluator identities must differ")
        bindings=[]
        for stage in plan["stages"]:
            if stage["required_capability_kind"]=="NOT_APPLICABLE": continue
            profile=self.registry.resolve(stage["required_capability_kind"],asset_family=plan["asset_family"],required_features=stage["required_features"],preferred_ids=preferred_capability_ids)
            bindings.append({"stage_id":stage["stage_id"],"capability_id":profile["capability_id"],"provider_id":profile["provider_id"],"execution_mode":profile["execution_mode"],"profile_sha256":canonical_sha256(profile)})
        core={"plan_ref":{"object_id":plan["plan_id"],"version":plan["plan_version"],"sha256":canonical_sha256(plan)},"producer_actor_id":producer_actor_id,"evaluator_actor_id":evaluator_actor_id,"stage_bindings":bindings,"semantic_values_owned_by_vae":False,"provider_bindings_owned_by_vae":True,"production_authorized":False}
        return {"workcell_id":semantic_id("workcell",core),"workcell_version":"1.0.0",**core}
