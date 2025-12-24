# YouTube Clip Downloader - Chrome Extension

Download YouTube clips directly from your browser with a single click! Includes a bonus live stream monitoring tool.

## Features

- 🌐 Chrome extension for one-click clip downloads from YouTube
- 🎬 Automatic highest quality downloads (1080p 60fps)
- 🔄 Monitor live streams and auto-download clips when stream ends
- ⚡ Smart format selection (HLS format for best results)
- 📦 Local Flask server handles all downloads

---

## Installation & Setup

### Step 1: Install Dependencies

**Requirements:**
- Python 3.7+
- Chrome/Chromium browser
- yt-dlp, Flask, and flask-cors

**Install dependencies:**

```bash
cd youtube-clip-downloader-extension

# Install yt-dlp (use pip3 to ensure Python 3)
pip3 install yt-dlp
# OR
brew install yt-dlp

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Flask (pip works inside venv, or use pip3)
pip install flask flask-cors
```

### Step 2: Load Chrome Extension

- Open Chrome and go to `chrome://extensions/`
- Enable "Developer mode" (toggle in top-right)
- Click "Load unpacked"
- Select the `youtube-clip-downloader-extension` folder
- You should see "YouTube Clip Downloader" in your extensions list

---

## Usage

### Using the Chrome Extension

**1. Start the download server:**

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

**2. Download clips:**

- Go to YouTube and open any clip URL (e.g., `https://youtube.com/clip/...`)
- Look for the red "Download Clip" button on the page
- Click it to start downloading
- Check your Downloads folder for the video file

**3. Stop the server when done:**

- Press `Ctrl+C` in the terminal

---

### Monitor Live Streams (Bonus Tool)

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
pip3 install yt-dlp
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
├── QUICK_START.md              # Quick reference guide
├── manifest.json                # Chrome extension manifest
├── background.js                # Extension background script
├── content.js                   # Extension content script
├── styles.css                   # Extension button styles
├── icon*.png                    # Extension icons
├── download_server.py           # Flask server for extension
├── monitor_and_download.py      # Live stream monitor script
├── start_server.sh              # Server startup script
└── requirements.txt             # Python dependencies
```

---

## Tips & Best Practices

1. **Best Quality:** All downloads default to highest quality (1080p60) automatically
2. **Live Streams:** Use `monitor_and_download.py` to automatically download when stream ends
3. **Server Management:** The download server runs locally and is only accessible from your browser
4. **File Names:** Files are automatically named based on the video title with special characters removed
5. **Extension Reload:** If you update the extension files, reload it in `chrome://extensions/`

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

## Related Projects

Looking for a simple CLI tool instead? Check out [YouTube Clip Downloader CLI](https://github.com/VanyaHuaman/youtube-clip-downloader)

---

## Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download engine
- [Flask](https://flask.palletsprojects.com/) - Web server framework
- Chrome Extensions API
