from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .canonical import require_enum, require_ref, require_source_span, require_string, semantic_id
from .domain import EPISTEMIC_STATES, make_tag_assertion
from .errors import AuthorityError, StateError, ValidationError
from .repository import InterviewRepository

class ExpressionGovernanceService:
    def __init__(self, repository: InterviewRepository): self.repository=repository

    def create_tag(self, *, source_package_ref: Mapping[str,Any], tag: str, epistemic_state: str, source_spans: list[Mapping[str,Any]], actor_id: str, evidence_refs: list[Mapping[str,Any]], rationale: str, idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref)
        package=self.repository.get_object(source_ref["object_id"])["payload"]
        if package["admission_mode"]=="IMPORTED" and epistemic_state=="PLANNED": raise ValidationError("imported source cannot fabricate planned tags")
        payload=make_tag_assertion(tag=tag,epistemic_state=epistemic_state,source_spans=source_spans,actor_id=actor_id,evidence_refs=evidence_refs,rationale=rationale)
        payload={"version":"1.0.0","source_package_ref":source_ref,**payload}
        result=self.repository.store_object("tag_assertion",payload,object_id=payload["tag_assertion_id"],idempotency_key=idempotency_key,lifecycle_state=epistemic_state)
        self.repository.add_edge(source_ref["object_id"],payload["tag_assertion_id"],"source_of_tag_assertion")
        return result

    def create_anchor_hit(self, *, source_package_ref: Mapping[str,Any], phrase_refs: list[Mapping[str,Any]], source_spans: list[Mapping[str,Any]], anchor_kind: str, epistemic_state: str, evidence_refs: list[Mapping[str,Any]], actor_id: str, idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref); phrases=[require_ref(r) for r in phrase_refs]; evidence=[require_ref(r) for r in evidence_refs]
        core={"source_package_ref":source_ref,"phrase_refs":sorted(phrases,key=lambda x:x["object_id"]),"source_spans":[require_source_span(s) for s in source_spans],"anchor_kind":require_string(anchor_kind,"anchor_kind"),"epistemic_state":require_enum(epistemic_state,EPISTEMIC_STATES,"epistemic_state"),"evidence_refs":sorted(evidence,key=lambda x:x["object_id"]),"actor_id":require_string(actor_id,"actor_id")}
        object_id=semantic_id("ie:anchor-hit",core); payload={"anchor_hit_id":object_id,"version":"1.0.0",**core}
        result=self.repository.store_object("anchor_hit",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state=epistemic_state)
        return result

    def propose_moment(self, *, source_package_ref: Mapping[str,Any], phrase_refs: list[Mapping[str,Any]], source_spans: list[Mapping[str,Any]], keyframe_refs: list[Mapping[str,Any]], reaction_receipt_refs: list[Mapping[str,Any]], candidate_reason: str, proposer_id: str, idempotency_key: str) -> dict[str,Any]:
        source_ref=require_ref(source_package_ref); phrases=[require_ref(r) for r in phrase_refs]
        if not phrases: raise ValidationError("Expression Moment requires phrase evidence")
        core={"source_package_ref":source_ref,"phrase_refs":sorted(phrases,key=lambda x:x["object_id"]),"source_spans":[require_source_span(s) for s in source_spans],"keyframe_refs":sorted([require_ref(r) for r in keyframe_refs],key=lambda x:x["object_id"]),"reaction_receipt_refs":sorted([require_ref(r) for r in reaction_receipt_refs],key=lambda x:x["object_id"]),"candidate_reason":require_string(candidate_reason,"candidate_reason"),"proposer_id":require_string(proposer_id,"proposer_id"),"lifecycle_state":"CANDIDATE","epistemic_state":"INFERRED","operator_approved":False}
        object_id=semantic_id("ie:expression-moment",core); payload={"expression_moment_id":object_id,"version":"1.0.0",**core}
        return self.repository.store_object("expression_moment",payload,object_id=object_id,idempotency_key=idempotency_key,lifecycle_state="CANDIDATE")

    def decide_moment(self, moment_id: str, *, decision: str, operator_id: str, rationale: str, idempotency_key: str) -> dict[str,Any]:
        decision=require_enum(decision,{"APPROVE","REJECT"},"decision")
        current=self.repository.get_object(moment_id); payload=dict(current["payload"])
        if payload["lifecycle_state"]!="CANDIDATE": raise StateError("only candidate moment may be decided")
        payload["operator_id"]=require_string(operator_id,"operator_id"); payload["operator_rationale"]=require_string(rationale,"rationale")
        payload["lifecycle_state"]="APPROVED" if decision=="APPROVE" else "REJECTED"
        payload["epistemic_state"]="OPERATOR_CONFIRMED" if decision=="APPROVE" else "REJECTED"
        payload["operator_approved"]=decision=="APPROVE"
        return self.repository.store_object("expression_moment",payload,object_id=moment_id,idempotency_key=idempotency_key,lifecycle_state=payload["lifecycle_state"],expected_revision=current["revision"])

    def approved_moments(self, source_package_id: str) -> list[dict[str,Any]]:
        return [o for o in self.repository.list_objects("expression_moment") if o["payload"]["source_package_ref"]["object_id"]==source_package_id and o["payload"]["lifecycle_state"]=="APPROVED"]
