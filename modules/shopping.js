import { state, persistState } from "./state.js";

const shoppingList = document.getElementById("shopping-list");
const shoppingForm = document.getElementById("shopping-form");

function renderShopping() {
  const byStore = state.shopping.reduce((acc, entry) => {
    acc[entry.store] = acc[entry.store] || [];
    acc[entry.store].push(entry);
    return acc;
  }, {});

  const stores = Object.entries(byStore);
  if (!stores.length) {
    shoppingList.innerHTML = `<li><div><strong>Nichts auf der Liste</strong><small>Lege Artikel pro Laden an.</small></div></li>`;
    return;
  }

  shoppingList.innerHTML = stores
    .map(([store, items]) => {
      const open = items.filter((i) => !i.done).length;
      const total = items.length;
      const content = items
        .map(
          (entry) => `
            <div class="store-row ${entry.done ? "is-done" : ""}">
              <div>
                <strong>${entry.item}</strong>
                <small>${entry.quantity} ×</small>
              </div>
              <div class="actions">
                <button class="btn btn-ghost" data-action="toggle-shopping" data-index="${state.shopping.indexOf(entry)}">${entry.done ? "Rückgängig" : "Abgehakt"}</button>
                <button class="btn btn-ghost" data-action="delete-shopping" data-index="${state.shopping.indexOf(entry)}">Löschen</button>
              </div>
            </div>
          `
        )
        .join("");

      return `
        <li class="store-block">
          <div class="store-block__header">
            <h4>${store}</h4>
            <small>${open} offen · ${total} gesamt</small>
          </div>
          ${content}
        </li>
      `;
    })
    .join("");
}

function addShopping(item) {
  state.shopping.push(item);
  persistState();
  renderShopping();
}

function initShoppingForm() {
  shoppingForm?.addEventListener("submit", (e) => {
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
}

function initShoppingActions() {
  shoppingList?.addEventListener("click", (event) => {
    const actionBtn = event.target.closest("[data-action]");
    if (!actionBtn) return;
    const index = Number(actionBtn.dataset.index);

    if (actionBtn.dataset.action === "toggle-shopping") {
      state.shopping[index].done = !state.shopping[index].done;
      persistState();
      renderShopping();
    }

    if (actionBtn.dataset.action === "delete-shopping") {
      state.shopping.splice(index, 1);
      persistState();
      renderShopping();
    }
  });
}

export function setupShopping() {
  renderShopping();
  initShoppingForm();
  initShoppingActions();
}
