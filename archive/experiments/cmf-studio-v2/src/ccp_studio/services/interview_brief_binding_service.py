from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class InterviewBriefBindingService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def bind(self, context, brief: dict):
        binding = self.story_doctor.bind_interview_brief(context, brief)
        graph = self.story_doctor.compile_expected_ingredient_graph(binding)
        return binding, graph
