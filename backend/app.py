from flask import Flask, request, jsonify
import subprocess
import os
from pathlib import Path
from urllib.parse import urlparse
from services import download_service
from schemas.schemas import DownloadWithOptionsSchema, DownloadBestSchema, DownloadAudioWithOptionsSchema
from marshmallow import ValidationError

app = Flask(__name__)

def validate_request(schema):
    """Decorator to validate request JSON against a schema"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                json_data = request.get_json()
                if json_data is None:
                    return jsonify({
                        'status': 'error',
                        'message': 'Request body must be valid JSON'
                    }), 400

                # Validate and deserialize
                validated_data = schema.load(json_data)
                return f(validated_data, *args, **kwargs)

            except ValidationError as e:
                return jsonify({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': e.messages
                }), 400
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


def process_download(validated_data, audio_only=False):
    """Process the download with validated data"""
    try:
        options = download_service.build_options_from_data(validated_data, audio_only=audio_only)
        print("Download options:", options)
        command = download_service.build_command(validated_data['url'], options)
        print("Built command:", " ".join(command))
        return download_service.execute_command(command)

    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Download timed out (exceeded 1 hour)'
        }), 408

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Download With Options Endpoint
@app.route('/download', methods=['POST'])
@validate_request(DownloadWithOptionsSchema())
def download_with_options(validated_data):
    """
    Download the media from the provided URL with options.

    Expected JSON body:
    {
        "url": "https://example.com/video",
        "video_resolution": "1080", # default is "best",
        "video_format": "mp4",   # default is "mp4",
        "audio_format": "m4a"    # default is "best",
        "referrer": "https://example.com"
    }
    """
    return process_download(validated_data)

# Download Audio Only Endpoint
@app.route('/download-audio', methods=['POST'])
@validate_request(DownloadAudioWithOptionsSchema())
def download_audio(validated_data):
    """
    Download audio only from the provided URL.

    Expected JSON body:
    {
        "url": "https://example.com/audio"
    }
    """
    try:
        return process_download(validated_data, audio_only=True)

    except subprocess.TimeoutExpired:
        return jsonify({
            'status': 'error',
            'message': 'Download timed out (exceeded 1 hour)'
        }), 408

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'downstream video downloader backend',
        'version': '1.0.0'
    }), 200
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5021)
