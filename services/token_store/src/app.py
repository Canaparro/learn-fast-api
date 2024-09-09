import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from services.token_store.src.persistence.database import DatabaseManager
from services.token_store.src.routers import token
from services.token_store.src.service.validation.validators import TokenValidationError
from services.token_store.src.web import exception_handlers


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
    uvicorn.run("services.token_store.src.app:app", host="0.0.0.0", port=8000, reload=True)