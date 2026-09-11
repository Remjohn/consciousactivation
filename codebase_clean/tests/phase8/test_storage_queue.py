from __future__ import annotations
import json
import pytest
from ._support import delegation_root
from ca_contracts import canonical_sha256
from cmf_vae.repository import VAERepository
from cmf_vae.storage import ContentAddressedStore
from cmf_vae.errors import QueueConflict,LeaseConflict,VAEError

def test_06_content_addressed_storage_roundtrip(tmp_path):
    store=ContentAddressedStore(tmp_path/'s'); rec=store.put(b'abc',logical_uri='asset/a.bin',media_type='application/octet-stream'); data,meta=store.get(rec['sha256']); assert data==b'abc'; assert meta['resource_ref'] if 'resource_ref' in meta else rec['resource_ref']

def test_07_content_addressed_storage_detects_tamper(tmp_path):
    store=ContentAddressedStore(tmp_path/'s'); rec=store.put(b'abc',logical_uri='asset/a.bin',media_type='application/octet-stream'); p=store.objects/rec['sha256'][:2]/rec['sha256']; p.write_bytes(b'evil')
    with pytest.raises(VAEError): store.get(rec['sha256'])

def repo(tmp_path): r=VAERepository(tmp_path/'q.sqlite3'); r.initialize(); return r

def test_08_queue_submission_is_idempotent(tmp_path):
    r=repo(tmp_path); a=r.submit_job({'x':1},['cap'],idempotency_key='k'); b=r.submit_job({'x':1},['cap'],idempotency_key='k'); assert a['job_id']==b['job_id']; assert len(r.list_job_events(a['job_id']))==1

def test_09_queue_detects_idempotency_conflict(tmp_path):
    r=repo(tmp_path); r.submit_job({'x':1},['cap'],idempotency_key='k')
    with pytest.raises(QueueConflict): r.submit_job({'x':2},['cap'],idempotency_key='k')

def test_10_worker_leasing_and_fencing(tmp_path):
    r=repo(tmp_path); r.register_worker('w',['cap'],canonical_sha256({'w':1})); j=r.submit_job({'x':1},['cap'],idempotency_key='k'); lease=r.lease_next('w',now_ms=1000); assert lease and lease['state']=='LEASED'
    with pytest.raises(LeaseConflict): r.checkpoint(j['job_id'],'w','wrong',{'stage':'x'},now_ms=1100)

def test_11_checkpoint_and_expired_lease_recovery(tmp_path):
    r=repo(tmp_path); r.register_worker('w',['cap'],canonical_sha256({'w':1})); j=r.submit_job({'x':1},['cap'],idempotency_key='k'); lease=r.lease_next('w',now_ms=1000,lease_ms=100); r.checkpoint(j['job_id'],'w',lease['fencing_token'],{'stage':'mask'},now_ms=1050); recovered=r.recover_expired(now_ms=1200); assert recovered[0]['state']=='RETRY_READY'; assert r.get_job(j['job_id'])['checkpoint']=={'stage':'mask'}

def test_12_cancellation_quarantines_late_result(tmp_path):
    r=repo(tmp_path); r.register_worker('w',['cap'],canonical_sha256({'w':1})); j=r.submit_job({'x':1},['cap'],idempotency_key='k'); lease=r.lease_next('w',now_ms=1000); r.request_cancel(j['job_id'],reason='operator'); result=r.complete_job(j['job_id'],'w',lease['fencing_token'],{'artifact':'x'},now_ms=1100); assert result['state']=='LATE_RESULT_QUARANTINED'

def test_13_cancellation_precedes_expired_recovery(tmp_path):
    r=repo(tmp_path); r.register_worker('w',['cap'],canonical_sha256({'w':1})); j=r.submit_job({'x':1},['cap'],idempotency_key='k'); r.lease_next('w',now_ms=1000,lease_ms=10); r.request_cancel(j['job_id'],reason='operator'); # state no longer LEASED, terminal recovery does not override
    assert r.recover_expired(now_ms=2000)==[{'job_id': j['job_id'], 'state': 'CANCELLED'}]; assert r.get_job(j['job_id'])['state']=='CANCELLED'
