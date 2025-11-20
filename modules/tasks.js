import { state, persistState } from "./state.js";
import { formatDate } from "./utils.js";

const taskList = document.getElementById("task-list");
const taskFilters = document.getElementById("task-filters");
const taskForm = document.getElementById("task-form");

let activeTaskFilter = "all";

function renderTasks() {
  const tasks = [...state.tasks].sort((a, b) => new Date(a.due) - new Date(b.due));
  const filtered = tasks.filter((task) => {
    if (activeTaskFilter === "all") return true;
    if (activeTaskFilter === "done") return task.done;
    if (activeTaskFilter === "offen") return !task.done;
    return task.priority === activeTaskFilter;
  });

  if (!filtered.length) {
    taskList.innerHTML = `<li><div><strong>Keine Aufgaben</strong><small>Der Filter liefert keine Ergebnisse.</small></div></li>`;
    return;
  }

  taskList.innerHTML = filtered
    .map(
      (task) => {
        const index = state.tasks.indexOf(task);
        return `
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
      `;
      }
    )
    .join("");
}

export function addTask(task) {
  state.tasks.push(task);
  persistState();
  renderTasks();
}

function initTaskForm() {
  taskForm?.addEventListener("submit", (e) => {
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
}

function initTaskActions() {
  taskList?.addEventListener("click", (event) => {
    const actionBtn = event.target.closest("[data-action]");
    if (!actionBtn) return;
    const index = Number(actionBtn.dataset.index);

    if (actionBtn.dataset.action === "toggle-task") {
      state.tasks[index].done = !state.tasks[index].done;
      persistState();
      renderTasks();
    }

    if (actionBtn.dataset.action === "delete-task") {
      state.tasks.splice(index, 1);
      persistState();
      renderTasks();
    }
  });
}

function initTaskFilters() {
  taskFilters?.addEventListener("click", (event) => {
    const btn = event.target.closest(".chip-toggle");
    if (!btn) return;
    taskFilters.querySelectorAll(".chip-toggle").forEach((el) => el.classList.remove("is-active"));
    btn.classList.add("is-active");
    activeTaskFilter = btn.dataset.filter;
    renderTasks();
  });
}

export function setupTasks() {
  renderTasks();
  initTaskForm();
  initTaskActions();
  initTaskFilters();
}
