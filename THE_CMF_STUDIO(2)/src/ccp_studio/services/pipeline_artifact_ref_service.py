from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineArtifactRef, PipelineArtifactRole, PipelineArtifactStorageState
class PipelineArtifactRefService:
    def pointer(self, role: PipelineArtifactRole, uri: str, source_ref_ids=None, **kwargs): return PipelineArtifactRef(role=role, uri=uri, source_ref_ids=source_ref_ids or [], storage_state=PipelineArtifactStorageState.POINTER_ONLY, **kwargs)
    def materialized(self, role: PipelineArtifactRole, uri: str, sha256: str, source_ref_ids=None, **kwargs): return PipelineArtifactRef(role=role, uri=uri, source_ref_ids=source_ref_ids or [], storage_state=PipelineArtifactStorageState.MATERIALIZED, sha256=sha256, **kwargs)
