from datetime import UTC, datetime

from app.services.leveling import apply_exp


async def try_award_project_exp(db, user: dict, project: dict) -> dict | None:
    project_id = project["_id"]
    user_id = user["_id"]

    existing = await db.exp_ledger.find_one({"projectId": project_id})
    if existing is not None:
        return None

    total = 0.0
    async for subtask in db.subtasks.find({"projectId": project_id}):
        if not subtask.get("completed", False):
            return None
        total += float(subtask.get("estimatedHours") or 0.0)

    gained_exp = total * 100.0
    progress = apply_exp(
        current_level=int(user["currentLevel"]),
        current_exp=float(user["currentExp"]),
        gained_exp=gained_exp,
    )
    awarded_at = datetime.now(UTC)
    await db.exp_ledger.insert_one(
        {
            "userId": user_id,
            "projectId": project_id,
            "expGained": gained_exp,
            "levelBefore": progress.level_before,
            "levelAfter": progress.level_after,
            "awardedAt": awarded_at,
        }
    )
    await db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "currentLevel": progress.level_after,
                "currentExp": progress.exp_after,
                "updatedAt": awarded_at,
            },
            "$inc": {"totalExpEarned": gained_exp},
        },
    )
    await db.projects.update_one(
        {"_id": project_id},
        {"$set": {"status": "completed", "completedAt": awarded_at, "expAwarded": gained_exp}},
    )
    return {
        "project_id": str(project_id),
        "awarded_exp": gained_exp,
        "level_before": progress.level_before,
        "level_after": progress.level_after,
    }
