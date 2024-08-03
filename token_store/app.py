from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from token_store.config import DATABASE_USERNAME, DATABASE_PASSWORD
from token_store.web import exception_handlers
from token_store.routers import tokens


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
            fastapi_app,
            db_url=f"postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/postgres",
            modules={"models": ["token_store.persistence.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
    ):
        # db connected
        yield
        # app teardown
    # db connections closed


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(Exception, exception_handlers.http_exception_handler)
app.include_router(tokens.router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
