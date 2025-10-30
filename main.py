import psycopg2
import os

db_name = "postgres"
db_user = "postgres"
db_password = "postgres666"
db_host = "localhost"
db_port = "5432"

"""Загрузка SQL-запроса из файла"""
def load_sql_query(file_path):
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

"""Установка соединения с базой данных"""
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn
    except psycopg2.Error as e:
        print(f"Connection error: {e}")
        return None

"""Выполнение SQL-запроса"""
def execute_query(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    except psycopg2.Error as e:
        print(f"Query execution error: {e}")
        return None

def main():
    conn = connect_to_db()
    if conn:
        query_film_counts = load_sql_query("sql_queries/get_category_film_counts.sql")
        if query_film_counts:
            results1 = execute_query(conn, query_film_counts)
            if results1:
                print("The number of films in each category, sorted in descending order:")
                for row in results1:
                    category, count = row
                    print(f"{category}: {count}")

        print("\n" + "-"*50 + "\n")

        query_top_actors_rentals_path = "sql_queries/get_top_actors_by_rentals.sql"
        query_top_actors_rentals_sql = load_sql_query(query_top_actors_rentals_path)
        if query_top_actors_rentals_sql:
            results_top_actors_rentals = execute_query(conn, query_top_actors_rentals_sql)
            if results_top_actors_rentals:
                print("The top 10 actors whose films were rented the most, sorted in descending order:")
                for row in results_top_actors_rentals:
                    first_name, last_name, rental_count = row
                    print(f"{first_name} {last_name}: {rental_count} rentals")

        print("\n" + "-" * 50 + "\n")

        query_top_revenue_category_path = "sql_queries/get_top_revenue_category.sql"
        query_top_revenue_category_sql = load_sql_query(query_top_revenue_category_path)
        if query_top_revenue_category_sql:
            results_top_revenue_category = execute_query(conn, query_top_revenue_category_sql)
            if results_top_revenue_category:
                print("The category of films that generated the highest revenue:")
                for row in results_top_revenue_category:
                    category, total_revenue = row
                    print(f"Category: {category} - Revenue: {total_revenue}")

        print("\n" + "-" * 50 + "\n")

        query_films_not_in_inventory_path = "sql_queries/get_films_not_in_inventory.sql"
        query_films_not_in_inventory_sql = load_sql_query(query_films_not_in_inventory_path)
        if query_films_not_in_inventory_sql:
            results_films_not_in_inventory = execute_query(conn, query_films_not_in_inventory_sql)
            if results_films_not_in_inventory:
                print("The titles of films not present in the inventory:")
                for row in results_films_not_in_inventory:
                    film_title = row[0]
                    print(f"{film_title}")

        print("\n" + "-" * 50 + "\n")

        query_top_children_actors_path = "sql_queries/get_top_actors_in_children_category.sql"
        query_top_children_actors_sql = load_sql_query(query_top_children_actors_path)
        if query_top_children_actors_sql:
            results_top_children_actors = execute_query(conn, query_top_children_actors_sql)
            if results_top_children_actors:
                print("The top 3 actors who appeared the most in films within the 'Children' category:")
                for row in results_top_children_actors:
                    first_name, last_name, rental_count = row  # rental_count здесь - это children_film_count
                    print(f"{first_name} {last_name}: {rental_count}")

        print("\n" + "-" * 50 + "\n")

        query_city_customer_activity_path = "sql_queries/get_city_customer_activity.sql"
        query_city_customer_activity_sql = load_sql_query(query_city_customer_activity_path)
        if query_city_customer_activity_sql:
            results_city_customer_activity = execute_query(conn, query_city_customer_activity_sql)
            if results_city_customer_activity:
                print("Cities with the count of active and inactive customers:")
                for row in results_city_customer_activity:
                    city, active_count, inactive_count = row
                    print(f"City: {city}: active - {active_count}, inactive- {inactive_count}")

        print("\n" + "-" * 50 + "\n")

        query_category_rental_duration_path = "sql_queries/get_category_rental_duration_by_city.sql"
        query_category_rental_duration_sql = load_sql_query(query_category_rental_duration_path)
        if query_category_rental_duration_sql:
            results_category_rental_duration = execute_query(conn, query_category_rental_duration_sql)
            if results_category_rental_duration:
                print("The film category with the highest total rental hours in cities where customer.address_id belongs to that city and starts with the letter 'a', containing the symbol '-':")
                for row in results_category_rental_duration:
                    category_name, total_hours = row
                    print(f"Category: {category_name}, Rental hours: {total_hours}")
    conn.close()

if __name__ == "__main__":
    main()