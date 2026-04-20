import { Routes } from '@angular/router';

import { AuthPageComponent } from './auth/auth-page.component';
import { CalendarPageComponent } from './calendar/calendar-page.component';
import { DashboardPageComponent } from './dashboard/dashboard-page.component';
import { ProjectPageComponent } from './project/project-page.component';

export const appRoutes: Routes = [
  { path: '', redirectTo: 'auth', pathMatch: 'full' },
  { path: 'auth', component: AuthPageComponent },
  { path: 'dashboard', component: DashboardPageComponent },
  { path: 'calendar', component: CalendarPageComponent },
  { path: 'project/:id', component: ProjectPageComponent },
];
