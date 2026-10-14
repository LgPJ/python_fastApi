from collections.abc import Sequence

from app.core.exceptions import DuplicateEmailError
from app.models.customer import Customer, CustomerStatus
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


class CustomerService:
    """Business rules for customers. Knows nothing about HTTP or SQL."""

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def create_customer(self, data: CustomerCreate) -> Customer:
        if self._repository.get_by_email(data.email) is not None:
            raise DuplicateEmailError(data.email)
        return self._repository.add(name=data.name, email=data.email)

    def list_customers(self, status: CustomerStatus | None = None) -> Sequence[Customer]:
        return self._repository.list(status)
