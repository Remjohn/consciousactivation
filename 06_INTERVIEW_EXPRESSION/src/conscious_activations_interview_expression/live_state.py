from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_enum, require_int, require_ref, require_string, semantic_id
from .domain import CALL_ORIGINS, SESSION_STATES
from .errors import AuthorityError, StateError, ValidationError
from .repository import InterviewRepository

class LiveSessionService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def start(self, *, source_package_ref: Mapping[str,Any], iac_ref: Mapping[str,Any], binding_ref: Mapping[str,Any], interviewer_id: str, allowed_actions: list[str], idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref); iac=require_ref(iac_ref); binding=require_ref(binding_ref)
        actions=sorted({require_string(a,"allowed_action") for a in allowed_actions})
        for required in ["RESET","LAND","STOP","CANCEL"]:
            if required not in actions: raise ValidationError("live session must preserve reset, land, stop and cancel")
        core={"source_package_ref":source_ref,"iac_ref":iac,"binding_ref":binding,"interviewer_id":require_string(interviewer_id,"interviewer_id"),"allowed_actions":actions}
        session_id=semantic_id("ie:live-session",core)
        snapshot={"session_id":session_id,"state":"ACTIVE","sequence":1,"source_package_ref":source_ref,"iac_ref":iac,"binding_ref":binding,"interviewer_id":interviewer_id,"acknowledged_proposal_refs":[],"delivered_call_refs":[],"reaction_refs":[],"pressure_history":[],"anchor_state":"UNOBSERVED","landing_state":"UNOBSERVED","target_distance":"UNKNOWN","lawful_next_actions":actions,"unresolved_assertions":[]}
        return self.repository.append_event(aggregate_id=session_id,event_type="SESSION_STARTED",payload=core,snapshot=snapshot,expected_sequence=0,idempotency_key=idempotency_key)

    def _current(self, session_id: str) -> tuple[int,dict[str,Any]]:
        snap=self.repository.latest_snapshot(session_id)
        if snap is None: raise StateError("session not found")
        return snap["sequence"],dict(snap["snapshot"])

    def acknowledge_air_proposal(self, session_id: str, *, proposal_ref: Mapping[str,Any], snapshot_ref: Mapping[str,Any], observation_watermark: int, idempotency_key: str) -> dict[str,Any]:
        seq,s=self._current(session_id)
        if s["state"]!="ACTIVE": raise StateError("session not active")
        if observation_watermark!=seq: raise StateError("STALE_AIR_POLICY")
        proposal=require_ref(proposal_ref); current_snapshot=require_ref(snapshot_ref)
        if current_snapshot["sha256"]!=self.repository.latest_snapshot(session_id)["sha256"]: raise StateError("STALE_AIR_POLICY")
        s["acknowledged_proposal_refs"]=sorted(s["acknowledged_proposal_refs"]+[proposal],key=lambda x:x["object_id"]); s["sequence"]=seq+1
        return self.repository.append_event(aggregate_id=session_id,event_type="AIR_PROPOSAL_ACKNOWLEDGED",payload={"proposal_ref":proposal,"observation_watermark":observation_watermark},snapshot=s,expected_sequence=seq,idempotency_key=idempotency_key)

    def deliver_call(self, session_id: str, *, origin: str, exact_expression: str, actor_id: str, proposal_ref: Mapping[str,Any] | str, pressure_units: int, idempotency_key: str) -> dict[str,Any]:
        seq,s=self._current(session_id)
        if s["state"]!="ACTIVE": raise StateError("delivery requires ACTIVE session")
        origin=require_enum(origin,CALL_ORIGINS,"origin")
        proposal="NOT_APPLICABLE" if proposal_ref=="NOT_APPLICABLE" else require_ref(proposal_ref)
        if origin=="SPONTANEOUS_HUMAN" and proposal!="NOT_APPLICABLE": raise ValidationError("spontaneous human delivery cannot carry AIR proposal ref")
        if origin.startswith("AIR_") and proposal=="NOT_APPLICABLE": raise ValidationError("AIR-origin delivery requires proposal ref")
        pressure=require_int(pressure_units,"pressure_units",minimum=0)
        core={"session_id":session_id,"origin":origin,"exact_delivered_expression":require_string(exact_expression,"exact_expression"),"actor_id":require_string(actor_id,"actor_id"),"proposal_ref":proposal,"pressure_units":pressure}
        call_id=semantic_id("ie:delivered-call",core); payload={"delivered_call_id":call_id,"version":"1.0.0",**core}
        stored=self.repository.store_object("delivered_call",payload,object_id=call_id,idempotency_key=f"{idempotency_key}:object",lifecycle_state="DELIVERED")
        call_ref={"object_id":call_id,"version":"1.0.0","sha256":stored["object"]["sha256"]}
        s["delivered_call_refs"]=s["delivered_call_refs"]+[call_ref]; s["pressure_history"]=s["pressure_history"]+[{"call_ref":call_ref,"pressure_units":pressure,"actor_id":actor_id}]; s["sequence"]=seq+1
        return self.repository.append_event(aggregate_id=session_id,event_type="CALL_DELIVERED",payload={"call_ref":call_ref,"origin":origin,"pressure_units":pressure},snapshot=s,expected_sequence=seq,idempotency_key=idempotency_key)

    def record_interviewer_reaction(self, session_id: str, *, reaction_text: str, actor_id: str, human_attested: bool, evidence_refs: list[Mapping[str,Any]], idempotency_key: str) -> dict[str,Any]:
        if not human_attested: raise AuthorityError("interviewer reaction requires human attestation")
        seq,s=self._current(session_id)
        core={"session_id":session_id,"reaction_text":require_string(reaction_text,"reaction_text"),"actor_id":require_string(actor_id,"actor_id"),"human_attested":True,"evidence_refs":sorted([require_ref(r) for r in evidence_refs],key=lambda x:x["object_id"])}
        rid=semantic_id("ie:interviewer-reaction",core); payload={"interviewer_reaction_id":rid,"version":"1.0.0",**core}
        stored=self.repository.store_object("interviewer_reaction",payload,object_id=rid,idempotency_key=f"{idempotency_key}:object",lifecycle_state="HUMAN_ATTESTED")
        ref={"object_id":rid,"version":"1.0.0","sha256":stored["object"]["sha256"]}
        s["reaction_refs"]=s["reaction_refs"]+[ref]; s["sequence"]=seq+1
        return self.repository.append_event(aggregate_id=session_id,event_type="INTERVIEWER_REACTION_RECORDED",payload={"reaction_ref":ref},snapshot=s,expected_sequence=seq,idempotency_key=idempotency_key)

    def transition(self, session_id: str, *, action: str, actor_id: str, evidence_refs: list[Mapping[str,Any]], idempotency_key: str) -> dict[str,Any]:
        seq,s=self._current(session_id); action=require_enum(action,{"PAUSE","RESUME","RESET","LAND","STOP","CANCEL"},"action")
        current=s["state"]
        if current in {"LANDED","STOPPED","CANCELLED"}: raise StateError("terminal session rejects transitions")
        if action=="RESUME" and current!="PAUSED": raise StateError("resume requires PAUSED")
        if action!="RESUME" and current=="PAUSED" and action not in {"STOP","CANCEL"}: raise StateError("paused session only permits resume, stop or cancel")
        mapping={"PAUSE":"PAUSED","RESUME":"ACTIVE","RESET":"ACTIVE","LAND":"LANDED","STOP":"STOPPED","CANCEL":"CANCELLED"}
        s["state"]=mapping[action]
        if action=="RESET": s["anchor_state"]="UNOBSERVED"; s["target_distance"]="UNKNOWN"
        if action=="LAND": s["landing_state"]="RECORDED_WITHOUT_OUTCOME_CLAIM"
        s["sequence"]=seq+1
        return self.repository.append_event(aggregate_id=session_id,event_type=f"SESSION_{action}",payload={"actor_id":require_string(actor_id,"actor_id"),"evidence_refs":sorted([require_ref(r) for r in evidence_refs],key=lambda x:x["object_id"])},snapshot=s,expected_sequence=seq,idempotency_key=idempotency_key)

    def replay(self, session_id: str) -> dict[str,Any]:
        events=self.repository.events(session_id); snap=self.repository.latest_snapshot(session_id)
        if not events or snap is None: raise StateError("session has no events")
        previous=None
        for e in events:
            if e["previous_event_sha256"]!=previous: raise StateError("event hash chain broken")
            previous=e["payload_sha256"]
        return {"session_id":session_id,"event_count":len(events),"head_sequence":snap["sequence"],"snapshot_sha256":snap["sha256"],"snapshot":snap["snapshot"],"hash_chain_valid":True}
