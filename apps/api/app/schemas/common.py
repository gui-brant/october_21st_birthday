from datetime import datetime
from typing import Any

from bson import ObjectId


def oid(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    return ObjectId(str(value))


def mongo_id(doc: dict[str, Any]) -> str:
    return str(doc["_id"])


def timestamp_pair() -> dict[str, datetime]:
    now = datetime.utcnow()
    return {"createdAt": now, "updatedAt": now}
