from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.resources.exceptions import (
    NotEnoughStock,
    OrderNotFound,
    ProductNotFound,
)


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_item(self, order_id: int, product_id: int, qty: int) -> int:
        """
        Добавляет товар в заказ.
        Если позиция уже есть — увеличивает qty.
        Если товара не хватает — кидает NotEnoughStock.
        Возвращает итоговое количество товара в заказе (new_qty).
        """
        order_exists = await self.session.execute(
            text("SELECT 1 FROM orders WHERE id = :order_id"),
            {"order_id": order_id},
        )
        if order_exists.scalar_one_or_none() is None:
            raise OrderNotFound

        prod_row = await self.session.execute(
            text(
                """
                SELECT id, stock_qty, price
                FROM products
                WHERE id = :product_id
                FOR UPDATE
                """
            ),
            {"product_id": product_id},
        )
        prod = prod_row.mappings().one_or_none()
        if prod is None:
            raise ProductNotFound

        if int(prod["stock_qty"]) < qty:
            raise NotEnoughStock

        upsert_res = await self.session.execute(
            text(
                """
                INSERT INTO order_items (order_id, product_id, qty, unit_price_at_order)
                VALUES (:order_id, :product_id, :qty, :price)
                ON CONFLICT (order_id, product_id)
                DO UPDATE SET qty = order_items.qty + EXCLUDED.qty
                RETURNING qty
                """
            ),
            {
                "order_id": order_id,
                "product_id": product_id,
                "qty": qty,
                "price": prod["price"],
            },
        )
        new_qty = upsert_res.scalar_one()

        await self.session.execute(
            text(
                """
                UPDATE products
                SET stock_qty = stock_qty - :qty
                WHERE id = :product_id
                """
            ),
            {"qty": qty, "product_id": product_id},
        )

        return int(new_qty)
