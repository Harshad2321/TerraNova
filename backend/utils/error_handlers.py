"""
Error handlers for the TerraNova application
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors for requests
    """
    error_messages = []
    for error in exc.errors():
        error_messages.append({
            "loc": error.get("loc", ["unknown"]),
            "msg": error.get("msg", "Unknown error"),
            "type": error.get("type", "unknown")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": error_messages,
            "message": "Invalid request parameters"
        }
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError):
    """
    Handle Pydantic validation errors
    """
    error_messages = []
    for error in exc.errors():
        error_messages.append({
            "loc": error.get("loc", ["unknown"]),
            "msg": error.get("msg", "Unknown error"),
            "type": error.get("type", "unknown")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": error_messages,
            "message": "Invalid model parameters"
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An unexpected error occurred",
            "detail": str(exc)
        }
    )
