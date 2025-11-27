import pytest
from models.download_options import DownloadOptions


class TestDownloadOptionsInstantiation:
    """Test cases for creating DownloadOptions instances"""

    def test_create_with_all_fields(self):
        """Test creating DownloadOptions with all fields"""
        options = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            video_resolution='1080',
            force_overwrite=True,
            embed_metadata=True,
            embed_thumbnail=True,
            apple_devices_compatible=False,
            referrer='https://example.com',
            audio_only=False,
            verbose=True
        )

        assert options.video_format == 'mp4'
        assert options.audio_format == 'm4a'
        assert options.video_resolution == '1080'
        assert options.force_overwrite is True
        assert options.embed_metadata is True
        assert options.embed_thumbnail is True
        assert options.apple_devices_compatible is False
        assert options.referrer == 'https://example.com'
        assert options.audio_only is False
        assert options.verbose is True

    def test_create_with_default_values(self):
        """Test creating DownloadOptions with default values"""
        options = DownloadOptions()

        assert options.video_format is None
        assert options.audio_format is None
        assert options.video_resolution is None
        assert options.force_overwrite is None
        assert options.embed_metadata is None
        assert options.embed_thumbnail is None
        assert options.apple_devices_compatible is None
        assert options.referrer is None
        assert options.audio_only is None
        assert options.verbose is None

    def test_create_with_partial_fields(self):
        """Test creating DownloadOptions with partial fields"""
        options = DownloadOptions(
            video_format='mp4',
            video_resolution='720',
            verbose=True
        )

        assert options.video_format == 'mp4'
        assert options.video_resolution == '720'
        assert options.verbose is True
        assert options.audio_format is None
        assert options.force_overwrite is None


class TestDownloadOptionsFromDict:
    """Test cases for DownloadOptions.from_dict classmethod"""

    def test_from_dict_empty(self):
        """Test creating DownloadOptions from empty dictionary"""
        data = {}
        options = DownloadOptions.from_dict(data)

        assert isinstance(options, DownloadOptions)
        assert options.video_format is None
        assert options.audio_format is None
        assert options.video_resolution is None
        assert options.force_overwrite is None
        assert options.embed_metadata is None
        assert options.embed_thumbnail is None
        assert options.apple_devices_compatible is None
        assert options.referrer is None
        assert options.audio_only is None
        assert options.verbose is None

    def test_from_dict_with_all_fields(self):
        """Test creating DownloadOptions from dictionary with all fields"""
        data = {
            'video_format': 'webm',
            'audio_format': 'opus',
            'video_resolution': '2160',
            'force_overwrite': False,
            'embed_metadata': True,
            'embed_thumbnail': False,
            'apple_devices_compatible': True,
            'referrer': 'https://test.com',
            'audio_only': True,
            'verbose': False
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_format == 'webm'
        assert options.audio_format == 'opus'
        assert options.video_resolution == '2160'
        assert options.force_overwrite is False
        assert options.embed_metadata is True
        assert options.embed_thumbnail is False
        assert options.apple_devices_compatible is True
        assert options.referrer == 'https://test.com'
        assert options.audio_only is True
        assert options.verbose is False

    def test_from_dict_with_partial_fields(self):
        """Test creating DownloadOptions from dictionary with partial fields"""
        data = {
            'video_format': 'mp4',
            'audio_format': 'aac',
            'verbose': True
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_format == 'mp4'
        assert options.audio_format == 'aac'
        assert options.verbose is True
        assert options.video_resolution is None
        assert options.force_overwrite is None
        assert options.embed_metadata is None
        assert options.embed_thumbnail is None
        assert options.apple_devices_compatible is None
        assert options.referrer is None
        assert options.audio_only is None

    def test_from_dict_with_extra_fields(self):
        """Test creating DownloadOptions from dictionary with extra unknown fields"""
        data = {
            'video_format': 'mp4',
            'unknown_field': 'should_be_ignored',
            'another_unknown': 123
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_format == 'mp4'
        assert not hasattr(options, 'unknown_field')
        assert not hasattr(options, 'another_unknown')

    def test_from_dict_with_none_values(self):
        """Test creating DownloadOptions from dictionary with explicit None values"""
        data = {
            'video_format': None,
            'audio_format': 'm4a',
            'video_resolution': None
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_format is None
        assert options.audio_format == 'm4a'
        assert options.video_resolution is None

    def test_from_dict_with_boolean_values(self):
        """Test creating DownloadOptions with various boolean values"""
        data_true = {
            'force_overwrite': True,
            'embed_metadata': True,
            'embed_thumbnail': True,
            'apple_devices_compatible': True,
            'audio_only': True,
            'verbose': True
        }
        options = DownloadOptions.from_dict(data_true)

        assert options.force_overwrite is True
        assert options.embed_metadata is True
        assert options.embed_thumbnail is True
        assert options.apple_devices_compatible is True
        assert options.audio_only is True
        assert options.verbose is True

        data_false = {
            'force_overwrite': False,
            'embed_metadata': False,
            'embed_thumbnail': False,
            'apple_devices_compatible': False,
            'audio_only': False,
            'verbose': False
        }
        options = DownloadOptions.from_dict(data_false)

        assert options.force_overwrite is False
        assert options.embed_metadata is False
        assert options.embed_thumbnail is False
        assert options.apple_devices_compatible is False
        assert options.audio_only is False
        assert options.verbose is False


class TestDownloadOptionsFieldTypes:
    """Test cases for DownloadOptions field types"""

    def test_string_fields(self):
        """Test string type fields"""
        options = DownloadOptions(
            video_format='mp4',
            audio_format='aac',
            video_resolution='1080',
            referrer='https://example.com'
        )

        assert isinstance(options.video_format, str)
        assert isinstance(options.audio_format, str)
        assert isinstance(options.video_resolution, str)
        assert isinstance(options.referrer, str)

    def test_boolean_fields(self):
        """Test boolean type fields"""
        options = DownloadOptions(
            force_overwrite=True,
            embed_metadata=False,
            embed_thumbnail=True,
            apple_devices_compatible=False,
            audio_only=True,
            verbose=False
        )

        assert isinstance(options.force_overwrite, bool)
        assert isinstance(options.embed_metadata, bool)
        assert isinstance(options.embed_thumbnail, bool)
        assert isinstance(options.apple_devices_compatible, bool)
        assert isinstance(options.audio_only, bool)
        assert isinstance(options.verbose, bool)

    def test_optional_none_values(self):
        """Test that Optional fields can be None"""
        options = DownloadOptions()

        # All fields should be None by default
        assert options.video_format is None
        assert options.audio_format is None
        assert options.video_resolution is None
        assert options.force_overwrite is None
        assert options.embed_metadata is None
        assert options.embed_thumbnail is None
        assert options.apple_devices_compatible is None
        assert options.referrer is None
        assert options.audio_only is None
        assert options.verbose is None


class TestDownloadOptionsDataclass:
    """Test cases for DownloadOptions dataclass behavior"""

    def test_dataclass_equality(self):
        """Test that two identical DownloadOptions instances are equal"""
        options1 = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            video_resolution='1080'
        )
        options2 = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            video_resolution='1080'
        )

        assert options1 == options2

    def test_dataclass_inequality(self):
        """Test that different DownloadOptions instances are not equal"""
        options1 = DownloadOptions(video_format='mp4')
        options2 = DownloadOptions(video_format='webm')

        assert options1 != options2

    def test_dataclass_repr(self):
        """Test dataclass string representation"""
        options = DownloadOptions(video_format='mp4')
        repr_str = repr(options)

        assert 'DownloadOptions' in repr_str
        assert 'video_format=' in repr_str

    def test_dataclass_is_immutable_attempt(self):
        """Test that dataclass fields can be modified (default dataclass behavior)"""
        options = DownloadOptions(video_format='mp4')

        # Dataclasses are mutable by default
        options.video_format = 'webm'
        assert options.video_format == 'webm'


class TestDownloadOptionsIntegration:
    """Integration tests for DownloadOptions with realistic scenarios"""

    def test_audio_download_options(self):
        """Test creating options for audio-only downloads"""
        data = {
            'audio_format': 'mp3',
            'audio_only': True,
            'verbose': True
        }
        options = DownloadOptions.from_dict(data)

        assert options.audio_only is True
        assert options.audio_format == 'mp3'
        assert options.video_format is None

    def test_video_download_options(self):
        """Test creating options for video downloads"""
        data = {
            'video_format': 'mp4',
            'audio_format': 'aac',
            'video_resolution': '1080',
            'force_overwrite': True
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_format == 'mp4'
        assert options.audio_format == 'aac'
        assert options.video_resolution == '1080'
        assert options.force_overwrite is True
        assert options.audio_only is None

    def test_high_quality_download_options(self):
        """Test creating options for high-quality downloads"""
        data = {
            'video_format': 'webm',
            'audio_format': 'opus',
            'video_resolution': '2160',
            'embed_metadata': True,
            'embed_thumbnail': True
        }
        options = DownloadOptions.from_dict(data)

        assert options.video_resolution == '2160'
        assert options.embed_metadata is True
        assert options.embed_thumbnail is True

    def test_minimal_download_options(self):
        """Test creating minimal options for downloads"""
        data = {'video_format': 'best'}
        options = DownloadOptions.from_dict(data)

        assert options.video_format == 'best'
        # All other fields should be None
        assert options.audio_format is None
        assert options.video_resolution is None
        assert options.force_overwrite is None

    def test_apple_compatible_options(self):
        """Test creating options for Apple-compatible downloads"""
        data = {
            'apple_devices_compatible': True,
            'embed_metadata': True
        }
        options = DownloadOptions.from_dict(data)

        assert options.apple_devices_compatible is True
        assert options.embed_metadata is True
