import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./customers.db")
    app_title: str = "Customers API"
    app_version: str = "1.0.0"


settings = Settings()
