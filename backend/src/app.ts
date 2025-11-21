import express from 'express';
import cors from 'cors';
import authRoutes from './modules/auth/auth.routes';
import householdRoutes from './modules/households/households.routes';
import calendarRoutes from './modules/calendar/calendar.routes';
import taskRoutes from './modules/tasks/tasks.routes';
import shoppingRoutes from './modules/shopping/shopping.routes';
import dashboardRoutes from './modules/dashboard/dashboard.routes';
import { errorHandler } from './middleware/errorHandler';

const app = express();

app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/auth', authRoutes);
app.use('/households', householdRoutes);
app.use('/households/:householdId/events', calendarRoutes);
app.use('/households/:householdId/tasks', taskRoutes);
app.use('/households/:householdId/shopping-lists', shoppingRoutes);
app.use('/households/:householdId/dashboard', dashboardRoutes);

app.use(errorHandler);

export default app;
