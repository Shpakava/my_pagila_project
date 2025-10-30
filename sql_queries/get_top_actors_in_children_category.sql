WITH ActorsInChildren AS (
    SELECT a.actor_id, a.first_name, a.last_name,
            COUNT(fa.film_id) AS children_film_count,
            RANK() OVER (ORDER BY COUNT(fa.film_id) DESC) as rnk
    FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id
                 JOIN film_category fc ON fa.film_id = fc.film_id
                 JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = 'Children'
    GROUP BY a.actor_id, a.first_name, a.last_name)

SELECT first_name, last_name, children_film_count
FROM ActorsInChildren
WHERE rnk <= 3
ORDER BY rnk;