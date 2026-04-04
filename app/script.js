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

      if (response.status == 429) {
        throw new Error("Too many requests! Please try again later.")
      }

      throw new Error(error.detail || "Error occured");
    }

    const data = await response.json();

    document.getElementById("js-shorten-result").innerText = `Short URL: ${data.short_url}`;
  }catch (exc) {
    document.getElementById("js-shorten-result").innerText = `Error: ${exc.message}`;
  }
}