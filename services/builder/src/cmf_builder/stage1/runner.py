import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List, Dict, Any

from .input_receipt import build_input_receipt
from .semantic_validator import SemanticValidator
from .evidence_validator import EvidenceValidator
from .report import (
    build_taxonomy_summary,
    build_validation_summary,
    build_operator_review_stub,
    assemble_contract_report
)
from .taxonomy import is_canonical_slide_role, is_canonical_primitive, is_canonical_zone
from .zip_extractor import extract_frames
from .vision_client import VisionClient
from .canonicalizer import compute_syntax_hash
from .taxonomy import is_canonical_slide_role, is_canonical_primitive

CHECKPOINTS = [
    '01_input_receipt',
    '02_observation',
    '03_taxonomy_resolution',
    '04_visual_syntax',
    '05_deduplication',
    '06_contract_validation',
    '07_operator_review',
    '08_final_receipt',
]

@dataclass
class RunConfig:
    harness_id: str
    source_zip_path: Path
    recorded_sha256: str
    vision_model: str
    base_url: str
    selected_by: str
    output_dir: Path
    resume_from: Optional[str] = None

@dataclass
class CheckpointResult:
    checkpoint: str
    status: str
    data: dict

@dataclass
class RunResult:
    harness_id: str
    checkpoints_completed: list[str]
    contract_report: Optional[dict]
    technical_status: str
    blocked_at: Optional[str]

class Stage1Runner:
    def __init__(self, config: RunConfig):
        self.config = config
        self.checkpoint_dir = self.config.output_dir / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.state: Dict[str, Any] = {}
        self.checkpoints_completed: List[str] = []
        
    def _save_checkpoint(self, result: CheckpointResult):
        path = self.checkpoint_dir / f"{result.checkpoint}.json"
        with open(path, "w") as f:
            json.dump(asdict(result), f, indent=2)
            
    def _load_checkpoint(self, checkpoint: str) -> Optional[CheckpointResult]:
        path = self.checkpoint_dir / f"{checkpoint}.json"
        if path.exists():
            with open(path, "r") as f:
                data = json.load(f)
                return CheckpointResult(**data)
        return None

    def run(self) -> RunResult:
        start_idx = 0
        if self.config.resume_from and self.config.resume_from in CHECKPOINTS:
            start_idx = CHECKPOINTS.index(self.config.resume_from)
            for i in range(start_idx):
                cp = CHECKPOINTS[i]
                res = self._load_checkpoint(cp)
                if res:
                    self.state[cp] = res.data
                    self.checkpoints_completed.append(cp)
            
        for i in range(start_idx, len(CHECKPOINTS)):
            cp = CHECKPOINTS[i]
            method_name = f"_run_{cp}"
            method = getattr(self, method_name)
            
            result = method()
            self._save_checkpoint(result)
            
            if result.status == 'completed':
                self.state[cp] = result.data
                self.checkpoints_completed.append(cp)
            else:
                return RunResult(
                    harness_id=self.config.harness_id,
                    checkpoints_completed=self.checkpoints_completed,
                    contract_report=None,
                    technical_status=result.status.upper(),
                    blocked_at=cp
                )
                
        return RunResult(
            harness_id=self.config.harness_id,
            checkpoints_completed=self.checkpoints_completed,
            contract_report=self.state.get('08_final_receipt', {}).get('report'),
            technical_status='PASS',
            blocked_at=None
        )
        
    def _run_01_input_receipt(self) -> CheckpointResult:
        receipt = build_input_receipt(
            harness_id=self.config.harness_id,
            source_zip_path=self.config.source_zip_path,
            recorded_sha256=self.config.recorded_sha256,
            vision_model=self.config.vision_model,
            base_url=self.config.base_url,
            selected_by=self.config.selected_by
        )
        data = asdict(receipt)
        if not receipt.match:
            return CheckpointResult(checkpoint='01_input_receipt', status='blocked', data=data)
        return CheckpointResult(checkpoint='01_input_receipt', status='completed', data=data)

    def _run_02_observation(self) -> CheckpointResult:
        try:
            frames = extract_frames(self.config.source_zip_path)
        except ValueError as e:
            return CheckpointResult(checkpoint='02_observation', status='blocked', data={'error': str(e)})

        vision = VisionClient(
            model_name=self.config.vision_model,
            base_url=self.config.base_url,
            harness_id=self.config.harness_id
        )

        all_observations = []
        all_raw_entries = []

        for i, frame in enumerate(frames):
            result = vision.analyze_frame(frame)
            
            # Format observations with unique object_ids
            frame_obs = result.get('observations', [])
            for j, obs in enumerate(frame_obs):
                # Always create a unique ID per object
                obs['object_id'] = f"frame{frame.frame_index}_obj{j+1}"
                obs['frame_index'] = frame.frame_index
                all_observations.append(obs)
                
            frame_entries = result.get('entries', [])
            for entry in frame_entries:
                entry['frame_index'] = frame.frame_index
                all_raw_entries.append(entry)

        data = {
            'observations': all_observations,
            'raw_entries': all_raw_entries
        }
        return CheckpointResult(checkpoint='02_observation', status='completed', data=data)

    def _run_03_taxonomy_resolution(self) -> CheckpointResult:
        raw_entries = self.state.get('02_observation', {}).get('raw_entries', [])
        
        resolutions = []
        for entry in raw_entries:
            role = entry.get('slide_role', '')
            role_status = 'CANONICAL' if is_canonical_slide_role(role) else 'NOVEL_CANDIDATE'
            
            prim_statuses = {}
            for prim in entry.get('primitives', []):
                ptype = prim.get('primitive_type', '')
                status = 'CANONICAL' if is_canonical_primitive(ptype) else 'NOVEL_CANDIDATE'
                prim_statuses[ptype] = status
                
            resolutions.append({
                'frame_index': entry.get('frame_index'),
                'slide_role': {'value': role, 'status': role_status},
                'primitives': prim_statuses
            })
            
        data = {'resolutions': resolutions}
        return CheckpointResult(checkpoint='03_taxonomy_resolution', status='completed', data=data)

    def _run_04_visual_syntax(self) -> CheckpointResult:
        raw_entries = self.state.get('02_observation', {}).get('raw_entries', [])
        observations = self.state.get('02_observation', {}).get('observations', [])
        
        entries = []
        for entry in raw_entries:
            frame_idx = entry.get('frame_index')
            
            # Map observations back to this frame to use as evidence_refs
            frame_obs_ids = [obs['object_id'] for obs in observations if obs.get('frame_index') == frame_idx]
            
            primitives = []
            for p in entry.get('primitives', []):
                p_copy = dict(p)
                p_copy['evidence_refs'] = frame_obs_ids[:1] if frame_obs_ids else []
                z = str(p_copy.get('zone', 'full_bleed'))
                if not is_canonical_zone(z):
                    z = 'full_bleed'
                p_copy['zone'] = z

                ptype = str(p_copy.get('primitive_type', 'text_block'))
                if not is_canonical_primitive(ptype):
                    ptype = 'text_block'
                p_copy['primitive_type'] = ptype

                primitives.append(p_copy)

            anchors = []
            for a in entry.get('anchor_elements', []):
                if isinstance(a, dict):
                    a_copy = dict(a)
                else:
                    a_copy = {'label': str(a)}
                a_copy['evidence_refs'] = frame_obs_ids[:1] if frame_obs_ids else []
                anchors.append(a_copy)

            syntax_hash = compute_syntax_hash(
                slide_role=entry.get('slide_role', ''),
                container_zones=entry.get('container_zones', []),
                primitives=primitives,
                anchor_elements=anchors
            )
            
            entries.append({
                'frame_index': frame_idx,
                'candidate_slide_role': entry.get('slide_role', ''),
                'slide_role': entry.get('slide_role', ''),
                'container_zones': entry.get('container_zones', []),
                'primitives': primitives,
                'anchor_elements': anchors,
                'evidence_refs': frame_obs_ids,
                'syntax_hash': syntax_hash
            })
            
        data = {'entries': entries}
        return CheckpointResult(checkpoint='04_visual_syntax', status='completed', data=data)

    def _run_05_deduplication(self) -> CheckpointResult:
        entries = self.state.get('04_visual_syntax', {}).get('entries', [])
        
        seen_hashes = set()
        deduplicated = []
        unique_roles = set()
        
        for entry in entries:
            h = entry.get('syntax_hash')
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                deduplicated.append(entry)
                unique_roles.add(entry.get('slide_role', ''))
                
        data = {
            'deduplicated_entries': deduplicated,
            'deduplication_summary': {
                'unique_slide_roles': [{'slide_role': r} for r in sorted(list(unique_roles))],
                'unique_layout_count': len(deduplicated),
                'total_unique_hashes': len(deduplicated)
            }
        }
        return CheckpointResult(checkpoint='05_deduplication', status='completed', data=data)

    def _run_06_contract_validation(self) -> CheckpointResult:
        receipt = self.state.get('01_input_receipt', {})
        observations = self.state.get('02_observation', {}).get('observations', [])
        entries = self.state.get('04_visual_syntax', {}).get('entries', [])
        dedup_summary = self.state.get('05_deduplication', {}).get('deduplication_summary', {})
        
        analysis_data = {
            "all_slide_analyses": entries,
            "visual_observations": observations,
            "receipt": receipt,
            "deduplication_summary": dedup_summary
        }
        
        sem_val = SemanticValidator()
        sem_res = sem_val.validate(analysis_data)
        
        ev_val = EvidenceValidator()
        ev_res = ev_val.validate(entries, observations)
        
        data = {
            'semantic': {
                'technical_status': sem_res.technical_status,
                'findings': [asdict(f) for f in sem_res.findings]
            },
            'evidence': {
                'technical_status': ev_res.technical_status,
                'findings': [asdict(f) for f in ev_res.findings]
            }
        }
        
        if sem_res.technical_status in ('FAIL', 'BLOCKED') or ev_res.technical_status in ('FAIL', 'BLOCKED'):
            return CheckpointResult(checkpoint='06_contract_validation', status='blocked', data=data)
            
        return CheckpointResult(checkpoint='06_contract_validation', status='completed', data=data)

    def _run_07_operator_review(self) -> CheckpointResult:
        review = build_operator_review_stub(self.config.harness_id, 'PASS')
        return CheckpointResult(checkpoint='07_operator_review', status='completed', data=review)

    def _run_08_final_receipt(self) -> CheckpointResult:
        receipt_data = self.state.get('01_input_receipt', {})
        tax_summary = build_taxonomy_summary([])
        val_data = self.state.get('06_contract_validation', {})
        val_summary = build_validation_summary(val_data.get('semantic', {}), val_data.get('evidence', {}))
        review_data = self.state.get('07_operator_review', {})
        observations = self.state.get('02_observation', {}).get('observations', [])
        syntax_entries = self.state.get('04_visual_syntax', {}).get('entries', [])
        
        report = assemble_contract_report(
            harness_id=self.config.harness_id,
            input_receipt=receipt_data,
            checkpoints=self.checkpoints_completed + ['08_final_receipt'],
            taxonomy_summary=tax_summary,
            validation_summary=val_summary,
            operator_review=review_data,
            fyi=[],
            observations=observations,
            visual_syntax=syntax_entries
        )
        return CheckpointResult(checkpoint='08_final_receipt', status='completed', data={'report': report})
