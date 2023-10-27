from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'username' and 'password' with your MySQL username and password
engine = create_engine('mysql://root:Chip3548@localhost/sakila')


query1 = """
SELECT c.name AS category, COUNT(r.rental_id) AS rental_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY category;
"""

# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query1, engine)

print(rental_data.columns)


# Set the figure size
plt.figure(figsize=(10, 6))

# Create a bar chart
plt.bar(rental_data['category'], rental_data['rental_count']) 

# Customize the chart
plt.title('Number of Rentals by Category')
plt.xlabel('Category')
plt.ylabel('Rental Count')
plt.xticks(rotation=45)  # Rotate category labels for readability

# Display the chart
plt.tight_layout()
plt.show()

#NOW moving on to query2

query2 = """
SELECT DATE(rental_date) AS rental_day, COUNT(rental_id) AS rental_count
FROM rental
GROUP BY rental_day;
""" #declaring a string in many lines

# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query2, engine)

# Set the figure size
plt.figure(figsize=(12, 6))

# Create a time-series line chart
plt.plot(rental_data['rental_day'], rental_data['rental_count'], marker='o', linestyle='-')

# Customize the chart
plt.title('Rental Count Over Time')
plt.xlabel('Rental Day')
plt.ylabel('Rental Count')
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Display the chart
plt.tight_layout()
plt.show()

query3 = """
SELECT f.film_id, f.title, COUNT(r.rental_id) AS rental_count,
f.rental_rate * COUNT(r.rental_id) AS revenue
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title -- we must put these tables in the select command
ORDER BY revenue DESC
LIMIT 5;
"""

# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query3, engine)
print(rental_data.columns)

# Set the figure size
plt.figure(figsize=(10, 6))


# Create a bar chart
plt.bar(rental_data['title'], rental_data['revenue']) 

# Customize the chart
plt.title('Revenue by Movie')
plt.xlabel('Film Name')
plt.ylabel('Revenue')
plt.xticks(rotation=45)  # Rotate category labels for readability

# Display the chart
plt.tight_layout()
plt.show()

query4 = """
SELECT
    a.first_name,
    a.last_name,
    COUNT(fa.film_id) AS film_count
FROM
    actor a
JOIN
    film_actor fa ON a.actor_id = fa.actor_id
GROUP BY
    a.actor_id
HAVING
    COUNT(fa.film_id) > 15
LIMIT 20;

"""
# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query4, engine)

# Set the figure size
plt.figure(figsize=(10, 6))


# Create a bar chart
plt.bar(rental_data['first_name'] + ' ' + rental_data['last_name'], rental_data['film_count'])

# Customize the chart
plt.title('Movie features by actor')
plt.xlabel('Actor Name')
plt.ylabel('Film Count')
plt.xticks(rotation=45)  # Rotate category labels for readability

# Display the chart
plt.tight_layout()
plt.show()

query5 = """
WITH CategoryAvgLength AS (
    SELECT
        c.name AS category_name,
        AVG(f.length) AS avg_length
    FROM
        film f
    JOIN
        film_category fc ON f.film_id = fc.film_id
    JOIN
        category c ON fc.category_id = c.category_id
    GROUP BY
        c.name
),
OverallAvgLength AS (
    SELECT
        AVG(length) AS overall_avg_length
    FROM
        film
)
SELECT
    c.category_name,
    c.avg_length,
    o.overall_avg_length
FROM
    CategoryAvgLength c
JOIN
    OverallAvgLength o ON 1 = 1
WHERE
    c.avg_length > o.overall_avg_length;

"""
# Execute the SQL query and load the results into a pandas DataFrame
rental_data = pd.read_sql(query5, engine)

# Set the figure size
plt.figure(figsize=(10, 6))


# Create a bar chart
plt.bar(rental_data['category_name'], rental_data['avg_length'])

# Customize the chart
plt.title('Average film length by category')
plt.xlabel('Category')
plt.ylabel('Average Film Length')
plt.xticks(rotation=45)  # Rotate category labels for readability

# Display the chart
plt.tight_layout()
plt.show()