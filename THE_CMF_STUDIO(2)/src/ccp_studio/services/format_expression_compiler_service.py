from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class FormatExpressionCompilerService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def score(self, cluster):
        return self.story_doctor.score_format_fit(cluster)
