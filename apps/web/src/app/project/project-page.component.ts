import { Component, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { StateService } from '../core/state.service';

@Component({
  standalone: true,
  imports: [FormsModule],
  template: `
    <section class="card">
      @if (project()) {
      <h2>{{ project()!.title }}</h2>
      <input [(ngModel)]="taskTitle" placeholder="New Task" />
      <button (click)="addTask()">Add Task</button>

      @for (task of project()!.tasks; track task.id) {
      <div class="card">
        <label><input type="checkbox" [checked]="task.completed" /> {{ task.title }}</label>
        <div>
          <input [(ngModel)]="subtaskTitle" placeholder="New Subtask" />
          <input [(ngModel)]="subtaskHours" type="number" placeholder="Estimated hours" />
          <button (click)="addSubtask(task.id)">Add Subtask</button>
        </div>
        @for (subtask of task.subtasks; track subtask.id) {
        <div>
          - {{ subtask.title }} @if (subtask.estimatedHours) {<span>({{ subtask.estimatedHours }} h)</span>}
        </div>
        }
      </div>
      }
      } @else {
      <p>Project not found.</p>
      }
    </section>
  `,
})
export class ProjectPageComponent {
  taskTitle = '';
  subtaskTitle = '';
  subtaskHours: number | null = null;

  readonly projectId: string;
  readonly project;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly state: StateService,
  ) {
    this.projectId = this.route.snapshot.paramMap.get('id') ?? '';
    this.project = computed(() =>
      this.state.projects().find((projectItem) => projectItem.id === this.projectId),
    );
  }

  addTask(): void {
    if (!this.taskTitle.trim()) {
      return;
    }
    this.state.addTask(this.projectId, this.taskTitle.trim());
    this.taskTitle = '';
  }

  addSubtask(taskId: string): void {
    if (!this.subtaskTitle.trim()) {
      return;
    }
    this.state.addSubtask(this.projectId, taskId, this.subtaskTitle.trim(), this.subtaskHours ?? undefined);
    this.subtaskTitle = '';
    this.subtaskHours = null;
  }
}
