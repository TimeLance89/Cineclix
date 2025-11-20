import { state, persistState } from "./state.js";
import { formatDate } from "./utils.js";

const eventGrid = document.getElementById("event-grid");
const calendarGrid = document.getElementById("calendar-grid");
const calendarMonthLabel = document.getElementById("calendar-month");
const calendarMeta = document.getElementById("calendar-meta");
const dayLabel = document.getElementById("day-label");
const dayEvents = document.getElementById("day-events");
const calendarSummary = document.getElementById("calendar-summary");
const eventForm = document.getElementById("event-form");
const prevMonthButton = document.getElementById("prev-month");
const nextMonthButton = document.getElementById("next-month");

let currentMonth = new Date();
let selectedDate = null;

function getEventsForDate(dateStr) {
  return state.events.filter((event) => event.date === dateStr);
}

function renderDayDetail(dateStr) {
  const events = getEventsForDate(dateStr).sort((a, b) => a.time.localeCompare(b.time));
  dayLabel.textContent = `${formatDate(dateStr)} (${events.length || "keine"} Termine)`;
  if (!events.length) {
    dayEvents.innerHTML = `<p class="muted">Noch keine Einträge – füge oben einen Termin hinzu.</p>`;
    return;
  }
  dayEvents.innerHTML = events
    .map(
      (event) => `
        <article class="mini-card">
          <div>
            <span class="badge">${event.type}</span>
            <h4>${event.title}</h4>
            <p class="muted">${event.time} Uhr • ${event.people}</p>
          </div>
        </article>
      `
    )
    .join("");
}

function renderCalendarSummary(monthEvents) {
  const byType = monthEvents.reduce((acc, event) => {
    acc[event.type] = (acc[event.type] || 0) + 1;
    return acc;
  }, {});
  const conflictPairs = monthEvents.filter((event, idx) =>
    monthEvents.some((other, j) => j !== idx && other.date === event.date && other.time === event.time)
  );

  const typeSummary = Object.entries(byType)
    .map(([type, count]) => `<div class="stat-pill"><strong>${count}</strong><span>${type}</span></div>`)
    .join("");

  calendarSummary.innerHTML = `
    <div class="stat-row">
      <div>
        <p class="eyebrow">Monatliche Verteilung</p>
        <div class="stat-pills">${typeSummary || "<span class='muted'>Noch keine Kategorien</span>"}</div>
      </div>
      <div>
        <p class="eyebrow">Konfliktcheck</p>
        <p class="muted">${conflictPairs.length ? `${conflictPairs.length} Termin(e) kollidieren – bitte prüfen.` : "Keine Überschneidungen"}</p>
      </div>
    </div>
  `;
}

function renderCalendar() {
  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const start = new Date(year, month, 1);
  const end = new Date(year, month + 1, 0);
  const offset = (start.getDay() + 6) % 7; // Montag als Start
  const totalDays = end.getDate();

  const monthEvents = state.events.filter((event) => {
    const d = new Date(`${event.date}T00:00:00`);
    return d.getMonth() === month && d.getFullYear() === year;
  });

  calendarMonthLabel.textContent = start.toLocaleDateString("de-DE", { month: "long", year: "numeric" });
  calendarMeta.textContent = `${monthEvents.length} Termin${monthEvents.length === 1 ? "" : "e"} im Monat`;

  const weekdays = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
  const cells = weekdays
    .map((weekday) => `<div class="weekday">${weekday}</div>`)
    .concat(Array.from({ length: offset }).map(() => `<div class="day empty"></div>`))
    .concat(
      Array.from({ length: totalDays }).map((_, idx) => {
        const day = idx + 1;
        const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        const eventsForDay = getEventsForDate(dateStr);
        const isToday = dateStr === new Date().toISOString().slice(0, 10);
        const isSelected = selectedDate === dateStr;
        return `
          <button class="day ${isToday ? "is-today" : ""} ${eventsForDay.length ? "has-events" : ""} ${isSelected ? "is-selected" : ""}" data-date="${dateStr}">
            <span class="day__number">${day}</span>
            ${eventsForDay
              .map((ev) => `<span class="day__pill" title="${ev.title}">${ev.time}</span>`)
              .slice(0, 2)
              .join("")}
            ${eventsForDay.length > 2 ? `<span class="day__more">+${eventsForDay.length - 2}</span>` : ""}
          </button>
        `;
      })
    );

  calendarGrid.innerHTML = cells.join("");

  const today = new Date().toISOString().slice(0, 10);
  if (!selectedDate || selectedDate.slice(0, 7) !== `${year}-${String(month + 1).padStart(2, "0")}`) {
    selectedDate = today.slice(0, 7) === `${year}-${String(month + 1).padStart(2, "0")}`
      ? today
      : `${year}-${String(month + 1).padStart(2, "0")}-01`;
  }

  renderDayDetail(selectedDate);
  renderCalendarSummary(monthEvents);
}

function renderEvents() {
  const events = [...state.events].sort((a, b) => new Date(a.date) - new Date(b.date));
  renderCalendar();
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

function addEvent(event) {
  state.events.push(event);
  persistState();
  renderEvents();
}

function initEventForm() {
  eventForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    addEvent({
      title: form.title.value,
      date: form.date.value,
      time: form.time.value,
      people: form.people.value,
      type: form.type.value,
    });
    form.reset();
  });
}

function initCalendarControls() {
  calendarGrid?.addEventListener("click", (event) => {
    const dayButton = event.target.closest(".day[data-date]");
    if (!dayButton) return;
    selectedDate = dayButton.dataset.date;
    renderCalendar();
  });

  prevMonthButton?.addEventListener("click", () => {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1);
    renderCalendar();
  });

  nextMonthButton?.addEventListener("click", () => {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 1);
    renderCalendar();
  });
}

function initEventGridActions() {
  eventGrid?.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-action='delete-event']");
    if (!btn) return;
    const index = Number(btn.dataset.index);
    state.events.splice(index, 1);
    persistState();
    renderEvents();
  });
}

export function setupCalendar() {
  renderEvents();
  initEventForm();
  initCalendarControls();
  initEventGridActions();
}
