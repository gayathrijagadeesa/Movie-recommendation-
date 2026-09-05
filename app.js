const input = document.getElementById("titleInput");
const btn = document.getElementById("searchBtn");
const status = document.getElementById("status");
const resultsEl = document.getElementById("results");

async function getRecommendations() {
  const title = input.value.trim();
  resultsEl.innerHTML = "";
  status.className = "";

  if (!title) {
    status.textContent = "Type a movie title to get started.";
    return;
  }

  status.textContent = "Finding similar movies...";

  try {
    const res = await fetch(`/recommend?title=${encodeURIComponent(title)}`);
    const data = await res.json();

    if (!res.ok) {
      status.className = "error";
      status.textContent = data.error || "Something went wrong.";
      return;
    }

    status.textContent = `Because you liked "${data.query}":`;

    data.results.forEach((movie, i) => {
      const card = document.createElement("div");
      card.className = "result-card";
      card.style.animationDelay = `${i * 60}ms`;
      card.innerHTML = `
        <h3>${movie.title}</h3>
        <p class="genres">${movie.genres}</p>
        <p class="overview">${movie.overview}</p>
        <p class="score">match score: ${movie.score}</p>
      `;
      resultsEl.appendChild(card);
    });
  } catch (err) {
    status.className = "error";
    status.textContent = "Could not reach the recommender service.";
  }
}

btn.addEventListener("click", getRecommendations);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") getRecommendations();
});
