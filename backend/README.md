# Downstream Backend

An open-source server application that exposes a REST API for downloading videos and audio from various sources. The backend leverages [yt-dlp](https://github.com/yt-dlp/yt-dlp) to handle downloads from YouTube, Twitch, TikTok, and many other platforms.

## Overview

This backend service provides a simple yet powerful API that allows you to:
- Download videos and audio from multiple sources
- Customize video resolution and audio format
- Extract metadata and embed thumbnails
- Convert audio to various formats (only to `mp3` and `m4a` for the moment)
- Support for Apple device compatibility

The application is built with Flask and provides a clean REST API for easy integration with frontend applications or other services.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation & Setup

1. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **System dependencies:**
   - **yt-dlp:**
   ```bash
   pip install yt-dlp
   ```

   - **FFmpeg:**
   ```
   TODO: Add FFmpeg installation instructions for different operating systems
   ```

### Running the Application

Start the development server:
```bash
python3 app.py
```

The server will be available at `http://localhost:5021`

**For testing with verbose output:**
```bash
python3 app.py --debug
```

## API Endpoints

### POST /download
Download the best quality video from a provided URL.

**Request:**
```json
{
  "url": "https://www.example.com/?vid=VIDEO_ID"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "downstream-backend-service"
}
```

## Usage Example

```bash
curl -X POST http://localhost:5021/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/?vid=VIDEO_ID"}'
```

## Downloaded Files

Videos are saved to the `downloads/` directory with their original titles.

## Testing

Run the test suite:
```bash
bash run_tests.sh
```

This will run all tests with coverage reporting for services and models.

## Project Structure

```
backend/
├── app.py                      # Flask application entry point
├── services/
│   └── download_service.py    # Core download logic
├── models/
│   └── download_options.py    # Download configuration dataclass
├── tests/
│   ├── download_service_tests.py    # Service tests
│   └── download_options_tests.py     # Model tests
├── downloads/                  # Directory for downloaded files
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Roadmap

Planned features for future releases:

### Short/Mid Term
- [ ] **Asynchronous Downloads** - Implement async download processing
- [ ] **Download Queue Management** - API endpoints to queue multiple downloads and manage them (pause, resume, cancel)
- [ ] **Processing Status Streaming** - Endpoint to stream real-time download progress and status updates
- [ ] **Download History & Persistence** - Store download history with metadata in a database
- [ ] **Playlist Download** - Support for playlist downloads
- [ ] **Format Presets** - Pre-configured download profiles for common use cases (audio only, HD video, etc.)
- [ ] **Docker Container** - Spin the app in a Docker container

### Long Term
- [ ] **User Authentication & Authorization** - API key-based authentication and rate limiting

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support the Project

If you find this project useful and would like to support its development, consider making a donation:

- **Cryptocurrency:**
  - Bitcoin: `bc1qsvksuytupcfvn5k667h9v4dwe4wsz2ugh8e6ap`
- **Buy Me a Coffee:** [Support on Buy Me a Coffee](buymeacoffee.com/maroulabs)

Your support helps keep this project alive and enables continued development of new features and improvements.

## License

This project is open-source. LICENSE file is work in progress.