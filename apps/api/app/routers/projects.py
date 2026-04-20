from datetime import UTC, datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.deps import current_user
from app.db.mongo import get_db
from app.schemas.domain import CompletionOut, ProjectCreateInput
from app.services.exp_award import try_award_project_exp

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def list_projects(
    q: str | None = Query(default=None, description="Whitespace-insensitive title filter"),
    user=Depends(current_user),
    db=Depends(get_db),
):
    query = {"userId": user["_id"], "status": {"$ne": "deleted"}}
    projects = []
    async for doc in db.projects.find(query).sort("createdAt", -1):
        title = doc["title"]
        if q:
            needle = "".join(q.lower().split())
            hay = "".join(title.lower().split())
            if needle not in hay:
                continue
        projects.append(
            {
                "id": str(doc["_id"]),
                "title": title,
                "status": doc["status"],
                "created_at": doc["createdAt"],
                "updated_at": doc["updatedAt"],
                "completed_at": doc.get("completedAt"),
                "exp_awarded": doc.get("expAwarded"),
            }
        )
    return {"items": projects}


@router.post("")
async def create_project(payload: ProjectCreateInput, user=Depends(current_user), db=Depends(get_db)):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title is required")
    now = datetime.now(UTC)
    doc = {
        "userId": user["_id"],
        "title": title,
        "status": "active",
        "expAwarded": None,
        "completedAt": None,
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.projects.insert_one(doc)
    return {"id": str(result.inserted_id), "title": title}


@router.delete("/{project_id}")
async def soft_delete_project(project_id: str, user=Depends(current_user), db=Depends(get_db)):
    result = await db.projects.update_one(
        {"_id": ObjectId(project_id), "userId": user["_id"]},
        {"$set": {"status": "deleted", "updatedAt": datetime.now(UTC)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"ok": True}


@router.post("/{project_id}/complete", response_model=CompletionOut)
async def complete_project(project_id: str, user=Depends(current_user), db=Depends(get_db)):
    project = await db.projects.find_one({"_id": ObjectId(project_id), "userId": user["_id"]})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    award = await try_award_project_exp(db, user=user, project=project)
    if award is None:
        raise HTTPException(status_code=409, detail="Project is not fully complete or already awarded")
    return CompletionOut(**award)
