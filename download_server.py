#!/usr/bin/env python3
"""
Local download server for YouTube Clip Downloader extension
Receives download requests from the browser extension and uses yt-dlp to download clips
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Allow requests from browser extension

# Default download directory
DOWNLOAD_DIR = str(Path.home() / "Downloads")

@app.route('/health', methods=['GET'])
def health_check():
    """Check if server is running"""
    return jsonify({'status': 'ok', 'message': 'Download server is running'})

@app.route('/download', methods=['POST'])
def download_clip():
    """
    Download a YouTube clip
    Expects JSON: { "url": "https://youtube.com/clip/...", "title": "clip title" }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        title = data.get('title', 'youtube_clip')

        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'}), 400

        print(f"📥 Received download request: {url}")
        print(f"📁 Saving to: {DOWNLOAD_DIR}")

        # Build yt-dlp command
        # Use HLS format 301 for best quality (1080p60) - works better for clips than DASH
        cmd = [
            'yt-dlp',
            url,
            '-o', os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            '--restrict-filenames',
            '-f', '301/300/299+140/bestvideo+bestaudio/best',
            '--merge-output-format', 'mp4',
            '--no-playlist',
            '--print', 'after_move:filepath'  # Print the final file path
        ]

        # Run yt-dlp
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        # Extract filepath from output
        filepath = result.stdout.strip().split('\n')[-1] if result.stdout else None

        print(f"✅ Download complete: {filepath}")

        return jsonify({
            'success': True,
            'message': 'Download complete',
            'filepath': filepath
        })

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        print(f"❌ Download failed: {error_msg}")
        return jsonify({
            'success': False,
            'error': f'yt-dlp error: {error_msg}'
        }), 500

    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/check-clip', methods=['POST'])
def check_clip():
    """
    Check if a clip is from a live stream
    Returns metadata about the clip
    """
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'}), 400

        # Get metadata
        cmd = ['yt-dlp', '-j', url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        import json
        metadata = json.loads(result.stdout)

        is_live = metadata.get('is_live', False)
        live_status = metadata.get('live_status', '')
        section_start = metadata.get('section_start')

        return jsonify({
            'success': True,
            'is_live': is_live or live_status == 'is_live',
            'has_clip_section': section_start is not None,
            'section_start': section_start,
            'section_end': metadata.get('section_end'),
            'duration': metadata.get('duration'),
            'title': metadata.get('title')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    PORT = 5001  # Changed from 5000 due to AirPlay conflict on macOS
    print("🚀 YouTube Clip Downloader Server")
    print(f"📁 Download directory: {DOWNLOAD_DIR}")
    print(f"🌐 Server running on http://localhost:{PORT}")
    print("\nEndpoints:")
    print("  GET  /health       - Health check")
    print("  POST /download     - Download a clip")
    print("  POST /check-clip   - Check clip metadata")
    print("\nPress Ctrl+C to stop\n")

    app.run(host='localhost', port=PORT, debug=False)
