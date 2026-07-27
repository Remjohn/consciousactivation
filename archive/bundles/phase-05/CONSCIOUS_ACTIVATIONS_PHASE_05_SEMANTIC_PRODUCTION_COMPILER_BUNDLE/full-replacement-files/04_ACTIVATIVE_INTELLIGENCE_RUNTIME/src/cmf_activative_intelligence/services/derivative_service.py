from __future__ import annotations
from typing import Any, Mapping
from ca_contracts import canonical_sha256
from ..repositories.air_repository import AirRepository
from .production_common import add_lineage_edges, require_air_ref
from .semantic_authority import SemanticAuthorityService

class DerivativeService:
    def __init__(self,repository:AirRepository): self.repository=repository; self.semantic=SemanticAuthorityService(repository)
    def store_input_manifest(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("derivative_input_manifest",payload)
        for field,kind in (("selected_hypothesis_ref","activation_hypothesis"),("matrix_of_edging_ref","matrix_of_edging"),("role_tension_ref","psychological_role_tension_contract"),("primitive_coalition_ref","primitive_coalition_contract"),("archetype_coalition_ref","archetype_coalition_program"),("brand_context_ref","brand_context_version"),("voice_dna_ref","voice_dna"),("visual_dna_ref","visual_dna")):
            require_air_ref(self.repository,n[field],object_types=kind)
        result = self.semantic.store("derivative_input_manifest",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="compiled_from", target_refs=[*n["source_package_refs"], *n["expression_moment_refs"], *n["reaction_receipt_refs"], n["observed_activative_pack_ref"], n["selected_hypothesis_ref"], n["matrix_of_edging_ref"], n["role_tension_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"], n["brand_context_ref"], n["voice_dna_ref"], n["visual_dna_ref"]], evidence={"service":"derivative_input_manifest","phase":"PHASE_05"})
        return result
    def store_program(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("derivative_activation_program",payload)
        for field,kind in (("input_manifest_ref","derivative_input_manifest"),("role_tension_ref","psychological_role_tension_contract"),("matrix_of_edging_ref","matrix_of_edging"),("primitive_coalition_ref","primitive_coalition_contract"),("archetype_coalition_ref","archetype_coalition_program"),("brand_context_ref","brand_context_version"),("voice_dna_ref","voice_dna"),("visual_dna_ref","visual_dna")):
            require_air_ref(self.repository,n[field],object_types=kind)
        result = self.semantic.store("derivative_activation_program",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="compiled_from", target_refs=[n["input_manifest_ref"], *n["source_ingredient_refs"], n["role_tension_ref"], n["matrix_of_edging_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"], n["brand_context_ref"], n["voice_dna_ref"], n["visual_dna_ref"]], evidence={"service":"derivative_program","phase":"PHASE_05"})
        return result
    def store_jit_request(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("jit_authoring_request",payload); require_air_ref(self.repository,n["program_ref"],object_types="derivative_activation_program"); require_air_ref(self.repository,n["voice_dna_ref"],object_types="voice_dna"); require_air_ref(self.repository,n["primitive_coalition_ref"],object_types="primitive_coalition_contract"); require_air_ref(self.repository,n["archetype_coalition_ref"],object_types="archetype_coalition_program")
        result = self.semantic.store("jit_authoring_request",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="authorizes_context_for", target_refs=[n["program_ref"], *n["approved_ingredient_refs"], n["voice_dna_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"]], evidence={"service":"jit_authoring","phase":"PHASE_05"})
        return result
    def store_proposal(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("script_proposal_artifact",payload); require_air_ref(self.repository,n["authoring_request_ref"],object_types="jit_authoring_request"); require_air_ref(self.repository,n["program_ref"],object_types="derivative_activation_program")
        result = self.semantic.store("script_proposal_artifact",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="proposed_for", target_refs=[n["authoring_request_ref"], n["program_ref"], *n["rejected_alternative_refs"]], evidence={"service":"script_proposal","phase":"PHASE_05"})
        return result
    def store_script(self,payload:Mapping[str,Any],*,idempotency_key:str,expected_revision:int|None=None)->dict[str,Any]:
        n=self.semantic.validate("final_script_package",payload)
        for field,kind in (("program_ref","derivative_activation_program"),("proposal_ref","script_proposal_artifact"),("role_tension_ref","psychological_role_tension_contract"),("primitive_coalition_ref","primitive_coalition_contract"),("archetype_coalition_ref","archetype_coalition_program"),("brand_context_ref","brand_context_version"),("voice_dna_ref","voice_dna")):
            require_air_ref(self.repository,n[field],object_types=kind)
        expected=canonical_sha256(n["segments"])
        if n["script_sha256"]!=expected: raise ValueError("script_sha256 must hash exact ordered segment bytes")
        for ref in n["source_lineage_refs"]: require_air_ref(self.repository,ref,object_types="source_transformation_lineage")
        for ref in n["distillation_receipt_refs"]: require_air_ref(self.repository,ref,object_types="distillation_layer_receipt")
        result = self.semantic.store("final_script_package",n,idempotency_key=idempotency_key,expected_revision=expected_revision)
        add_lineage_edges(self.repository, source_result=result, relation_type="compiled_from", target_refs=[n["program_ref"], n["proposal_ref"], *n["source_lineage_refs"], n["role_tension_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"], n["brand_context_ref"], n["voice_dna_ref"], *n["distillation_receipt_refs"]], evidence={"service":"final_script","phase":"PHASE_05","operator_approved":n["operator_approved"]})
        return result
    def approve_script(self,*,candidate_script_ref:Mapping[str,Any],operator_id:str,operator_decision_ref:Mapping[str,Any],evaluation_refs:list[Mapping[str,Any]],rationale:str,approval_idempotency_key:str,script_revision_idempotency_key:str)->dict[str,Any]:
        candidate=require_air_ref(self.repository,candidate_script_ref,object_types="final_script_package")
        receipt_payload={"receipt_id":f"approval:{candidate.object_id}","version":"1.0.0","authority":dict(candidate.payload["authority"]),"candidate_script_ref":candidate.immutable_ref(),"approved_script_sha256":candidate.payload["script_sha256"],"operator_id":operator_id,"operator_decision_ref":dict(operator_decision_ref),"decision":"APPROVE","exact_bytes_approved":True,"evaluation_refs":[dict(x) for x in evaluation_refs],"resulting_script_ref":candidate.immutable_ref(),"rationale":rationale}
        approval=self.semantic.store("final_script_approval_receipt",receipt_payload,idempotency_key=approval_idempotency_key)
        approval_ref={"object_id":approval["object"]["object_id"],"version":approval["object"]["semantic_version"],"sha256":approval["object"]["canonical_sha256"]}
        successor=dict(candidate.payload); successor.update({"lifecycle_state":"approved","epistemic_state":"operator_confirmed","operator_approved":True,"composition_eligible":True,"approval_receipt_ref":approval_ref,"supersedes_ref":candidate.immutable_ref()})
        script=self.store_script(successor,idempotency_key=script_revision_idempotency_key,expected_revision=candidate.revision)
        return {"approval":approval,"script":script}
    def store_animation_package(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("animation_scene_package",payload); script=require_air_ref(self.repository,n["final_script_ref"],object_types="final_script_package");
        if not script.payload["operator_approved"]: raise ValueError("animation scene package requires approved Final Script")
        result = self.semantic.store("animation_scene_package",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="derived_from", target_refs=[n["final_script_ref"], *[ref for scene in n["scenes"] for ref in [*scene["source_refs"], *scene["identity_continuity_refs"], *scene["wrong_reading_lock_refs"]]]], evidence={"service":"animation_scene_package","phase":"PHASE_05"})
        return result
    def store_semantic_package(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("semantic_production_package",payload)
        for field,kind in (("derivative_program_ref","derivative_activation_program"),("approved_final_script_ref","final_script_package"),("animation_scene_package_ref","animation_scene_package"),("activation_transfer_contract_ref","activation_transfer_contract"),("matrix_of_edging_ref","matrix_of_edging"),("role_tension_ref","psychological_role_tension_contract"),("primitive_coalition_ref","primitive_coalition_contract"),("archetype_coalition_ref","archetype_coalition_program"),("brand_context_ref","brand_context_version"),("voice_dna_ref","voice_dna"),("visual_dna_ref","visual_dna"),("approval_receipt_ref","final_script_approval_receipt")):
            require_air_ref(self.repository,n[field],object_types=kind)
        for ref in n["source_lineage_refs"]: require_air_ref(self.repository,ref,object_types="source_transformation_lineage")
        for ref in n["distillation_receipt_refs"]: require_air_ref(self.repository,ref,object_types="distillation_layer_receipt")
        result = self.semantic.store("semantic_production_package",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="packages", target_refs=[n["derivative_program_ref"], n["approved_final_script_ref"], n["animation_scene_package_ref"], n["activation_transfer_contract_ref"], *n["source_lineage_refs"], n["matrix_of_edging_ref"], n["role_tension_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"], n["brand_context_ref"], n["voice_dna_ref"], n["visual_dna_ref"], *n["distillation_receipt_refs"], n["approval_receipt_ref"]], evidence={"service":"semantic_production_package","phase":"PHASE_05"})
        return result
