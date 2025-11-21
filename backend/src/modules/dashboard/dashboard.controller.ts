import { Response } from 'express';
import { AuthRequest } from '../../middleware/authMiddleware';
import { getDashboard } from './dashboard.service';

export const dashboardHandler = (req: AuthRequest, res: Response) => {
  const { householdId } = req.params;
  const data = getDashboard(householdId, req.user!.id);
  return res.status(200).json(data);
};
