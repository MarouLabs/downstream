from dataclasses import dataclass
from typing import Optional


@dataclass
class DownloadOptions:
    """Data structure representing video download options for building yt-dlp commands"""

    video_format: Optional[str] = None
    audio_format: Optional[str] = None
    video_resolution: Optional[str] = None
    force_overwrite: Optional[bool] = None
    embed_metadata: Optional[bool] = None
    embed_thumbnail: Optional[bool] = None
    apple_devices_compatible: Optional[bool] = None
    referrer: Optional[str] = None
    audio_only: Optional[bool] = None
    verbose: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DownloadOptions':
        """
        Create a DownloadOptions instance from a dictionary, with optional default values.

        Args:
            data: Dictionary containing download option values
            defaults: Dictionary containing default values for optional fields

        Returns:
            DownloadOptions instance
        """

        return cls(
            video_format=data.get('video_format'),
            audio_format=data.get('audio_format'),
            video_resolution=data.get('video_resolution'),
            force_overwrite=data.get('force_overwrite'),
            embed_metadata=data.get('embed_metadata'),
            embed_thumbnail=data.get('embed_thumbnail'),
            apple_devices_compatible=data.get('apple_devices_compatible'),
            verbose=data.get('verbose'),
            audio_only=data.get('audio_only'),
            referrer=data.get('referrer')
        )
