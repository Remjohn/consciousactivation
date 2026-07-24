from __future__ import annotations

from typing import Any, Mapping, Sequence

from ca_contracts import canonical_sha256

from ..production_domain import EVALUATION_DIMENSIONS, HYPOTHESIS_GATES
from ..repositories.air_repository import AirRepository
from .production_common import add_lineage_edges, require_air_ref
from .semantic_authority import SemanticAuthorityService


class HypothesisService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    @staticmethod
    def diversity_proof(axes: Mapping[str, str]) -> str:
        return canonical_sha256(dict(sorted(axes.items())))

    def store_hypothesis(self, payload: Mapping[str, Any], *, idempotency_key: str, expected_revision: int | None = None) -> dict[str, Any]:
        normalized = self.semantic.validate("activation_hypothesis", payload)
        require_air_ref(self.repository, normalized["matrix_of_edging_ref"], object_types="matrix_of_edging")
        expected = self.diversity_proof(normalized["diversity_signature"]["axes"])
        if normalized["diversity_signature"]["proof_sha256"] != expected:
            raise ValueError("diversity_signature.proof_sha256 does not match axes")
        for ref in normalized["primitive_application_refs"]:
            require_air_ref(self.repository, ref, object_types="primitive_binding")
        result = self.semantic.store("activation_hypothesis", normalized, idempotency_key=idempotency_key, expected_revision=expected_revision)
        add_lineage_edges(self.repository, source_result=result, relation_type="derived_from", target_refs=[normalized["matrix_of_edging_ref"], *normalized["source_refs"], *normalized["primitive_application_refs"]], evidence={"service":"hypothesis","phase":"PHASE_05"})
        return result

    def store_portfolio(self, payload: Mapping[str, Any], *, idempotency_key: str, expected_revision: int | None = None) -> dict[str, Any]:
        normalized = self.semantic.validate("activation_hypothesis_portfolio", payload)
        signatures: set[str] = set()
        for ref in normalized["candidate_refs"]:
            candidate = require_air_ref(self.repository, ref, object_types="activation_hypothesis")
            proof = str(candidate.payload["diversity_signature"]["proof_sha256"])
            if proof in signatures:
                raise ValueError("portfolio contains semantically duplicate diversity signatures")
            signatures.add(proof)
        result = self.semantic.store("activation_hypothesis_portfolio", normalized, idempotency_key=idempotency_key, expected_revision=expected_revision)
        add_lineage_edges(self.repository, source_result=result, relation_type="contains_candidate", target_refs=normalized["candidate_refs"], evidence={"service":"hypothesis_portfolio","phase":"PHASE_05"})
        return result

    def gate_hypothesis(self, *, receipt_id: str, version: str, authority: Mapping[str, Any], portfolio_ref: Mapping[str, Any], hypothesis_ref: Mapping[str, Any], gate_profile_ref: Mapping[str, Any], evaluator_actor_id: str, producer_actor_id: str, outcomes: Mapping[str, bool], evidence_refs: Sequence[Mapping[str, Any]], idempotency_key: str) -> dict[str, Any]:
        require_air_ref(self.repository, portfolio_ref, object_types="activation_hypothesis_portfolio")
        hypothesis = require_air_ref(self.repository, hypothesis_ref, object_types="activation_hypothesis")
        if set(outcomes) != set(HYPOTHESIS_GATES):
            raise ValueError("outcomes must cover all hypothesis gates exactly once")
        checks=[]
        for gate in HYPOTHESIS_GATES:
            checks.append({"gate":gate,"applicability":"APPLIES","verdict":"PASS" if outcomes[gate] else "FAIL","reason":f"deterministic development check for {gate}","evidence_refs":list(evidence_refs)})
        overall="ELIGIBLE" if all(outcomes.values()) else "INELIGIBLE"
        payload={"receipt_id":receipt_id,"version":version,"authority":dict(authority),"portfolio_ref":dict(portfolio_ref),"hypothesis_ref":dict(hypothesis_ref),"gate_profile_ref":dict(gate_profile_ref),"evaluator_actor_id":evaluator_actor_id,"producer_actor_id":producer_actor_id,"checks":checks,"overall":overall,"input_hashes":[hypothesis.canonical_sha256, canonical_sha256(outcomes)],"limitations":["development-only deterministic gate"]}
        return self.semantic.store("hypothesis_gate_result", payload, idempotency_key=idempotency_key)

    def compare_portfolio(self, *, receipt_id: str, version: str, authority: Mapping[str, Any], portfolio_ref: Mapping[str, Any], evaluation_profile_ref: Mapping[str, Any], evaluator_actor_id: str, producer_actor_ids: Sequence[str], gate_receipt_refs: Sequence[Mapping[str, Any]], candidate_scores: Mapping[str, Mapping[str, int]], decisive_margin_micros: int, idempotency_key: str) -> dict[str, Any]:
        portfolio=require_air_ref(self.repository,portfolio_ref,object_types="activation_hypothesis_portfolio")
        eligibility={}
        for ref in gate_receipt_refs:
            gate=require_air_ref(self.repository,ref,object_types="hypothesis_gate_result")
            eligibility[gate.payload["hypothesis_ref"]["object_id"]]=gate.payload["overall"]=="ELIGIBLE"
        ids=[r["object_id"] for r in portfolio.payload["candidate_refs"]]
        if set(ids)!=set(candidate_scores) or set(ids)!=set(eligibility): raise ValueError("scores and gate receipts must cover every candidate")
        rows=[]
        for cid in ids:
            scores=dict(candidate_scores[cid])
            if set(scores)!=set(EVALUATION_DIMENSIONS): raise ValueError("dimension scores incomplete")
            if any(not isinstance(v,int) or isinstance(v,bool) or v<0 or v>1_000_000 for v in scores.values()): raise ValueError("scores must be integer micros")
            obj=self.repository.get_object(cid); rows.append({"hypothesis_ref":obj.immutable_ref(),"dimension_scores_micros":scores,"total_micros":sum(scores.values()),"eligible":eligibility[cid]})
        eligible=sorted([r for r in rows if r["eligible"]],key=lambda r:(-r["total_micros"],r["hypothesis_ref"]["object_id"]))
        selected=None
        if not eligible: decision="NO_ELIGIBLE_CANDIDATE"
        elif len(eligible)==1 or eligible[0]["total_micros"]-eligible[1]["total_micros"]>=decisive_margin_micros:
            decision="DECISIVE_WINNER"; selected=eligible[0]["hypothesis_ref"]
        else: decision="AMBIGUOUS"
        payload={"receipt_id":receipt_id,"version":version,"authority":dict(authority),"portfolio_ref":dict(portfolio_ref),"evaluation_profile_ref":dict(evaluation_profile_ref),"evaluator_actor_id":evaluator_actor_id,"producer_actor_ids":list(producer_actor_ids),"candidate_scores":rows,"decision":decision,"decisive_margin_micros":decisive_margin_micros,"selected_hypothesis_ref":selected,"limitations":["development evaluation uses integer micros"]}
        return self.semantic.store("comparative_evaluation_receipt",payload,idempotency_key=idempotency_key)

    def stop_search(self, *, receipt_id: str, version: str, authority: Mapping[str, Any], portfolio_ref: Mapping[str, Any], evaluation_ref: Mapping[str, Any], remaining_budget: Mapping[str, int], diversity_exhausted: bool, idempotency_key: str) -> dict[str, Any]:
        require_air_ref(self.repository,portfolio_ref,object_types="activation_hypothesis_portfolio")
        evaluation=require_air_ref(self.repository,evaluation_ref,object_types="comparative_evaluation_receipt")
        decision=evaluation.payload["decision"]
        if decision=="DECISIVE_WINNER": reason="DECISIVE_ELIGIBLE_WINNER"; selected=evaluation.payload["selected_hypothesis_ref"]; question=None
        elif decision=="NO_ELIGIBLE_CANDIDATE": reason="SHARED_DEFECT"; selected=None; question=None
        elif diversity_exhausted: reason="DIVERSITY_EXHAUSTED"; selected=None; question=None
        elif remaining_budget["consumed_provider_cost_micros"]>=remaining_budget["maximum_provider_cost_micros"]: reason="BUDGET_BOUNDARY"; selected=None; question=None
        else: reason="OPERATOR_OWNED_AMBIGUITY"; selected=None; question="Which tension and viewer role should govern the next search round?"
        payload={"receipt_id":receipt_id,"version":version,"authority":dict(authority),"portfolio_ref":dict(portfolio_ref),"stop_reason":reason,"evidence_refs":[dict(evaluation_ref)],"remaining_budget":dict(remaining_budget),"limitations":["no automatic semantic convergence beyond governed stop"],"selected_hypothesis_ref":selected,"operator_question":question}
        return self.semantic.store("hypothesis_stopping_receipt",payload,idempotency_key=idempotency_key)

    def store_planned_pack(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        normalized=self.semantic.validate("planned_activative_intelligence_pack",payload)
        for field,kind in (("portfolio_ref","activation_hypothesis_portfolio"),("selected_hypothesis_ref","activation_hypothesis"),("matrix_of_edging_ref","matrix_of_edging"),("role_tension_ref","psychological_role_tension_contract")):
            require_air_ref(self.repository,normalized[field],object_types=kind)
        result = self.semantic.store("planned_activative_intelligence_pack",normalized,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="selected_from", target_refs=[normalized["portfolio_ref"], normalized["selected_hypothesis_ref"], normalized["matrix_of_edging_ref"], normalized["role_tension_ref"], *normalized["source_refs"]], evidence={"service":"planned_pack","phase":"PHASE_05"})
        return result

    def promote(self,payload:Mapping[str,Any],*,idempotency_key:str)->dict[str,Any]:
        normalized=self.semantic.validate("hypothesis_promotion_receipt",payload)
        portfolio=require_air_ref(self.repository,normalized["portfolio_ref"],object_types="activation_hypothesis_portfolio")
        selected=require_air_ref(self.repository,normalized["selected_hypothesis_ref"],object_types="activation_hypothesis")
        stop=require_air_ref(self.repository,normalized["stopping_receipt_ref"],object_types="hypothesis_stopping_receipt")
        require_air_ref(self.repository,normalized["planned_pack_ref"],object_types="planned_activative_intelligence_pack")
        if stop.payload["stop_reason"]!="DECISIVE_ELIGIBLE_WINNER" or stop.payload.get("selected_hypothesis_ref")!=selected.immutable_ref(): raise ValueError("promotion requires decisive selected hypothesis")
        if selected.immutable_ref() not in portfolio.payload["candidate_refs"]: raise ValueError("selected hypothesis not in portfolio")
        result = self.semantic.store("hypothesis_promotion_receipt",normalized,idempotency_key=idempotency_key)
        add_lineage_edges(self.repository, source_result=result, relation_type="promotes", target_refs=[normalized["portfolio_ref"], normalized["selected_hypothesis_ref"], normalized["stopping_receipt_ref"], normalized["planned_pack_ref"], normalized["authority_decision_ref"]], evidence={"service":"hypothesis_promotion","phase":"PHASE_05"})
        return result
