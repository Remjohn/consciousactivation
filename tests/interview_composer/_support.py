from __future__ import annotations

from typing import Any

from conscious_activations_interview_composer.application import InterviewComposerApplication

AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def ref(object_id: str, sha256: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha256 or ("f" * 64)}


def composer_app(tmp_path) -> InterviewComposerApplication:
    app = InterviewComposerApplication(tmp_path / "ic.sqlite3")
    app.initialize()
    return app


def valid_seed() -> dict[str, object]:
    return {
        "psychological_role": "self-recognizing witness",
        "tension": "keep control as proof of competence or recognize what it prevents",
        "activation_direction_set": ["MIRROR"],
        "pressure_path": "concealed protection to visible relational cost",
        "stance": "name the protective logic before offering movement",
        "counteractivation_strategy": "preserve the hesitation and belief revision before any instruction",
        "smallest_commitment": "notice one moment when control prevents listening",
    }


def valid_question(qid: str = "q1") -> dict[str, str]:
    return {
        "question_text": "What happened when you realized that?",
        "activation_direction": "MIRROR",
        "psychological_role": "self-recognizing witness",
    }