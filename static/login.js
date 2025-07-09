document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");

  loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const login = document.getElementById("login").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!login || !password) {
      alert("Please enter your email/phone and password.");
      return;
    }

    try {
      const res = await fetch("/login_password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login, password }),
      });

      const data = await res.json();
      if (data.status === "success") {
        alert("Login successful!");
        window.location.href = "/";
      } else {
        alert("Login failed: Invalid credentials.");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("An error occurred while logging in.");
    }
  });
});

