from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for path in reversed([ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'services/air/src',ROOT/'services/pipeline/src',ROOT/'services/interview/src']):
    if str(path) not in sys.path:sys.path.insert(0,str(path))
from ca_contracts import canonical_sha256

def ref(object_id,seed):return {'object_id':object_id,'version':'1.0.0','sha256':canonical_sha256({'seed':seed})}
