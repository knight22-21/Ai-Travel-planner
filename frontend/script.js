let chatHistory = []; // Track messages for PDF

async function sendMessage() {
  const input = document.getElementById("userMessage");
  const sendBtn = document.getElementById("sendBtn");
  const chatBox = document.getElementById("chatBox");

  const message = input.value.trim();
  if (!message) return;

  // Disable input & button while processing
  input.disabled = true;
  sendBtn.disabled = true;
  input.value = "";

  // Add user message with timestamp
  appendMessage("user", message);
  chatHistory.push({ role: "user", content: message });

  // Add loading indicator
  const loaderId = "loading-" + Date.now();
  appendMessage("guide", "Typing...", loaderId, true);

  try {
    const res = await fetch("/api/v1/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) throw new Error("Network response was not ok");

    const data = await res.json();

    // Replace loader with actual response
    replaceMessage(loaderId, data.response);
    chatHistory.push({ role: "guide", content: data.response });

  } catch (error) {
    const errorMsg = "❌ Sorry, something went wrong. Please try again.";
    replaceMessage(loaderId, errorMsg);
    chatHistory.push({ role: "guide", content: errorMsg });
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

function appendMessage(sender, text, id = null, isLoading = false) {
  const chatBox = document.getElementById("chatBox");
  const messageElem = document.createElement("div");
  messageElem.classList.add("message", sender);
  if (id) messageElem.id = id;

  // Show loading animation if applicable
  messageElem.innerHTML = isLoading
    ? `<div class="dots"><span>.</span><span>.</span><span>.</span></div>`
    : marked.parse(text); // Markdown support

  // Timestamp
  if (!isLoading) {
    const timeElem = document.createElement("div");
    timeElem.classList.add("timestamp");
    const now = new Date();
    timeElem.innerText = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    messageElem.appendChild(timeElem);
  }

  chatBox.appendChild(messageElem);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}

function replaceMessage(id, newText) {
  const messageElem = document.getElementById(id);
  if (messageElem) {
    // Convert Markdown to HTML
    const html = marked.parse(newText);
    messageElem.innerHTML = html;

    // Add timestamp
    const timeElem = document.createElement("div");
    timeElem.classList.add("timestamp");
    const now = new Date();
    timeElem.innerText = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    messageElem.appendChild(timeElem);
  }
}

// Handle PDF download
document.getElementById("downloadBtn").addEventListener("click", async () => {
  if (chatHistory.length === 0) {
    alert("No chat history to download.");
    return;
  }

  try {
    const response = await fetch("/api/v1/pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ history: chatHistory })
    });

    if (!response.ok) throw new Error("Failed to download PDF");

    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "chat_history.pdf";
    link.click();
  } catch (err) {
    console.error("PDF download failed:", err);
    alert("Failed to generate PDF. Please try again.");
  }
});

// Intro message
window.onload = () => {
  appendMessage("guide", "👋 Hi! I’m your AI Travel Guide. Tell me your travel plans.");
  chatHistory.push({ role: "guide", content: "👋 Hi! I’m your AI Travel Guide. Tell me your travel plans." });
};
