from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class ContentSubsystemCompilerService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def compile_clusters(self, beat_map, source_packet):
        clusters = self.story_doctor.compile_clusters(beat_map, source_packet)
        graph = self.story_doctor.compile_cluster_meaning_graph(clusters)
        return clusters, graph
