from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ListStyle = Literal["numbered", "bullet", "dash"]


class ProjectCreateInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class ProjectOut(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    exp_awarded: float | None = None


class TaskCreateInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    listing_style: ListStyle = "numbered"


class SubtaskCreateInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    listing_style: ListStyle = "numbered"
    estimated_hours: float | None = Field(default=None, ge=0, le=1000)
    due_date_utc: datetime | None = None


class CompletionOut(BaseModel):
    project_id: str
    awarded_exp: float
    level_before: int
    level_after: int
