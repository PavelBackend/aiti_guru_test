import os
import sys
from copy import deepcopy
from fastapi import Request
from loguru import logger
from config import settings


async def log_json(request: Request):
    main_info = f"Request: [{request.method}] -> {request.url} >>> {request.headers} <<<"

    try:
        request_json = deepcopy(await request.json())
        logger.info(f"{main_info} {request_json}")
    except:
        logger.info(f"{main_info} {request.path_params}")


def configure_logging(app):
    logging_level = "DEBUG" if settings.MODE == "DEV" else "INFO"
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[request_ip]} | {extra[request_id]} | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"

    if getattr(app.state, "log_sinks", None):
        return

    worker_n = os.getpid() % settings.NUM_WORKERS + 1

    logger.remove()

    sinks = []

    sinks.append(
        logger.add(
            f"/app/logs/{{time:YYYY_MM_DD}}__worker_{worker_n}.log",
            level=logging_level,
            format=fmt,
            rotation="00:00" if settings.LOG_ROTATION else None,
            enqueue=settings.LOG_ENQUEUE,
        )
    )

    if settings.LOGGER_STDOUT:
        sinks.append(
            logger.add(sys.stdout, colorize=True, level=logging_level, format=fmt)
        )

    if settings.LOGGER_SERIALIZE:
        sinks.append(
            logger.add(
                f"/app/logs/{{time:YYYY_MM_DD}}__worker_{worker_n}.jsonl",
                level=logging_level,
                serialize=True,
                rotation="00:00" if settings.LOG_ROTATION else None,
                enqueue=settings.LOG_ENQUEUE,
            )
        )

    logger.configure(extra={"request_ip": "INTERNAL", "request_id": "INTERNAL"})

    app.state.log_sinks = sinks
