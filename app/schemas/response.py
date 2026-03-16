from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Consistent response envelope used by every endpoint."""

    success: bool = True
    data: T
    message: str = ""
