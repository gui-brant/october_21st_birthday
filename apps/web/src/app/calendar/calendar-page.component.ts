import { Component } from '@angular/core';

@Component({
  standalone: true,
  template: `
    <section class="card">
      <h2>Calendar</h2>
      <p>
        FullCalendar + Google sync scaffold. Policy: Google is source of truth for time and app is source
        of truth for task structure.
      </p>
    </section>
  `,
})
export class CalendarPageComponent {}
