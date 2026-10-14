from collections.abc import Sequence
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailError
from app.models.customer import Customer, CustomerStatus


class CustomerRepository(Protocol):
    """Persistence contract the service depends on (Dependency Inversion)."""

    def add(self, name: str, email: str) -> Customer: ...

    def get(self, customer_id: int) -> Customer | None: ...

    def get_by_email(self, email: str) -> Customer | None: ...

    def list(self, status: CustomerStatus | None = None) -> Sequence[Customer]: ...


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

    def get(self, customer_id: int) -> Customer | None:
        return self._session.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        return self._session.scalar(select(Customer).where(Customer.email == email))

    def list(self, status: CustomerStatus | None = None) -> Sequence[Customer]:
        query = select(Customer).order_by(Customer.id)
        if status is not None:
            query = query.where(Customer.status == status)
        return self._session.scalars(query).all()
