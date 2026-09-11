from __future__ import annotations

from dataclasses import asdict, dataclass

from ..domain.errors import PipelineValidationError


@dataclass(frozen=True, slots=True)
class CompilerProfile:
    profile_id: str
    package_profile: str
    category_mode: str
    semantic_mode: str
    version: str


class HarnessDefinitionProfileRegistry:
    def __init__(self):
        profiles = (
            CompilerProfile("portable-generic-v1", "portable_generic_v1", "generic", "generic", "1.0.0"),
            CompilerProfile("portable-activative-v1", "portable_activative_v1", "category_bound", "activative", "1.0.0"),
        )
        self._profiles = {item.package_profile: item for item in profiles}

    def resolve(self, package_profile: str) -> CompilerProfile:
        try:
            return self._profiles[package_profile]
        except KeyError as exc:
            raise PipelineValidationError(
                f"no exact Harness compiler profile for package_profile={package_profile!r}"
            ) from exc

    def status(self) -> dict[str, object]:
        return {
            "profile_count": len(self._profiles),
            "profiles": [asdict(item) for item in sorted(self._profiles.values(), key=lambda value: value.profile_id)],
            "shape_guessing_enabled": False,
        }
