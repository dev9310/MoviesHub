import sqlite3
import pandas as pd

class Db_Manager:
    
    def __init__(self):
        self.total_movies = 0 
        self.conn = None
        self.count_movies()
        self.total_pages = self.total_movies//30 
    
    def get_db_connection(self):
        # Set check_same_thread=False to allow usage across threads
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
    def fetch_movie(self, n=30):
        if self.conn is None:
            self.get_db_connection()
        
        # Fetch movies with a limit
        df = pd.read_sql(f"SELECT * FROM 'movies' WHERE Time = 2024 LIMIT {n}", self.conn)
        data = df.to_dict(orient='records')
        return data

    def fetch_by_page_no(self, pg_no=1):
        if self.conn is None:
            self.get_db_connection()
        
        # Adjust LIMIT and OFFSET for pagination
        offset = (pg_no - 1) * 30  # Calculate the offset based on the page number
        query = f"SELECT * FROM 'movies' LIMIT 30 OFFSET {offset}"
        
        df = pd.read_sql(query, self.conn)
        data = df.to_dict(orient='records')
        return data

    def fetch_by_id(self, id):
        if self.conn is None:
            self.get_db_connection()

        query = f"SELECT * FROM `movies` WHERE `Id` = {id}"
        df = pd.read_sql(query, self.conn)

        # Return the first record as a dictionary if it exists
        if not df.empty:
            return df.iloc[0].to_dict()  # Return the first record as a dict
        return {}


    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
                
    def count_movies(self):
        if self.conn == None:
            self.get_db_connection()
            
        query = f"SELECT COUNT(*) AS total_movies FROM 'movies'"
        result = pd.read_sql(query,self.conn)
        self.total_movies = result['total_movies'][0]     
        
    
