from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


@dataclass
class Task:
    id: int | None
    title: str
    description: str
    status: TaskStatus = TaskStatus.pending
    priority: int = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None
