from __future__ import annotations
from typing import Any, Mapping
from ..repositories.air_repository import AirRepository
from .production_common import add_lineage_edges, require_air_ref
from .semantic_authority import SemanticAuthorityService

class TransferService:
    def __init__(self,repository:AirRepository): self.repository=repository; self.semantic=SemanticAuthorityService(repository)
    def store_contract(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("activation_transfer_contract",payload)
        for field,kind in (("selected_hypothesis_ref","activation_hypothesis"),("role_tension_ref","psychological_role_tension_contract"),("primitive_coalition_ref","primitive_coalition_contract"),("archetype_coalition_ref","archetype_coalition_program"),("final_script_ref","final_script_package")):
            require_air_ref(self.repository,n[field],object_types=kind)
        result = self.semantic.store("activation_transfer_contract",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="governs_transfer_of", target_refs=[*n["source_expression_refs"], *n["source_package_refs"], *n["expression_moment_refs"], *n["reaction_receipt_refs"], n["selected_hypothesis_ref"], n["role_tension_ref"], n["primitive_coalition_ref"], n["archetype_coalition_ref"], n["final_script_ref"]], evidence={"service":"activation_transfer_contract","phase":"PHASE_05"})
        return result
    def store_lineage(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("source_transformation_lineage",payload)
        result = self.semantic.store("source_transformation_lineage",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="transforms", target_refs=[*n["source_refs"], n["target_ref"], *n["source_span_refs"]], evidence={"service":"source_transformation_lineage","phase":"PHASE_05","transformation_class":n["transformation_class"]})
        return result
    def store_checkpoint(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("transfer_checkpoint",payload); require_air_ref(self.repository,n["contract_ref"],object_types="activation_transfer_contract")
        result = self.semantic.store("transfer_checkpoint",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="evaluates", target_refs=[n["contract_ref"], n["target_ref"]], evidence={"service":"transfer_checkpoint","phase":"PHASE_05","checkpoint":n["checkpoint"]})
        return result
    def store_evaluation(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("activation_transfer_evaluation_receipt",payload); require_air_ref(self.repository,n["contract_ref"],object_types="activation_transfer_contract");
        for ref in n["checkpoint_refs"]: require_air_ref(self.repository,ref,object_types="transfer_checkpoint")
        result = self.semantic.store("activation_transfer_evaluation_receipt",n,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="evaluates", target_refs=[n["contract_ref"], *n["checkpoint_refs"], n["independent_evaluation_ref"]], evidence={"service":"transfer_evaluation","phase":"PHASE_05","verdict":n["verdict"]})
        return result
    def store_failure(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("transfer_failure",payload); require_air_ref(self.repository,n["contract_ref"],object_types="activation_transfer_contract"); require_air_ref(self.repository,n["checkpoint_ref"],object_types="transfer_checkpoint"); return self.semantic.store("transfer_failure",n,idempotency_key=idempotency_key)
    def store_repair(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        n=self.semantic.validate("transfer_repair_request",payload); require_air_ref(self.repository,n["failure_ref"],object_types="transfer_failure"); return self.semantic.store("transfer_repair_request",n,idempotency_key=idempotency_key)
