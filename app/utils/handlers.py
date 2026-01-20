import traceback
import uuid
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger as log
from starlette.concurrency import iterate_in_threadpool
from app.schemas.base import AppHTTPException, BaseError
from app.utils.contextvars import request_ip_contextvar, endpoint_name_contextvar
from asgi_correlation_id.context import correlation_id
from config import settings


async def request_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    endpoint_name = request.scope.get("path").replace("/", "")
    request_ip = request.client.host

    request_ip_contextvar.set(request_ip)
    endpoint_name_contextvar.set(endpoint_name)

    extra = {'request_id': request_id, 'request_ip': request_ip, 'ip': request_ip}
    log.configure(extra=extra)

    # ! ----------------------------------------------------------------------------------------------------------------
    response = await call_next(request)
    # ! ----------------------------------------------------------------------------------------------------------------

    response.headers["X-Request-ID"] = request_id
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    request_info = (
        f"({request_ip_contextvar.get()}) Request: [{request.method}] "
        f"-> {request.url} >>> {request.headers} <<<"
    )
    log.info(f"{request_info} Server response: {(b''.join(response_body)).decode()}")
    return response


async def error_exception_handler(request: Request, exc: Exception):
    exception_info = (
        f"({request_ip_contextvar.get()}) Request: [{request.method}] "
        f"-> {request.url} >>> {request.headers} <<<"
    )
    corr_id = str(correlation_id.get()) if correlation_id.get() else "No-correlation-id"
    content = BaseError(
            detail=f"[{request.method}] -> {request.url}: {repr(exc)} ({corr_id})",
            user_message="Unexpected error",
            type="InternalServerError"
    ).model_dump()
    log.error(f"{exception_info} Server response: {content} <<< Exception: {repr(exc)}\n{traceback.format_exc()}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content
    )

sensitive_header = ["Authorization", "Secret"]


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    _headers = request.headers.mutablecopy()
    for key in sensitive_header:
        del _headers[key]

    exception_info = f"({request_ip_contextvar.get()}) Request: [{request.method}] -> {request.url} >>> {_headers} <<<"
    corr_id = str(correlation_id.get()) if correlation_id.get() else "No-correlation-id"
    content = BaseError(
            detail=jsonable_encoder(exc.errors()),
            user_message=f"RequestValidationError ({corr_id}). Details: " 
                         f"{exception_info if settings.ADD_VALIDATION_ERRORS_TO_RESPONSES else 'N/A'}",
            type="ValidationError"
    ).model_dump()
    log.error(f"{exception_info} Server response {content} <<< Exception: {repr(exc)}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content
    )


async def app_error_handler(request: Request, exc: AppHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content=BaseError(
            detail=exc.detail,
            user_message=exc.user_message,
            type=exc.type
        ).model_dump()
    )
