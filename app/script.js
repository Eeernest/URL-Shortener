async function shortenUrl() {
  const longUrl = document.getElementById("js-long-url").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/shorten", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({long_url: longUrl})
    });

    if (!response.ok) {
      const error = await response.json();

      throw new Error(error.detail || "Unexpected error happened");
    }

    const data = await response.json();

    document.getElementById("js-shorten-result").innerText = `Short URL: ${data.short_url}`;
  } catch (exc) {
    document.getElementById("js-shorten-result").innerText = `Error: ${exc.message}`;
  }
}

async function showStats() {
  const shortUrl = document.getElementById("js-short-url").value;

  try {
    const response = await fetch(`http://127.0.0.1:8000/stats/${encodeURIComponent(shortUrl)}`, {
      method: "GET",
    });

    if (!response.ok) {
      const error = await response.json();

      throw new Error(error.detail || "Unexpected error happened");
    }

    const data = await response.json();

    document.getElementById("js-stats-result").innerText = `Clicks: ${data.click_count}`;
  } catch(exc) {
    document.getElementById("js-stats-result").innerText = `Error: ${exc.message}`;
  }
}