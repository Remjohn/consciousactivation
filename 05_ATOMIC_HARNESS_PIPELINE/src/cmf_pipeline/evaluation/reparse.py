from __future__ import annotations
import json,struct,zlib,subprocess
from pathlib import Path
from typing import Any,Mapping
from ca_contracts import bytes_sha256, canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref, reject_noncanonical, semantic_identity


def png_dimensions(path:Path)->tuple[int,int]:
    data=path.read_bytes()
    if not data.startswith(b'\x89PNG\r\n\x1a\n') or data[12:16]!=b'IHDR': raise PipelineValidationError('invalid PNG')
    return struct.unpack('>II',data[16:24])

class RenderReparseService:
    def reparse_static(self, *, artifact_path:str|Path, artifact_ref:Mapping[str,Any], composition:Mapping[str,Any])->dict[str,Any]:
        path=Path(artifact_path);ref=require_ref(artifact_ref,'artifact_ref')
        if bytes_sha256(path.read_bytes())!=ref['sha256']:raise PipelineValidationError('artifact hash mismatch')
        width,height=png_dimensions(path);expected=composition['canvas']
        discrepancies=[]
        if width!=expected['width_px'] or height!=expected['height_px']: discrepancies.append({'code':'CANVAS_DIMENSION_MISMATCH','responsible_layer':'RUNTIME','expected':[expected['width_px'],expected['height_px']],'observed':[width,height]})
        core={'artifact_ref':ref,'composition_ref':{'object_id':composition['composition_id'],'version':composition['composition_version'],'sha256':canonical_sha256(composition)},'observed':{'width_px':width,'height_px':height,'artifact_sha256':ref['sha256']},'discrepancies':discrepancies,'result':'PASS' if not discrepancies else 'FAIL'}
        reject_noncanonical(core);return {'reparse_receipt_id':semantic_identity('render-reparse',core),'reparse_receipt_version':'1.0.0',**core}

    def reparse_video(self, *, artifact_path:str|Path, artifact_ref:Mapping[str,Any], program:Mapping[str,Any])->dict[str,Any]:
        path=Path(artifact_path);ref=require_ref(artifact_ref,'artifact_ref')
        if bytes_sha256(path.read_bytes())!=ref['sha256']:raise PipelineValidationError('artifact hash mismatch')
        proc=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True,capture_output=True)
        if proc.returncode!=0:raise PipelineValidationError('ffprobe failed')
        p=json.loads(proc.stdout);streams={s.get('codec_type') for s in p.get('streams',[])};discrepancies=[]
        if 'video' not in streams:discrepancies.append({'code':'VIDEO_STREAM_MISSING','responsible_layer':'RUNTIME'})
        core={'artifact_ref':ref,'program_ref':{'object_id':program['program_id'],'version':program['program_version'],'sha256':canonical_sha256(program)},'observed':{'stream_types':sorted(str(x) for x in streams),'probe_sha256':canonical_sha256(p)},'discrepancies':discrepancies,'result':'PASS' if not discrepancies else 'FAIL'}
        reject_noncanonical(core);return {'reparse_receipt_id':semantic_identity('render-reparse',core),'reparse_receipt_version':'1.0.0',**core}
