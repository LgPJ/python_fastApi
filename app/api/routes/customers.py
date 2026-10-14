from collections.abc import Sequence

from fastapi import APIRouter
from fastapi import status as http_status

from app.api.deps import CustomerServiceDep
from app.models.customer import Customer, CustomerStatus
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerStatusUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=CustomerRead,
    status_code=http_status.HTTP_201_CREATED,
    summary="Create a customer (status starts as PENDING)",
)
def create_customer(data: CustomerCreate, service: CustomerServiceDep) -> CustomerRead:
    return service.create_customer(data)


@router.get(
    "",
    response_model=list[CustomerRead],
    summary="List customers, optionally filtered by status",
)
def list_customers(
    service: CustomerServiceDep, status: CustomerStatus | None = None
) -> Sequence[Customer]:
    return service.list_customers(status)


@router.get(
    "/{customer_id}",
    response_model=CustomerRead,
    summary="Get a customer by id",
    responses={404: {"description": "Customer not found"}},
)
def get_customer(customer_id: int, service: CustomerServiceDep) -> Customer:
    return service.get_customer(customer_id)


@router.patch(
    "/{customer_id}/status",
    response_model=CustomerRead,
    summary="Update a customer's status",
    responses={404: {"description": "Customer not found"}},
)
def update_customer_status(
    customer_id: int, data: CustomerStatusUpdate, service: CustomerServiceDep
) -> Customer:
    return service.update_status(customer_id, data.status)
