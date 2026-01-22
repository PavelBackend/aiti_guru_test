SELECT c.name, COALESCE(SUM(oi.unit_price_at_order * oi.qty), 0) AS total_sum
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name;