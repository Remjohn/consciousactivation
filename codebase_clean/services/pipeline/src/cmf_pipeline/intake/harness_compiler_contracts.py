from __future__ import annotations

from dataclasses import dataclass


class HarnessCompilationBlocked(Exception):
    def __init__(self, *, field: str, reason: str, blocker_ref: str) -> None:
        super().__init__(f"{field}: {reason} (see {blocker_ref})")
        self.field = field
        self.reason = reason
        self.blocker_ref = blocker_ref  # e.g. "TS-APP-BRIDGE-001#blocker-5"


BLOCKER_1_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for versioned, "
    "hashed semantic references; provenance_refs are bare strings without "
    "version or sha256 — see TS-APP-BRIDGE-001 Section 4 Blocker 1"
)
BLOCKER_2_TEXT = (
    "capability_requirements are bare capability_id strings; owner_kind, "
    "required_features, and authority_boundary have no source — see "
    "TS-APP-BRIDGE-001 Section 4 Blocker 2"
)
BLOCKER_3_TEXT = (
    "mode='generic' Harnesses have category_id=None; this compiler only "
    "supports mode='activative' — see TS-APP-BRIDGE-001 Section 4 Blocker 3 "
    "for the open question of whether generic Harnesses need Pipeline "
    "execution at all"
)
BLOCKER_4_TEXT = (
    "manifest_version is not valid semantic version format "
    "(^[0-9]+\\.[0-9]+\\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$) — see "
    "TS-APP-BRIDGE-001 Section 4 Blocker 4"
)
BLOCKER_5_TEXT = (
    "no source structure in PortableAtomicHarnessDefinition for a "
    "multi-node workflow graph; Builder produces one flat atomic task, not "
    "a decomposed node/edge graph — this is the central unresolved product "
    "decision in TS-APP-BRIDGE-001 Section 4 Blocker 5, offered but not "
    "decided unilaterally"
)
BLOCKER_6_EVAL_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for evaluation "
    "requirements — see TS-APP-BRIDGE-001 Section 4 Blocker 6"
)
BLOCKER_6_REPAIR_TEXT = (
    "no source field in PortableAtomicHarnessDefinition for repair laws — "
    "see TS-APP-BRIDGE-001 Section 4 Blocker 6"
)
