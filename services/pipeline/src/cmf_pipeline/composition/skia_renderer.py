from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from ca_contracts import bytes_sha256, canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_relative_path, reject_noncanonical, semantic_identity
from .raster import RasterCanvas

class SkiaStaticRenderer:
    """Skia binding with a deterministic built-in reference rasterizer fallback."""
    def __init__(self):
        try:
            import skia as _skia
            self.skia=_skia;self.renderer_kind='SKIA_PYTHON'
        except Exception:
            self.skia=None;self.renderer_kind='SKIA_COMPATIBLE_REFERENCE_RASTERIZER'

    def display_list(self,composition:Mapping[str,Any],page_index:int)->dict[str,Any]:
        page=composition['pages'][page_index];commands=[]
        for e in page['elements']:
            commands.append({'op':'rect','element_id':e['element_id'],'bbox':e['bbox'],'rgb':e['background_rgb'],'z_index':e['z_index']})
            if e['text']!='NOT_APPLICABLE': commands.append({'op':'text','element_id':e['element_id'],'bbox':e['bbox'],'text':e['text'],'font_size_px':e['font_size_px'],'rgb':e['foreground_rgb'],'lines':e['text_measurement']['lines'],'z_index':e['z_index']+1})
        return {'display_list_version':'1.0.0','composition_ref':{'object_id':composition['composition_id'],'version':composition['composition_version'],'sha256':canonical_sha256(composition)},'page_id':page['page_id'],'canvas':composition['canvas'],'commands':sorted(commands,key=lambda x:(x['z_index'],x['element_id'],x['op']))}

    def render_page(self,composition:Mapping[str,Any],page_index:int,destination:str|Path,logical_uri:str)->dict[str,Any]:
        logical=require_relative_path(logical_uri,'logical_uri');dl=self.display_list(composition,page_index);canvas_cfg=dl['canvas'];width=canvas_cfg['width_px'];height=canvas_cfg['height_px']
        if self.skia is not None:
            surface=self.skia.Surface(width,height);c=surface.getCanvas();c.clear(self.skia.Color(*canvas_cfg['background_rgb']))
            for cmd in dl['commands']:
                b=cmd['bbox'];x=b['x']*width//1_000_000;y=b['y']*height//1_000_000;w=b['width']*width//1_000_000;h=b['height']*height//1_000_000
                if cmd['op']=='rect':
                    p=self.skia.Paint(Color=self.skia.Color(*cmd['rgb']));c.drawRect(self.skia.Rect.MakeXYWH(x,y,w,h),p)
                else:
                    p=self.skia.Paint(Color=self.skia.Color(*cmd['rgb']),AntiAlias=True);font=self.skia.Font(None,cmd['font_size_px'])
                    yy=y+cmd['font_size_px']
                    for line in cmd['lines']:
                        c.drawString(line,x,yy,font,p);yy+=max(cmd['font_size_px'],cmd['font_size_px']*12//10)
            data=surface.makeImageSnapshot().encodeToData();Path(destination).parent.mkdir(parents=True,exist_ok=True);Path(destination).write_bytes(bytes(data))
        else:
            canvas=RasterCanvas(width,height,canvas_cfg['background_rgb'])
            for cmd in dl['commands']:
                b=cmd['bbox'];x=b['x']*width//1_000_000;y=b['y']*height//1_000_000;w=b['width']*width//1_000_000;h=b['height']*height//1_000_000
                if cmd['op']=='rect': canvas.rect(x,y,w,h,cmd['rgb'])
                else: canvas.text(x,y,'\n'.join(cmd['lines']),cmd['font_size_px'],cmd['rgb'],w)
            canvas.save(Path(destination))
        path=Path(destination);manifest={'artifact_id':semantic_identity('static-render-artifact',{'logical_uri':logical,'sha256':bytes_sha256(path.read_bytes()),'page_id':dl['page_id']}),'artifact_version':'1.0.0','logical_uri':logical,'sha256':bytes_sha256(path.read_bytes()),'byte_count':path.stat().st_size,'renderer_kind':self.renderer_kind,'display_list_sha256':canonical_sha256(dl),'page_id':dl['page_id'],'production_authorized':False}
        reject_noncanonical(manifest);return {'manifest':manifest,'display_list':dl,'output_path':str(path)}
