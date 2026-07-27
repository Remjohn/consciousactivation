from __future__ import annotations
import hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_01_03_TRACEABILITY'
def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
class TraceabilityTests(unittest.TestCase):
 def test_all_specs_and_evidence_paths_exist(self):
  data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text(encoding='utf-8'))
  self.assertEqual(len(data['specs']),18)
  for spec in data['specs']:
   path=ROOT/spec['spec_path']; self.assertTrue(path.is_file(),spec['spec_path']); self.assertEqual(sha(path),spec['spec_sha256'])
   for field in ('implementation_paths','test_paths'):
    for item in filter(None,spec[field].split(';')): self.assertTrue((ROOT/item.split('::')[0]).exists(),item)
 def test_no_full_spec_completion_is_overclaimed(self):
  data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text(encoding='utf-8'))
  self.assertTrue(all(not item['full_spec_completed'] for item in data['specs']))
 def test_closed_gap_records_exist(self):
  data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text(encoding='utf-8'))
  closed={g['gap_id'] for g in data['gaps'] if g['status']=='CLOSED'}
  self.assertEqual(closed,{'GAP-SQLITE-CONNECTION-LIFECYCLE','GAP-TRACEABILITY-EVIDENCE','GAP-PHASE-CLAIM-BOUNDARY'})
if __name__=='__main__': unittest.main()
