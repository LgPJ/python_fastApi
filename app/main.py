from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    return FastAPI(title=settings.app_title, version=settings.app_version)


app = create_app()
