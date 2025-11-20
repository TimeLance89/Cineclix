import { setupDashboard } from "./modules/dashboard.js";
import { setupCalendar } from "./modules/calendar.js";
import { setupTasks } from "./modules/tasks.js";
import { setupShopping } from "./modules/shopping.js";
import { setupFinance } from "./modules/finance.js";
import { setupMessages } from "./modules/messages.js";
import { setupRoadmap } from "./modules/roadmap.js";
import { setupNavigation } from "./modules/navigation.js";

function init() {
  setupDashboard();
  setupCalendar();
  setupTasks();
  setupShopping();
  setupFinance();
  setupMessages();
  setupRoadmap();
  setupNavigation();
}

init();
