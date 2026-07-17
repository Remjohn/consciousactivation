from __future__ import annotations
import hashlib
import pytest
from cmf_builder.workflow.actor_explicit_contracts import ActorKind,WorkflowNode
from cmf_builder.workflow.manual_shadow_routing import *
def digest(v:str)->str:return hashlib.sha256(v.encode()).hexdigest()
def node(kind:ActorKind,nid="node")->WorkflowNode:return WorkflowNode(nid,kind,f"owner:{nid}","in/v1","out/v1","authority",(),("valid",),"complete","reject",False,"checkpoint","cancel",f"owner:{nid}",(),"validator",actor_rationale="explicit responsibility")
def code_receipt(success=True,nid="node"):return CodeResultReceipt("receipt",nid,"v1","validator",digest("input"),digest("output"),"validator-v1",(digest("authority"),),success)
def binding(nid="node",active=True,permissions=("DEFAULT_DENY",)):return PhaseLocalCapsuleBinding(nid,"v1","agent-adapter", "capsule",digest("capsule"),"in/v1","out/v1","model-policy",permissions,digest("skill-in"),digest("skill-out"),(digest("evaluation"),),(digest("maturity"),),active,(nid,))
def test_code_owned_node_requires_exact_code_receipt_and_no_agent_capsule():
    result=validate_node_execution_boundary(node(ActorKind.DETERMINISTIC_CODE_NODE),code_result_receipt=code_receipt())
    assert result.execution_performed is False and result.provider_used is False
    with pytest.raises(ManualShadowError) as missing:validate_node_execution_boundary(node(ActorKind.DETERMINISTIC_CODE_NODE))
    assert missing.value.code=="MISSING_EXACT_CODE_RESULT_RECEIPT"
    with pytest.raises(ManualShadowError) as delegated:validate_node_execution_boundary(node(ActorKind.DETERMINISTIC_CODE_NODE),code_result_receipt=code_receipt(),agent_capsule_binding=binding())
    assert delegated.value.code=="DETERMINISTIC_WORK_DELEGATED_TO_AGENT"
def test_agent_node_requires_active_exact_scoped_default_deny_capsule():
    result=validate_node_execution_boundary(node(ActorKind.GOVERNED_AGENT_NODE),agent_capsule_binding=binding())
    assert result.execution_performed is False and result.network_used is False
    with pytest.raises(ManualShadowError):validate_node_execution_boundary(node(ActorKind.GOVERNED_AGENT_NODE),agent_capsule_binding=binding(active=False))
    with pytest.raises(ManualShadowError) as permissions:binding(permissions=("ALLOW_ALL",))
    assert permissions.value.code=="TOOL_PERMISSIONS_NOT_DEFAULT_DENY"
def test_human_node_rejects_synthetic_fixture_as_approval():
    with pytest.raises(ManualShadowError) as caught:validate_node_execution_boundary(node(ActorKind.HUMAN_NODE))
    assert caught.value.code=="HUMAN_APPROVAL_NOT_PROVIDED"
def test_external_boundary_validation_never_executes_external_product():
    result=validate_node_execution_boundary(node(ActorKind.EXTERNAL_BOUNDARY_NODE))
    assert result.execution_performed is False and result.network_used is False and result.provider_used is False

