import { v4 as uuid } from 'uuid';

export type Role = 'owner' | 'member';
export type TaskStatus = 'open' | 'done';

export interface User {
  id: string;
  email: string;
  passwordHash: string;
  firstName?: string;
  lastName?: string;
}

export interface Household {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface HouseholdMember {
  id: string;
  userId: string;
  householdId: string;
  role: Role;
  createdAt: Date;
}

export interface Invitation {
  id: string;
  householdId: string;
  email: string;
  token: string;
  status: 'pending' | 'accepted' | 'expired';
  createdAt: Date;
  expiresAt: Date;
}

export interface CalendarEvent {
  id: string;
  householdId: string;
  title: string;
  description?: string;
  startDatetime: string;
  endDatetime: string;
  allDay: boolean;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Task {
  id: string;
  householdId: string;
  title: string;
  description?: string;
  dueDate?: string;
  assignedTo?: string;
  status: TaskStatus;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ShoppingList {
  id: string;
  householdId: string;
  name: string;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ShoppingListItem {
  id: string;
  listId: string;
  name: string;
  quantity?: string;
  isDone: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export const store = {
  users: [] as User[],
  households: [] as Household[],
  householdMembers: [] as HouseholdMember[],
  invitations: [] as Invitation[],
  calendarEvents: [] as CalendarEvent[],
  tasks: [] as Task[],
  shoppingLists: [] as ShoppingList[],
  shoppingListItems: [] as ShoppingListItem[],
};

export const createId = () => uuid();
