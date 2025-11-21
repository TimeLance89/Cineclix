import { Request, Response } from 'express';
import { z } from 'zod';
import { registerUser, loginUser, getCurrentUser } from './auth.service';
import { AuthRequest } from '../../middleware/authMiddleware';

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

export const registerHandler = async (req: Request, res: Response) => {
  const parsed = registerSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }

  try {
    const { email, password, first_name, last_name } = parsed.data;
    const result = await registerUser({ email, password, firstName: first_name, lastName: last_name });
    const { passwordHash, ...safeUser } = result.user;
    return res.status(201).json({ user: safeUser, token: result.token });
  } catch (err: any) {
    return res.status(400).json({ error: { code: 'BAD_REQUEST', message: err.message } });
  }
};

export const loginHandler = async (req: Request, res: Response) => {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }

  try {
    const { email, password } = parsed.data;
    const result = await loginUser(email, password);
    const { passwordHash, ...safeUser } = result.user;
    return res.status(200).json({ user: safeUser, token: result.token });
  } catch (err: any) {
    return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: err.message } });
  }
};

export const meHandler = (req: AuthRequest, res: Response) => {
  if (!req.user) {
    return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Not authenticated' } });
  }

  const user = getCurrentUser(req.user.id);
  if (!user) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: 'User not found' } });
  }

  const { passwordHash, ...safeUser } = user;
  return res.status(200).json(safeUser);
};
