import logging

from fastapi import Request
from fastapi.responses import JSONResponse


def http_exception_handler(request: Request, exc: Exception):
    # log as info the request data and the exception use % instead of fstring
    logging.info("Request data: %s", request.json())

    return JSONResponse(status_code=400, content={"message": f"{str(exc)}"})
