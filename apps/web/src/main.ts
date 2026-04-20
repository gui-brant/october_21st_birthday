import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';

import { AppComponent } from './app/app.component';
import { appRoutes } from './app/app.routes';

function debugLog(
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

debugLog('pre-fix', 'H1', 'src/main.ts:startup', 'main.ts execution started', {
  href: window.location.href,
  baseHref: document.querySelector('base')?.getAttribute('href') ?? null,
});

bootstrapApplication(AppComponent, {
  providers: [provideRouter(appRoutes)],
})
  .then(() => {
    debugLog('pre-fix', 'H1', 'src/main.ts:bootstrap-then', 'bootstrapApplication resolved', {
      appRootExists: !!document.querySelector('app-root'),
    });
  })
  .catch((err: unknown) => {
    debugLog('pre-fix', 'H1', 'src/main.ts:bootstrap-catch', 'bootstrapApplication rejected', {
      error:
        err instanceof Error
          ? { name: err.name, message: err.message, stack: err.stack?.split('\n').slice(0, 5) }
          : String(err),
    });
    console.error(err);
  });
