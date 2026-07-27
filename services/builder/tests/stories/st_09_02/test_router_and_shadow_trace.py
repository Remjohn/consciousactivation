from __future__ import annotations
import hashlib
import pytest
from cmf_builder.workflow.manual_shadow_routing import *

def digest(v:str)->str:return hashlib.sha256(v.encode()).hexdigest()
def profile(pid="shadow-profile")->WorkflowProfile:return WorkflowProfile(pid,"1.0.0-development",digest(pid),("structural-review",),("reply_dm",),("bounded",),True,False,(digest("authority"),))
def request(risk="bounded")->RouteRequest:return RouteRequest("structural-review","reply_dm","compiled",risk,"none","registry-v1",digest("registry"))
def step(kind:ShadowStepKind,index:int)->ShadowStep:return ShadowStep(f"step-{index}",index,kind,"SYNTHETIC_ACTOR",f"actor-{index}",f"action-{index}",(digest(f"in-{index}"),),(digest(f"out-{index}"),),"OD_AM_001", "observed synthetic condition","","","cost not applicable to local fixture",(),f"node-{index}","","repository-owned synthetic fixture")
def steps():return tuple(step(kind,index) for index,kind in enumerate(ShadowStepKind))

def test_exact_route_is_selected_before_execution():
    result=route_workflow_before_execution(request(),(profile(),))
    assert result.selected_profile_id=="shadow-profile";assert result.routing_completed_before_execution is True
def test_unmatched_and_ambiguous_route_fail_closed():
    with pytest.raises(ManualShadowError) as no_route:route_workflow_before_execution(request("unknown"),(profile(),))
    assert no_route.value.code=="UNMATCHED_WORKFLOW_PROFILE"
    with pytest.raises(ManualShadowError) as ambiguous:route_workflow_before_execution(request("high"),(profile("a"),profile("b")))
    assert ambiguous.value.code=="UNMATCHED_WORKFLOW_PROFILE" or ambiguous.value.code=="AMBIGUOUS_HIGH_RISK_ROUTE"
def test_trace_contains_all_eight_ordered_step_kinds_and_exact_refs():
    trace=compile_manual_shadow_trace(workflow_identity=digest("workflow"),node_identity=digest("node"),input_snapshot_ref=digest("input"),proposed_automated_output_ref=digest("output"),shadow_review_request_ref=digest("review"),reviewer_identity="synthetic-reviewer",reviewer_response="synthetic structural response",comparison="exact synthetic structure",divergence_classification="EXACT_AGREEMENT",final_disposition="PASS_SYNTHETIC_STRUCTURAL_PARITY_ONLY",authority_ref=digest("authority"),observed_at="2026-07-17T00:00:00Z",invalidation_state="ACTIVE",steps=steps())
    assert tuple(x.step_kind.value for x in trace.steps)==SHADOW_STEP_KINDS
    assert trace.as_dict()["human_approval_issued"] is False
    assert trace.as_dict()["automation_promotion_available"] is False
def test_missing_step_kind_or_sequence_gap_fails():
    values=dict(workflow_identity=digest("workflow"),node_identity=digest("node"),input_snapshot_ref=digest("input"),proposed_automated_output_ref=digest("output"),shadow_review_request_ref=digest("review"),reviewer_identity="fixture",reviewer_response="fixture",comparison="fixture",divergence_classification="EXACT",final_disposition="PASS_SYNTHETIC_STRUCTURAL_PARITY_ONLY",authority_ref=digest("authority"),observed_at="2026-07-17T00:00:00Z",invalidation_state="ACTIVE")
    with pytest.raises(ManualShadowError) as missing:compile_manual_shadow_trace(**values,steps=steps()[:-1])
    assert missing.value.code=="INCOMPLETE_SHADOW_STEP_COVERAGE"
    broken=list(steps());broken[-1]=step(ShadowStepKind.ARTIFACT_OBSERVATION,99)
    with pytest.raises(ManualShadowError) as sequence:compile_manual_shadow_trace(**values,steps=tuple(broken))
    assert sequence.value.code=="NON_CANONICAL_SHADOW_SEQUENCE"
def test_unmapped_step_requires_governed_exclusion():
    with pytest.raises(ManualShadowError) as caught:step=ShadowStep("x",0,ShadowStepKind.HUMAN_ACTION,"HUMAN","fixture","action",(),(),"boundary","condition","","","n/a",(),"","","provenance")
    assert caught.value.code=="UNMAPPED_SHADOW_STEP"

