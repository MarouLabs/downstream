import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from services.download_service import (
    build_options_from_data,
    build_format_from_options,
    build_command,
    execute_command,
)
from models.download_options import DownloadOptions


@pytest.fixture
def flask_app():
    """Create a Flask app context for testing"""
    app = Flask(__name__)
    with app.app_context():
        yield app


class TestBuildOptionsFromData:
    """Test cases for build_options_from_data function"""

    def test_build_options_with_minimal_data(self):
        """Test building options with minimal data"""
        data = {}
        options = build_options_from_data(data)
        assert isinstance(options, DownloadOptions)
        assert options.audio_only is False
        assert options.video_format is None
        assert options.audio_format is None
        assert options.video_resolution is None

    def test_build_options_with_custom_values(self):
        """Test building options with custom values"""
        data = {
            'video_format': 'mp4',
            'audio_format': 'wav',
            'video_resolution': '720'
        }
        options = build_options_from_data(data)
        assert options.video_format == 'mp4'
        assert options.audio_format == 'wav'
        assert options.video_resolution == '720'

    def test_build_options_with_referrer(self):
        """Test building options with referrer"""
        data = {
            'referrer': 'https://example.com'
        }
        options = build_options_from_data(data)
        assert options.referrer == 'https://example.com'

    def test_build_options_audio_only_flag(self):
        """Test that audio_only flag is properly set"""
        data = {}
        options = build_options_from_data(data, audio_only=True)
        assert options.audio_only is True

        options = build_options_from_data(data, audio_only=False)
        assert options.audio_only is False

    def test_build_options_all_fields(self):
        """Test building options with all fields"""
        data = {
            'video_format': 'mp4',
            'audio_format': 'm4a',
            'video_resolution': '1080',
            'force_overwrite': True,
            'embed_metadata': True,
            'embed_thumbnail': True,
            'apple_devices_compatible': True,
            'referrer': 'https://example.com',
            'verbose': True
        }
        options = build_options_from_data(data, audio_only=False)
        assert options.video_format == 'mp4'
        assert options.audio_format == 'm4a'
        assert options.video_resolution == '1080'
        assert options.force_overwrite is True
        assert options.embed_metadata is True
        assert options.embed_thumbnail is True
        assert options.apple_devices_compatible is True
        assert options.referrer == 'https://example.com'
        assert options.verbose is True
        assert options.audio_only is False


class TestBuildFormatFromOptions:
    """Test cases for build_format_from_options function"""

    def test_format_with_video_and_audio(self):
        """Test format string with both video and audio"""
        format_str = build_format_from_options('mp4', 'm4a', '1080')
        assert format_str == 'bestvideo[height<=1080]+bestaudio/best'

    def test_format_with_best_resolution(self):
        """Test format string with 'best' resolution"""
        format_str = build_format_from_options('mp4', 'm4a', 'best')
        assert format_str == 'bestvideo+bestaudio/best'
        assert '[height<=' not in format_str

    def test_format_with_video_only(self):
        """Test format string with only video"""
        format_str = build_format_from_options('mp4', None, '1080')
        assert format_str == 'bestvideo[height<=1080]/best'
        assert 'bestaudio' not in format_str

    def test_format_with_audio_only(self):
        """Test format string with only audio"""
        format_str = build_format_from_options(None, 'm4a', '1080')
        assert format_str == 'bestaudio/bestaudio'
        assert 'bestvideo' not in format_str

    def test_format_with_multiple_resolutions(self):
        """Test format string with various resolutions"""
        for resolution in ['240', '480', '720', '1440']:
            format_str = build_format_from_options('mp4', 'm4a', resolution)
            assert f'[height<={resolution}]' in format_str
            assert '+' in format_str

    def test_format_with_none_resolution(self):
        """Test format string with None resolution"""
        format_str = build_format_from_options('mp4', 'm4a', None)
        assert format_str == 'bestvideo+bestaudio/best'
        assert '[height<=' not in format_str

    def test_format_with_empty_formats(self):
        """Test format string with both formats as None causes IndexError"""
        # When no formats provided, format_parts will be empty and cause IndexError
        # This tests edge case handling
        with pytest.raises(IndexError):
            build_format_from_options(None, None, '1080')


class TestBuildCommand:
    """Test cases for build_command function"""

    def test_build_command_basic_video_audio(self):
        """Test building command with video and audio"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            video_resolution='1080'
        )
        command = build_command(url, options)
        assert command[0] == 'yt-dlp'
        assert '--format' in command
        assert url in command
        assert '-o' in command
        command_str = ' '.join(command)
        assert '%(title)s' in command_str
        assert '%(ext)s' in command_str
        # Should have merge format for non-audio-only
        assert '--merge-output-format' in command
        assert 'mp4' in command

    def test_build_command_audio_only(self):
        """Test building command with audio_only flag"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            audio_format='m4a',
            audio_only=True
        )
        command = build_command(url, options)
        assert '--extract-audio' in command
        assert '--audio-format' in command
        assert 'm4a' in command
        assert '--merge-output-format' not in command

    def test_build_command_with_referrer(self):
        """Test building command with referrer"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            referrer='https://example.com'
        )
        command = build_command(url, options)
        assert '--referer' in command
        assert 'https://example.com' in command
        referrer_idx = command.index('--referer')
        assert command[referrer_idx + 1] == 'https://example.com'

    def test_build_command_without_referrer(self):
        """Test building command without referrer"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            audio_format='m4a'
        )
        command = build_command(url, options)
        assert '--referer' not in command

    def test_build_command_force_overwrite(self):
        """Test building command with force overwrite"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            force_overwrite=True
        )
        command = build_command(url, options)
        assert '--force-overwrites' in command

    def test_build_command_without_force_overwrite(self):
        """Test building command without force overwrite"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            force_overwrite=False
        )
        command = build_command(url, options)
        assert '--force-overwrites' not in command

    def test_build_command_embed_metadata(self):
        """Test building command with embed metadata"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            embed_metadata=True
        )
        command = build_command(url, options)
        assert '--embed-metadata' in command

    def test_build_command_embed_thumbnail(self):
        """Test building command with embed thumbnail"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            embed_thumbnail=True
        )
        command = build_command(url, options)
        assert '--embed-thumbnail' in command

    def test_build_command_verbose(self):
        """Test building command with verbose flag"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            verbose=True
        )
        command = build_command(url, options)
        assert '--verbose' in command

    def test_build_command_apple_devices_compatible(self):
        """Test building command with apple devices compatible format"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            apple_devices_compatible=True
        )
        command = build_command(url, options)
        format_idx = command.index('--format')
        format_value = command[format_idx + 1]
        assert format_value == 'bv*[vcodec^=avc]+ba[ext=m4a]'

    def test_build_command_contains_url_at_end(self):
        """Test that command contains the URL at the end"""
        url = 'https://example.com/video'
        options = DownloadOptions(video_format='mp4')
        command = build_command(url, options)
        assert command[-1] == url

    def test_build_command_all_options(self):
        """Test building command with all options enabled"""
        url = 'https://example.com/video'
        options = DownloadOptions(
            video_format='mp4',
            audio_format='m4a',
            video_resolution='1080',
            force_overwrite=True,
            embed_metadata=True,
            embed_thumbnail=True,
            referrer='https://example.com',
            verbose=True,
            audio_only=False
        )
        command = build_command(url, options)
        assert '--force-overwrites' in command
        assert '--embed-metadata' in command
        assert '--embed-thumbnail' in command
        assert '--referer' in command
        assert '--verbose' in command
        assert '--merge-output-format' in command


class TestExecuteCommand:
    """Test cases for execute_command function"""

    @patch('services.download_service.subprocess.run')
    def test_execute_command_success(self, mock_run, flask_app):
        """Test executing command with successful result"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'Download completed'
        mock_result.stderr = ''
        mock_run.return_value = mock_result

        command = ['yt-dlp', '-f', 'best', 'https://example.com/video']
        response, status_code = execute_command(command)

        assert status_code == 200
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['status'] == 'success'
        assert 'Video downloaded successfully' in response_data['message']
        assert response_data['output'] == 'Download completed'

    @patch('services.download_service.subprocess.run')
    def test_execute_command_failure(self, mock_run, flask_app):
        """Test executing command with failure result"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ''
        mock_result.stderr = 'Video not found'
        mock_run.return_value = mock_result

        command = ['yt-dlp', '-f', 'best', 'https://example.com/video']
        response, status_code = execute_command(command)

        assert status_code == 400
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['status'] == 'error'
        assert 'Failed to download video' in response_data['message']
        assert 'Video not found' in response_data['details']

    @patch('services.download_service.subprocess.run')
    def test_execute_command_timeout(self, mock_run, flask_app):
        """Test executing command with timeout"""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired('yt-dlp', 3600)

        command = ['yt-dlp', '-f', 'best', 'https://example.com/video']
        response, status_code = execute_command(command)

        assert status_code == 408
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['status'] == 'error'
        assert 'timed out' in response_data['message'].lower()

    @patch('services.download_service.subprocess.run')
    def test_execute_command_exception(self, mock_run, flask_app):
        """Test executing command with general exception"""
        mock_run.side_effect = Exception('Command execution failed')

        command = ['yt-dlp', '-f', 'best', 'https://example.com/video']
        response, status_code = execute_command(command)

        assert status_code == 500
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['status'] == 'error'
        assert 'Command execution failed' in response_data['message']

    @patch('services.download_service.subprocess.run')
    def test_execute_command_calls_subprocess_with_correct_args(self, mock_run, flask_app):
        """Test that execute_command calls subprocess.run with correct arguments"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'Success'
        mock_result.stderr = ''
        mock_run.return_value = mock_result

        command = ['yt-dlp', '-f', 'best', 'https://example.com/video']
        execute_command(command)

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == command
        assert call_args[1]['capture_output'] is True
        assert call_args[1]['text'] is True
        assert call_args[1]['timeout'] == 3600

    @patch('services.download_service.subprocess.run')
    def test_execute_command_with_stderr_output(self, mock_run, flask_app):
        """Test executing command with stderr output on failure"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = 'Some output'
        mock_result.stderr = 'Critical error occurred'
        mock_run.return_value = mock_result

        command = ['yt-dlp', 'https://example.com/video']
        response, status_code = execute_command(command)

        assert status_code == 400
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['details'] == 'Critical error occurred'


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_full_workflow_with_valid_data(self, flask_app):
        """Test full workflow from options building to command building"""
        url = 'https://example.com/video'
        data = {
            'video_format': 'mp4',
            'audio_format': 'm4a',
            'video_resolution': '1080'
        }

        # Step 1: Build options
        options = build_options_from_data(data)
        assert options.video_format == 'mp4'
        assert options.audio_format == 'm4a'
        assert options.video_resolution == '1080'

        # Step 2: Build command
        command = build_command(url, options)
        assert 'yt-dlp' in command
        assert url in command

    def test_full_workflow_with_minimal_data(self, flask_app):
        """Test full workflow using minimal data with video format"""
        url = 'https://example.com/video'
        data = {'video_format': 'best'}

        options = build_options_from_data(data)
        assert isinstance(options, DownloadOptions)
        assert options.video_format == 'best'

        command = build_command(url, options)
        assert isinstance(command, list)
        assert len(command) > 0
        assert command[0] == 'yt-dlp'

    @patch('services.download_service.subprocess.run')
    def test_full_workflow_with_command_execution(self, mock_run, flask_app):
        """Test full workflow including command execution"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'Downloaded successfully'
        mock_result.stderr = ''
        mock_run.return_value = mock_result

        url = 'https://example.com/video'
        data = {
            'video_format': 'mp4',
            'audio_format': 'm4a'
        }

        options = build_options_from_data(data, audio_only=False)
        command = build_command(url, options)
        response, status_code = execute_command(command)

        assert status_code == 200
        response_data = response.json if isinstance(response.json, dict) else json.loads(response.json)
        assert response_data['status'] == 'success'

    def test_workflow_audio_only_download(self, flask_app):
        """Test workflow for audio-only download"""
        url = 'https://example.com/video'
        data = {'audio_format': 'm4a'}

        options = build_options_from_data(data, audio_only=True)
        assert options.audio_only is True
        assert options.audio_format == 'm4a'

        command = build_command(url, options)
        assert '--extract-audio' in command
        assert '--audio-format' in command
        assert url in command


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
