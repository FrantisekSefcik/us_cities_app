import csv
import io
from typing import List, Tuple

from flask import Flask, render_template, request, url_for, redirect

from db_client import DbClient

# initialize flask app
app = Flask(__name__)
# initialize db client
db_client = DbClient()


def process_csv_file(csv_file) -> List[Tuple[str, str, str]]:
    stream = io.StringIO(csv_file.stream.read().decode("UTF-8"), newline=None)
    reader = csv.DictReader(stream)
    return [(row['state_name'], row['county_name'], row['city_ascii']) for row in reader]


def process_rows_into_tree_structure(rows: List[Tuple[str, str, str]]) -> dict:
    tree_structure = {}
    for (state, country, city) in rows:
        if tree_structure.get(state) is None:
            tree_structure[state] = {}
        if tree_structure[state].get(country) is None:
            tree_structure[state][country] = {}
        tree_structure[state][country][city] = city
    return tree_structure


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload_csv", methods=['POST'])
def upload_csv():
    f = request.files.get('file')
    # Truncate table before new entries are saved.
    db_client.truncate_table('cities')
    # Process csv file into array of values.
    cities_rows = process_csv_file(f)
    # Save values into table.
    db_client.save_cities(cities_rows)
    return redirect(url_for('cities'))


@app.route("/cities", methods=['GET'])
def cities():
    search_value = request.args.get('searchValue')
    search_type = request.args.get('type')

    # Apply search if there is any defined by request arguments
    if search_type == 'state':
        rows = db_client.get_cities_by_state(search_value)
    elif search_type == 'country':
        rows = db_client.get_cities_by_country(search_value)
    elif search_type == 'city':
        rows = db_client.get_cities_by_city(search_value)
    else:
        rows = db_client.get_all_cities()

    # Process rows into tree structure
    cities_tree = process_rows_into_tree_structure(rows)

    return render_template(
        'cities.html',
        cities_tree=cities_tree
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
