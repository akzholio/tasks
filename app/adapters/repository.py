from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.adapters.models import TaskLogModel, TaskModel, TaskStatus
from app.domain.models import Task
from app.notifications import enqueue_notification


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: Task) -> Task:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
        )
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return Task(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            priority=db_task.priority,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
        )

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Task(
            id=row.id,
            title=row.title,
            description=row.description,
            status=row.status,
            priority=row.priority,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def list_all(
        self,
        title_filter: str | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Task]:
        query = select(TaskModel)

        if title_filter:
            query = query.where(TaskModel.title.ilike(f"%{title_filter}%"))
        if status:
            query = query.where(TaskModel.status == status)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)

        return [
            Task(
                id=row.id,
                title=row.title,
                description=row.description,
                status=row.status,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in result.scalars()
        ]

    async def update_status(self, task_id: int, new_status: TaskStatus) -> None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        task.status = new_status
        task.updated_at = datetime.now()
        self.session.add(task)

        log = TaskLogModel(task_id=task_id, status=new_status)
        self.session.add(log)

        await self.session.commit()
        await enqueue_notification(task_id, new_status)

    async def delete(self, task_id: int) -> None:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        await self.session.delete(task)
        await self.session.commit()
