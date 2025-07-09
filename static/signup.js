const API_BASE_URL = "http://35.200.236.188:5000"; // Use your backend IP/domain

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signupForm");
  const sendOtpBtn = document.getElementById("sendOtpBtn");
  const otpInput = document.querySelector("input[name='otp']");

  // 🔹 Send OTP to Mobile
  sendOtpBtn?.addEventListener("click", async () => {
    const code = document.querySelector("select[name='country_code']").value;
    const number = document.querySelector("input[name='mobile']").value;
    const fullMobile = code + number;

    if (!number || !/^\d{7,15}$/.test(number)) {
      return alert("Please enter a valid mobile number.");
    }

    try {
      const res = await fetch(`${API_BASE_URL}/send_otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: fullMobile }),
      });

      const data = await res.json();
      alert(data.message || "OTP Sent!");

      if (otpInput) {
        otpInput.style.display = "block";
      }
    } catch (err) {
      console.error("OTP Send Error:", err);
      alert("Failed to send OTP. Check console or server.");
    }
  });

  // 🔹 Handle Signup Form Submit
  signupForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(signupForm);
    const data = Object.fromEntries(formData.entries());

    // Combine full mobile number
    if (data.country_code && data.mobile) {
      data.mobile = data.country_code + data.mobile;
    }
    delete data.country_code;

    // Validate password match
    if (!data.password || data.password !== data.confirm_password) {
      return alert("Passwords do not match.");
    }
    delete data.confirm_password;

    try {
      const res = await fetch(`${API_BASE_URL}/verify_signup_otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      if (result.status === "success") {
        alert("Signup successful!");
        window.location.href = "/login";
      } else {
        alert("Signup failed: Invalid OTP or user data.");
      }
    } catch (err) {
      console.error("Signup Error:", err);
      alert("Signup failed. Please check your inputs.");
    }
  });
});

