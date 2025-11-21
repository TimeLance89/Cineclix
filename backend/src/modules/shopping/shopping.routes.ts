import { Router } from 'express';
import { authMiddleware } from '../../middleware/authMiddleware';
import {
  addItemHandler,
  createListHandler,
  deleteItemHandler,
  listItemsHandler,
  listListsHandler,
  updateItemHandler,
} from './shopping.controller';

const router = Router({ mergeParams: true });

router.get('/', authMiddleware, listListsHandler);
router.post('/', authMiddleware, createListHandler);
router.get('/:listId/items', authMiddleware, listItemsHandler);
router.post('/:listId/items', authMiddleware, addItemHandler);
router.patch('/:listId/items/:itemId', authMiddleware, updateItemHandler);
router.delete('/:listId/items/:itemId', authMiddleware, deleteItemHandler);

export default router;
