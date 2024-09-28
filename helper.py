import sqlite3
import pandas as pd
import ast
import pycountry


class Db_Manager:
    
    def __init__(self):
        self.conn = None
        self.get_db_connection()  # Ensure the database connection is established
        self.total_movies = self.count_movies()
        self.total_pages = self.total_movies // 30
        self.unique_genre_ = self.genreList_extractor()
        self.unique_country_ = self.countryList_extractor()
        self.unique_production_ = self.productionList_extractor()

    def get_db_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect('movies.db', check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def count_movies(self):
        query = "SELECT COUNT(*) AS total_movies FROM 'movies'"
        result = pd.read_sql(query, self.conn)
        return result['total_movies'][0]
    
    def fetch_movie(self, n=30):
        query = f"SELECT * FROM 'movies' WHERE Time = 2024 LIMIT {n}"
        df = pd.read_sql(query, self.conn)
        return df.to_dict(orient='records')
    
    def fetch_by_page_no(self, pg_no=1, genre='all'):
        offset = (pg_no - 1) * 30  # Calculate offset for pagination

        if genre == 'all':
            query = f"SELECT * FROM 'movies' LIMIT 30 OFFSET {offset}"
            total_movies_query = "SELECT COUNT(*) AS total_movies FROM 'movies'"
        else:
            query = f"SELECT * FROM 'movies' WHERE Genre LIKE ? LIMIT 30 OFFSET {offset}"
            total_movies_query = f"SELECT COUNT(*) AS total_movies FROM 'movies' WHERE Genre LIKE ?"
        
        # Fetch the total number of movies
        if genre == 'all':
            total_movies_df = pd.read_sql(total_movies_query, self.conn)
            df = pd.read_sql(query, self.conn)
        else:
            total_movies_df = pd.read_sql(total_movies_query, self.conn, params=(f"%{genre}%",))
            df = pd.read_sql(query, self.conn, params=(f"%{genre}%",))

        total_movies = total_movies_df['total_movies'][0]
        total_pages = total_movies // 30 + (1 if total_movies % 30 else 0)

        return df.to_dict(orient='records'), total_pages

    def fetch_by_id(self, id):
        query = f"SELECT * FROM `movies` WHERE `Id` = {id}"
        df = pd.read_sql(query, self.conn)

        if df.empty:
            return {}

        df_dict = df.iloc[0].to_dict()

        return {
            'id': df_dict['Id'],
            'title': df_dict['Title'],
            'time': df_dict['Time'],
            'type': df_dict['Type'],
            'duration': df_dict['Duration'],
            'img': df_dict['Img'],
            'coverBg': df_dict['CoverBg'],
            'movieDesc': df_dict['movieDesc'],
            'released': df_dict['Released'],
            'genre': ast.literal_eval(df_dict['Genre']),
            'casts': ast.literal_eval(df_dict['Casts']),
            'country': pycountry.countries.get(alpha_2=df_dict['Country'].upper()).name,
            'production': ast.literal_eval(df_dict['Production']),
            'imdb': df_dict['IMDB_rating']
        }

    def genreList_extractor(self):
        query = "SELECT DISTINCT `Genre` FROM `movies`"
        df = pd.read_sql(query, self.conn)
        genres = df['Genre'].apply(ast.literal_eval).explode()
        return genres.unique()

    def countryList_extractor(self):
        query = """
        SELECT `Country`, COUNT(*) as country_count 
        FROM `movies`
        GROUP BY `Country`
        ORDER BY country_count DESC
        LIMIT 40
        """
        df = pd.read_sql(query, self.conn)
        country_codes = df['Country'].tolist()
        return [pycountry.countries.get(alpha_2=code).name if pycountry.countries.get(alpha_2=code) else f"Unknown ({code})" for code in country_codes]

    def productionList_extractor(self):
        query = """
        SELECT `Production`, COUNT(*) as production_count 
        FROM `movies`
        GROUP BY `Production`
        ORDER BY production_count DESC
        LIMIT 30
        """
        df = pd.read_sql(query, self.conn)
        productions = df['Production'].apply(ast.literal_eval).explode()
        return productions.unique()
