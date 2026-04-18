function scrapeEmails() {
  const emails = [];

  // Gmail renders each email thread row in the inbox
  const rows = Array.from(document.querySelectorAll("tr.zA")).slice(0, 15);

  rows.forEach((row) => {
    const subjectEl = row.querySelector(".bog, .y6");
    const senderEl  = row.querySelector(".yX, .zF");
    const snippetEl = row.querySelector(".y2");

    if (subjectEl) {
      emails.push({
        subject: subjectEl.innerText.trim(),
        sender:  senderEl  ? senderEl.innerText.trim()  : "",
        snippet: snippetEl ? snippetEl.innerText.trim() : "",
        // build a readable email string for your pipeline
        text: `From: ${senderEl ? senderEl.innerText.trim() : "Unknown"}\nSubject: ${subjectEl.innerText.trim()}\n\n${snippetEl ? snippetEl.innerText.trim() : ""}`
      });
    }
  });

  return emails;
}

// listen for message from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "scrape") {
    const emails = scrapeEmails();
    sendResponse({ emails });
  }
});