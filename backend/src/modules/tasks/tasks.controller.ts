import { Response } from 'express';
import { z } from 'zod';
import { AuthRequest } from '../../middleware/authMiddleware';
import { createTask, deleteTask, listTasks, updateTask } from './tasks.service';

const taskSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
  due_date: z.string().optional(),
  assigned_to: z.string().optional(),
  status: z.enum(['open', 'done']).optional(),
});

export const listTasksHandler = (req: AuthRequest, res: Response) => {
  const { householdId } = req.params;
  const tasks = listTasks(householdId, req.user!.id, {
    status: req.query.status as 'open' | 'done' | undefined,
    due_from: req.query.due_from as string | undefined,
    due_to: req.query.due_to as string | undefined,
  });
  return res.status(200).json(tasks);
};

export const createTaskHandler = (req: AuthRequest, res: Response) => {
  const parsed = taskSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId } = req.params;
  const task = createTask(householdId, req.user!.id, {
    title: parsed.data.title,
    description: parsed.data.description,
    dueDate: parsed.data.due_date,
    assignedTo: parsed.data.assigned_to,
    status: parsed.data.status,
  });
  return res.status(201).json(task);
};

export const updateTaskHandler = (req: AuthRequest, res: Response) => {
  const parsed = taskSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId, taskId } = req.params;
  try {
    const task = updateTask(householdId, req.user!.id, taskId, {
      title: parsed.data.title,
      description: parsed.data.description,
      dueDate: parsed.data.due_date,
      assignedTo: parsed.data.assigned_to,
      status: parsed.data.status,
    });
    return res.status(200).json(task);
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};

export const deleteTaskHandler = (req: AuthRequest, res: Response) => {
  const { householdId, taskId } = req.params;
  try {
    deleteTask(householdId, req.user!.id, taskId);
    return res.status(204).send();
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};
