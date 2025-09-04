let isPlaying = false;

function msToTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

async function fetchNowPlaying() {
  try {
    const res = await fetch("/current");
    const data = await res.json();

    if (data.error || !data.name) {
      document.getElementById("track-name").textContent = "Geen muziek afgespeeld";
      isPlaying = false;
      updatePlayButton();
      return;
    }

    document.getElementById("track-name").textContent = data.name;
    document.getElementById("artist-name").textContent = data.artists;
    document.getElementById("album-art").src = data.album_image;

    const progress = (data.progress_ms / data.duration_ms) * 100;
    document.getElementById("progress").style.width = progress + "%";

    document.getElementById("track-duration").textContent = msToTime(data.duration_ms);
    document.getElementById("track-position").textContent = msToTime(data.progress_ms);
    document.getElementById("track-popularity").textContent = data.popularity;
    document.getElementById("album-name").textContent = data.album;
    document.getElementById("playlist-name").textContent = data.playlist || "Onbekend";


    isPlaying = data.is_playing ?? false;
    updatePlayButton();

  } catch (e) {
    console.error("Fout bij ophalen van gegevens:", e);
  }
}


async function apiCall(endpoint, method = "POST") {
  try {
    await fetch(`https://api.spotify.com/v1/me/player/${endpoint}`, {
      method,
      headers: {
        "Authorization": `Bearer ${SPOTIFY_TOKEN}`,
        "Content-Type": "application/json",
      },
    });
  } catch (err) {
    console.error("Spotify API fout:", err);
  }
}


document.getElementById("play-btn").addEventListener("click", async () => {
  if (isPlaying) {
    await apiCall("pause", "PUT");
    isPlaying = false;
  } else {
    await apiCall("play", "PUT");
    isPlaying = true;
  }
  updatePlayButton();
});

document.getElementById("next-btn").addEventListener("click", () => apiCall("next"));
document.getElementById("prev-btn").addEventListener("click", () => apiCall("previous"));


function updatePlayButton() {
  const btn = document.getElementById("play-btn");
  btn.textContent = isPlaying ? "⏸" : "▶";
}


document.getElementById("fullscreen-btn").addEventListener("click", () => {
  const elem = document.documentElement;
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => alert(`Fullscreen mislukt: ${err.message}`));
  } else {
    document.exitFullscreen();
  }
});


fetchNowPlaying();
setInterval(fetchNowPlaying, 1000);
