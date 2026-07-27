"""Governed, provider-neutral Builder skill contracts.

The package contains Builder-owned compilation and lifecycle contracts.  It does
not contain an external model provider, skill runtime, or product authority.
"""

from cmf_builder.skills.necessity import (
    ACTIVATIVE_COMPILER_SKILL_ID,
    HarnessSkillMode,
    SkillRequirementDecision,
    determine_skill_requirement,
)
from cmf_builder.skills.activative_contracts import (
    ActivativeCompilerInput,
    ActivativeIntelligencePack,
)
from cmf_builder.skills.portable_package import PortableSkillPackage

__all__ = [
    "ACTIVATIVE_COMPILER_SKILL_ID",
    "ActivativeCompilerInput",
    "ActivativeIntelligencePack",
    "HarnessSkillMode",
    "SkillRequirementDecision",
    "PortableSkillPackage",
    "determine_skill_requirement",
]
