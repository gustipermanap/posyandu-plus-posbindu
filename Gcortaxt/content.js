const downloadLinks = Array.from(document.querySelectorAll('a'))
  .filter(a => a.href.includes('.pdf') || a.href.includes('download'));

browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getLinks") {
    const urls = downloadLinks.map(link => link.href);
    sendResponse({ urls });
  }
});
