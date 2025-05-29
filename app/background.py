import asyncio
import logging

from app.adapters.repository import TaskRepository, TaskStatus
from app.config import DATABASE_URL
from app.db import get_engine, get_session_factory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

engine = get_engine(DATABASE_URL)
SessionLocal = get_session_factory(engine)


async def process_task(task_id: int):
    logger.info(f"Starting background task for task_id={task_id}")
    async with SessionLocal() as session:
        repo = TaskRepository(session)
        await repo.update_status(task_id, TaskStatus.in_progress)
        logger.info(f"Task {task_id} status set to in_progress")

    # simulate processing
    await asyncio.sleep(5)
    logger.info(f"Finished processing simulation for task_id={task_id}")

    async with SessionLocal() as session:
        repo = TaskRepository(session)
        await repo.update_status(task_id, TaskStatus.completed)
        logger.info(f"Task {task_id} status set to completed")
