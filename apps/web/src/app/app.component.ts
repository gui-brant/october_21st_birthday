import { Component } from '@angular/core';
import { NavigationEnd, NavigationError, Router, RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <nav class="container">
      <a routerLink="/auth">Auth</a> |
      <a routerLink="/dashboard">Main</a> |
      <a routerLink="/calendar">Calendar</a>
    </nav>
    <main class="container">
      <router-outlet />
    </main>
  `,
})
export class AppComponent {
  constructor(private readonly router: Router) {
    this.debugLog('pre-fix', 'H2', 'src/app/app.component.ts:constructor', 'AppComponent constructed', {
      url: this.router.url,
      bodyChildren: document.body.childElementCount,
    });

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.debugLog(
          'pre-fix',
          'H3',
          'src/app/app.component.ts:navigation-end',
          'NavigationEnd received',
          { url: event.urlAfterRedirects },
        );
      }

      if (event instanceof NavigationError) {
        this.debugLog(
          'pre-fix',
          'H4',
          'src/app/app.component.ts:navigation-error',
          'NavigationError received',
          {
            url: event.url,
            error:
              event.error instanceof Error
                ? {
                    name: event.error.name,
                    message: event.error.message,
                    stack: event.error.stack?.split('\n').slice(0, 5),
                  }
                : String(event.error),
          },
        );
      }
    });
  }

  private debugLog(
    runId: string,
    hypothesisId: string,
    location: string,
    message: string,
    data: Record<string, unknown>,
  ): void {
    // #region agent log
    fetch('http://127.0.0.1:7525/ingest/3a41880b-9948-44cd-8c6b-f83166b7859f', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '028af7' },
      body: JSON.stringify({
        sessionId: '028af7',
        runId,
        hypothesisId,
        location,
        message,
        data,
        timestamp: Date.now(),
      }),
    }).catch(() => {});
    // #endregion
  }
}
