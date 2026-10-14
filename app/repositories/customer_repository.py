from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailError
from app.models.customer import Customer, CustomerStatus


class CustomerRepository(Protocol):
    """Persistence contract the service depends on (Dependency Inversion)."""

    def add(self, name: str, email: str) -> Customer: ...

    def get_by_email(self, email: str) -> Customer | None: ...


class SqlAlchemyCustomerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, name: str, email: str) -> Customer:
        customer = Customer(name=name, email=email, status=CustomerStatus.PENDING)
        self._session.add(customer)
        try:
            self._session.commit()
        except IntegrityError as exc:
            # Unique constraint also protects against concurrent duplicate inserts.
            self._session.rollback()
            raise DuplicateEmailError(email) from exc
        return customer

    def get_by_email(self, email: str) -> Customer | None:
        return self._session.scalar(select(Customer).where(Customer.email == email))
