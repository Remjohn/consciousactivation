from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for p in reversed([
 ROOT/'packages/ca_contracts/src', ROOT/'packages/ca_runtime/src',
 ROOT/'04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src', ROOT/'05_ATOMIC_HARNESS_PIPELINE/src',
 ROOT/'06_INTERVIEW_EXPRESSION/src']):
 s=str(p)
 if s not in sys.path: sys.path.insert(0,s)

from ca_contracts import bytes_sha256
from conscious_activations_interview_expression.application import InterviewExpressionApplication
from conscious_activations_interview_expression.domain import make_media_asset, make_source_span

AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}

def base(object_id_field: str, object_id: str, *, epistemic: bool = True, lifecycle: bool = True) -> dict[str, object]:
    value: dict[str, object] = {object_id_field: object_id, "version": "1.0.0", "authority": dict(AUTHORITY)}
    if lifecycle:
        value["lifecycle_state"] = "approved"
    if epistemic:
        value["epistemic_state"] = "operator_confirmed"
    return value

def ref(value, sha: str | None = None, version: str = "1.0.0"):
    if isinstance(value, str):
        return {"object_id": value, "version": version, "sha256": sha or ("f" * 64)}
    stored = value
    o = stored["object"] if "object" in stored else stored
    return {"object_id": o["object_id"], "version": o["version"], "sha256": o["sha256"]}

def imported_app(tmp_path):
 app=InterviewExpressionApplication(tmp_path/'ie.sqlite3'); app.initialize()
 data=b'fixture-talking-head-media'
 media=make_media_asset(logical_uri='workspace://fixture/interview.mp4',sha256=bytes_sha256(data),bytes_count=len(data),media_type='video/mp4',technical={'probe_status':'DECLARED_TEST','duration_ms':6000,'streams':[{'index':0,'codec_type':'video','codec_name':'fixture','width':1080,'height':1920}], 'limitations':['TEST_FIXTURE']})
 admitted=app.source_packages.admit({'workspace_id':'ws','project_id':'prj','admission_mode':'IMPORTED','source_kind':'INTERVIEW_EXPRESSION','media_assets':[media],'source_authority':{'operator_id':'op','authority_scope':'DEVELOPMENT_TEST','assertion_id':'assert-1'},'planning_lineage':{'state':'ABSENT_NOT_CREATED'}},idempotency_key='admit')
 return app, ref(admitted), admitted

def words():
 texts=['I','thought','success','meant','control.','Um','then','I','learned','to','listen.']
 return [{'word_id':f'w-{i:03d}','index':i,'text':t,'start_ms':i*300,'end_ms':i*300+240,'speaker_id':'guest','speaker_state':'RESOLVED','epistemic_state':'OBSERVED','tag_refs':[],'event_refs':[]} for i,t in enumerate(texts)]

def build_transcript(app, package_ref):
 aligned=app.transcripts.align(source_package_ref=package_ref,words=words(),speaker_segments=[{'segment_id':'seg-1','start_ms':0,'end_ms':3500,'speaker_id':'guest','speaker_state':'RESOLVED'}],policy_id='align-v1',idempotency_key='align')
 ar=ref(aligned)
 packed=app.transcripts.pack_phrases(ar,policy={'policy_id':'pack-v1','max_words':7,'max_gap_ms':500,'break_on_terminal_punctuation':True},idempotency_key='pack')
 pr=ref(packed)
 app.source_packages.bind_component(package_ref['object_id'],'transcript_alignment',ar,idempotency_key='bind-a')
 app.source_packages.bind_component(package_ref['object_id'],'packed_phrase_transcript',pr,idempotency_key='bind-p')
 return aligned, packed, ar, pr

def build_visual(app, package_ref):
 v=app.visual.compile(source_package_ref=package_ref,duration_ms=6000,shots=[{'shot_id':'s0','start_ms':0,'end_ms':3000,'transition_in':'SOURCE_START','transition_out':'HARD_CUT'},{'shot_id':'s1','start_ms':3000,'end_ms':6000,'transition_in':'HARD_CUT','transition_out':'SOURCE_END'}],keyframe_candidates=[{'candidate_id':'k0','timestamp_ms':1500,'frame_number':45,'score':80,'logical_uri':'artifact://k0.png','sha256':'c'*64},{'candidate_id':'k1','timestamp_ms':4500,'frame_number':135,'score':90,'logical_uri':'artifact://k1.png','sha256':'d'*64}],profile_id='talking-head-v1',idempotency_key='visual')
 vr=ref(v);app.source_packages.bind_component(package_ref['object_id'],'visual_structure_index',vr,idempotency_key='bind-v')
 return v,vr
