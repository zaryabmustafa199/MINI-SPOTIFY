document.addEventListener("DOMContentLoaded", async () => {
    const playlistContainer = document.getElementById("playlistContainer");

    try {
        const response = await fetch("http://127.0.0.1:8001/playlists");
        const playlists = await response.json();

        playlists.forEach((playlist) => {
            const card = document.createElement("div");
            card.className = "playlist-card";

            // Fix image path - prepend backend URL if it's a relative path
            const imagePath = playlist.cover_image.startsWith('http')
                ? playlist.cover_image
                : `http://127.0.0.1:8001/${playlist.cover_image}`;

            card.innerHTML = `
        <a href="playlist.html?playlist_id=${playlist.id}">
          <img src="${imagePath}" alt="${playlist.name}">
          <p>${playlist.name}</p>
        </a>
      `;

            playlistContainer.appendChild(card);
        });
    } catch (err) {
        playlistContainer.innerHTML = "<p>Error fetching playlists from backend.</p>";
    }
});
