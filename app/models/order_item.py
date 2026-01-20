from sqlalchemy import ForeignKey, UniqueConstraint, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_items_order_product"),
        CheckConstraint("qty > 0", name="ck_order_items_qty_pos"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    qty: Mapped[int] = mapped_column(nullable=False)
    unit_price_at_order: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
