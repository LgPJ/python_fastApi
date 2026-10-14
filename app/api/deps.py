from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.repositories.customer_repository import SqlAlchemyCustomerRepository
from app.services.customer_service import CustomerService


def get_customer_service(
    session: Annotated[Session, Depends(get_session)],
) -> CustomerService:
    return CustomerService(SqlAlchemyCustomerRepository(session))


CustomerServiceDep = Annotated[CustomerService, Depends(get_customer_service)]
