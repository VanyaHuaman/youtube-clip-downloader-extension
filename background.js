// YouTube Clip Downloader - Background Script

const SERVER_URL = 'http://localhost:5001';

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'downloadClip') {
    handleDownload(request.clipInfo)
      .then(() => sendResponse({ success: true }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

async function handleDownload(clipInfo) {
  try {
    console.log('Sending download request to local server:', clipInfo.url);

    // First, check if server is running
    const healthCheck = await fetch(`${SERVER_URL}/health`).catch(() => null);

    if (!healthCheck || !healthCheck.ok) {
      throw new Error(
        'Download server not running. Please start the server:\n' +
        'python3 download_server.py'
      );
    }

    // Send download request to local server
    const response = await fetch(`${SERVER_URL}/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: clipInfo.url,
        title: clipInfo.title
      })
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Download failed');
    }

    console.log('Download completed:', result.filepath);
    return result;

  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
}
