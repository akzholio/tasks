from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_engine(db_url: str):
    return create_async_engine(db_url, echo=True)


def get_session_factory(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)
