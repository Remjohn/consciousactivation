from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineRecipeCatalog, PipelineRecipeId
from ccp_studio.services.pipeline_recipe_registry_service import PipelineRecipeRegistryService
class PipelineRecipeCatalogService:
    def __init__(self, registry=None): self.registry = registry or PipelineRecipeRegistryService()
    def compile_catalog(self): return PipelineRecipeCatalog(recipes=self.registry.all_recipes())
    def get_recipe(self, recipe_id: PipelineRecipeId):
        for r in self.compile_catalog().recipes:
            if r.recipe_id == recipe_id: return r
        raise KeyError(recipe_id)
