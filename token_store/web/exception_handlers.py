from fastapi import Request
from fastapi.responses import JSONResponse


# @app.exception_handler(Exception)
async def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse( status_code=500, content={"message": "There was a problem processing your request."})
