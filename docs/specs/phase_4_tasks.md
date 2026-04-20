# Phase 4 Spec: Tasks and Subtasks

## Behavior
- New task insertion defaults to top in current UX draft (explicit temporary decision).
- Task and subtask list styles are stored separately in the data model.
- Subtask completion can auto-complete parent task when all child subtasks are done.

## Constraints
- Ordering is maintained by `orderIndex` in both `tasks` and `subtasks`.
- Due date fields are UTC in storage and timezone-adjusted at API/UI boundaries.

## Edge cases
- Reordering updates index values deterministically.
- Due time is disabled when due date is absent.
