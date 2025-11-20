import { state, persistState } from "./state.js";

const messageList = document.getElementById("message-list");
const messageForm = document.getElementById("message-form");

function renderMessages() {
  const sorted = [...state.messages].sort((a, b) => Number(b.pinned) - Number(a.pinned));
  messageList.innerHTML = sorted
    .map(
      (message, index) => `
        <li class="${message.pinned ? "is-pinned" : ""}">
          <div>
            <strong>${message.author}</strong>
            <small>${message.pinned ? "Gepinnt" : "Neu"}</small>
            <p>${message.text}</p>
          </div>
          <div class="actions">
            <button class="btn btn-ghost" data-action="toggle-pin" data-index="${index}">${message.pinned ? "Lösen" : "Anpinnen"}</button>
            <button class="btn btn-ghost" data-action="delete-message" data-index="${index}">Löschen</button>
          </div>
        </li>
      `
    )
    .join("");
}

function addMessage(message) {
  state.messages.push(message);
  persistState();
  renderMessages();
}

function initMessageForm() {
  messageForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addMessage({
      author: form.author.value,
      text: form.text.value,
      pinned: form.pinned.checked,
    });
    form.reset();
  });
}

function initMessageActions() {
  messageList?.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-action]");
    if (!btn) return;
    const index = Number(btn.dataset.index);

    if (btn.dataset.action === "toggle-pin") {
      const sorted = [...state.messages].sort((a, b) => Number(b.pinned) - Number(a.pinned));
      sorted[index].pinned = !sorted[index].pinned;
      state.messages = sorted;
      persistState();
      renderMessages();
    }

    if (btn.dataset.action === "delete-message") {
      const sorted = [...state.messages].sort((a, b) => Number(b.pinned) - Number(a.pinned));
      sorted.splice(index, 1);
      state.messages = sorted;
      persistState();
      renderMessages();
    }
  });
}

export function setupMessages() {
  renderMessages();
  initMessageForm();
  initMessageActions();
}
