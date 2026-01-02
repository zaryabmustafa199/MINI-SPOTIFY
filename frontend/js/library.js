document.addEventListener("DOMContentLoaded", async () => {
    const favoritesContainer = document.getElementById("favoritesContainer");
    const audioPlayer = document.getElementById("audioPlayer");
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        favoritesContainer.innerHTML = "<p>Please log in to see your library.</p>";
        return;
    }

    try {
        // Fetch favorite songs from backend
        const response = await fetch(`http://127.0.0.1:8001/favorites/${userId}`);
        const favorites = await response.json();

        if (favorites.length === 0) {
            favoritesContainer.innerHTML = "<p>No favorite songs yet.</p>";
            return;
        }

        favorites.forEach((song) => {
            const div = document.createElement("div");
            div.className = "song-item";
            div.innerHTML = `
        <p><strong>${song.title}</strong> - ${song.artist}</p>
        <button class="playBtn">Play</button>
        <button class="removeFavBtn">Remove</button>
      `;
            favoritesContainer.appendChild(div);

            // Play button
            div.querySelector(".playBtn").addEventListener("click", () => {
                audioPlayer.src = song.file_path;
                audioPlayer.play();
            });

            // Remove favorite button
            div.querySelector(".removeFavBtn").addEventListener("click", async () => {
                const formData = new FormData();
                formData.append("user_id", userId);
                formData.append("song_id", song.id);

                try {
                    const res = await fetch("http://127.0.0.1:8001/favorite", {
                        method: "DELETE",
                        body: formData,
                    });

                    const data = await res.json();
                    if (res.ok) {
                        alert("Removed from favorites");
                        div.remove(); // Remove from DOM
                    } else {
                        alert(data.detail);
                    }
                } catch (err) {
                    alert("Error connecting to backend");
                }
            });
        });
    } catch (err) {
        favoritesContainer.innerHTML = "<p>Error fetching favorites from backend.</p>";
    }
});
