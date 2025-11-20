import { state, persistState } from "./state.js";

const expenseList = document.getElementById("expense-list");
const expenseForm = document.getElementById("expense-form");

function renderExpenses() {
  const total = state.expenses.reduce((sum, e) => sum + Number(e.amount), 0);
  const byCategory = state.expenses.reduce((acc, expense) => {
    acc[expense.category] = (acc[expense.category] || 0) + Number(expense.amount);
    return acc;
  }, {});
  const byPayer = state.expenses.reduce((acc, expense) => {
    acc[expense.payer] = (acc[expense.payer] || 0) + Number(expense.amount);
    return acc;
  }, {});
  const avg = total / Object.keys(byPayer).length || 0;
  const balances = Object.entries(byPayer)
    .map(([payer, amount]) => ({ payer, balance: amount - avg }))
    .sort((a, b) => b.balance - a.balance);

  const categoryRow = Object.entries(byCategory)
    .map(([cat, amount]) => `<div class="stat-pill"><strong>€${amount.toFixed(2)}</strong><span>${cat}</span></div>`)
    .join("");
  const payerRow = balances
    .map(({ payer, balance }) => `<div class="stat-pill"><strong>${balance >= 0 ? "+" : ""}${balance.toFixed(2)}€</strong><span>${payer}</span></div>`)
    .join("");

  expenseList.innerHTML = `
    <li class="list__header">
      <div>
        <strong>Aktueller Monat</strong>
        <small>Summe: €${total.toFixed(2)}</small>
      </div>
    </li>
    <li class="stat-row">
      <div>
        <p class="eyebrow">Kategorien</p>
        <div class="stat-pills">${categoryRow || "<span class='muted'>Noch keine Kategorien</span>"}</div>
      </div>
      <div>
        <p class="eyebrow">Ausgleich</p>
        <div class="stat-pills">${payerRow || "<span class='muted'>Noch keine Zahler</span>"}</div>
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

function addExpense(expense) {
  state.expenses.push(expense);
  persistState();
  renderExpenses();
}

function initExpenseForm() {
  expenseForm?.addEventListener("submit", (e) => {
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
}

function initExpenseActions() {
  expenseList?.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-action='delete-expense']");
    if (!btn) return;
    const index = Number(btn.dataset.index);
    state.expenses.splice(index, 1);
    persistState();
    renderExpenses();
  });
}

export function setupFinance() {
  renderExpenses();
  initExpenseForm();
  initExpenseActions();
}
