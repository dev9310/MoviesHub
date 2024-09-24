import sqlite3
import pandas as pd
def get_db_connection():
    conn = sqlite3.connect('data.db')  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # To access rows as dictionaries
    return conn

def fetch_movie(n=30):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM 'movies' WHERE Time=2024 LIMIT {n}", conn)
    conn.close()
    data = df.to_dict(orient='records')
    return data

# ORDER BY RANDOM()

def count_movies():
    
    conn = get_db_connection()
    query = f"SELECT COUNT(*) AS total_movies FROM 'movies'"
    result = pd.read_sql(query, conn)
    conn.close()
    return result['total_movies'][0]