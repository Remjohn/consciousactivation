from _support import *
import pytest
from conscious_activations_interview_expression.errors import ValidationError

def test_exact_alignment_and_phrase_coverage(tmp_path):
 app,pref,_=imported_app(tmp_path); aligned,packed,_,_=build_transcript(app,pref)
 assert aligned['object']['payload']['coverage']['included_word_count']==11
 phrase_words=[w for p in packed['object']['payload']['phrases'] for w in p['word_refs']]
 assert phrase_words==[f'w-{i:03d}' for i in range(11)]
 assert any(p['hesitation_word_refs'] for p in packed['object']['payload']['phrases'])

def test_unknown_speaker_not_guessed(tmp_path):
 app,pref,_=imported_app(tmp_path); ws=words();ws[0]['speaker_state']='UNKNOWN';ws[0]['speaker_id']='guest'
 with pytest.raises(ValidationError,match='UNKNOWN'): app.transcripts.align(source_package_ref=pref,words=ws,speaker_segments=[],policy_id='p',idempotency_key='x')

def test_overlap_requires_explicit_state(tmp_path):
 app,pref,_=imported_app(tmp_path);ws=words();ws[1]['start_ms']=100
 with pytest.raises(ValidationError,match='OVERLAP'): app.transcripts.align(source_package_ref=pref,words=ws,speaker_segments=[],policy_id='p',idempotency_key='x')

def test_deterministic_phrase_pack(tmp_path):
 app,pref,_=imported_app(tmp_path);a,p,ar,pr=build_transcript(app,pref)
 again=app.transcripts.pack_phrases(ar,policy={'policy_id':'pack-v1','max_words':7,'max_gap_ms':500,'break_on_terminal_punctuation':True},idempotency_key='pack')
 assert again['idempotent_replay'] is True
 assert again['object']['sha256']==p['object']['sha256']
