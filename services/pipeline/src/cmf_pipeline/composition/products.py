from __future__ import annotations
from pathlib import Path
from typing import Any, Mapping
from ca_contracts import bytes_sha256, canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_relative_path, reject_noncanonical, semantic_identity
from .skia_renderer import SkiaStaticRenderer
from .pdf import SimplePdfExporter

class SuperVisualService:
    def __init__(self,renderer:SkiaStaticRenderer|None=None): self.renderer=renderer or SkiaStaticRenderer()
    def render(self,composition:Mapping[str,Any],output_dir:str|Path,logical_uri:str)->dict[str,Any]:
        if composition['composition_kind']!='SUPERVISUAL' or len(composition['pages'])!=1: raise PipelineValidationError('invalid SuperVisual composition')
        out=Path(output_dir)/Path(require_relative_path(logical_uri,'logical_uri')).name
        result=self.renderer.render_page(composition,0,out,logical_uri)
        result['manifest']['product_kind']='SUPERVISUAL';return result

class CarouselService:
    def __init__(self,renderer:SkiaStaticRenderer|None=None): self.renderer=renderer or SkiaStaticRenderer();self.pdf=SimplePdfExporter()
    def render(self,composition:Mapping[str,Any],output_dir:str|Path,logical_prefix:str)->dict[str,Any]:
        if composition['composition_kind']!='CAROUSEL' or len(composition['pages'])<2: raise PipelineValidationError('carousel requires at least two pages')
        prefix=require_relative_path(logical_prefix,'logical_prefix');outdir=Path(output_dir);outdir.mkdir(parents=True,exist_ok=True);pages=[]
        for i in range(len(composition['pages'])):
            logical=f'{prefix}-slide-{i+1:02d}.png';pages.append(self.renderer.render_page(composition,i,outdir/Path(logical).name,logical))
        pdf_path=self.pdf.export(composition,outdir/f'{Path(prefix).name}.pdf')
        core={'composition_ref':{'object_id':composition['composition_id'],'version':composition['composition_version'],'sha256':canonical_sha256(composition)},'slide_artifacts':[x['manifest'] for x in pages],'pdf_artifact':{'logical_uri':pdf_path.name,'sha256':bytes_sha256(pdf_path.read_bytes()),'byte_count':pdf_path.stat().st_size},'reading_order':[p['page_id'] for p in composition['pages']],'production_authorized':False}
        reject_noncanonical(core)
        return {'manifest':{'carousel_artifact_id':semantic_identity('carousel-artifact',core),'carousel_artifact_version':'1.0.0',**core},'pages':pages,'pdf_path':str(pdf_path)}
