from typing import Any, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException


class BaseError(BaseModel):
    detail: Any
    user_message: str
    type: Optional[str] = Field("BaseError", description="Exception class name")


class AppHTTPException(HTTPException):
    http_code: int = 400
    detail: Any = "Error occurred"
    user_message: str = "Unexpected error"
    type: str = "AppHTTPException"

    def __init__(self, detail: Any | None = None):
        super().__init__(
            status_code=self.http_code,
            detail={
                "type": self.type,
                "message": self.user_message,
                "detail": detail if detail is not None else self.detail,
            },
        )
