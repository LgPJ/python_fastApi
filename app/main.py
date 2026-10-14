from fastapi import FastAPI

from app.api.error_handlers import register_error_handlers
from app.api.routes import customers, health
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_title, version=settings.app_version)
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(customers.router)
    return app


app = create_app()
