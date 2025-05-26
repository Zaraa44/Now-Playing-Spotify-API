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

  } catch (e) {
    console.error("Fout bij ophalen van gegevens:", e);
  }
}

fetchNowPlaying();
setInterval(fetchNowPlaying);

document.getElementById("fullscreen-btn").addEventListener("click", () => {
  const elem = document.documentElement;
  if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => {
      alert(`Fullscreen mislukt: ${err.message}`);
    });
  } else {
    document.exitFullscreen();
  }
});
