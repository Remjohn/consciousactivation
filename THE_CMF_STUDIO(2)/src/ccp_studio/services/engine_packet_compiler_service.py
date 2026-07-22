from __future__ import annotations

from ccp_studio.services.narrative_story_doctor_service import NarrativeStoryDoctorService


class EnginePacketCompilerService:
    def __init__(self, story_doctor: NarrativeStoryDoctorService | None = None):
        self.story_doctor = story_doctor or NarrativeStoryDoctorService()

    def compile_core_packets(self, cluster, beat_map, expression_inventory, edge):
        return {
            "supervisual": self.story_doctor.compile_supervisual_packet(cluster, edge),
            "carousel": self.story_doctor.compile_carousel_packet(cluster, edge),
            "video": self.story_doctor.compile_video_packet(beat_map, expression_inventory),
            "format01": self.story_doctor.compile_format01_packet(cluster, beat_map, edge),
        }
