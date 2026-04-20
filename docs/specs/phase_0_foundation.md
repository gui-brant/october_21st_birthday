# Phase 0 Spec: Foundation

## Behavior
- Monorepo has `apps/web` (Angular), `apps/api` (FastAPI), and plan/spec docs.
- API creates required MongoDB indexes at startup.
- CI runs deterministic checks for API (`ruff`, `pyright`, `pytest`) and web build.

## Constraints
- Stack is fixed to Angular + TypeScript, FastAPI + Python, MongoDB.
- Docker/Google Cloud are postponed.

## Edge cases
- API should fail early if MongoDB is unavailable.
- API should remain idempotent when startup index creation runs repeatedly.

## Security and performance expectations
- No plaintext credential-like values in database.
- Startup index creation includes TTL and unique constraints from DB design.
- Search and leveling benchmark harness exists for baseline comparisons.
