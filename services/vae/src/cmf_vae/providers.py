from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from ca_contracts import canonical_json_text, canonical_sha256

from .errors import CapabilityGap, VAEValidationError
from .png import gray_png, rgba_png
from .storage import ContentAddressedStore
from .validation import reject_noncanonical, safe_relative


class ReferenceProviders:
    def __init__(self, store: ContentAddressedStore):
        self.store=store

    def segmentation(self, *, width: int, height: int, logical_uri: str, demand_id: str) -> dict[str, Any]:
        cx,cy=width//2,height//2
        rx,ry=max(1,width*3//10),max(1,height*2//5)
        def mask(x,y):
            return 255 if ((x-cx)*(x-cx)*10000//(rx*rx)+(y-cy)*(y-cy)*10000//(ry*ry))<=10000 else 0
        data=gray_png(width,height,mask)
        artifact=self.store.put(data,logical_uri=logical_uri,media_type="image/png",metadata={"capability":"REFERENCE_SEGMENTATION","demand_id":demand_id})
        geometry={
            "geometry_pack_id":f"geometry:{canonical_sha256({'demand_id':demand_id,'width':width,'height':height})}",
            "subject_bbox":{"x":2000,"y":1000,"width":6000,"height":8000},
            "face_bbox":{"x":3800,"y":1800,"width":2400,"height":2200},
            "gaze_vector":{"x_basis_points":1500,"y_basis_points":0},
            "negative_space_regions":[{"x":6200,"y":800,"width":3000,"height":2600}],
            "mask_ref":artifact["resource_ref"],
            "provider_claim":"REFERENCE_IMPLEMENTATION_NOT_SAM3",
        }
        return {"artifact":artifact,"geometry":geometry,"execution_evidence":{"executed":True,"provider":"CMF_REFERENCE_SEGMENTER","real_sam3":False}}

    def matting(self, *, width: int, height: int, logical_uri: str, demand_id: str) -> dict[str, Any]:
        cx,cy=width//2,height//2; rx,ry=max(1,width*3//10),max(1,height*2//5)
        def pixel(x,y):
            metric=((x-cx)*(x-cx)*10000//(rx*rx)+(y-cy)*(y-cy)*10000//(ry*ry))
            alpha=255 if metric<8500 else max(0,255-(metric-8500)//10)
            return (75+(x*80//max(1,width-1)),100+(y*60//max(1,height-1)),170,alpha)
        data=rgba_png(width,height,pixel)
        artifact=self.store.put(data,logical_uri=logical_uri,media_type="image/png",metadata={"capability":"REFERENCE_MATTING","demand_id":demand_id})
        return {"artifact":artifact,"execution_evidence":{"executed":True,"provider":"CMF_REFERENCE_MATTER","real_lucida":False}}

    def materialize(self, *, width: int, height: int, logical_uri: str, demand_id: str, wrong_reading_locks: Sequence[str]) -> dict[str, Any]:
        def pixel(x,y):
            bg=(18+x*30//max(1,width-1),28+y*30//max(1,height-1),55,255)
            if width//5 < x < width*3//5 and height//8 < y < height*9//10:
                return (72+x*45//max(1,width-1),115+y*55//max(1,height-1),175,255)
            return bg
        data=rgba_png(width,height,pixel)
        artifact=self.store.put(data,logical_uri=logical_uri,media_type="image/png",metadata={"capability":"REFERENCE_RASTER","demand_id":demand_id,"wrong_reading_locks":list(wrong_reading_locks)})
        return {"artifact":artifact,"execution_evidence":{"executed":True,"provider":"CMF_REFERENCE_RASTERIZER","production_provider":False}}

    def gnm_geometry(self, *, demand_id: str, purpose: str, head_pose: Mapping[str,int], gaze: Mapping[str,int], logical_uri: str) -> dict[str, Any]:
        if purpose not in {"GEOMETRY_REFERENCE","POSE_REFERENCE","GAZE_REFERENCE","EXPRESSION_GEOMETRY_REFERENCE"}:
            raise VAEValidationError("GNM may be used only for bounded geometry, pose, gaze, or expression-geometry reference")
        payload={
            "gnm_reference_id":f"gnm-ref:{canonical_sha256({'demand_id':demand_id,'purpose':purpose,'head_pose':head_pose,'gaze':gaze})}",
            "purpose":purpose,
            "demand_id":demand_id,
            "head_pose":dict(head_pose),
            "gaze":dict(gaze),
            "landmarks":[{"name":"left_eye","x_basis_points":4000,"y_basis_points":3500},{"name":"right_eye","x_basis_points":6000,"y_basis_points":3500},{"name":"chin","x_basis_points":5000,"y_basis_points":7600}],
            "mesh_summary":{"vertex_count":128,"face_count":224},
            "identity_authority":False,
            "emotional_truth_authority":False,
            "provider_claim":"REFERENCE_GEOMETRY_NOT_REAL_GNM_EXECUTION",
        }
        artifact=self.store.put((canonical_json_text(payload)+"\n").encode(),logical_uri=logical_uri,media_type="application/json",metadata={"capability":"REFERENCE_GNM_GEOMETRY","demand_id":demand_id})
        return {"artifact":artifact,"geometry":payload,"execution_evidence":{"executed":True,"real_google_gnm":False}}


class ExternalCommandProvider:
    def __init__(self, *, provider_id: str, command_template: Sequence[str], timeout_seconds: int = 120):
        if not command_template: raise CapabilityGap("external provider command is empty")
        self.provider_id=provider_id; self.command_template=list(command_template); self.timeout_seconds=timeout_seconds

    def execute(self, request: Mapping[str,Any], output_dir: str|Path) -> dict[str,Any]:
        reject_noncanonical(request)
        out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
        request_path=out/"request.json"; response_path=out/"response.json"
        request_path.write_text(canonical_json_text(request)+"\n",encoding="utf-8")
        command=[item.replace("{request}",str(request_path)).replace("{response}",str(response_path)).replace("{output_dir}",str(out)) for item in self.command_template]
        result=subprocess.run(command,text=True,capture_output=True,timeout=self.timeout_seconds)
        if result.returncode!=0:
            raise CapabilityGap(f"{self.provider_id} command failed: {result.stderr[-1000:]}")
        if not response_path.is_file(): raise CapabilityGap(f"{self.provider_id} did not produce response.json")
        response=json.loads(response_path.read_text(encoding="utf-8")); reject_noncanonical(response)
        if response.get("provider_id")!=self.provider_id or response.get("request_sha256")!=canonical_sha256(request):
            raise CapabilityGap(f"{self.provider_id} response identity mismatch")
        return {"response":response,"command":[Path(command[0]).name,*command[1:]],"stdout":result.stdout[-2000:],"stderr":result.stderr[-2000:],"executed":True}
