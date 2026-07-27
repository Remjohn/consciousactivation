from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json


ACTIVATIVE_COMPILER_SKILL_ID = "activative_intelligence_pack_compiler"
ACTIVATIVE_COMPILER_SKILL_VERSION = "1.0.0"


class SkillRequirementError(ValueError):
    """A skill-necessity claim is incomplete or contradicts governed evidence."""


class HarnessSkillMode(str, Enum):
    GENERIC_DETERMINISTIC = "generic_deterministic_fixture"
    ACTIVATIVE = "activative_harness_fixture"


@dataclass(frozen=True, slots=True)
class SkillAlternativeEvidence:
    alternative: str
    adequate: bool
    reason: str
    evidence_refs: tuple[str, ...]

    def canonical_dict(self) -> dict[str, object]:
        if not self.alternative.strip() or not self.reason.strip():
            raise SkillRequirementError("Alternative evidence must be attributable.")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise SkillRequirementError("Alternative evidence references must be non-empty.")
        return {
            "alternative": self.alternative,
            "adequate": self.adequate,
            "reason": self.reason,
            "evidence_refs": sorted(set(self.evidence_refs)),
        }


@dataclass(frozen=True, slots=True)
class SkillRequirementDecision:
    mode: HarnessSkillMode
    required_capability: str
    real_skill_required: bool
    required_skill_id: str | None
    required_skill_version: str | None
    governing_policy_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    alternatives: tuple[SkillAlternativeEvidence, ...]
    decision_status: str
    production_eligible: bool
    certified: bool
    decision_hash: str

    @classmethod
    def create(
        cls,
        *,
        mode: HarnessSkillMode,
        required_capability: str,
        real_skill_required: bool,
        required_skill_id: str | None,
        required_skill_version: str | None,
        governing_policy_refs: tuple[str, ...],
        authority_refs: tuple[str, ...],
        alternatives: tuple[SkillAlternativeEvidence, ...],
        decision_status: str = "development_uncertified",
    ) -> "SkillRequirementDecision":
        if not required_capability.strip():
            raise SkillRequirementError("The required capability must be explicit.")
        if not governing_policy_refs or not authority_refs:
            raise SkillRequirementError("Policy and authority evidence are required.")
        if any(not value.strip() for value in governing_policy_refs + authority_refs):
            raise SkillRequirementError("Blank authority or policy evidence is forbidden.")
        if decision_status not in {"development_uncertified", "development_validated"}:
            raise SkillRequirementError("A development decision cannot claim certification.")
        if real_skill_required:
            if (
                required_skill_id != ACTIVATIVE_COMPILER_SKILL_ID
                or required_skill_version != ACTIVATIVE_COMPILER_SKILL_VERSION
            ):
                raise SkillRequirementError("The exact governed Activative skill must be pinned.")
            if mode is not HarnessSkillMode.ACTIVATIVE:
                raise SkillRequirementError("The Activative skill is not required by the generic fixture.")
        elif required_skill_id is not None or required_skill_version is not None:
            raise SkillRequirementError("A no-skill decision cannot carry a hidden skill pin.")
        if not alternatives:
            raise SkillRequirementError("Skill alternatives must be evaluated independently.")
        alternative_payload = [item.canonical_dict() for item in alternatives]
        if real_skill_required and any(
            item["alternative"] == "deterministic_builder_code" and item["adequate"]
            for item in alternative_payload
        ):
            raise SkillRequirementError("A real skill cannot be required when code is adequate.")
        if not real_skill_required and not any(item["adequate"] for item in alternative_payload):
            raise SkillRequirementError("A no-skill decision requires an adequate governed alternative.")
        payload = {
            "schema": "cmf-builder-skill-requirement-decision/v1",
            "mode": mode.value,
            "required_capability": required_capability,
            "real_skill_required": real_skill_required,
            "required_skill_id": required_skill_id,
            "required_skill_version": required_skill_version,
            "governing_policy_refs": sorted(set(governing_policy_refs)),
            "authority_refs": sorted(set(authority_refs)),
            "alternatives": alternative_payload,
            "decision_status": decision_status,
            "production_eligible": False,
            "certified": False,
        }
        digest = sha256(_canonical_bytes(payload)).hexdigest()
        return cls(
            mode=mode,
            required_capability=required_capability,
            real_skill_required=real_skill_required,
            required_skill_id=required_skill_id,
            required_skill_version=required_skill_version,
            governing_policy_refs=tuple(payload["governing_policy_refs"]),
            authority_refs=tuple(payload["authority_refs"]),
            alternatives=alternatives,
            decision_status=decision_status,
            production_eligible=False,
            certified=False,
            decision_hash=digest,
        )

    def canonical_dict(self) -> dict[str, object]:
        payload = {
            "schema": "cmf-builder-skill-requirement-decision/v1",
            "mode": self.mode.value,
            "required_capability": self.required_capability,
            "real_skill_required": self.real_skill_required,
            "required_skill_id": self.required_skill_id,
            "required_skill_version": self.required_skill_version,
            "governing_policy_refs": list(self.governing_policy_refs),
            "authority_refs": list(self.authority_refs),
            "alternatives": [item.canonical_dict() for item in self.alternatives],
            "decision_status": self.decision_status,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
        }
        if sha256(_canonical_bytes(payload)).hexdigest() != self.decision_hash:
            raise SkillRequirementError("The skill-necessity decision hash has drifted.")
        return {**payload, "decision_hash": self.decision_hash}


def determine_skill_requirement(mode: HarnessSkillMode) -> SkillRequirementDecision:
    policy = (
        "Builder PRD V1.2:F09",
        "TS-08",
        "docs/implementation/skills/ST0503_BLOCKER_DISPOSITION.yaml",
    )
    authority = (
        "Activative Intelligence Constitution V1.1:Section 7",
        "Builder PRD V1.2",
    )
    if mode is HarnessSkillMode.GENERIC_DETERMINISTIC:
        return SkillRequirementDecision.create(
            mode=mode,
            required_capability="deterministic_synthetic_text_normalization",
            real_skill_required=False,
            required_skill_id=None,
            required_skill_version=None,
            governing_policy_refs=policy,
            authority_refs=authority,
            alternatives=(
                SkillAlternativeEvidence(
                    alternative="deterministic_builder_code",
                    adequate=True,
                    reason="The governed synthetic operation is completely deterministic and code-owned.",
                    evidence_refs=(
                        "ST-05.02:StoryCompletionReceipt",
                        "builder-core-empty-skill-registry-policy-v1",
                    ),
                ),
            ),
            decision_status="development_validated",
        )
    if mode is HarnessSkillMode.ACTIVATIVE:
        return SkillRequirementDecision.create(
            mode=mode,
            required_capability="compile_activative_intelligence_pack_without_inventing_human_truth",
            real_skill_required=True,
            required_skill_id=ACTIVATIVE_COMPILER_SKILL_ID,
            required_skill_version=ACTIVATIVE_COMPILER_SKILL_VERSION,
            governing_policy_refs=policy,
            authority_refs=authority,
            alternatives=(
                SkillAlternativeEvidence(
                    alternative="deterministic_builder_code",
                    adequate=False,
                    reason="Code validates contracts but cannot replace governed semantic compilation under Analyst authority.",
                    evidence_refs=("Builder PRD V1.2:F09", "XDEP-006"),
                ),
                SkillAlternativeEvidence(
                    alternative="inline_instruction",
                    adequate=False,
                    reason="Inline instructions are not versioned, behaviorally evaluated, or portable.",
                    evidence_refs=("FR-087", "FR-088", "FR-089", "FR-090"),
                ),
                SkillAlternativeEvidence(
                    alternative="canonical_portable_skill",
                    adequate=True,
                    reason="A pinned package preserves behavioral anchors, authority boundaries, lineage, and evaluator evidence.",
                    evidence_refs=("TS-08", "ADR-009", "ST-05.03"),
                ),
            ),
        )
    raise SkillRequirementError(f"Unsupported skill mode: {mode!r}")


def _canonical_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
