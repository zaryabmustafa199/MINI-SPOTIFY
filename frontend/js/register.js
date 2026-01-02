const registerForm = document.getElementById("registerForm");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch("http://127.0.0.1:8001/register", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registration successful! You can now log in.");
            window.location.href = "login.html";
        } else {
            message.textContent = data.detail;
        }
    } catch (err) {
        message.textContent = "Error connecting to backend";
    }
});
