from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class PrimitiveCoalitionCompilerService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def compile(self, cluster, edge=None):
        primitive_set = self.story_doctor.compile_primitive_candidates(cluster, edge)
        coalition = self.story_doctor.compile_primitive_coalition(primitive_set)
        return primitive_set, coalition
