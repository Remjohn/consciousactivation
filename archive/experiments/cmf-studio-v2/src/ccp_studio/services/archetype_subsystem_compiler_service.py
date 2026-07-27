from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class ArchetypeSubsystemCompilerService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def compile(self, cluster):
        matrix = self.story_doctor.score_archetype_fit(cluster)
        program = self.story_doctor.compile_archetype_program(matrix)
        recipe = self.story_doctor.compile_delivery_recipe(program)
        return matrix, program, recipe
