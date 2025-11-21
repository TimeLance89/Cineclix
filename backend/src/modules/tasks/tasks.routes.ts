import { Router } from 'express';
import { authMiddleware } from '../../middleware/authMiddleware';
import { createTaskHandler, deleteTaskHandler, listTasksHandler, updateTaskHandler } from './tasks.controller';

const router = Router({ mergeParams: true });

router.get('/', authMiddleware, listTasksHandler);
router.post('/', authMiddleware, createTaskHandler);
router.put('/:taskId', authMiddleware, updateTaskHandler);
router.delete('/:taskId', authMiddleware, deleteTaskHandler);

export default router;
