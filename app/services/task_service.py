from app.adapters.repository import TaskRepository
from app.domain.models import Task, TaskStatus


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, title: str, description: str, priority: int) -> Task:
        task = Task(
            id=None,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.pending,
        )
        return await self.repo.add(task)

    async def list_tasks(
        self,
        title_filter: str | None = None,
        status: str | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Task]:
        return await self.repo.list_all(
            title_filter=title_filter, status=status, offset=offset, limit=limit
        )

    async def get_task(self, task_id: int) -> Task:
        task = await self.repo.get_by_id(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        return task

    async def update_status(self, task_id: int, status: TaskStatus) -> dict[str, str]:
        await self.repo.update_status(task_id, status)
        return {"message": f"Task {task_id} status updated to {status}"}

    async def delete_task(self, task_id: int) -> dict[str, str]:
        await self.repo.delete(task_id)
        return {"message": f"Task {task_id} has been deleted"}
