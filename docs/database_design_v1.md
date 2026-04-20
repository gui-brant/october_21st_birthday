# ProsthetiX — MongoDB Schema Reference

> **Database:** `prosthetics` · **MongoDB 6.0+**  
> Designed for scalability: all cross-entity relationships use `ObjectId` references, never embedding.

---

## Collections

### `users`
One document per registered user.

| Field | Type | Notes |
|---|---|---|
| `email` | String | Unique. Primary identifier. |
| `passwordHash` | String | Bcrypt hash. Never store plaintext. |
| `firstName` / `lastName` | String | Displayed in dashboard header. |
| `age` | Int | Stored for profile/settings. |
| `timezone` | String | IANA format (e.g. `America/Toronto`). Detected on signup; applied globally to all due date rendering. |
| `currentLevel` | Int | Current EXP level (starts at 1). |
| `currentExp` | Double | EXP accumulated toward the next level threshold. |
| `totalExpEarned` | Double | All-time EXP. Used for stats. |
| `googleAccessToken` / `googleRefreshToken` | String\|null | OAuth 2.0 tokens for Google Calendar. |
| `googleTokenExpiry` | Date\|null | When to refresh the access token. |
| `sessionTimeoutMinutes` | Int | Defaults to `30`. Options: 5, 15, 30, 60, 180, 1440, 7200, `-1` (logout-only). Exposed in Settings (future patch). |
| `listingStyle` | String | `numbered` \| `bullet` \| `dash`. Global preference; drives both task and subtask style until the Settings split ships. |
| `createdAt` / `updatedAt` | Date | — |

**Indexes:** `email` (unique)

---

### `otp_tokens`
Short-lived. One document per OTP issuance. Auto-deleted by MongoDB TTL on expiry.

| Field | Type | Notes |
|---|---|---|
| `userId` | ObjectId | Ref → `users` |
| `codeHash` | String | Bcrypt hash of the 6-digit code. |
| `attempts` | Int | Increments on each wrong entry. Max 5. |
| `locked` | Bool | Set to `true` after 5 failed attempts. |
| `expiresAt` | Date | 5 minutes from creation. TTL index purges the document automatically. |

**Indexes:** `expiresAt` (TTL), `userId`

---

### `sessions`
Server-side session store. Auto-deleted by MongoDB TTL on expiry.

| Field | Type | Notes |
|---|---|---|
| `userId` | ObjectId | Ref → `users` |
| `tokenHash` | String | Hash of the session cookie value. Unique. |
| `userAgent` / `ip` | String\|null | Metadata for future active-sessions UI. |
| `expiresAt` | Date | Derived from `users.sessionTimeoutMinutes`. TTL index purges automatically. Logout invalidates immediately regardless of expiry. |

**Indexes:** `expiresAt` (TTL), `tokenHash` (unique), `userId`

---

### `projects`
One document per project. Soft-deleted (never hard-deleted) so EXP history stays intact.

| Field | Type | Notes |
|---|---|---|
| `userId` | ObjectId | Ref → `users` |
| `title` | String | Editable. Trimmed on save; empty string never persists. |
| `status` | String | `active` \| `completed` \| `deleted` |
| `expAwarded` | Double\|null | Populated when project completes and EXP is granted. |
| `completedAt` | Date\|null | Set when all tasks are ticked. |
| `createdAt` / `updatedAt` | Date | `createdAt` drives the latest-first sort on the main tab. |

**Indexes:** `{ userId, createdAt: -1 }`, `{ userId, status }`

---

### `tasks`
One document per task. Tasks belong to a project and are ordered within it.

| Field | Type | Notes |
|---|---|---|
| `projectId` | ObjectId | Ref → `projects` |
| `userId` | ObjectId | Denormalized for single-user queries without a project join. |
| `title` | String | Editable inline (double-click). |
| `orderIndex` | Int | 0-based position within the project. Rewritten on drag-reorder. |
| `listingStyle` | String | `numbered` \| `bullet` \| `dash`. Stored independently from subtasks to support future split controls. |
| `completed` | Bool | Set manually or auto-set when all child subtasks are ticked. |
| `completedAt` | Date\|null | — |

**Indexes:** `{ projectId, orderIndex }`, `userId`

---

### `subtasks`
One document per subtask. Kept as a separate collection (not embedded in tasks) because the calendar tab queries subtasks across all tasks and projects by due date, and Google Calendar sync requires a direct index on `calendarEventId`.

| Field | Type | Notes |
|---|---|---|
| `taskId` | ObjectId | Ref → `tasks` |
| `projectId` | ObjectId | Denormalized. Avoids a join when loading the calendar tab. |
| `userId` | ObjectId | Denormalized. Single-user queries without traversing up the tree. |
| `title` | String | Editable inline (double-click). |
| `orderIndex` | Int | 0-based position within the parent task. |
| `listingStyle` | String | Stored independently from tasks. Currently mirrors task style; will be independently configurable in a future patch. |
| `estimatedHours` | Double\|null | Core EXP input: `EXP gained = Σ estimatedHours × 100` across the project. |
| `dueDateUtc` / `dueTimeUtc` | Date\|null / String\|null | Stored in UTC. Rendered using `users.timezone` at the API layer. |
| `completed` / `completedAt` | Bool / Date\|null | — |
| `calendarEventId` | String\|null | Google Calendar event ID. Set when the subtask is pushed to Google Calendar. |
| `calendarSyncedAt` | Date\|null | Timestamp of last successful sync. |

**Indexes:** `{ taskId, orderIndex }`, `projectId`, `userId`, `{ dueDateUtc }`, `calendarEventId` (sparse)

---

### `exp_ledger`
One document per EXP award event (one per completed project, ever). This collection is **not actively used in v0.1** but is written to on every project completion. It exists to support future features — per-project EXP breakdowns, history views, leaderboards, or analytics — without requiring a backfill migration later.

| Field | Type | Notes |
|---|---|---|
| `userId` | ObjectId | Ref → `users` |
| `projectId` | ObjectId | Unique. EXP can only be awarded once per project. |
| `expGained` | Double | `Σ subtask.estimatedHours × 100` at time of completion. |
| `levelBefore` / `levelAfter` | Int | Snapshot of the user's level before and after the award. |
| `awardedAt` | Date | — |

**Indexes:** `{ userId, awardedAt: -1 }`, `projectId` (unique)

---

## Planned Schema Additions
*(do not implement until the corresponding feature ships)*

| Field | Location | Reason |
|---|---|---|
| `taskInsertPosition` | `users` | Top vs. bottom insertion toggle (Settings patch) |
| Independent `listingStyle` controls | `users` | Separate task/subtask style preferences (Settings patch) |