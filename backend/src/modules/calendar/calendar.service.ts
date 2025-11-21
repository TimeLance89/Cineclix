import { createId, CalendarEvent, store } from '../../data/store';
import { ensureMembership } from '../households/households.service';

export const listEvents = (householdId: string, userId: string, from?: string, to?: string) => {
  ensureMembership(householdId, userId);
  return store.calendarEvents.filter((event) => {
    if (event.householdId !== householdId) return false;
    if (from && new Date(event.endDatetime) < new Date(from)) return false;
    if (to && new Date(event.startDatetime) > new Date(to)) return false;
    return true;
  });
};

export const createEvent = (
  householdId: string,
  userId: string,
  data: Omit<CalendarEvent, 'id' | 'createdAt' | 'updatedAt' | 'householdId' | 'createdBy'>,
) => {
  ensureMembership(householdId, userId);
  const now = new Date();
  const event: CalendarEvent = {
    id: createId(),
    householdId,
    createdBy: userId,
    createdAt: now,
    updatedAt: now,
    ...data,
  };
  store.calendarEvents.push(event);
  return event;
};

export const updateEvent = (
  householdId: string,
  userId: string,
  eventId: string,
  data: Partial<Omit<CalendarEvent, 'id' | 'householdId' | 'createdBy' | 'createdAt'>>,
) => {
  ensureMembership(householdId, userId);
  const idx = store.calendarEvents.findIndex((e) => e.id === eventId && e.householdId === householdId);
  if (idx === -1) throw new Error('Event not found');
  store.calendarEvents[idx] = { ...store.calendarEvents[idx], ...data, updatedAt: new Date() };
  return store.calendarEvents[idx];
};

export const deleteEvent = (householdId: string, userId: string, eventId: string) => {
  ensureMembership(householdId, userId);
  const idx = store.calendarEvents.findIndex((e) => e.id === eventId && e.householdId === householdId);
  if (idx === -1) throw new Error('Event not found');
  store.calendarEvents.splice(idx, 1);
};
