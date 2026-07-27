from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from ca_contracts import canonical_sha256
from ..domain.errors import PipelineValidationError
from ..domain.validation import require_ref, require_string, reject_noncanonical, semantic_identity

class RemotionBindingCompiler:
    def compile(self, *, program: Mapping[str,Any], composition_id: str, runtime_ref: Mapping[str,Any]) -> dict[str,Any]:
        runtime=require_ref(runtime_ref,"runtime_ref")
        cid=require_string(composition_id,"composition_id")
        props={"programId":program["program_id"],"programVersion":program["program_version"],"programSha256":canonical_sha256(program),"canvas":program["canvas"],"tracks":program["tracks"]}
        core={"binding_kind":"REMOTION","composition_id":cid,"runtime_ref":runtime,"input_props":props,"canonical_source":"VideoEditProgram","runtime_execution_authorized":False,"production_authorized":False}
        reject_noncanonical(core)
        return {"binding_id":semantic_identity("remotion-binding",core),"binding_version":"1.0.0",**core}

class HyperFramesBindingCompiler:
    def compile(self, *, program: Mapping[str,Any], block_registry_ref: Mapping[str,Any], block_ids: list[str]) -> dict[str,Any]:
        registry=require_ref(block_registry_ref,"block_registry_ref")
        ids=[require_string(x,f"block_ids[{i}]") for i,x in enumerate(block_ids)]
        if ids!=sorted(set(ids)): raise PipelineValidationError("block IDs must be sorted and unique")
        core={"binding_kind":"HYPERFRAMES","program_ref":{"object_id":program["program_id"],"version":program["program_version"],"sha256":canonical_sha256(program)},"block_registry_ref":registry,"block_ids":ids,"seekable_timebase":program["timebase"],"canonical_source":"VideoEditProgram","runtime_execution_authorized":False,"production_authorized":False}
        reject_noncanonical(core)
        return {"binding_id":semantic_identity("hyperframes-binding",core),"binding_version":"1.0.0",**core}
