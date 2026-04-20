# Phase 2 Spec: Leveling and EXP Awarding

## Behavior
- EXP is awarded only when all tasks and subtasks in a project are completed.
- Each project can award EXP exactly once.
- EXP awarded equals `sum(subtask.estimatedHours) * 100`.

## Constraints
- `exp_ledger.projectId` unique index enforces one-time award.
- Level thresholds follow piecewise `H(x)` and `E(x) = 100 * H(x)`.

## Edge cases
- Concurrent completion requests must not double award.
- Projects with missing estimates award only what is explicitly estimated.

## Known v0.1 gap
- Users can create very small projects and claim EXP quickly; this is accepted temporarily and flagged for a hardening patch.
