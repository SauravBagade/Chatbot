// -------------------------------
// ⚙️ Config
// -------------------------------
const API = "http://127.0.0.1:8000/auth";

// -------------------------------
// 🔔 Show Alert
// -------------------------------
function showAlert(message, type = "danger") {
  const alertBox = document.getElementById("alertBox");
  if (!alertBox) return;

  alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
      ${message}
    </div>
  `;
}

// -------------------------------
// 🔐 LOGIN
// -------------------------------
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  // Validation
  if (!username || !password) {
    showAlert("Please enter username and password");
    return;
  }

  try {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok && data.access_token) {
      // Save token
      localStorage.setItem("token", data.access_token);

      showAlert("Login successful! Redirecting...", "success");

      setTimeout(() => {
        window.location.href = "index.html";
      }, 1000);

    } else {
      showAlert(data.detail || "Invalid login credentials");
    }

  } catch (err) {
    showAlert("Server error ❌");
  }
}

// -------------------------------
// 🆕 REGISTER
// -------------------------------
async function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmPassword").value.trim();

  // Validation
  if (!username || !password || !confirmPassword) {
    showAlert("Please fill all fields");
    return;
  }

  if (password.length < 6) {
    showAlert("Password must be at least 6 characters");
    return;
  }

  if (password !== confirmPassword) {
    showAlert("Passwords do not match");
    return;
  }

  try {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
      showAlert("Registration successful! Redirecting...", "success");

      setTimeout(() => {
        window.location.href = "login.html";
      }, 1500);

    } else {
      showAlert(data.detail || "Registration failed");
    }

  } catch (err) {
    showAlert("Server error ❌");
  }
}

// -------------------------------
// 🔓 LOGOUT (Reusable)
// -------------------------------
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

// -------------------------------
// 🔍 Check Auth (Optional Helper)
// -------------------------------
function requireAuth() {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "login.html";
  }
}
