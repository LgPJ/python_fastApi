from collections.abc import Sequence
from dataclasses import dataclass

from app.core.exceptions import CustomerNotFoundError, DuplicateEmailError
from app.models.customer import Customer, CustomerStatus
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


@dataclass(frozen=True)
class CustomerPage:
    items: Sequence[Customer]
    total: int


class CustomerService:
    """Business rules for customers. Knows nothing about HTTP or SQL."""

    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def create_customer(self, data: CustomerCreate) -> Customer:
        if self._repository.get_by_email(data.email) is not None:
            raise DuplicateEmailError(data.email)
        return self._repository.add(name=data.name, email=data.email)

    def list_customers(
        self, status: CustomerStatus | None = None, limit: int = 50, offset: int = 0
    ) -> CustomerPage:
        return CustomerPage(
            items=self._repository.list(status, limit, offset),
            total=self._repository.count(status),
        )

    def get_customer(self, customer_id: int) -> Customer:
        customer = self._repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        return customer

    def update_status(self, customer_id: int, status: CustomerStatus) -> Customer:
        customer = self.get_customer(customer_id)
        return self._repository.update_status(customer, status)
