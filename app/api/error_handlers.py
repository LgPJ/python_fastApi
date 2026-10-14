from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import CustomerNotFoundError, DuplicateEmailError


def register_error_handlers(app: FastAPI) -> None:
    """Translate domain errors into HTTP responses (the only place that knows both)."""

    @app.exception_handler(DuplicateEmailError)
    async def duplicate_email(_: Request, exc: DuplicateEmailError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(CustomerNotFoundError)
    async def not_found(_: Request, exc: CustomerNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
