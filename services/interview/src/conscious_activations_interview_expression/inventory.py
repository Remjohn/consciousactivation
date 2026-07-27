from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_ref, semantic_id
from .errors import ValidationError
from .repository import InterviewRepository

class AssetInventoryService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def compile(self, *, source_package_ref: Mapping[str,Any], expression_moment_refs: list[Mapping[str,Any]], phrase_pack_ref: Mapping[str,Any], visual_index_ref: Mapping[str,Any], reaction_receipt_refs: list[Mapping[str,Any]], idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref); moment_refs=[require_ref(r) for r in expression_moment_refs]
        if not moment_refs: raise ValidationError("asset inventory requires approved Expression Moments")
        moments=[]
        for r in moment_refs:
            obj=self.repository.get_object(r["object_id"])
            if obj["payload"]["lifecycle_state"]!="APPROVED": raise ValidationError("asset inventory cannot consume unapproved moment")
            moments.append(obj["payload"])
        phrase_ref=require_ref(phrase_pack_ref); visual_ref=require_ref(visual_index_ref); reactions=[require_ref(r) for r in reaction_receipt_refs]
        phrases=self.repository.get_object(phrase_ref["object_id"])["payload"]["phrases"]
        visual=self.repository.get_object(visual_ref["object_id"])["payload"]
        selected_phrase_ids={p for m in moments for p in [r["object_id"] for r in m["phrase_refs"]]}
        quote_candidates=[{"phrase_id":p["phrase_id"],"text":p["text"],"speaker_id":p["speaker_id"],"start_ms":p["start_ms"],"end_ms":p["end_ms"],"transformation_state":"SOURCE_VERBATIM"} for p in phrases if p["phrase_id"] in selected_phrase_ids]
        keyframes=[{"candidate_id":k["candidate_id"],"timestamp_ms":k["timestamp_ms"],"logical_uri":k["logical_uri"],"sha256":k["sha256"],"shot_id":k["shot_id"]} for k in visual["keyframes"]]
        core={"source_package_ref":source_ref,"expression_moment_refs":sorted(moment_refs,key=lambda x:x["object_id"]),"reaction_receipt_refs":sorted(reactions,key=lambda x:x["object_id"]),"phrase_pack_ref":phrase_ref,"visual_index_ref":visual_ref,"quote_candidates":quote_candidates,"keyframe_candidates":keyframes,"voiceover_spans":[s for m in moments for s in m["source_spans"]],"animation_reference_inputs":keyframes,"semantic_programs_created":False,"final_scripts_created":False,"production_authorized":False}
        object_id=semantic_id("ie:asset-package-spec",core); payload={"asset_package_spec_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("asset_package_spec",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="COMPILED")
        for r in moment_refs: self.repository.add_edge(r["object_id"],object_id,"expression_ingredient")
        return result

    def observed_evidence_pack(self, *, source_package_ref: Mapping[str,Any], expression_moment_refs: list[Mapping[str,Any]], reaction_receipt_refs: list[Mapping[str,Any]], tag_assertion_refs: list[Mapping[str,Any]], idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref)
        core={"source_package_ref":source_ref,"expression_moment_refs":sorted([require_ref(r) for r in expression_moment_refs],key=lambda x:x["object_id"]),"reaction_receipt_refs":sorted([require_ref(r) for r in reaction_receipt_refs],key=lambda x:x["object_id"]),"tag_assertion_refs":sorted([require_ref(r) for r in tag_assertion_refs],key=lambda x:x["object_id"]),"owner":"INTERVIEW_EXPRESSION","semantic_interpretation_owner":"ACTIVATIVE_INTELLIGENCE_RUNTIME","epistemic_state":"OBSERVED","production_authorized":False}
        object_id=semantic_id("ie:observed-evidence-pack",core); payload={"observed_evidence_pack_id":object_id,"version":"1.0.0",**core}
        return self.repository.store_object("observed_expression_evidence_pack",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
