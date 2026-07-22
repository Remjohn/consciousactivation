from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class ExtractionCommanderService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def authorize(self, source_fidelity, gap_report=None):
        return self.story_doctor.authorize_extraction(source_fidelity, gap_report)
