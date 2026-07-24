from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_int, require_string

SCALE=1_000_000

@dataclass(frozen=True)
class BBox:
    x:int;y:int;width:int;height:int
    @classmethod
    def from_mapping(cls,value:Mapping[str,Any],field='bbox'):
        if not isinstance(value,Mapping) or set(value)!={'x','y','width','height'}: raise PipelineValidationError(f'{field} invalid shape')
        box=cls(*(require_int(value[k],f'{field}.{k}') for k in ('x','y','width','height')))
        if box.width<=0 or box.height<=0 or box.x+box.width>SCALE or box.y+box.height>SCALE: raise PipelineValidationError(f'{field} outside normalized canvas')
        return box
    def to_dict(self): return {'x':self.x,'y':self.y,'width':self.width,'height':self.height}
    def intersects(self,other:'BBox')->bool: return self.x<other.x+other.width and other.x<self.x+self.width and self.y<other.y+other.height and other.y<self.y+self.height
    def intersection_area(self,other:'BBox')->int:
        if not self.intersects(other): return 0
        return max(0,min(self.x+self.width,other.x+other.width)-max(self.x,other.x))*max(0,min(self.y+self.height,other.y+other.height)-max(self.y,other.y))

class GeometryValidator:
    def validate_elements(self,elements:list[Mapping[str,Any]])->dict[str,Any]:
        boxes=[];ids=set();violations=[]
        for i,e in enumerate(elements):
            if not isinstance(e,Mapping): raise PipelineValidationError('element must be object')
            element_id=require_string(e.get('element_id'),f'elements[{i}].element_id')
            if element_id in ids: raise PipelineValidationError('duplicate element ID')
            ids.add(element_id);box=BBox.from_mapping(e.get('bbox'),f'elements[{i}].bbox');boxes.append((element_id,box,e))
        for i,(aid,a,aobj) in enumerate(boxes):
            for bid,b,bobj in boxes[i+1:]:
                if a.intersects(b) and not (aobj.get('overlap_allowed') is True and bobj.get('overlap_allowed') is True):
                    violations.append({'code':'BBOX_COLLISION','a':aid,'b':bid,'intersection_area':a.intersection_area(b)})
        return {'result':'PASS' if not violations else 'FAIL','violations':violations,'element_count':len(elements)}
