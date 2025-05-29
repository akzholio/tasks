import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text, func)

from app.db import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    priority = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class TaskLogModel(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    status = Column(Enum(TaskStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
