import { state } from "./state.js";

const summaryCards = document.getElementById("summary-cards");
const todayList = document.getElementById("today-list");

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

export function setupDashboard() {
  renderSummary();
  renderQuickActions();
}
