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
    { title: "Kindergeburtstag Leo", date: "2024-09-25", time: "14:00", people: "Team Kita", type: "Freizeit" },
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

export const state = loadState();

export function persistState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}
