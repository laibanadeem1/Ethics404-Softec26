document.getElementById("sendBtn").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Scraping emails...";

  // get the active Gmail tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // ask content.js to scrape
  chrome.tabs.sendMessage(tab.id, { action: "scrape" }, async (response) => {
    if (!response || !response.emails.length) {
      status.textContent = "No emails found. Make sure Gmail is open.";
      return;
    }

    status.textContent = `Found ${response.emails.length} emails. Sending...`;

    // send to your Flask endpoint
    try {
      const res = await fetch("http://localhost:5050/receive", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ emails: response.emails.map(e => e.text) })
      });

      const data = await res.json();
      status.textContent = `✅ ${data.count} emails sent to ScanAhead!`;
    } catch (err) {
      status.textContent = "Could not reach ScanAhead app. Is it running?";
    }
  });
});