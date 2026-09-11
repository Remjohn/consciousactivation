from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .canonical import require_ref


def pipeline_source_package_handoff(source_package: Mapping[str,Any], observed_pack_ref: Mapping[str,Any], asset_package_ref: Mapping[str,Any]) -> dict[str,Any]:
    obj=source_package["object"] if "object" in source_package else source_package
    return {"handoff_type":"INTERVIEW_EXPRESSION_TO_PIPELINE","source_package_ref":{"object_id":obj["object_id"],"version":obj["version"],"sha256":obj["sha256"]},"observed_evidence_pack_ref":require_ref(observed_pack_ref),"asset_package_spec_ref":require_ref(asset_package_ref),"semantic_values_owned_by_pipeline":False,"production_authorized":False}


def air_read_only_evidence_handoff(observed_pack: Mapping[str,Any]) -> dict[str,Any]:
    obj=observed_pack["object"] if "object" in observed_pack else observed_pack
    return {"handoff_type":"INTERVIEW_EXPRESSION_TO_AIR_READ_ONLY","observed_evidence_pack_ref":{"object_id":obj["object_id"],"version":obj["version"],"sha256":obj["sha256"]},"air_may_mutate_source_evidence":False}


def studio_projection(source_package: Mapping[str,Any], *, moment_refs: list[Mapping[str,Any]], reaction_refs: list[Mapping[str,Any]]) -> dict[str,Any]:
    obj=source_package["object"] if "object" in source_package else source_package
    return {"projection_type":"INTERVIEW_SOURCE_REVIEW","source_package_ref":{"object_id":obj["object_id"],"version":obj["version"],"sha256":obj["sha256"]},"lifecycle_state":obj["payload"]["lifecycle_state"],"derivative_eligible":obj["payload"]["derivative_eligible"],"moment_refs":sorted([require_ref(r) for r in moment_refs],key=lambda x:x["object_id"]),"reaction_refs":sorted([require_ref(r) for r in reaction_refs],key=lambda x:x["object_id"]),"canonical_state_owned_by_studio":False}
