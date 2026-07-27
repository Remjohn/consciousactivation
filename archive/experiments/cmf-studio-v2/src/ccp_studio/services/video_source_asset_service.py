from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import VideoSourceAssetSet, VideoSourceMedia


class VideoSourceAssetService:
    def compile_source_asset_set(
        self,
        *,
        source_media: list[VideoSourceMedia],
        source_span_refs: list[str],
    ) -> VideoSourceAssetSet:
        asset_hashes = {media.source_media_id: media.source_ref for media in source_media}
        return VideoSourceAssetSet(source_media=source_media, source_span_refs=source_span_refs, asset_hashes=asset_hashes)
