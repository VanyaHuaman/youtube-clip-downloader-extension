# YouTube Clip Downloader

Download YouTube clips in the highest quality (1080p60) with ease! Choose between a simple Python CLI tool or a Chrome browser extension.

## Features

- 🎬 Download YouTube clips and videos in highest quality (1080p 60fps)
- 🔄 Monitor live streams and auto-download clips when stream ends
- 🌐 Chrome extension for one-click downloads from YouTube
- 📦 Simple Python CLI tool for quick downloads
- ⚡ Automatic quality selection (HLS format for best results)

---

## Quick Start Guide

### Option 1: Python CLI Tool (Simplest!)

**Requirements:**
- Python 3.7+
- yt-dlp

**Installation:**

```bash
# Install yt-dlp
pip install yt-dlp
# OR using Homebrew on macOS
brew install yt-dlp
```

**Usage:**

```bash
# Download a clip (highest quality by default)
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID"

# Download to specific folder
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID" -o ~/Downloads

# Choose specific quality
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID" -q 720p

# See all options
python3 youtube_clip_downloader.py --help
```

---

### Option 2: Chrome Browser Extension

**Requirements:**
- Python 3.7+
- Chrome/Chromium browser
- yt-dlp, Flask, and flask-cors

**Installation:**

1. **Install dependencies:**

```bash
cd youtube-clip-downloader-extension

# Install yt-dlp
pip install yt-dlp
# OR
brew install yt-dlp

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Flask
pip install flask flask-cors
```

2. **Load Chrome Extension:**

- Open Chrome and go to `chrome://extensions/`
- Enable "Developer mode" (toggle in top-right)
- Click "Load unpacked"
- Select the `youtube-clip-downloader-extension` folder
- You should see "YouTube Clip Downloader" in your extensions list

**Usage:**

1. **Start the download server:**

```bash
cd youtube-clip-downloader-extension
./start_server.sh
```

You should see:
```
🚀 YouTube Clip Downloader Server
📁 Download directory: /Users/yourname/Downloads
🌐 Server running on http://localhost:5001
```

2. **Download clips:**

- Go to YouTube and open any clip URL (e.g., `https://youtube.com/clip/...`)
- Look for the red "Download Clip" button on the page
- Click it to start downloading
- Check your Downloads folder for the video file

3. **Stop the server when done:**

- Press `Ctrl+C` in the terminal

---

### Option 3: Monitor Live Streams

Download clips from live streams automatically when the stream ends.

**Usage:**

```bash
python3 monitor_and_download.py "VIDEO_URL" "CLIP_URL" [CHECK_INTERVAL]
```

**Example:**

```bash
# Monitor stream and download clip when it ends (check every 60 seconds)
python3 monitor_and_download.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  "https://www.youtube.com/clip/CLIP_ID" \
  60
```

The script will:
- Check if the stream is still live every 60 seconds
- Automatically download the clip when the stream ends
- Save to your Downloads folder in highest quality

---

## Quality Information

**Default Quality:**
- All tools default to the highest quality available (1080p 60fps)
- Uses HLS format 301 for best results with clips
- Automatically falls back to other high-quality formats if unavailable

**Format Priority:**
1. Format 301 - HLS 1080p 60fps (best for clips)
2. Format 300 - HLS 720p 60fps
3. Format 299+140 - DASH 1080p 60fps + audio
4. bestvideo+bestaudio - Best available
5. best - Fallback

**Typical file sizes (for a 54-second clip):**
- 1080p 60fps: ~8-21 MB
- 720p 60fps: ~5-10 MB
- 360p 30fps: ~2-3 MB

---

## Important Notes

### Live Stream Clips

If you create a clip from a **currently live stream**, the download may not work correctly because:
- YouTube doesn't make past segments of live streams available until the stream ends
- yt-dlp can only access the current live buffer

**Solution:**
- Use Option 3 (Monitor Live Streams) to automatically download when the stream ends
- Or wait for the live stream to end and be archived, then download the clip

### Troubleshooting

**"yt-dlp not found":**
```bash
pip install yt-dlp
# or
brew install yt-dlp
```

**"Download server not running" (Chrome Extension):**
- Make sure you've started the server: `./start_server.sh`
- Check that the server is running on port 5001
- Look for error messages in the terminal

**"Download button doesn't appear" (Chrome Extension):**
- Refresh the YouTube clip page
- Make sure the extension is enabled in `chrome://extensions/`
- Make sure you're on a clip URL (`/clip/` in the URL)

**"Port 5000 already in use":**
- The extension uses port 5001 (not 5000) to avoid conflicts with macOS AirPlay
- If port 5001 is also in use, edit both `download_server.py` and `background.js` to use a different port

**Download fails:**
- Check the terminal for error messages
- Make sure yt-dlp is installed: `yt-dlp --version`
- Try the Python CLI tool to see detailed error messages

---

## Project Structure

```
youtube-clip-downloader-extension/
├── README.md                    # This file
├── youtube_clip_downloader.py   # Python CLI tool
├── monitor_and_download.py      # Live stream monitor
├── download_server.py           # Flask server for extension
├── background.js                # Extension background script
├── content.js                   # Extension content script
├── styles.css                   # Extension button styles
├── manifest.json                # Chrome extension manifest
├── start_server.sh              # Server startup script
├── QUICK_START.md              # Quick reference guide
└── icon*.png                    # Extension icons
```

---

## Tips & Best Practices

1. **Best Quality:** All tools default to highest quality (1080p60), but you can override with `-q` flag in CLI
2. **Live Streams:** Use `monitor_and_download.py` to automatically download when stream ends
3. **Batch Downloads:** Use the CLI tool with a loop for multiple clips
4. **Server Management:** The download server runs locally and is only accessible from your browser
5. **File Names:** Files are automatically named based on the video title with special characters removed

---

## Privacy & Security

- All downloads happen locally on your computer
- No data is sent to external servers
- The extension only runs on YouTube.com pages
- Source code is fully visible and auditable

---

## License

Free to use and modify. Share with friends! 🎉

---

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download engine
- [Flask](https://flask.palletsprojects.com/) - Web server framework
- Chrome Extensions API
