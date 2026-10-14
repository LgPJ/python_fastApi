class DomainError(Exception):
    """Base class for business-rule errors, independent of HTTP."""


class DuplicateEmailError(DomainError):
    def __init__(self, email: str) -> None:
        super().__init__(f"A customer with email '{email}' already exists")
        self.email = email


class CustomerNotFoundError(DomainError):
    def __init__(self, customer_id: int) -> None:
        super().__init__(f"Customer {customer_id} not found")
        self.customer_id = customer_id
