from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_enum, require_int, require_ref, require_string, semantic_id
from .errors import ValidationError
from .repository import InterviewRepository

TRANSITIONS={"HARD_CUT","DISSOLVE","FADE","WIPE","SOURCE_START","SOURCE_END","UNKNOWN"}

class VisualIndexService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def compile(self, *, source_package_ref: Mapping[str,Any], duration_ms: int, shots: list[Mapping[str,Any]], keyframe_candidates: list[Mapping[str,Any]], profile_id: str, idempotency_key: str) -> dict[str,Any]:
        ref=require_ref(source_package_ref,"source_package_ref"); duration=require_int(duration_ms,"duration_ms",minimum=1)
        if not shots: shots=[{"shot_id":"shot-0000","start_ms":0,"end_ms":duration,"transition_in":"SOURCE_START","transition_out":"SOURCE_END"}]
        normalized=[]
        for i,s in enumerate(shots):
            if set(s)!={"shot_id","start_ms","end_ms","transition_in","transition_out"}: raise ValidationError("shot shape invalid")
            normalized.append({"shot_id":require_string(s["shot_id"],"shot_id"),"index":i,"start_ms":require_int(s["start_ms"],"start_ms",minimum=0),"end_ms":require_int(s["end_ms"],"end_ms",minimum=1),"transition_in":require_enum(s["transition_in"],TRANSITIONS,"transition_in"),"transition_out":require_enum(s["transition_out"],TRANSITIONS,"transition_out")})
        normalized.sort(key=lambda x:(x["start_ms"],x["end_ms"],x["shot_id"]))
        cursor=0
        for i,s in enumerate(normalized):
            if s["start_ms"]!=cursor: raise ValidationError("shot map must partition source without gaps or overlaps")
            if s["end_ms"]<=s["start_ms"] or s["end_ms"]>duration: raise ValidationError("invalid shot interval")
            cursor=s["end_ms"]
        if cursor!=duration: raise ValidationError("shot map must cover full source duration")
        candidates=[]
        for c in keyframe_candidates:
            if set(c)!={"candidate_id","timestamp_ms","frame_number","score","logical_uri","sha256"}: raise ValidationError("keyframe candidate shape invalid")
            ts=require_int(c["timestamp_ms"],"timestamp_ms",minimum=0)
            if ts>=duration: raise ValidationError("keyframe outside source")
            shot=next((s for s in normalized if s["start_ms"]<=ts<s["end_ms"]),None)
            if not shot: raise ValidationError("keyframe not addressable to a shot")
            candidates.append({"candidate_id":require_string(c["candidate_id"],"candidate_id"),"timestamp_ms":ts,"frame_number":require_int(c["frame_number"],"frame_number",minimum=0),"score":require_int(c["score"],"score",minimum=0),"logical_uri":require_string(c["logical_uri"],"logical_uri"),"sha256":require_string(c["sha256"],"sha256"),"shot_id":shot["shot_id"]})
        selected=[]
        for shot in normalized:
            subset=[c for c in candidates if c["shot_id"]==shot["shot_id"]]
            if subset:
                chosen=sorted(subset,key=lambda x:(-x["score"],x["timestamp_ms"],x["frame_number"],x["candidate_id"]))[0]
                selected.append(chosen)
        core={"source_package_ref":ref,"profile_id":require_string(profile_id,"profile_id"),"duration_ms":duration,"shots":normalized,"keyframes":selected,"technical_only":True,"creates_expression_moments":False,"limitations":[]}
        object_id=semantic_id("ie:visual-index",core); payload={"visual_index_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("source_visual_structure_index",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
        self.repository.add_edge(ref["object_id"],object_id,"source_of_visual_index")
        return result
