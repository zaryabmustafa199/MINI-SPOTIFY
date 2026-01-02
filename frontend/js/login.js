const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch("http://127.0.0.1:8001/login", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Save user_id in localStorage to use for favorites / library
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("username", data.username);
            // Redirect to home page
            window.location.href = "index.html";
        } else {
            message.textContent = data.detail;
        }
    } catch (err) {
        message.textContent = "Error connecting to backend";
    }
});
