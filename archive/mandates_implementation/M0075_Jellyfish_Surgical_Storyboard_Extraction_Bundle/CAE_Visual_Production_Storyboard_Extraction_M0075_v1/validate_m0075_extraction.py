"""Validate the M0075 reference-only extraction contract without CAE runtime integration."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
MAPPING = ROOT / "M0075_JELLYFISH_MAPPING.json"
REQUIRED_ADOPTED = {"JF-01", "JF-02", "JF-03", "JF-04", "JF-05"}
REQUIRED_EXCLUSIONS = {
    "Jellyfish database schema and project/task authority model",
    "Jellyfish frontend UI state as a source of truth",
    "provider/model configuration",
    "generation runtime and task execution",
    "external service invocation",
    "parallel authoritative storyboard state model",
    "new StoryboardSession/StoryboardRevision persistent objects",
}


def validate() -> None:
    data = json.loads(MAPPING.read_text(encoding="utf-8"))
    assert data["mandate_id"] == "M0075"
    assert data["status"] == "BLOCKED_OPERATOR_REVIEW_REQUIRED"
    assert data["source"]["license"] == "Apache-2.0"
    assert data["source"]["source_commit_sha"] is None
    ids = {item["id"] for item in data["adopted_behaviors"]}
    assert ids == REQUIRED_ADOPTED
    assert set(data["excluded_behavior"]) == REQUIRED_EXCLUSIONS
    assert data["concept_mapping"]["StoryboardSession"]["cae_authority"] == [
        "EditorialStoryboardRecord",
        "PreparationGraphRecord",
    ]
    assert data["concept_mapping"]["StoryboardRevision"]["cae_authority"] == ["GraphRevisionRecord"]
    assert "StaleBaseRevisionError" in data["revision_and_operator_mapping"]["edit"]["error_route"]
    assert data["anti_centroid"]["expected_result"].startswith("presentation is allowed")


if __name__ == "__main__":
    validate()
    print("M0075 reference extraction validation: PASS")
