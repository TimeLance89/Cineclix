import { state } from "./state.js";
import { addTask } from "./tasks.js";

const roadmapList = document.getElementById("roadmap-list");

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

function initRoadmapActions() {
  roadmapList?.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-action='roadmap-to-task']");
    if (!btn) return;
    const item = state.roadmap[Number(btn.dataset.index)];
    addTask({
      title: `Roadmap: ${item.title}`,
      due: new Date().toISOString().slice(0, 10),
      assignee: "Product",
      priority: "mittel",
      done: false,
    });
  });
}

export function setupRoadmap() {
  renderRoadmap();
  initRoadmapActions();
}
