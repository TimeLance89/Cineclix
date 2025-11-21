import { store } from '../../data/store';
import { ensureMembership } from '../households/households.service';

export const getDashboard = (householdId: string, userId: string) => {
  ensureMembership(householdId, userId);
  const now = new Date();
  const sevenDaysLater = new Date();
  sevenDaysLater.setDate(now.getDate() + 7);

  const upcomingEvents = store.calendarEvents
    .filter((e) => e.householdId === householdId && new Date(e.startDatetime) <= sevenDaysLater && new Date(e.endDatetime) >= now)
    .sort((a, b) => new Date(a.startDatetime).getTime() - new Date(b.startDatetime).getTime())
    .slice(0, 5);

  const openTasks = store.tasks
    .filter((t) => t.householdId === householdId && t.status === 'open')
    .sort((a, b) => {
      if (!a.dueDate) return 1;
      if (!b.dueDate) return -1;
      return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
    })
    .slice(0, 5);

  const lists = store.shoppingLists.filter((l) => l.householdId === householdId).sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
  const latestListId = lists[0]?.id;
  const shoppingItems = latestListId
    ? store.shoppingListItems.filter((i) => i.listId === latestListId && !i.isDone).slice(0, 5).map((item) => {
        const list = store.shoppingLists.find((l) => l.id === item.listId)!;
        return {
          list_id: list.id,
          list_name: list.name,
          item_id: item.id,
          name: item.name,
          quantity: item.quantity,
        };
      })
    : [];

  return {
    upcoming_events: upcomingEvents,
    open_tasks: openTasks,
    shopping_items: shoppingItems,
  };
};
