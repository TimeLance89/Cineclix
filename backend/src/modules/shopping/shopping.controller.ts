import { Response } from 'express';
import { z } from 'zod';
import { AuthRequest } from '../../middleware/authMiddleware';
import { addItem, createShoppingList, deleteItem, listItems, listShoppingLists, updateItem } from './shopping.service';

const listSchema = z.object({ name: z.string().min(1) });
const itemSchema = z.object({
  name: z.string().min(1).optional(),
  quantity: z.string().optional(),
  is_done: z.boolean().optional(),
});

export const listListsHandler = (req: AuthRequest, res: Response) => {
  const { householdId } = req.params;
  const lists = listShoppingLists(householdId, req.user!.id);
  return res.status(200).json(lists);
};

export const createListHandler = (req: AuthRequest, res: Response) => {
  const parsed = listSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId } = req.params;
  const list = createShoppingList(householdId, req.user!.id, parsed.data.name);
  return res.status(201).json(list);
};

export const listItemsHandler = (req: AuthRequest, res: Response) => {
  const { householdId, listId } = req.params;
  try {
    const items = listItems(householdId, req.user!.id, listId);
    return res.status(200).json(items);
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};

export const addItemHandler = (req: AuthRequest, res: Response) => {
  const parsed = itemSchema.required({ name: true }).safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId, listId } = req.params;
  try {
    const item = addItem(householdId, req.user!.id, listId, parsed.data.name!, parsed.data.quantity);
    return res.status(201).json(item);
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};

export const updateItemHandler = (req: AuthRequest, res: Response) => {
  const parsed = itemSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId, listId, itemId } = req.params;
  try {
    const item = updateItem(householdId, req.user!.id, listId, itemId, {
      name: parsed.data.name,
      quantity: parsed.data.quantity,
      isDone: parsed.data.is_done,
    });
    return res.status(200).json(item);
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};

export const deleteItemHandler = (req: AuthRequest, res: Response) => {
  const { householdId, listId, itemId } = req.params;
  try {
    deleteItem(householdId, req.user!.id, listId, itemId);
    return res.status(204).send();
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};
