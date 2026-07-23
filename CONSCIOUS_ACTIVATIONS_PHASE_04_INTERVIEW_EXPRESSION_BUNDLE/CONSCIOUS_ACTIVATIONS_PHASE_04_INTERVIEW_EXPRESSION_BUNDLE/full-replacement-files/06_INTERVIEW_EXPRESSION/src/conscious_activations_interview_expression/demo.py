from __future__ import annotations
from pathlib import Path
from typing import Any
from ca_contracts import bytes_sha256
from .application import InterviewExpressionApplication
from .domain import make_media_asset, make_source_span
from .source_package import SourcePackageService


def _ref(stored):
    o=stored["object"] if "object" in stored else stored
    return {"object_id":o["object_id"],"version":o["version"],"sha256":o["sha256"]}

def run_demo(database_path: str|Path) -> dict[str,Any]:
    app=InterviewExpressionApplication(database_path); app.initialize()
    media_bytes=b"phase4-synthetic-talking-head-source"
    media=make_media_asset(logical_uri="workspace://demo/interview.mp4",sha256=bytes_sha256(media_bytes),bytes_count=len(media_bytes),media_type="video/mp4",technical={"probe_status":"SYNTHETIC_DECLARED","duration_ms":5000,"streams":[{"index":0,"codec_type":"video","codec_name":"fixture","width":1080,"height":1920}],"limitations":["SYNTHETIC_DEVELOPMENT_FIXTURE"]})
    admitted=app.source_packages.admit({"workspace_id":"demo-workspace","project_id":"demo-project","admission_mode":"IMPORTED","source_kind":"INTERVIEW_EXPRESSION","media_assets":[media],"source_authority":{"operator_id":"demo-operator","authority_scope":"DEVELOPMENT_FIXTURE","assertion_id":"demo-authority-001"},"planning_lineage":{"state":"ABSENT_NOT_CREATED"}},idempotency_key="demo:admit")
    package_ref=_ref(admitted)
    words=[]
    texts=["I","thought","success","meant","control.","Um","then","I","learned","to","listen."]
    for i,text in enumerate(texts):
        words.append({"word_id":f"word-{i:03d}","index":i,"text":text,"start_ms":i*300,"end_ms":i*300+240,"speaker_id":"guest","speaker_state":"RESOLVED","epistemic_state":"OBSERVED","tag_refs":[],"event_refs":[]})
    aligned=app.transcripts.align(source_package_ref=package_ref,words=words,speaker_segments=[{"segment_id":"speaker-guest","start_ms":0,"end_ms":3500,"speaker_id":"guest","speaker_state":"RESOLVED"}],policy_id="exact-word-alignment-v1",idempotency_key="demo:align")
    alignment_ref=_ref(aligned)
    packed=app.transcripts.pack_phrases(alignment_ref,policy={"policy_id":"phrase-v1","max_words":7,"max_gap_ms":500,"break_on_terminal_punctuation":True},idempotency_key="demo:pack")
    phrase_ref=_ref(packed)
    app.source_packages.bind_component(package_ref["object_id"],"transcript_alignment",alignment_ref,idempotency_key="demo:bind-alignment")
    app.source_packages.bind_component(package_ref["object_id"],"packed_phrase_transcript",phrase_ref,idempotency_key="demo:bind-phrases")
    visual=app.visual.compile(source_package_ref=package_ref,duration_ms=5000,shots=[{"shot_id":"shot-0","start_ms":0,"end_ms":5000,"transition_in":"SOURCE_START","transition_out":"SOURCE_END"}],keyframe_candidates=[{"candidate_id":"keyframe-0","timestamp_ms":1800,"frame_number":54,"score":90,"logical_uri":"artifact://demo/keyframe-0.png","sha256":"c"*64}],profile_id="talking-head-vertical-v1",idempotency_key="demo:visual")
    visual_ref=_ref(visual); app.source_packages.bind_component(package_ref["object_id"],"visual_structure_index",visual_ref,idempotency_key="demo:bind-visual")
    span=make_source_span(source_ref=package_ref,start_ms=1500,end_ms=3500,speaker_id="guest")
    observation=app.reactions.record_observation(source_package_ref=package_ref,trigger_ref="NOT_APPLICABLE",source_spans=[span],modality_coverage={"audio":"PRESENT","video":"PRESENT","transcript":"PRESENT","operator_observation":"PRESENT"},observation_kind="STATE_CHANGE_OBSERVED",epistemic_state="OBSERVED",actor_id="demo-observer",value={"description":"hesitation followed by reframing"},idempotency_key="demo:observation")
    observation_ref=_ref(observation)
    reaction=app.reactions.create_receipt(source_package_ref=package_ref,delivered_call_ref="NOT_APPLICABLE",pressure_decision_ref="NOT_APPLICABLE",observation_refs=[observation_ref],outcome="STATE_TRANSITION",counteractivation={"state":"NOT_OBSERVED"},uncertainty={"level":"LOW"},evaluator_id="demo-independent-evaluator",producer_id="demo-observer",planned_observed_delta={"planning_state":"ABSENT_NOT_CREATED"},alternatives=["UNEXPECTED_EDGE"],idempotency_key="demo:reaction")
    reaction_ref=_ref(reaction)
    phrase=packed["object"]["payload"]["phrases"][-1]
    phrase_obj={"phrase_id":phrase["phrase_id"],"version":"1.0.0",**phrase}
    phrase_stored=app.repository.store_object("packed_phrase",phrase_obj,object_id=phrase["phrase_id"],idempotency_key="demo:phrase-object",lifecycle_state="VALIDATED")
    phrase_item_ref=_ref(phrase_stored)
    moment=app.expression.propose_moment(source_package_ref=package_ref,phrase_refs=[phrase_item_ref],source_spans=[span],keyframe_refs=[{"object_id":"keyframe-0","version":"1.0.0","sha256":"c"*64}],reaction_receipt_refs=[reaction_ref],candidate_reason="source-backed perspective shift",proposer_id="demo-hunter",idempotency_key="demo:moment")
    approved=app.expression.decide_moment(moment["object"]["object_id"],decision="APPROVE",operator_id="demo-operator",rationale="preserves genuine guest expression",idempotency_key="demo:approve")
    moment_ref=_ref(approved)
    inventory=app.inventory.compile(source_package_ref=package_ref,expression_moment_refs=[moment_ref],phrase_pack_ref=phrase_ref,visual_index_ref=visual_ref,reaction_receipt_refs=[reaction_ref],idempotency_key="demo:inventory")
    inventory_ref=_ref(inventory)
    observed=app.inventory.observed_evidence_pack(source_package_ref=package_ref,expression_moment_refs=[moment_ref],reaction_receipt_refs=[reaction_ref],tag_assertion_refs=[],idempotency_key="demo:observed")
    observed_ref=_ref(observed)
    app.source_packages.bind_component(package_ref["object_id"],"reaction_receipts",reaction_ref,idempotency_key="demo:bind-reaction")
    app.source_packages.bind_component(package_ref["object_id"],"expression_moments",moment_ref,idempotency_key="demo:bind-moment")
    app.source_packages.bind_component(package_ref["object_id"],"asset_package_spec",inventory_ref,idempotency_key="demo:bind-inventory")
    app.source_packages.bind_component(package_ref["object_id"],"observed_evidence_pack",observed_ref,idempotency_key="demo:bind-observed")
    published=app.source_packages.publish(package_ref["object_id"],archive_only=False,idempotency_key="demo:publish")
    return {"source_package":published["object"],"alignment_ref":alignment_ref,"phrase_pack_ref":phrase_ref,"visual_index_ref":visual_ref,"reaction_receipt_ref":reaction_ref,"expression_moment_ref":moment_ref,"asset_package_spec_ref":inventory_ref,"observed_evidence_pack_ref":observed_ref,"health":app.repository.health(),"claim_ceiling":"PHASE_04_INTERVIEW_EXPRESSION_DEVELOPMENT_EVIDENCE","production_authorized":False,"certified":False,"format02_activated":False}
