from __future__ import annotations

import json
import urllib.request
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .errors import CapabilityGap, VAEValidationError
from .validation import reject_noncanonical, require_resource_ref, semantic_id


class ComfyUIGraphCompiler:
    NODE_LOCK={"LoadImage":"1.0.0","MaskComposite":"1.0.0","SaveImage":"1.0.0","VAEEncode":"1.0.0","VAEDecode":"1.0.0"}

    def compile(self, *, plan: Mapping[str,Any], workcell: Mapping[str,Any], input_refs: list[Mapping[str,Any]]) -> dict[str,Any]:
        refs=[require_resource_ref(item,f"input_refs[{index}]") for index,item in enumerate(input_refs)]
        graph={
            "nodes":{
                "10":{"class_type":"LoadImage","version":self.NODE_LOCK["LoadImage"],"inputs":{"artifact_ref":refs[0]}},
                "20":{"class_type":"MaskComposite","version":self.NODE_LOCK["MaskComposite"],"inputs":{"source":["10",0],"mask_ref":refs[1] if len(refs)>1 else refs[0]}},
                "30":{"class_type":"VAEEncode","version":self.NODE_LOCK["VAEEncode"],"inputs":{"pixels":["20",0]}},
                "40":{"class_type":"VAEDecode","version":self.NODE_LOCK["VAEDecode"],"inputs":{"samples":["30",0]}},
                "50":{"class_type":"SaveImage","version":self.NODE_LOCK["SaveImage"],"inputs":{"images":["40",0],"filename_prefix":"ca-phase8-output"}},
            },
            "execution_policy":{"network_fetch_allowed":False,"runtime_node_install_allowed":False,"manual_graph_edit_allowed":False},
        }
        reject_noncanonical(graph)
        core={"plan_ref":{"object_id":plan["plan_id"],"version":plan["plan_version"],"sha256":canonical_sha256(plan)},"workcell_ref":{"object_id":workcell["workcell_id"],"version":workcell["workcell_version"],"sha256":canonical_sha256(workcell)},"node_lock":dict(sorted(self.NODE_LOCK.items())),"graph":graph,"runtime_execution_authorized":False,"compiler_claim":"GRAPH_COMPILED_NOT_EXECUTED"}
        return {"bundle_id":semantic_id("comfyui-graph",core),"bundle_version":"1.0.0","graph_sha256":canonical_sha256(graph),**core}

    def validate(self, bundle: Mapping[str,Any]) -> None:
        if bundle["node_lock"]!=dict(sorted(self.NODE_LOCK.items())): raise VAEValidationError("ComfyUI node lock mismatch")
        if canonical_sha256(bundle["graph"])!=bundle["graph_sha256"]: raise VAEValidationError("ComfyUI graph hash mismatch")
        policy=bundle["graph"]["execution_policy"]
        if any(policy.values()): raise VAEValidationError("ComfyUI graph enables forbidden mutable behavior")
        for node in bundle["graph"]["nodes"].values():
            if self.NODE_LOCK.get(node["class_type"])!=node["version"]: raise VAEValidationError("unregistered ComfyUI node or version")


class ComfyUIHttpAdapter:
    def __init__(self, endpoint: str, timeout_seconds: int = 30): self.endpoint=endpoint.rstrip("/"); self.timeout_seconds=timeout_seconds
    def submit(self, bundle: Mapping[str,Any]) -> dict[str,Any]:
        payload=json.dumps({"prompt":bundle["graph"],"client_id":"conscious-activations-phase8"}).encode()
        request=urllib.request.Request(self.endpoint+"/prompt",data=payload,headers={"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(request,timeout=self.timeout_seconds) as response:
                body=json.loads(response.read().decode())
        except Exception as exc:
            raise CapabilityGap(f"ComfyUI HTTP submission failed: {exc}") from exc
        return {"executed":True,"endpoint_class":"OPERATOR_CONFIGURED_HTTP","response":body,"graph_sha256":bundle["graph_sha256"]}
