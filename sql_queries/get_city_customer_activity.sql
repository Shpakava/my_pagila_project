SELECT ct.city,
       SUM(CASE WHEN c.active = 1 THEN 1 ELSE 0 END) AS active_customers,
       SUM(CASE WHEN c.active = 0 THEN 1 ELSE 0 END) AS inactive_customers
FROM city ct JOIN address a ON ct.city_id = a.city_id
             JOIN customer c ON a.address_id = c.address_id
GROUP BY ct.city
ORDER BY inactive_customers DESC;