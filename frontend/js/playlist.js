document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const playlistId = urlParams.get("playlist_id");
    const songContainer = document.getElementById("songContainer");
    const playlistName = document.getElementById("playlistName");
    const audioPlayer = document.getElementById("audioPlayer");
    const userId = localStorage.getItem("user_id"); // Logged in user

    if (!playlistId) {
        songContainer.innerHTML = "<p>No playlist selected.</p>";
        return;
    }

    try {
        // Fetch songs from backend
        const response = await fetch(`http://127.0.0.1:8001/playlist/${playlistId}`);
        const songs = await response.json();

        if (songs.length === 0) {
            songContainer.innerHTML = "<p>No songs in this playlist.</p>";
            return;
        }

        // Optionally set playlist name to first song's playlist name (if backend provides it)
        playlistName.textContent = `Playlist ${playlistId}`;

        songs.forEach((song) => {
            const div = document.createElement("div");
            div.className = "song-item";
            div.innerHTML = `
        <p><strong>${song.title}</strong> - ${song.artist}</p>
        <button class="playBtn">Play</button>
        <button class="favBtn">❤</button>
      `;
            songContainer.appendChild(div);

            // Play button
            div.querySelector(".playBtn").addEventListener("click", () => {
                audioPlayer.src = song.file_path; // file path from backend
                audioPlayer.play();
            });

            // Favorite button
            div.querySelector(".favBtn").addEventListener("click", async () => {
                if (!userId) {
                    alert("Please log in to add favorites");
                    return;
                }

                const formData = new FormData();
                formData.append("user_id", userId);
                formData.append("song_id", song.id);

                try {
                    const res = await fetch("http://127.0.0.1:8001/favorite", {
                        method: "POST",
                        body: formData,
                    });

                    const data = await res.json();
                    if (res.ok) {
                        alert("Added to favorites!");
                    } else {
                        alert(data.detail);
                    }
                } catch (err) {
                    alert("Error connecting to backend");
                }
            });
        });
    } catch (err) {
        songContainer.innerHTML = "<p>Error fetching songs from backend.</p>";
    }
});
