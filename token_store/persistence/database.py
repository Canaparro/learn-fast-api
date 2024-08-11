import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncAttrs
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


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
    Singleton class to manage the database connection.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize_engine()
        return cls._instance

    def _initialize_engine(self):
        database, host, password, port, username = get_database_env_values()
        self.engine: AsyncEngine = create_async_engine(
            f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        )

    async def create_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


async def database_session_factory():
    database_manager = DatabaseManager()
    async_sessionmaker_instance = async_sessionmaker(autocommit=False, autoflush=False, bind=database_manager.engine)
    session = async_sessionmaker_instance()
    yield session
    await session.close()
