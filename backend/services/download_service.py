import subprocess
import os
from pathlib import Path
from flask import jsonify
from models.download_options import DownloadOptions as download_options


# Configure download directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'downloads')
Path(DOWNLOAD_DIR).mkdir(exist_ok=True)

default_timeout_seconds = 3600  # 1 hour
capture_command_output_flag = True

def build_options_from_data(data, audio_only=False):
    data['audio_only'] = audio_only
    return download_options.from_dict(data)

def build_format_from_options(video_format, audio_format, video_resolution):
    format_parts = []
    if video_format:
        video_format_part = 'bestvideo'
        if video_resolution and video_resolution != 'best':
            video_format_part += f'[height<={video_resolution}]'
        format_parts.append(video_format_part)
        
    if audio_format:
        format_parts.append(f'bestaudio')
    
    format = ''
    if len(format_parts) >= 2:
        format = '+'.join(format_parts)
    else:
        format = format_parts[0]

    return format + (f'/best' if video_format else '/bestaudio')

def build_command(url, options):
    format = build_format_from_options(options.video_format, options.audio_format, options.video_resolution) if not options.apple_devices_compatible else 'bv*[vcodec^=avc]+ba[ext=m4a]'
    
    command = [
        'yt-dlp',
        '--format', format,
    ]
    
    if options.audio_only:
        command.append('--extract-audio')
        command.append('--audio-format')
        command.append(options.audio_format)
    else:
        merge = 'mp4' # Only merge to mp4 for now
        command.append('--merge-output-format'),
        command.append(merge)

    command.append('-o')
    command.append(os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'))    

    if options.force_overwrite:
        command.append('--force-overwrites')
        
    if options.embed_metadata:
        command.append('--embed-metadata')
        
    if options.embed_thumbnail:
        command.append('--embed-thumbnail')
        
    if options.referrer is not None:
        command.append('--referer')
        command.append(options.referrer)
        
    if options.verbose:
        command.append('--verbose')
    
    command.append(url)
    
    return command

def execute_command(command):
    try:
        # Execute the command
        result = subprocess.run(
            command,
            capture_output=capture_command_output_flag,
            text=True,
            timeout=default_timeout_seconds
        )

        if result.returncode != 0:
            return jsonify({
                'status': 'error',
                'message': 'Failed to download video',
                'details': result.stderr
            }), 400

        return jsonify({
            'status': 'success',
            'message': 'Video downloaded successfully',
            'output': result.stdout
        }), 200

    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Download timed out (exceeded 5 minutes)'
        }), 408

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500