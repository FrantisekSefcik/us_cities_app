import psycopg2
import os


class DbClient:

    def __init__(self):
        # Init connection and create table, drop the table if any exist before.
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS cities;")
        cur.execute("CREATE TABLE cities ("
                    "state VARCHAR ( 255 ) NOT NULL, "
                    "country VARCHAR ( 255 ) NOT NULL, "
                    "city VARCHAR ( 255 ) NOT NULL);")
        self.conn.commit()
        cur.close()

    def truncate_table(self, table_name: str):
        cur = self.conn.cursor()
        cur.execute(f"TRUNCATE TABLE {table_name};")
        cur.close()

    def save_cities(self, cities):
        cur = self.conn.cursor()
        sql_query = "INSERT INTO cities VALUES (%s, %s, %s);"
        for row_values in cities:
            cur.execute(sql_query, row_values)
        self.conn.commit()
        cur.close()

    def get_all_cities(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cities;")
        result = cur.fetchall()
        cur.close()
        return result

    def get_cities_by_state(self, state: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cities WHERE state=%s;", (state,))
        result = cur.fetchall()
        cur.close()
        return result

    def get_cities_by_country(self, country: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cities WHERE country=%s;", (country,))
        return cur.fetchall()

    def get_cities_by_city(self, city: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cities WHERE city=%s;", (city,))
        result = cur.fetchall()
        cur.close()
        return result

