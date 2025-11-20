export function formatDate(date) {
  const d = new Date(`${date}T00:00:00`);
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "short", year: "numeric" });
}
