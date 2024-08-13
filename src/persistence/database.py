import os

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    pass


def get_database_env_values():
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    username = os.getenv("POSTGRES_USERNAME", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
    database = os.getenv("POSTGRES_DATABASE_NAME", "postgres")
    return database, host, password, port, username


class DatabaseManager:
    """
    Class to manage the database connection.
    """

    _engine: AsyncEngine | None = None

    @classmethod
    def _initialize(cls):
        if cls._engine is None:
            database, host, password, port, username = get_database_env_values()
            cls._engine = create_async_engine(
                f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
            )

    @classmethod
    async def create_database(cls):
        cls._initialize()
        async with cls._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    def get_session_factory(cls):
        cls._initialize()
        return async_sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)


async def database_session_factory():
    async_sessionmaker_instance = DatabaseManager.get_session_factory()
    session = async_sessionmaker_instance()
    yield session
    await session.close()
