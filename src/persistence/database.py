import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    pass


def get_database_env_values() -> tuple[str, str, str, str, str]:
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

    @property
    def engine(self) -> AsyncEngine:
        if self.__class__._engine is None:
            database, host, password, port, username = get_database_env_values()
            self.__class__._engine = create_async_engine(
                f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
            )
        return self.__class__._engine

    async def create_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


async def database_session_factory() -> AsyncGenerator[AsyncSession, None]:
    async_sessionmaker_instance = DatabaseManager().get_session_factory()
    session = async_sessionmaker_instance()
    yield session
    await session.close()
