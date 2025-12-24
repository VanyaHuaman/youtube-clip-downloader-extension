#!/bin/bash
# Start the YouTube Clip Downloader server

cd "$(dirname "$0")"
source venv/bin/activate
python3 download_server.py
