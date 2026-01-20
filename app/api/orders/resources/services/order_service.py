from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.resources.crud.order_repo import OrderRepo
from app.api.orders.resources.schemas.order_item import AddItemRequest


class OrderService:
    def __init__(self, session: AsyncSession):
        self.repo = OrderRepo(session)

    async def add_item_to_order(self, order_id: int, order_data: AddItemRequest):
        async with self.repo.session.begin():
            await self.repo.add_item(
                order_id=order_id, product_id=order_data.product_id, qty=order_data.qty
            )
        return {"ok": True}
