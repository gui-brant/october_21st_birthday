from pymongo import ASCENDING, DESCENDING


async def ensure_indexes(db) -> None:
    await db.users.create_index("email", unique=True, name="users_email_unique")

    await db.otp_tokens.create_index("expiresAt", expireAfterSeconds=0, name="otp_ttl")
    await db.otp_tokens.create_index("userId", name="otp_user_idx")

    await db.sessions.create_index("expiresAt", expireAfterSeconds=0, name="sessions_ttl")
    await db.sessions.create_index("tokenHash", unique=True, name="sessions_token_unique")
    await db.sessions.create_index("userId", name="sessions_user_idx")

    await db.projects.create_index([("userId", ASCENDING), ("createdAt", DESCENDING)])
    await db.projects.create_index([("userId", ASCENDING), ("status", ASCENDING)])

    await db.tasks.create_index([("projectId", ASCENDING), ("orderIndex", ASCENDING)])
    await db.tasks.create_index("userId", name="tasks_user_idx")

    await db.subtasks.create_index([("taskId", ASCENDING), ("orderIndex", ASCENDING)])
    await db.subtasks.create_index("projectId", name="subtasks_project_idx")
    await db.subtasks.create_index("userId", name="subtasks_user_idx")
    await db.subtasks.create_index("dueDateUtc", name="subtasks_due_date_idx")
    await db.subtasks.create_index("calendarEventId", sparse=True, name="subtasks_calendar_sparse")

    await db.exp_ledger.create_index([("userId", ASCENDING), ("awardedAt", DESCENDING)])
    await db.exp_ledger.create_index("projectId", unique=True, name="exp_ledger_project_unique")
