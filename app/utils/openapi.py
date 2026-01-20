from fastapi import APIRouter
from fastapi.routing import APIRoute


def simplify_operation_ids(main_router: APIRouter) -> None:
    """
    Simplify operation IDs so that generated clients have simpler api function names
    """
    for route in main_router.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.endpoint.__name__
