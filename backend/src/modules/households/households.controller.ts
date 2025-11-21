import { Response } from 'express';
import { z } from 'zod';
import { AuthRequest } from '../../middleware/authMiddleware';
import { createHousehold, listHouseholdsForUser } from './households.service';

const createSchema = z.object({ name: z.string().min(1) });

export const listHandler = (req: AuthRequest, res: Response) => {
  const households = listHouseholdsForUser(req.user!.id);
  return res.status(200).json(households);
};

export const createHandler = (req: AuthRequest, res: Response) => {
  const parsed = createSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }

  const household = createHousehold(req.user!.id, parsed.data.name);
  return res.status(201).json(household);
};
