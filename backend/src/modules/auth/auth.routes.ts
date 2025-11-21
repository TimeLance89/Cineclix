import { Router } from 'express';
import { loginHandler, meHandler, registerHandler } from './auth.controller';
import { authMiddleware } from '../../middleware/authMiddleware';

const router = Router();

router.post('/register', registerHandler);
router.post('/login', loginHandler);
router.get('/me', authMiddleware, meHandler);

export default router;
