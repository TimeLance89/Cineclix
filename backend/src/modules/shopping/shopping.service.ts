import { createId, ShoppingList, ShoppingListItem, store } from '../../data/store';
import { ensureMembership } from '../households/households.service';

export const listShoppingLists = (householdId: string, userId: string) => {
  ensureMembership(householdId, userId);
  return store.shoppingLists.filter((list) => list.householdId === householdId);
};

export const createShoppingList = (householdId: string, userId: string, name: string) => {
  ensureMembership(householdId, userId);
  const now = new Date();
  const list: ShoppingList = { id: createId(), householdId, name, createdBy: userId, createdAt: now, updatedAt: now };
  store.shoppingLists.push(list);
  return list;
};

export const listItems = (householdId: string, userId: string, listId: string) => {
  ensureMembership(householdId, userId);
  const list = store.shoppingLists.find((l) => l.id === listId && l.householdId === householdId);
  if (!list) throw new Error('List not found');
  return store.shoppingListItems.filter((item) => item.listId === listId);
};

export const addItem = (householdId: string, userId: string, listId: string, name: string, quantity?: string) => {
  ensureMembership(householdId, userId);
  const list = store.shoppingLists.find((l) => l.id === listId && l.householdId === householdId);
  if (!list) throw new Error('List not found');
  const now = new Date();
  const item: ShoppingListItem = {
    id: createId(),
    listId,
    name,
    quantity,
    isDone: false,
    createdAt: now,
    updatedAt: now,
  };
  store.shoppingListItems.push(item);
  list.updatedAt = now;
  return item;
};

export const updateItem = (
  householdId: string,
  userId: string,
  listId: string,
  itemId: string,
  updates: Partial<Omit<ShoppingListItem, 'id' | 'listId' | 'createdAt'>>,
) => {
  ensureMembership(householdId, userId);
  const list = store.shoppingLists.find((l) => l.id === listId && l.householdId === householdId);
  if (!list) throw new Error('List not found');
  const idx = store.shoppingListItems.findIndex((i) => i.id === itemId && i.listId === listId);
  if (idx === -1) throw new Error('Item not found');
  store.shoppingListItems[idx] = { ...store.shoppingListItems[idx], ...updates, updatedAt: new Date() };
  list.updatedAt = new Date();
  return store.shoppingListItems[idx];
};

export const deleteItem = (householdId: string, userId: string, listId: string, itemId: string) => {
  ensureMembership(householdId, userId);
  const list = store.shoppingLists.find((l) => l.id === listId && l.householdId === householdId);
  if (!list) throw new Error('List not found');
  const idx = store.shoppingListItems.findIndex((i) => i.id === itemId && i.listId === listId);
  if (idx === -1) throw new Error('Item not found');
  store.shoppingListItems.splice(idx, 1);
  list.updatedAt = new Date();
};
