#!/usr/bin/env python3
"""
Monitor a live stream and automatically download a clip when the stream ends
"""

import subprocess
import json
import time
import sys
from datetime import datetime
from pathlib import Path

DOWNLOAD_DIR = str(Path.home() / "Downloads")

def check_stream_status(video_url):
    """Check if a YouTube video is still live"""
    try:
        cmd = ['yt-dlp', '-j', video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)

        is_live = metadata.get('is_live', False)
        live_status = metadata.get('live_status', '')
        title = metadata.get('title', 'Unknown')

        return {
            'is_live': is_live or live_status == 'is_live',
            'live_status': live_status,
            'title': title
        }
    except Exception as e:
        print(f"Error checking stream status: {e}")
        return None

def download_clip(clip_url, output_dir=DOWNLOAD_DIR):
    """Download a YouTube clip"""
    try:
        print(f"\n📥 Starting download...")
        print(f"📁 Saving to: {output_dir}")

        # Use HLS format 301 for best quality (1080p60) - works better for clips than DASH
        cmd = [
            'yt-dlp',
            clip_url,
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            '--restrict-filenames',
            '-f', '301/300/299+140/bestvideo+bestaudio/best',
            '--merge-output-format', 'mp4',
            '--no-playlist'
        ]

        result = subprocess.run(cmd, check=True)
        print("\n✅ Download complete!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed: {e}")
        return False

def monitor_stream(video_url, clip_url, check_interval=60):
    """Monitor a stream and download clip when it ends"""

    print("🎬 YouTube Live Stream Monitor")
    print("=" * 60)
    print(f"Stream URL: {video_url}")
    print(f"Clip URL: {clip_url}")
    print(f"Check interval: {check_interval} seconds")
    print("=" * 60)

    # Initial check
    print("\n🔍 Checking stream status...")
    status = check_stream_status(video_url)

    if not status:
        print("❌ Could not check stream status. Exiting.")
        return False

    print(f"📺 Stream: {status['title']}")
    print(f"🔴 Status: {status['live_status']}")

    if not status['is_live']:
        print("\n✅ Stream is already offline! Downloading clip now...")
        return download_clip(clip_url)

    print(f"\n⏳ Stream is live. Monitoring every {check_interval} seconds...")
    print("   Press Ctrl+C to stop monitoring\n")

    check_count = 0

    try:
        while True:
            time.sleep(check_interval)
            check_count += 1

            timestamp = datetime.now().strftime("%H:%M:%S")
            status = check_stream_status(video_url)

            if not status:
                print(f"[{timestamp}] ⚠️  Check #{check_count}: Could not fetch status, retrying...")
                continue

            if status['is_live']:
                print(f"[{timestamp}] 🔴 Check #{check_count}: Still live, waiting...")
            else:
                print(f"\n[{timestamp}] ✅ Stream ended! Status: {status['live_status']}")
                print("\n🎉 Stream is now archived! Starting download...\n")

                # Wait a bit for YouTube to finish processing
                print("⏳ Waiting 30 seconds for YouTube to process the archive...")
                time.sleep(30)

                return download_clip(clip_url)

    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
        print(f"Total checks performed: {check_count}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 monitor_and_download.py <video_url> <clip_url> [check_interval]")
        print("\nExample:")
        print('  python3 monitor_and_download.py \\')
        print('    "https://www.youtube.com/watch?v=VIDEO_ID" \\')
        print('    "https://www.youtube.com/clip/CLIP_ID" \\')
        print('    60  # optional: check every 60 seconds (default)')
        sys.exit(1)

    video_url = sys.argv[1]
    clip_url = sys.argv[2]
    check_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    success = monitor_stream(video_url, clip_url, check_interval)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
