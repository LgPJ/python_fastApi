from fastapi import APIRouter, status

from app.api.deps import CustomerServiceDep
from app.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a customer (status starts as PENDING)",
)
def create_customer(data: CustomerCreate, service: CustomerServiceDep) -> CustomerRead:
    return service.create_customer(data)
