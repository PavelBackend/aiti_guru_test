from fastapi import APIRouter
# from st_bases.tools.openapi import simplify_operation_ids

from app.api.orders.router import router as orders_router

main_router = APIRouter()

main_router.include_router(orders_router, tags=["Orders"], prefix="/orders")

# simplify_operation_ids(main_router)
