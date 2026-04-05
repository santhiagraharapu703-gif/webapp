document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");
    const loginForm = document.getElementById("loginForm");
    const loginButton = document.getElementById("loginButton");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                togglePassword.textContent = "Hide";
            } else {
                passwordInput.type = "password";
                togglePassword.textContent = "Show";
            }
        });
    }

    if (loginForm && loginButton) {
        loginForm.addEventListener("submit", function () {
            loginButton.classList.add("loading");
            loginButton.textContent = "Logging in...";
        });
    }
});