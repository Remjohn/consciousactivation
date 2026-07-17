from __future__ import annotations
from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys
import pytest
from cmf_builder.workflow.manual_shadow_routing import *
from tests.stories.st_09_02.test_failure_authority_boundaries import authority,command,evaluation,issue_receipt,digest
def test_identical_evaluation_and_issue_are_deterministic_and_idempotent():
    a,b=issue_receipt(),issue_receipt();assert a.evaluation_identity==b.evaluation_identity;assert validate_repeat_manual_shadow(a,b) is a
def test_conflicting_repeat_fails_closed():
    with pytest.raises(ManualShadowError) as caught:validate_repeat_manual_shadow(issue_receipt(),issue_receipt(candidate=evaluation(divergence_class=DivergenceClass.SEMANTIC_DIVERGENCE)))
    assert caught.value.code=="CONFLICTING_REPEAT_COMMAND"
def test_nested_tamper_is_detected():
    value=issue_receipt();object.__setattr__(value.review_request.input_snapshot,"snapshot_sha256",digest("tampered"))
    with pytest.raises(ManualShadowError) as caught:value.as_dict()
    assert caught.value.code=="MUTATED_GOVERNED_OBJECT"
@pytest.mark.parametrize("action",(ShadowAction.INVALIDATE,ShadowAction.ROLLBACK))
def test_invalidation_and_rollback_preserve_history(action):
    value=issue_receipt();historical=canonical_json_bytes(value.as_dict());auth=authority(action);payload=compute_shadow_transition_payload_sha256(value.receipt_identity,action);cmd=command(action=action,resource_id=value.receipt_identity,payload_sha256=payload,governed_authority=auth,command_id=f"{action.value.lower()}-shadow")
    result=(invalidate_manual_shadow_receipt if action is ShadowAction.INVALIDATE else rollback_manual_shadow_receipt)(value,cmd,auth)
    assert result.active_after is False and result.historical_receipt_preserved is True;assert canonical_json_bytes(value.as_dict())==historical
def test_failed_transition_has_zero_partial_state():
    value=issue_receipt();auth=authority(ShadowAction.INVALIDATE);cmd=command(action=ShadowAction.INVALIDATE,resource_id=value.receipt_identity,payload_sha256=digest("wrong"),governed_authority=auth,command_id="bad")
    with pytest.raises(ManualShadowError) as caught:invalidate_manual_shadow_receipt(value,cmd,auth)
    assert caught.value.code=="COMMAND_PAYLOAD_MISMATCH"
def test_fresh_process_byte_equality():
    repo=Path(__file__).resolve().parents[3];env=dict(os.environ);env["PYTHONPATH"]=os.pathsep.join((str(repo/"src"),str(repo)));script="from tests.stories.st_09_02.test_failure_authority_boundaries import issue_receipt; from cmf_builder.workflow.manual_shadow_routing import canonical_json_bytes; import sys; sys.stdout.buffer.write(canonical_json_bytes(issue_receipt().as_dict()))";fresh=subprocess.check_output([sys.executable,"-c",script],cwd=repo,env=env);assert fresh==canonical_json_bytes(issue_receipt().as_dict())
