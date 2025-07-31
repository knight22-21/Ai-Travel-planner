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

  // Add loading indicator
  const loaderId = "loading-" + Date.now();
  appendMessage("guide", "Typing...", loaderId, true);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) throw new Error("Network response was not ok");

    const data = await res.json();

    // Replace loader with actual response
    replaceMessage(loaderId, data.response);
  } catch (error) {
    replaceMessage(loaderId, "❌ Sorry, something went wrong. Please try again.");
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
   : text;


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

// Replace loader with actual response
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


// Intro message
window.onload = () => {
  appendMessage("guide", "👋 Hi! I’m your AI Travel Guide. Tell me your travel plans.");
};
