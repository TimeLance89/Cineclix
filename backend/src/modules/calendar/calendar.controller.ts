import { Request, Response } from 'express';
import { z } from 'zod';
import { AuthRequest } from '../../middleware/authMiddleware';
import { createEvent, deleteEvent, listEvents, updateEvent } from './calendar.service';

const eventSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
  start_datetime: z.string(),
  end_datetime: z.string(),
  all_day: z.boolean().optional().default(false),
});

export const listEventsHandler = (req: AuthRequest, res: Response) => {
  const { householdId } = req.params;
  const events = listEvents(householdId, req.user!.id, req.query.from as string | undefined, req.query.to as string | undefined);
  return res.status(200).json(events);
};

export const createEventHandler = (req: AuthRequest, res: Response) => {
  const parsed = eventSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId } = req.params;
  const payload = parsed.data;
  const event = createEvent(householdId, req.user!.id, {
    title: payload.title,
    description: payload.description,
    startDatetime: payload.start_datetime,
    endDatetime: payload.end_datetime,
    allDay: payload.all_day ?? false,
  });
  return res.status(201).json(event);
};

export const updateEventHandler = (req: AuthRequest, res: Response) => {
  const parsed = eventSchema.partial().safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: parsed.error.message } });
  }
  const { householdId, eventId } = req.params;
  try {
    const event = updateEvent(householdId, req.user!.id, eventId, {
      title: parsed.data.title,
      description: parsed.data.description,
      startDatetime: parsed.data.start_datetime,
      endDatetime: parsed.data.end_datetime,
      allDay: parsed.data.all_day,
    });
    return res.status(200).json(event);
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};

export const deleteEventHandler = (req: AuthRequest, res: Response) => {
  const { householdId, eventId } = req.params;
  try {
    deleteEvent(householdId, req.user!.id, eventId);
    return res.status(204).send();
  } catch (err: any) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', message: err.message } });
  }
};
