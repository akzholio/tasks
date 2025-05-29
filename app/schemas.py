from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = ""
    priority: int = 1


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
