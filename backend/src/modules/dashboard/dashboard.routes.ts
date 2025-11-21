import { Router } from 'express';
import { authMiddleware } from '../../middleware/authMiddleware';
import { dashboardHandler } from './dashboard.controller';

const router = Router({ mergeParams: true });

router.get('/', authMiddleware, dashboardHandler);

export default router;
