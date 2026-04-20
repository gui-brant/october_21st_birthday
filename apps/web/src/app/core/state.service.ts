import { Injectable, signal } from '@angular/core';

type Project = { id: string; title: string; tasks: Task[] };
type Task = { id: string; title: string; completed: boolean; subtasks: Subtask[] };
type Subtask = { id: string; title: string; completed: boolean; estimatedHours?: number };

@Injectable({ providedIn: 'root' })
export class StateService {
  userName = signal('October');
  projects = signal<Project[]>([]);

  addProject(title: string): string {
    const id = crypto.randomUUID();
    this.projects.update((prev) => [{ id, title, tasks: [] }, ...prev]);
    return id;
  }

  addTask(projectId: string, title: string): string {
    const taskId = crypto.randomUUID();
    this.projects.update((projects) =>
      projects.map((p) =>
        p.id === projectId
          ? { ...p, tasks: [...p.tasks, { id: taskId, title, completed: false, subtasks: [] }] }
          : p,
      ),
    );
    return taskId;
  }

  addSubtask(projectId: string, taskId: string, title: string, estimatedHours?: number): void {
    this.projects.update((projects) =>
      projects.map((p) =>
        p.id !== projectId
          ? p
          : {
              ...p,
              tasks: p.tasks.map((t) =>
                t.id !== taskId
                  ? t
                  : {
                      ...t,
                      subtasks: [
                        ...t.subtasks,
                        { id: crypto.randomUUID(), title, completed: false, estimatedHours },
                      ],
                    },
              ),
            },
      ),
    );
  }
}
