const summaryCards = document.getElementById("summary-cards");
const todayList = document.getElementById("today-list");
const eventGrid = document.getElementById("event-grid");
const taskList = document.getElementById("task-list");
const shoppingList = document.getElementById("shopping-list");
const expenseList = document.getElementById("expense-list");
const messageList = document.getElementById("message-list");
const roadmapList = document.getElementById("roadmap-list");

const CTA_DEMO = document.getElementById("cta-demo");
const CTA_BACKLOG = document.getElementById("cta-backlog");

const storageKey = "lifehub-state";

const initialState = {
  summary: [
    {
      title: "Geteilter Kalender",
      text: "Termine mit Benachrichtigungen, Konfliktcheck und Rollen (Verantwortlich/Info).",
    },
    {
      title: "Aufgaben & Chores",
      text: "Zuweisen, kommentieren, abhaken – sichtbar für alle Familienmitglieder.",
    },
    {
      title: "Einkaufslisten",
      text: "Echtzeit-Updates, Vorräte tracken und automatisch aus dem Essensplan befüllen.",
    },
    {
      title: "Haushaltsbuch",
      text: "Gemeinsame Ausgaben erfassen, Kategorien zuweisen und Ausgleich berechnen.",
    },
  ],
  quickActions: [
    { title: "17:00 Elternabend", meta: "Kalender • Teilnehmer: Alex, Sam" },
    { title: "Einkauf abschließen", meta: "Liste • 4 offene Positionen" },
    { title: "Haushaltsbudget aktualisieren", meta: "Finanzen • 2 neue Buchungen" },
    { title: "Müll rausstellen", meta: "Aufgabe • Erinnerung 21:00" },
  ],
  events: [
    { title: "Elternabend", date: "2024-09-20", time: "17:00", people: "Alex, Sam", type: "Familie" },
    { title: "Zahnarzt Mia", date: "2024-09-22", time: "09:30", people: "Mia", type: "Gesundheit" },
  ],
  tasks: [
    { title: "Wäsche falten", due: "2024-09-19", assignee: "Alex", priority: "mittel", done: false },
    { title: "Kitatasche packen", due: "2024-09-20", assignee: "Sam", priority: "hoch", done: false },
  ],
  shopping: [
    { item: "Hafermilch", quantity: 2, store: "Rewe", done: false },
    { item: "Pasta", quantity: 3, store: "Edeka", done: true },
  ],
  expenses: [
    { title: "Wocheneinkauf", amount: 86.4, payer: "Alex", category: "Haushalt" },
    { title: "Schwimmbad", amount: 22.0, payer: "Sam", category: "Freizeit" },
  ],
  messages: [
    { author: "Sam", text: "Bin mit Mia beim Sport, zurück 18:30.", pinned: true },
    { author: "Alex", text: "Einkauf erledigt – Milch und Obst im Kühlschrank.", pinned: false },
  ],
  roadmap: [
    { title: "PWA & Offline", status: "In Arbeit" },
    { title: "Push & E-Mail Alerts", status: "Geplant" },
    { title: "Persönliche vs. geteilte Views", status: "Geplant" },
    { title: "Automatischer Essensplan + Einkauf", status: "Entwurf" },
    { title: "Import aus CSV/Notizen", status: "Entwurf" },
    { title: "E2E für Chat & Dateien", status: "In Arbeit" },
  ],
};

function loadState() {
  const raw = localStorage.getItem(storageKey);
  if (!raw) return structuredClone(initialState);
  try {
    const parsed = JSON.parse(raw);
    return { ...structuredClone(initialState), ...parsed };
  } catch (err) {
    console.warn("State konnte nicht geladen werden, verwende Defaults", err);
    return structuredClone(initialState);
  }
}

let state = loadState();

function persist() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function renderSummary() {
  summaryCards.innerHTML = state.summary
    .map(
      (item) => `
      <article class="summary-card">
        <h3>${item.title}</h3>
        <p>${item.text}</p>
      </article>
    `
    )
    .join("");
}

function renderQuickActions() {
  todayList.innerHTML = state.quickActions
    .map(
      (item) => `
        <article class="feature-card">
          <h4>${item.title}</h4>
          <p class="muted">${item.meta}</p>
        </article>
      `
    )
    .join("");
}

function renderEvents() {
  const events = [...state.events].sort((a, b) => new Date(a.date) - new Date(b.date));
  eventGrid.innerHTML = events
    .map(
      (event, index) => `
        <article class="feature-card">
          <span class="badge">${event.type}</span>
          <h3>${event.title}</h3>
          <p class="muted">${formatDate(event.date)} · ${event.time} Uhr</p>
          <p class="muted">${event.people}</p>
          <button class="link" data-action="delete-event" data-index="${index}">Entfernen</button>
        </article>
      `
    )
    .join("");
}

function renderTasks() {
  const tasks = [...state.tasks].sort((a, b) => new Date(a.due) - new Date(b.due));
  taskList.innerHTML = tasks
    .map(
      (task, index) => `
        <li class="${task.done ? "is-done" : ""}">
          <div>
            <strong>${task.title}</strong>
            <small>Fällig ${formatDate(task.due)} • ${task.assignee} • Priorität: ${task.priority}</small>
          </div>
          <div class="actions">
            <button class="btn btn-ghost" data-action="toggle-task" data-index="${index}">${task.done ? "Reaktivieren" : "Erledigt"}</button>
            <button class="btn btn-ghost" data-action="delete-task" data-index="${index}">Löschen</button>
          </div>
        </li>
      `
    )
    .join("");
}

function renderShopping() {
  shoppingList.innerHTML = state.shopping
    .map(
      (entry, index) => `
        <li class="${entry.done ? "is-done" : ""}">
          <div>
            <strong>${entry.item}</strong>
            <small>${entry.quantity} × • ${entry.store}</small>
          </div>
          <div class="actions">
            <button class="btn btn-ghost" data-action="toggle-shopping" data-index="${index}">${entry.done ? "Rückgängig" : "Abgehakt"}</button>
            <button class="btn btn-ghost" data-action="delete-shopping" data-index="${index}">Löschen</button>
          </div>
        </li>
      `
    )
    .join("");
}

function renderExpenses() {
  const total = state.expenses.reduce((sum, e) => sum + Number(e.amount), 0);
  expenseList.innerHTML = `
    <li>
      <div>
        <strong>Aktueller Monat</strong>
        <small>Summe: €${total.toFixed(2)}</small>
      </div>
    </li>
  `;
  expenseList.innerHTML += state.expenses
    .map(
      (entry, index) => `
        <li>
          <div>
            <strong>${entry.title}</strong>
            <small>€${Number(entry.amount).toFixed(2)} • ${entry.category} • ${entry.payer}</small>
          </div>
          <button class="btn btn-ghost" data-action="delete-expense" data-index="${index}">Löschen</button>
        </li>
      `
    )
    .join("");
}

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

function renderRoadmap() {
  roadmapList.innerHTML = state.roadmap
    .map((item, index) => `
      <li>
        <div>
          <strong>${item.title}</strong>
          <small>Status: ${item.status}</small>
        </div>
        <button class="btn btn-ghost" data-action="roadmap-to-task" data-index="${index}">Als Task anlegen</button>
      </li>
    `)
    .join("");
}

function formatDate(date) {
  const d = new Date(date + "T00:00:00");
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "short", year: "numeric" });
}

function addEvent(event) {
  state.events.push(event);
  persist();
  renderEvents();
}

function addTask(task) {
  state.tasks.push(task);
  persist();
  renderTasks();
}

function addShopping(item) {
  state.shopping.push(item);
  persist();
  renderShopping();
}

function addExpense(expense) {
  state.expenses.push(expense);
  persist();
  renderExpenses();
}

function addMessage(message) {
  state.messages.push(message);
  persist();
  renderMessages();
}

function initForms() {
  document.getElementById("event-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addEvent({
      title: form.title.value,
      date: form.date.value,
      time: form.time.value,
      people: form.people.value,
      type: "Familie",
    });
    form.reset();
  });

  document.getElementById("task-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addTask({
      title: form.title.value,
      due: form.due.value,
      assignee: form.assignee.value,
      priority: form.priority.value,
      done: false,
    });
    form.reset();
  });

  document.getElementById("shopping-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addShopping({
      item: form.item.value,
      quantity: Number(form.quantity.value),
      store: form.store.value,
      done: false,
    });
    form.reset();
    form.quantity.value = 1;
  });

  document.getElementById("expense-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addExpense({
      title: form.title.value,
      amount: Number(form.amount.value),
      payer: form.payer.value,
      category: form.category.value,
    });
    form.reset();
  });

  document.getElementById("message-form").addEventListener("submit", (e) => {
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

function handleActions() {
  document.body.addEventListener("click", (event) => {
    const target = event.target;
    const action = target.dataset.action;
    if (!action) return;
    const index = Number(target.dataset.index);

    if (action === "delete-event") {
      state.events.splice(index, 1);
      persist();
      renderEvents();
    }

    if (action === "toggle-task") {
      state.tasks[index].done = !state.tasks[index].done;
      persist();
      renderTasks();
    }

    if (action === "delete-task") {
      state.tasks.splice(index, 1);
      persist();
      renderTasks();
    }

    if (action === "toggle-shopping") {
      state.shopping[index].done = !state.shopping[index].done;
      persist();
      renderShopping();
    }

    if (action === "delete-shopping") {
      state.shopping.splice(index, 1);
      persist();
      renderShopping();
    }

    if (action === "delete-expense") {
      state.expenses.splice(index, 1);
      persist();
      renderExpenses();
    }

    if (action === "toggle-pin") {
      const sorted = [...state.messages].sort((a, b) => Number(b.pinned) - Number(a.pinned));
      sorted[index].pinned = !sorted[index].pinned;
      state.messages = sorted;
      persist();
      renderMessages();
    }

    if (action === "delete-message") {
      const sorted = [...state.messages].sort((a, b) => Number(b.pinned) - Number(a.pinned));
      sorted.splice(index, 1);
      state.messages = sorted;
      persist();
      renderMessages();
    }

    if (action === "roadmap-to-task") {
      const item = state.roadmap[index];
      addTask({
        title: `Roadmap: ${item.title}`,
        due: new Date().toISOString().slice(0, 10),
        assignee: "Product", // placeholder
        priority: "mittel",
        done: false,
      });
    }
  });
}

function initCtas() {
  CTA_DEMO.addEventListener("click", () => {
    document.getElementById("calendar").scrollIntoView({ behavior: "smooth" });
  });
  CTA_BACKLOG.addEventListener("click", () => {
    document.getElementById("roadmap").scrollIntoView({ behavior: "smooth" });
  });
}

function init() {
  renderSummary();
  renderQuickActions();
  renderEvents();
  renderTasks();
  renderShopping();
  renderExpenses();
  renderMessages();
  renderRoadmap();
  initForms();
  handleActions();
  initCtas();
}

init();
