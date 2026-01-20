"""seed test data

Revision ID: 0e6e3da3d653
Revises: c1dbf3e59f45
Create Date: 2026-01-20 17:57:40.166314

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0e6e3da3d653'
down_revision: Union[str, Sequence[str], None] = 'c1dbf3e59f45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO categories (id, name, parent_id) VALUES
        (1, 'Электроника', NULL),
        (2, 'Телефоны', 1),
        (3, 'Ноутбуки', 1),
        (4, 'Аксессуары', 1),
        (5, 'Android', 2),
        (6, 'iPhone', 2);
        """
    )

    op.execute(
        """
        INSERT INTO products (id, name, stock_qty, price, category_id) VALUES
        (1, 'iPhone 15', 10, 120000, 6),
        (2, 'Samsung Galaxy S23', 15, 90000, 5),
        (3, 'MacBook Air M2', 5, 150000, 3),
        (4, 'Lenovo ThinkPad', 7, 110000, 3),
        (5, 'Наушники Sony', 20, 15000, 4);
        """
    )

    op.execute(
        """
        INSERT INTO clients (id, name, address) VALUES
        (1, 'ООО Ромашка', 'Москва, ул. Ленина, 1'),
        (2, 'ИП Иванов', 'Санкт-Петербург, Невский пр., 10'),
        (3, 'ЗАО ТехноМир', 'Казань, ул. Баумана, 5');
        """
    )

    op.execute(
        """
        INSERT INTO orders (id, client_id, created_at) VALUES
        (1, 1, NOW() - INTERVAL '10 days'),
        (2, 1, NOW() - INTERVAL '40 days'),
        (3, 2, NOW() - INTERVAL '5 days'),
        (4, 3, NOW() - INTERVAL '2 days');
        """
    )

    op.execute(
        """
        INSERT INTO order_items (order_id, product_id, qty, unit_price_at_order) VALUES
        (1, 1, 2, 120000),
        (1, 5, 3, 15000),

        (2, 2, 1, 90000),
        (2, 3, 1, 150000),

        (3, 2, 2, 90000),
        (3, 5, 1, 15000),

        (4, 3, 1, 150000),
        (4, 4, 2, 110000);
        """
    )

    op.execute(
        """
        SELECT setval(pg_get_serial_sequence('categories', 'id'), (SELECT MAX(id) FROM categories));
        SELECT setval(pg_get_serial_sequence('products', 'id'), (SELECT MAX(id) FROM products));
        SELECT setval(pg_get_serial_sequence('clients', 'id'), (SELECT MAX(id) FROM clients));
        SELECT setval(pg_get_serial_sequence('orders', 'id'), (SELECT MAX(id) FROM orders));
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM order_items;")
    op.execute("DELETE FROM orders;")
    op.execute("DELETE FROM products;")
    op.execute("DELETE FROM categories;")
    op.execute("DELETE FROM clients;")
