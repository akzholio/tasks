from app.db import get_engine, get_session_factory

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/taskdb"
engine = get_engine(DATABASE_URL)
AsyncSessionLocal = get_session_factory(engine)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
