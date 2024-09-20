import sqlite3
import pandas as pd
def get_db_connection():
    conn = sqlite3.connect('data.db')  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # To access rows as dictionaries
    return conn

def fetch_movie(n=30):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM 'movies' WHERE Time=2024 ORDER BY RANDOM() LIMIT {n}", conn)
    conn.close()
    data = df.to_dict(orient='records')
    return data

