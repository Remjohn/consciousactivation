from __future__ import annotations
from dataclasses import dataclass
from ..domain.errors import PipelineValidationError

@dataclass(frozen=True)
class TextMeasurement:
    lines: tuple[str,...]; width_px:int; height_px:int; font_size_px:int; line_height_px:int; fits:bool
    def to_dict(self): return {'lines':list(self.lines),'width_px':self.width_px,'height_px':self.height_px,'font_size_px':self.font_size_px,'line_height_px':self.line_height_px,'fits':self.fits}

class PretextEngine:
    """Deterministic integer text-measurement and wrapping reference engine."""
    def glyph_width(self,ch:str,font_size:int)->int:
        if ch==' ': return max(1,font_size*35//100)
        if ch in 'ilI.,:;!|': return max(1,font_size*28//100)
        if ch in 'MW@#%&': return max(1,font_size*85//100)
        return max(1,font_size*58//100)
    def measure_line(self,text:str,font_size:int)->int: return sum(self.glyph_width(ch,font_size) for ch in text)
    def wrap(self,text:str,max_width_px:int,font_size_px:int,max_height_px:int,line_height_bps:int=12000)->TextMeasurement:
        if max_width_px<=0 or max_height_px<=0 or font_size_px<=0: raise PipelineValidationError('invalid text measurement bounds')
        words=text.split();lines=[];current=''
        for word in words:
            candidate=word if not current else current+' '+word
            if self.measure_line(candidate,font_size_px)<=max_width_px: current=candidate
            elif current:
                lines.append(current);current=word
            else:
                # hard wrap an overlong token
                chunk=''
                for ch in word:
                    if chunk and self.measure_line(chunk+ch,font_size_px)>max_width_px: lines.append(chunk);chunk=ch
                    else: chunk+=ch
                current=chunk
        if current or not lines: lines.append(current)
        line_height=max(font_size_px,font_size_px*line_height_bps//10000)
        width=max((self.measure_line(line,font_size_px) for line in lines),default=0);height=len(lines)*line_height
        return TextMeasurement(tuple(lines),width,height,font_size_px,line_height,width<=max_width_px and height<=max_height_px)
    def fit(self,text:str,max_width_px:int,max_height_px:int,max_font_size_px:int,min_font_size_px:int=12)->TextMeasurement:
        for size in range(max_font_size_px,min_font_size_px-1,-1):
            result=self.wrap(text,max_width_px,size,max_height_px)
            if result.fits:return result
        return self.wrap(text,max_width_px,min_font_size_px,max_height_px)
