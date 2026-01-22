CREATE OR REPLACE VIEW top_5_most_sellable_products_last_month AS
WITH RECURSIVE category_path AS (
    SELECT c.id AS category_id, c.parent_id, c.id AS current_id, c.name AS current_name
    FROM categories c

    UNION ALL

    SELECT cp.category_id, p.parent_id, p.id AS current_id, p.name AS current_name
    FROM category_path cp
    JOIN categories p ON p.id = cp.parent_id
),
category_root AS (
    SELECT category_id, current_id AS root_id, current_name AS root_name
    FROM category_path
    WHERE parent_id IS NULL
),
sales_last_month AS (
    SELECT oi.product_id, SUM(oi.qty) AS total_qty_sold
    FROM order_items oi
    JOIN orders o ON o.id = oi.order_id
    WHERE o.created_at >= NOW() - INTERVAL '1 month'
    GROUP BY oi.product_id
)
SELECT p.name AS product_name, cr.root_name AS level_1_category, s.total_qty_sold
FROM sales_last_month s
JOIN products p ON p.id = s.product_id
JOIN category_root cr ON cr.category_id = p.category_id
ORDER BY s.total_qty_sold DESC, p.name
LIMIT 5;
