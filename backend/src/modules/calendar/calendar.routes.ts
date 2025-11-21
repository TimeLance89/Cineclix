import { Router } from 'express';
import { authMiddleware } from '../../middleware/authMiddleware';
import { createEventHandler, deleteEventHandler, listEventsHandler, updateEventHandler } from './calendar.controller';

const router = Router({ mergeParams: true });

router.get('/', authMiddleware, listEventsHandler);
router.post('/', authMiddleware, createEventHandler);
router.put('/:eventId', authMiddleware, updateEventHandler);
router.delete('/:eventId', authMiddleware, deleteEventHandler);

export default router;
