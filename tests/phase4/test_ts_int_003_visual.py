from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError

def test_shot_map_partitions_and_keyframes_are_deterministic(tmp_path):
 app,pref,_=imported_app(tmp_path);v,_=build_visual(app,pref)
 payload=v['object']['payload']; assert len(payload['shots'])==2; assert len(payload['keyframes'])==2
 assert payload['technical_only'] is True and payload['creates_expression_moments'] is False

def test_gap_or_overlap_rejected(tmp_path):
 app,pref,_=imported_app(tmp_path)
 with pytest.raises(ValidationError,match='partition'):
  app.visual.compile(source_package_ref=pref,duration_ms=6000,shots=[{'shot_id':'s','start_ms':1,'end_ms':6000,'transition_in':'SOURCE_START','transition_out':'SOURCE_END'}],keyframe_candidates=[],profile_id='p',idempotency_key='x')

def test_visual_change_never_creates_semantic_moment(tmp_path):
 app,pref,_=imported_app(tmp_path);v,_=build_visual(app,pref)
 assert not app.expression.approved_moments(pref['object_id'])
