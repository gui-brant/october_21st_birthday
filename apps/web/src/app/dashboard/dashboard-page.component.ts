import { Component, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { StateService } from '../core/state.service';

@Component({
  standalone: true,
  imports: [FormsModule, RouterLink],
  template: `
    <section class="card">
      <h1>Hello, {{ state.userName() }}, what are we working on today?</h1>
      <input [(ngModel)]="query" placeholder="Search for Project" />
      <button (click)="createProject()">+ New Project</button>
      @if (filteredProjects().length === 0) {
      <p>No projects found.</p>
      }
      @for (project of filteredProjects(); track project.id) {
      <div>
        <a [routerLink]="['/project', project.id]">{{ project.title }}</a>
      </div>
      }
    </section>
  `,
})
export class DashboardPageComponent {
  query = '';
  constructor(public readonly state: StateService, private readonly router: Router) {}

  filteredProjects = computed(() => {
    const needle = this.query.toLowerCase().replace(/\s+/g, '');
    return this.state
      .projects()
      .filter((project) => project.title.toLowerCase().replace(/\s+/g, '').includes(needle));
  });

  createProject(): void {
    const id = this.state.addProject(`Project ${this.state.projects().length + 1}`);
    this.router.navigate(['/project', id]);
  }
}
