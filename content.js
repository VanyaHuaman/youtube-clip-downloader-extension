// YouTube Clip Downloader - Content Script

(function() {
  'use strict';

  let downloadButton = null;

  // Check if we're on a clip page
  function isClipPage() {
    return window.location.href.includes('/clip/');
  }

  // Extract clip information from the page
  function getClipInfo() {
    const url = window.location.href;
    const clipMatch = url.match(/\/clip\/(Ugk[\w-]+)/);

    if (!clipMatch) return null;

    const clipId = clipMatch[1];
    const videoId = new URLSearchParams(window.location.search).get('v') ||
                    document.querySelector('meta[itemprop="videoId"]')?.content;

    // Try to get title from page
    const titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string') ||
                        document.querySelector('h1.title');
    const title = titleElement?.textContent?.trim() || 'youtube_clip';

    return {
      clipId,
      videoId,
      title,
      url
    };
  }

  // Create download button
  function createDownloadButton() {
    if (downloadButton) return;

    const clipInfo = getClipInfo();
    if (!clipInfo) return;

    downloadButton = document.createElement('button');
    downloadButton.id = 'clip-download-btn';
    downloadButton.className = 'clip-download-button';
    downloadButton.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      Download Clip
    `;

    downloadButton.addEventListener('click', async () => {
      await downloadClip(clipInfo);
    });

    // Insert button into the page
    insertButton();
  }

  // Insert button into YouTube's UI
  function insertButton() {
    if (!downloadButton) return;

    // Try multiple locations to insert the button
    const insertLocations = [
      // Below the video player
      () => document.querySelector('#below'),
      // In the actions menu
      () => document.querySelector('#menu-container'),
      // Fallback: top of page
      () => document.querySelector('#primary')
    ];

    for (const getLocation of insertLocations) {
      const location = getLocation();
      if (location && !document.getElementById('clip-download-btn')) {
        const container = document.createElement('div');
        container.className = 'clip-download-container';
        container.appendChild(downloadButton);
        location.insertBefore(container, location.firstChild);
        break;
      }
    }
  }

  // Download the clip using yt-dlp approach
  async function downloadClip(clipInfo) {
    downloadButton.disabled = true;
    downloadButton.innerHTML = `
      <svg class="spinner" width="20" height="20" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" opacity="0.25"/>
        <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="2" fill="none"/>
      </svg>
      Downloading...
    `;

    try {
      // Send message to background script to initiate download
      chrome.runtime.sendMessage({
        action: 'downloadClip',
        clipInfo: clipInfo
      }, (response) => {
        if (response && response.success) {
          downloadButton.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Downloaded!
          `;
          setTimeout(() => {
            downloadButton.disabled = false;
            downloadButton.innerHTML = `
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              Download Clip
            `;
          }, 2000);
        } else {
          throw new Error(response?.error || 'Download failed');
        }
      });
    } catch (error) {
      console.error('Download error:', error);
      downloadButton.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        Failed - Try Again
      `;
      downloadButton.disabled = false;
    }
  }

  // Initialize when page is ready
  function init() {
    if (isClipPage()) {
      // Wait a bit for YouTube to load its UI
      setTimeout(() => {
        createDownloadButton();
      }, 1000);
    }
  }

  // Watch for navigation changes (YouTube is a SPA)
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      downloadButton = null;
      init();
    }
  }).observe(document, { subtree: true, childList: true });

  // Initial load
  init();
})();
