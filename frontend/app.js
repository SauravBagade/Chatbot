// -------------------------------
// ⚙️ Config
// -------------------------------
const API = "http://127.0.0.1:8000/api";
const token = localStorage.getItem("token");

// -------------------------------
// 🔐 Check Authentication
// -------------------------------
if (!token) {
  window.location.href = "login.html";
}

// -------------------------------
// 💬 Append Message to UI
// -------------------------------
function appendMessage(message, sender) {
  const chatBox = document.getElementById("chatBox");

  const div = document.createElement("div");
  div.classList.add("message", sender);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerText = message;

  div.appendChild(bubble);
  chatBox.appendChild(div);

  chatBox.scrollTop = chatBox.scrollHeight;
}

// -------------------------------
// ⏳ Show Typing Indicator
// -------------------------------
function showTyping() {
  const chatBox = document.getElementById("chatBox");

  const div = document.createElement("div");
  div.classList.add("message", "bot");
  div.id = "typing";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerText = "Typing...";

  div.appendChild(bubble);
  chatBox.appendChild(div);

  chatBox.scrollTop = chatBox.scrollHeight;
}

// -------------------------------
// ❌ Remove Typing Indicator
// -------------------------------
function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

// -------------------------------
// 🚀 Send Message
// -------------------------------
async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();

  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  showTyping();

  try {
    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ query: message })
    });

    const data = await res.json();

    removeTyping();

    if (res.ok) {
      appendMessage(data.response, "bot");
    } else {
      appendMessage(data.detail || "Error occurred", "bot");
    }

  } catch (err) {
    removeTyping();
    appendMessage("Server error ❌", "bot");
  }
}

// -------------------------------
// 📜 Load Chat History
// -------------------------------
async function loadHistory() {
  try {
    const res = await fetch(`${API}/history`, {
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    const data = await res.json();

    if (data.messages) {
      data.messages.forEach(msg => {
        appendMessage(
          msg.content,
          msg.role === "user" ? "user" : "bot"
        );
      });
    }

  } catch (err) {
    console.log("No history found");
  }
}

// -------------------------------
// 🔐 Logout
// -------------------------------
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

// -------------------------------
// ⌨️ Enter Key Support
// -------------------------------
document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// -------------------------------
// 🔄 Init App
// -------------------------------
loadHistory();
