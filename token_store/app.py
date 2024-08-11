from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from token_store.persistence.database import DatabaseManager
from token_store.web import exception_handlers
from token_store.routers import tokens


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseManager().create_database()
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, exception_handlers.http_exception_handler)
app.include_router(tokens.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
