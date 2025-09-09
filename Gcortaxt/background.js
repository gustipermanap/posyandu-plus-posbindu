browser.runtime.onMessage.addListener((request) => {
  if (request.action === "downloadFiles") {
    request.urls.forEach((url, index) => {
      browser.downloads.download({
        url: url,
        filename: `coretax/file_${index + 1}.pdf`,
        conflictAction: "uniquify"
      });
    });
  }
});
