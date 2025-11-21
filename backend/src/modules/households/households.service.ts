import { createId, Household, HouseholdMember, store } from '../../data/store';

export const listHouseholdsForUser = (userId: string) => {
  const memberships = store.householdMembers.filter((m) => m.userId === userId);
  return memberships.map((m) => {
    const household = store.households.find((h) => h.id === m.householdId)!;
    return {
      id: household.id,
      name: household.name,
      role: m.role,
    };
  });
};

export const createHousehold = (userId: string, name: string) => {
  const now = new Date();
  const household: Household = { id: createId(), name, createdAt: now, updatedAt: now };
  store.households.push(household);

  const membership: HouseholdMember = {
    id: createId(),
    userId,
    householdId: household.id,
    role: 'owner',
    createdAt: now,
  };
  store.householdMembers.push(membership);
  return household;
};

export const ensureMembership = (householdId: string, userId: string) => {
  const member = store.householdMembers.find((m) => m.householdId === householdId && m.userId === userId);
  if (!member) {
    throw new Error('Access denied for household');
  }
  return member;
};
