import { createId, store, Task } from '../../data/store';
import { ensureMembership } from '../households/households.service';

interface TaskFilters {
  status?: 'open' | 'done';
  due_from?: string;
  due_to?: string;
}

export const listTasks = (householdId: string, userId: string, filters: TaskFilters) => {
  ensureMembership(householdId, userId);
  return store.tasks.filter((task) => {
    if (task.householdId !== householdId) return false;
    if (filters.status && task.status !== filters.status) return false;
    if (filters.due_from && task.dueDate && new Date(task.dueDate) < new Date(filters.due_from)) return false;
    if (filters.due_to && task.dueDate && new Date(task.dueDate) > new Date(filters.due_to)) return false;
    return true;
  });
};

export const createTask = (
  householdId: string,
  userId: string,
  data: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'householdId' | 'createdBy' | 'status'> & { status?: 'open' | 'done' },
) => {
  ensureMembership(householdId, userId);
  const now = new Date();
  const task: Task = {
    id: createId(),
    householdId,
    createdBy: userId,
    createdAt: now,
    updatedAt: now,
    status: data.status ?? 'open',
    ...data,
  };
  store.tasks.push(task);
  return task;
};

export const updateTask = (
  householdId: string,
  userId: string,
  taskId: string,
  updates: Partial<Omit<Task, 'id' | 'createdBy' | 'householdId' | 'createdAt'>>,
) => {
  ensureMembership(householdId, userId);
  const idx = store.tasks.findIndex((t) => t.id === taskId && t.householdId === householdId);
  if (idx === -1) throw new Error('Task not found');
  store.tasks[idx] = { ...store.tasks[idx], ...updates, updatedAt: new Date() };
  return store.tasks[idx];
};

export const deleteTask = (householdId: string, userId: string, taskId: string) => {
  ensureMembership(householdId, userId);
  const idx = store.tasks.findIndex((t) => t.id === taskId && t.householdId === householdId);
  if (idx === -1) throw new Error('Task not found');
  store.tasks.splice(idx, 1);
};
