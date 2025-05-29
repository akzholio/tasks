import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Shared queue for notification jobs
notification_queue: asyncio.Queue = asyncio.Queue()


class Notification:
    def __init__(self, task_id: int, new_status: str):
        self.task_id = task_id
        self.new_status = new_status


async def enqueue_notification(task_id: int, new_status: str):
    await notification_queue.put(Notification(task_id, new_status))


async def notification_worker():
    while True:
        notification = await notification_queue.get()
        try:
            logger.info(
                f"[NOTIFY] Task {notification.task_id} status changed to {notification.new_status}"
            )
            # Replace with actual webhook/email/etc logic
        except Exception as e:
            logger.error(f"Notification failed: {e}")
        finally:
            notification_queue.task_done()
