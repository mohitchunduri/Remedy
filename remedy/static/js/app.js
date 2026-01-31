const chatLog = document.getElementById("chat-log");
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chipRow = document.getElementById("chip-row");
const clearBtn = document.getElementById("clear-btn");
const completeBtn = document.getElementById("complete-btn");

const defaultChips = [
  "I have a sore throat and congestion.",
  "I am exhausted and low energy.",
  "I feel nauseous and my stomach is upset.",
  "My allergies are flaring up.",
];

const statusMessages = {
  empty: "Tell me what is going on and I will help.",
  "not-configured":
    "AI responses are not enabled yet. Add your API key to continue.",
  "not-implemented":
    "AI wiring is not set up yet. A backend developer can plug it in.",
};

function createMessage(role, text, stampText) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const stamp = document.createElement("span");
  stamp.className = "stamp";
  stamp.textContent = stampText || (role === "user" ? "You" : "Assistant");

  wrapper.appendChild(bubble);
  wrapper.appendChild(stamp);
  return wrapper;
}

function appendMessage(role, text, stampText) {
  const message = createMessage(role, text, stampText);
  chatLog.appendChild(message);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function appendTyping() {
  const wrapper = document.createElement("div");
  wrapper.className = "message assistant";
  wrapper.dataset.typing = "true";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = "Typing...";

  wrapper.appendChild(bubble);
  chatLog.appendChild(wrapper);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function removeTyping() {
  const typing = chatLog.querySelector("[data-typing='true']");
  if (typing) typing.remove();
}

function setSuggestions(list) {
  chipRow.innerHTML = "";
  if (!list || !list.length) return;
  list.forEach((item) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.type = "button";
    chip.dataset.text = item;
    chip.textContent = item;
    chipRow.appendChild(chip);
  });
}

async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  appendMessage("user", trimmed, "You");
  messageInput.value = "";
  appendTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: trimmed }),
    });
    const data = await response.json();
    removeTyping();
    if (data.reply) {
      appendMessage("assistant", data.reply, "Remedy");
    }

    if (data.status === "completed") {
      appendMessage("system", "Session cleared. You can start again anytime.", "System");
    }

    if (!data.reply && data.status && statusMessages[data.status]) {
      appendMessage("assistant", statusMessages[data.status], "Remedy");
    }

    if (data.suggestions) {
      setSuggestions(data.suggestions);
    }
  } catch (error) {
    removeTyping();
    appendMessage(
      "assistant",
      "I hit a small snag. Try that again when you are ready.",
      "Remedy"
    );
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInput.value);
});

chipRow.addEventListener("click", (event) => {
  const target = event.target;
  if (target.matches("button[data-text]")) {
    sendMessage(target.dataset.text);
  }
});

clearBtn.addEventListener("click", () => {
  chatLog.innerHTML = "";
  const welcome = window.REMEDY_WELCOME || "Hi, I am Remedy. Tell me what you are feeling.";
  appendMessage("assistant", welcome, "Remedy");
  setSuggestions(defaultChips);
});

completeBtn.addEventListener("click", () => {
  sendMessage("COMPLETED");
});
