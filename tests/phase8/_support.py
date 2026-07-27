from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for path in reversed([
    ROOT/'packages/ca_contracts/src', ROOT/'packages/ca_runtime/src', ROOT/'packages/ca_delegation_rc4/src',
    ROOT/'services/air/src', ROOT/'services/pipeline/src',
    ROOT/'services/interview/src', ROOT/'services/vae/src',
]):
    if str(path) not in sys.path: sys.path.insert(0,str(path))
from ca_contracts import canonical_sha256

def ref(object_id:str,seed:str)->dict[str,str]:
    return {'object_id':object_id,'version':'1.0.0','sha256':canonical_sha256({'seed':seed})}

def delegation_root()->Path:
    return ROOT/'services/delegation/delegation-contracts/1.1.0-rc.4'

def compile_demand(width:int=128,height:int=128):
    from cmf_pipeline.delegation import VisualDelegationService
    svc=VisualDelegationService(delegation_root())
    return svc.compile_demand(
        source_package_ref=ref('source-package:test','source'),
        reaction_receipt_refs=[ref('reaction-receipt:test','reaction')],
        expression_moment_refs=[ref('expression-moment:test','moment')],
        semantic_program_ref=ref('semantic-program:test','semantic'),
        final_script_ref=ref('final-script:test','script'),
        primitive_coalition_ref=ref('primitive-coalition:test','primitive'),
        archetype_coalition_ref=ref('archetype-coalition:test','archetype'),
        activation_transfer_contract_ref=ref('transfer:test','transfer'),
        content_harness_ref=ref('harness:test','harness'),
        category_profile_ref=ref('category:static','category'),
        format_profile_ref=ref('format:supervisual','format'),
        width_px=width,height_px=height,
        wrong_reading_locks=['Do not erase source identity.','Preserve negative space.'],
    )
