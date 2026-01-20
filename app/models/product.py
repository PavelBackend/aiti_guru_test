from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("stock_qty >= 0", name="ck_products_stock_nonneg"),
        CheckConstraint("price >= 0", name="ck_products_price_nonneg"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    stock_qty: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category = relationship("Category")
