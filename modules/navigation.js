const menuGrid = document.getElementById("menu-grid");
const CTA_DEMO = document.getElementById("cta-demo");
const CTA_BACKLOG = document.getElementById("cta-backlog");

function initMenuBoard() {
  menuGrid?.addEventListener("click", (event) => {
    const card = event.target.closest(".menu-card");
    if (!card) return;
    const targetId = card.dataset.target;
    const el = document.getElementById(targetId);
    el?.scrollIntoView({ behavior: "smooth" });
  });
}

function initCtas() {
  CTA_DEMO?.addEventListener("click", () => {
    document.getElementById("calendar")?.scrollIntoView({ behavior: "smooth" });
  });
  CTA_BACKLOG?.addEventListener("click", () => {
    document.getElementById("roadmap")?.scrollIntoView({ behavior: "smooth" });
  });
}

export function setupNavigation() {
  initMenuBoard();
  initCtas();
}
