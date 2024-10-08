import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from token_store.persistence.database import DatabaseManager
from token_store.routers import token
from token_store.service.validation.validators import TokenValidationError
from token_store.web import exception_handlers


@asynccontextmanager
async def lifespan(running_app: FastAPI) -> AsyncIterator[None]:
    try:
        await DatabaseManager().create_database()
    except ConnectionRefusedError as e:
        logging.error("Error creating database: %s", e)
        # TODO: make application shutdown if database is not available
        raise
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(
    TokenValidationError, exception_handlers.http_exception_handler
)
app.include_router(token.router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
