import contextvars

request_ip_contextvar = contextvars.ContextVar("request_ip", default="")
endpoint_name_contextvar = contextvars.ContextVar("endpoint_name", default="")
