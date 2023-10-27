import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

# Connect to the Sakila database
engine = create_engine('mysql://root:Chip3548@localhost/sakila')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Sakila Rental Data Over Time"),
    
    # Dropdown to select a category
    dcc.Dropdown(
        id='query-dropdown',
        options=[
            {'label': 'Query 1', 'value': 1},
            {'label': 'Query 2', 'value': 2},
            {'label': 'Query 3', 'value': 3},
            {'label': 'Query 4', 'value': 4},
            {'label': 'Query 5', 'value': 5}
            # Add more options based on your data
        ],
        value=1  # Default selected option
    ),
    
    # Line chart to display data over time
    dcc.Graph(id='line-chart')
])

# Define callback to update the line chart based on the selected category
@app.callback(
    Output('line-chart', 'figure'),
    [Input('query-dropdown', 'value')]
)
def update_line_chart(selected_query):
    # SQL query to retrieve data for the selected category over time
    query = f"""
    SELECT DATE(rental_date) AS rental_day, COUNT(rental_id) AS rental_count
    FROM rental, inventory, film, film_category
    WHERE rental.inventory_id = inventory.inventory_id AND
    inventory.film_id = film.film_id AND
    film.film_id = film_category.film_id AND
    category_id = {selected_query}
    GROUP BY rental_day;
    """
    query2 = """
    SELECT f.film_id, f.title, COUNT(r.rental_id) AS rental_count,
    f.rental_rate * COUNT(r.rental_id) AS revenue
    FROM film f
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY f.film_id, f.title -- we must put these tables in the select command
    ORDER BY revenue DESC
    LIMIT 5;
    """
    query3 = """
    SELECT a.first_name, a.last_name,
    COUNT(fa.film_id) AS film_count
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    GROUP BY a.actor_id
    HAVING COUNT(fa.film_id) > 15
    LIMIT 20;

    """
    query4 = """
    WITH CategoryAvgLength AS (
    SELECT c.name AS category_name,
    AVG(f.length) AS avg_length
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    GROUP BY c.name),
    OverallAvgLength AS (
    SELECT AVG(length) AS overall_avg_length
    FROM film)
    SELECT c.category_name, c.avg_length, o.overall_avg_length
    FROM CategoryAvgLength c
    JOIN OverallAvgLength o ON 1 = 1
    WHERE c.avg_length > o.overall_avg_length;
    """
    query5 = """
    SELECT DATE(rental_date) AS rental_day, COUNT(rental_id) AS rental_count
    FROM rental
    GROUP BY rental_day;
    """

    rental_data = pd.read_sql(query, engine)
    query_data2 = pd.read_sql(query2, engine)
    query_data3 = pd.read_sql(query3, engine)
    query_data4 = pd.read_sql(query4, engine)
    query_data5 = pd.read_sql(query5, engine)

    # Create the line chart
    fig = {
        'data': [
            {
                'x': rental_data['rental_day'],
                'y': rental_data['rental_count'],
                'type': 'bar',
                'marker': {'color': 'blue'}
            }
        ],
        'layout': {
            'title': f'Rental Count for Category {selected_query}',
            'xaxis': {'title': 'Rental Day'},
            'yaxis': {'title': 'Rental Count'}
        }
    }

    fig2 = {
        'data': [
            {
                'x': query_data2['title'],
                'y': query_data2['revenue'],
                'type': 'bar',
                'marker': {'color': 'pink'}
            }
        ],
        'layout': {
            'title': f'Revenue by Movie',
            'xaxis': {'title': 'Film Name'},
            'yaxis': {'title': 'Revenue'}
        }
    }

    fig3 = {
        'data': [
            {
                'x': query_data3['first_name'] + ' ' + query_data3['last_name'],
                'y': query_data3['film_count'],
                'type': 'bar',
                'marker': {'color': 'purple'}
            }
        ],
        'layout': {
            'title': f'Movie features by actor',
            'xaxis': {'title': 'Actor Name'},
            'yaxis': {'title': 'Film Count'}
        }
    }
    fig4 = {
        'data': [
            {
                'x': query_data4['category_name'],
                'y': query_data4['avg_length'],
                'type': 'bar',
                'marker': {'color': 'pink'}
            }
        ],
        'layout': {
            'title': f'Average film length by category',
            'xaxis': {'title': 'Category'},
            'yaxis': {'title': 'Average Film Length'}
        }
    }
    fig5 = {
        'data': [
            {
                'x': query_data5['rental_day'],
                'y': query_data5['rental_count'],
                'type': 'line',
                'marker': {'color': 'pink'}
            }
        ],
        'layout': {
            'title': f'Rental Count Over Time',
            'xaxis': {'title': 'Rental Day'},
            'yaxis': {'title': 'Rental Count'}
        }
    }
    if selected_query == 1:
        return fig
    elif selected_query == 2:
        return fig2
    elif selected_query == 3:
        return fig3
    elif selected_query == 4:
        return fig4
    elif selected_query == 5:
        return fig5

if __name__ == '__main__':
    app.run_server(debug=True)
