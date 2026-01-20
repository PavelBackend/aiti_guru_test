from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from app.api.orders.router import router as orders_router
from app.schemas.base import AppHTTPException
from app.utils.handlers import app_error_handler, error_exception_handler, request_middleware, validation_exception_handler
from app.utils.logging import configure_logging, log_json
from asgi_correlation_id import CorrelationIdMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Aiti Guru Test",
    version="1.0.0",
    description="API for Aiti Guru Test project",
    dependencies=[Depends(log_json)],
)

app.add_event_handler("startup", lambda: configure_logging(app))
app.add_exception_handler(Exception, handler=error_exception_handler)
app.add_exception_handler(RequestValidationError, handler=validation_exception_handler)
app.add_exception_handler(AppHTTPException, handler=app_error_handler)
app.add_middleware(BaseHTTPMiddleware, dispatch=request_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
)

app.include_router(orders_router)
