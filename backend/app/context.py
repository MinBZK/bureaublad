from contextvars import ContextVar

# Async-safe context variable for storing request ID
# This allows all loggers to access the current request's ID
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """
    Get the current request ID from context.
    """
    return request_id_var.get()


def set_request_id(request_id: str) -> None:
    """
    Set the request ID in context.
    """
    request_id_var.set(request_id)
