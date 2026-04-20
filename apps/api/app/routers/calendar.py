from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.core.deps import current_user
from app.db.mongo import get_db

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/events")
async def list_events(
    start: datetime = Query(...),
    end: datetime = Query(...),
    user=Depends(current_user),
    db=Depends(get_db),
):
    query = {
        "userId": user["_id"],
        "dueDateUtc": {"$gte": start, "$lte": end},
    }
    items = []
    async for sub in db.subtasks.find(query).sort("dueDateUtc", 1):
        items.append(
            {
                "id": str(sub["_id"]),
                "title": sub["title"],
                "start": sub["dueDateUtc"],
                "calendar_event_id": sub.get("calendarEventId"),
            }
        )
    return {"items": items, "sync_policy": "google_time_app_structure"}


@router.post("/google/sync")
async def sync_google_calendar(user=Depends(current_user)):
    # v0.1 mock endpoint for deterministic integration testing and later provider wiring.
    return {"ok": True, "user_id": str(user["_id"]), "mode": "mock_sync"}
