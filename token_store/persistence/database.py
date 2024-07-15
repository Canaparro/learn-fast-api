import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from token_store.persistence.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_database())


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
