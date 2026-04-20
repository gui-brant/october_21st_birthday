import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  imports: [FormsModule],
  template: `
    <section class="card">
      <h2>{{ signupMode() ? 'Sign up' : 'Log in' }}</h2>
      <label>Email <input [(ngModel)]="email" /></label><br />
      <label>Password <input type="password" [(ngModel)]="password" /></label><br />
      @if (signupMode()) {
      <label>First Name <input [(ngModel)]="firstName" /></label><br />
      <label>Last Name <input [(ngModel)]="lastName" /></label><br />
      <label>Age <input type="number" [(ngModel)]="age" /></label><br />
      }
      <button (click)="submit()">{{ signupMode() ? 'Sign up' : 'Log in' }}</button>
      <button (click)="toggle()">{{ signupMode() ? 'Switch to login' : 'Switch to signup' }}</button>
    </section>
  `,
})
export class AuthPageComponent {
  signupMode = signal(false);
  email = '';
  password = '';
  firstName = '';
  lastName = '';
  age = 21;

  constructor(private readonly router: Router) {}

  toggle(): void {
    this.signupMode.update((v) => !v);
  }

  submit(): void {
    this.router.navigateByUrl('/dashboard');
  }
}
