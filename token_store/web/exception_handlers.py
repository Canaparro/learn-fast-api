from fastapi import Request
from fastapi.responses import JSONResponse


# @app.exception_handler(Exception)
def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=400, content={"message": f"{str(exc)}"})
