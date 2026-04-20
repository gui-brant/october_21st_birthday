# Phase 3 Spec: Dashboard and Project Search

## Behavior
- Dashboard greets user and lists projects latest-first.
- Search is whitespace-insensitive and case-insensitive.
- Empty state text is exactly: `No projects found.`
- Project delete is soft-delete only (`status = deleted`).

## Constraints
- Query latency should remain responsive for large project lists.
- Filter correctness should match baseline naive implementation.

## Adversarial validation
- Very long input strings.
- Inputs with mixed spaces/tabs.
- Non-matching queries should never return hidden/deleted projects.
