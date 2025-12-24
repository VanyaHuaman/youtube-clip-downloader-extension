# Quick Start Guide

## ✅ Step 1: Server is Running!

The download server is already running in the background. You should see:
```
🚀 YouTube Clip Downloader Server
🌐 Server running on http://localhost:5000
```

## 📌 Step 2: Load Extension in Chrome

1. **Open Chrome** and navigate to:
   ```
   chrome://extensions/
   ```

2. **Enable Developer Mode**
   - Look for the toggle switch in the top right corner
   - Click it to turn it ON

3. **Load the Extension**
   - Click the "Load unpacked" button (top left)
   - Navigate to and select this folder:
     ```
     /Users/vanyahuaman/youtube-clip-downloader-extension
     ```
   - Click "Select Folder"

4. **Verify Installation**
   - You should see "YouTube Clip Downloader" in your extensions list
   - Make sure it's enabled (toggle is ON)

## 🎬 Step 3: Test It!

1. **Go to a YouTube clip** (or create one):
   - Open any YouTube video
   - Click the "Clip" button under the video
   - Create a clip or use an existing one
   - You'll be on a URL like: `https://www.youtube.com/clip/Ugk...`

2. **Look for the Download Button**
   - A red "Download Clip" button should appear on the page
   - It may take a second to load

3. **Click to Download**
   - Click the "Download Clip" button
   - Wait for it to complete (button will show "Downloaded!")
   - Check your Downloads folder for the video file

## ⚠️ Important Notes

**Live Stream Clips:**
- If the clip is from a LIVE stream that's currently broadcasting, the download won't capture the correct timestamp
- Wait for the stream to end, then try again

**Troubleshooting:**
- If button doesn't appear: Refresh the page
- If download fails: Check the terminal where the server is running for errors
- If "server not running" error: Make sure you see the server message above

## 🛑 To Stop the Server

When you're done downloading clips, you can stop the server:
- The server is running in the background
- To stop it, just close the terminal or press Ctrl+C

## 🔄 To Restart the Server Later

Next time you want to use the extension:
```bash
cd /Users/vanyahuaman/youtube-clip-downloader-extension
./start_server.sh
```

---

**Need help?** Check the full README.md for detailed troubleshooting and advanced options.
