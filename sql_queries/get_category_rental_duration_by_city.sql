WITH CityFiltered AS (
    SELECT city_id, city
    FROM city
    WHERE city LIKE 'A%' AND city LIKE 'a%'

    UNION ALL

    SELECT city_id, city
    FROM city
    WHERE city LIKE '%-%'),

    RentalDurationByCategory AS (
    SELECT c.name AS category_name,
           SUM(f.length) AS total_rental_duration_minutes,
           SUM(f.length) / 60.0 AS total_rental_duration_hours
    FROM category c JOIN film_category fc ON c.category_id = fc.category_id
                    JOIN film f ON fc.film_id = f.film_id
                    JOIN inventory i ON f.film_id = i.film_id
                    JOIN rental r ON i.inventory_id = r.inventory_id
    WHERE c.category_id IN (SELECT category_id FROM film_category)
    GROUP BY c.name),

    CustomerAddressesInFilteredCities AS (
    SELECT a.address_id
    FROM address a JOIN CityFiltered cf ON a.city_id = cf.city_id),

    RentalsFromFilteredCustomers AS (
    SELECT r.rental_id, r.inventory_id
    FROM rental r JOIN CustomerAddressesInFilteredCities ca ON r.customer_id = ca.address_id),

    CorrectRentalsFromFilteredCustomers AS (
    SELECT r.rental_id, r.inventory_id
    FROM rental r JOIN customer c ON r.customer_id = c.customer_id
                  JOIN address a ON c.address_id = a.address_id
                  JOIN CityFiltered cf ON a.city_id = cf.city_id),

    RentalDurationByCategoryInFilteredCities AS (
    SELECT c.name AS category_name,
           SUM(f.length) AS total_rental_duration_minutes,
           SUM(f.length) / 60.0 AS total_rental_duration_hours
    FROM category c JOIN film_category fc ON c.category_id = fc.category_id
                    JOIN film f ON fc.film_id = f.film_id
                    JOIN inventory i ON f.film_id = i.film_id
                    JOIN CorrectRentalsFromFilteredCustomers r ON i.inventory_id = r.inventory_id
    GROUP BY c.name)

SELECT category_name, total_rental_duration_hours
FROM RentalDurationByCategoryInFilteredCities
ORDER BY total_rental_duration_hours DESC
LIMIT 1;