# Phase 5 Spec: Calendar and Google Sync

## Behavior
- Calendar reads due-date subtasks by UTC date window.
- Sync policy: Google is source of truth for event timing; app is source of truth for task structure.
- Calendar event IDs are persisted for idempotent updates.

## Constraints
- Timezone conversion happens at API/UI boundaries, not in storage.
- OAuth scopes must remain minimal and explicit.

## Edge cases
- Revoked tokens.
- Duplicate sync attempts.
- Daylight saving boundary windows.
