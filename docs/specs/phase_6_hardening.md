# Phase 6 Spec: Hardening and Critique

## Deterministic checks
- API: lint, static typing, unit tests.
- Web: production build.
- Benchmarks: baseline search harness.

## Independent critique prompt
Ask an independent reviewer/model:
1. Where can OTP/session logic be bypassed?
2. Can EXP be double-awarded via concurrency?
3. Are timezone assumptions inconsistent between storage and rendering?
4. Is any sensitive token or PII exposed in logs or API responses?

## Risk escalation policy
- Highest: auth, sessions, OTP, OAuth token handling.
- Medium: EXP correctness and project completion idempotency.
- Lower: rendering-only UI defects.
