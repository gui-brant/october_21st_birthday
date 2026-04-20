from datetime import UTC, datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import current_user
from app.db.mongo import get_db
from app.schemas.domain import SubtaskCreateInput, TaskCreateInput

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/projects/{project_id}")
async def create_task(project_id: str, payload: TaskCreateInput, user=Depends(current_user), db=Depends(get_db)):
    project = await db.projects.find_one({"_id": ObjectId(project_id), "userId": user["_id"]})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    count = await db.tasks.count_documents({"projectId": ObjectId(project_id)})
    now = datetime.now(UTC)
    doc = {
        "projectId": ObjectId(project_id),
        "userId": user["_id"],
        "title": payload.title.strip(),
        "orderIndex": count,
        "listingStyle": payload.listing_style,
        "completed": False,
        "completedAt": None,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.tasks.insert_one(doc)
    return {"id": str(result.inserted_id)}


@router.post("/{task_id}/subtasks")
async def create_subtask(task_id: str, payload: SubtaskCreateInput, user=Depends(current_user), db=Depends(get_db)):
    task = await db.tasks.find_one({"_id": ObjectId(task_id), "userId": user["_id"]})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    count = await db.subtasks.count_documents({"taskId": ObjectId(task_id)})
    now = datetime.now(UTC)
    doc = {
        "taskId": ObjectId(task_id),
        "projectId": task["projectId"],
        "userId": user["_id"],
        "title": payload.title.strip(),
        "orderIndex": count,
        "listingStyle": payload.listing_style,
        "estimatedHours": payload.estimated_hours,
        "dueDateUtc": payload.due_date_utc,
        "dueTimeUtc": None,
        "completed": False,
        "completedAt": None,
        "calendarEventId": None,
        "calendarSyncedAt": None,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.subtasks.insert_one(doc)
    return {"id": str(result.inserted_id)}


@router.post("/subtasks/{subtask_id}/toggle")
async def toggle_subtask(subtask_id: str, user=Depends(current_user), db=Depends(get_db)):
    subtask = await db.subtasks.find_one({"_id": ObjectId(subtask_id), "userId": user["_id"]})
    if subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    new_state = not bool(subtask.get("completed"))
    await db.subtasks.update_one(
        {"_id": subtask["_id"]},
        {"$set": {"completed": new_state, "completedAt": datetime.now(UTC) if new_state else None}},
    )
    all_done = (
        await db.subtasks.count_documents({"taskId": subtask["taskId"], "completed": {"$ne": True}}) == 0
    )
    await db.tasks.update_one(
        {"_id": subtask["taskId"]},
        {"$set": {"completed": all_done, "completedAt": datetime.now(UTC) if all_done else None}},
    )
    return {"completed": new_state}


@router.get("/projects/{project_id}/tree")
async def project_tree(project_id: str, user=Depends(current_user), db=Depends(get_db)):
    project = await db.projects.find_one({"_id": ObjectId(project_id), "userId": user["_id"]})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    items = []
    async for task in db.tasks.find({"projectId": ObjectId(project_id)}).sort("orderIndex", 1):
        subs = []
        async for sub in db.subtasks.find({"taskId": task["_id"]}).sort("orderIndex", 1):
            subs.append(
                {
                    "id": str(sub["_id"]),
                    "title": sub["title"],
                    "completed": sub["completed"],
                    "estimated_hours": sub.get("estimatedHours"),
                    "due_date_utc": sub.get("dueDateUtc"),
                }
            )
        items.append(
            {
                "id": str(task["_id"]),
                "title": task["title"],
                "completed": task["completed"],
                "listing_style": task.get("listingStyle", "numbered"),
                "subtasks": subs,
            }
        )
    return {"project_id": project_id, "tasks": items}
