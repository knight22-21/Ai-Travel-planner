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

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) throw new Error("Network response was not ok");

    const data = await res.json();

    appendMessage("guide", data.response);
  } catch (error) {
    appendMessage("guide", "Sorry, something went wrong. Please try again.");
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

// Helper function to append message bubbles
function appendMessage(sender, text) {
  const chatBox = document.getElementById("chatBox");
  const messageElem = document.createElement("div");
  messageElem.classList.add("message", sender);
  messageElem.innerText = text;

  // Timestamp
  const timeElem = document.createElement("div");
  timeElem.classList.add("timestamp");
  const now = new Date();
  timeElem.innerText = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  messageElem.appendChild(timeElem);
  chatBox.appendChild(messageElem);

  // Scroll to bottom smoothly
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
}
