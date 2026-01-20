from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    type: str
    message: str
    detail: Any
