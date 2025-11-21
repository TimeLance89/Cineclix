import { Router } from 'express';
import { authMiddleware } from '../../middleware/authMiddleware';
import { createHandler, listHandler } from './households.controller';

const router = Router();

router.get('/', authMiddleware, listHandler);
router.post('/', authMiddleware, createHandler);

export default router;
