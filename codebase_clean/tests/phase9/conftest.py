from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for p in [ROOT/'packages/ca_contracts/src',ROOT/'packages/ca_runtime/src',ROOT/'packages/ca_delegation_rc4/src',ROOT/'services/air/src',ROOT/'services/pipeline/src',ROOT/'services/interview/src',ROOT/'services/vae/src']:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
