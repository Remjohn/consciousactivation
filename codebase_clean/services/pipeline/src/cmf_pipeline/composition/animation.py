from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Any, Mapping
from ca_contracts import bytes_sha256, canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_relative_path, reject_noncanonical, semantic_identity
from .raster import RasterCanvas

class AnimationSceneRealizer:
    def realize(self, *, scene_package: Mapping[str,Any], composition: Mapping[str,Any], output_dir: str|Path, logical_uri: str, frame_count: int=24, fps: int=12) -> dict[str,Any]:
        if 'format02' in str(scene_package).lower(): raise PipelineValidationError('Format 02 remains deferred')
        if composition['composition_kind']!='ANIMATION_SCENE': raise PipelineValidationError('animation realization requires ANIMATION_SCENE composition')
        logical=require_relative_path(logical_uri,'logical_uri');out=Path(output_dir);frames=out/'frames';frames.mkdir(parents=True,exist_ok=True)
        page=composition['pages'][0];width=composition['canvas']['width_px'];height=composition['canvas']['height_px'];bg=composition['canvas']['background_rgb']
        for frame in range(frame_count):
            canvas=RasterCanvas(width,height,bg)
            for e in page['elements']:
                b=e['bbox'];x=b['x']*width//1_000_000;y=b['y']*height//1_000_000;w=b['width']*width//1_000_000;h=b['height']*height//1_000_000
                if e['syntax_role']=='MOTION_SUBJECT': x += (frame*max(1,width//20))//max(1,frame_count-1)
                canvas.rect(x,y,w,h,e['background_rgb'])
                if e['text']!='NOT_APPLICABLE': canvas.text(x,y,'\n'.join(e['text_measurement']['lines']),e['font_size_px'],e['foreground_rgb'],w)
            canvas.save(frames/f'frame-{frame:04d}.png')
        output=out/Path(logical).name
        proc=subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(fps),'-i',str(frames/'frame-%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],text=True,capture_output=True)
        if proc.returncode!=0: raise PipelineValidationError(f'animation render failed: {proc.stderr.strip()}')
        core={'scene_package_ref':{'object_id':scene_package['animation_scene_package_id'],'version':scene_package['animation_scene_package_version'],'sha256':canonical_sha256(scene_package)},'composition_ref':{'object_id':composition['composition_id'],'version':composition['composition_version'],'sha256':canonical_sha256(composition)},'logical_uri':logical,'sha256':bytes_sha256(output.read_bytes()),'byte_count':output.stat().st_size,'frame_count':frame_count,'fps':fps,'performance_class':'GENERATED_PERFORMANCE','format02_activated':False,'production_authorized':False}
        reject_noncanonical(core)
        return {'manifest':{'animation_artifact_id':semantic_identity('animation-artifact',core),'animation_artifact_version':'1.0.0',**core},'output_path':str(output),'frame_directory':str(frames)}
