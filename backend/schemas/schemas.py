from marshmallow import Schema, fields, validate, validates, ValidationError
from urllib.parse import urlparse

supported_video_formats_input = ['mp4']
supported_video_resolutions_input = ['best', '1440', '1080', '720', '480', '360', '240', '144']
supported_audio_formats_input = ['m4a', 'mp3']

default_video_format = 'mp4'
default_audio_format = 'm4a'
default_output_format = None
default_video_resolution = '1080'

default_force_overwrite = False
default_embed_metadata = False
default_embed_thumbnail = True


class URLField(fields.Field):
    """Custom field for URL validation"""
    def _deserialize(self, value, attr, data, **kwargs):
        if not value or not isinstance(value, str):
            raise ValidationError('URL must be a non-empty string')

        try:
            parsed_url = urlparse(value)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValidationError('Invalid URL format')
        except Exception:
            raise ValidationError('Invalid URL format')

        return value


class DownloadWithOptionsSchema(Schema):
    """Schema for /download endpoint with options"""
    url = URLField(required=True)
    video_resolution = fields.String(
        required=False,
        validate=validate.OneOf(supported_video_resolutions_input),
        load_default=default_video_resolution
    )
    video_format = fields.String(
        required=False,
        validate=validate.OneOf(supported_video_formats_input),
        load_default=default_video_format
    )
    audio_format = fields.String(
        required=False,
        validate=validate.OneOf(supported_audio_formats_input),
        load_default=default_audio_format
    )
    referrer = URLField(required=False, load_default=None)
    embed_metadata = fields.Boolean(required=False, load_default=default_embed_metadata)
    embed_thumbnail = fields.Boolean(required=False, load_default=default_embed_thumbnail)
    force_overwrite = fields.Boolean(required=False, load_default=default_force_overwrite)
    apple_devices_compatible = fields.Boolean(required=False, load_default=False)
    verbose = fields.Boolean(required=False, load_default=False)

    class Meta:
        # Only allow these fields
        unknown = "raise"

class DownloadAudioWithOptionsSchema(Schema):
    """Schema for /download endpoint with options"""
    url = URLField(required=True)
    audio_format = fields.String(
        required=False,
        validate=validate.OneOf(supported_audio_formats_input),
        load_default=default_audio_format
    )
    referrer = URLField(required=False, load_default=None)
    embed_metadata = fields.Boolean(required=False, load_default=default_embed_metadata)
    embed_thumbnail = fields.Boolean(required=False, load_default=default_embed_thumbnail)
    force_overwrite = fields.Boolean(required=False, load_default=default_force_overwrite)
    verbose = fields.Boolean(required=False, load_default=False)
    audio_only = True

    class Meta:
        # Only allow these fields
        unknown = "raise"


class DownloadBestSchema(Schema):
    """Schema for /download-best endpoint (minimal options)"""
    url = URLField(required=True)

    class Meta:
        # Only allow these fields
        unknown = "raise"


class DownloadResponseSchema(Schema):
    """Schema for successful download response"""
    status = fields.String()
    message = fields.String()
    output = fields.String(required=False)


class ErrorResponseSchema(Schema):
    """Schema for error response"""
    status = fields.String()
    message = fields.String()
    details = fields.String(required=False)
