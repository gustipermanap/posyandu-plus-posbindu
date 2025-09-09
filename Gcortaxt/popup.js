document.getElementById('startDownload').addEventListener('click', () => {
  browser.tabs.query({ active: true, currentWindow: true }).then(tabs => {
    browser.tabs.sendMessage(tabs[0].id, { action: "getLinks" }).then(response => {
      browser.runtime.sendMessage({ action: "downloadFiles", urls: response.urls });
    });
  });
});
