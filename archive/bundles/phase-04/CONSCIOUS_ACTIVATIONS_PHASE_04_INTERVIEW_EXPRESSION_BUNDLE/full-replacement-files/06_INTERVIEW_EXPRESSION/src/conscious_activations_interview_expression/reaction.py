from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_enum, require_int, require_ref, require_source_span, require_string, semantic_id
from .domain import EPISTEMIC_STATES, MODALITY_STATES, REACTION_OUTCOMES
from .errors import EvidenceGapError, ValidationError
from .repository import InterviewRepository

class ReactionEvidenceService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def record_observation(self, *, source_package_ref: Mapping[str,Any], trigger_ref: Mapping[str,Any] | str, source_spans: list[Mapping[str,Any]], modality_coverage: Mapping[str,Any], observation_kind: str, epistemic_state: str, actor_id: str, value: Mapping[str,Any], idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref,"source_package_ref")
        spans=[require_source_span(s,f"source_spans[{i}]") for i,s in enumerate(source_spans)]
        coverage={}
        for key in ["audio","video","transcript","operator_observation"]:
            if key not in modality_coverage: raise ValidationError("modality coverage incomplete")
            coverage[key]=require_enum(modality_coverage[key],MODALITY_STATES,f"modality_coverage.{key}")
        if all(v=="ABSENT_NOT_CAPTURED" for v in coverage.values()): raise EvidenceGapError("no modality captured")
        trigger="NOT_APPLICABLE" if trigger_ref=="NOT_APPLICABLE" else require_ref(trigger_ref,"trigger_ref")
        core={"source_package_ref":source_ref,"trigger_ref":trigger,"source_spans":sorted(spans,key=lambda x:(x["start_ms"],x["end_ms"])),"modality_coverage":coverage,"observation_kind":require_string(observation_kind,"observation_kind"),"epistemic_state":require_enum(epistemic_state,EPISTEMIC_STATES,"epistemic_state"),"actor_id":require_string(actor_id,"actor_id"),"value":dict(value)}
        object_id=semantic_id("ie:reaction-observation",core); payload={"observation_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("reaction_observation",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="RECORDED")
        self.repository.add_edge(source_ref["object_id"],object_id,"source_of_reaction_observation")
        return result

    def create_receipt(self, *, source_package_ref: Mapping[str,Any], delivered_call_ref: Mapping[str,Any] | str, pressure_decision_ref: Mapping[str,Any] | str, observation_refs: list[Mapping[str,Any]], outcome: str, counteractivation: Mapping[str,Any], uncertainty: Mapping[str,Any], evaluator_id: str, producer_id: str, planned_observed_delta: Mapping[str,Any], alternatives: list[str], idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref); observations=[require_ref(r) for r in observation_refs]
        if not observations: raise ValidationError("Reaction Receipt requires observation refs")
        outcome=require_enum(outcome,REACTION_OUTCOMES,"outcome")
        if evaluator_id==producer_id: raise ValidationError("independent evaluator must differ from producer")
        obs_payloads=[self.repository.get_object(r["object_id"])["payload"] for r in observations]
        all_absent=all(all(v=="ABSENT_NOT_CAPTURED" for v in o["modality_coverage"].values()) for o in obs_payloads)
        if all_absent: raise EvidenceGapError("capture gap cannot become a reaction outcome")
        if outcome=="SILENCE" and not any(o["observation_kind"]=="SILENCE_EVENT" for o in obs_payloads): raise ValidationError("SILENCE outcome requires observed silence event")
        call_ref="NOT_APPLICABLE" if delivered_call_ref=="NOT_APPLICABLE" else require_ref(delivered_call_ref)
        pressure_ref="NOT_APPLICABLE" if pressure_decision_ref=="NOT_APPLICABLE" else require_ref(pressure_decision_ref)
        core={"source_package_ref":source_ref,"delivered_call_ref":call_ref,"pressure_decision_ref":pressure_ref,"observation_refs":sorted(observations,key=lambda x:x["object_id"]),"outcome":outcome,"counteractivation":dict(counteractivation),"uncertainty":dict(uncertainty),"planned_observed_delta":dict(planned_observed_delta),"alternative_outcomes":sorted([require_enum(a,REACTION_OUTCOMES,"alternative") for a in alternatives]),"producer_id":require_string(producer_id,"producer_id"),"evaluator_id":require_string(evaluator_id,"evaluator_id"),"evaluator_independent":True,"maximum_claim":"SOURCE_LINKED_REACTION_EVIDENCE","expression_moment_auto_approved":False}
        object_id=semantic_id("ie:reaction-receipt",core); payload={"reaction_receipt_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("reaction_receipt",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="VALIDATED")
        for r in observations: self.repository.add_edge(r["object_id"],object_id,"supports_reaction_receipt")
        self.repository.add_edge(source_ref["object_id"],object_id,"source_of_reaction_receipt")
        return result
