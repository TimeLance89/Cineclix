import { createId, store, User } from '../../data/store';
import { hashPassword, verifyPassword } from '../../utils/password';
import { createToken } from '../../utils/jwt';

interface RegisterInput {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export const registerUser = async ({ email, password, firstName, lastName }: RegisterInput) => {
  const existing = store.users.find((u) => u.email === email);
  if (existing) {
    throw new Error('Email already registered');
  }

  const passwordHash = await hashPassword(password);
  const user: User = {
    id: createId(),
    email,
    passwordHash,
    firstName,
    lastName,
  };

  store.users.push(user);
  const token = createToken({ userId: user.id, email: user.email });
  return { user, token };
};

export const loginUser = async (email: string, password: string) => {
  const user = store.users.find((u) => u.email === email);
  if (!user) {
    throw new Error('Invalid credentials');
  }

  const valid = await verifyPassword(password, user.passwordHash);
  if (!valid) {
    throw new Error('Invalid credentials');
  }

  const token = createToken({ userId: user.id, email: user.email });
  return { user, token };
};

export const getCurrentUser = (userId: string) => {
  return store.users.find((u) => u.id === userId);
};
