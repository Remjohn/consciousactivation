"""Voice continuity critic boundary for TS-CMF-011."""

from __future__ import annotations

from uuid import UUID

from ccp_studio.contracts.voice import CalibrationReport, new_calibration_report


class VoiceContinuityCritic:
    def evaluate(
        self,
        *,
        render_output_id: UUID,
        semantic_continuity_score: float,
        voice_continuity_score: float,
        anti_draft_score: float,
        evidence_refs: list[str],
    ) -> CalibrationReport:
        return new_calibration_report(
            render_output_id=render_output_id,
            semantic_continuity_score=semantic_continuity_score,
            voice_continuity_score=voice_continuity_score,
            anti_draft_score=anti_draft_score,
            evidence_refs=evidence_refs,
        )
