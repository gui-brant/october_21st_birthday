# Phase 1 Spec: Auth, OTP, Sessions

## Behavior
- Signup/login require email/password.
- OTP challenge is required before session issuance.
- OTP expires in 5 minutes, max 5 attempts, lock on max attempts.
- Session uses HTTP-only cookie and server-side session store.

## Constraints
- `users.email` must be unique.
- OTP and sessions use TTL-backed collections.

## Edge cases
- Wrong OTP increments attempt count.
- Expired OTP returns challenge failure.
- Re-login invalidates prior OTP challenge and creates a fresh challenge.

## Security expectations
- Never store plaintext password, OTP code, or session token.
- Use uniform failure wording where possible to reduce enumeration risk.
