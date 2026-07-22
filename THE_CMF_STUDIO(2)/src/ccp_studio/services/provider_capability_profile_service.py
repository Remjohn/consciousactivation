from ccp_studio.contracts.provider_runtime import ProviderCapabilityProfile, ProviderJobKind, ProviderName, ProviderRole

class ProviderCapabilityProfileService:
    def compile_ideogram_profile(self, configured=False, tested=False, available=False):
        return ProviderCapabilityProfile(
            provider_name=ProviderName.IDEOGRAM,
            provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR,
            capability_id="provider:image:ideogram",
            configured=configured,
            tested=tested,
            available=available,
            supported_job_kinds=[ProviderJobKind.SCENE_SAMPLE, ProviderJobKind.TEMPLATE_PREVIEW_SAMPLE, ProviderJobKind.SINGLE_COMPOSITION_PLATE, ProviderJobKind.COMPOSITION_PLATE_BATCH],
            model_family="ideogram",
        )

    def compile_flux_profile(self, configured=False, tested=False, available=False):
        return ProviderCapabilityProfile(
            provider_name=ProviderName.FLUX,
            provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
            capability_id="provider:image:flux",
            configured=configured,
            tested=tested,
            available=available,
            supported_job_kinds=[ProviderJobKind.FACE_PLATE_SAMPLE, ProviderJobKind.SINGLE_REFERENCE_EDIT, ProviderJobKind.REFERENCE_EDIT_BATCH],
            model_family="flux",
        )
