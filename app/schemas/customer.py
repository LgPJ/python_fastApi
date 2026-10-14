from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.customer import CustomerStatus


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120, examples=["Juan Pérez"])
    email: EmailStr = Field(examples=["juan@example.com"])

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    status: CustomerStatus
    created_at: datetime


class CustomerStatusUpdate(BaseModel):
    status: CustomerStatus
