from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_delegation_rc4 import ContractSet

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref


def _resource(ref: Mapping[str,str]) -> dict[str,str]:
    r=require_ref(ref,"reference")
    return {"resource_id":r["object_id"],"version":r["version"],"payload_hash":"sha256:"+r["sha256"],"canonical_ref":f"cmf-contract://resources/{r['object_id']}/{r['version']}"}


def _replace(value: Any) -> Any:
    if isinstance(value,str): return value.replace("format02","phase8").replace("FORMAT02","PHASE8").replace("Format 02","Phase 8")
    if isinstance(value,list): return [_replace(item) for item in value]
    if isinstance(value,dict): return {k:_replace(v) for k,v in value.items()}
    return value


class VisualDelegationService:
    def __init__(self, delegation_root):
        self.contracts=ContractSet(delegation_root); self.contracts.verify_release()

    def compile_demand(self, *, source_package_ref: Mapping[str,str], reaction_receipt_refs: list[Mapping[str,str]], expression_moment_refs: list[Mapping[str,str]], semantic_program_ref: Mapping[str,str], final_script_ref: Mapping[str,str], primitive_coalition_ref: Mapping[str,str], archetype_coalition_ref: Mapping[str,str], activation_transfer_contract_ref: Mapping[str,str], content_harness_ref: Mapping[str,str], category_profile_ref: Mapping[str,str], format_profile_ref: Mapping[str,str], width_px: int, height_px: int, wrong_reading_locks: list[str]) -> dict[str,Any]:
        if not reaction_receipt_refs or not expression_moment_refs: raise PipelineValidationError("interview source demand requires Reaction Receipt and Expression Moment references")
        if width_px<1 or height_px<1: raise PipelineValidationError("delivery dimensions must be positive")
        template=_replace(self.contracts.example("visual-asset-demand"))
        core_seed={"source":source_package_ref,"semantic":semantic_program_ref,"script":final_script_ref,"width":width_px,"height":height_px,"locks":wrong_reading_locks}
        request_id=f"req-phase8-{canonical_sha256(core_seed)[:20]}"
        template["request_id"]=request_id; template["version"]=1; template["supersedes"]=None
        template["content_harness_ref"]=_resource(content_harness_ref); template["category_profile"]=_resource(category_profile_ref); template["format_profile"]=_resource(format_profile_ref)
        template["asset_classification"]={"family":"EDITORIAL_IMAGE","subtype":"SOURCE_GROUNDED_VISUAL","harness_role":"semantic_support","visual_syntax_role":"source_grounded_visual"}
        template["source_provenance"]={"source_kind":"interview_expression"}
        template["activative_semantic_lineage"]["activative_intelligence_pack_ref"]=_resource(semantic_program_ref)
        template["activative_semantic_lineage"]["source_evidence_refs"]=[_resource(source_package_ref)]
        template["activative_semantic_lineage"]["reaction_receipt_refs"]=[_resource(item) for item in reaction_receipt_refs]
        template["activative_semantic_lineage"]["expression_moment_refs"]=[_resource(item) for item in expression_moment_refs]
        template["activative_semantic_lineage"]["matrix_edge_product_ref"]=_resource(primitive_coalition_ref)
        template["activative_semantic_lineage"]["context_premise_ref"]=_resource(activation_transfer_contract_ref)
        template["activative_semantic_lineage"]["identity_dna_ref"]=_resource(final_script_ref)
        template["activative_semantic_lineage"]["resonance_map_ref"]=_resource(archetype_coalition_ref)
        template["activative_semantic_lineage"]["activative_call_refs"]=[_resource(final_script_ref)]
        template["semantic_intent"]["evidence_refs"]=[_resource(source_package_ref)]
        template["semantic_intent"]["subject"]="Source-grounded visual expression supporting the approved Final Script."
        template["semantic_intent"]["recognition_target"]="Preserve source identity, edge, and the approved viewer role inside the tension."
        template["visual_semantic_pack"]["audience_visual_world_refs"]=[_resource(archetype_coalition_ref)]
        template["visual_semantic_pack"]["semiotic_mcda_receipt_ref"]=_resource(semantic_program_ref)
        template["reference_evidence"]=[_resource(source_package_ref)]
        template["feature_contracts"]=[{"feature":"negative_space","required_for_meaning":True,"contract_ref":_resource(activation_transfer_contract_ref)},{"feature":"source_fidelity","required_for_meaning":True,"contract_ref":_resource(final_script_ref)}]
        template["identity_continuity"]={"character_ref":_resource(source_package_ref),"environment_ref":None}
        template["delivery"]={"candidate_count":1,"width_px":width_px,"height_px":height_px,"media_type":"image/png"}
        template["composition_intent"]={"canvas_width_px":width_px,"canvas_height_px":height_px,"intended_region":{"x":1000,"y":1000,"width":6000,"height":8000},"reserved_regions":[{"x":6200,"y":800,"width":3000,"height":2600}],"tolerance_basis_points":300,"visual_weight":"PRIMARY","layer_role":"foreground_subject","gaze_direction":"RIGHT"}
        template["wrong_reading_locks"]=sorted(set(wrong_reading_locks)); template["notes"]="Phase 8 provider-neutral demand. Provider selection belongs to VAE."
        template["evaluation_policy"]["profile_ref"]=_resource(activation_transfer_contract_ref); template["evaluation_policy"]["hard_gate_codes"]=["SOURCE_FIDELITY","NEGATIVE_SPACE","WRONG_READING_LOCKS"]
        template["execution_policy"]["budget_authorization_ref"]=_resource(content_harness_ref)
        self.contracts.validate("visual-asset-demand",template)
        if "format02" in str(template).lower(): raise PipelineValidationError("Format 02 identifier leaked into Phase 8 demand")
        demand_hash=canonical_sha256(template)
        return {"demand":template,"demand_ref":{"request_id":request_id,"version":1,"payload_hash":"sha256:"+demand_hash,"canonical_ref":f"cmf-contract://demands/{request_id}/1"},"delegation_release":self.contracts.version,"release_digest":self.contracts.digest,"production_authorized":False}

    def validate_result(self, result: Mapping[str,Any]) -> None:
        self.contracts.validate("asset-result-contract",dict(result))
        if "consumption_authorized" in result: raise PipelineValidationError("VAE result must not assert downstream consumption authority")

    def acknowledge(self, *, demand: Mapping[str,Any], result: Mapping[str,Any], decision: str, consumption_authorized: bool, evidence_ref: Mapping[str,Any]) -> dict[str,Any]:
        self.validate_result(result)
        if decision not in {"ACCEPTED","ACCEPTED_WITH_CONCERNS","REJECTED"}: raise PipelineValidationError("invalid acknowledgement decision")
        result_ref={"result_id":result["result_id"],"version":result["version"],"payload_hash":"sha256:"+canonical_sha256(result),"canonical_ref":f"cmf-contract://results/{result['result_id']}/{result['version']}"}
        acknowledgement={"acknowledgement_id":f"ack-{result['result_id']}","result":result_ref,"demand":dict(demand),"decision":decision,"consumption_authorized":bool(consumption_authorized),"findings":[{"code":"PIPELINE_RESULT_REVIEW","verdict":"PASS" if decision!="REJECTED" else "FAIL","evidence_refs":[dict(evidence_ref)],"note":"Consumption authority belongs to the Pipeline/Harness acknowledgement boundary."}],"acknowledged_at":utc_now_rfc3339()}
        self.contracts.validate("result-acknowledgement",acknowledgement)
        return acknowledgement
