from __future__ import annotations

from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

from .domain.errors import PipelineValidationError
from .domain.validation import reject_noncanonical, require_ref, require_string


class CrossDerivativeContinuityService:
    def __init__(self, repository): self.repository=repository

    def compile(self, *, source_package_ref: Mapping[str,Any], semantic_production_package_ref: Mapping[str,Any], final_script_ref: Mapping[str,Any], activation_transfer_contract_ref: Mapping[str,Any], derivatives: Sequence[Mapping[str,Any]], usage_records: Sequence[Mapping[str,Any]], evaluation_refs: Sequence[Mapping[str,Any]], idempotency_key: str) -> dict[str,Any]:
        source=require_ref(source_package_ref,"source_package_ref"); semantic=require_ref(semantic_production_package_ref,"semantic_production_package_ref"); script=require_ref(final_script_ref,"final_script_ref"); transfer=require_ref(activation_transfer_contract_ref,"activation_transfer_contract_ref")
        normalized_derivatives=[]; artifact_ids=set(); derivative_ids=set()
        for index,item in enumerate(derivatives):
            required={"derivative_id","derivative_type","artifact_ref","source_package_ref","source_span_refs","semantic_program_ref","final_script_ref","transfer_contract_ref","evaluation_refs","consumption_state"}
            if set(item)!=required: raise PipelineValidationError(f"derivatives[{index}] fields invalid")
            if require_ref(item["source_package_ref"],"source_package_ref") != source: raise PipelineValidationError("cross-derivative source package mismatch")
            if require_ref(item["final_script_ref"],"final_script_ref") != script: raise PipelineValidationError("cross-derivative Final Script mismatch")
            if require_ref(item["transfer_contract_ref"],"transfer_contract_ref") != transfer: raise PipelineValidationError("cross-derivative transfer contract mismatch")
            artifact=require_ref(item["artifact_ref"],"artifact_ref"); did=require_string(item["derivative_id"],"derivative_id")
            if did in derivative_ids or artifact["object_id"] in artifact_ids: raise PipelineValidationError("duplicate derivative or artifact identity")
            derivative_ids.add(did);artifact_ids.add(artifact["object_id"])
            spans=[]
            for span in item["source_span_refs"]:
                if set(span)!={"source_ref","start_ms","end_ms","speaker_id","transcript_sha256"}: raise PipelineValidationError("invalid source span")
                if require_ref(span["source_ref"],"source_ref") != source: raise PipelineValidationError("source span uses a different source package")
                if not isinstance(span["start_ms"],int) or not isinstance(span["end_ms"],int) or span["end_ms"]<=span["start_ms"]: raise PipelineValidationError("invalid source span interval")
                spans.append(dict(span))
            normalized_derivatives.append({"derivative_id":did,"derivative_type":require_string(item["derivative_type"],"derivative_type"),"artifact_ref":artifact,"source_package_ref":source,"source_span_refs":sorted(spans,key=lambda s:(s["start_ms"],s["end_ms"])),"semantic_program_ref":require_ref(item["semantic_program_ref"],"semantic_program_ref"),"final_script_ref":script,"transfer_contract_ref":transfer,"evaluation_refs":sorted([require_ref(r,"evaluation_ref") for r in item["evaluation_refs"]],key=lambda r:r["object_id"]),"consumption_state":require_string(item["consumption_state"],"consumption_state")})
        normalized_derivatives.sort(key=lambda d:d["derivative_id"])
        normalized_usage=[]
        for record in usage_records:
            required={"usage_id","source_artifact_ref","consumer_derivative_id","usage_role","time_or_page_locator","acknowledgement_ref"}
            if set(record)!=required: raise PipelineValidationError("usage record fields invalid")
            source_artifact=require_ref(record["source_artifact_ref"],"source_artifact_ref")
            if source_artifact["object_id"] not in artifact_ids: raise PipelineValidationError("usage source artifact not in batch")
            if record["consumer_derivative_id"] not in derivative_ids: raise PipelineValidationError("usage consumer derivative not in batch")
            normalized_usage.append({"usage_id":require_string(record["usage_id"],"usage_id"),"source_artifact_ref":source_artifact,"consumer_derivative_id":require_string(record["consumer_derivative_id"],"consumer_derivative_id"),"usage_role":require_string(record["usage_role"],"usage_role"),"time_or_page_locator":dict(record["time_or_page_locator"]),"acknowledgement_ref":require_ref(record["acknowledgement_ref"],"acknowledgement_ref")})
        normalized_usage.sort(key=lambda r:r["usage_id"])
        graph_edges=[]
        for d in normalized_derivatives:
            graph_edges.extend([
                {"source_id":source["object_id"],"target_id":d["derivative_id"],"relation_type":"grounds_derivative"},
                {"source_id":semantic["object_id"],"target_id":d["derivative_id"],"relation_type":"authorizes_semantic_program"},
                {"source_id":script["object_id"],"target_id":d["derivative_id"],"relation_type":"scripts_derivative"},
                {"source_id":transfer["object_id"],"target_id":d["derivative_id"],"relation_type":"governs_transfer"},
            ])
        for u in normalized_usage: graph_edges.append({"source_id":u["source_artifact_ref"]["object_id"],"target_id":u["consumer_derivative_id"],"relation_type":"reused_as_"+u["usage_role"].lower()})
        graph_edges.sort(key=lambda e:(e["source_id"],e["target_id"],e["relation_type"]))
        payload={"continuity_package_id":f"continuity:{canonical_sha256({'source':source,'derivatives':[d['derivative_id'] for d in normalized_derivatives],'usage':[u['usage_id'] for u in normalized_usage]})}","version":"1.0.0","source_package_ref":source,"semantic_production_package_ref":semantic,"final_script_ref":script,"activation_transfer_contract_ref":transfer,"derivatives":normalized_derivatives,"usage_records":normalized_usage,"evaluation_refs":sorted([require_ref(r,"evaluation_ref") for r in evaluation_refs],key=lambda r:r["object_id"]),"lineage_edges":graph_edges,"historical_replay_policy":"IMMUTABLE_CONTENT_ADDRESSED","result":"PASS"}
        reject_noncanonical(payload);payload["continuity_sha256"]=canonical_sha256(payload)
        return self.repository.store_object("cross_derivative_continuity_package",payload,object_id=payload["continuity_package_id"],idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
