from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_int, require_ref, require_string, require_string_list, reject_noncanonical, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository

TRACK_TYPES={"VIDEO","AUDIO","CAPTION","OVERLAY","MOTION","EVIDENCE"}
ELEMENT_KINDS={"SOURCE_SEGMENT","APPROVED_ASSET","GENERATED_SLOT","TEXT","AUDIO","MOTION_SLOT"}


def _strict(value: Any, required: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value)!=required:
        raise PipelineValidationError(f"{label} must contain exactly {sorted(required)}")
    return value


class VideoEditProgramService:
    def __init__(self, repository: PipelineRepository):
        self.repository=repository

    def compile(self, request: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        required={
            "derivative_job_ref","source_registration_ref","semantic_production_package_ref",
            "final_script_ref","activation_transfer_contract_ref","harness_binding_ref",
            "canvas","timebase","tracks","evaluation_profile_ref","wrong_reading_locks",
        }
        _strict(request,required,"video edit request")
        refs={field:require_ref(request[field],field) for field in (
            "derivative_job_ref","source_registration_ref","semantic_production_package_ref",
            "final_script_ref","activation_transfer_contract_ref","harness_binding_ref","evaluation_profile_ref",
        )}
        canvas=_strict(request["canvas"],{"width","height","fps_numerator","fps_denominator","duration_ms"},"canvas")
        normalized_canvas={
            "width":require_int(canvas["width"],"canvas.width",minimum=1),
            "height":require_int(canvas["height"],"canvas.height",minimum=1),
            "fps_numerator":require_int(canvas["fps_numerator"],"canvas.fps_numerator",minimum=1),
            "fps_denominator":require_int(canvas["fps_denominator"],"canvas.fps_denominator",minimum=1),
            "duration_ms":require_int(canvas["duration_ms"],"canvas.duration_ms",minimum=1),
        }
        timebase=_strict(request["timebase"],{"numerator","denominator"},"timebase")
        normalized_timebase={"numerator":require_int(timebase["numerator"],"timebase.numerator",minimum=1),"denominator":require_int(timebase["denominator"],"timebase.denominator",minimum=1)}
        tracks=[]
        primary_count=0
        element_ids=set()
        for ti,raw_track in enumerate(request["tracks"]):
            track=_strict(raw_track,{"track_id","track_type","role","z_index","elements"},f"tracks[{ti}]")
            track_type=require_string(track["track_type"],f"tracks[{ti}].track_type")
            if track_type not in TRACK_TYPES: raise PipelineValidationError("unsupported track type")
            role=require_string(track["role"],f"tracks[{ti}].role")
            if role=="PRIMARY_A_ROLL_SPINE": primary_count+=1
            elements=[]
            for ei,raw in enumerate(track["elements"]):
                fields={"element_id","kind","output_start_ms","output_end_ms","semantic_role","sequence_role","source_registration_ref","source_start_ms","source_end_ms","artifact_ref","generated_slot_state","bbox_intent_ref","text"}
                elem=_strict(raw,fields,f"tracks[{ti}].elements[{ei}]")
                element_id=require_string(elem["element_id"],"element_id")
                if element_id in element_ids: raise PipelineValidationError("element IDs must be unique")
                element_ids.add(element_id)
                kind=require_string(elem["kind"],"kind")
                if kind not in ELEMENT_KINDS: raise PipelineValidationError("unsupported element kind")
                out_start=require_int(elem["output_start_ms"],"output_start_ms")
                out_end=require_int(elem["output_end_ms"],"output_end_ms",minimum=1)
                if out_end<=out_start or out_end>normalized_canvas["duration_ms"]: raise PipelineValidationError("invalid output interval")
                source_ref="NOT_APPLICABLE" if elem["source_registration_ref"]=="NOT_APPLICABLE" else require_ref(elem["source_registration_ref"],"source_registration_ref")
                source_start=elem["source_start_ms"]; source_end=elem["source_end_ms"]
                if kind=="SOURCE_SEGMENT":
                    if source_ref=="NOT_APPLICABLE": raise PipelineValidationError("source segment requires source registration")
                    source_start=require_int(source_start,"source_start_ms")
                    source_end=require_int(source_end,"source_end_ms",minimum=1)
                    if source_end<=source_start: raise PipelineValidationError("invalid source interval")
                else:
                    if source_start!="NOT_APPLICABLE" or source_end!="NOT_APPLICABLE": raise PipelineValidationError("non-source element source times must be NOT_APPLICABLE")
                artifact_ref="NOT_APPLICABLE" if elem["artifact_ref"]=="NOT_APPLICABLE" else require_ref(elem["artifact_ref"],"artifact_ref")
                bbox_ref="NOT_APPLICABLE" if elem["bbox_intent_ref"]=="NOT_APPLICABLE" else require_ref(elem["bbox_intent_ref"],"bbox_intent_ref")
                generated_state=require_string(elem["generated_slot_state"],"generated_slot_state")
                if kind=="GENERATED_SLOT" and generated_state not in {"UNMATERIALIZED","MATERIALIZED"}: raise PipelineValidationError("invalid generated slot state")
                if kind=="GENERATED_SLOT" and generated_state=="UNMATERIALIZED" and artifact_ref!="NOT_APPLICABLE": raise PipelineValidationError("unmaterialized generated slot cannot have artifact")
                elements.append({
                    "element_id":element_id,"kind":kind,"output_start_ms":out_start,"output_end_ms":out_end,
                    "semantic_role":require_string(elem["semantic_role"],"semantic_role"),"sequence_role":require_string(elem["sequence_role"],"sequence_role"),
                    "source_registration_ref":source_ref,"source_start_ms":source_start,"source_end_ms":source_end,
                    "artifact_ref":artifact_ref,"generated_slot_state":generated_state,"bbox_intent_ref":bbox_ref,
                    "text":require_string(elem["text"],"text") if elem["text"]!="NOT_APPLICABLE" else "NOT_APPLICABLE",
                })
            elements.sort(key=lambda x:(x["output_start_ms"],x["output_end_ms"],x["element_id"]))
            for left,right in zip(elements,elements[1:]):
                if left["output_end_ms"]>right["output_start_ms"] and track_type in {"VIDEO","AUDIO","CAPTION"}:
                    raise PipelineValidationError(f"overlap in exclusive track {track['track_id']}")
            tracks.append({"track_id":require_string(track["track_id"],"track_id"),"track_type":track_type,"role":role,"z_index":require_int(track["z_index"],"z_index"),"elements":elements})
        if primary_count!=1: raise PipelineValidationError("source-led program requires exactly one PRIMARY_A_ROLL_SPINE")
        tracks.sort(key=lambda x:(x["z_index"],x["track_id"]))
        locks=require_string_list(request["wrong_reading_locks"],"wrong_reading_locks",non_empty=True)
        core={**refs,"canvas":normalized_canvas,"timebase":normalized_timebase,"tracks":tracks,"wrong_reading_locks":locks,
              "timeline_authority":"CANONICAL_VIDEO_EDIT_PROGRAM","source_a_roll_required":True,"production_authorized":False}
        reject_noncanonical(core)
        program={"program_id":semantic_identity("video-edit-program",core),"program_version":"1.0.0",**core}
        result=self.repository.store_object("video_edit_program",program,idempotency_key=idempotency_key,object_id=program["program_id"],lifecycle_state="COMPILED")
        for field in refs:
            self.repository.add_edge(refs[field]["object_id"],program["program_id"],f"{field}_input")
        return result

    def projection(self, program_id: str) -> dict[str, Any]:
        obj=self.repository.get_object(program_id)
        payload=obj["payload"]
        return {"program_ref":{"object_id":program_id,"version":payload["program_version"],"sha256":obj["canonical_sha256"]},"canvas":payload["canvas"],"tracks":payload["tracks"],"read_only":True}
