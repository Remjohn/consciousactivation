from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_enum, require_int, require_ref, require_string, semantic_id
from .domain import EPISTEMIC_STATES, SPEAKER_STATES
from .errors import ValidationError
from .repository import InterviewRepository

HESITATIONS = {"um", "uh", "erm", "hmm", "mm"}


class TranscriptService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def align(self, *, source_package_ref: Mapping[str, Any], words: list[Mapping[str, Any]], speaker_segments: list[Mapping[str, Any]], policy_id: str, idempotency_key: str) -> dict[str, Any]:
        source_ref=require_ref(source_package_ref,"source_package_ref")
        if not words: raise ValidationError("words must be non-empty")
        normalized=[]; prior_end=0; indices=set()
        for pos,item in enumerate(words):
            required={"word_id","index","text","start_ms","end_ms","speaker_id","speaker_state","epistemic_state","tag_refs","event_refs"}
            if not isinstance(item,Mapping) or set(item)!=required: raise ValidationError(f"words[{pos}] has invalid shape")
            idx=require_int(item["index"],f"words[{pos}].index",minimum=0)
            if idx in indices: raise ValidationError("word indices must be unique")
            indices.add(idx)
            start=require_int(item["start_ms"],"start_ms",minimum=0); end=require_int(item["end_ms"],"end_ms",minimum=1)
            if end<=start: raise ValidationError("word end must exceed start")
            state=require_enum(item["speaker_state"],SPEAKER_STATES,"speaker_state")
            speaker=require_string(item["speaker_id"],"speaker_id")
            if state=="UNKNOWN" and speaker!="UNKNOWN": raise ValidationError("unknown speaker state must keep speaker UNKNOWN")
            if start<prior_end and state!="OVERLAP": raise ValidationError("overlapping words require OVERLAP state")
            prior_end=max(prior_end,end)
            normalized.append({"word_id":require_string(item["word_id"],"word_id"),"index":idx,"text":require_string(item["text"],"text"),"start_ms":start,"end_ms":end,"speaker_id":speaker,"speaker_state":state,"epistemic_state":require_enum(item["epistemic_state"],EPISTEMIC_STATES,"epistemic_state"),"tag_refs":sorted([require_ref(r) for r in item["tag_refs"]],key=lambda x:x["object_id"]),"event_refs":sorted([require_ref(r) for r in item["event_refs"]],key=lambda x:x["object_id"])})
        normalized.sort(key=lambda x:(x["index"],x["start_ms"],x["word_id"]))
        if [x["index"] for x in normalized] != list(range(len(normalized))): raise ValidationError("word indices must be contiguous from zero")
        segments=[]
        for i,s in enumerate(speaker_segments):
            if set(s)!={"segment_id","start_ms","end_ms","speaker_id","speaker_state"}: raise ValidationError("speaker segment shape invalid")
            segments.append({"segment_id":require_string(s["segment_id"],"segment_id"),"start_ms":require_int(s["start_ms"],"start_ms",minimum=0),"end_ms":require_int(s["end_ms"],"end_ms",minimum=1),"speaker_id":require_string(s["speaker_id"],"speaker_id"),"speaker_state":require_enum(s["speaker_state"],SPEAKER_STATES,"speaker_state")})
        core={"source_package_ref":source_ref,"policy_id":require_string(policy_id,"policy_id"),"words":normalized,"speaker_segments":sorted(segments,key=lambda x:(x["start_ms"],x["end_ms"],x["segment_id"])),"coverage":{"eligible_word_count":len(normalized),"included_word_count":len(normalized),"excluded_word_count":0},"limitations":[]}
        object_id=semantic_id("ie:transcript-alignment",core); payload={"alignment_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("transcript_alignment",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
        self.repository.add_edge(source_ref["object_id"],object_id,"source_of_transcript")
        return result

    def pack_phrases(self, alignment_ref: Mapping[str,Any], *, policy: Mapping[str,Any], idempotency_key: str) -> dict[str,Any]:
        ref=require_ref(alignment_ref,"alignment_ref"); alignment=self.repository.get_object(ref["object_id"])["payload"]
        if alignment["source_package_ref"]["sha256"] != self.repository.get_object_by_sha(alignment["source_package_ref"]["object_id"], alignment["source_package_ref"]["sha256"])["sha256"]: raise ValidationError("source package drift")
        required={"policy_id","max_words","max_gap_ms","break_on_terminal_punctuation"}
        if set(policy)!=required: raise ValidationError("phrase policy shape invalid")
        max_words=require_int(policy["max_words"],"max_words",minimum=1); max_gap=require_int(policy["max_gap_ms"],"max_gap_ms",minimum=0); break_punct=bool(policy["break_on_terminal_punctuation"])
        phrases=[]; current=[]
        def flush():
            nonlocal current
            if not current: return
            core={"source_package_ref":alignment["source_package_ref"],"speaker_id":current[0]["speaker_id"],"start_ms":current[0]["start_ms"],"end_ms":current[-1]["end_ms"],"word_refs":[x["word_id"] for x in current],"text":" ".join(x["text"] for x in current),"hesitation_word_refs":[x["word_id"] for x in current if x["text"].lower().strip('.,!?') in HESITATIONS],"tag_refs":sorted({r["object_id"] for x in current for r in x["tag_refs"]}),"event_refs":sorted({r["object_id"] for x in current for r in x["event_refs"]})}
            phrases.append({"phrase_id":semantic_id("ie:phrase",core),"index":len(phrases),**core}); current=[]
        for word in alignment["words"]:
            if current and (word["speaker_id"]!=current[-1]["speaker_id"] or word["start_ms"]-current[-1]["end_ms"]>max_gap or len(current)>=max_words): flush()
            current.append(word)
            if break_punct and word["text"].rstrip().endswith((".","?","!")): flush()
        flush()
        covered=[w for p in phrases for w in p["word_refs"]]
        expected=[w["word_id"] for w in alignment["words"]]
        if covered!=expected: raise ValidationError("phrase pack does not cover every word exactly once")
        core={"alignment_ref":ref,"source_package_ref":alignment["source_package_ref"],"policy":dict(policy),"phrases":phrases,"coverage":{"word_count":len(expected),"covered_word_count":len(covered),"complete":True},"transformations":["WHITESPACE_JOIN_ONLY"],"semantic_meaning_owner":"NOT_INTERVIEW_EXPRESSION"}
        object_id=semantic_id("ie:phrase-pack",core); payload={"phrase_pack_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("packed_phrase_transcript",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
        self.repository.add_edge(ref["object_id"],object_id,"compiled_into_phrase_pack")
        return result
