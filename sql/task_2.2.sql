SELECT cp.name, COUNT(cc.id) as children_count
FROM categories cp
LEFT JOIN categories cc ON cp.id = cc.parent_id
GROUP BY cp.id, cp.name;