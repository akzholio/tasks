import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository import TaskRepository
from app.background import process_task
from app.db import Base
from app.dependencies import engine, get_session
from app.schemas import TaskCreate, TaskRead, TaskStatus
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan, title="Async Task Management API")


# Dependency wiring
def get_service(session: AsyncSession = Depends(get_session)):
    repo = TaskRepository(session)
    return TaskService(repo)


@app.get("/healthcheck", status_code=200)
async def healthcheck():
    return {"status": "ok"}


# POST /tasks
@app.post("/tasks", response_model=TaskRead, status_code=201)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_service)):
    created = await service.create_task(task.title, task.description, task.priority)
    return created


# GET /tasks
@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    title: str | None = Query(None),
    status: TaskStatus | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    service: TaskService = Depends(get_service),
):
    return await service.list_tasks(
        title_filter=title, status=status, offset=offset, limit=limit
    )


# GET /tasks/{task_id}
@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, service: TaskService = Depends(get_service)):
    try:
        return await service.get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUT /tasks/{task_id}
@app.put("/tasks/{task_id}", status_code=204)
async def update_task_status(
    task_id: int, status: TaskStatus, service: TaskService = Depends(get_service)
):
    try:
        await service.update_status(task_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    try:
        await service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/tasks/{task_id}/process", status_code=202)
async def start_task_processing(
    task_id: int, session: AsyncSession = Depends(get_session)
):
    logger.info(f"Received request to process task {task_id}")
    repo = TaskRepository(session)

    try:
        task = await repo.get_by_id(task_id)
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving task {task_id}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error") from e

    if not task:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    logger.info(f"Starting background task processing for task {task_id}")
    asyncio.create_task(process_task(task_id))
    return {"message": f"Task {task_id} processing started"}
