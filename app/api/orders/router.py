from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.resources.schemas.error import ErrorResponse
from app.api.orders.resources.schemas.order_item import AddItemRequest
from app.api.orders.resources.services.order_service import OrderService
from app.db.session import get_session

router = APIRouter()


@cbv(router)
class OrderRouter:
    # prefix: /orders
    session: AsyncSession = Depends(get_session)

    @router.post(
        '/{order_id}/items',
        name='Add Item to Order',
        description='Добавление товара в заказ',
        responses={
            404: {
                "model": ErrorResponse,
                "description": "Order or product not found",
            },
            409: {
                "model": ErrorResponse,
                "description": "Not enough stock",
            },
            400: {
                "model": ErrorResponse,
                "description": "Validation or business error",
            },
        },
        include_in_schema=True,
    )
    async def add_item_to_order(self, order_id: int, order_data: AddItemRequest):
        service = OrderService(self.session)

        await service.add_item_to_order(order_id=order_id, order_data=order_data)
