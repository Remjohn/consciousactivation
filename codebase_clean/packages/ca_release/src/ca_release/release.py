from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from ca_contracts import bytes_sha256, canonical_json_text, canonical_sha256


class ReleaseEvidenceBuilder:
    def __init__(self, repo_root: str|Path): self.repo_root=Path(repo_root)

    @staticmethod
    def artifact(path: Path, logical_uri: str, kind: str) -> dict[str,Any]:
        data=path.read_bytes();return {'artifact_id':f"artifact:{bytes_sha256(data)}",'artifact_kind':kind,'logical_uri':logical_uri,'sha256':bytes_sha256(data),'bytes':len(data)}

    def build(self,*,release_id:str,output_dir:str|Path,source_refs:Sequence[Mapping[str,Any]],semantic_refs:Sequence[Mapping[str,Any]],continuity_ref:Mapping[str,Any],artifact_paths:Sequence[tuple[str|Path,str,str]],evaluation_refs:Sequence[Mapping[str,Any]],audit_export_refs:Sequence[Mapping[str,Any]],backup_receipts:Sequence[Mapping[str,Any]],benchmark_receipts:Sequence[Mapping[str,Any]],sbom:Mapping[str,Any],deployment_manifest:Mapping[str,Any],open_gaps:Sequence[Mapping[str,Any]],implementation_handoff:Mapping[str,Any])->dict[str,Any]:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        artifacts=[self.artifact(Path(path),uri,kind) for path,uri,kind in artifact_paths]
        artifacts.sort(key=lambda x:x['logical_uri'])
        claim_ledger={
            'development_reference_pilot_executed':True,
            'real_imported_human_interview_executed':False,
            'external_model_execution_proven':False,
            'real_sam3_executed':False,
            'real_lucida_executed':False,
            'real_comfyui_worker_executed':False,
            'real_google_gnm_executed':False,
            'certified_independent_vlm_evaluation':False,
            'production_authorized':False,
            'certified':False,
            'format02_activated':False,
            'vae_stage5_authorized':False,
        }
        manifest_without_hash={'release_id':release_id,'release_version':'0.9.0-dev.1','release_state':'DEVELOPMENT_REFERENCE_CANDIDATE','source_refs':sorted([dict(r) for r in source_refs],key=lambda x:x['object_id']),'semantic_refs':sorted([dict(r) for r in semantic_refs],key=lambda x:x['object_id']),'continuity_ref':dict(continuity_ref),'artifacts':artifacts,'evaluation_refs':sorted([dict(r) for r in evaluation_refs],key=lambda x:x['object_id']),'audit_export_refs':sorted([dict(r) for r in audit_export_refs],key=lambda x:x['object_id']),'backup_receipts':list(backup_receipts),'benchmark_receipts':list(benchmark_receipts),'sbom_ref':{'object_id':'sbom:phase9','version':'1.0.0','sha256':sbom['sbom_sha256']},'deployment_manifest_ref':{'object_id':'deployment:phase9-local','version':'1.0.0','sha256':canonical_sha256(deployment_manifest)},'open_gaps':sorted([dict(g) for g in open_gaps],key=lambda x:x['gap_id']),'implementation_handoff':dict(implementation_handoff),'claim_ledger':claim_ledger,'historical_replay_policy':'CONTENT_ADDRESSED_IMMUTABLE'}
        manifest={**manifest_without_hash,'release_manifest_sha256':canonical_sha256(manifest_without_hash)}
        evidence_index={'release_ref':{'object_id':release_id,'version':'0.9.0-dev.1','sha256':manifest['release_manifest_sha256']},'artifact_count':len(artifacts),'evidence_types':['source','semantic','artifact','evaluation','audit','backup','benchmark','sbom','deployment','gap','handoff'],'claim_ceiling':'PHASE_09_DEVELOPMENT_RELEASE_CANDIDATE_EVIDENCE'}
        (out/'RELEASE_MANIFEST.json').write_text(canonical_json_text(manifest)+'\n',encoding='utf-8')
        (out/'CLAIM_LEDGER.json').write_text(canonical_json_text(claim_ledger)+'\n',encoding='utf-8')
        (out/'EVIDENCE_INDEX.json').write_text(canonical_json_text(evidence_index)+'\n',encoding='utf-8')
        (out/'SBOM.json').write_text(canonical_json_text(sbom)+'\n',encoding='utf-8')
        (out/'DEPLOYMENT_MANIFEST.json').write_text(canonical_json_text(deployment_manifest)+'\n',encoding='utf-8')
        (out/'IMPLEMENTATION_HANDOFF.json').write_text(canonical_json_text(dict(implementation_handoff))+'\n',encoding='utf-8')
        return {'manifest':manifest,'evidence_index':evidence_index,'claim_ledger':claim_ledger,'output_dir':str(out)}
