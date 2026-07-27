from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .validation import semantic_id


def project_okf(*, plan: Mapping[str,Any], result: Mapping[str,Any], evaluation: Mapping[str,Any]) -> dict[str,Any]:
    title=f"Visual Asset Result {result['result_id']}"
    frontmatter={"type":"visual_asset_result","id":result["result_id"],"version":str(result["version"]),"status":"validated_development_reference","authority_class":"VAE_DERIVED_PROJECTION","source_record_refs":[plan["plan_id"],result["demand"]["request_id"],evaluation["evaluation_id"]],"content_hash":result["artifact_ref"]["payload_hash"],"asset_family":plan["asset_family"],"failure_code":None,"validity":"development_only"}
    lines=["---"]+[f"{key}: {value}" for key,value in frontmatter.items()]+["---",f"# {title}","",f"Demand: `{result['demand']['request_id']}`",f"Artifact: `{result['artifact_ref']['resource_id']}`",f"Evaluation: `{evaluation['verdict']}`", "", "This projection is derived knowledge. Canonical workflow state remains in the VAE stores."]
    markdown="\n".join(lines)+"\n"
    core={"document_id":semantic_id("okf-visual-asset",{"result_id":result["result_id"],"artifact":result["artifact_ref"]}),"frontmatter":frontmatter,"markdown_sha256":canonical_sha256({"markdown":markdown}),"canonical_state":False,"rebuildable":True}
    return {**core,"markdown":markdown}


def control_tower_projection(*, admission: Mapping[str,Any], plan: Mapping[str,Any], workcell: Mapping[str,Any], job: Mapping[str,Any], events: list[Mapping[str,Any]], evaluation: Mapping[str,Any] | None, result: Mapping[str,Any] | None, projection_fresh: bool = True) -> dict[str,Any]:
    core={"projection_state":"CURRENT" if projection_fresh else "STALE","demand_ref":admission["demand_ref"],"plan_ref":{"object_id":plan["plan_id"],"version":plan["plan_version"],"sha256":canonical_sha256(plan)},"workcell_ref":{"object_id":workcell["workcell_id"],"version":workcell["workcell_version"],"sha256":canonical_sha256(workcell)},"job":{"job_id":job["job_id"],"state":job["state"],"attempt_number":job["attempt_number"],"cancellation_requested":job["cancellation_requested"]},"event_count":len(events),"latest_event":events[-1]["event_type"] if events else "NONE","evaluation_ref":{"object_id":evaluation["evaluation_id"],"version":evaluation["evaluation_version"],"sha256":canonical_sha256(evaluation)} if evaluation else "NOT_AVAILABLE","result_ref":{"result_id":result["result_id"],"version":result["version"],"payload_hash":"sha256:"+canonical_sha256(result),"canonical_ref":f"cmf-contract://results/{result['result_id']}/{result['version']}"} if result else "NOT_AVAILABLE","production_authorized":False,"certified":False}
    return {"projection_id":semantic_id("vae-control-tower",core),"projection_version":"1.0.0",**core}
